from rest_framework import serializers
from .models import ProjectBudget, ResourceSpending, ContractSpending


class CreateUpdateListSerializer(serializers.ListSerializer):
    def create(self, validated_data, *args, **kwargs):
        return [self.child.create(attrs) for attrs in validated_data ]


class ProjectBudgetSerializer(serializers.ModelSerializer):    
    def create(self, validated_data, *args, **kwargs):
        instance = ProjectBudget(**validated_data)
        try:
            proj_budget = ProjectBudget.objects.get(project_charter=instance.project_charter, year=instance.year)
            proj_budget.budget = instance.budget
            proj_budget.save()
            instance = proj_budget

        except ProjectBudget.DoesNotExist:
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



class ResourceSpendingSerializer(serializers.ModelSerializer):
    def create(self, validated_data, *args, **kwargs):
        amount = validated_data.get('assignment') * validated_data.get('resource').cost
        date = validated_data.get('date')
        if date.year != validated_data.get('budget').year:
            raise serializers.ValidationError('Spending date must be in budget year.')

        instance = ResourceSpending.objects.create(
            project = validated_data.get('project'),
            resource = validated_data.get('resource'),
            budget = validated_data.get('budget'),
            assignment = validated_data.get('assignment'),
            amount = amount,
            description = validated_data.get('description'),
            date = date
        )

        # check if actual cost (including last spending) is greater than current budget, deny last spending    
        if instance.budget.actual_cost().get('actual_cost') > instance.budget.budget:
            instance.approval_status = 'denied'
            instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.assignment = validated_data.get("assignment", instance.assignment)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.amount = instance.assignment * instance.resource.cost
        
        # check if actual cost (including last updated spending) is greater than current budget, deny last update    
        if instance.budget.actual_cost().get('actual_cost') > instance.budget.budget:
            raise serializers.ValidationError('You are over budget.')
        else: 
            instance.approval_status = 'approved'

        instance.save()
        return instance


    class Meta:
        model = ResourceSpending
        fields = ('id', 'project', 'resource', 'budget', 'assignment', 'amount', 'description', 'date', 'approval_status')



class ContractSpendingSerializer(serializers.ModelSerializer):
    def create(self, validated_data, *args, **kwargs):
        amount = validated_data.get('contract').total_cost()
        date = validated_data.get('date')
        if date.year != validated_data.get('budget').year:
            raise serializers.ValidationError('Spending date must be in budget year.')

        instance = ContractSpending.objects.create(
            project = validated_data.get('project'),
            contract = validated_data.get('contract'),
            budget = validated_data.get('budget'),
            amount = amount,
            description = validated_data.get('description'),
            date = date
        )

        # check if actual cost (including last updated spending) is greater than current budget, deny last update    
        if instance.budget.actual_cost().get('actual_cost') > instance.budget.budget:
            instance.approval_status = 'denied'
            instance.save()
            
        return instance

    def update(self, instance, validated_data):
        instance.contract = validated_data.get("contract", instance.contract)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.amount = instance.contract.total_cost()

        # check if actual cost (including last updated spending) is greater than current budget, deny last update    
        if instance.budget.actual_cost().get('actual_cost') > instance.budget.budget:
            raise serializers.ValidationError('You are over budget.')
        else: 
            instance.approval_status = 'approved'

        instance.save()
        return instance


    class Meta:
        model = ContractSpending
        fields = ('id', 'project', 'contract', 'budget', 'amount', 'description', 'date', 'approval_status')