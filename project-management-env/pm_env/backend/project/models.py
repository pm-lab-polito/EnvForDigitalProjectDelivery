from django.db import models
from accounts.models import User


class Project(models.Model):
    project_name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ('project_name',)
        permissions = (
            ('add_project_charter', 'Can add project charter / to project charter'),
            ('change_project_charter', 'Can change project charter'),
            ('delete_project_charter', 'Can delete project charter'),
            ('view_project_charter', 'Can view project charter')
        )
