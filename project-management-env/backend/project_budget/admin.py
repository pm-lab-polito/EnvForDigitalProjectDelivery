from django.contrib import admin
from .models import ProjectBudget, ResourceSpending, ContractSpending


class CustomProjectBudgetManager(admin.ModelAdmin):
    ordering = ('project_charter',) 
    list_display = ('project_charter', 'year', 'budget')
    search_fields = ('project_charter', 'year')
    readonly_fields = ('id',)

    filer_horizontal = ()
    list_filter = ()


# Register your models here.
admin.site.register(ProjectBudget, CustomProjectBudgetManager)


class CustomResourceSpendingManager(admin.ModelAdmin):
    ordering = ('project', 'budget') 
    list_display = ('project', 'resource', 'budget', 'assignment', 'amount', 'description', 'date', 'approval_status')
    search_fields = ('project', 'resource', 'budget')
    readonly_fields = ('id',)

    filer_horizontal = ()
    list_filter = ()


admin.site.register(ResourceSpending, CustomResourceSpendingManager)


class CustomContractSpendingManager(admin.ModelAdmin):
    ordering = ('project', 'budget') 
    list_display = ('project', 'contract', 'budget', 'amount', 'description', 'date', 'approval_status')
    search_fields = ('project', 'contract', 'budget')
    readonly_fields = ('id',)

    filer_horizontal = ()
    list_filter = ()


admin.site.register(ContractSpending, CustomContractSpendingManager)