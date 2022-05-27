from django.contrib import admin
from .models import ProjectCharter, BusinessCaseSWOT


class CustomProjectCharterManager(admin.ModelAdmin):
    ordering = ('project',) 
    list_display = ('project', 'sow', 'contract', 'business_case',)
    search_fields = ('project', 'author')
    readonly_fields = ('id', 'created', 'last_updated')

    filer_horizontal = ()
    list_filter = ()


class CustomBusinessCaseSWOTManager(admin.ModelAdmin):
    ordering = ('project_charter',) 
    list_display = ('project_charter', 'swot_type', 'content',)
    search_fields = ('project_charter', 'swot_type')
    readonly_fields = ('id',)

    filer_horizontal = ()
    list_filter = ()


admin.site.register(ProjectCharter, CustomProjectCharterManager)
admin.site.register(BusinessCaseSWOT, CustomBusinessCaseSWOTManager)