from django import template
from store.models import Basket

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        basket, is_created = Basket.objects.get_or_create(user=user)
        return basket.count_item
    return 0
