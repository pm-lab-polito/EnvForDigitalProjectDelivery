from django.urls import path
from .views import *


urlpatterns = [
    path('add/', AddResourceAPI.as_view(), name='add-resource'),
    path('<int:pk>/remove/', RemoveResourceAPI.as_view(), name='remove-resource'),
    path('<int:pk>/update/', UpdateResourceAPI.as_view(), name='update-resource'),
    path('<int:pk>/get/', GetResourceAPI.as_view(), name='get-resource'),
    path('get/list/<int:project_id>/', GetResourceListOfProjectAPI.as_view(), 
        name='get-resource-list-of-project'),

]