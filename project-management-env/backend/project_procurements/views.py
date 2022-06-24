from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from .serializers import ContractSerializer
from .models import Contract
from projects.models import Project
from .permissions import *


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
                'contract': ContractSerializer(contract, 
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
