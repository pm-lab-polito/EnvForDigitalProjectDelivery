from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from .serializers import ContractSerializer
from .models import Contract
from projects.models import Project
from accounts.models import User
from custom_permissions import permissions as cust_perm
from .permissions import *
from guardian.shortcuts import assign_perm, remove_perm


class AddContractAPI(generics.CreateAPIView):
    name = 'add-contract'
    serializer_class = ContractSerializer
    permission_classes = [hasAddProjectContractPermission,]

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(request, serializer.validated_data.get('project'))
        contract = serializer.save()

        return Response(
            {
                'detail': 'Contract added successfully.',
                'resource': ContractSerializer(contract, 
                                        context=self.get_serializer_context()).data,
            },
            status=status.HTTP_201_CREATED
        )


class UpdateContractAPI(generics.UpdateAPIView):
    name= 'update-contract'
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [hasChangeProjectContractPermission,]


class GetContractDetailsAPI(generics.RetrieveAPIView):
    name = 'get-contract-details'
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [hasViewProjectContractPermission,]


class GetContractsOfProjectAPI(generics.ListAPIView):
    name = 'get-contracts-of-project'
    serializer_class = ContractSerializer
    model = serializer_class.Meta.model
    permission_classes = [hasViewProjectContractPermission,]
    lookup_url_kwarg = 'project_id'

    def get_queryset(self):
        try:
            project_id = self.kwargs.get('project_id')
            project = Project.objects.get(id=project_id)
            queryset = self.model.objects.filter(project=project)
            self.check_object_permissions(self.request, queryset[0])
            return queryset
        except Project.DoesNotExist:
            raise Http404


class DeleteContractAPI(generics.DestroyAPIView):
    name = 'delete-contract'
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [hasDeleteProjectContractPermission,]



#### Permissions #####
def validated_project_charter_permissions(permissions):
    if permissions and len(permissions) > 0:
        if ('add_project_contract' in permissions or
            'change_project_contract' in permissions or 
            'delete_project_contract' in permissions or 
            'view_project_contract' in permissions):
            return True
    return False

        
class AddProjectContractPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'add-project-contract-permissions'
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
                    if 'add_project_contract' in permissions:
                            assign_perm('project_procurements.add_project_contract', user, project)

                    if 'change_project_contract' in permissions:
                            assign_perm('project_procurements.change_project_contract', user, project)

                    if 'delete_project_contract' in permissions:
                            assign_perm('project_procurements.delete_project_contract', user, project)

                    if 'view_project_contract' in permissions:
                            assign_perm('project_procurements.view_project_contract', user, project)
                    
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


class DeleteProjectContractPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'delete-project-contract-permissions'
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
                if 'add_project_contract' in permissions:
                        remove_perm('project_procurements.add_project_contract', user, project)

                if 'change_project_contract' in permissions:
                        remove_perm('project_procurements.change_project_contract', user, project)

                if 'delete_project_contract' in permissions:
                        remove_perm('project_procurements.delete_project_contract', user, project)

                if 'view_project_contract' in permissions:
                        remove_perm('project_procurements.view_project_contract', user, project)
                
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