from django.urls import path, include
from .views import *


urlpatterns = [
    path('create/', ProjectCharterAPI.as_view(), name='create-project-charter'),
    path('<int:pk>/delete/', DeleteProjectCharterAPI.as_view(), name='delete-project-charter'),
    path('<int:pk>/edit/', EditProjectCharterAPI.as_view(), name='edit-project-charter'),
    path('<int:pk>/details/', ProjectCharterDetailsAPI.as_view(), name='details-project-charter'),
    path('swot/add/', BusinessCaseSWOTAPI.as_view(), name='add-business-case-swot'),
    path('swot/<int:pk>/delete/', DeleteBusinessCaseSWOTAPI.as_view(), name='delete-swot'),
    path('swot/<int:pk>/', SWOTDetailsAPI.as_view(), name='swot-details'),
    path('<int:project_charter_pk>/swot/list/', SWOTListOfProjectCharterAPI.as_view(), name='swot-list-of-project-charter'),
    

    path('budget/', include('project_budget.urls'), name='project-budget'),
]