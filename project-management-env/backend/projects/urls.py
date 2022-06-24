from django.urls import path, include
from .views import (ProjectAPI, EditProjectAPI, DeleteProjectAPI, ProjectDetailsAPI,
                        AddProjectPermissionsOfUserAPI, GetProjectPermissionsOfUserAPI,
                        DeleteProjectPermissionsOfUserAPI, AddStakeholdersToProjectAPI, 
                        RemoveStakeholdersFromProjectAPI, GetStakeholdersOfProjectAPI, 
                        GetProjectsOfStakeholderAPI, AssignAllProjectPermissionsToStakeholderAPI,
                        GetActualCostOfProjectAPI)


urlpatterns = [
    path('create/', ProjectAPI.as_view(), name='create-project'),
    path('<int:pk>/delete/', DeleteProjectAPI.as_view(), name='delete-project'),
    path('<int:pk>/edit/', EditProjectAPI.as_view(), name='edit-project-name'),
    path('<int:pk>/details/', ProjectDetailsAPI.as_view(), name='project-details'),
    path('myprojects/', GetProjectsOfStakeholderAPI.as_view(), 
        name='get-projects-of-stakeholder'),
    path('<int:project_id>/stakeholders/add/', AddStakeholdersToProjectAPI.as_view(), 
        name='add-project-stakeholders'),
    path('<int:project_id>/stakeholders/remove/', RemoveStakeholdersFromProjectAPI.as_view(), 
        name='remove-project-stakeholders'),
    path('<int:project_id>/stakeholders/get/', GetStakeholdersOfProjectAPI.as_view(), 
            name='get-stakeholders-of-project'),
    path('<int:pk>/actual-cost/get/', GetActualCostOfProjectAPI.as_view(), name='get-actual-cost-of-project'),
    
    path('permissions/add/', AddProjectPermissionsOfUserAPI.as_view(), name='add-project-permissions'),
    path('permissions/assign-all/', AssignAllProjectPermissionsToStakeholderAPI.as_view(), 
        name='assign-all-project-permissions'),
    path('<int:project_id>/user/<int:user_id>/permissions/get/', GetProjectPermissionsOfUserAPI.as_view(), 
        name='get-project-permissions'),
    path('permissions/delete/', DeleteProjectPermissionsOfUserAPI.as_view(), 
        name='delete-project-permissions'),
    
    path('project-charter/', include('project_charter.urls'), name='project-charter'),
    path('resources/', include('project_resources.urls'), name='project-resources'),
    path('procurements/', include('project_procurements.urls'), name='procurements'),
]