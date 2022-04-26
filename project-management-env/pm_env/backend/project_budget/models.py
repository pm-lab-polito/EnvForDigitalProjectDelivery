from django.db import models
from project_charter.models import ProjectCharter
import datetime


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+100)]

def current_year():
    return datetime.date.today().year

class ProjectBudget(models.Model):
    project_charter = models.ForeignKey(ProjectCharter, related_name='project_budget', on_delete=models.CASCADE)
    year = models.IntegerField(('year'), choices=year_choices(), default=current_year())
    budget = models.IntegerField(default=0)
