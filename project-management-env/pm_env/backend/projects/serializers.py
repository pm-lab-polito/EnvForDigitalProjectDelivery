from rest_framework import serializers
from .models import Project
from accounts.models import User
from accounts.serializers import UserSerializer
from project_charter.serializers import ProjectCharterSerializer


class ProjectCreateSerializer(serializers.ModelSerializer):
    project_charter = ProjectCharterSerializer(required=False)
    stakeholders = UserSerializer(many=True, required=False)
    
    def create(self, data):
        project = Project.objects.create(
            project_name = data.get('project_name'),
            author = data.get('author')
        )
        project.stakeholders.add(data.get('author'))
        return project

    def update(self, instance, validated_data):
        if validated_data.get('project_name'): 
            instance.project_name = validated_data.get('project_name', instance.project_name)
            instance.save()
            return instance
        else: 
            raise serializers.ValidationError(
                {
                    'detail':"'project_name' attribute  does not exist"
                }
            )
        
    
    class Meta:
        model = Project
        fields = ('id', 'project_name', 'author', 'created', 'stakeholders', 'project_charter')



class ProjectViewSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=True)
    project_charter = ProjectCharterSerializer(required=False)
    stakeholders = UserSerializer(many=True, required=False)

    def to_representation(self, instance):
        ret = super(ProjectViewSerializer, self).to_representation(instance)
        ret.get('author').pop('is_active')
        for user in ret.get('stakeholders'):
            user.pop('is_active')
        
        return ret
    
    
    class Meta:
        model = Project
        fields = ('id', 'project_name', 'author', 'created', 'stakeholders', 'project_charter')




class StakeholderProjectsSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=True)
    def to_representation(self, instance):
        ret = super(StakeholderProjectsSerializer, self).to_representation(instance)
        ret.get('author').pop('is_active')
        
        return ret

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'author', 'created')



class AddStakeholderSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        stakeholders = validated_data.get('stakeholders')
        if stakeholders and len(stakeholders) > 0: 
            for stakeholder in stakeholders:
                if stakeholder.user_role == 'U':
                    raise serializers.ValidationError(
                        {
                            'detail': f"User: {stakeholder.id} needs to be defined user_role before adding to the project."
                        }
                    )
            instance.stakeholders.add(*stakeholders)
            instance.save()
            return instance
        else: 
            raise serializers.ValidationError(
                {
                    'detail': "'stakeholders' attribute  is not defined correctly"
                }
            )


    class Meta:
        model = Project
        fields = ('id', 'stakeholders')
        


class RemoveStakeholderSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        stakeholders_to_remove = validated_data.get('stakeholders')
        if stakeholders_to_remove and len(stakeholders_to_remove) > 0: 
            instance.stakeholders.remove(*stakeholders_to_remove)
            instance.save()
            return instance
        else: 
            raise serializers.ValidationError(
                {
                    'detail': "'stakeholders' attribute  is not defined correctly"
                }
            )


    class Meta:
        model = Project
        fields = ('id', 'stakeholders')


class GetStakeholdersSerializer(serializers.ModelSerializer):
    stakeholders = UserSerializer(many=True)

    def to_representation(self, instance):
        ret = super(GetStakeholdersSerializer, self).to_representation(instance)
        for user in ret.get('stakeholders'):
            user.pop('is_active')
        
        return ret
        

    class Meta:
        model = Project
        fields = ('stakeholders',)