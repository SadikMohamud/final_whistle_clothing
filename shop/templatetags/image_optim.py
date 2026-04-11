from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django import template


register = template.Library()


def _cloudinary_transform(url: str, width: int | None = None) -> str:
    if not url:
        return ""

    parsed = urlparse(url)
    if "res.cloudinary.com" not in parsed.netloc:
        return url

    marker = "/upload/"
    if marker not in parsed.path:
        return url

    transforms = ["f_auto", "q_auto", "dpr_auto", "c_limit"]
    if width and width > 0:
        transforms.append(f"w_{int(width)}")

    before, after = parsed.path.split(marker, 1)
    transformed_path = f"{before}{marker}{','.join(transforms)}/{after}"
    return urlunparse(parsed._replace(path=transformed_path))


def _shopify_resize(url: str, width: int | None = None) -> str:
    if not url:
        return ""

    parsed = urlparse(url)
    if "cdn.shopify.com" not in parsed.netloc:
        return url

    if not width or width <= 0:
        return url

    params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    params["width"] = str(int(width))
    return urlunparse(parsed._replace(query=urlencode(params)))


def _optimize_url(url: str, width: int | None = None) -> str:
    if "res.cloudinary.com" in (urlparse(url).netloc if url else ""):
        return _cloudinary_transform(url, width)
    if "cdn.shopify.com" in (urlparse(url).netloc if url else ""):
        return _shopify_resize(url, width)
    return url


@register.simple_tag
def optimized_image_url(url: str, width: int | None = None) -> str:
    return _optimize_url(url, width)


@register.simple_tag
def responsive_image_srcset(url: str, widths: str = "320,480,640,960,1280") -> str:
    if not url:
        return ""

    srcset_parts: list[str] = []
    for raw in widths.split(","):
        value = raw.strip()
        if not value or not value.isdigit():
            continue
        width = int(value)
        srcset_parts.append(f"{_optimize_url(url, width)} {width}w")
    return ", ".join(srcset_parts)
