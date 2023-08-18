from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Tag)
admin.site.register(Platform)


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['id', 'name', 'publisher', 'platForm']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'sex']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer']

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product' ,'quantity', 'type']

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password','status']

class PurchasedItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'customer', 'product']

class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product']

class PhoneCardPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'mobile_carrier', 'value']

admin.site.register(Product, ProductAdmin)
admin.site.register(PurchasedItem, PurchasedItemAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)
admin.site.register(PhoneCardPayment, PhoneCardPaymentAdmin)

