from django.urls import path
from .views import (ProjectBudgetAPI, DeleteProjectBudgetAPI, DeleteTotalProjectBudgetAPI, 
                        ProjectBudgetDetailsAPI, TotalProjectBudgetAPI, EditProjectBudgetAPI, 
                        AddResourceSpendingAPI, UpdateResourceSpendingAPI, GetResourceSpendingDetailsAPI,
                        DeleteResourceSpendingAPI, GetResourceSpendingsByBudgetAPI, AddContractSpendingAPI, 
                        UpdateContractSpendingAPI, GetContractSpendingDetailsAPI, GetContractSpendingsByBudgetAPI,
                        DeleteContractSpendingAPI, GetActualCostOfProjectByBudgetAPI)


urlpatterns = [
    path('set/<int:project_charter>/', ProjectBudgetAPI.as_view(), name='set-project-budget'),
    path('delete/<int:pk>/', DeleteProjectBudgetAPI.as_view(), name='delete-project-budget'),
    path('delete/total/<int:project_charter_pk>/', DeleteTotalProjectBudgetAPI.as_view(), 
        name='delete-total-project-budget'),
    path('details/<int:pk>/', ProjectBudgetDetailsAPI.as_view(), name='project-budget-details'),
    path('total/<int:project_charter_pk>/', TotalProjectBudgetAPI.as_view(), name='total-project-budget'),
    path('edit/<int:pk>/', EditProjectBudgetAPI.as_view(), name='edit-project-budget'),
    path('<int:pk>/get/actual-cost/', GetActualCostOfProjectByBudgetAPI.as_view(), 
        name='get-actual-cost-of-project-by-budget'),
    
    ##### resource spendings
    path('resource-spendings/add/', AddResourceSpendingAPI.as_view(), name='add-resource-spending'),
    path('resource-spendings/<int:pk>/update/', UpdateResourceSpendingAPI.as_view(), 
        name='update-resource-spending'),
    path('resource-spendings/<int:pk>/get/', GetResourceSpendingDetailsAPI.as_view(), name='get-resource-spending'),
    path('resource-spendings/<int:budget_id>/get/list/', GetResourceSpendingsByBudgetAPI.as_view(), 
        name='get-resource-spendings-by-budget'),
    path('resource-spendings/<int:pk>/delete/', DeleteResourceSpendingAPI.as_view(), 
        name='delete-resource-spending'),

    ##### contract spendings
    path('contract-spendings/add/', AddContractSpendingAPI.as_view(), name='add-contract-spending'),
    path('contract-spendings/contract/<int:pk>/update/', UpdateContractSpendingAPI.as_view(), 
        name='update-contract-spending'),
    path('contract-spendings/<int:pk>/get/', GetContractSpendingDetailsAPI.as_view(), 
        name='get-contract-spending-details'),
    path('contract-spendings/<int:budget_id>/get/list/', GetContractSpendingsByBudgetAPI.as_view(), 
        name='get-contract-spendings-by-budget'),
    path('contract-spendings/<int:pk>/delete/', DeleteContractSpendingAPI.as_view(), 
        name='delete-contract-spending'),
]