from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import SellerProfile

@receiver(post_save, sender=SellerProfile)
def update_user_status(sender, instance, **kwargs):
    if instance.is_verfied:
        instance.user.is_seller = True
        instance.user.save()

