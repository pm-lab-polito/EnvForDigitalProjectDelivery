from rest_framework import generics, status
from .serializers import ProjectCharterSerializer, BusinessCaseSWOTSerializer
from rest_framework.response import Response
from custom_permissions.permissions import IsProjectManagementOffice, IsProjectManager
from .models import ProjectCharter, BusinessCaseSWOT

#   Create a new project charter
class ProjectCharterAPI(generics.GenericAPIView):
    name = 'create-project-charter'
    serializer_class = ProjectCharterSerializer
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]
    queryset = ProjectCharter.objects.all()


#   Edit a project charter
class EditProjectCharterAPI(generics.UpdateAPIView):
    name = 'edit-project-charter'
    serializer_class = ProjectCharterSerializer
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]
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
    permission_classes = [] # IsProjectManagementOffice | IsProjectManager)
    queryset = ProjectCharter.objects.all()
    serializer_class = ProjectCharterSerializer


######## Business Case SWOT

#   Add a new swot
class BusinessCaseSWOTAPI(generics.GenericAPIView):
    name = 'add-business-case-swot'
    serializer_class = BusinessCaseSWOTSerializer
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]

    # Create a new project charter
    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]
    queryset = BusinessCaseSWOT.objects.all()


#   Get single swot instance
class SWOTDetailsAPI(generics.RetrieveAPIView): 
    name = 'swot-details'
    permission_classes = [] # IsProjectManagementOffice | IsProjectManager)
    queryset = BusinessCaseSWOT.objects.all()
    serializer_class = BusinessCaseSWOTSerializer


#   Get swot list of project charter
class SWOTListOfProjectCharterAPI(generics.ListAPIView):
    name = 'swot-list-of-project-charter'
    queryset = BusinessCaseSWOT.objects.all()
    serializer_class = BusinessCaseSWOTSerializer
    permission_classes = [] # IsProjectManagementOffice | IsProjectManager)

    def list(self, request, pk):
        queryset = self.get_queryset()
        return Response(
            {
                'swot-list': self.get_serializer(queryset.filter(project_charter=pk), 
                    context=self.get_serializer_context(), many=True).data
            },
            status=status.HTTP_200_OK
        )