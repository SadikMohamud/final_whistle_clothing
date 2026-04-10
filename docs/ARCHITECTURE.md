# Architecture

## 1. System Overview

Final Whistle Clothing is a Django monolith optimized for rapid product iteration and low operational overhead.

Key characteristics:

1. Single deployable web app.
2. Server-rendered templates for storefront and account pages.
3. App-level modularity through Django apps.
4. Environment-driven configuration for development versus production.

## 2. High-Level Components

1. Django Core
	1. URL routing.
	2. Middleware pipeline.
	3. Template rendering.
	4. ORM and migrations.
2. Shop app
	1. Home/landing rendering.
	2. Homepage card CMS model and admin.
	3. Static assets (CSS/JS).
3. Customers app
	1. Profile lifecycle and preferences.
	2. Address and order records.
	3. Auth-adjacent user flows.
4. Authentication stack
	1. Django auth.
	2. allauth social integration.
5. Storage layer
	1. SQLite for local development.
	2. Optional Cloudinary for media in production.
6. Delivery layer
	1. Gunicorn process model.
	2. WhiteNoise static file delivery.
	3. Heroku dyno runtime.

## 3. Request Lifecycle

1. Client sends request to route.
2. Middleware chain executes:
	1. Security/session/csrf handling.
	2. Language and request context handling.
3. URL resolver maps request to view.
4. View composes context from models and settings.
5. Template rendered to HTML.
6. Response middleware applies headers.
7. Response returned to client.

## 4. Data Domains

### 4.1 Identity and Account

1. User credentials and session state.
2. Social login identity mapping.
3. Email verification status.

### 4.2 Customer Profile

1. Names and contact information.
2. Preferences and consent fields.
3. Address records.

### 4.3 Commerce and Content

1. Homepage merchandising cards.
2. Customer order snapshots.
3. Wishlist and notification preference data.

## 5. Template and Frontend Strategy

1. Server-rendered HTML templates.
2. One primary site stylesheet and script bundle.
3. i18n string replacement using client-side dictionary.
4. Mobile-first responsive behavior.

## 6. Configuration Strategy

Configuration is controlled by environment variables, not hardcoded constants.

Primary categories:

1. Security: secret key, debug flag, allowed hosts.
2. Deployment: site URL, trusted origins.
3. Integrations: OAuth, Cloudinary, optional storefront APIs.

## 7. Security Architecture

1. CSRF middleware active for state-changing requests.
2. Host header validation in production.
3. Trusted origins for HTTPS POST workflows.
4. Secret material isolated to environment variables.
5. Admin restricted to authenticated privileged users.

## 8. SEO and Discoverability Architecture

1. robots endpoint served dynamically.
2. sitemap endpoint served dynamically.
3. metadata populated in templates.
4. structured data embedded in page templates.

## 9. Deployment Architecture (Heroku)

1. Git push triggers buildpack pipeline.
2. Dependencies installed from requirements.txt.
3. collectstatic runs at build/release time.
4. Gunicorn boots app from wsgi module.
5. Dyno serves traffic behind Heroku router.

## 10. Reliability Considerations

1. Keep migrations backward compatible where possible.
2. Protect against missing static references when manifest storage is enabled.
3. Ensure admin and auth routes are included in smoke tests every release.
4. Use small, reversible deployment increments.

## 11. Observability and Operations

1. Use Heroku logs for runtime exceptions.
2. Track release numbers and outcomes.
3. Maintain a release checklist and rollback plan.

## 12. Future Evolution Path

1. Introduce CI pipeline for automatic checks and tests.
2. Add structured test suite by domain.
3. Split settings into base/dev/prod modules if complexity grows.
4. Consider managed PostgreSQL as default for all non-local environments.

