# SEO Quick Start

This document is the shortest path to validating SEO setup in development and production.

## 1. Ten-Minute Setup

1. Confirm SITE_URL in environment variables points to your active domain.
2. Ensure robots and sitemap routes are enabled in URL routing.
3. Ensure homepage template includes canonical, og, twitter, and language tags.
4. Deploy latest code and verify endpoints.

## 2. Must-Pass Validation Commands

```powershell
python manage.py check
python manage.py test
```

## 3. Must-Pass URL Checks

Open and verify status code 200:

1. /robots.txt
2. /sitemap.xml
3. /

Expected outcomes:

1. robots includes sitemap location.
2. sitemap includes canonical absolute URLs.
3. homepage source includes title, description, and social tags.

## 4. Local Verification Script

```powershell
python manage.py shell
```

```python
from django.test import RequestFactory
from shop.views import robots_txt, sitemap_xml

factory = RequestFactory()
print(robots_txt(factory.get('/robots.txt')).status_code)
print(sitemap_xml(factory.get('/sitemap.xml')).status_code)
```

## 5. Production Verification

1. Google Rich Results test for homepage.
2. Schema validator for JSON-LD syntax.
3. PageSpeed Insights for performance baseline.
4. Search Console sitemap submission.

## 6. Minimum Metadata Checklist

1. title tag present.
2. meta description present.
3. canonical link present.
4. og:title, og:description, og:image present.
5. twitter card tags present.
6. language and hreflang tags present.

## 7. Common Fast Fixes

1. Wrong domain in canonical tags:
   1. Correct SITE_URL.
2. Missing schema:
   1. Confirm script block is rendered in template.
3. Missing robots/sitemap in production:
   1. Confirm URL patterns and middleware are deployed.

## 8. What to Read Next

1. docs/SEO_OPTIMIZATION_GUIDE.md for deep implementation details.
2. docs/SEO_COMPLETE_CHECKLIST.md for release checklist.
3. docs/SEO_FINAL_SUMMARY.md for status and roadmap.

