from django.urls import path, include
from .views import (ProjectCharterAPI, DeleteProjectCharterAPI, EditProjectCharterAPI, 
                        BusinessCaseSWOTAPI, DeleteBusinessCaseSWOTAPI, SWOTDetailsAPI, 
                        SWOTListOfProjectCharterAPI, ProjectCharterDetailsAPI, 
                        AddProjectCharterPermissionsOfUserAPI, DeleteProjectCharterPermissionsOfUserAPI)


urlpatterns = [
    path('create/', ProjectCharterAPI.as_view(), name='create-project-charter'),
    path('delete/<int:pk>/', DeleteProjectCharterAPI.as_view(), name='delete-project-charter'),
    path('edit/<int:pk>/', EditProjectCharterAPI.as_view(), name='edit-project-charter'),
    path('details/<int:pk>/', ProjectCharterDetailsAPI.as_view(), name='details-project-charter'),
    path('swot/add/', BusinessCaseSWOTAPI.as_view(), name='add-business-case-swot'),
    path('swot/delete/<int:pk>/', DeleteBusinessCaseSWOTAPI.as_view(), name='delete-swot'),
    path('swot/<int:pk>/', SWOTDetailsAPI.as_view(), name='swot-details'),
    path('swot/list/<int:project_charter_pk>/', SWOTListOfProjectCharterAPI.as_view(), name='swot-list-of-project-charter'),
    path('permissions/add/', AddProjectCharterPermissionsOfUserAPI.as_view(), 
        name='add-project-charter-permissions'),
    path('permissions/delete/', DeleteProjectCharterPermissionsOfUserAPI.as_view(), 
        name='delete-project-charter-permissions'),

    path('budget/', include('project_budget.urls'), name='project-budget'),
]