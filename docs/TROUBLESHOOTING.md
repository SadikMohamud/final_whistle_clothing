# Troubleshooting Guide

This guide is optimized for fast diagnosis in local development and Heroku production.

## 1. Triage Process

Always follow this order:

1. Reproduce issue consistently.
2. Capture exact error output.
3. Check latest code delta.
4. Verify environment variables.
5. Validate migrations and static assets.

## 2. High-Value Commands

Local:

```powershell
python manage.py check
python manage.py test
python manage.py showmigrations
```

Heroku:

```powershell
heroku ps --app <app-name>
heroku releases --app <app-name>
heroku logs --tail --app <app-name>
heroku config --app <app-name>
```

## 3. Startup Failures

Symptoms:

1. Gunicorn process crashes immediately.
2. App returns 503/500 right after deploy.

Checks:

1. Confirm Procfile points to correct WSGI app.
2. Confirm dependencies installed from requirements.txt.
3. Confirm .python-version is valid for stack.
4. Confirm required environment variables exist.

## 4. DisallowedHost Errors

Cause:

1. Active host missing from allowed hosts config.

Fix:

1. Add Heroku URL and custom domain to allowed hosts variable.
2. Redeploy or restart dyno.

## 5. CSRF Verification Failed

Cause:

1. Missing origin in CSRF trusted origins.

Fix:

1. Add full https origin to trusted origins.
2. Verify forms use csrf token tags.

## 6. Static Files Missing or Unstyled Pages

Symptoms:

1. HTML renders but looks unstyled.
2. Browser shows 404 for CSS or JS.

Checks:

1. Confirm WhiteNoise middleware and storage config.
2. Confirm collectstatic completed successfully.
3. Check for missing static references under manifest storage.
4. Hard refresh browser to bypass stale cache.

## 7. OAuth Login Problems

Symptoms:

1. Redirect loops.
2. provider error invalid redirect_uri.
3. Landing on unexpected default template.

Checks:

1. Callback URI exact match in provider console.
2. Correct client key and secret in environment.
3. Social app linked to correct site in admin.
4. Custom route redirects not conflicting with callback endpoint.

## 8. Migration Issues

Symptoms:

1. no such column errors.
2. relation does not exist errors.

Checks:

1. showmigrations output.
2. Run migrate on target environment.
3. Verify migration files are committed.

## 9. Admin Issues

1. Admin not loading expected custom UI:
	1. Verify template path overrides.
2. CSV export action missing:
	1. Confirm admin action registration.
	2. Confirm user permissions.

## 10. Debugging 500 Errors in Production

Workflow:

1. Open Heroku logs tail.
2. Reproduce with exact URL.
3. Inspect first traceback frame in project code.
4. Validate env vars used by that code path.
5. Fix locally and re-run checks/tests.
6. Deploy and re-verify.

## 11. Common Release Regressions

1. Template references static file that no longer exists.
2. Route changed but links still point to old endpoint.
3. Added required env var but not set in production.
4. Social auth provider settings diverge between admin and env.

## 12. Preventive Controls

1. Run check and test before every deploy.
2. Keep deployment checklist in pull request template.
3. Add smoke test scripts for critical routes.
4. Review logs after every production release.

