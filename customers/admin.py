import csv
from datetime import timedelta
from decimal import Decimal

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

try:
    from allauth.account.models import EmailAddress
except Exception:  # pragma: no cover - safety fallback for environments without allauth
    EmailAddress = None

from .models import (
    CustomerProfile,
    CustomerAddress,
    CustomerOrder,
    CustomerWishlist,
    CustomerNotification,
)


class RecentCustomerFilter(admin.SimpleListFilter):
    title = 'new customers'
    parameter_name = 'recent_customers'

    def lookups(self, request, model_admin):
        return (
            ('7d', 'Last 7 days'),
            ('30d', 'Last 30 days'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == '7d':
            return queryset.filter(account_created__gte=now - timedelta(days=7))
        if self.value() == '30d':
            return queryset.filter(account_created__gte=now - timedelta(days=30))
        return queryset


class ProfileDataQualityFilter(admin.SimpleListFilter):
    title = 'profile data quality'
    parameter_name = 'profile_quality'

    def lookups(self, request, model_admin):
        return (
            ('clean', 'Complete profile'),
            ('empty', 'Missing required profile data'),
            ('unverified', 'Unverified email'),
        )

    def queryset(self, request, queryset):
        missing_profile_q = (
            Q(first_name='')
            | Q(last_name='')
            | Q(phone='')
            | Q(city='')
            | Q(postal_code='')
        )

        if self.value() == 'clean':
            qs = queryset.exclude(missing_profile_q)
            if EmailAddress is not None:
                qs = qs.filter(user__emailaddress__verified=True)
            return qs.distinct()

        if self.value() == 'empty':
            return queryset.filter(missing_profile_q)

        if self.value() == 'unverified' and EmailAddress is not None:
            return queryset.exclude(user__emailaddress__verified=True).distinct()

        return queryset


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    change_list_template = 'admin/customers/customerprofile/change_list.html'
    list_display = (
        'user_email',
        'full_name',
        'phone',
        'country',
        'oauth_provider_display',
        'email_verification_status',
        'profile_quality_badge',
        'newsletter_subscription',
        'account_created',
    )
    list_filter = (
        RecentCustomerFilter,
        ProfileDataQualityFilter,
        'oauth_provider',
        'newsletter_subscription',
        'marketing_consent',
        'preferred_language',
        'account_created',
    )
    search_fields = (
        'user__email',
        'first_name',
        'last_name',
        'phone',
        'shopify_customer_id',
    )
    readonly_fields = (
        'user',
        'email',
        'account_created',
        'account_updated',
        'last_login_ip',
    )
    actions = ('export_profiles_csv',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'export-all-csv/',
                self.admin_site.admin_view(self.export_all_profiles_csv_view),
                name='customers_customerprofile_export_all_csv',
            ),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'email', 'first_name', 'last_name', 'phone')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'preferred_language')
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'postal_code', 'country')
        }),
        ('Shopify Integration', {
            'fields': ('shopify_customer_id', 'shopify_email'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('newsletter_subscription', 'marketing_consent')
        }),
        ('OAuth', {
            'fields': ('oauth_provider',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('last_login_ip', 'account_created', 'account_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def oauth_provider_display(self, obj):
        colors = {'google': '#4285F4', 'email': '#555'}
        color = colors.get(obj.oauth_provider, '#999')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_oauth_provider_display()
        )
    oauth_provider_display.short_description = 'Provider'

    def email_verification_status(self, obj):
        if EmailAddress is None:
            return format_html('<span style="color: #999;">Unknown</span>')

        is_verified = EmailAddress.objects.filter(user=obj.user, verified=True).exists()
        if is_verified:
            return format_html('<span style="color: #E6E6E6; font-weight: bold;">Verified</span>')
        return format_html('<span style="color: #cc5500; font-weight: bold;">Unverified</span>')
    email_verification_status.short_description = 'Email Status'

    def profile_quality_badge(self, obj):
        missing = any([
            not obj.first_name,
            not obj.last_name,
            not obj.phone,
            not obj.city,
            not obj.postal_code,
        ])
        if missing:
            return format_html('<span style="color: #cc5500; font-weight: bold;">Needs Attention</span>')
        return format_html('<span style="color: #E6E6E6; font-weight: bold;">Complete</span>')
    profile_quality_badge.short_description = 'Data Check'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        now = timezone.now()
        qs = self.get_queryset(request)
        extra_context['new_customers_7_days'] = qs.filter(account_created__gte=now - timedelta(days=7)).count()
        extra_context['new_customers_30_days'] = qs.filter(account_created__gte=now - timedelta(days=30)).count()
        extra_context['total_customers'] = qs.count()
        extra_context['export_all_profiles_url'] = reverse('admin:customers_customerprofile_export_all_csv')
        return super().changelist_view(request, extra_context=extra_context)

    def _export_profiles_to_csv_response(self, queryset, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow([
            'user_id', 'email', 'first_name', 'last_name', 'phone', 'country',
            'preferred_language', 'newsletter_subscription', 'marketing_consent',
            'oauth_provider', 'account_created',
        ])

        for profile in queryset.select_related('user'):
            writer.writerow([
                profile.user_id,
                profile.user.email,
                profile.first_name,
                profile.last_name,
                profile.phone,
                profile.country,
                profile.preferred_language,
                profile.newsletter_subscription,
                profile.marketing_consent,
                profile.oauth_provider,
                profile.account_created.isoformat() if profile.account_created else '',
            ])
        return response

    @admin.action(description='Export selected profiles to CSV')
    def export_profiles_csv(self, request, queryset):
        return self._export_profiles_to_csv_response(queryset, 'customer_profiles_selected.csv')

    def export_all_profiles_csv_view(self, request):
        queryset = self.get_queryset(request)
        return self._export_profiles_to_csv_response(queryset, 'customer_profiles_all.csv')


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = (
        'customer_email',
        'address_type',
        'full_address_display',
        'is_default',
        'created_at',
    )
    list_filter = ('address_type', 'is_default', 'country', 'created_at')
    search_fields = (
        'customer__user__email',
        'first_name',
        'last_name',
        'street_address',
        'city',
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = ('export_addresses_csv',)
    fieldsets = (
        ('Address Type', {
            'fields': ('customer', 'address_type', 'is_default')
        }),
        ('Recipient', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('street_address', 'apartment_suite', 'postal_code', 'city', 'country')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'export-all-csv/',
                self.admin_site.admin_view(self.export_all_addresses_csv_view),
                name='customers_customeraddress_export_all_csv',
            ),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'customer__user')
    
    def customer_email(self, obj):
        return obj.customer.user.email
    customer_email.short_description = 'Customer Email'
    
    def full_address_display(self, obj):
        return obj.get_full_address()[:50] + '...' if len(obj.get_full_address()) > 50 else obj.get_full_address()
    full_address_display.short_description = 'Address'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_all_addresses_url'] = reverse('admin:customers_customeraddress_export_all_csv')
        return super().changelist_view(request, extra_context=extra_context)

    def _export_addresses_to_csv_response(self, queryset, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow([
            'customer_email', 'address_type', 'first_name', 'last_name', 'email', 'phone',
            'street_address', 'apartment_suite', 'postal_code', 'city', 'country',
            'is_default', 'created_at',
        ])

        for address in queryset.select_related('customer', 'customer__user'):
            writer.writerow([
                address.customer.user.email,
                address.get_address_type_display(),
                address.first_name,
                address.last_name,
                address.email,
                address.phone,
                address.street_address,
                address.apartment_suite,
                address.postal_code,
                address.city,
                address.country,
                'Yes' if address.is_default else 'No',
                address.created_at.isoformat() if address.created_at else '',
            ])
        return response

    @admin.action(description='Export selected addresses to CSV')
    def export_addresses_csv(self, request, queryset):
        return self._export_addresses_to_csv_response(queryset, 'customer_addresses_selected.csv')

    def export_all_addresses_csv_view(self, request):
        queryset = self.get_queryset(request)
        return self._export_addresses_to_csv_response(queryset, 'customer_addresses_all.csv')


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    change_list_template = 'admin/customers/customerorder/change_list.html'
    list_display = (
        'shopify_order_number',
        'customer_email',
        'status_display',
        'total_price_display',
        'ordered_at',
        'items_count',
    )
    list_filter = (
        'status',
        'currency',
        'ordered_at',
    )
    search_fields = (
        'customer__user__email',
        'shopify_order_id',
        'shopify_order_number',
    )
    readonly_fields = (
        'customer',
        'shopify_order_id',
        'created_at',
        'updated_at',
    )
    actions = ('export_orders_csv',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'export-all-csv/',
                self.admin_site.admin_view(self.export_all_orders_csv_view),
                name='customers_customerorder_export_all_csv',
            ),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'customer__user')
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'shopify_order_id', 'shopify_order_number')
        }),
        ('Status & Details', {
            'fields': ('status', 'total_price', 'currency', 'items_count')
        }),
        ('Timeline', {
            'fields': ('ordered_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
        ('Shopify Data', {
            'fields': ('items_data',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def customer_email(self, obj):
        return obj.customer.user.email
    customer_email.short_description = 'Customer'
    
    def status_display(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#4285F4',
            'shipped': '#0066cc',
            'delivered': '#E6E6E6',
            'cancelled': '#FF0000',
            'refunded': '#FF6600',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def total_price_display(self, obj):
        return f"{obj.currency} {obj.total_price}"
    total_price_display.short_description = 'Total'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        queryset = self.get_queryset(request)
        status_counts = (
            queryset
            .values('status')
            .annotate(total=Count('id'))
            .order_by('status')
        )
        extra_context['order_status_counts'] = list(status_counts)
        aggregates = queryset.aggregate(
            total_orders=Count('id'),
            total_items=Sum('items_count'),
            sales_revenue=Sum('total_price'),
        )
        extra_context['total_orders'] = aggregates.get('total_orders') or 0
        extra_context['total_items'] = aggregates.get('total_items') or 0
        extra_context['sales_revenue'] = aggregates.get('sales_revenue') or Decimal('0.00')
        extra_context['sales_currency'] = 'EUR'
        recent_queryset = queryset.filter(ordered_at__gte=timezone.now() - timedelta(days=30))
        recent_revenue = recent_queryset.aggregate(total=Sum('total_price')).get('total') or Decimal('0.00')
        extra_context['revenue_30_days'] = recent_revenue

        if request.GET.get('show_status_summary') == '1':
            summary = ', '.join([f"{row['status']}: {row['total']}" for row in status_counts]) or 'No orders yet'
            self.message_user(request, f"Orders by status - {summary}", level=messages.INFO)

        extra_context['export_all_orders_url'] = reverse('admin:customers_customerorder_export_all_csv')

        return super().changelist_view(request, extra_context=extra_context)

    def _export_orders_to_csv_response(self, queryset, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow([
            'order_number', 'shopify_order_id', 'customer_email', 'status',
            'total_price', 'currency', 'items_count', 'ordered_at',
        ])

        for order in queryset.select_related('customer', 'customer__user'):
            writer.writerow([
                order.shopify_order_number,
                order.shopify_order_id,
                order.customer.user.email,
                order.status,
                order.total_price,
                order.currency,
                order.items_count,
                order.ordered_at.isoformat() if order.ordered_at else '',
            ])
        return response

    @admin.action(description='Export selected orders to CSV')
    def export_orders_csv(self, request, queryset):
        return self._export_orders_to_csv_response(queryset, 'customer_orders_selected.csv')

    def export_all_orders_csv_view(self, request):
        queryset = self.get_queryset(request)
        return self._export_orders_to_csv_response(queryset, 'customer_orders_all.csv')


@admin.register(CustomerWishlist)
class CustomerWishlistAdmin(admin.ModelAdmin):
    list_display = (
        'customer_email',
        'item_count',
        'updated_at',
    )
    list_filter = ('updated_at', 'created_at')
    search_fields = ('customer__user__email',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ('export_wishlists_csv',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'export-all-csv/',
                self.admin_site.admin_view(self.export_all_wishlists_csv_view),
                name='customers_customerwishlist_export_all_csv',
            ),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'customer__user')
    
    def customer_email(self, obj):
        return obj.customer.user.email
    customer_email.short_description = 'Customer'
    
    def item_count(self, obj):
        return len(obj.items) if obj.items else 0
    item_count.short_description = 'Items'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_all_wishlists_url'] = reverse('admin:customers_customerwishlist_export_all_csv')
        return super().changelist_view(request, extra_context=extra_context)

    def _export_wishlists_to_csv_response(self, queryset, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow([
            'customer_email', 'item_count', 'items', 'updated_at', 'created_at',
        ])

        for wishlist in queryset.select_related('customer', 'customer__user'):
            items_str = '; '.join([str(item) for item in wishlist.items]) if wishlist.items else ''
            writer.writerow([
                wishlist.customer.user.email,
                len(wishlist.items) if wishlist.items else 0,
                items_str,
                wishlist.updated_at.isoformat() if wishlist.updated_at else '',
                wishlist.created_at.isoformat() if wishlist.created_at else '',
            ])
        return response

    @admin.action(description='Export selected wishlists to CSV')
    def export_wishlists_csv(self, request, queryset):
        return self._export_wishlists_to_csv_response(queryset, 'customer_wishlists_selected.csv')

    def export_all_wishlists_csv_view(self, request):
        queryset = self.get_queryset(request)
        return self._export_wishlists_to_csv_response(queryset, 'customer_wishlists_all.csv')


@admin.register(CustomerNotification)
class CustomerNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'customer_email',
        'email_order_updates',
        'email_promotional',
        'email_newsletter',
        'newsletter_frequency',
    )
    list_filter = (
        'email_order_updates',
        'email_promotional',
        'email_newsletter',
        'newsletter_frequency',
    )
    search_fields = ('customer__user__email',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Customer', {
            'fields': ('customer',)
        }),
        ('Email Notifications', {
            'fields': (
                'email_order_updates',
                'email_promotional',
                'email_newsletter',
                'email_product_reviews',
            )
        }),
        ('Newsletter', {
            'fields': ('newsletter_frequency',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def customer_email(self, obj):
        return obj.customer.user.email
    customer_email.short_description = 'Customer'


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    extra = 0
    fields = (
        'first_name',
        'last_name',
        'phone',
        'country',
        'preferred_language',
        'newsletter_subscription',
        'marketing_consent',
        'oauth_provider',
    )


class CustomUserAdmin(UserAdmin):
    inlines = [CustomerProfileInline]
    list_display = UserAdmin.list_display + ('is_staff',)


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
