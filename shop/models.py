from django.db import models
from django.conf import settings
from django.contrib import admin
from datetime import datetime

from users.models import GuestUser


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        "Category",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
    )
    offers = models.ManyToManyField("Offer", blank=True)
    image = models.ImageField(upload_to="products/")
    stock_quantity = models.PositiveBigIntegerField(default=10)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    desciption = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @admin.display(description="Category Product Count")
    def get_category_product_count(self):
        return self.products.count()


class Offer(models.Model):
    title = models.CharField(max_length=255, verbose_name="Offer")
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Discount Percentage",
        null=True,
        blank=True,
    )
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @admin.display(description="Discount Percentage")
    def get_display_discount_percentage(self):
        """
        Returns the discount percentage if available, or N/A if it's None.
        """
        return f"{self.discount_percentage}%" if self.discount_percentage else "N/A"


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    guest_user = models.ForeignKey(
        GuestUser,
        related_name="guest_orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-order_date"]

    def __str__(self):
        formatted_date = self.order_date.strftime("%d %B %Y (%A)")

        if self.user:
            return f"Order: {self.id} by {self.user.address.name} on {formatted_date}"
        else:
            return f"Order: {self.id} by {self.guest_user.guest_address.name} on {formatted_date}"

    def is_guest(self):
        return True if self.guest_user else False

    is_guest.boolean = True

    @admin.display(description="Order Number")
    def get_order_number(self):
        return f"#{self.id}"
    
    @admin.display(description="Order By")
    def get_ordered_by(self):
        return (
            self.user.address.name if self.user else self.guest_user.guest_address.name
        )
    
    @admin.display(description="Order On")
    def get_ordered_on(self):
        formatted_date = self.order_date.strftime("%d %B %Y (%A)")
        return formatted_date


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def subtotal(self):
        return self.quantity * self.product.price
    
    @admin.display(description="Order Number")
    def get_order_number(self):
        return f"#{self.order.pk}"


