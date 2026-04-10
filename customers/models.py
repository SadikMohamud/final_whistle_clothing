"""
Customer profile, address, order, and preference models
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class CustomerProfile(models.Model):
    """Extended user profile with customer-specific data"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('nl', 'Dutch'),
        ('de', 'German'),
        ('fr', 'French'),
    ]
    
    OAUTH_PROVIDER_CHOICES = [
        ('email', 'Email/Password'),
        ('google', 'Google'),
    ]
    
    # User relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    # Personal information
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    # Address information
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=2, default='NL')
    
    # Shopify integration
    shopify_customer_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    shopify_email = models.EmailField(blank=True)
    
    # Preferences
    newsletter_subscription = models.BooleanField(default=True)
    marketing_consent = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    
    # OAuth tracking
    oauth_provider = models.CharField(max_length=20, choices=OAUTH_PROVIDER_CHOICES, default='email')
    account_created = models.DateTimeField(auto_now_add=True)
    account_updated = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-account_created']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['shopify_customer_id']),
        ]
    
    def __str__(self):
        return f"{self.get_display_name()} ({self.user.email})"
    
    @property
    def email(self):
        """Get email from associated user"""
        return self.user.email
    
    @property
    def full_name(self):
        """Get full name from first and last name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_display_name(self):
        """Get name to display (full_name or email)"""
        return self.full_name or self.user.username
    
    def set_oauth_provider(self, provider):
        """Set OAuth provider and save"""
        self.oauth_provider = provider
        self.save(update_fields=['oauth_provider', 'account_updated'])


class CustomerAddress(models.Model):
    """Multiple delivery/billing addresses per customer"""
    
    ADDRESS_TYPE_CHOICES = [
        ('billing', 'Billing Address'),
        ('shipping', 'Shipping Address'),
    ]
    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES)
    is_default = models.BooleanField(default=False)
    
    # Recipient information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Address details
    street_address = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name_plural = "Customer Addresses"
    
    def __str__(self):
        return f"{self.address_type} - {self.first_name} {self.last_name}"
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = [self.street_address]
        if self.apartment_suite:
            parts.append(self.apartment_suite)
        parts.extend([self.postal_code, self.city, self.country])
        return ", ".join(filter(None, parts))


class CustomerOrder(models.Model):
    """Shopify order tracking"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    
    # Shopify identifiers
    shopify_order_id = models.CharField(max_length=255, unique=True)
    shopify_order_number = models.CharField(max_length=20, unique=True)
    
    # Status and financial
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='EUR')
    
    # Timestamps
    ordered_at = models.DateTimeField()
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Shopify data (for future API integration)
    items_count = models.IntegerField(default=0)
    items_data = models.JSONField(default=dict, null=True, blank=True)
    
    class Meta:
        ordering = ['-ordered_at']
        indexes = [
            models.Index(fields=['customer', '-ordered_at']),
            models.Index(fields=['shopify_order_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Order {self.shopify_order_number} - {self.status}"


class CustomerWishlist(models.Model):
    """Saved items/products for future purchase"""
    
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='wishlist')
    items = models.JSONField(default=list, help_text="List of Shopify product IDs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Customer Wishlists"
    
    def __str__(self):
        return f"Wishlist for {self.customer.get_display_name()}"
    
    def add_item(self, product_id):
        """Add item to wishlist"""
        if product_id not in self.items:
            self.items.append(product_id)
            self.save(update_fields=['items', 'updated_at'])
    
    def remove_item(self, product_id):
        """Remove item from wishlist"""
        if product_id in self.items:
            self.items.remove(product_id)
            self.save(update_fields=['items', 'updated_at'])


class CustomerNotification(models.Model):
    """Email notification preferences"""
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('never', 'Never'),
    ]
    
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='notifications')
    
    # Email preferences
    email_order_updates = models.BooleanField(default=True)
    email_promotional = models.BooleanField(default=True)
    email_newsletter = models.BooleanField(default=True)
    email_product_reviews = models.BooleanField(default=True)
    
    # Frequency
    newsletter_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Customer Notifications"
    
    def __str__(self):
        return f"Notifications for {self.customer.get_display_name()}"
