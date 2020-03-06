from django.db import models

class Project(models.Model):
    number = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f'{self.number}: {self.name}'


class Source(models.Model):
    source_type = [
        ('FS','Filesystem'),
        ('DB','Database'),    
    ]
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class PerformanceIndicator(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    measuring_unit = models.CharField(max_length=20)
    formula = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20)
    sources = models.ManyToManyField(Source)
    pi_type = models.CharField(max_length=20)
    default_value_calc = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectGoal(models.Model):
    number = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=1000)
    performance_indicator = models.ManyToManyField(PerformanceIndicator)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number} for {self.project.name}'


class Target(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    green = models.IntegerField()
    yellow = models.IntegerField()
    red = models.IntegerField()
    performance_indicator = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE)


class Value(models.Model):
    performance_indicator = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value
