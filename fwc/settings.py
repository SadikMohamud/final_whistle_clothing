import os
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(path: Path) -> None:
	if not path.exists():
		return

	for raw_line in path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		os.environ.setdefault(key.strip(), value.strip())


_load_env_file(BASE_DIR / ".env")


IS_PRODUCTION = bool(os.getenv("DATABASE_URL") or os.getenv("DYNO"))
default_debug = "False" if IS_PRODUCTION else "True"
DEBUG = os.getenv("DJANGO_DEBUG", default_debug).lower() == "true"

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me" if not IS_PRODUCTION else "").strip()
if IS_PRODUCTION and not SECRET_KEY:
	raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production.")

allowed_hosts_default = "127.0.0.1,localhost" if not IS_PRODUCTION else ""
allowed_hosts_raw = os.getenv("DJANGO_ALLOWED_HOSTS", allowed_hosts_default).strip()
if IS_PRODUCTION and not allowed_hosts_raw:
	raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must be set in production.")
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_raw.split(",") if h.strip()]

INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.sites",
	
	"rest_framework",
	"rest_framework.authtoken",
	"allauth",
	"allauth.account",
	"allauth.socialaccount",
	"allauth.socialaccount.providers.google",
	"dj_rest_auth",
	"dj_rest_auth.registration",
	
	"shop",
	"customers",
	"cloudinary",
	"cloudinary_storage",
]

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"whitenoise.middleware.WhiteNoiseMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"allauth.account.middleware.AccountMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"shop.middleware.SEOHeadersMiddleware",
	"shop.middleware.LanguageMiddleware",
	"shop.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "fwc.urls"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [BASE_DIR / "templates"],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
			],
		},
	},
]

WSGI_APPLICATION = "fwc.wsgi.application"
ASGI_APPLICATION = "fwc.asgi.application"

# Database Configuration
# Priority:
# 1) DATABASE_URL (Heroku / cloud platforms)
# 2) Explicit DB_ENGINE=postgresql and DB_* variables
# 3) Local sqlite fallback
database_url = os.getenv("DATABASE_URL", "").strip()

if database_url:
	parsed_db = urlparse(database_url)
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.postgresql",
			"NAME": parsed_db.path.lstrip("/"),
			"USER": parsed_db.username or "",
			"PASSWORD": parsed_db.password or "",
			"HOST": parsed_db.hostname or "",
			"PORT": str(parsed_db.port or "5432"),
			"CONN_MAX_AGE": 600,
			"CONN_HEALTH_CHECKS": True,
		}
	}
else:
	db_engine = os.getenv("DB_ENGINE", "sqlite3")
	if db_engine == "postgresql":
		DATABASES = {
			"default": {
				"ENGINE": "django.db.backends.postgresql",
				"NAME": os.getenv("DB_NAME", "finalwhistle"),
				"USER": os.getenv("DB_USER", "postgres"),
				"PASSWORD": os.getenv("DB_PASSWORD", ""),
				"HOST": os.getenv("DB_HOST", "localhost"),
				"PORT": os.getenv("DB_PORT", "5432"),
			}
		}
	else:
		DATABASES = {
			"default": {
				"ENGINE": "django.db.backends.sqlite3",
				"NAME": BASE_DIR / "db.sqlite3",
			}
		}

AUTH_PASSWORD_VALIDATORS = [
	{"NAME": "customers.password_validators.CustomerPasswordPolicyValidator"},
	{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
	{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
	{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
	{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Amsterdam"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_FINDERS = [
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1

# Authentication Backends
AUTHENTICATION_BACKENDS = [
	"allauth.account.auth_backends.AuthenticationBackend",
	"django.contrib.auth.backends.ModelBackend",
]

# Django Allauth Settings
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_ADAPTER = "customers.adapters.CustomAccountAdapter"
SOCIALACCOUNT_ADAPTER = "customers.adapters.CustomSocialAccountAdapter"
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# REST Framework Settings  
REST_FRAMEWORK = {
	"DEFAULT_AUTHENTICATION_CLASSES": [
		"rest_framework.authentication.SessionAuthentication",
	],
	"DEFAULT_PERMISSION_CLASSES": [
		"rest_framework.permissions.IsAuthenticatedOrReadOnly",
	],
	"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
	"PAGE_SIZE": 20,
}

# REST Auth Settings
REST_AUTH = {
	"USE_JWT": False,
	"SESSION_LOGIN": True,
	"OLD_PASSWORD_FIELD_ENABLED": True,
}

# Google OAuth Configuration (Placeholder)
SOCIALACCOUNT_PROVIDERS = {
	"google": {
		"SCOPE": [
			"profile",
			"email",
		],
		"AUTH_PARAMS": {
			"prompt": "select_account",
		},
	}
}

# Login/Logout Redirect URLs
LOGIN_REDIRECT_URL = "/account/profile/"
LOGIN_URL = "/account/login/"
LOGOUT_REDIRECT_URL = "/"

# Email configuration
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "").strip()
EMAIL_HOST = os.getenv("EMAIL_HOST", "").strip()
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@finalwhistleclothing.com")

if IS_PRODUCTION and not EMAIL_BACKEND:
	raise ImproperlyConfigured(
		"EMAIL_BACKEND must be explicitly set in production."
	)

if not EMAIL_BACKEND:
	EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if EMAIL_USE_TLS and EMAIL_USE_SSL:
	raise ImproperlyConfigured("EMAIL_USE_TLS and EMAIL_USE_SSL cannot both be True.")

if IS_PRODUCTION and EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
	if not EMAIL_HOST:
		raise ImproperlyConfigured("EMAIL_HOST must be set for SMTP backend in production.")
	if not DEFAULT_FROM_EMAIL:
		raise ImproperlyConfigured("DEFAULT_FROM_EMAIL must be set in production.")

# Security & SEO Headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
if IS_PRODUCTION:
	SECURE_SSL_REDIRECT = True
	SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
	SESSION_COOKIE_SECURE = True
	CSRF_COOKIE_SECURE = True
	SECURE_HSTS_SECONDS = 31536000
	SECURE_HSTS_INCLUDE_SUBDOMAINS = True
	SECURE_HSTS_PRELOAD = True
	SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

csrf_trusted_origins_default = (
	"http://127.0.0.1:8000,http://localhost:8000" if not IS_PRODUCTION else ""
)
CSRF_TRUSTED_ORIGINS = [
	origin.strip()
	for origin in os.getenv(
		"DJANGO_CSRF_TRUSTED_ORIGINS",
		csrf_trusted_origins_default,
	).split(",")
	if origin.strip()
]

if IS_PRODUCTION and not CSRF_TRUSTED_ORIGINS:
	raise ImproperlyConfigured("DJANGO_CSRF_TRUSTED_ORIGINS must be set in production.")

SECURE_CONTENT_SECURITY_POLICY = {
	"default-src": ("'self'",),
	"script-src": ("'self'", "'unsafe-inline'", "fonts.googleapis.com", "fonts.gstatic.com", "accounts.google.com"),
	"style-src": ("'self'", "'unsafe-inline'", "fonts.googleapis.com"),
	"font-src": ("'self'", "fonts.gstatic.com"),
	"img-src": ("'self'", "data:", "https:", "res.cloudinary.com"),
	"connect-src": ("'self'", "accounts.google.com", "accounts.gstatic.com"),
	"frame-src": ("accounts.google.com",),
}

# Cloudinary media storage
CLOUDINARY_STORAGE = {
	"CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME", ""),
	"API_KEY": os.getenv("CLOUDINARY_API_KEY", ""),
	"API_SECRET": os.getenv("CLOUDINARY_API_SECRET", ""),
}

cloud_name = CLOUDINARY_STORAGE["CLOUD_NAME"]
if cloud_name:
	STORAGES = {
		"default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
		"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
	}
	MEDIA_URL = f"https://res.cloudinary.com/{cloud_name}/"
else:
	STORAGES = {
		"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
		"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
	}

# SEO Configuration
SEO_CONFIG = {
	"SITE_NAME": "Final Whistle Clothing",
	"SITE_URL": os.getenv("SITE_URL", "https://finalwhistleclothing.com"),
	"SITE_DESCRIPTION": "Premium Dutch streetwear. Refined everyday pieces with SS26 collection energy.",
	"DEFAULT_IMAGE": "https://placehold.co/1200x630/111111/C8F400?text=Final+Whistle+Clothing",
	"ORGANIZATION": {
		"name": "Final Whistle Clothing",
		"logo": "https://placehold.co/512x512/111111/C8F400?text=FW",
		"url": os.getenv("SITE_URL", "https://finalwhistleclothing.com"),
		"same_as": [
			"https://www.instagram.com/finalwhistleclothing",
			"https://www.tiktok.com/@finalwhistleclothing",
			"https://www.youtube.com/@finalwhistleclothing",
		],
		"contact_email": "contact@finalwhistleclothing.com",
		"address": {
			"country": "NL",
			"locality": "Netherlands",
		},
	},
	"LANGUAGES": {
		"nl": {"name": "Nederlands", "code": "nl_NL"},
		"en": {"name": "English", "code": "en_US"},
	},
}

# Shopify Storefront API settings.
SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "")
SHOPIFY_STOREFRONT_ACCESS_TOKEN = os.getenv("SHOPIFY_STOREFRONT_ACCESS_TOKEN", "")
SHOPIFY_STOREFRONT_API_VERSION = os.getenv("SHOPIFY_STOREFRONT_API_VERSION", "2025-01")
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN", "")
SHOPIFY_WEBHOOK_SECRET = os.getenv("SHOPIFY_WEBHOOK_SECRET", "")

if IS_PRODUCTION and SHOPIFY_STORE_DOMAIN and not SHOPIFY_WEBHOOK_SECRET:
	raise ImproperlyConfigured(
		"SHOPIFY_WEBHOOK_SECRET must be set when Shopify is enabled in production."
	)

