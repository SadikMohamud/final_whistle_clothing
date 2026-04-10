# SEO Optimization Guide

## 1. Purpose

This guide defines how SEO is implemented, validated, and maintained in this repository.

It focuses on engineering execution, not only marketing theory.

## 2. SEO Architecture

Current implementation is split into four layers:

1. Technical indexability
   1. robots endpoint.
   2. sitemap endpoint.
   3. canonical URL handling.
2. Metadata and social previews
   1. title and description tags.
   2. Open Graph tags.
   3. Twitter card tags.
3. Structured data
   1. organization schema.
   2. website schema.
   3. breadcrumb and FAQ-ready extensions.
4. Content and UX signals
   1. heading structure.
   2. image alt quality.
   3. mobile performance and accessibility.

## 3. Implementation Checklist by Layer

### 3.1 Indexability

1. /robots.txt returns 200 and includes sitemap location.
2. /sitemap.xml returns valid XML with absolute URLs.
3. Canonical points to one stable URL per page.

### 3.2 Metadata

1. Unique page title and meta description per key page.
2. Open Graph title, description, image, and URL.
3. Twitter card tags aligned with OG tags.

### 3.3 Structured Data

1. JSON-LD script validates in schema tooling.
2. Organization schema includes name, URL, and contact channels.
3. Optional FAQ schema includes truthful, visible page content.

### 3.4 Content Semantics

1. One H1 per page.
2. H2 and H3 hierarchy reflects sections.
3. Internal links use descriptive anchor text.
4. Images contain descriptive alt text.

## 4. International SEO

1. Default language is Dutch.
2. Secondary language support is English.
3. hreflang tags should include both language variants and x-default.
4. Translated text should preserve intent, not literal wording.

## 5. Performance and SEO Coupling

Core Web Vitals affect rankings and conversion quality.

Focus areas:

1. Compress and cache static assets.
2. Lazy-load non-critical images.
3. Avoid render-blocking resources where possible.
4. Keep template payloads lean.

## 6. Local Validation Workflow

```powershell
python manage.py check
python manage.py test
```

Manual checks:

1. View source of homepage.
2. Confirm metadata presence.
3. Confirm schema JSON syntax.
4. Confirm robots and sitemap responses.

## 7. Production Validation Workflow

1. Use Google Rich Results Test.
2. Use schema validator.
3. Submit sitemap to Search Console.
4. Monitor indexing and coverage reports.
5. Review page speed monthly.

## 8. Keyword Strategy Framework

Use three tiers:

1. Branded terms.
2. Category terms with local intent.
3. Long-tail buying-intent terms.

Selection rules:

1. Prioritize purchase intent over vanity traffic.
2. Map one primary keyword per page cluster.
3. Avoid cannibalization by assigning clear topic ownership.

## 9. Content Operations

Per new page or campaign:

1. Define search intent and keyword mapping.
2. Draft title and description variants.
3. Add internal links from existing relevant pages.
4. Publish and validate structured data.
5. Monitor impressions and CTR after indexing.

## 10. Monitoring KPIs

Primary metrics:

1. Indexed pages count.
2. Query impressions.
3. Organic CTR.
4. Average position for target terms.
5. Organic conversion rate.

## 11. Failure Modes

1. Duplicate titles and descriptions.
2. Broken canonical URLs.
3. Invalid schema JSON.
4. Soft 404 content.
5. Slow mobile rendering.

## 12. Governance

1. SEO checks required for template-level changes.
2. Documentation update required when routes or metadata logic changes.
3. Post-release smoke tests include SEO endpoints.

## 13. Next Technical Enhancements

1. Add product-level structured data for dynamic product pages.
2. Generate sitemap sections by content type.
3. Add automated metadata linting in CI.
4. Add broken-link crawling step in release pipeline.

