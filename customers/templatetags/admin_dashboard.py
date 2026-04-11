from decimal import Decimal

from django import template
from django.db.models import Count, Sum

from customers.models import CustomerOrder, CustomerProfile

register = template.Library()


@register.simple_tag
def admin_total_revenue():
    return CustomerOrder.objects.aggregate(total=Sum("total_price")).get("total") or Decimal("0.00")


@register.simple_tag
def admin_revenue_30_days():
    from django.utils import timezone
    from datetime import timedelta

    start = timezone.now() - timedelta(days=30)
    return CustomerOrder.objects.filter(ordered_at__gte=start).aggregate(total=Sum("total_price")).get("total") or Decimal("0.00")


@register.simple_tag
def admin_total_orders():
    return CustomerOrder.objects.aggregate(total=Count("id")).get("total") or 0


@register.simple_tag
def admin_total_customers():
    return CustomerProfile.objects.aggregate(total=Count("id")).get("total") or 0
