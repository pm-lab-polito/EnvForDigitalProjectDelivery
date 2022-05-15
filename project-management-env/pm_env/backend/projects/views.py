from django.http import Http404
from rest_framework import generics, status
from .serializers import (ProjectCreateSerializer, ProjectViewSerializer, AddStakeholderSerializer, 
    RemoveStakeholderSerializer, GetStakeholdersSerializer, StakeholderProjectsSerializer, )
from rest_framework.response import Response
import custom_permissions.permissions as perm # import (IsProjectManagementOffice, hasChangeProjectPermission, 
    # hasDeleteProjectPermission, hasViewProjectPermission, IsAuthorOfProject, IsOwnerOfUserAccount, RequestSenderIsRequestedUser)
from .models import Project
from accounts.models import User
from guardian.shortcuts import assign_perm, get_user_perms, remove_perm


def assign_full_project_perm_to_stakeholder(project, author):
    user = User.objects.get(id=author.id)
    assign_perm('project.change_project', user, project)
    assign_perm('project.delete_project', user, project)
    assign_perm('project.view_project', user, project)
    assign_perm('project_charter.add_project_charter', user, project)
    assign_perm('project_charter.change_project_charter', user, project)
    assign_perm('project_charter.delete_project_charter', user, project)
    assign_perm('project_charter.view_project_charter', user, project)
    assign_perm('resources.add_project_resource', user, project)
    assign_perm('resources.change_project_resource', user, project)
    assign_perm('resources.delete_project_resource', user, project)
    assign_perm('resources.view_project_resource', user, project)


#   Create a new project
class ProjectAPI(generics.GenericAPIView):
    name = 'create-project'
    serializer_class = ProjectCreateSerializer
    permission_classes = [perm.IsProjectManagementOffice,]

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        assign_full_project_perm_to_stakeholder(project=project, author=project.author)

        return Response(
            {
                'detail': 'Project created successfully.',
                'project': ProjectViewSerializer(project, context=self.get_serializer_context()).data,
            },
            status=status.HTTP_201_CREATED
        )


#   Edit a project name
class EditProjectAPI(generics.UpdateAPIView):
    name = 'edit-project-name'
    serializer_class = ProjectCreateSerializer
    permission_classes = [perm.hasChangeProjectPermission,]
    queryset = Project.objects.all()
    http_method_names = ['patch']

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Project name updated successfully"
            },  
            status=status.HTTP_204_NO_CONTENT
        )


#   Delete an existing project
class DeleteProjectAPI(generics.DestroyAPIView):
    name = 'delete-project'
    serializer_class = ProjectCreateSerializer
    permission_classes = [perm.hasDeleteProjectPermission,]
    queryset = Project.objects.all()


#   Get a project 
class ProjectDetailsAPI(generics.RetrieveAPIView): 
    name = 'project-details'
    permission_classes = [perm.hasViewProjectPermission,]
    queryset = Project.objects.all()
    serializer_class = ProjectViewSerializer


#   Get projects of stakeholder 
class GetProjectsOfStakeholderAPI(generics.ListAPIView): 
    name = 'get-projects-of-stakeholder'
    permission_classes = [perm.RequestSenderIsRequestedUser,]
    queryset = Project.objects.all()
    serializer_class = StakeholderProjectsSerializer
    model = serializer_class.Meta.model
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        try:
            user_id = self.kwargs['user_id']
            stakeholder = User.objects.get(id=user_id)
            queryset = self.model.objects.filter(stakeholders=stakeholder)

            return queryset

        except User.DoesNotExist:
            raise Http404



# Add stakeholders to a project
class AddStakeholdersToProjectAPI(generics.UpdateAPIView):
    name = 'add-project-stakeholders'
    serializer_class = AddStakeholderSerializer
    permission_classes = [perm.hasChangeProjectPermission,]
    queryset = Project.objects.all()
    http_method_names = ['patch']
    lookup_url_kwarg = 'project_id'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Stakeholders added successfully"
            },  
            status=status.HTTP_204_NO_CONTENT
        )


# Remove stakeholders from a project
class RemoveStakeholdersFromProjectAPI(generics.UpdateAPIView):
    name = 'remove-project-stakeholders'
    serializer_class = RemoveStakeholderSerializer
    permission_classes = [perm.hasDeleteProjectPermission,]
    queryset = Project.objects.all()
    http_method_names = ['patch']
    lookup_url_kwarg = 'project_id'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Stakeholders removed successfully"
            },  
            status=status.HTTP_204_NO_CONTENT
        )


class GetStakeholdersOfProjectAPI(generics.RetrieveAPIView):
    name = 'get-stakeholders-of-project'
    serializer_class = GetStakeholdersSerializer
    permission_classes = [perm.hasViewProjectPermission,]
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'


class GetActualCostOfProjectAPI(generics.GenericAPIView):
    name = 'get-actual-cost-of-project'
    serializer_class = ProjectViewSerializer
    permission_classes = [perm.hasViewProjectPermission,]

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs.get('pk')
            project = Project.objects.get(id=id)
            actual_cost = project.actual_cost()
            return Response(actual_cost)
            
        except Project.DoesNotExist:
            raise Http404



#### Permissions #####
def validated_project_permissions(permissions):
    if permissions and len(permissions) > 0:
        if ('change_project' in permissions or 
            'delete_project' in permissions or 
            'view_project' in permissions):
            return True
    return False

        
class AddProjectPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'add-project-permissions'
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
            # user is stakeholder of the project
            if user in project.stakeholders.all():
                if validated_project_permissions(permissions):
                    # if 'add_project' in permissions:
                    #         # assign_perm('project.add_project', user, project)
                    #         content_type = ContentType.objects.get_for_model(Project)
                    #         permission = Permission.objects.get(
                    #                 codename="add_project", content_type=content_type
                    #                     )
                    #         user.user_permissions.add(permission)

                    if 'change_project' in permissions:
                            assign_perm('project.change_project', user, project)

                    if 'delete_project' in permissions:
                            assign_perm('project.delete_project', user, project)

                    if 'view_project' in permissions:
                            assign_perm('project.view_project', user, project)
                    
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


class AssignAllProjectPermissionsToStakeholderAPI(generics.GenericAPIView):
    name = 'assign-all-project-permissions'
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
            # user is stakeholder of the project
            if user in project.stakeholders.all():
                assign_full_project_perm_to_stakeholder(project=project, author=user)
                return Response(status=status.HTTP_201_CREATED)

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



class DeleteProjectPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'delete-project-permissions'
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
            if validated_project_permissions(permissions):
                # if 'add_project' in permissions:
                #         # remove_perm('project.add_project', user, project)
                #         user.user_permissions.remove('project.add_project')

                if 'change_project' in permissions:
                        remove_perm('project.change_project', user, project)

                if 'delete_project' in permissions:
                        remove_perm('project.delete_project', user, project)

                if 'view_project' in permissions:
                        remove_perm('project.view_project', user, project)
                
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

            
class GetProjectPermissionsOfUserAPI(generics.GenericAPIView):
    name = 'get-project-permissions'
    permission_classes = [perm.IsAuthorOfProject | perm.IsOwnerOfUserAccount,]

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get('user_id')
            user = User.objects.get(id=user_id)
            project_id = self.kwargs.get('project_id')
            project = Project.objects.get(id=project_id)
            
            permissions = get_user_perms(user, project)

            perm_obj = {
                'user': user,
                'project': project
            }
            # check if a request user is a project author or is owner of user account
            self.check_object_permissions(request, perm_obj)

            return Response({
                    'permissions': permissions,
                }, 
                status=status.HTTP_200_OK
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

