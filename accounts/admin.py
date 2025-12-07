from django.contrib import admin

from .models import *

@admin.register(SellerVerification)
class SellerVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', "created_at")
    list_filter = ('status',)
    search_fields = ('user__username',"full_name", "phone")