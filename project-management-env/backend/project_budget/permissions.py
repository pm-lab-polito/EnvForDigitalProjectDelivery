from rest_framework import permissions
from guardian.shortcuts import get_user_perms


### Project Spendings permissions

class hasAddProjectBudgetSpendingsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'add_project_spendings' in permissions 

class hasChangeProjectBudgetSpendingsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'change_project_spendings' in permissions 

class hasDeleteProjectBudgetSpendingsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'delete_project_spendings' in permissions 

class hasViewProjectBudgetSpendingsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'view_project_spendings' in permissions 