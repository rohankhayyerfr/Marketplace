from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_home, name='cart_home'),  # صفحه سبد خرید
    path('update/', views.update_cart_item, name='update_item'),
    path('remove/', views.remove_cart_item, name='remove_item'),
    ]