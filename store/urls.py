from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "store"

urlpatterns = [
    # Public views

    path('', views.home, name='home'),
    path('product_list/', views.product_list, name="product_list"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:pk>/', views.category_products, name='category'),
    # Dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/products/create/', views.product_create, name="product_create"),
    path("dashboard/products/<int:pk>/edit/", views.product_edit, name="product_edit"),

    path("dashboard/products/<int:pk>/delete/", views.product_delete, name="delete_product"),
    #other pages
    path('faqs/', views.faqs, name="faqs"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
