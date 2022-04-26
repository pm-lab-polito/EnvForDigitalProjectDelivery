from rest_framework import generics, status
from project_budget.models import ProjectBudget
from .serializers import ProjectBudgetSerializer
from rest_framework.response import Response
from custom_permissions.permissions import IsProjectManagementOffice, IsProjectManager

#   Set a budget of a project charter
class ProjectBudgetAPI(generics.ListCreateAPIView):
    name = 'set-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        
        project_charter = self.kwargs.get('project_charter')
        for attrs in self.request.data:
            attrs["project_charter"]=project_charter 
        
        return super(ProjectBudgetAPI, self).get_serializer(*args, **kwargs)



#   Delete a single instance of a project budget
class DeleteProjectBudgetAPI(generics.DestroyAPIView):
    name = 'delete-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]
    queryset = ProjectBudget.objects.all()


#   Delete all budget of a project charter
class DeleteTotalProjectBudgetAPI(generics.GenericAPIView):
    name = 'delete-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]
    
    def delete(self, request, pk, *args, **kwargs):
        total_budget = ProjectBudget.objects.all().filter(project_charter=pk)
        if total_budget.count() > 0:
            total_budget.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


#   Get a single instance of a project budget
class ProjectBudgetDetailsAPI(generics.RetrieveAPIView): 
    name = 'project-budget-details'
    permission_classes = () # IsProjectManagementOffice | IsProjectManager)
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer


#   Get total budget of a project 
class TotalProjectBudgetAPI(generics.ListAPIView): 
    name = 'total-project-budget'
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer

    def list(self, request, pk):
        qs = self.get_queryset().filter(project_charter=pk)
        serializer = ProjectBudgetSerializer(qs, many=True)
        return Response(serializer.data)



#   Edit a project budget
class EditProjectBudgetAPI(generics.UpdateAPIView):
    name = 'edit-project-budget'
    serializer_class = ProjectBudgetSerializer
    permission_classes = [IsProjectManagementOffice | IsProjectManager,]
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
            status=status.HTTP_204_NO_CONTENT
        )
