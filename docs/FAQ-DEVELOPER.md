# Developer FAQ

## 1. How do I set up the project from scratch?

```powershell
git clone <repo-url>
cd Final_whistle_clothing
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 2. What are the minimum commands before opening a PR?

```powershell
python manage.py check
python manage.py test
git status
```

## 3. Where do I configure environment variables?

In the local .env file for development, and Heroku config vars for production.

Never commit .env.

## 4. Why does the deployed app throw DisallowedHost?

DJANGO_ALLOWED_HOSTS is missing the active domain.

Fix by adding both Heroku hostname and custom domain.

## 5. Why do I get CSRF verification errors in production?

DJANGO_CSRF_TRUSTED_ORIGINS does not include the full https origin.

## 6. Why are CSS and JS missing after deploy?

Likely causes:

1. collectstatic failed.
2. WhiteNoise manifest references a missing file.
3. Browser cache not refreshed.

## 7. How do I verify deployment quickly?

```powershell
heroku ps --app <app-name>
heroku releases --app <app-name>
heroku logs --tail --app <app-name>
```

Then smoke test:

1. /
2. /accounts/login/
3. /admin/
4. /robots.txt
5. /sitemap.xml

## 8. Where should I implement visual changes?

1. shop/static/shop/css/site.css for global style tokens and components.
2. templates/finalwhistleclothing.html for page-level markup.
3. app-specific templates for account/admin behavior.

## 9. How is language switching implemented?

UI strings are mapped in the site JavaScript dictionary and bound using i18n keys in templates.

## 10. How do I add a new admin export?

1. Add admin action or custom admin view.
2. Use csv writer with explicit headers.
3. Add permission guard via admin site auth wrapper.
4. Add regression tests for export response shape.

## 11. How do I debug Google OAuth issues?

Checklist:

1. Callback URI exact match.
2. Social app credentials in environment/admin.
3. Correct Site object association.
4. Confirm login route redirects are not overriding callback behavior.

## 12. What is the preferred branching strategy?

1. Create short-lived feature branches from main.
2. Keep one purpose per branch.
3. Rebase or merge main regularly.
4. Keep PRs reviewable and small.

## 13. How should commit messages be written?

Use imperative, explicit messages with business context, for example:

1. Add account force-login route behavior.
2. Fix static manifest image reference crash.
3. Remove green accents from storefront palette.

## 14. How do I run app-specific tests only?

```powershell
python manage.py test customers
python manage.py test shop
```

## 15. What should I do if secrets were accidentally committed?

1. Rotate affected secrets immediately.
2. Remove secrets from git history.
3. Force push only after team approval.
4. Validate scanners pass before reopening PR.

## 16. How do I add a new environment variable safely?

1. Add read logic in settings with safe defaults.
2. Document variable in README and deployment guide.
3. Add to Heroku config and local .env.
4. Validate startup without the variable when possible.

## 17. What are common first checks for a 500 error?

1. heroku logs tail.
2. Recent deployment diff.
3. Missing migrations.
4. Missing static artifact.
5. Missing or malformed env var.

## 18. How should documentation be updated?

For any production-impacting change, update:

1. README summary.
2. DEPLOYMENT_GUIDE operational steps.
3. One specialized doc under docs for deep details.

