# Final Whistle Clothing

Production-grade Django e-commerce foundation for Final Whistle Clothing, with custom customer flows, admin tooling, SEO infrastructure, and Heroku deployment support.

![Django](https://img.shields.io/badge/Django-5.2.12-black?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.14+-blue?style=flat-square)
![Deployment](https://img.shields.io/badge/Deploy-Heroku-6762a6?style=flat-square)

## 1. Product Overview

This repository contains:

1. A customer-facing storefront with Dutch and English UI support.
2. Custom account experience layered on Django allauth.
3. Admin workflows for customer data quality, order tracking, and CSV exports.
4. Homepage card CMS for content and merchandising control.
5. SEO baseline including robots, sitemap, metadata, and schema-ready templates.
6. Heroku-ready deployment with static asset handling and production settings support.

## 2. Tech Stack

1. Python 3.14+
2. Django 5.2.x
3. Django allauth for identity and social auth
4. Gunicorn for WSGI serving
5. WhiteNoise for static asset delivery
6. Optional Cloudinary for media storage
7. SQLite in local development (PostgreSQL recommended in production)

## 3. Repository Layout

Top-level structure in this workspace includes:

1. settings.py, urls.py, asgi.py, wsgi.py: Django project configuration.
2. manage.py: Django management entrypoint.
3. templates/: application templates (including allauth overrides).
4. shop/: storefront app (views, static assets, models/admin as applicable).
5. customers/: account/profile/order app (views, templates, admin).
6. docs/: engineering and operational documentation.
7. requirements.txt: Python dependency lock list for this project.

## 4. Local Setup

### 4.1 Prerequisites

1. Git
2. Python 3.14+
3. PowerShell (Windows instructions below)

### 4.2 Clone and Virtual Environment

```powershell
git clone <your-repo-url>
cd Final_whistle_clothing
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4.3 Environment Variables

Create a .env file in project root. Never commit this file.

```env
DJANGO_SECRET_KEY=<generate-a-strong-secret>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

SITE_URL=http://127.0.0.1:8000

# Optional Cloudinary
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Optional Google OAuth
GOOGLE_OAUTH2_KEY=
GOOGLE_OAUTH2_SECRET=

# Optional Shopify integration
SHOPIFY_STORE_DOMAIN=
SHOPIFY_STOREFRONT_ACCESS_TOKEN=
SHOPIFY_STOREFRONT_API_VERSION=2025-01
```

Generate a secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4.4 Database and Admin Bootstrapping

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 4.5 Run Locally

```powershell
python manage.py runserver 8000
```

Open:

1. Storefront: http://127.0.0.1:8000/
2. Admin: http://127.0.0.1:8000/admin/

## 5. Testing and Quality Gates

### 5.1 Minimum Pre-Commit Checks

Run these before every commit:

```powershell
python manage.py check
python manage.py test
```

### 5.2 Focused Test Runs

```powershell
python manage.py test customers
python manage.py test shop
```

### 5.3 Optional Coverage Workflow

```powershell
pip install coverage
coverage run manage.py test
coverage report -m
```

Suggested quality target:

1. No failing tests.
2. No system check errors.
3. Coverage trending up release over release.

## 6. Authentication and Accounts

Implemented behaviors:

1. Email/password sign-in and registration.
2. Optional Google OAuth via allauth provider configuration.
3. Custom account routing so user-facing auth pages remain consistent.
4. Customer profile/address/notification pages in app templates.

See docs/AUTH.md for full flow diagrams and troubleshooting.

## 7. Admin and Operations Features

1. Customer profile completeness indicators.
2. Email verification visibility.
3. Customer and order CSV exports.
4. Homepage card content management.
5. Order status overview and management helpers.

## 8. Frontend and Branding Notes

Current design direction is monochrome (black/white neutral palette) with no green accent.

Primary files for storefront styling and behavior:

1. shop/static/shop/css/site.css
2. shop/static/shop/js/site.js
3. templates/finalwhistleclothing.html

## 9. Deployment Summary

Production deployment supports Heroku with Gunicorn and WhiteNoise.

High-level production flow:

1. Set all required Heroku config vars.
2. Push main branch to Heroku remote.
3. Run migrate and createsuperuser as one-off dyno tasks.
4. Verify health, static files, and auth flows.

Detailed step-by-step runbook: DEPLOYMENT_GUIDE.md

## 10. Security Baseline

1. Keep DEBUG off in production.
2. Set strict ALLOWED_HOSTS and CSRF trusted origins.
3. Keep all secrets in environment variables only.
4. Rotate OAuth and API keys if accidentally exposed.
5. Do not commit test credentials or plaintext secrets.

## 11. Documentation Index

1. docs/ARCHITECTURE.md: system architecture, modules, data flow.
2. docs/AUTH.md: auth routes, social login, edge-case handling.
3. docs/PASSWORD_POLICY.md: password constraints and validation behavior.
4. docs/TROUBLESHOOTING.md: incident-response style debugging playbook.
5. docs/FAQ-DEVELOPER.md: practical development questions and answers.
6. docs/SEO_QUICK_START.md: fast SEO verification flow.
7. docs/SEO_OPTIMIZATION_GUIDE.md: full SEO implementation details.
8. docs/SEO_COMPLETE_CHECKLIST.md: production SEO checklist.
9. docs/SEO_FINAL_SUMMARY.md: SEO status and next milestones.

## 12. Contribution Workflow

1. Create a feature branch from main.
2. Keep commits focused and atomic.
3. Run checks and tests locally.
4. Submit pull request with:
   1. Problem statement
   2. Approach summary
   3. Validation evidence (commands and outcomes)
   4. Rollback notes for risky changes

## 13. License

MIT License.


### Getting Help
1. Check `docs/TROUBLESHOOTING.md`
2. Review Django error messages
3. Check environment variables (`.env`)
4. Review server logs: `python manage.py runserver` output

### Issues & Questions
- Open an issue on GitHub
- Check existing issues first
- Provide error messages and steps to reproduce

## 🎯 Roadmap

- [ ] Complete checkout flow
- [ ] Payment processing (Stripe/Mollie)
- [ ] Email notifications
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard
- [ ] Inventory management
- [ ] Product reviews & ratings
- [ ] Social media integration

## 📝 Version History

**v1.0.0** (April 6, 2026)
- Initial release
- Django 5.2.12 setup
- Authentication with Google OAuth
- Admin customer/order management
- Homepage card management
- Cloudinary integration
- i18n support (NL/EN)

---

**Built with ❤️ for Dutch streetwear enthusiasts**
