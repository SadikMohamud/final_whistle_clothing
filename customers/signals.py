"""
Django signals for customer management
Automatically creates CustomerProfile and related objects
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import (
    CustomerProfile,
    CustomerNotification,
    CustomerWishlist,
)


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """
    Signal to create CustomerProfile when User is created
    """
    if created:
        # Check if profile already exists
        if not hasattr(instance, 'customer_profile'):
            profile = CustomerProfile.objects.create(
                user=instance,
                shopify_email=instance.email,
            )
            
            # Create default notification preferences
            CustomerNotification.objects.create(customer=profile)
            
            # Create empty wishlist
            CustomerWishlist.objects.create(customer=profile)


@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    """
    Signal to update CustomerProfile when User is updated
    """
    try:
        if instance.customer_profile:
            instance.customer_profile.save()
    except CustomerProfile.DoesNotExist:
        pass
