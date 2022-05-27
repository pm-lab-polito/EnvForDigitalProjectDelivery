from rest_framework import serializers
from .models import ProjectCharter, BusinessCaseSWOT
from project_budget.serializers import ProjectBudgetSerializer
from rest_framework.validators import UniqueValidator


class BusinessCaseSWOTSerializer(serializers.ModelSerializer):
    def create(self, data):
        swot = BusinessCaseSWOT.objects.create(
            project_charter = data.get('project_charter'),
            swot_type = data.get('swot_type'),
            content = data.get('content')
        )
        return swot

    class Meta:
        model = BusinessCaseSWOT
        fields = ['id', 'project_charter', 'swot_type', 'content']
        

class ProjectCharterSerializer(serializers.ModelSerializer):
    bus_case_swot = BusinessCaseSWOTSerializer(many=True, required=False)
    project_budget = ProjectBudgetSerializer(many=True, required=False)
    
    def create(self, data):
        project_charter = ProjectCharter.objects.create(
            project = data.get('project'),
            author = data.get('author'),
            sow = data.get('sow'),
            contract = data.get('contract'),
            business_case = data.get('business_case')
        )
        return project_charter

    def update(self, instance, validated_data):
        if validated_data.get('sow') or validated_data.get('contract') or validated_data.get('business_case'): 
            instance.sow = validated_data.get('sow', instance.sow)
            instance.contract = validated_data.get('contract', instance.contract)
            instance.business_case = validated_data.get('business_case', instance.business_case)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'detail':"At least, one attribute must be provided (sow/contract/business_case)"})
       
    class Meta:
        model = ProjectCharter
        fields = ('id', 'project', 'author', 'created', 'last_updated',
                    'sow', 'contract', 'business_case', 'bus_case_swot', 'project_budget')
        extra_kwargs = {
                'project': {
                    'validators': [
                        UniqueValidator(
                            queryset=ProjectCharter.objects.all(), 
                            message = 'This project already has a project charter.'
                        )
                    ]
                }
            }
