# Authentication Guide

## 1. Overview

Authentication combines Django auth, Django allauth, and custom customer-facing templates.

Supported methods:

1. Email/password account login.
2. New account registration.
3. Google social login (optional when configured).

## 2. Auth Goals

1. Keep user-visible auth experience branded and consistent.
2. Preserve secure defaults from Django and allauth.
3. Avoid confusion between default allauth templates and custom account pages.

## 3. Core Routes

Typical route groups in this project:

1. /accounts/login/
2. /accounts/signup/
3. /accounts/google/login/
4. /accounts/google/login/callback/
5. /account/profile/
6. /account/profile/edit/

Depending on URL mapping, some allauth routes may be redirected to custom customer templates.

## 4. Email and Password Flow

1. User submits login form.
2. Credentials validated by auth backend.
3. Session created.
4. User redirected to target route.

Registration flow:

1. User submits signup form.
2. Account created.
3. Optional email verification is initiated.
4. User is redirected according to allauth settings.

## 5. Google OAuth Flow

1. User clicks Google sign-in.
2. Browser redirected to provider consent page.
3. Provider returns authorization code to callback URL.
4. allauth exchanges code and binds social account.
5. User signs in or account linkage/creation occurs.

## 6. Required Google Setup

1. Create OAuth client in Google Cloud Console.
2. Set authorized redirect URIs for local and production.
3. Add client ID and secret to environment variables.
4. Configure social app in Django admin and associate correct site.

Recommended callback examples:

1. Local: http://127.0.0.1:8000/accounts/google/login/callback/
2. Production: https://<app-domain>/accounts/google/login/callback/

## 7. allauth Configuration Notes

Important settings often used in this project style:

1. SOCIALACCOUNT_LOGIN_ON_GET for direct social flow.
2. SOCIALACCOUNT_AUTO_SIGNUP for account creation behavior.
3. Provider auth params such as prompt=select_account.
4. Login/signup route overrides to custom pages.

## 8. Session and Security Controls

1. CSRF protection is mandatory on POST forms.
2. Secure cookie behavior should be enabled in production.
3. Host and origin validation must match deployed domain.
4. Admin access should enforce strong credentials and MFA where available.

## 9. Common Auth Issues and Fixes

1. User sees wrong login page:
	1. Check URL overrides and redirect mapping.
	2. Confirm correct template paths.
2. Google login loops or fails:
	1. Validate callback URL exact match.
	2. Validate social app site binding.
	3. Validate client key/secret in environment.
3. CSRF error after deploy:
	1. Add deployed domain to trusted origins.
4. Authenticated user cannot reach explicit login page:
	1. Check custom logic that auto-redirects signed-in users.

## 10. Test Plan for Authentication

Run this matrix before releases:

1. Email login with valid credentials.
2. Email login with invalid credentials.
3. Signup flow with new user.
4. Logout and re-login.
5. Google sign-in with existing user.
6. Google sign-in with new user path.
7. Password reset request flow.
8. Admin login flow.

Minimum command checks:

```powershell
python manage.py check
python manage.py test customers
```

## 11. Hardening Recommendations

1. Enable secure and httponly cookie policies in production.
2. Rotate social OAuth credentials on schedule.
3. Monitor failed login patterns.
4. Add account lockout/rate-limiting if abuse appears.

