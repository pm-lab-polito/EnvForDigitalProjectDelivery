from rest_framework import permissions
from guardian.shortcuts import get_user_perms

### Additional Budget permissions

class hasAddAdditionalBudgetPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'add_additional_budget' in permissions 

class hasChangeAdditionalBudgetPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.budget.project_charter.project
        permissions = get_user_perms(request.user, project)
        return 'change_additional_budget' in permissions 

class hasViewAdditionalBudgetPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.budget.project_charter.project
        permissions = get_user_perms(request.user, project)
        return 'view_additional_budget' in permissions 

        

### Project Spending permissions

class hasAddProjectBudgetSpendingPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permissions = get_user_perms(request.user, obj)
        return 'add_project_spending' in permissions 

class hasChangeProjectBudgetSpendingPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'change_project_spending' in permissions 

class hasDeleteProjectBudgetSpendingPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'delete_project_spending' in permissions 

class hasViewProjectBudgetSpendingPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project
        permissions = get_user_perms(request.user, project)
        return 'view_project_spending' in permissions 