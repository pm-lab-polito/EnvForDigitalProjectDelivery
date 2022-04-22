from rest_framework import serializers
from .models import Project
from project_charter.serializers import ProjectCharterSerializer


class ProjectSerializer(serializers.ModelSerializer):
    project_charter = ProjectCharterSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'author', 'created', 'project_charter')

    def create(self, data):
        project = Project.objects.create(
            project_name = data.get('project_name'),
            author = data.get('author')
        )
        return project

    def update(self, instance, validated_data):
        if validated_data.get('project_name'): 
            instance.project_name = validated_data.get('project_name', instance.project_name)
            instance.save()
            return instance
        else: 
            raise serializers.ValidationError({'detail':"'project_name' attribute  does not exist"})