from django.contrib import admin

from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
    ]
    list_display_links = [
        'user',
    ]
    search_fields = [
        'user__username',
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone',
        'address'
    ]


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
