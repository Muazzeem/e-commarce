from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from store.models import Item, LineItem, Basket


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    basket, is_created = Basket.objects.get_or_create(user=request.user)
    basket = request.user.basket
    line_item, is_created = LineItem.objects.get_or_create(
        basket=basket, product=item,
        defaults={'quantity': 1, 'price': item.price}
    )
    if line_item.quantity >= item.current_stock:
        messages.info(request, "This product out of stock.")
        return redirect("core:order-summary")
    if not is_created:
        line_item.quantity += 1
        line_item.save()

    messages.info(request, "This item was added to your cart.")
    return redirect("core:order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
    line = request.user.basket.lines.filter(product__slug=slug).first()
    if line:
        line.quantity -= 1
        line.save()
    if line and line.quantity == 0:
        line.delete()
    messages.info(request, "This item quantity was updated.")
    return redirect("core:order-summary")
