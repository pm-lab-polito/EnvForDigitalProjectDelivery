from django.contrib import admin
from .models import Project


class CustomProjectManager(admin.ModelAdmin):
    ordering = ('project_name',) 
    list_display = ('project_name', 'author', 'created')
    search_fields = ('project_name', 'author')
    readonly_fields = ('id', 'created')

    filer_horizontal = ()
    list_filter = ()


# Register your models here.
admin.site.register(Project, CustomProjectManager)
