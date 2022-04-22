from rest_framework import generics, status, permissions
from .serializers import ProjectSerializer
from rest_framework.response import Response
from custom_permissions.permissions import IsProjectManagementOffice
from .models import Project

#   Create a new project
class ProjectAPI(generics.GenericAPIView):
    name = 'create-project'
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectManagementOffice]

    # Create a new project
    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response(
            {
                'detail': 'Project created successfully.',
                'project': ProjectSerializer(project, context=self.get_serializer_context()).data,
            },
            status=status.HTTP_201_CREATED
        )


#   Edit a project name
class EditProjectAPI(generics.UpdateAPIView):
    name = 'edit-project-name'
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectManagementOffice]
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
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectManagementOffice]
    queryset = Project.objects.all()


#   Get a project 
class ProjectDetailsAPI(generics.RetrieveAPIView): 
    name = 'project-details'
    permission_classes = (permissions.IsAuthenticated,) # IsProjectManagementOffice)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    

#   Get a project list 
class ProjectListAPI(generics.ListAPIView): 
    name = 'project-list'
    permission_classes = (permissions.IsAuthenticated, IsProjectManagementOffice)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer