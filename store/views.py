from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product, ProductVariant, Category
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


# Dashboard
@login_required
def dashboard(request):
    products = Product.objects.filter(owner=request.user)


    return render(request, 'dashboard/index.html', {'products': products})


# @login_required
# def product_create(request):
#     categories = Category.objects.all()
#     try:
#         seller_profile = request.user.seller_profile
#     except SellerProfile.DoesNotExist:
#         return redirect('store:dashboard')
#
#     if not seller_profile.is_verified:
#         messages.error(request, 'شما هنوز تایید نشده اید!')
#         return redirect('accounts:become_seller')
#
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#
#
#         if form.is_valid():
#             p = form.save(commit=False)
#             p.owner = request.user
#             p.save()
#
#
#
#             return redirect("store:dashboard")
#     else:
#         form = ProductForm()
#
#
#     return render(
#         request,
#         'dashboard/product_form.html',
#         {
#             'form': form,
#
#             'categories': categories,
#         }
#     )
#
#
# @login_required
# def product_edit(request, pk):
#     product = get_object_or_404(Product, pk=pk, owner=request.user)
#
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         formset = VariantFormSet(request.POST, instance=product)
#
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect("store:dashboard")
#
#     else:
#         form = ProductForm(instance=product)
#         formset = VariantFormSet(instance=product)
#
#     return render(
#         request,
#         'dashboard/product_form.html',
#         {
#             'form': form,
#             'formset': formset,
#             'product': product
#         }
#     )
#
#
# @login_required
# def product_delete(request, pk):
#     product = get_object_or_404(Product, pk=pk, owner=request.user)
#     product.delete()
#     return redirect("store:dashboard")



def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)

    return render(request, 'category_product.html', {
        'category': category,
        'products': products
    })