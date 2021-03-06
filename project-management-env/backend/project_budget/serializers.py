from dataclasses import fields
from rest_framework import serializers
from .models import ProjectBudget, ResourceSpending, ContractSpending, AdditionalBudget
from .eva import EVA
from django.db.models import Sum


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



class AdditionalBudgetSerializer(serializers.ModelSerializer):
    def create(self, data, *args, **kwargs):
        instance = AdditionalBudget.objects.create(
            budget=data.get('budget'),
            amount=data.get('amount')
        )
        instance.save()

        return instance

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        if status == 'approved' or status == 'denied':
            instance.status = status
        else:
            raise serializers.ValidationError({"detail": "Status is not defined correctly."})
        instance.save()

        return instance


    class Meta:
        model = AdditionalBudget
        fields = ('id', 'budget', 'amount', 'date', 'status')


class AdditionalBudgetViewSerializer(serializers.ModelSerializer):
    budget = ProjectBudgetSerializer(required=True)
    
    class Meta:
        model = AdditionalBudget
        fields = ('id', 'budget', 'amount', 'date', 'status')



class ResourceSpendingSerializer(serializers.ModelSerializer):
    def create(self, validated_data, *args, **kwargs):
        amount = validated_data.get('assignment') * validated_data.get('resource').cost
        date = validated_data.get('date')
        if date.year != validated_data.get('budget').year:
            raise serializers.ValidationError({"detail": "Spending date must be in budget year."})

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
        budget = instance.budget.budget 
        additional_budget = AdditionalBudget.objects.all().filter(budget=budget).filter(status='approved').aggregate(Sum('amount')).get('amount__sum')    
        if not additional_budget:
            additional_budget = 0.0
        budget += additional_budget
        if instance.budget.actual_cost().get('actual_cost') > budget:
            instance.approval_status = 'denied'
            instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.assignment = validated_data.get("assignment", instance.assignment)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.amount = instance.assignment * instance.resource.cost
        
        if instance.date.year != instance.budget.year:
            raise serializers.ValidationError({"detail": "Spending date must be in budget year."})

        # check if actual cost (including last updated spending) is greater than current budget, deny last update    
        budget = instance.budget.budget 
        additional_budget = AdditionalBudget.objects.all().filter(budget=budget).filter(status='approved').aggregate(Sum('amount')).get('amount__sum')    
        if not additional_budget:
            additional_budget = 0.0
        budget += additional_budget
        if instance.budget.actual_cost().get('actual_cost') > budget:
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
            raise serializers.ValidationError({"detail": "Spending date must be in budget year."})

        instance = ContractSpending.objects.create(
            project = validated_data.get('project'),
            contract = validated_data.get('contract'),
            budget = validated_data.get('budget'),
            amount = amount,
            description = validated_data.get('description'),
            date = date
        )

        # check if actual cost (including last updated spending) is greater than current budget, deny last update    
        budget = instance.budget.budget 
        additional_budget = AdditionalBudget.objects.all().filter(budget=budget).filter(status='approved').aggregate(Sum('amount')).get('amount__sum')    
        if not additional_budget:
            additional_budget = 0.0
        budget += additional_budget
        if instance.budget.actual_cost().get('actual_cost') > budget:
            instance.approval_status = 'denied'
            instance.save()
            
        return instance

    def update(self, instance, validated_data):
        instance.contract = validated_data.get("contract", instance.contract)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.amount = instance.contract.total_cost()

        if instance.date.year != instance.budget.year:
            raise serializers.ValidationError({"detail": "Spending date must be in budget year."})

        # check if actual cost (including last updated spending) is greater than current budget, deny last update    
        budget = instance.budget.budget 
        additional_budget = AdditionalBudget.objects.all().filter(budget=budget).filter(status='approved').aggregate(Sum('amount')).get('amount__sum')    
        if not additional_budget:
            additional_budget = 0.0
        budget += additional_budget
        if instance.budget.actual_cost().get('actual_cost') > budget:
            raise serializers.ValidationError('You are over budget.')
        else: 
            instance.approval_status = 'approved'

        instance.save()
        return instance


    class Meta:
        model = ContractSpending
        fields = ('id', 'project', 'contract', 'budget', 'amount', 'description', 'date', 'approval_status')



class ForecastBalanceSerializer(serializers.Serializer):
    total_scheduled_tasks = serializers.IntegerField()
    task_duration = serializers.IntegerField()
    employee_cost_day = serializers.FloatField()
    actual_activity = serializers.ListField()

    def create(self, data):
        eva = EVA(
            total_scheduled_tasks = data.get('total_scheduled_tasks'),
            task_duration = data.get('task_duration'),
            employee_cost_day = data.get('employee_cost_day'),
            actual_activity = data.get('actual_activity')        
        )

        forecast_balance = {
                'estimate_to_complete': eva.estimate_to_complete(),
                'estimate_at_complete': eva.estimate_at_complete()
            }

        return forecast_balance




class ForecastSerializer(serializers.Serializer):
    total_scheduled_tasks = serializers.IntegerField()
    task_duration = serializers.IntegerField()
    employee_cost_day = serializers.FloatField()
    actual_activity = serializers.ListField()

    def create(self, data):
        eva = EVA(
            total_scheduled_tasks = data.get('total_scheduled_tasks'),
            task_duration = data.get('task_duration'),
            employee_cost_day = data.get('employee_cost_day'),
            actual_activity = data.get('actual_activity')        
        )

        earned_value_analysis = {
                'planned_work_percentage': eva.planned_work_percentage(), 
                'budget_work': eva.budget_work(), 
                'actual_work_percentage': eva.actual_work_percentage(), 
                'budgeted_cost_of_work_scheduled': eva.budgeted_cost_of_work_scheduled(),
                'actual_cost_of_work_performed': eva.actual_cost_of_work_performed(),
                'budgeted_cost_of_work_performed': eva.budgeted_cost_of_work_performed(),
                'earned_value': eva.earned_value(),
                'schedule_performance_index': eva.schedule_performance_index(),
                'schedule_variance': eva.schedule_variance(),
                'schedule_variance_percentage': eva.schedule_variance_percentage(),
                'cost_variance': eva.cost_variance(),
                'cost_performance_index': eva.cost_performance_index(),
                'cost_variance_percentage': eva.cost_variance_percentage(),
                'estimate_to_complete': eva.estimate_to_complete(),
                'estimate_at_complete': eva.estimate_at_complete(),
                'cost_variance_at_completion': eva.cost_variance_at_completion(),
                'time_variance': eva.time_variance(),
                'time_variance_percentage': eva.time_variance_percentage(),
                'earned_schedule': eva.earned_schedule(),
                'time_performance_index': eva.time_performance_index(),
                'estimated_accomplishment_rate': eva.estimated_accomplishment_rate(),
                'time_estimate_at_completion': eva.time_estimate_at_completion(),
                'time_variance_at_completion': eva.time_variance_at_completion()
            }

        return earned_value_analysis