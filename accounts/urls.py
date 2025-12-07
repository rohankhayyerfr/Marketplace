from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path("verify/", views.verify_identity, name='verify_identity'),
    path("verify/status/", views.verification_status, name='verify_status'),

]