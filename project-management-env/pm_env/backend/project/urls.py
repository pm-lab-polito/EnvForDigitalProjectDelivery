from django.urls import path, include
from .views import (ProjectAPI, EditProjectAPI, DeleteProjectAPI, ProjectDetailsAPI,
                        AddProjectPermissionsOfUserAPI, GetProjectPermissionsOfUserAPI,
                        DeleteProjectPermissionsOfUserAPI, AddStakeholdersToProjectAPI, 
                        RemoveStakeholdersFromProjectAPI, GetStakeholdersOfProjectAPI, 
                        GetProjectsOfStakeholderAPI, AssignAllProjectPermissionsToStakeholderAPI)


urlpatterns = [
    path('create/', ProjectAPI.as_view(), name='create-project'),
    path('delete/<int:pk>/', DeleteProjectAPI.as_view(), name='delete-project'),
    path('edit/<int:pk>/', EditProjectAPI.as_view(), name='edit-project-name'),
    path('details/<int:pk>/', ProjectDetailsAPI.as_view(), name='project-details'),
    path('myprojects/<int:user_id>/', GetProjectsOfStakeholderAPI.as_view(), 
        name='get-projects-of-stakeholder'),
    path('stakeholders/add/<int:project_id>/', AddStakeholdersToProjectAPI.as_view(), 
        name='add-project-stakeholders'),
    path('stakeholders/remove/<int:project_id>/', RemoveStakeholdersFromProjectAPI.as_view(), 
        name='remove-project-stakeholders'),
    path('stakeholders/get/<int:project_id>/', GetStakeholdersOfProjectAPI.as_view(), 
            name='get-stakeholders-of-project'),
    path('permissions/add/', AddProjectPermissionsOfUserAPI.as_view(), name='add-project-permissions'),
    path('permissions/assign-all/', AssignAllProjectPermissionsToStakeholderAPI.as_view(), 
        name='assign-all-project-permissions'),
    path('permissions/get/user/<int:user_id>/project/<int:project_id>/', GetProjectPermissionsOfUserAPI.as_view(), 
        name='get-project-permissions'),
    path('permissions/delete/', DeleteProjectPermissionsOfUserAPI.as_view(), 
        name='delete-project-permissions'),
    
    path('project-charter/', include('project_charter.urls'), name='project-charter'),
    path('resources/', include('resources.urls'), name='resources'),
]