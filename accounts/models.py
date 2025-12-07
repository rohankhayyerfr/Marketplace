from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

class SellerVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    national_id = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    id_cart_image = models.ImageField(upload_to='identity/id_card/')
    selfie_image = models.ImageField(upload_to='identity/selfie/', null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"


User.add_to_class('is_seller', models.BooleanField(default=False))