from rest_framework import generics, status
from project_budget.models import (ProjectBudget, ResourceSpending, ContractSpending)
from .serializers import (ProjectBudgetSerializer, ResourceSpendingSerializer, ContractSpendingSerializer)
from rest_framework.response import Response
import custom_permissions.permissions as custom_perm
from project_charter.models import ProjectCharter
from django.http import Http404

#   Set a budget of a project charter
class ProjectBudgetAPI(generics.ListCreateAPIView):
    name = 'set-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [custom_perm.hasAddProjectCharterPermission |
        custom_perm.hasChangeProjectCharterPermission | custom_perm.hasChangeProjectPermission,]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        
        project_charter_id = self.kwargs.get('project_charter')
        try:
            project_charter = ProjectCharter.objects.get(id=project_charter_id)
            self.check_object_permissions(self.request, project_charter)
        except ProjectCharter.DoesNotExist:
            raise Http404

        if isinstance(self.request.data, list):
            for attrs in self.request.data:
                attrs["project_charter"]=project_charter_id 
        else: 
            self.request.data["project_charter"]=project_charter_id 

        return super(ProjectBudgetAPI, self).get_serializer(*args, **kwargs)



#   Delete a single instance of a project budget
class DeleteProjectBudgetAPI(generics.DestroyAPIView):
    name = 'delete-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [custom_perm.hasDeleteProjectCharterPermission | 
        custom_perm.hasDeleteProjectPermission,]
    queryset = ProjectBudget.objects.all()


#   Delete all budget of a project charter
class DeleteTotalProjectBudgetAPI(generics.GenericAPIView):
    name = 'delete-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [custom_perm.hasDeleteProjectCharterPermission | 
        custom_perm.hasDeleteProjectPermission,]
    
    def delete(self, request, project_charter_pk, *args, **kwargs):
        try:
            project_charter = ProjectCharter.objects.get(id=project_charter_pk)
            self.check_object_permissions(request, project_charter)
        except ProjectCharter.DoesNotExist:
            raise Http404
            
        total_budget = ProjectBudget.objects.all().filter(project_charter=project_charter_pk)
        if total_budget.count() > 0:
            total_budget.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


#   Get a single instance of a project budget
class ProjectBudgetDetailsAPI(generics.RetrieveAPIView): 
    name = 'project-budget-details'
    permission_classes = [custom_perm.hasViewProjectCharterPermission | 
        custom_perm.hasViewProjectPermission,]
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer


#   Get total budget of a project 
class TotalProjectBudgetAPI(generics.ListAPIView): 
    name = 'total-project-budget'
    permission_classes = [custom_perm.hasViewProjectCharterPermission | 
        custom_perm.hasViewProjectPermission,]
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer

    def list(self, request, project_charter_pk):
        qs = self.get_queryset().filter(project_charter=project_charter_pk)
        serializer = ProjectBudgetSerializer(qs, many=True)
        try:
            project_charter = ProjectCharter.objects.get(id=project_charter_pk)
            self.check_object_permissions(request, project_charter)
        except ProjectCharter.DoesNotExist:
            raise Http404

        return Response(serializer.data)


class GetActualCostOfProjectByBudgetAPI(generics.GenericAPIView):
    name = 'get-actual-cost-of-project-by-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            budget_id = self.kwargs.get('pk')
            budget = ProjectBudget.objects.get(id=budget_id)
            actual_cost = budget.actual_cost()
            return Response(actual_cost)
            
        except ProjectBudget.DoesNotExist:
            raise Http404


#   Edit a project budget
class EditProjectBudgetAPI(generics.UpdateAPIView):
    name = 'edit-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [custom_perm.hasChangeProjectCharterPermission | 
        custom_perm.hasChangeProjectPermission,]
    queryset = ProjectBudget.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Project budget updated successfully"
            },  
            status=status.HTTP_204_NO_CONTENT
        )





############ Resource Spending ############

class AddResourceSpendingAPI(generics.CreateAPIView):
    name = 'add-resource-spending'
    serializer_class = ResourceSpendingSerializer
    permission_classes = []


class UpdateResourceSpendingAPI(generics.UpdateAPIView):
    name = 'update-resource-spending'
    serializer_class = ResourceSpendingSerializer
    queryset = ResourceSpending.objects.all()
    permission_classes = []


class GetResourceSpendingDetailsAPI(generics.RetrieveAPIView):
    name = 'get-resource-spending-details'
    serializer_class = ResourceSpendingSerializer
    queryset = ResourceSpending.objects.all()
    permission_classes = []


class GetResourceSpendingsByBudgetAPI(generics.ListAPIView):
    name = 'get-resource-spendings-by-budget'
    serializer_class = ResourceSpendingSerializer
    model = serializer_class.Meta.model
    permission_classes = []
    lookup_url_kwarg = 'budget_id'

    def get_queryset(self):
        try:
            budget_id = self.kwargs.get('budget_id')
            budget = ProjectBudget.objects.get(id=budget_id)
            qs = self.model.objects.filter(budget=budget)
            return qs
        except ProjectBudget.DoesNotExist:
            raise Http404


class DeleteResourceSpendingAPI(generics.DestroyAPIView):
    name = 'delete-resource-spending'
    serializer_class = ResourceSpendingSerializer
    queryset = ResourceSpending.objects.all()
    permission_classes = []




############ Contract Spending ############

class AddContractSpendingAPI(generics.CreateAPIView):
    name = 'add-contract-spending'
    serializer_class = ContractSpendingSerializer
    permission_classes = []


class UpdateContractSpendingAPI(generics.UpdateAPIView):
    name = 'update-contract-spending'
    serializer_class = ContractSpendingSerializer
    queryset = ContractSpending.objects.all()
    permission_classes = []


class GetContractSpendingDetailsAPI(generics.RetrieveAPIView):
    name = 'get-contract-spending-details'
    serializer_class = ContractSpendingSerializer
    queryset = ContractSpending.objects.all()
    permission_classes = []


class GetContractSpendingsByBudgetAPI(generics.ListAPIView):
    name = 'get-contract-spendings-by-budget'
    serializer_class = ContractSpendingSerializer
    model = serializer_class.Meta.model
    permission_classes = []
    lookup_url_kwarg = 'budget_id'

    def get_queryset(self):
        try:
            budget_id = self.kwargs.get('budget_id')
            budget = ProjectBudget.objects.get(id=budget_id)
            qs = self.model.objects.filter(budget=budget)
            return qs
        except ProjectBudget.DoesNotExist:
            raise Http404


class DeleteContractSpendingAPI(generics.DestroyAPIView):
    name = 'delete-contract-spending'
    serializer_class = ContractSpendingSerializer
    queryset = ContractSpending.objects.all()
    permission_classes = []