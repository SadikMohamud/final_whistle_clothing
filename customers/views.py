"""
Views for customer authentication and profile management
"""

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.cache import never_cache
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from allauth.socialaccount.models import SocialAccount, SocialApp

from .models import (
    CustomerProfile,
    CustomerAddress,
    CustomerOrder,
    CustomerWishlist,
    CustomerNotification,
)
from .address_formats import get_address_format, get_browser_language_to_country


def _client_ip(request) -> str:
    forwarded_for = (request.META.get('HTTP_X_FORWARDED_FOR') or '').strip()
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return (request.META.get('REMOTE_ADDR') or 'unknown').strip()


def _rate_limit_key(prefix: str, request, identifier: str = '') -> str:
    client_ip = _client_ip(request)
    normalized_identifier = (identifier or '').strip().lower()[:120]
    if normalized_identifier:
        return f"auth_rl:{prefix}:{client_ip}:{normalized_identifier}"
    return f"auth_rl:{prefix}:{client_ip}"


def _too_many_attempts(key: str, max_attempts: int) -> bool:
    attempts = int(cache.get(key, 0) or 0)
    return attempts >= max_attempts


def _record_auth_failure(key: str) -> int:
    attempts = int(cache.get(key, 0) or 0) + 1
    cache.set(key, attempts, timeout=max(1, int(settings.AUTH_RATE_LIMIT_WINDOW_SECONDS)))
    return attempts


def _clear_auth_failures(key: str) -> None:
    cache.delete(key)


@never_cache
def register_view(request):
    """User registration with email"""
    google_social_app = SocialApp.objects.filter(provider='google').exists()

    if request.user.is_authenticated:
        return redirect('customer_profile')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        rate_limit_key = _rate_limit_key('register', request, email or 'anonymous')
        max_register_attempts = max(1, int(getattr(settings, 'AUTH_REGISTER_MAX_ATTEMPTS', 6)))

        if _too_many_attempts(rate_limit_key, max_register_attempts):
            return render(request, 'customers/signup.html', {
                'errors': ['Too many signup attempts. Please try again in a few minutes.'],
                'email': email,
                'first_name': request.POST.get('first_name', '').strip(),
                'last_name': request.POST.get('last_name', '').strip(),
                'google_social_app': google_social_app,
            }, status=429)

        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        # Validation
        errors = []
        
        if not email:
            errors.append('Email is required')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered')
        
        if not password:
            errors.append('Password is required')
        else:
            try:
                temp_user = User(username=email, email=email, first_name=first_name, last_name=last_name)
                validate_password(password, temp_user)
            except ValidationError as exc:
                errors.extend(exc.messages)
        
        if password != password_confirm:
            errors.append('Passwords do not match')
        
        if errors:
            attempts = _record_auth_failure(rate_limit_key)
            if attempts >= max_register_attempts:
                errors = ['Too many signup attempts. Please try again in a few minutes.']
            return render(request, 'customers/signup.html', {
                'errors': errors,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'google_social_app': google_social_app,
            }, status=429 if attempts >= max_register_attempts else 200)
        
        # Create user
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                
                # Update customer profile
                profile = user.customer_profile
                profile.first_name = first_name
                profile.last_name = last_name
                profile.shopify_email = email
                profile.oauth_provider = 'email'
                profile.save()

            _clear_auth_failures(rate_limit_key)

            return render(request, 'customers/email_confirm.html', {
                'email': email,
            })
        
        except Exception as e:
            attempts = _record_auth_failure(rate_limit_key)
            errors.append('Registration failed. Please try again.')
            if attempts >= max_register_attempts:
                errors = ['Too many signup attempts. Please try again in a few minutes.']
            return render(request, 'customers/signup.html', {
                'errors': errors,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'google_social_app': google_social_app,
            }, status=429 if attempts >= max_register_attempts else 200)

    return render(request, 'customers/signup.html', {
        'google_social_app': google_social_app,
    })


@never_cache
def login_view(request):
    """User login with email/password"""
    google_social_app = SocialApp.objects.filter(provider='google').exists()

    # Allow forcing the login screen from navbar/account links.
    force_login = request.GET.get('force') == '1'

    if request.user.is_authenticated and not force_login:
        return redirect('customer_profile')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        rate_limit_key = _rate_limit_key('login', request, email or 'anonymous')
        max_login_attempts = max(1, int(getattr(settings, 'AUTH_LOGIN_MAX_ATTEMPTS', 5)))

        if _too_many_attempts(rate_limit_key, max_login_attempts):
            return render(request, 'customers/login.html', {
                'error': 'Too many login attempts. Please try again in a few minutes.',
                'email': email,
                'google_social_app': google_social_app,
            }, status=429)

        password = request.POST.get('password', '')
        
        user = authenticate(username=email, password=password)
        
        if user is not None:
            _clear_auth_failures(rate_limit_key)
            login(request, user)
            next_url = request.GET.get('next', 'customer_profile')
            return redirect(next_url)
        else:
            attempts = _record_auth_failure(rate_limit_key)
            error_message = 'Invalid email or password'
            status_code = 200
            if attempts >= max_login_attempts:
                error_message = 'Too many login attempts. Please try again in a few minutes.'
                status_code = 429
            return render(request, 'customers/login.html', {
                'error': error_message,
                'email': email,
                'google_social_app': google_social_app,
            }, status=status_code)

    return render(request, 'customers/login.html', {
        'google_social_app': google_social_app,
    })


@login_required(login_url='customer_login')
def profile_view(request):
    """Customer profile dashboard"""
    profile = request.user.customer_profile
    addresses = profile.addresses.all()
    orders = profile.orders.all()[:10]  # Last 10 orders
    notifications = profile.notifications
    wishlist = profile.wishlist
    
    # Check if user has social auth
    social_account = None
    try:
        social_account = SocialAccount.objects.get(user=request.user)
    except SocialAccount.DoesNotExist:
        pass
    
    context = {
        'profile': profile,
        'addresses': addresses,
        'orders': orders,
        'notifications': notifications,
        'wishlist': wishlist,
        'social_account': social_account,
        'auth_methods': {
            'email': True,
            'google': social_account is not None and social_account.provider == 'google',
        }
    }
    
    return render(request, 'customers/profile.html', context)


@login_required(login_url='customer_login')
def profile_edit_view(request):
    """Edit customer profile"""
    profile = request.user.customer_profile
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update user
                request.user.first_name = request.POST.get('first_name', '')
                request.user.last_name = request.POST.get('last_name', '')
                request.user.save()
                
                # Update profile
                profile.first_name = request.POST.get('first_name', '')
                profile.last_name = request.POST.get('last_name', '')
                profile.phone = request.POST.get('phone', '')
                profile.street_address = request.POST.get('street_address', '')
                profile.city = request.POST.get('city', '')
                profile.postal_code = request.POST.get('postal_code', '')
                profile.country = request.POST.get('country', 'NL')
                profile.preferred_language = request.POST.get('preferred_language', 'nl')
                profile.newsletter_subscription = request.POST.get('newsletter_subscription') == 'on'
                profile.marketing_consent = request.POST.get('marketing_consent') == 'on'
                profile.save()
                
                return render(request, 'customers/profile.html', {
                    'profile': profile,
                    'message': 'Profile updated successfully!',
                    'message_type': 'success',
                })
        
        except Exception as e:
            return render(request, 'customers/profile_edit.html', {
                'profile': profile,
                'error': f'Failed to update profile: {str(e)}',
            })
    
    return render(request, 'customers/profile_edit.html', {'profile': profile})


@login_required(login_url='customer_login')
def addresses_view(request):
    """Manage customer addresses"""
    profile = request.user.customer_profile
    addresses = profile.addresses.all()
    
    context = {
        'profile': profile,
        'addresses': addresses,
    }
    
    return render(request, 'customers/addresses.html', context)


@login_required(login_url='customer_login')
@require_http_methods(["GET", "POST"])
def add_address_view(request):
    """Add new address with country-specific format"""
    profile = request.user.customer_profile
    
    if request.method == 'GET':
        # Detect user's browser language and country
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'nl-NL')
        browser_language = accept_language.split(',')[0].strip()
        detected_country = get_browser_language_to_country(browser_language)
        address_format = get_address_format(detected_country)
        
        context = {
            'profile': profile,
            'detected_country': detected_country,
            'address_format': address_format,
        }
        return render(request, 'customers/add_address.html', context)
    
    # POST request - create address
    try:
        country = request.POST.get('country', 'NL').upper()
        
        address = CustomerAddress.objects.create(
            customer=profile,
            address_type=request.POST.get('address_type', 'shipping'),
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=request.POST.get('email', request.user.email),
            phone=request.POST.get('phone', ''),
            street_address=request.POST.get('street_address', ''),
            apartment_suite=request.POST.get('apartment_suite', ''),
            city=request.POST.get('city', ''),
            postal_code=request.POST.get('postal_code', ''),
            country=country,
            is_default=request.POST.get('is_default') == 'on',
        )
        
        messages.success(request, 'Address added successfully!')
        return redirect('customer_addresses')
    
    except Exception as e:
        messages.error(request, f'Failed to add address: {str(e)}')
        
        # Re-render form with error
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'nl-NL')
        browser_language = accept_language.split(',')[0].strip()
        detected_country = get_browser_language_to_country(browser_language)
        address_format = get_address_format(detected_country)
        
        context = {
            'profile': profile,
            'detected_country': detected_country,
            'address_format': address_format,
        }
        return render(request, 'customers/add_address.html', context)


@login_required(login_url='customer_login')
def orders_view(request):
    """Customer order history"""
    profile = request.user.customer_profile
    orders = profile.orders.all()
    
    context = {
        'profile': profile,
        'orders': orders,
    }
    
    return render(request, 'customers/orders.html', context)


@login_required(login_url='customer_login')
def order_detail_view(request, order_id):
    """Order detail view"""
    profile = request.user.customer_profile
    
    try:
        order = profile.orders.get(id=order_id)
    except CustomerOrder.DoesNotExist:
        return render(request, 'error.html', {
            'error': 'Order not found',
            'status': 404,
        }, status=404)
    
    context = {
        'profile': profile,
        'order': order,
    }
    
    return render(request, 'customers/order_detail.html', context)


@login_required(login_url='customer_login')
def notifications_view(request):
    """Manage notification preferences"""
    profile = request.user.customer_profile
    notifications = profile.notifications
    
    if request.method == 'POST':
        try:
            notifications.email_order_updates = request.POST.get('email_order_updates') == 'on'
            notifications.email_promotional = request.POST.get('email_promotional') == 'on'
            notifications.email_newsletter = request.POST.get('email_newsletter') == 'on'
            notifications.email_product_reviews = request.POST.get('email_product_reviews') == 'on'
            notifications.newsletter_frequency = request.POST.get('newsletter_frequency', 'weekly')
            notifications.save()
            
            message = 'Notification preferences updated successfully!'
            message_type = 'success'
        
        except Exception as e:
            message = f'Failed to update preferences: {str(e)}'
            message_type = 'error'
        
        return render(request, 'customers/notifications.html', {
            'profile': profile,
            'notifications': notifications,
            'message': message,
            'message_type': message_type,
        })
    
    context = {
        'profile': profile,
        'notifications': notifications,
    }
    
    return render(request, 'customers/notifications.html', context)


@login_required(login_url='customer_login')
def wishlist_view(request):
    """Customer wishlist (placeholder)"""
    profile = request.user.customer_profile
    wishlist = profile.wishlist
    
    # Placeholder: items are Shopify product IDs
    items = wishlist.items if wishlist else []
    
    context = {
        'profile': profile,
        'wishlist': wishlist,
        'items': items,
        'items_count': len(items),
    }
    
    return render(request, 'customers/wishlist.html', context)


@login_required(login_url='customer_login')
@require_POST
def wishlist_add_view(request):
    product_id = request.POST.get('product_id', '').strip()
    if not product_id:
        messages.error(request, 'Missing product identifier.')
        return redirect(request.META.get('HTTP_REFERER', 'customer_wishlist'))

    wishlist = request.user.customer_profile.wishlist
    wishlist.add_item(product_id)
    messages.success(request, 'Item added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'customer_wishlist'))


@login_required(login_url='customer_login')
@require_POST
def wishlist_remove_view(request):
    product_id = request.POST.get('product_id', '').strip()
    if not product_id:
        messages.error(request, 'Missing product identifier.')
        return redirect('customer_wishlist')

    wishlist = request.user.customer_profile.wishlist
    wishlist.remove_item(product_id)
    messages.success(request, 'Item removed from wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'customer_wishlist'))


def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('/')


@login_required(login_url='customer_login')
def account_settings_view(request):
    """Account settings and security"""
    profile = request.user.customer_profile
    
    # Check for social auth
    social_account = None
    try:
        social_account = SocialAccount.objects.get(user=request.user)
    except SocialAccount.DoesNotExist:
        pass
    
    context = {
        'profile': profile,
        'social_account': social_account,
    }
    
    return render(request, 'customers/account_settings.html', context)
