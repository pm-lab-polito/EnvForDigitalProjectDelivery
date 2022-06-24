from django.urls import path
from .views import *


urlpatterns = [
    path('set/<int:project_charter>/', ProjectBudgetAPI.as_view(), name='set-project-budget'),
    path('<int:pk>/delete/', DeleteProjectBudgetAPI.as_view(), name='delete-project-budget'),
    path('delete/total/<int:project_charter_pk>/', DeleteTotalProjectBudgetAPI.as_view(), 
        name='delete-total-project-budget'),
    path('<int:pk>/details/', ProjectBudgetDetailsAPI.as_view(), name='project-budget-details'),
    path('total/<int:project_charter_pk>/', TotalProjectBudgetAPI.as_view(), name='total-project-budget'),
    path('<int:pk>/edit/', EditProjectBudgetAPI.as_view(), name='edit-project-budget'),
    path('<int:pk>/actual-cost/get/', GetActualCostOfProjectByBudgetAPI.as_view(), 
        name='get-actual-cost-of-project-by-budget'),

    ##### addtional budget
    path('additional-budget/request/', RequestAdditionalBudgetAPI.as_view(), name='request-additional-budget'),
    path('additional-budget/<int:pk>/update-status/', UpdateAdditionalFundRequestStatusAPI.as_view(), 
        name='update-fund-request-status'),
    path('additional-budget/<int:pk>/get/', GetAdditionalBudgetDetailsAPI.as_view(), 
        name='get-additional-budget-details'),
    path('additional-budget/<int:project_id>/budget-requests/all/', GetAdditionalBudgetRequestsAPI.as_view(), 
        name='get-additional-budget-requests'),
    
    ##### resource spending
    path('resource-spending/add/', AddResourceSpendingAPI.as_view(), name='add-resource-spending'),
    path('resource-spending/<int:pk>/update/', UpdateResourceSpendingAPI.as_view(), 
        name='update-resource-spending'),
    path('resource-spending/<int:pk>/get/', GetResourceSpendingDetailsAPI.as_view(), 
        name='get-resource-spending-details'),
    path('resource-spending/get/list/<int:budget_id>/', GetResourceSpendingsByBudgetAPI.as_view(), 
        name='get-resource-spending-by-budget'),
    path('resource-spending/<int:pk>/delete/', DeleteResourceSpendingAPI.as_view(), 
        name='delete-resource-spending'),

    ##### contract spending
    path('contract-spending/add/', AddContractSpendingAPI.as_view(), name='add-contract-spending'),
    path('contract-spending/contract/<int:pk>/update/', UpdateContractSpendingAPI.as_view(), 
        name='update-contract-spending'),
    path('contract-spending/<int:pk>/get/', GetContractSpendingDetailsAPI.as_view(), 
        name='get-contract-spending-details'),
    path('contract-spending/get/list/<int:budget_id>/', GetContractSpendingsByBudgetAPI.as_view(), 
        name='get-contract-spending-by-budget'),
    path('contract-spending/<int:pk>/delete/', DeleteContractSpendingAPI.as_view(), 
        name='delete-contract-spending'),

    # Forecast spending
    path('<int:pk>/forecast-balance/', ForecastBalanceAPI.as_view(), 
        name='get-forecast-balance'),
    path('<int:pk>/forecast-future-spending/', ForecastFutureSpendingAPI.as_view(), 
        name='forecast-future-spending'),

]