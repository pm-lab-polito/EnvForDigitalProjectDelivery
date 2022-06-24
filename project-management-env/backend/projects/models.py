from django.db import models
from accounts.models import User
import project_budget
from django.db.models import Sum


class Project(models.Model):
    project_name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    stakeholders = models.ManyToManyField(User, blank=True, related_name="stakeholders")

    def actual_cost(self):
        resource_spending = project_budget.models.ResourceSpending.objects.all().filter(project=self).filter(approval_status='approved').aggregate(Sum('amount')).get('amount__sum')
        contract_spending = project_budget.models.ContractSpending.objects.all().filter(project=self).filter(approval_status='approved').aggregate(Sum('amount')).get('amount__sum')
        if not resource_spending:
            resource_spending = 0.0
        if not contract_spending:
            contract_spending = 0.0 
        actual_cost= resource_spending + contract_spending

        return {
            "actual_cost": actual_cost,
            "resource_spending": resource_spending,
            "contract_spending": contract_spending
        }

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ('project_name',)
        permissions = (
            ('add_project_charter', 'Can add project charter /to project charter'),
            ('change_project_charter', 'Can change project charter'),
            ('delete_project_charter', 'Can delete project charter'),
            ('view_project_charter', 'Can view project charter'),

            ('add_additional_budget', 'Can add additonal budget request'),
            ('change_additional_budget', 'Can change additional budget'),
            ('view_additional_budget', 'Can view additional budget'),

            ('add_project_resource', 'Can add project resource'),
            ('change_project_resource', 'Can change project resource'),
            ('delete_project_resource', 'Can delete project resource'),
            ('view_project_resource', 'Can view project resource'),

            ('add_project_contract', 'Can add project contract'),
            ('change_project_contract', 'Can change project contract'),
            ('delete_project_contract', 'Can delete project contract'),
            ('view_project_contract', 'Can view project contract'),

            ('add_project_spending', 'Can add project spending'),
            ('change_project_spending', 'Can change project spending'),
            ('delete_project_spending', 'Can delete project spending'),
            ('view_project_spending', 'Can view project spending'),
        )
