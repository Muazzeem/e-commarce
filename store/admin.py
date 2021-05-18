from django.contrib import admin

from .models import *

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(LineItem)
admin.site.register(OrderLine)
admin.site.register(Address)
admin.site.register(Basket)
admin.site.register(Order)
