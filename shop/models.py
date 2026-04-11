from django.db import models


class HomepageCard(models.Model):
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=255, blank=True)
    price_label = models.CharField(max_length=64, blank=True)
    cta_url = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='homepage/cards/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_hero = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    source = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
