from rest_framework import permissions
from guardian.shortcuts import get_user_perms
from accounts.models import User
from projects.models import Project


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



class RequestSenderIsRequestedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_id = request.resolver_match.kwargs.get('user_id')
            user = User.objects.get(id=user_id)
            return request.user == user
            
        except User.DoesNotExist:
            return False

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
        

class hasChangeProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'change_project' in permissions 

class hasDeleteProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'delete_project' in permissions 

class hasViewProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'view_project' in permissions 



### Project Charter permissions

class hasAddProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'add_project_charter' in permissions 

class hasChangeProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'change_project_charter' in permissions 

class hasDeleteProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'delete_project_charter' in permissions 

class hasViewProjectCharterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'project_charter'):
            project = obj.project_charter.project
        elif hasattr(obj, 'project'):
            project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'view_project_charter' in permissions 



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

class hasViewProjectResourceListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            project_id = request.resolver_match.kwargs.get('project_id')
            project = Project.objects.get(id=project_id)
            permissions = get_user_perms(request.user, project)
            return 'view_project_resource' in permissions
            
        except Project.DoesNotExist:
            return False