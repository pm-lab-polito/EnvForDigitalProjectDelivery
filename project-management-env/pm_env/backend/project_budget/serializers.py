from rest_framework import serializers
from .models import ProjectBudget


class CreateUpdateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return [self.child.create(attrs) for attrs in validated_data]


class ProjectBudgetSerializer(serializers.ModelSerializer):    

    def create(self, validated_data):
        instance = ProjectBudget(**validated_data)
        instance.save()
        return instance
        
    def update(self, instance, validated_data):
        instance.year = validated_data.get("year", instance.year)
        instance.budget = validated_data.get("budget", instance.budget)
        instance.save()
        return instance

    class Meta:
        model = ProjectBudget
        fields = ('id', 'project_charter', 'year', 'budget',)
        list_serializer_class = CreateUpdateListSerializer
