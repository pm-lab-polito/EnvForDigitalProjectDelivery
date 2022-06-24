from rest_framework import generics, status
from .serializers import ResourceSerializer
from rest_framework.response import Response
from .models import Resource
from projects.models import Project
from django.http import Http404
from .permissions import *



class AddResourceAPI(generics.GenericAPIView):
    name = 'add-resource'
    serializer_class = ResourceSerializer
    permission_classes = [hasAddProjectResourcePermission,]

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(request, serializer.validated_data.get('project'))
        resource = serializer.save()

        return Response(
            {
                'detail': 'Resource added successfully.',
                'resource': ResourceSerializer(resource, 
                                        context=self.get_serializer_context()).data,
            },
            status=status.HTTP_201_CREATED
        )


class RemoveResourceAPI(generics.DestroyAPIView):
    name = "remove-resource"
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    permission_classes = [hasDeleteProjectResourcePermission,]


class UpdateResourceAPI(generics.UpdateAPIView):
    name = "update-resource"
    serializer_class = ResourceSerializer
    permission_classes = [hasChangeProjectResourcePermission,]
    queryset = Resource.objects.all()
    http_method_names = ['patch']

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Resource updated successfully"
            },  
            status=status.HTTP_200_OK
        )


class GetResourceAPI(generics.RetrieveAPIView):
    name = "get-resource"
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    permission_classes = [hasViewProjectResourcePermission,]


class GetResourceListOfProjectAPI(generics.ListAPIView):
    name = "get-resource-list-of-project"
    serializer_class = ResourceSerializer
    model = serializer_class.Meta.model
    permission_classes = [hasViewProjectResourcePermission,]
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
