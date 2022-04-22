from django.urls import path, include
from .views import (ProjectAPI, EditProjectAPI, DeleteProjectAPI, ProjectDetailsAPI,
                        ProjectListAPI)


urlpatterns = [
    path('create/', ProjectAPI.as_view(), name='create-project'),
    path('delete/<int:pk>/', DeleteProjectAPI.as_view(), name='delete-project'),
    path('edit/<int:pk>/', EditProjectAPI.as_view(), name='edit-project-name'),
    path('details/<int:pk>/', ProjectDetailsAPI.as_view(), name='project-details'),
    path('list/', ProjectListAPI.as_view(), name='project-list'),
    
    path('project-charter/', include('project_charter.urls'), name='project-charter'),
]