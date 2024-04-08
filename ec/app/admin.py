from django.contrib import admin
from .models import Product,Customer, Cart, OrderPlaced, Wishlist    #import product từ models
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
# Register your models here.


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "discounted_price", "category", "product_image")   # equal


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "locality", "mobile", "state", "zipcode") 
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "products", "quantity") 
    def products(self,obj):
        link = reverse("admin:app_product_change", args= [obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.title )

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "customers", "products", "quantity", "ordered_date", "status") 
    
    def customers(self,obj):
        link = reverse("admin:app_customer_change", args= [obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.customer.name )
    
    def products(self,obj):
        link = reverse("admin:app_product_change", args= [obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.title )

    
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "products") # chuyển product thành products mới hoạt động
    def products(self,obj):
        link = reverse("admin:app_product_change", args= [obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.title )

admin.site.unregister(Group) # Xoá gr khỏi django admin