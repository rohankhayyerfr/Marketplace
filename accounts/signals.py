from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import SellerVerfication

@receiver(post_save, sender=SellerVerfication)
def update_user_seller(sender, instance, **kwargs):
    if instance.status == "approved":
        instance.user.is_staff = True
        instance.user.is_staff = True
        instance.user.save()

