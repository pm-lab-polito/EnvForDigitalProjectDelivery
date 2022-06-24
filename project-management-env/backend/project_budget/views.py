from rest_framework import generics, status
from project_budget.models import (ProjectBudget, ResourceSpending, ContractSpending)
from .serializers import *
from rest_framework.response import Response
from project_charter import permissions as charter_perm
from .permissions import *
from project_charter.models import ProjectCharter
from django.http import Http404
from projects.models import Project

#   Set a budget of a project charter
class ProjectBudgetAPI(generics.ListCreateAPIView):
    name = 'set-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [charter_perm.hasAddProjectCharterPermission,]

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
    permission_classes = [charter_perm.hasDeleteProjectCharterPermission,]
    queryset = ProjectBudget.objects.all()


#   Delete all budget of a project charter
class DeleteTotalProjectBudgetAPI(generics.GenericAPIView):
    name = 'delete-total-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [charter_perm.hasDeleteProjectCharterPermission,]
    
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
    permission_classes = [charter_perm.hasViewProjectCharterPermission,]
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer


#   Get total budget of a project 
class TotalProjectBudgetAPI(generics.ListAPIView): 
    name = 'total-project-budget'
    permission_classes = [charter_perm.hasViewProjectCharterPermission,]
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
    permission_classes = [charter_perm.hasViewProjectCharterPermission,]

    def get(self, request, *args, **kwargs):
        try:
            budget_id = self.kwargs.get('pk')
            budget = ProjectBudget.objects.get(id=budget_id)
            self.check_object_permissions(request, budget.project_charter)
            actual_cost = budget.actual_cost()
            return Response(actual_cost)
            
        except ProjectBudget.DoesNotExist:
            raise Http404


#   Edit a project budget
class EditProjectBudgetAPI(generics.UpdateAPIView):
    name = 'edit-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [charter_perm.hasChangeProjectCharterPermission,]
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
            status=status.HTTP_200_OK
        )





############ Additional Budget ############

class RequestAdditionalBudgetAPI(generics.CreateAPIView):
    name = 'request-additional-budget'
    serializer_class = AdditionalBudgetSerializer
    permission_classes = [hasAddAdditionalBudgetPermission,]

    def create(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=request.data.get('project'))
            self.check_object_permissions(request, project)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            budget = serializer.save()

            return Response(
                {
                    'detail': 'Additional budget request placed successfully.',
                    'additional-budget': AdditionalBudgetSerializer(budget, context=self.get_serializer_context()).data,
                },
                status=status.HTTP_201_CREATED
            )
        except Project.DoesNotExist:
            raise Http404


class UpdateAdditionalFundRequestStatusAPI(generics.UpdateAPIView):
    name = 'update-fund-request-status'
    serializer_class = AdditionalBudgetSerializer
    queryset = AdditionalBudget.objects.all()
    permission_classes = [hasChangeAdditionalBudgetPermission,]


class GetAdditionalBudgetDetailsAPI(generics.RetrieveAPIView):
    name = 'get-additional-budget-details'
    serializer_class = AdditionalBudgetViewSerializer
    queryset = AdditionalBudget.objects.all()
    permission_classes = [hasViewAdditionalBudgetPermission,]


#   Get all additional budget requests of a project 
class GetAdditionalBudgetRequestsAPI(generics.ListAPIView): 
    name = 'get-additional-budget-requests'
    permission_classes = [hasViewAdditionalBudgetPermission,]
    queryset = AdditionalBudget.objects.all()
    serializer_class = AdditionalBudgetViewSerializer
    model = serializer_class.Meta.model

    def list(self, request, project_id):
        try:
            project_charter = ProjectCharter.objects.get(project=project_id)
            budgets = ProjectBudget.objects.all().filter(project_charter=project_charter)
            qs = self.model.objects.filter(budget__in=budgets)
            serializer = AdditionalBudgetViewSerializer(qs, many=True)
            self.check_object_permissions(self.request, qs[0])
        except ProjectCharter.DoesNotExist:
            raise Http404

        return Response(serializer.data)


############ Resource Spending ############

class AddResourceSpendingAPI(generics.CreateAPIView):
    name = 'add-resource-spending'
    serializer_class = ResourceSpendingSerializer
    permission_classes = [hasAddProjectBudgetSpendingPermission,]

    def create(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=request.data.get('project'))
            self.check_object_permissions(request, project)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            resource = serializer.save()

            return Response(
                {
                    'detail': 'Resource Spending added successfully.',
                    'resource-spending': ResourceSpendingSerializer(resource, context=self.get_serializer_context()).data,
                },
                status=status.HTTP_201_CREATED
            )
        except Project.DoesNotExist:
            raise Http404


class UpdateResourceSpendingAPI(generics.UpdateAPIView):
    name = 'update-resource-spending'
    serializer_class = ResourceSpendingSerializer
    queryset = ResourceSpending.objects.all()
    permission_classes = [hasChangeProjectBudgetSpendingPermission,]


class GetResourceSpendingDetailsAPI(generics.RetrieveAPIView):
    name = 'get-resource-spending-details'
    serializer_class = ResourceSpendingSerializer
    queryset = ResourceSpending.objects.all()
    permission_classes = [hasViewProjectBudgetSpendingPermission,]


class GetResourceSpendingsByBudgetAPI(generics.ListAPIView):
    name = 'get-resource-spending-by-budget'
    serializer_class = ResourceSpendingSerializer
    model = serializer_class.Meta.model
    permission_classes = [hasViewProjectBudgetSpendingPermission,]
    lookup_url_kwarg = 'budget_id'

    def get_queryset(self):
        try:
            budget_id = self.kwargs.get('budget_id')
            budget = ProjectBudget.objects.get(id=budget_id)
            qs = self.model.objects.filter(budget=budget)
            self.check_object_permissions(self.request, qs[0])
            return qs
        except ProjectBudget.DoesNotExist:
            raise Http404


class DeleteResourceSpendingAPI(generics.DestroyAPIView):
    name = 'delete-resource-spending'
    serializer_class = ResourceSpendingSerializer
    queryset = ResourceSpending.objects.all()
    permission_classes = [hasDeleteProjectBudgetSpendingPermission,]




############ Contract Spending ############

class AddContractSpendingAPI(generics.CreateAPIView):
    name = 'add-contract-spending'
    serializer_class = ContractSpendingSerializer
    permission_classes = [hasAddProjectBudgetSpendingPermission,]

    def create(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=request.data.get('project'))
            self.check_object_permissions(request, project)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            contract = serializer.save()

            return Response(
                {
                    'detail': 'Contract Spending added successfully.',
                    'contract-spending': ContractSpendingSerializer(contract, context=self.get_serializer_context()).data,
                },
                status=status.HTTP_201_CREATED
            )
        except Project.DoesNotExist:
            raise Http404


class UpdateContractSpendingAPI(generics.UpdateAPIView):
    name = 'update-contract-spending'
    serializer_class = ContractSpendingSerializer
    queryset = ContractSpending.objects.all()
    permission_classes = [hasChangeProjectBudgetSpendingPermission,]


class GetContractSpendingDetailsAPI(generics.RetrieveAPIView):
    name = 'get-contract-spending-details'
    serializer_class = ContractSpendingSerializer
    queryset = ContractSpending.objects.all()
    permission_classes = [hasViewProjectBudgetSpendingPermission,]


class GetContractSpendingsByBudgetAPI(generics.ListAPIView):
    name = 'get-contract-spending-by-budget'
    serializer_class = ContractSpendingSerializer
    model = serializer_class.Meta.model
    permission_classes = [hasViewProjectBudgetSpendingPermission,]
    lookup_url_kwarg = 'budget_id'

    def get_queryset(self):
        try:
            budget_id = self.kwargs.get('budget_id')
            budget = ProjectBudget.objects.get(id=budget_id)
            qs = self.model.objects.filter(budget=budget)
            self.check_object_permissions(self.request, qs[0])
            return qs
        except ProjectBudget.DoesNotExist:
            raise Http404


class DeleteContractSpendingAPI(generics.DestroyAPIView):
    name = 'delete-contract-spending'
    serializer_class = ContractSpendingSerializer
    queryset = ContractSpending.objects.all()
    permission_classes = [hasDeleteProjectBudgetSpendingPermission,]


############ Forecast Spending ############

class ForecastBalanceAPI(generics.GenericAPIView):
    name = 'get-forecast-balance'
    serializer_class = ForecastBalanceSerializer
    permission_classes = [hasViewProjectBudgetSpendingPermission,]

    def post(self, request, *args, **kwargs):
        try:
            budget_id = self.kwargs.get('pk')
            budget = ProjectBudget.objects.get(pk=budget_id)
            project = budget.project_charter
            self.check_object_permissions(self.request, project)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            balance = serializer.save()
            return Response(balance)
        
        except ProjectBudget.DoesNotExist:
            raise Http404


class ForecastFutureSpendingAPI(generics.GenericAPIView):
    name = 'forecast-future-spending'
    serializer_class = ForecastSerializer
    permission_classes = [hasViewProjectBudgetSpendingPermission,]

    def post(self, request, *args, **kwargs):
        try:
            budget_id = self.kwargs.get('pk')
            budget = ProjectBudget.objects.get(pk=budget_id)
            project = budget.project_charter
            self.check_object_permissions(self.request, project)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            eva = serializer.save()
            return Response(eva)
        
        except ProjectBudget.DoesNotExist:
            raise Http404
