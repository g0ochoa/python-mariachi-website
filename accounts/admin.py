from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register custom User model with Django admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for User model.
    Extends Django's built-in UserAdmin with our custom fields.
    """
    # Fields to display in the user list
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_test_account', 'is_guest', 'active_from', 'active_until')

    # Filters in the right sidebar
    list_filter = ('role', 'is_staff', 'is_active', 'promo_opt_in', 'is_test_account', 'is_guest')
    
    # Search functionality
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    
    # Organize fields in the edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Permissions', {
            'fields': ('role',)
        }),
        ('Customer Information', {
            'fields': ('phone', 'promo_opt_in'),
            'description': 'Fields for customer accounts'
        }),
        ('Musician Information', {
            'fields': ('instrument', 'google_id', 'default_hourly_rate', 'active_from', 'active_until', 'is_test_account', 'is_guest'),
            'description': 'Fields for musician accounts (band members)'
        }),
    )
    
    # Fields shown when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {
            'fields': ('role',)
        }),
    )

