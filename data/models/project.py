from django.db import models

from vpi.models import Project


class ProjectActiviteit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.code}{self.description}'


class ProjectFase(models.Model):
    INRICHTING = 'INR'
    ONTWERP = 'ONT'
    UITVOER = 'UIT'
    OPLEVERING = 'OPL'
    OVERIG = 'OVG'
    CHOICES = [
        (INRICHTING, 'Inrichting'),
        (ONTWERP, 'Ontwerp'),
        (UITVOER, 'Uitvoer'),
        (OPLEVERING, 'Oplevering'),
        (OVERIG, 'Overig')
    ]
    fase = models.CharField(max_length=3, choices=CHOICES)
    description = models.TextField()
    activities = models.ManyToManyField(ProjectActiviteit)

    def __str__(self):
        return self.fase

