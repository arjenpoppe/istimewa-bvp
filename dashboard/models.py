from django.db import models

from data.models.project import Project
from vpi.models import VPI


class GeneralDashboard(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    vpis = models.ManyToManyField(VPI)


class ProjectDashboard(GeneralDashboard):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def get_data(self):
        data = []
        for vpi in self.project.vpis.all():
            vpi.get_value(self.project.number)



class Report(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)


