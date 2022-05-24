from rest_framework import permissions
from guardian.shortcuts import get_user_perms


### Project Contract permissions

class hasAddProjectContractPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'add_project_contract' in permissions 

class hasChangeProjectContractPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'change_project_contract' in permissions 

class hasDeleteProjectContractPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'delete_project_contract' in permissions 

class hasViewProjectContractPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'view_project_contract' in permissions 