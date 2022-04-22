from django.urls import path
from .views import (ProjectBudgetAPI, DeleteProjectBudgetAPI, DeleteTotalProjectBudgetAPI, 
                        ProjectBudgetDetailsAPI, TotalProjectBudgetAPI, EditProjectBudgetAPI)


urlpatterns = [
    path('set/', ProjectBudgetAPI.as_view(), name='set-project-budget'),
    path('delete/<int:pk>/', DeleteProjectBudgetAPI.as_view(), name='delete-project-budget'),
    path('delete/total/<int:pk>/', DeleteTotalProjectBudgetAPI.as_view(), name='delete-total-project-budget'),
    path('details/<int:pk>/', ProjectBudgetDetailsAPI.as_view(), name='project-budget-details'),
    path('total/<int:pk>/', TotalProjectBudgetAPI.as_view(), name='total-project-budget'),
    path('edit/<int:pk>/', EditProjectBudgetAPI.as_view(), name='edit-project-budget'),
    
]