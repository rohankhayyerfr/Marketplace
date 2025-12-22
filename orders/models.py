from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)

    # اضافه کردن فیلدهای مشتری
    full_name = models.CharField(max_length=255, default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=20, default="")
    address = models.TextField(default="")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # وضعیت پرداخت: pending, paid, failed
    payment_status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


