"""
SEO Middleware for Final Whistle Clothing
Handles SEO-related headers and response optimization
"""

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils import translation


class SEOHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add SEO-friendly headers to all responses
    """
    
    def process_response(self, request, response):
        """Add SEO headers to response"""
        
        # X-Content-Type-Options prevents MIME type sniffing
        response["X-Content-Type-Options"] = "nosniff"
        
        # X-Frame-Options prevents clickjacking
        if "X-Frame-Options" not in response:
            response["X-Frame-Options"] = "DENY"
        
        # Enables XSS protection in older browsers
        response["X-XSS-Protection"] = "1; mode=block"
        
        # Controls referrer information
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions policy (formerly Feature-Policy)
        response["Permissions-Policy"] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )
        
        # Controls DNS prefetching
        response["X-DNS-Prefetch-Control"] = "on"
        
        # Cache control for static assets
        if request.path.startswith("/static/"):
            response["Cache-Control"] = "public, max-age=31536000, immutable"
        # Cache control for HTML pages (shorter cache, allow validation)
        elif response.get("Content-Type", "").startswith("text/html"):
            response["Cache-Control"] = "public, max-age=3600, must-revalidate"
        
        return response


class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware to handle language preferences
    Stores language preference in session and sets proper lang attribute
    """
    
    def process_request(self, request):
        """Extract and store language preference"""

        # Keep Django admin interface in English regardless of user/session settings.
        if request.path.startswith("/admin/"):
            request.fwc_lang = "en"
            request.LANGUAGE_CODE = "en"
            translation.activate("en")
            return None
        
        # Get language from GET parameter, session, or accept-language header
        lang = request.GET.get("lang")
        
        if lang:
            request.session["fwc_lang"] = lang
        else:
            lang = request.session.get("fwc_lang", self._get_default_language(request))
        
        # Store in request for use in templates
        request.fwc_lang = lang
        request.LANGUAGE_CODE = lang
        translation.activate(lang)
        
        return None
    
    def _get_default_language(self, request):
        """
        Determine default language from Accept-Language header
        Falls back to English (en) if not recognized
        """
        return "en"


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware for Content Security Policy and other security headers
    """
    
    def process_response(self, request, response):
        """Add security headers for better crawlability and protection"""
        
        # Strict-Transport-Security (HTTPS enforcement)
        if not settings.DEBUG:
            response["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # Content Security Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' fonts.googleapis.com fonts.gstatic.com",
            "style-src 'self' 'unsafe-inline' fonts.googleapis.com",
            "font-src 'self' fonts.gstatic.com",
            "img-src 'self' data: https:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        
        if not settings.DEBUG:
            csp_directive = "; ".join(csp_directives)
            response["Content-Security-Policy"] = csp_directive
        
        return response


class PasswordResetRateLimitMiddleware(MiddlewareMixin):
    """Throttle password-reset POST attempts to reduce abuse."""

    def process_request(self, request):
        if request.method != "POST":
            return None

        if not request.path.startswith("/accounts/password/reset/"):
            return None

        max_attempts = max(1, int(getattr(settings, "AUTH_PASSWORD_RESET_MAX_ATTEMPTS", 5)))
        window_seconds = max(1, int(getattr(settings, "AUTH_RATE_LIMIT_WINDOW_SECONDS", 300)))
        email = (request.POST.get("email") or "").strip().lower()[:120]
        client_ip = self._client_ip(request)
        cache_key = f"auth_rl:password_reset:{client_ip}:{email or 'anonymous'}"

        attempts = int(cache.get(cache_key, 0) or 0)
        if attempts >= max_attempts:
            return HttpResponse(
                "Too many password reset attempts. Please try again in a few minutes.",
                status=429,
                content_type="text/plain",
            )

        cache.set(cache_key, attempts + 1, timeout=window_seconds)
        return None

    @staticmethod
    def _client_ip(request):
        forwarded_for = (request.META.get("HTTP_X_FORWARDED_FOR") or "").strip()
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return (request.META.get("REMOTE_ADDR") or "unknown").strip()
