from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    # by default ordering username
    ordering = ('email',)   
    list_display = ('email', 'first_name', 'last_name', 'user_role', 'is_active', 'is_staff', 'last_login')
    search_fields = ('email', 'first_name', 'last_name', 'user_role')
    readonly_fields = ('id', 'last_login', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('id', 'email', 'password', 'first_name', 'last_name', 
            'user_role', 'is_active', 'is_staff', 'last_login', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 
                'user_role', 'is_active', 'is_staff', 'last_login', 'is_superuser'),
        }),
    )    
    filer_horizontal = ()
    list_filter = ()


admin.site.register(User, CustomUserAdmin)
