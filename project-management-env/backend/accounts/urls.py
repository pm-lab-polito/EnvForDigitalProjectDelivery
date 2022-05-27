from django.urls import path
from knox import views as knox_views
from .views import (RegisterAPI, LoginAPI, ActivateUserAPI, DeactivateUserAPI, 
                        UserDetailsAPI, UserListAPI, UpdateUserRoleAPI)


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    path('<int:pk>/', UserDetailsAPI.as_view(), name='user-details'),
    path('', UserListAPI.as_view(), name='user-list'),
    path('activateuser/<int:pk>/', ActivateUserAPI.as_view(), name='activate-user'),
    path('deactivateuser/<int:pk>/', DeactivateUserAPI.as_view(), name='deactivate-user'),
    path('update/user-role/<int:pk>/', UpdateUserRoleAPI.as_view(), name='update-user-role'),
]