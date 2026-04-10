from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("story/", views.story_view, name="story"),
    path("api/products/", views.products_api, name="products_api"),
    path("products/<slug:handle>/", views.product_detail, name="product_detail"),
    path("collections/<slug:slug>/", views.collection_view, name="collection_view"),
    path("search/", views.search_view, name="search"),
    path("checkout/shopify/", views.shopify_checkout, name="shopify_checkout"),
    path("newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("webhooks/shopify/orders/create", views.shopify_orders_create_webhook, name="shopify_orders_create_webhook"),
    path("webhooks/shopify/orders/updated", views.shopify_orders_updated_webhook, name="shopify_orders_updated_webhook"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
]

