from django.db import models
from projects.models import Project
from accounts.models import User


class ProjectCharter(models.Model):
    project = models.OneToOneField(Project, related_name='project_charter', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    sow = models.CharField(max_length=1024, blank=True, null=True)
    contract = models.CharField(max_length=1024, blank=True, null=True)
    business_case = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.project.project_name

    class Meta:
       ordering = ('project',)


class BusinessCaseSWOT(models.Model):
    project_charter = models.ForeignKey(ProjectCharter, related_name='bus_case_swot', on_delete=models.CASCADE)
    swot_type = models.CharField(
        max_length=11,
        choices=[('strength', 'strength'), ('weakness', 'weakness'), 
            ('opportunity', 'opportunity'), ('threat', 'threat'),]
    )
    content = models.CharField(max_length=1024, blank=True)
    
    def __str__(self):
        return self.swot_type

    class Meta:
        ordering = ('project_charter',)