from django.db import models
from projects.models import Project
from datetime import date


class Contract(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=1024)
    unit_price = models.FloatField(default=0)
    assignment = models.IntegerField(default=0)
    supplier = models.CharField(max_length=255)
    date = models.DateField(default=date.today())
 
    def total_cost(self):
        return self.unit_price * self.assignment

    def __str__(self):
        return self.product

    class Meta:
        ordering = ('project', 'date')