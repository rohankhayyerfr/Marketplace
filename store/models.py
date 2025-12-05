from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField()
    main_image = models.ImageField(upload_to='products/main/')

    def __str__(self):
        return self.name

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)

    image = models.ImageField(upload_to='products/gallery/')
    def __str__(self):
         return f"Gallery image for {self.product.name}"

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='features/icons/')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.product.name} - {self.title}'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    title = models.CharField(max_length=100)
    price = models.BigIntegerField()
    stock = models.PositiveIntegerField(default=0)
    is_bestseller = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.title}"

# class Review(models.Model):
#     product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField()
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.product.name} - {self.name}"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True, default=None)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.company_name



class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=8)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id} - {self.full_name}'
