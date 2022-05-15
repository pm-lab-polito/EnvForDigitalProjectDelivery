from rest_framework import generics
from .serializers import ContractSerializer
from .models import Contract
from projects.models import Project
from django.http import Http404


class AddContractAPI(generics.CreateAPIView):
    name = 'add-contract'
    serializer_class = ContractSerializer
    permission_classes = []


class UpdateContractAPI(generics.UpdateAPIView):
    name= 'update-contract'
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = []


class GetContractDetailsAPI(generics.RetrieveAPIView):
    name = 'get-contract-details'
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = []


class GetContractsOfProjectAPI(generics.ListAPIView):
    name = 'get-contracts-of-project'
    serializer_class = ContractSerializer
    model = serializer_class.Meta.model
    lookup_url_kwarg = 'project_id'

    def get_queryset(self):
        try:
            project_id = self.kwargs.get('project_id')
            project = Project.objects.get(id=project_id)
            queryset = self.model.objects.filter(project=project)
            return queryset
        except Project.DoesNotExist:
            raise Http404


class DeleteContractAPI(generics.DestroyAPIView):
    name = 'delete-contract'
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = []
