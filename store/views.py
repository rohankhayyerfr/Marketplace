from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm, ProductGalleryFormSet, ProductFeatureFormSet, ProductSpecificationFormSet, \
    ProductVariantFormSet
from .models import *
from django.contrib.auth.decorators import login_required
from accounts.views import verify_identity
from accounts.models import SellerVerification

def home(request):
    return render(request, 'home.html')
def product_list(request):
    products = Product.objects.filter(status="approved")
    return render(request, 'products/list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


# Dashboard
@login_required
def dashboard(request):
    products = Product.objects.filter(owner=request.user)

    try:
        identity = request.user.sellerverification
    except SellerVerification.DoesNotExist:
        identity = None

    return render(request, 'dashboard/index.html', {
        'products': products,
        'identity': identity
    })

def product_create(request):
    try:
        identity = request.user.sellerverification
        if identity.status != "approved":
            return redirect('accounts:verify_status')
    except SellerVerification.DoesNotExist:
        return redirect('accounts:verify_identity')

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        gallery_formset = ProductGalleryFormSet(request.POST, request.FILES)
        feature_formset = ProductFeatureFormSet(request.POST, request.FILES)
        specification_formset = ProductSpecificationFormSet(request.POST)
        variant_formset = ProductVariantFormSet(request.POST)

        if (product_form.is_valid() and gallery_formset.is_valid() and
            feature_formset.is_valid() and specification_formset.is_valid() and
            variant_formset.is_valid()):

            product = product_form.save(commit=False)
            product.owner = request.user
            product.status = "pending"
            product.save()

            gallery_formset.instance = product
            gallery_formset.save()

            feature_formset.instance = product
            feature_formset.save()

            specification_formset.instance = product
            specification_formset.save()

            variant_formset.instance = product
            variant_formset.save()

            messages.success(request, 'محصول شما در دست مدیریت است به محض تایید شدن در سایت اضافه میشود')
            return redirect('store:dashboard')
    else:
        product_form = ProductForm()
        gallery_formset = ProductGalleryFormSet()
        feature_formset = ProductFeatureFormSet()
        specification_formset = ProductSpecificationFormSet()
        variant_formset = ProductVariantFormSet()

    return render(request, 'products/product_create.html', {
        'product_form': product_form,
        'gallery_formset': gallery_formset,
        'feature_formset': feature_formset,
        'specification_formset': specification_formset,
        'variant_formset': variant_formset
    })




def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)

    return render(request, 'category_product.html', {
        'category': category,
        'products': products
    })


def faqs(request):
    return render(request, 'faqs.html')