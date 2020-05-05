from django.db import models


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

    def __str__(self):
        return f'{self.number}: {self.name}'


class ProjectGoal(models.Model):
    number = models.IntegerField()
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    goal = models.TextField()

    def __str__(self):
        return f'{self.project.number}:{self.project.name} - Projectdoel {self.number}'


class VPI(models.Model):
    AREA = 'AC'
    CARD = 'CA'
    BAR = 'BC'
    PIE = 'PC'
    CHOICES = [
        (AREA, 'Area chart'),
        (CARD, 'Card'),
        (BAR, 'Bar chart'),
        (PIE, 'Pie chart')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    measuring_unit = models.CharField(max_length=20, blank=True)
    formula = models.CharField(max_length=200, blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    chart_type = models.CharField(max_length=2, choices=CHOICES)
    project = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return f'{self.name}'


class VPITarget(models.Model):
    LOWER = 'lower'
    HIGHER = 'higher'
    CHOICES = [
        (LOWER, 'Lower'),
        (HIGHER, 'Higher')
    ]
    vpi = models.ForeignKey(VPI, on_delete=models.CASCADE)
    lower_limit = models.FloatField()
    upper_limit = models.FloatField()
    is_better = models.CharField(max_length=6, choices=CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.project:
            return f'{str(self.project)}'
        else:
            return f'VPI: {str(self.vpi)}'


class VPIValue(models.Model):
    value = models.FloatField()
    vpi = models.ForeignKey(VPI, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)

    def get_target_color(self):
        target = self.vpi.vpitarget_set.last()
        upper_limit = target.upper_limit
        lower_limit = target.lower_limit

        if lower_limit <= self.value <= upper_limit:
            return 'warning'
        elif target.is_better == 'higher':
            if self.value > upper_limit:
                return 'success'
            else:
                return 'danger'
        elif target.is_better == 'lower':
            if self.value < lower_limit:
                return 'success'
            else:
                return 'danger'

