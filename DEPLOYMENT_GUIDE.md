# Final Whistle Clothing Deployment Guide

This guide is written as an operations runbook for production deployment and maintenance.

## 1. Scope

Covers:

1. Local release validation.
2. Heroku deployment and environment configuration.
3. Post-deploy verification.
4. Incident response and rollback.
5. Operational checklists for repeatable releases.

## 2. Deployment Model

1. Application: Django served with Gunicorn.
2. Static files: WhiteNoise.
3. Media: local in dev, optional Cloudinary in production.
4. Database: SQLite locally, managed PostgreSQL recommended in production.
5. Platform: Heroku (heroku-24 stack).

## 3. Prerequisites

1. Heroku CLI installed.
2. Git remote configured for Heroku app.
3. Access to production config variables.
4. Local environment passing minimum checks.

Verify auth and app access:

```powershell
heroku auth:whoami
heroku apps
```

## 4. Required Environment Variables

Set all required variables before first release.

```powershell
heroku config:set DJANGO_SECRET_KEY=<strong-secret> --app <app-name>
heroku config:set DJANGO_DEBUG=False --app <app-name>
heroku config:set DJANGO_ALLOWED_HOSTS=<app-name>.herokuapp.com,<custom-domain> --app <app-name>
heroku config:set DJANGO_CSRF_TRUSTED_ORIGINS=https://<app-name>.herokuapp.com,https://<custom-domain> --app <app-name>
heroku config:set SITE_URL=https://<custom-domain-or-heroku-url> --app <app-name>
```

Optional integration variables:

```powershell
heroku config:set CLOUDINARY_CLOUD_NAME=<value> --app <app-name>
heroku config:set CLOUDINARY_API_KEY=<value> --app <app-name>
heroku config:set CLOUDINARY_API_SECRET=<value> --app <app-name>
heroku config:set GOOGLE_OAUTH2_KEY=<value> --app <app-name>
heroku config:set GOOGLE_OAUTH2_SECRET=<value> --app <app-name>
```

Production email variables (Mailtrap-ready):

```powershell
heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend --app <app-name>
heroku config:set EMAIL_HOST=sandbox.smtp.mailtrap.io --app <app-name>
heroku config:set EMAIL_PORT=587 --app <app-name>
heroku config:set EMAIL_HOST_USER=<mailtrap-username> --app <app-name>
heroku config:set EMAIL_HOST_PASSWORD=<mailtrap-password> --app <app-name>
heroku config:set EMAIL_USE_TLS=True --app <app-name>
heroku config:set EMAIL_USE_SSL=False --app <app-name>
heroku config:set EMAIL_TIMEOUT=10 --app <app-name>
heroku config:set DEFAULT_FROM_EMAIL=no-reply@finalwhistleclothing.com --app <app-name>
```

Notes:

1. Keep `EMAIL_USE_TLS=True` for Mailtrap port `587`.
2. Do not keep production on the console backend once SMTP credentials are available.
3. Rotate Mailtrap credentials if they are exposed.

## 5. Release Preparation Checklist

### 5.1 Production Preflight (Config Vars)

Run this command before each release:

```powershell
heroku config --app <app-name>
```

Confirm these values are present and non-empty:

1. `DJANGO_SECRET_KEY`
2. `DJANGO_DEBUG` set to `False`
3. `DJANGO_ALLOWED_HOSTS` with explicit production domains only (no wildcards/local hosts)
4. `DJANGO_CSRF_TRUSTED_ORIGINS` with explicit https origins only (no wildcards/local origins)
5. `EMAIL_BACKEND`
6. `DEFAULT_FROM_EMAIL`
7. If `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`:
8. `EMAIL_HOST`
9. `EMAIL_HOST_USER`
10. `EMAIL_HOST_PASSWORD`
11. `EMAIL_PORT`
12. `EMAIL_USE_TLS` / `EMAIL_USE_SSL` are valid for selected port

Notes:

1. Shopify tokens/secrets can stay pending until integration day.
2. If `SHOPIFY_STORE_DOMAIN` is set in production, `SHOPIFY_WEBHOOK_SECRET` must also be set.

### 5.2 Local Validation Gate

Run locally from repo root:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
git status
```

Release gate criteria:

1. manage.py check has zero errors.
2. test suite passes.
3. No accidental secret files staged.
4. Deployment files present and valid:
   1. Procfile
   2. requirements.txt
   3. .python-version

Fast gate command:

```powershell
python manage.py check && python manage.py test shop customers
```

## 6. Deploy to Heroku

```powershell
git push heroku main
```

If this is a first deployment, run one-off commands:

```powershell
heroku run python manage.py migrate --app <app-name>
heroku run python manage.py createsuperuser --app <app-name>
```

## 7. Post-Deploy Verification

### 7.1 App Health

```powershell
heroku ps --app <app-name>
heroku releases --app <app-name>
```

### 7.2 Runtime Logs

```powershell
heroku logs --tail --app <app-name>
```

### 7.3 Browser Smoke Tests

Validate all of the following manually:

1. Home page loads and styles are applied.
2. Login page and signup page load correctly.
3. Google sign-in route redirects correctly.
4. Admin login works.
5. Robots and sitemap endpoints return 200.

Key URLs:

1. /
2. /accounts/login/
3. /accounts/signup/
4. /admin/
5. /robots.txt
6. /sitemap.xml

## 8. Static and Media Notes

1. WhiteNoise manifest storage can fail if templates reference missing static files.
2. During release, collectstatic warnings about duplicate destination paths should be cleaned when possible.
3. If static assets are stale in browser, hard refresh and check response headers.

## 9. OAuth Production Checklist

For Google OAuth:

1. Authorized redirect URIs include production callback.
   1. Expected format: https://<app-domain>/accounts/google/login/callback/
2. Client ID and secret exist in Heroku config vars.
3. Social app is configured in Django admin for correct site.
4. Site domain in provider console matches production host.

## 10. Rollback Procedure

If critical regression is detected:

1. Identify last known good release.
2. Roll back from Heroku dashboard or CLI.
3. Verify dyno health and smoke tests.
4. Open incident note with root cause and remediation.

CLI release inspection:

```powershell
heroku releases --app <app-name>
```

## 11. Common Failure Modes

1. DisallowedHost: missing host in DJANGO_ALLOWED_HOSTS.
2. CSRF verification failed: missing trusted origin.
3. 500 on startup: bad env var or migration mismatch.
4. Missing CSS/JS: collectstatic or WhiteNoise manifest issue.
5. OAuth loop or wrong page: route overrides or provider misconfiguration.
6. Password reset email not delivered: invalid SMTP host/user/password or TLS/port mismatch.

See docs/TROUBLESHOOTING.md for deep diagnostics.

## 12. Security Controls for Release

1. Never commit .env.
2. Never publish OAuth or API secrets in documentation.
3. Rotate compromised keys immediately.
4. Use least privilege for cloud credentials.
5. Audit recent git history before pushing public remotes.

## 13. Suggested CI Pipeline

Recommended automated stages:

1. Lint and static analysis.
2. Django system checks.
3. Unit and integration tests.
4. Build artifact validation.
5. Deployment to staging.
6. Manual approval.
7. Deployment to production.

## 14. Operations Cadence

Per release:

1. Run checks and tests.
2. Deploy.
3. Validate routes and logs.
4. Announce release status.

Weekly:

1. Review logs for recurring warnings.
2. Review auth and SEO route behavior.
3. Review admin export workflows.

Monthly:

1. Dependency review and patch updates.
2. Secret rotation schedule review.
3. Performance and SEO health review.

```
1. Go to Search Console
2. Settings → Coverage
3. Request indexing for important pages
4. Enable email notifications for issues
```

#### Step 6.2: Set Up Analytics Goals
```
In Google Analytics:
1. Create goal: "Newsletter signup"
2. Create goal: "Product view"
3. Create goal: "Outbound link click"
```

#### Step 6.3: Monitor Core Web Vitals
```
In Search Console:
1. Navigate to: Experience → Core Web Vitals
2. Check mobile and desktop scores
3. Identify pages with issues
4. Fix issues and retest
```

#### Step 6.4: Keyword Tracking
```
Use tools like:
- Ahrefs (paid)
- SEMrush (paid)
- Google Search Console (free)

Track these keywords:
- "Dutch football streetwear"
- "voetbal kleding"
- "Final Whistle Clothing"
```

---

## ☑️ PRE-LAUNCH CHECKLIST

### **SEO Checklist**
- [ ] All 5 JSON-LD schemas validated
- [ ] Sitemap.xml returns 200 status
- [ ] Robots.txt properly configured
- [ ] All meta tags present (40+)
- [ ] Images have alt text
- [ ] Mobile-friendly confirmed
- [ ] Page speed 90+
- [ ] Security headers present
- [ ] HTTPS enabled
- [ ] Domains indexed in GSC

### **Business Checklist**
- [ ] Contact email configured
- [ ] Social media links updated
- [ ] Privacy policy page ready
- [ ] Terms & conditions ready
- [ ] Return policy documented
- [ ] Shipping info complete
- [ ] Payment methods configured
- [ ] Support email setup

### **Technical Checklist**
- [ ] .env file configured (non-Git)
- [ ] Static files collected
- [ ] Database migrated
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configured
- [ ] Email backend configured
- [ ] Logging setup
- [ ] Backups configured

---

## 📊 EXPECTED RESULTS

### **Baseline (Before Launch)**
- Organic sessions: 0
- Search impressions: 0
- Pages indexed: 0

### **Month 1**
- Organic sessions: 200-500
- Pages indexed: 50+
- Search impressions: 5,000-10,000
- CTR: 2-3%

### **Month 3**
- Organic sessions: 2,000-3,000
- Pages indexed: 100+
- Keywords ranking: 50+
- CTR: 3-5%

### **Month 6**
- Organic sessions: 5,000-8,000
- Pages indexed: 150+
- Keywords in top 20: 20+
- Conversion rate: 1-2%

---

## 🔄 ONGOING MAINTENANCE

### **Daily** (5 mins)
- Monitor site uptime
- Check for errors in logs

### **Weekly** (15 mins)
- Review Google Search Console
- Check for crawl errors
- Monitor top pages

### **Monthly** (1 hour)
- Update sitemap with new content
- Check keyword rankings
- Analyze traffic patterns
- Review backlink profile

### **Quarterly** (2-3 hours)
- Full SEO audit
- Competitor analysis
- Content strategy review
- Performance optimization

---

## 🆘 TROUBLESHOOTING

### **Sitemap not updating**
```bash
# Reload Django app
python manage.py shell
>>> from shop.views import sitemap_xml
>>> # Force cache clear if using caching
```

### **Meta tags not showing**
```bash
# Check template rendering
python manage.py shell
>>> from django.template import loader
>>> template = loader.get_template('finalwhistleclothing.html')
>>> print(template.render())  # Search for meta tags
```

### **Schema validation errors**
```
https://validator.schema.org/
# Paste page HTML
# Fix any errors shown
```

### **Robots.txt not serving**
```bash
# Check URL pattern
curl https://finalwhistleclothing.com/robots.txt
# Should return text/plain content-type
```

---

## 📞 SUPPORT

### **Documentation**
- SEO_OPTIMIZATION_GUIDE.md - Comprehensive strategies
- SEO_COMPLETE_CHECKLIST.md - 100+ items to verify
- SEO_QUICK_START.md - 5-minute setup guide

### **Resources**
- Django Docs: https://docs.djangoproject.com/
- Google Search Central: https://developers.google.com/search
- Schema.org: https://schema.org/
- Structured Data Testing: https://search.google.com/test/rich-results

### **Tools**
- Google Search Console: https://search.google.com/search-console
- Google Analytics: https://analytics.google.com
- PageSpeed Insights: https://pagespeed.web.dev/
- Mobile-Friendly Test: https://search.google.com/test/mobile-friendly

---

## ✅ COMPLETION STATUS

✅ Complete SEO infrastructure implemented  
✅ 5 JSON-LD schemas added  
✅ Dynamic sitemap & robots.txt  
✅ 3 custom middleware layers  
✅ 40+ meta tags optimized  
✅ Comprehensive documentation  
✅ **READY FOR PRODUCTION LAUNCH** 🚀

---

**Version:** 2.0  
**Last Updated:** April 6, 2026  
**Status:** PRODUCTION READY ✅

Now follow the 6 deployment phases above and your site will be fully optimized for search engines!
