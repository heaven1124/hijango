from django.contrib import admin
from orderapp.models import Order, Cart


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('num', 'title', 'price', 'pay_type', 'pay_status', 'receiver', 'receiver_phone', 'receiver_address')
    fields = ('num', 'title', 'price', 'pay_type', 'pay_status', 'receiver', 'receiver_phone', 'receiver_address')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'no')


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
