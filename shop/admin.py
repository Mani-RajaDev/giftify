from django.contrib import admin

from .models import Product, Category, Offer, Order, OrderItem, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    list_filter = ["category", "name"]
    search_fields = ["name", "category__name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "get_category_product_count"]


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ["title", "get_display_discount_percentage", "is_active"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["get_order_number", "get_ordered_by", "is_guest", "get_ordered_on"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["get_order_number", "__str__", "product", "quantity", "subtotal"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "is_guest", "created_at"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]
