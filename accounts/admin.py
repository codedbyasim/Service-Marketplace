# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

# Inline profile editing on the User admin page
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    # Add custom fields to the list display
    list_display = BaseUserAdmin.list_display + ('is_seller', 'is_client')
    list_filter = BaseUserAdmin.list_filter + ('is_seller', 'is_client')

    # Add custom fields to the user editing page
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('is_seller', 'is_client')}),
    )
    
    # Ensure profile image can be uploaded via admin
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'bio', 'profile_image')
    search_fields = ('user__username', 'full_name')