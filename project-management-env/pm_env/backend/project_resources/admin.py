from django.contrib import admin
from .models import Resource


class CustomResourceManager(admin.ModelAdmin):
    ordering = ('project',) 
    list_display = ('project', 'name', 'description', 'cost', 'category')
    search_fields = ('project', 'name', 'category')
    readonly_fields = ('id',)

    filer_horizontal = ()
    list_filter = ()


# Register your models here.
admin.site.register(Resource, CustomResourceManager)
