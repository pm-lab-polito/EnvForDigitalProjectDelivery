from django.db import models
from project_charter.models import ProjectCharter
from project_resources.models import Resource
from projects.models import Project
from project_procurements.models import Contract
import datetime
from django.db.models import Sum


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+100)]

def current_year():
    return datetime.date.today().year

class ProjectBudget(models.Model):
    project_charter = models.ForeignKey(ProjectCharter, related_name='project_budget', on_delete=models.CASCADE)
    year = models.IntegerField(('year'), choices=year_choices(), default=current_year())
    budget = models.IntegerField(default=0)

    def actual_cost(self):
        resource_spendings = ResourceSpending.objects.all().filter(budget=self).aggregate(Sum('amount')).get('amount__sum')
        contract_spendings = ContractSpending.objects.all().filter(budget=self).aggregate(Sum('amount')).get('amount__sum')
        actual_cost= resource_spendings + contract_spendings
        return {
            "actual_cost": actual_cost,
            "resource_spendings": resource_spendings,
            "contract_spendings": contract_spendings
        }
    
    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ('project_charter', 'year')



class ResourceSpending(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    budget = models.ForeignKey(ProjectBudget, on_delete=models.CASCADE)
    assignment = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    description = models.TextField(blank=True, max_length=1024)
    date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return str(self.resource)

    class Meta:
        ordering = ('project', 'budget')




class ContractSpending(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    budget = models.ForeignKey(ProjectBudget, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    description = models.TextField(blank=True, max_length=1024)
    date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return str(self.contract)

    class Meta:
        ordering = ('project', 'budget')