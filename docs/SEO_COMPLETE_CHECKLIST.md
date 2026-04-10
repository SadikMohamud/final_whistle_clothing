# SEO Complete Checklist

Use this checklist for release readiness and monthly SEO health audits.

## 1. Technical Indexability

- [ ] /robots.txt returns 200 in production.
- [ ] robots includes sitemap URL.
- [ ] /sitemap.xml returns 200 and valid XML.
- [ ] Sitemap contains canonical absolute URLs.
- [ ] No blocked important routes in robots.
- [ ] Canonical tags render on all key pages.

## 2. Metadata Quality

- [ ] Unique title tag per key page.
- [ ] Meta description present and unique.
- [ ] Open Graph tags present.
- [ ] Twitter card tags present.
- [ ] Correct og:image path and dimensions.
- [ ] Language tags present.
- [ ] hreflang tags reflect available languages.

## 3. Structured Data

- [ ] JSON-LD scripts parse without syntax errors.
- [ ] Organization schema includes brand and URL.
- [ ] Website schema includes search action where applicable.
- [ ] FAQ schema reflects visible page content.
- [ ] No schema warnings in validator that indicate critical issues.

## 4. Content and Semantics

- [ ] Exactly one H1 on each core landing page.
- [ ] Heading levels are not skipped without reason.
- [ ] Internal links use descriptive text.
- [ ] Primary images include useful alt text.
- [ ] Avoid duplicated paragraph blocks across major pages.

## 5. Performance and UX Signals

- [ ] Mobile page speed within acceptable range.
- [ ] No large unoptimized images in above-the-fold sections.
- [ ] Non-critical images are lazy-loaded.
- [ ] Static assets are cacheable in production.
- [ ] No major layout shifts on initial render.

## 6. International SEO

- [ ] Dutch default language path is consistent.
- [ ] English variant is discoverable.
- [ ] hreflang values map correctly to page variants.
- [ ] Mixed-language content is intentional and reviewed.

## 7. Deployment Integrity

- [ ] python manage.py check passes before deploy.
- [ ] python manage.py test passes before deploy.
- [ ] collectstatic completes in release logs.
- [ ] No static manifest missing-file errors.
- [ ] Post-deploy smoke tests include SEO endpoints.

## 8. Monitoring and Tooling

- [ ] Search Console property verified.
- [ ] Sitemap submitted to Search Console.
- [ ] Coverage report reviewed monthly.
- [ ] Rich Results validation run on homepage after major template updates.
- [ ] PageSpeed monitored monthly for regressions.

## 9. Security and Trust Signals

- [ ] HTTPS enforced on all public routes.
- [ ] Security headers are present in response.
- [ ] No secrets are embedded in page source.
- [ ] Contact and legal information is accessible.

## 10. Content Operations

- [ ] Each new campaign page has keyword intent mapping.
- [ ] Internal links added from at least one existing page.
- [ ] Metadata reviewed by engineering before release.
- [ ] Copy reviewed for clarity and authenticity.

## 11. Monthly SEO Review Template

Capture these items in one monthly record:

1. Top 20 organic queries by impressions.
2. CTR trend for top 20 queries.
3. Pages with declining impressions.
4. Crawl or indexing errors introduced this month.
5. Improvements shipped and measurable impact.

## 12. Release Sign-Off Block

Release date:

Release owner:

Checklist result:

1. Passed
2. Blocked
3. Passed with known risks

Known risks and mitigation:

