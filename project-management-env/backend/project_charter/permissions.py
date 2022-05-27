from rest_framework import permissions
from guardian.shortcuts import get_user_perms


### Project Charter permissions

class hasAddProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'add_project_charter' in permissions 

class hasChangeProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'change_project_charter' in permissions 

class hasDeleteProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'delete_project_charter' in permissions 

class hasViewProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'view_project_charter' in permissions 