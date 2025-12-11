from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
from store.models import Product, ProductVariant

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def items(self):
        return self.cartitem_set.all()

    @property
    def sub_total(self):
        return sum(item.total_price for item in self.items)

    @property
    def discount(self):
        return 0  # یا محاسبه تخفیف واقعی

    @property
    def shipping_fee(self):
        return 0  # یا محاسبه هزینه ارسال

    @property
    def final_total(self):
        return self.sub_total - self.discount + self.shipping_fee

def update_totals(self):
    self.sub_total = sum(item.total_price for item in self.items.all())
    self.final_total = self.sub_total + self.shipping_fee - self.discount
    self.save()


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def unit_price(self):
        return self.variant.price if self.variant else self.product.price
    @property
    def total_price(self):
        return  self.quantity * (self.variant.price if self.variant else self.product.price)
