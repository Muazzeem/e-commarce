from django import template
from store.models import Basket, LineItem

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        order_qs = Basket.objects.filter(user=user)
        if order_qs:
            basket_id = order_qs.first().id
        else:
            Basket.objects.create(user=user)
            basket_id = order_qs.first().id
        if order_qs:
            order_qs = LineItem.objects.filter(basket_id=basket_id)
            return order_qs.count()

    return 0
