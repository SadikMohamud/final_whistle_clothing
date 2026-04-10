# Prioritised Fix Plan

This plan turns the current audit into a safe, iterative delivery sequence. The goal is to ship the highest-risk fixes first, keep each change small, and verify after every commit.

## Delivery Rules

1. One small fix per commit.
2. Run `manage.py check` after every code change.
3. Run the most relevant tests for the touched area before pushing.
4. If a change touches frontend behavior, verify it in the browser on desktop and mobile.
5. If a change touches auth or deployment, verify it on Heroku before moving to the next item.

## Phase 0: Freeze and Baseline

1. Confirm current live app behavior on Heroku.
2. Capture current branch state and release version.
3. Keep this phase read-only except for the plan document.

## Phase 1: High-Risk Security and Production Stability

Priority: highest

Status: mostly complete

1. Tighten production settings in `fwc/settings.py`.
2. Make `DEBUG` default to false outside local development.
3. Require an explicit production `SECRET_KEY`.
4. Narrow `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to actual deployment domains.
5. Add secure cookie and redirect settings for production.
6. Fail closed for missing email or webhook secrets instead of silently degrading.

Completed in this phase:

1. Production settings hardening, explicit secret key requirement, and secure production defaults.
2. Explicit email backend requirement with SMTP validation checks.
3. Narrowed production hosts/origins and guardrails against wildcard/local values.
4. Fail-closed webhook secret requirement when Shopify domain is enabled.

Remaining in this phase:

1. Final Shopify token/secret configuration after client provides credentials.

Suggested commit sequence:

1. Security settings hardening.
2. Email and reset flow production config.
3. Shopify webhook validation cleanup.

## Phase 2: Authentication and Account Flow

Priority: high

Status: complete for current scope

1. Add tests for login, signup, logout, and password reset.
2. Remove duplicate or conflicting auth template paths.
3. Make account and reset pages fully consistent across the flow.
4. Add rate limiting or a lightweight brute-force guard for login and reset endpoints.
5. Improve error handling so users do not see raw exception messages.

Completed in this phase:

1. Added auth flow tests for login/signup/logout/password reset.
2. Removed duplicate conflicting password-reset templates.
3. Added rate limiting for login, signup, and password reset endpoint.
4. Hardened customer-facing error messages with server-side logging.

Suggested commit sequence:

1. Auth tests.
2. Password reset flow cleanup.
3. Login/signup hardening.

## Phase 3: Language and Theme UX

Priority: medium-high

Status: in progress

1. Keep English as the default site language.
2. Persist the customer language choice consistently.
3. Make the language toggle reliable across all page shells.
4. Keep the theme toggle stable and testable.
5. Replace fragile toggle code with small, explicit helpers.

Completed in this phase:

1. English-first default enforced in middleware and JS fallback behavior.
2. Language persistence hardened and toggle/session sync stabilized.
3. Theme toggle initialization hardened for edge-page DOM/storage cases.

Remaining in this phase:

1. Final cross-shell visual consistency check of toggles on all auth/account templates.

Suggested commit sequence:

1. Language default and persistence.
2. Theme toggle reliability.
3. Shared toggle design update after client approval.

## Phase 4: Frontend Stability

Priority: medium

Status: mostly complete

1. Keep the custom cursor fail-safe on desktop only.
2. Preserve native cursor behavior on touch devices.
3. Add browser checks for main navigation and landing-page interactions.
4. Verify image, font, and asset loading after each change.

Completed in this phase:

1. Cursor behavior made fail-safe and desktop-only.
2. Landing interactions and toggle script regressions fixed.

Remaining in this phase:

1. One final manual smoke pass across mobile + desktop key routes.

Suggested commit sequence:

1. Cursor and interaction hardening.
2. Landing-page smoke checks.

## Phase 5: Tests and Deployment Hygiene

Priority: medium

Status: in progress

1. Add meaningful tests to `customers/tests.py` and `shop/tests.py`.
2. Add deploy preflight checks to the deployment guide.
3. Verify migrations, static collection, and environment variables before release.
4. Add checks for production email delivery configuration.
5. Add webhook and storage-path tests.

Completed in this phase:

1. Added meaningful tests in `customers/tests.py` and `shop/tests.py`.
2. Added deploy preflight checks and gate commands in deployment docs.

Remaining in this phase:

1. Add storage-path tests.
2. Add Shopify webhook tests after credentials/integration window opens.

Suggested commit sequence:

1. Auth and reset tests.
2. Shop/webhook tests.
3. Deployment guide preflight updates.

## Phase 6: Admin and Content Improvements

Priority: lower

1. Add admin bulk actions where they are useful.
2. Improve null handling and filters in admin tools.
3. Clean up placeholder wording that is no longer accurate.
4. Review content for any remaining Dutch-only defaults where English should be first.

Suggested commit sequence:

1. Admin improvements.
2. Content cleanup.

## Recommended Order To Ship

If the goal is a client-ready release with minimal risk, I would ship in this order:

1. Production security hardening.
2. Auth and reset flow stability.
3. Language/theme reliability.
4. Cursor and frontend stability.
5. Tests and deployment guide.
6. Admin and content cleanup.

## Acceptance Criteria

1. No runtime 500s in auth/reset paths.
2. English loads first on every page.
3. Toggles work reliably on desktop and degrade safely on mobile.
4. Live Heroku build passes after each commit.
5. Tests exist for the most important flows.

## Notes For Client Review

1. This repo is already functional, but several production hardening items are still missing.
2. The safest path is incremental delivery, not a large single merge.
3. Each phase above is designed to be independently reviewable and revertible.
