from rest_framework import permissions


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
