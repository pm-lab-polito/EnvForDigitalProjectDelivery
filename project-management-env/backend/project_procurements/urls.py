from django.urls import path
from .views import *

urlpatterns = [
    path('contracts/add/', AddContractAPI.as_view(), name='add-contract'),
    path('contracts/<int:pk>/update/', UpdateContractAPI.as_view(), name='update-contract'),
    path('contracts/<int:pk>/get/', GetContractDetailsAPI.as_view(), name='get-contract-details'),
    path('project/<int:project_id>/contracts/get/', GetContractsOfProjectAPI.as_view(), 
        name='get-contracts-of-project'),
    path('contracts/<int:pk>/delete/', DeleteContractAPI.as_view(), name='delete-contract'),

]