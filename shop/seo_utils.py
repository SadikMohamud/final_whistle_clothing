"""
SEO Utilities for Final Whistle Clothing
Provides helper functions for search engine optimization
"""

from django.conf import settings
from django.templatetags.static import static
from datetime import datetime


def get_site_config():
    """Returns the SEO configuration from settings"""
    return settings.SEO_CONFIG


def get_canonical_url(request):
    """Generate canonical URL for the current page"""
    site_url = settings.SEO_CONFIG["SITE_URL"]
    path = request.path
    return f"{site_url}{path}"


def get_og_image_url(request=None):
    """Get Open Graph image URL"""
    config = get_site_config()
    return config.get(
        "DEFAULT_IMAGE",
        "https://placehold.co/1200x630/111111/C8F400?text=Final+Whistle+Clothing",
    )


def get_organization_schema():
    """Returns organization schema for JSON-LD"""
    config = get_site_config()
    org = config["ORGANIZATION"]
    
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": org["name"],
        "url": org["url"],
        "logo": org["logo"],
        "description": config["SITE_DESCRIPTION"],
        "sameAs": org["same_as"],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "Customer Service",
            "email": org["contact_email"],
        },
        "address": {
            "@type": "PostalAddress",
            "addressCountry": org["address"]["country"],
            "addressLocality": org["address"]["locality"],
        },
    }


def get_breadcrumb_schema(items):
    """
    Generate breadcrumb schema
    
    Args:
        items: List of tuples (name, url)
    """
    breadcrumb_items = []
    for idx, (name, url) in enumerate(items, 1):
        breadcrumb_items.append({
            "@type": "ListItem",
            "position": idx,
            "name": name,
            "item": url,
        })
    
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumb_items,
    }


def get_product_schema(product_data):
    """
    Generate product schema for JSON-LD
    
    Args:
        product_data: Dictionary with product info
    """
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product_data.get("title", ""),
        "description": product_data.get("description", ""),
        "image": product_data.get("image_url", ""),
        "brand": {
            "@type": "Brand",
            "name": "Final Whistle Clothing",
        },
        "offers": {
            "@type": "Offer",
            "price": product_data.get("price", ""),
            "priceCurrency": product_data.get("currency", "EUR"),
            "availability": "InStock",
            "seller": {
                "@type": "Organization",
                "name": "Final Whistle Clothing",
            },
        },
    }


def get_faq_schema(faqs):
    """
    Generate FAQ schema for JSON-LD
    
    Args:
        faqs: List of tuples (question, answer)
    """
    main_entity = []
    for question, answer in faqs:
        main_entity.append({
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer,
            },
        })
    
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity,
    }


def get_website_schema(site_url):
    """Generate website schema for JSON-LD"""
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Final Whistle Clothing",
        "url": site_url,
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{site_url}?q={{search_term_string}}",
            },
            "query-input": "required name=search_term_string",
        },
    }


def get_meta_tags(request, title=None, description=None, image=None):
    """
    Generate meta tags for a page
    
    Args:
        request: Django request object
        title: Page title (optional)
        description: Meta description (optional)
        image: OG image URL (optional)
    """
    config = get_site_config()
    
    return {
        "title": title or f"{config['SITE_NAME']} | Premium Dutch Streetwear",
        "description": description or config["SITE_DESCRIPTION"],
        "image": image or get_og_image_url(request),
        "canonical": get_canonical_url(request),
        "site_url": config["SITE_URL"],
    }


def get_hreflang_links(current_path="/"):
    """
    Generate hreflang links for language variants
    
    Args:
        current_path: Current page path
    """
    config = get_site_config()
    base_url = config["SITE_URL"].rstrip("/")
    
    links = []
    for lang_code, lang_info in config["LANGUAGES"].items():
        links.append({
            "rel": "alternate",
            "hreflang": lang_code,
            "href": f"{base_url}{current_path}?lang={lang_code}",
        })
    
    # x-default for default language
    links.append({
        "rel": "alternate",
        "hreflang": "x-default",
        "href": f"{base_url}{current_path}",
    })
    
    return links
