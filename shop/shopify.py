import logging
from decimal import Decimal

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


def _shopify_domain() -> str:
  return settings.SHOPIFY_STORE_DOMAIN.strip()


def _storefront_token() -> str:
  return settings.SHOPIFY_STOREFRONT_ACCESS_TOKEN.strip()


def _storefront_version() -> str:
  return settings.SHOPIFY_STOREFRONT_API_VERSION.strip()


def _admin_token() -> str:
  return getattr(settings, "SHOPIFY_ADMIN_ACCESS_TOKEN", "").strip()


def _to_money(amount: str) -> str:
  try:
    return f"{Decimal(amount):.2f}"
  except Exception:
    return "0.00"


def _parse_variant_gid(variant_gid: str) -> str:
  if not variant_gid:
    return ""
  return variant_gid.rsplit("/", 1)[-1]


def _parse_product_node(node: dict, domain: str) -> dict:
  variant_edges = (node.get("variants") or {}).get("edges", [])
  first_variant_gid = ""
  variants = []
  in_stock = False

  for edge in variant_edges:
    variant = edge.get("node", {})
    variant_gid = variant.get("id", "")
    available = bool(variant.get("availableForSale", False))
    in_stock = in_stock or available

    price_data = (variant.get("price") or {})
    variants.append(
      {
        "id": variant_gid,
        "legacy_id": _parse_variant_gid(variant_gid),
        "title": variant.get("title", "Default"),
        "available": available,
        "price": _to_money(price_data.get("amount", "0")),
        "currency": price_data.get("currencyCode", "EUR"),
        "sku": variant.get("sku", ""),
      }
    )
    if not first_variant_gid:
      first_variant_gid = variant_gid

  price_data = (node.get("priceRange") or {}).get("minVariantPrice", {})
  images = []
  image_edges = (node.get("images") or {}).get("edges", [])
  for edge in image_edges:
    image = edge.get("node", {})
    url = image.get("url", "")
    if url:
      images.append({"url": url, "alt": image.get("altText") or node.get("title", "Product")})

  featured_image = node.get("featuredImage") or {}
  if featured_image.get("url") and not images:
    images.append({
      "url": featured_image.get("url", ""),
      "alt": featured_image.get("altText") or node.get("title", "Product"),
    })

  return {
    "id": node.get("id", ""),
    "title": node.get("title", "Untitled Product"),
    "handle": node.get("handle", ""),
    "description": node.get("description", ""),
    "variant_id": first_variant_gid,
    "legacy_variant_id": _parse_variant_gid(first_variant_gid),
    "image_url": featured_image.get("url", "") if featured_image else (images[0]["url"] if images else ""),
    "image_alt": (featured_image.get("altText") if featured_image else "") or node.get("title", "Product"),
    "price": _to_money(price_data.get("amount", "0")),
    "currency": price_data.get("currencyCode", "EUR"),
    "product_url": f"https://{domain}/products/{node.get('handle', '')}",
    "vendor": node.get("vendor", ""),
    "product_type": node.get("productType", ""),
    "tags": node.get("tags", []),
    "variants": variants,
    "images": images,
    "in_stock": in_stock,
  }


def _storefront_graphql(query: str, variables: dict) -> dict:
  domain = _shopify_domain()
  token = _storefront_token()
  version = _storefront_version()

  if not domain or not token:
    return {}

  url = f"https://{domain}/api/{version}/graphql.json"
  headers = {
    "Content-Type": "application/json",
    "X-Shopify-Storefront-Access-Token": token,
  }

  try:
    response = requests.post(
      url,
      headers=headers,
      json={"query": query, "variables": variables},
      timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
  except requests.RequestException as exc:
    logger.exception("Shopify Storefront request failed: %s", exc)
    return {}

  if payload.get("errors"):
    logger.error("Shopify Storefront GraphQL errors: %s", payload["errors"])
    return {}

  return payload.get("data", {})


def shopify_admin_get(path: str, params: dict | None = None) -> dict:
  domain = _shopify_domain()
  token = _admin_token()
  version = _storefront_version()

  if not domain or not token:
    logger.warning("Shopify admin settings missing. Returning empty response.")
    return {}

  url = f"https://{domain}/admin/api/{version}/{path.lstrip('/')}"
  headers = {
    "X-Shopify-Access-Token": token,
    "Content-Type": "application/json",
    "Accept": "application/json",
  }
  try:
    response = requests.get(url, headers=headers, params=params or {}, timeout=20)
    response.raise_for_status()
    return response.json()
  except requests.RequestException as exc:
    logger.exception("Shopify Admin GET failed: %s", exc)
    return {}


def fetch_storefront_products(limit: int = 8) -> list[dict]:
  """Fetch products from Shopify Storefront GraphQL API."""
  domain = _shopify_domain()
  token = _storefront_token()
  version = _storefront_version()

  if not domain or not token:
    logger.warning("Shopify settings missing. Returning empty product list.")
    return []

  url = f"https://{domain}/api/{version}/graphql.json"
  headers = {
    "Content-Type": "application/json",
    "X-Shopify-Storefront-Access-Token": token,
  }
  query = """
    query GetProducts($limit: Int!) {
      products(first: $limit) {
        edges {
          node {
            id
            title
            handle
            variants(first: 1) {
              edges {
                node {
                  id
                }
              }
            }
            featuredImage {
              url
              altText
            }
            priceRange {
              minVariantPrice {
                amount
                currencyCode
              }
            }
          }
        }
      }
    }
  """

  try:
    response = requests.post(
      url,
      headers=headers,
      json={"query": query, "variables": {"limit": limit}},
      timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
  except requests.RequestException as exc:
    logger.exception("Shopify request failed: %s", exc)
    return []

  if payload.get("errors"):
    logger.error("Shopify GraphQL errors: %s", payload["errors"])
    return []

  edges = payload.get("data", {}).get("products", {}).get("edges", [])
  products = []

  for edge in edges:
    node = edge.get("node", {})
    products.append(_parse_product_node(node, domain))

  return products


def fetch_product_by_handle(handle: str) -> dict:
    query = """
    query GetProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id
        title
        handle
        description
        vendor
        productType
        tags
        featuredImage {
          url
          altText
        }
        images(first: 10) {
          edges {
            node {
              url
              altText
            }
          }
        }
        variants(first: 25) {
          edges {
            node {
              id
              title
              availableForSale
              sku
              price {
                amount
                currencyCode
              }
            }
          }
        }
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
        }
      }
    }
    """
    data = _storefront_graphql(query, {"handle": handle})
    node = data.get("productByHandle") or {}
    if not node:
        return {}
    return _parse_product_node(node, _shopify_domain())


def fetch_products_by_query(query_string: str, limit: int = 24) -> list[dict]:
    query = """
    query SearchProducts($query: String!, $limit: Int!) {
      products(first: $limit, query: $query) {
        edges {
          node {
            id
            title
            handle
            description
            productType
            tags
            vendor
            featuredImage {
              url
              altText
            }
            images(first: 6) {
              edges {
                node {
                  url
                  altText
                }
              }
            }
            variants(first: 5) {
              edges {
                node {
                  id
                  title
                  availableForSale
                  sku
                  price {
                    amount
                    currencyCode
                  }
                }
              }
            }
            priceRange {
              minVariantPrice {
                amount
                currencyCode
              }
            }
          }
        }
      }
    }
    """

    data = _storefront_graphql(query, {"query": query_string, "limit": limit})
    edges = (data.get("products") or {}).get("edges", [])
    domain = _shopify_domain()
    products = []
    for edge in edges:
        node = edge.get("node", {})
        products.append(_parse_product_node(node, domain))
    return products
