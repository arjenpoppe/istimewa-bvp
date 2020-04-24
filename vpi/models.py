from django.db import models


class Project(models.Model):
    number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.number}: {self.name}'


class ProjectGoal(models.Model):
    number = models.IntegerField()
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    goal = models.TextField()

    def __str__(self):
        return f'{self.project.number}:{self.project.name} - Projectdoel {self.number}'


class VPI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    measuring_unit = models.CharField(max_length=20)
    formula = models.CharField(max_length=200, blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class VPITarget(models.Model):
    project_goal = models.OneToOneField(ProjectGoal, on_delete=models.CASCADE, null=True)
    vpi = models.OneToOneField(VPI, on_delete=models.CASCADE)
    green = models.CharField(max_length=10)
    yellow = models.CharField(max_length=20)
    red = models.CharField(max_length=20)

    def __str__(self):
        if self.project_goal:
            return f'{str(self.project_goal)}'
        else:
            return f'VPI: {str(self.vpi)}'


class Value(models.Model):
    value = models.FloatField()
    vpi = models.ForeignKey(VPI, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)

