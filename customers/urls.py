"""
URLs for customer authentication and profile management
"""

from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='customer_register'),
    path('login/', views.login_view, name='customer_login'),
    path('logout/', views.logout_view, name='customer_logout'),
    
    # Profile
    path('profile/', views.profile_view, name='customer_profile'),
    path('profile/edit/', views.profile_edit_view, name='customer_profile_edit'),
    
    # Addresses
    path('addresses/', views.addresses_view, name='customer_addresses'),
    path('addresses/add/', views.add_address_view, name='customer_add_address'),
    
    # Orders
    path('orders/', views.orders_view, name='customer_orders'),
    path('orders/<int:order_id>/', views.order_detail_view, name='customer_order_detail'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='customer_wishlist'),
    path('wishlist/add/', views.wishlist_add_view, name='customer_wishlist_add'),
    path('wishlist/remove/', views.wishlist_remove_view, name='customer_wishlist_remove'),

    # Password reset shortcuts to allauth flow
    path('password/reset/', RedirectView.as_view(url='/accounts/password/reset/', permanent=False), name='customer_password_reset'),
    
    # Notifications
    path('notifications/', views.notifications_view, name='customer_notifications'),
    
    # Settings
    path('settings/', views.account_settings_view, name='customer_settings'),
]
