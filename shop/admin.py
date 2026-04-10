from django.contrib import admin

from .models import HomepageCard, NewsletterSubscription


@admin.register(HomepageCard)
class HomepageCardAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'sort_order', 'updated_at')
	list_filter = ('is_active',)
	search_fields = ('title', 'subtitle')
	list_editable = ('is_active', 'sort_order')


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
	list_display = ("email", "source", "is_active", "created_at")
	list_filter = ("is_active", "source")
	search_fields = ("email",)

