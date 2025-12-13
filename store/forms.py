from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Product, ProductVariant, ProductGallery, ProductFeature, ProductSpecification


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name' , 'description', 'price', 'inventory', 'main_image']
        exclude = ("slug", "owner", "status")

ProductGalleryFormSet = inlineformset_factory(
    Product, ProductGallery,
    fields=['image'],
    extra=1,
    max_num=15,
    can_delete=True
)

ProductFeatureFormSet = inlineformset_factory(
    Product, ProductFeature,
    fields=['icon', 'title', 'description'],
    extra=1,
    max_num=4,
    can_delete=True
)

ProductSpecificationFormSet = inlineformset_factory(
    Product, ProductSpecification,
    fields=['title', 'value'],
    extra=1,
    max_num=50,
    can_delete=True
)

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant,
    fields=['title', 'description', 'price', 'stock', 'is_bestseller'],
    extra=1,
    max_num=10,
    can_delete=True
)



class ProductImageForm(forms.ModelForm):
    image = forms.ImageField()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



