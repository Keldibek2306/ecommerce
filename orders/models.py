from django.db import models

from accounts.models import User
from products.models import Product


class Order(models.Model):
    OrderStatus = [
        ('panding', 'Panding'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]
    PaymentStatus = [
        ('panding', 'Panding'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=True, null=True, 
        related_name='orders'
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(choices=OrderStatus, default='panding')
    payment_status = models.CharField(choices=PaymentStatus, default='panding')
    address = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=12, decimal_places=2)
