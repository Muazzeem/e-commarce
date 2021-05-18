from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import Signer
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, View
from .forms import CheckoutForm
from .models import *


class HomeView(ListView):
    model = Item
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get("category")
        context['categories'] = Category.objects.all()
        if category:
            context['items'] = Item.objects.filter(category__name=category)
        else:
            context['items'] = Item.objects.all()
        return context


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            basket = Basket.objects.get(user=self.request.user)
            context = {
                'object': basket
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            basket = Basket.objects.get(user=self.request.user)
            context = {
                'order': basket,
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            user_address = Address(
                user=self.request.user,
                address=form.cleaned_data.get('address'),
                phone=form.cleaned_data.get('phone')
            )
            basket = Basket.objects.get(user=self.request.user)
            user_address.save()
            order = Order.objects.create(user=self.request.user, billing_address=user_address,
                                         total=basket.total)
            for order_item in basket.lines.all():
                OrderLine.objects.get_or_create(
                    order=order,
                    product=order_item.product,
                    quantity=order_item.quantity,
                    price=order_item.price, total=order_item.total
                )
                item = get_object_or_404(Item, slug=order_item.product.slug)
                item.current_stock -= order_item.quantity
                item.save()
            basket.delete()
            signer = Signer()
            value = signer.sign(order.id)
            return redirect(reverse('core:generate-pdf', kwargs={"number": value}))
        return redirect(reverse('core:generate-pdf'))
