from django.db import models
from project.models import Project


class Resource(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, default=None)
    cost = models.FloatField(default=0.00)
    category = models.CharField(max_length=255)

    class Meta:
        def __str__(self):
            return self.name
