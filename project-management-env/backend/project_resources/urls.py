from django.urls import path
from .views import (AddResourceAPI, RemoveResourceAPI, UpdateResourceAPI, GetResourceAPI,
                    GetResourceListOfProjectAPI, AddProjectResourcePermissionsOfUserAPI, 
                    DeleteProjectResourcePermissionsOfUserAPI)


urlpatterns = [
    path('add/', AddResourceAPI.as_view(), name='add-resource'),
    path('remove/<int:pk>/', RemoveResourceAPI.as_view(), name='remove-resource'),
    path('update/<int:pk>/', UpdateResourceAPI.as_view(), name='update-resource'),
    path('get/<int:pk>/', GetResourceAPI.as_view(), name='get-resource'),
    path('get/list/<int:project_id>/', GetResourceListOfProjectAPI.as_view(), 
        name='get-resource-list-of-project'),
    
    path('permissions/add/', AddProjectResourcePermissionsOfUserAPI.as_view(), 
        name='add-project-resource-permissions'),
    path('permissions/delete/', DeleteProjectResourcePermissionsOfUserAPI.as_view(),
        name='delete-project-resource-permissions'),

]