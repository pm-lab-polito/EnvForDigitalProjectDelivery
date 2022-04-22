from django.contrib import admin
from .models import ProjectBudget


class CustomProjectBudgetManager(admin.ModelAdmin):
    ordering = ('project_charter',) 
    list_display = ('project_charter', 'year', 'budget')
    search_fields = ('project_charter', 'year')
    readonly_fields = ('id',)

    filer_horizontal = ()
    list_filter = ()


# Register your models here.
admin.site.register(ProjectBudget, CustomProjectBudgetManager)
