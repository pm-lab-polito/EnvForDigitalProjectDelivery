from rest_framework import generics, status
from .serializers import ProjectCharterSerializer, BusinessCaseSWOTSerializer
from rest_framework.response import Response
import custom_permissions.permissions as custom_perm
from .models import ProjectCharter, BusinessCaseSWOT
from accounts.models import User
from project.models import Project
from guardian.shortcuts import assign_perm, remove_perm

#   Create a new project charter
class ProjectCharterAPI(generics.GenericAPIView):
    name = 'create-project-charter'
    serializer_class = ProjectCharterSerializer
    permission_classes = [custom_perm.hasAddProjectCharterPermission | custom_perm.IsAuthorOfProject,]

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(request, serializer.validated_data.get('project'))
        project_charter = serializer.save()

        return Response(
            {
                'detail': 'Project charter created successfully.',
                'project_charter': ProjectCharterSerializer(project_charter, 
                                        context=self.get_serializer_context()).data,
            },
            status=status.HTTP_201_CREATED
        )


#   Delete an existing project charter
class DeleteProjectCharterAPI(generics.DestroyAPIView):
    name = 'delete-project-charter'
    serializer_class = ProjectCharterSerializer
    permission_classes = [custom_perm.hasDeleteProjectCharterPermission |
         custom_perm.hasDeleteProjectPermission,]
    queryset = ProjectCharter.objects.all()


#   Edit a project charter
class EditProjectCharterAPI(generics.UpdateAPIView):
    name = 'edit-project-charter'
    serializer_class = ProjectCharterSerializer
    permission_classes = [custom_perm.hasChangeProjectCharterPermission | 
        custom_perm.hasChangeProjectPermission,]
    queryset = ProjectCharter.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Project charter updated successfully"
            },  
            status=status.HTTP_204_NO_CONTENT
        )


#   Get a project charter
class ProjectCharterDetailsAPI(generics.RetrieveAPIView): 
    name = 'details-project-charter'
    permission_classes = [custom_perm.hasViewProjectCharterPermission |
        custom_perm.hasViewProjectPermission] 
    queryset = ProjectCharter.objects.all()
    serializer_class = ProjectCharterSerializer


######## Business Case SWOT

#   Add a new swot
class BusinessCaseSWOTAPI(generics.GenericAPIView):
    name = 'add-business-case-swot'
    serializer_class = BusinessCaseSWOTSerializer
    permission_classes = [custom_perm.hasAddProjectCharterPermission |
        custom_perm.hasChangeProjectCharterPermission | custom_perm.hasChangeProjectPermission,]

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(request, serializer.validated_data.get('project_charter'))
        swot = serializer.save()
        return Response(
            {
                'detail': 'Business case swot added successfully.',
                'swot': BusinessCaseSWOTSerializer(swot, context=self.get_serializer_context()).data,
            },
            status=status.HTTP_201_CREATED
        )


#   Delete an existing project charter
class DeleteBusinessCaseSWOTAPI(generics.DestroyAPIView):
    name = 'delete-swot'
    serializer_class = BusinessCaseSWOTSerializer
    permission_classes = [custom_perm.hasDeleteProjectCharterPermission | 
        custom_perm.hasDeleteProjectPermission,]
    queryset = BusinessCaseSWOT.objects.all()


#   Get single swot instance
class SWOTDetailsAPI(generics.RetrieveAPIView): 
    name = 'swot-details'
    permission_classes = [custom_perm.hasViewProjectCharterPermission | 
        custom_perm.hasViewProjectPermission,]
    queryset = BusinessCaseSWOT.objects.all()
    serializer_class = BusinessCaseSWOTSerializer


#   Get swot list of project charter
class SWOTListOfProjectCharterAPI(generics.ListAPIView):
    name = 'swot-list-of-project-charter'
    queryset = BusinessCaseSWOT.objects.all()
    serializer_class = BusinessCaseSWOTSerializer
    permission_classes = [custom_perm.hasViewProjectCharterPermission | 
        custom_perm.hasViewProjectPermission,]

    def list(self, request, project_charter_pk):
        queryset = self.get_queryset()
        return Response(
            {
                'swot-list': self.get_serializer(queryset.filter(project_charter=project_charter_pk), 
                    context=self.get_serializer_context(), many=True).data
            },
            status=status.HTTP_200_OK
        )

    



#### Permissions #####
def validated_project_charter_permissions(permissions):
    if permissions and len(permissions) > 0:
        if ('add_project_charter' in permissions or
            'change_project_charter' in permissions or 
            'delete_project_charter' in permissions or 
            'view_project_charter' in permissions):
            return True
    return False

        
class AddProjectCharterPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'add-project-charter-permissions'
    permission_classes = [custom_perm.IsAuthorOfProject,]

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
                if 'add_project_charter' in permissions:
                        assign_perm('project_charter.add_project_charter', user, project)

                if 'change_project_charter' in permissions:
                        assign_perm('project_charter.change_project_charter', user, project)

                if 'delete_project_charter' in permissions:
                        assign_perm('project_charter.delete_project_charter', user, project)

                if 'view_project_charter' in permissions:
                        assign_perm('project_charter.view_project_charter', user, project)
                
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


class DeleteProjectCharterPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'delete-project-permissions'
    permission_classes = [custom_perm.IsAuthorOfProject,]

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
                if 'add_project_charter' in permissions:
                        remove_perm('project_charter.add_project_charter', user, project)

                if 'change_project_charter' in permissions:
                        remove_perm('project_charter.change_project_charter', user, project)

                if 'delete_project_charter' in permissions:
                        remove_perm('project_charter.delete_project_charter', user, project)

                if 'view_project_charter' in permissions:
                        remove_perm('project_charter.view_project_charter', user, project)
                
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
