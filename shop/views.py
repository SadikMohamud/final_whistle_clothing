import base64
import hashlib
import hmac
import json
import logging
from datetime import datetime, timedelta, timezone as dt_timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import HomepageCard, NewsletterSubscription
from .forms import ContactForm
from .seo_utils import get_faq_schema
from .shopify import (
    fetch_product_by_handle,
    fetch_products_by_query,
    fetch_storefront_products,
)
from customers.models import CustomerOrder, CustomerProfile


logger = logging.getLogger(__name__)


def _info_page_context(
    request,
    *,
    page_title: str,
    page_eyebrow: str,
    page_heading: str,
    page_intro: str,
    sections: list[dict],
    cta_label: str | None = None,
    cta_url: str | None = None,
    contact_form: ContactForm | None = None,
    faq_items: list[tuple[str, str]] | None = None,
):
    context = {
        "page_title": page_title,
        "page_eyebrow": page_eyebrow,
        "page_heading": page_heading,
        "page_intro": page_intro,
        "sections": sections,
        "cta_label": cta_label,
        "cta_url": cta_url,
        "contact_form": contact_form,
    }
    if faq_items:
        context["faq_schema_json"] = json.dumps(get_faq_schema(faq_items))
    return render(request, "shop/info_page.html", context)


def home(request):
    search_term = request.GET.get("q", "").strip()
    products = fetch_storefront_products(limit=8)
    search_results = []
    if search_term:
        search_results = fetch_products_by_query(search_term, limit=20)

    homepage_cards_qs = HomepageCard.objects.filter(is_active=True).order_by("sort_order", "-created_at")
    hero_card = homepage_cards_qs.filter(image__isnull=False).first()
    if hero_card:
        homepage_cards = list(homepage_cards_qs.exclude(pk=hero_card.pk)[:8])
    else:
        homepage_cards = list(homepage_cards_qs[:8])
    context = {
        "products": products,
        "search_term": search_term,
        "search_results": search_results,
        "homepage_cards": homepage_cards,
        "hero_card": hero_card,
        "site_url": settings.SEO_CONFIG["SITE_URL"],
        "organization": settings.SEO_CONFIG["ORGANIZATION"],
        "current_lang": getattr(request, "fwc_lang", "nl"),
    }
    return render(request, "shop/home.html", context)


def products_api(request):
    products = fetch_storefront_products(limit=8)
    return JsonResponse({"products": products})


def product_detail(request, handle):
    product = fetch_product_by_handle(handle)
    if not product:
        return render(request, "404.html", status=404)

    context = {
        "product": product,
    }
    return render(request, "shop/product_detail.html", context)


def collection_view(request, slug):
    collection_queries = {
        "all": "available_for_sale:true",
        "tshirts": "product_type:'T-Shirts' OR tag:tshirts OR tag:tee",
        "hoodies": "product_type:Hoodies OR tag:hoodies",
        "tracksuits": "product_type:Tracksuits OR tag:tracksuits",
        "jackets": "product_type:Jackets OR tag:jackets",
        "shorts": "product_type:Shorts OR tag:shorts",
        "caps": "product_type:Caps OR tag:caps",
        "accessories": "product_type:Accessories OR tag:accessories",
        "sale": "tag:sale",
    }

    query = collection_queries.get(slug)
    if not query:
        return render(request, "404.html", status=404)

    products = fetch_products_by_query(query, limit=30)
    context = {
        "collection_slug": slug,
        "products": products,
    }
    return render(request, "shop/collection.html", context)


def search_view(request):
    term = request.GET.get("q", "").strip()
    products = fetch_products_by_query(term, limit=24) if term else []
    context = {
        "query": term,
        "products": products,
    }
    return render(request, "shop/search_results.html", context)


def story_view(request):
    context = {
        "story_title": "Our Story",
        "story_intro": (
            "Final Whistle Clothing started as a small idea: create elevated streetwear with the "
            "same edge and confidence people look for in the city. What began as sketches and "
            "samples became a label shaped by clean silhouettes, sharp details, and a focus on "
            "pieces people actually want to wear every day."
        ),
    }
    return render(request, "shop/story.html", context)


def shipping_view(request):
    sections = [
        {
            "title": "Drop 1 - Ready to ship",
            "text": "Drop 1 items are in stock and ship directly from our headquarters once processing is complete.",
        },
        {
            "title": "Processing time",
            "text": "Please allow 1-2 business days for order processing before dispatch.",
        },
        {
            "title": "Delivery in the Netherlands",
            "text": "Orders delivered within the Netherlands typically arrive within 1-3 business days after dispatch.",
        },
        {
            "title": "Drop 2 - Made to order",
            "text": "Drop 2 products are made to order and produced specifically for you after purchase.",
        },
        {
            "title": "International shipping",
            "text": "Shipping times outside the Netherlands vary by destination. Rates and estimated delivery times are calculated at checkout.",
        },
        {
            "title": "Tracking and order updates",
            "text": "You will receive a tracking number as soon as your order has been handed to the carrier.",
        },
        {
            "title": "Important shipping notes",
            "text": "Orders containing both Drop 1 and Drop 2 items may arrive separately. Please review your shipping address carefully, as changes cannot be made once production has started.",
        },
    ]
    return _info_page_context(
        request,
        page_title="Shipping Policy",
        page_eyebrow="Info",
        page_heading="Shipping Policy",
        page_intro="Clear information on order processing, delivery timing, made-to-order production, and worldwide shipping.",
        sections=sections,
        cta_label="Browse products",
        cta_url=reverse("collection_view", kwargs={"slug": "all"}),
    )


def returns_view(request):
    sections = [
        {
            "title": "Return window",
            "text": "Orders may be returned within 14 days of receipt.",
        },
        {
            "title": "Condition requirements",
            "text": "Items must be unworn, unwashed, unaltered, and returned with all original tags attached. Where possible, please include the original packaging.",
        },
        {
            "title": "Return shipping",
            "text": "Return shipping to our warehouse is at the customer’s expense unless the item is faulty or the order was sent in error.",
        },
        {
            "title": "Refunds and exchanges",
            "text": "Approved returns are processed as a refund or exchange, depending on the request and item eligibility. Refunds are issued to the original payment method.",
        },
        {
            "title": "Processing time",
            "text": "Refunds are typically processed within 7-10 business days once your return has been received and approved.",
        },
        {
            "title": "Non-returnable items",
            "text": "For hygiene reasons, underwear briefs, bodysuits, swimwear, and pierced jewellery cannot be returned or exchanged unless faulty.",
        },
        {
            "title": "Faulty or damaged items",
            "text": "If you receive a faulty, damaged, or incorrect item, please contact us with your order details and supporting photos so we can resolve the matter promptly.",
        },
    ]
    return _info_page_context(
        request,
        page_title="Refund Policy",
        page_eyebrow="Info",
        page_heading="Refund Policy",
        page_intro="A clear returns and refund policy designed to set expectations around eligibility, condition, and processing times.",
        sections=sections,
        cta_label="Contact us",
        cta_url=reverse("contact"),
    )


def contact_view(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contact_email = settings.SEO_CONFIG["ORGANIZATION"]["contact_email"]
        subject = f"Final Whistle Clothing contact: {form.cleaned_data['subject']}"
        message = (
            f"Name: {form.cleaned_data['name']}\n"
            f"Email: {form.cleaned_data['email']}\n\n"
            f"Message:\n{form.cleaned_data['message']}"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [contact_email],
                fail_silently=False,
            )
            messages.success(request, "Thanks, your message has been sent. We’ll reply as soon as possible.")
            return redirect("contact")
        except Exception:
            logger.exception("Contact form failed to send")
            messages.error(request, "Your message could not be sent right now. Please try again later.")

    sections = [
        {
            "title": "General enquiries",
            "text": f"Email us at {settings.SEO_CONFIG['ORGANIZATION']['contact_email']} for product, order, or brand questions.",
        },
        {
            "title": "Response times",
            "text": "We aim to reply as quickly as possible during business hours.",
        },
        {
            "title": "Order support",
            "text": "Include your order number if your message is about shipping, returns, or a delivery update.",
        },
    ]
    return _info_page_context(
        request,
        page_title="Contact",
        page_eyebrow="Info",
        page_heading="Contact",
        page_intro="Send us a message and we’ll get back to you with the right next step.",
        sections=sections,
        contact_form=form,
        cta_label="Browse products",
        cta_url=reverse("collection_view", kwargs={"slug": "all"}),
    )


def faq_view(request):
    faq_items = [
        (
            "What is Final Whistle Clothing?",
            "Final Whistle Clothing is a premium Dutch streetwear brand built around sharp silhouettes, everyday wearability, and a clean visual language.",
        ),
        (
            "How much is shipping?",
            "Shipping is free on orders above €100. Below that threshold, the standard shipping rate is shown at checkout.",
        ),
        (
            "How long does delivery take?",
            "Orders placed before 22:00 are prepared for next-business-day delivery in the Netherlands.",
        ),
        (
            "What is your return policy?",
            "You have 30 days to request a return or exchange for eligible items.",
        ),
        (
            "How do I contact support?",
            "Use the contact page form or email us directly for order support and brand enquiries.",
        ),
    ]
    sections = [
        {
            "title": question,
            "text": answer,
        } for question, answer in faq_items
    ]
    context = _info_page_context(
        request,
        page_title="FAQ",
        page_eyebrow="Info",
        page_heading="FAQ",
        page_intro="Quick answers to the questions customers ask most often.",
        sections=sections,
        cta_label="Contact us",
        cta_url=reverse("contact"),
        faq_items=faq_items,
    )
    return context


def privacy_view(request):
    sections = [
        {
            "title": "Collecting personal information",
            "text": (
                "When you visit the Site or place an order, we may collect information about your device, your browsing activity, and the details needed to process purchases or support requests."
            ),
        },
        {
            "title": "Device and order information",
            "text": (
                "Device information may include browser version, IP address, time zone, cookies, and browsing behaviour. Order information may include your name, billing and shipping details, payment information, email address, and phone number."
            ),
        },
        {
            "title": "How we use your information",
            "text": (
                "We use personal information to provide our services, fulfil orders, process payments, arrange shipping, send order confirmations, improve the Site, and respond to customer support requests."
            ),
        },
        {
            "title": "Sharing personal information",
            "text": (
                "We share personal information only where necessary to operate the Site, fulfil orders, comply with legal obligations, or work with service providers that help us deliver our services."
            ),
        },
        {
            "title": "Cookies and tracking technologies",
            "text": (
                "We use cookies and similar technologies to remember preferences, keep the Site functioning properly, and understand how visitors use the Site. You can manage cookies through your browser settings."
            ),
        },
        {
            "title": "Your rights",
            "text": (
                "Depending on your location, you may have the right to access, correct, update, export, or request deletion of your personal information. To exercise your rights or raise a privacy concern, contact us using the details below."
            ),
        },
        {
            "title": "Contact information",
            "text": (
                "For privacy-related questions or complaints, please contact finalwhistleclothing@gmail.com. If required by law, you may also contact your local data protection authority."
            ),
        },
    ]
    return _info_page_context(
        request,
        page_title="Privacy Policy",
        page_eyebrow="Legal",
        page_heading="Privacy Policy",
        page_intro=(
            "This policy explains how Final Whistle Clothing collects, uses, stores, and shares personal information when you use the Site or place an order."
        ),
        sections=sections,
        cta_label="Contact us",
        cta_url=reverse("contact"),
    )


def terms_view(request):
    sections = [
        {
            "title": "Overview",
            "text": "By visiting this Site or placing an order, you agree to the Terms of Service and any related policies referenced on the Site.",
        },
        {
            "title": "Online store terms",
            "text": "You may not use the Site for unlawful purposes, violate applicable laws, or transmit malicious code or disruptive content.",
        },
        {
            "title": "General conditions",
            "text": "We reserve the right to refuse service at any time and to modify or discontinue the Site, features, or pricing without notice.",
        },
        {
            "title": "Products and services",
            "text": "Product availability, descriptions, and pricing may change without notice. We do not guarantee that every detail will always be current or error-free.",
        },
        {
            "title": "Billing and account information",
            "text": "You agree to provide current, complete, and accurate purchase and account information and to keep those details up to date when needed.",
        },
        {
            "title": "Third-party links and tools",
            "text": "Any third-party links or tools are provided for convenience only and are used at your own risk under the applicable third-party terms.",
        },
        {
            "title": "User submissions",
            "text": "If you send comments, suggestions, or other submissions to us, you grant us the right to use them without obligation to maintain them in confidence or provide compensation.",
        },
        {
            "title": "Liability and indemnification",
            "text": "Use of the Site is at your own risk. To the fullest extent permitted by law, FINAL WHISTLE is not liable for indirect or consequential losses arising from use of the Site or its services.",
        },
        {
            "title": "Governing law and changes",
            "text": "These Terms are governed by the laws of the Netherlands. We may update the Terms from time to time, and continued use of the Site indicates acceptance of those changes.",
        },
        {
            "title": "Contact information",
            "text": "Questions about these Terms of Service can be sent to finalwhistleclothing@gmail.com.",
        },
    ]
    return _info_page_context(
        request,
        page_title="Terms of Service",
        page_eyebrow="Legal",
        page_heading="Terms of Service",
        page_intro="These Terms explain how the Site may be used, what governs purchases, and the expectations that apply to customers and visitors.",
        sections=sections,
        cta_label="Privacy Policy",
        cta_url=reverse("privacy_policy"),
    )


@login_required(login_url='customer_login')
def shopify_checkout(request):
    """
    Redirect authenticated users to Shopify checkout/cart flow.
    If a variant ID is provided, go directly to cart for checkout.
    """
    domain = settings.SHOPIFY_STORE_DOMAIN.strip()
    if not domain:
        return redirect('home')

    variant_id = request.GET.get("variant", "").strip()
    quantity = request.GET.get("qty", "1").strip()

    # Ensure quantity is valid positive integer
    if not quantity.isdigit() or int(quantity) <= 0:
        quantity = "1"

    if variant_id:
        variant_id = variant_id.rsplit("/", 1)[-1]
        checkout_url = (
            f"https://{domain}/cart/{variant_id}:{quantity}"
            f"?checkout[email]={request.user.email}"
        )
    else:
        # Fallback when no variant is present
        checkout_url = f"https://{domain}/checkout"

    return redirect(checkout_url)


def robots_txt(request):
    """
    Serve robots.txt for SEO
    """
    site_url = settings.SEO_CONFIG["SITE_URL"]
    content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /*?
Disallow: /checkout/
Disallow: /cart/

# Specific crawl-delay for bots
Crawl-delay: 1

# Sitemaps
Sitemap: {site_url}/sitemap.xml
Sitemap: {site_url}/sitemap-nl.xml
Sitemap: {site_url}/sitemap-en.xml

# Common bots
User-agent: Googlebot
Disallow: /admin/
Crawl-delay: 0.5

User-agent: Bingbot
Disallow: /admin/
Crawl-delay: 1

# Block bad bots
User-agent: MJ12bot
Disallow: /

User-agent: AhrefsBot
Crawl-delay: 1

User-agent: SemrushBot
Crawl-delay: 1
"""
    return HttpResponse(content, content_type="text/plain")


@require_POST
def newsletter_subscribe(request):
    email = request.POST.get("email", "").strip().lower()
    source = request.POST.get("source", "homepage")[:120]

    if not email:
        messages.error(request, "Please provide an email address.")
        return redirect("home")

    subscription, created = NewsletterSubscription.objects.get_or_create(
        email=email,
        defaults={"source": source, "is_active": True},
    )

    if not created and not subscription.is_active:
        subscription.is_active = True
        subscription.source = source or subscription.source
        subscription.save(update_fields=["is_active", "source", "updated_at"])

    if created:
        messages.success(request, "You have been subscribed to the newsletter.")
    else:
        messages.info(request, "This email is already subscribed.")

    return redirect("home")


def _shopify_hmac_is_valid(request) -> bool:
    secret = getattr(settings, "SHOPIFY_WEBHOOK_SECRET", "").encode("utf-8")
    if not secret:
        return False

    provided_hmac = request.headers.get("X-Shopify-Hmac-Sha256", "")
    computed_hmac = base64.b64encode(
        hmac.new(secret, request.body, hashlib.sha256).digest()
    ).decode("utf-8")
    return hmac.compare_digest(provided_hmac, computed_hmac)


def _resolve_customer_profile(payload: dict) -> CustomerProfile | None:
    customer = payload.get("customer") or {}
    customer_email = (
        customer.get("email")
        or payload.get("email")
        or payload.get("contact_email")
        or ""
    ).strip().lower()
    shopify_customer_id = str(customer.get("id") or "").strip()

    profile = None
    if shopify_customer_id:
        profile = CustomerProfile.objects.filter(shopify_customer_id=shopify_customer_id).first()

    if not profile and customer_email:
        profile = CustomerProfile.objects.filter(user__email__iexact=customer_email).first()

    if not profile and customer_email:
        user, _ = User.objects.get_or_create(
            username=customer_email,
            defaults={"email": customer_email},
        )
        if not user.has_usable_password():
            user.set_unusable_password()
            user.save(update_fields=["password"])
        profile = user.customer_profile

    if not profile:
        return None

    updates = []
    if customer_email and profile.shopify_email != customer_email:
        profile.shopify_email = customer_email
        updates.append("shopify_email")
    if shopify_customer_id and profile.shopify_customer_id != shopify_customer_id:
        profile.shopify_customer_id = shopify_customer_id
        updates.append("shopify_customer_id")
    if updates:
        profile.save(update_fields=updates + ["account_updated"])
    return profile


def _parse_shopify_datetime(value: str):
    if not value:
        return timezone.now()
    dt = parse_datetime(value)
    if not dt:
        return timezone.now()
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone=dt_timezone.utc)
    return dt


def _status_from_payload(payload: dict) -> str:
    fulfillment_status = (payload.get("fulfillment_status") or "").lower()
    financial_status = (payload.get("financial_status") or "").lower()
    canceled_at = payload.get("cancelled_at")

    if canceled_at:
        return "cancelled"
    if financial_status in {"refunded", "partially_refunded"}:
        return "refunded"
    if fulfillment_status in {"fulfilled", "delivered"}:
        return "delivered"
    if fulfillment_status in {"partial", "in_progress"}:
        return "processing"
    return "pending"


def _extract_items(payload: dict) -> tuple[int, list[dict]]:
    items = payload.get("line_items") or []
    normalized = []
    for item in items:
        normalized.append(
            {
                "shopify_line_item_id": item.get("id"),
                "product_id": item.get("product_id"),
                "variant_id": item.get("variant_id"),
                "title": item.get("title"),
                "variant_title": item.get("variant_title"),
                "sku": item.get("sku"),
                "quantity": item.get("quantity", 0),
                "price": item.get("price"),
            }
        )
    return len(normalized), normalized


def _sync_customer_order_from_payload(payload: dict) -> bool:
    profile = _resolve_customer_profile(payload)
    if not profile:
        return False

    shopify_order_id = str(payload.get("id") or "").strip()
    shopify_order_number = str(payload.get("order_number") or payload.get("name") or "").strip("# ")

    if not shopify_order_id or not shopify_order_number:
        return False

    items_count, items_data = _extract_items(payload)

    defaults = {
        "customer": profile,
        "status": _status_from_payload(payload),
        "total_price": payload.get("total_price") or "0",
        "currency": payload.get("currency") or "EUR",
        "ordered_at": _parse_shopify_datetime(payload.get("created_at")),
        "items_count": items_count,
        "items_data": {"line_items": items_data, "raw": payload},
    }

    with transaction.atomic():
        order, created = CustomerOrder.objects.get_or_create(
            shopify_order_id=shopify_order_id,
            defaults={"shopify_order_number": shopify_order_number, **defaults},
        )
        if not created:
            order.customer = profile
            order.shopify_order_number = shopify_order_number
            order.status = defaults["status"]
            order.total_price = defaults["total_price"]
            order.currency = defaults["currency"]
            order.ordered_at = defaults["ordered_at"]
            order.items_count = defaults["items_count"]
            order.items_data = defaults["items_data"]
            order.save()

    return True


@csrf_exempt
@require_POST
def shopify_orders_create_webhook(request):
    if not _shopify_hmac_is_valid(request):
        return JsonResponse({"ok": False, "error": "Invalid signature"}, status=401)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

    synced = _sync_customer_order_from_payload(payload)
    status = 200 if synced else 202
    return JsonResponse({"ok": True, "synced": synced}, status=status)


@csrf_exempt
@require_POST
def shopify_orders_updated_webhook(request):
    if not _shopify_hmac_is_valid(request):
        return JsonResponse({"ok": False, "error": "Invalid signature"}, status=401)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

    synced = _sync_customer_order_from_payload(payload)
    status = 200 if synced else 202
    return JsonResponse({"ok": True, "synced": synced}, status=status)


def sitemap_xml(request):
    """
    Serve dynamic XML sitemap for SEO with all major pages
    """
    site_url = settings.SEO_CONFIG["SITE_URL"].rstrip('/')
    
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
    
    <!-- Homepage (Primary) -->
    <url>
        <loc>{site_url}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
        <xhtml:link rel="alternate" hreflang="nl" href="{site_url}/?lang=nl" />
        <xhtml:link rel="alternate" hreflang="en" href="{site_url}/?lang=en" />
    </url>
    
    <!-- Shop/Collections Section -->
    <url>
        <loc>{site_url}/#shop</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.95</priority>
    </url>
    
    <!-- Category: T-Shirts -->
    <url>
        <loc>{site_url}/#tshirts</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- Category: Hoodies -->
    <url>
        <loc>{site_url}/#hoodies</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- Category: Tracksuits -->
    <url>
        <loc>{site_url}/#tracksuits</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- Category: Accessories -->
    <url>
        <loc>{site_url}/#accessories</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- Collections Section -->
    <url>
        <loc>{site_url}/#collections</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    
    <!-- Collection: Tops & Sweaters -->
    <url>
        <loc>{site_url}/#collection-tops</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- Collection: Bottoms & Shorts -->
    <url>
        <loc>{site_url}/#collection-bottoms</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- Collection: Caps & Accessories -->
    <url>
        <loc>{site_url}/#collection-accessories</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <!-- Campaign/Story Section -->
    <url>
        <loc>{site_url}/#story</loc>
        <lastmod>{yesterday}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.85</priority>
    </url>
    
    <!-- Newsletter Section -->
    <url>
        <loc>{site_url}/#newsletter</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>

    <!-- Privacy Policy -->
    <url>
        <loc>{site_url}/privacy-policy/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.4</priority>
    </url>
    
</urlset>"""
    
    return HttpResponse(sitemap, content_type="application/xml")

