from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from store.models import Item, LineItem, Basket


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Basket.objects.filter(user=request.user)
    if order_qs:
        basket_id = order_qs.first().id
    else:
        Basket.objects.create(user=request.user)
        basket_id = order_qs.first().id
    lineItem = LineItem.objects.filter(basket_id=basket_id)
    product = LineItem.objects.filter(product__slug=item.slug)
    if product.exists():
        order_item = LineItem.objects.get(
            product__slug=item.slug
        )
        if order_item.quantity == item.current_stock or \
                order_item.quantity >= item.current_stock:
            messages.info(request, "This item are running out.")
        else:
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
    else:
        lineItem.create(basket_id=basket_id, product=item, price=item.price)
        messages.info(request, "This item was added to your cart.")
    return redirect("core:order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = LineItem.objects.get_or_create(
        product__slug=item.slug
    )
    order_qs = Basket.objects.filter(user=request.user)
    basket_id = order_qs.first().id
    item_quantity = LineItem.objects.filter(basket_id=basket_id)
    product = LineItem.objects.filter(product__slug=item.slug)
    if item_quantity.exists():
        if product.exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "This item quantity was updated.")
        return redirect("core:order-summary")
