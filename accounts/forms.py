from django import forms
from .models import SellerVerification

class SellerVerificationForm(forms.ModelForm):
    class Meta:
        model = SellerVerification
        fields = [
            "full_name", "country", "city", "national_id",
            "phone", "id_cart_image", "selfie_image", "address", "company"
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }
