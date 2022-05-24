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
        resource_spendings = project_budget.models.ResourceSpending.objects.all().filter(project=self).filter(approval_status='approved').aggregate(Sum('amount')).get('amount__sum')
        contract_spendings = project_budget.models.ContractSpending.objects.all().filter(project=self).filter(approval_status='approved').aggregate(Sum('amount')).get('amount__sum')
        if not resource_spendings:
            resource_spendings = 0.0
        if not contract_spendings:
            contract_spendings = 0.0 
        actual_cost= resource_spendings + contract_spendings

        return {
            "actual_cost": actual_cost,
            "resource_spendings": resource_spendings,
            "contract_spendings": contract_spendings
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

            ('add_project_resource', 'Can add project resource'),
            ('change_project_resource', 'Can change project resource'),
            ('delete_project_resource', 'Can delete project resource'),
            ('view_project_resource', 'Can view project resource'),

            ('add_project_contract', 'Can add project contract'),
            ('change_project_contract', 'Can change project contract'),
            ('delete_project_contract', 'Can delete project contract'),
            ('view_project_contract', 'Can view project contract'),

            ('add_project_spendings', 'Can add project spendings'),
            ('change_project_spendings', 'Can change project spendings'),
            ('delete_project_spendings', 'Can delete project spendings'),
            ('view_project_spendings', 'Can view project spendings'),
        )
