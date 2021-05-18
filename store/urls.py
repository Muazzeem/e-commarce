from django.urls import path

from invoice.views import GeneratePdf
from order.views import *
from .views import (
    CheckoutView,
    HomeView,
    OrderSummaryView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('generate-pdf/<str:number>', GeneratePdf.as_view(), name="generate-pdf"),
]
