from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    ordering = ('email',)   # by default ordering username
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff', 'last_login')
    search_fields = ('email', 'first_name', 'last_name', 'user_type')
    readonly_fields = ('id', )

    filer_horizontal = ()
    list_filter = ()


admin.site.register(User, CustomUserAdmin)
