from django.db import models
from django.contrib.admin.utils import quote


class Address(models.Model):
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=10)
    street = models.CharField(max_length=20)
    number = models.IntegerField()
    number_addition = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return f'{self.street} {self.number}{self.number_addition if self.number_addition else ""}, {self.postal_code} {self.city}'


class Opdrachtgever(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class OpdrachtgeverContactPersoon(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    opdrachtgever = models.ForeignKey(Opdrachtgever, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Project(models.Model):
    number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    opdrachtgever = models.ForeignKey(Opdrachtgever, on_delete=models.CASCADE, null=True)
    object_amount = models.IntegerField(default=1)
    vpis = models.ManyToManyField(to='vpi.VPI', blank=True)

    def __str__(self):
        return f'{self.number}: {self.name}'

    def encode_number(self):
        return quote(self.number)


class ProjectGoal(models.Model):
    number = models.IntegerField()
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    goal = models.TextField()

    def __str__(self):
        return f'{self.project.number}:{self.project.name} - Projectdoel {self.number}'


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
