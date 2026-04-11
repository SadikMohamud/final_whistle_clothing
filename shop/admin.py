from django.contrib import admin

from .models import HomepageCard, NewsletterSubscription


@admin.register(HomepageCard)
class HomepageCardAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'is_hero', 'sort_order', 'updated_at')
	list_filter = ('is_active',)
	search_fields = ('title', 'subtitle')
	list_editable = ('is_active', 'is_hero', 'sort_order')
	actions = ('set_as_homepage_hero',)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		if obj.is_hero:
			HomepageCard.objects.exclude(pk=obj.pk).update(is_hero=False)

	@admin.action(description='Set selected card as homepage hero')
	def set_as_homepage_hero(self, request, queryset):
		selected = queryset.order_by('sort_order', '-created_at').first()
		if selected is None:
			return
		HomepageCard.objects.update(is_hero=False)
		HomepageCard.objects.filter(pk=selected.pk).update(is_hero=True)


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
	list_display = ("email", "source", "is_active", "created_at")
	list_filter = ("is_active", "source")
	search_fields = ("email",)

