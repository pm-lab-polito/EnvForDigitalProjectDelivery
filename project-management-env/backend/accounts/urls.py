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
    path('<int:pk>/activateuser/', ActivateUserAPI.as_view(), name='activate-user'),
    path('<int:pk>/deactivateuser/', DeactivateUserAPI.as_view(), name='deactivate-user'),
    path('<int:pk>/user-role/update/', UpdateUserRoleAPI.as_view(), name='update-user-role'),
]