from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
from io import BytesIO

from django.views import View
from xhtml2pdf import pisa
from django.template.loader import get_template

from .models import *
from .utils import cartData, guestOrder


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    categories = Category.objects.all()
    category = request.GET.get("category")
    context = {'cartItems': cartItems, 'categories': categories}
    if category:
        products = Product.objects.filter(category__name=category)
        context.update({'products': products})
    else:
        context.update({'products': products})
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product, created = Product.objects.get_or_create(id=productId)
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    data = json.loads(request.body)
    customer, order = guestOrder(request, data)
    OrderItem.objects.filter(order_id=order.id)
    total = float(data['form']['total'])
    if total == order.get_cart_total:
        order.save()
    # ShippingAddress.objects.create(
    #     customer=customer,
    #     order=order,
    #     phone=data["form"]["phone"],
    # )
    return HttpResponse()


def render_to_pdf(template_src, context_dict=None, *args, **kwargs):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('store/invoice.html')
        return HttpResponse(pdf, content_type='application/pdf')
