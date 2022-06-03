from rest_framework import generics, status
from project_budget.models import (ProjectBudget, ResourceSpending, ContractSpending)
from .serializers import *
from rest_framework.response import Response
from custom_permissions import permissions as cust_perm
from project_charter import permissions as charter_perm
from .permissions import *
from project_charter.models import ProjectCharter
from django.http import Http404
from accounts.models import User
from projects.models import Project
from guardian.shortcuts import assign_perm, remove_perm

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





############ Resource Spending ############

class AddResourceSpendingAPI(generics.CreateAPIView):
    name = 'add-resource-spending'
    serializer_class = ResourceSpendingSerializer
    permission_classes = [hasAddProjectBudgetSpendingsPermission,]

    def create(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=request.data.get('project'))
            self.check_object_permissions(request, project)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            resource = serializer.save()

            return Response(
                {
                    'detail': 'Project resource added successfully.',
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
    permission_classes = [hasChangeProjectBudgetSpendingsPermission,]


class GetResourceSpendingDetailsAPI(generics.RetrieveAPIView):
    name = 'get-resource-spending-details'
    serializer_class = ResourceSpendingSerializer
    queryset = ResourceSpending.objects.all()
    permission_classes = [hasViewProjectBudgetSpendingsPermission,]


class GetResourceSpendingsByBudgetAPI(generics.ListAPIView):
    name = 'get-resource-spendings-by-budget'
    serializer_class = ResourceSpendingSerializer
    model = serializer_class.Meta.model
    permission_classes = [hasViewProjectBudgetSpendingsPermission,]
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
    permission_classes = [hasDeleteProjectBudgetSpendingsPermission,]




############ Contract Spending ############

class AddContractSpendingAPI(generics.CreateAPIView):
    name = 'add-contract-spending'
    serializer_class = ContractSpendingSerializer
    permission_classes = [hasAddProjectBudgetSpendingsPermission,]

    def create(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=request.data.get('project'))
            self.check_object_permissions(request, project)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            contract = serializer.save()

            return Response(
                {
                    'detail': 'Procurement contract added successfully.',
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
    permission_classes = [hasChangeProjectBudgetSpendingsPermission,]


class GetContractSpendingDetailsAPI(generics.RetrieveAPIView):
    name = 'get-contract-spending-details'
    serializer_class = ContractSpendingSerializer
    queryset = ContractSpending.objects.all()
    permission_classes = [hasViewProjectBudgetSpendingsPermission,]


class GetContractSpendingsByBudgetAPI(generics.ListAPIView):
    name = 'get-contract-spendings-by-budget'
    serializer_class = ContractSpendingSerializer
    model = serializer_class.Meta.model
    permission_classes = [hasViewProjectBudgetSpendingsPermission,]
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
    permission_classes = [hasDeleteProjectBudgetSpendingsPermission,]


############ Forecast Spendings ############

class ForecastBalanceAPI(generics.GenericAPIView):
    name = 'get-forecast-balance'
    serializer_class = ForecastBalanceSerializer
    permission_classes = [hasViewProjectBudgetSpendingsPermission,]

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


class ForecastFutureSpendingsAPI(generics.GenericAPIView):
    name = 'forecast-future-spendings'
    serializer_class = ForecastSerializer
    permission_classes = [hasViewProjectBudgetSpendingsPermission,]

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




#### Permissions #####
def validated_project_charter_permissions(permissions):
    if permissions and len(permissions) > 0:
        if ('add_project_spendings' in permissions or
            'change_project_spendings' in permissions or 
            'delete_project_spendings' in permissions or 
            'view_project_spendings' in permissions):
            return True
    return False

        
class AddProjectBudgetPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'add-project-budget-spendings-permissions'
    permission_classes = [cust_perm.IsAuthorOfProject,]

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            project_id = request.data.get('project_id')
            project = Project.objects.get(id=project_id)
            permissions = request.data.get('permissions')
            # check if a request user is a project author 
            self.check_object_permissions(request, project)
            # user is stakeholder of the project
            if user in project.stakeholders.all():
                if validated_project_charter_permissions(permissions):
                    if 'add_project_spendings' in permissions:
                            assign_perm('project_budget.add_project_spendings', user, project)

                    if 'change_project_spendings' in permissions:
                            assign_perm('project_budget.change_project_spendings', user, project)

                    if 'delete_project_spendings' in permissions:
                            assign_perm('project_budget.delete_project_spendings', user, project)

                    if 'view_project_spendings' in permissions:
                            assign_perm('project_budget.view_project_spendings', user, project)
                    
                    return Response(status=status.HTTP_201_CREATED)
                
                return Response({
                        'detail': 'Permissions is not defined correctly.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                        'detail': 'User must be a stakeholder of the project to assign permissions.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {
                    'detail': 'User does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Project.DoesNotExist:
            return Response(
                {
                    'detail': 'Project does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class DeleteProjectBudgetPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'delete-project-budget-spendings-permissions'
    permission_classes = [cust_perm.IsAuthorOfProject,]

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            project_id = request.data.get('project_id')
            project = Project.objects.get(id=project_id)
            permissions = request.data.get('permissions')
            # check if a request user is a project author 
            self.check_object_permissions(request, project)
            if validated_project_charter_permissions(permissions):
                if 'add_project_spendings' in permissions:
                        remove_perm('project_budget.add_project_spendings', user, project)

                if 'change_project_spendings' in permissions:
                        remove_perm('project_budget.change_project_spendings', user, project)

                if 'delete_project_spendings' in permissions:
                        remove_perm('project_budget.delete_project_spendings', user, project)

                if 'view_project_spendings' in permissions:
                        remove_perm('project_budget.view_project_spendings', user, project)
                
                return Response(status=status.HTTP_204_NO_CONTENT)

            
            return Response({
                    'detail': 'Permissions is not defined correctly.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {
                    'detail': 'User does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Project.DoesNotExist:
            return Response(
                {
                    'detail': 'Project does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
