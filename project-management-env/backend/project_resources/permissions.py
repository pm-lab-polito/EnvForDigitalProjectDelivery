from rest_framework import permissions
from guardian.shortcuts import get_user_perms


### Project Resource permissions

class hasAddProjectResourcePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'add_project_resource' in permissions 

class hasChangeProjectResourcePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'change_project_resource' in permissions 

class hasDeleteProjectResourcePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'delete_project_resource' in permissions 

class hasViewProjectResourcePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'view_project_resource' in permissions 
