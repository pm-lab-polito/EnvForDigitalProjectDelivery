from rest_framework import generics, status
from .serializers import ResourceSerializer
from rest_framework.response import Response
from .models import Resource
from project.models import Project
from accounts.models import User
from django.http import Http404
from custom_permissions import permissions as perm
from guardian.shortcuts import assign_perm, remove_perm



class AddResourceAPI(generics.GenericAPIView):
    name = 'add-resource'
    serializer_class = ResourceSerializer
    permission_classes = [perm.hasAddProjectResourcePermission]

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
    permission_classes = [perm.hasDeleteProjectResourcePermission 
        | perm.hasDeleteProjectPermission]


class UpdateResourceAPI(generics.UpdateAPIView):
    name = "update-resource"
    serializer_class = ResourceSerializer
    permission_classes = [perm.hasChangeProjectResourcePermission 
        | perm.hasChangeProjectPermission]
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
            status=status.HTTP_204_NO_CONTENT
        )


class GetResourceAPI(generics.RetrieveAPIView):
    name = "get-resource"
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    permission_classes = [perm.hasViewProjectResourcePermission 
        | perm.hasViewProjectPermission]


class GetResourceListOfProjectAPI(generics.ListAPIView):
    name = "get-resource-list-of-project"
    serializer_class = ResourceSerializer
    model = serializer_class.Meta.model
    permission_classes = [perm.hasViewProjectResourceListPermission,]
    lookup_url_kwarg = 'project_id'

    def get_queryset(self):
        try:
            project_id = self.kwargs.get('project_id')
            project = Project.objects.get(id=project_id)
            queryset = self.model.objects.filter(project=project)
            return queryset

        except Project.DoesNotExist:
            raise Http404




#### Permissions #####
def validated_project_charter_permissions(permissions):
    if permissions and len(permissions) > 0:
        if ('add_project_resource' in permissions or
            'change_project_resource' in permissions or 
            'delete_project_resource' in permissions or 
            'view_project_resource' in permissions):
            return True
    return False

        
class AddProjectResourcePermissionsOfUserAPI(generics.GenericAPIView):
    name = 'add-project-resource-permissions'
    permission_classes = [perm.IsAuthorOfProject,]

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
                if 'add_project_resource' in permissions:
                        assign_perm('resources.add_project_resource', user, project)

                if 'change_project_resource' in permissions:
                        assign_perm('resources.change_project_resource', user, project)

                if 'delete_project_resource' in permissions:
                        assign_perm('resources.delete_project_resource', user, project)

                if 'view_project_resource' in permissions:
                        assign_perm('resources.view_project_resource', user, project)
                
                return Response(status=status.HTTP_201_CREATED)

            
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


class DeleteProjectResourcePermissionsOfUserAPI(generics.GenericAPIView):
    name = 'delete-project-resource-permissions'
    permission_classes = [perm.IsAuthorOfProject,]

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
                if 'add_project_resource' in permissions:
                        remove_perm('resources.add_project_resource', user, project)

                if 'change_project_resource' in permissions:
                        remove_perm('resources.change_project_resource', user, project)

                if 'delete_project_resource' in permissions:
                        remove_perm('resources.delete_project_resource', user, project)

                if 'view_project_resource' in permissions:
                        remove_perm('resources.view_project_resource', user, project)
                
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