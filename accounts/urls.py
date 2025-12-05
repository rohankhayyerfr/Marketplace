from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('become_seller/', views.become_seller, name='become_seller'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]