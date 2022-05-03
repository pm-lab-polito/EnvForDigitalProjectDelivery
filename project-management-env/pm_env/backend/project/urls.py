from django.urls import path, include
from .views import (ProjectAPI, EditProjectAPI, DeleteProjectAPI, ProjectDetailsAPI,
                        ProjectListAPI, AddProjectPermissionsOfUserAPI, GetProjectPermissionsOfUserAPI,
                        DeleteProjectPermissionsOfUserAPI,)


urlpatterns = [
    path('create/', ProjectAPI.as_view(), name='create-project'),
    path('delete/<int:pk>/', DeleteProjectAPI.as_view(), name='delete-project'),
    path('edit/<int:pk>/', EditProjectAPI.as_view(), name='edit-project-name'),
    path('details/<int:pk>/', ProjectDetailsAPI.as_view(), name='project-details'),
    path('list/', ProjectListAPI.as_view(), name='project-list'),
    path('permissions/add/', AddProjectPermissionsOfUserAPI.as_view(), name='add-project-permissions'),
    path('permissions/get/<int:user_id>/<int:project_id>/', GetProjectPermissionsOfUserAPI.as_view(), 
        name='get-project-permissions'),
    path('permissions/delete/', DeleteProjectPermissionsOfUserAPI.as_view(), 
        name='delete-project-permissions'),
    
    path('project-charter/', include('project_charter.urls'), name='project-charter'),
]