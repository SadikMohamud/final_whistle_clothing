from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
	path("admin/", admin.site.urls),
	# Force allauth login/signup entrypoints to use the custom customer auth pages.
	path("accounts/login/", RedirectView.as_view(pattern_name="customer_login", permanent=False)),
	path("accounts/signup/", RedirectView.as_view(pattern_name="customer_register", permanent=False)),
	path("accounts/", include("allauth.urls")),
	path("account/", include("customers.urls")),
	path("", include("shop.urls")),
]

# Serve media files in development
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

