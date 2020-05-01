from django.db import models
from vpi.models import VPI, Project


class Dashboard(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    vpis = models.ManyToManyField(VPI)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
