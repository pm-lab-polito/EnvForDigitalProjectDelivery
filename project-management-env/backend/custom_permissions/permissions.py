from rest_framework import permissions
from guardian.shortcuts import get_user_perms
from accounts.models import User


class IsProjectManagementOffice(permissions.BasePermission):
    def has_permission(self, request, view):
        # Write permissions are only allowed to the PMO
        return request.user.is_authenticated and request.user.user_role == 'PMO'


class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Write permissions are only allowed to the PM
        return request.user.is_authenticated and request.user.user_role == 'PM'

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the Owner
        return request.user == obj

class IsOwnerOrProjectManagementOffice(permissions.BasePermission): 
     #  Allow access to pmo and owners
     def has_object_permission(self, request, view, obj):
         return (IsProjectManagementOffice.has_permission(self, request, view) or
                IsOwner.has_object_permission(self, request, view, obj))




class IsOwnerOfUserAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = obj.get('user')
        return request.user == user

class IsAuthorOfProject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if isinstance(obj, dict):
            project = obj.get('project')            
        return request.user == project.author
        

class hasAddProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'add_project' in permissions 


class hasChangeProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'change_project' in permissions 


class hasDeleteProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'delete_project' in permissions 


class hasViewProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'view_project' in permissions 