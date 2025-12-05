from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Product,ProductVariant

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'price', 'inventory', 'main_image']


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



