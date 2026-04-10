"""
Custom adapters for django-allauth
Handles user account and social account creation/updates
"""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from .models import CustomerProfile, CustomerNotification, CustomerWishlist


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter for regular Django auth and allauth account management"""
    
    def save_user(self, request, sociallogin, form=None):
        """Save user and create associated customer profile"""
        user = super().save_user(request, sociallogin, form)
        request.user = user
        return user
    
    def populate_user(self, request, sociallogin, data):
        """Populate user instance with data from social provider or form"""
        user = super().populate_user(request, sociallogin, data)
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter for social account (Google OAuth) management"""
    
    def save_user(self, request, sociallogin):
        """Save user from social login and create customer profile"""
        user = super().save_user(request, sociallogin)
        
        # Create or update customer profile
        customer_profile, created = CustomerProfile.objects.get_or_create(user=user)
        
        if created:
            # Set profile data from social account
            extra_data = sociallogin.account.extra_data
            
            customer_profile.first_name = extra_data.get('given_name', user.first_name or '')
            customer_profile.last_name = extra_data.get('family_name', user.last_name or '')
            customer_profile.shopify_email = user.email
            customer_profile.oauth_provider = 'google'
            customer_profile.marketing_consent = False
            customer_profile.save()
            
            # Create notification preferences
            CustomerNotification.objects.create(customer=customer_profile)
            
            # Create empty wishlist
            CustomerWishlist.objects.create(customer=customer_profile)
        
        return user
    
    def pre_social_login(self, request, sociallogin):
        """Before social login, handle any necessary setup"""
        # Check if user already exists
        if sociallogin.is_existing:
            return
        
        # Optional: If email matches existing user, connect the accounts
        if 'email' in sociallogin.account.extra_data:
            email = sociallogin.account.extra_data['email']
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
    
    def populate_user(self, request, sociallogin, data):
        """Populate user instance from social account data"""
        user = super().populate_user(request, sociallogin, data)
        
        # Set additional user data from Google
        if 'given_name' in data:
            user.first_name = data['given_name']
        if 'family_name' in data:
            user.last_name = data['family_name']
        
        return user
