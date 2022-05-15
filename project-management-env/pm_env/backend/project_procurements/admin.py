from django.contrib import admin
from .models import Contract


class CustomContractManager(admin.ModelAdmin):
    ordering = ('project',) 
    list_display = ('project', 'product', 'description', 'unit_price', 'assignment', 'supplier', 'date')
    search_fields = ('project', 'product')
    readonly_fields = ('id',)

    filer_horizontal = ()
    list_filter = ()


# Register your models here.
admin.site.register(Contract, CustomContractManager)
