from rest_framework import permissions


class IsPMO(permissions.BasePermission):
    def has_permission(self, request, view):
        # Write permissions are only allowed to the PMO
        return request.user.user_type == 'PMO'


class IsOwnerOrPMO(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the PMO or Owner
        return obj == request.user or request.user.user_type == 'PMO'