# services/admin.py

from django.contrib import admin
from .models import Category, Service

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'seller')
    search_fields = ('title', 'description', 'seller__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    # Fieldsets to organize the admin form
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description')
        }),
        ('Pricing & Category', {
            'fields': ('category', 'price', 'cover_image')
        }),
        ('Status', {
            'fields': ('is_active', 'seller'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Automatically set the seller to the logged-in user if not already set
        if not obj.seller_id:
            obj.seller = request.user
        super().save_model(request, obj, form, change)