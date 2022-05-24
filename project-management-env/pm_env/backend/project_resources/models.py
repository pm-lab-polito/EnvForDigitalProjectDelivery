from django.db import models
from projects.models import Project


class Resource(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, default=None)
    cost = models.FloatField(default=0.00)
    unit = models.CharField(max_length=255, default='euro')
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('project', 'name')
