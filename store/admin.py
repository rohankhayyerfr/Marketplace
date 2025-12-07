from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, Order, ProductGallery, ProductFeature, ProductVariant, \
    ProductSpecification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1
    max_num = 4


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    max_num = 15

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    min_num = 1
    max_num = 10
class ProductSpecificInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    min_num = 1
    max_num = 50


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'created_at', 'total', 'paid')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductGalleryInline, ProductFeatureInline, ProductVariantInline, ProductSpecificInline]
    list_display = ('name', 'price', 'inventory', 'category')
    prepopulated_fields = {'slug': ('name',)}