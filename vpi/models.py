from django.db import models
from vpi import vpis


class VPI(models.Model):
    AREA = 'AC'
    CARD = 'CA'
    BAR = 'BC'
    PIE = 'PC'
    CHART_CHOICES = [
        (AREA, 'Area chart'),
        (CARD, 'Card'),
        (BAR, 'Bar chart'),
        (PIE, 'Pie chart')
    ]

    AVG = 'avg'
    LAST = 'last'
    FIRST = 'first'
    SINGLE = 'single'
    MEASURE_CHOICES = [
        (AVG, 'Gemiddlede'),
        (LAST, 'Laatste'),
        (FIRST, 'Eerste'),
        (SINGLE, 'Enkele waarde')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    measuring_unit = models.CharField(max_length=20, blank=True)
    formula = models.CharField(max_length=200, blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    chart_type = models.CharField(max_length=2, choices=CHART_CHOICES)
    label = models.CharField(max_length=20)
    function = models.CharField(max_length=30, null=True, blank=True)
    has_subset = models.BooleanField(default=False)
    decimal_amount = models.IntegerField(default=2)

    def __str__(self):
        return f'{self.name}'

    def get_value(self, project=None):
        """
        Generic function which calls the function that returns the values for this specific vpi. Returns cached value
        if available.
        @param project: (optional) project object
        @return: data can be dictionary or float
        """
        return getattr(vpis, f'{self.function}')(project)

    def get_target(self, project=None):
        """
        Returns the targat which is set for a vpi in de database
        @param project: (optional) get target for specific project
        @return: VPITarget object
        """
        try:
            return self.vpitarget_set.get(project=project)
        except VPITarget.DoesNotExist:
            return self.vpitarget_set.get()
        except VPITarget.DoesNotExist:
            return None


class VPIValue(models.Model):
    value = models.FloatField()
    vpi = models.ForeignKey(VPI, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)


class VPITarget(models.Model):
    LOWER = 'lower'
    HIGHER = 'higher'
    CHOICES = [
        (LOWER, 'Lower'),
        (HIGHER, 'Higher')
    ]
    vpi = models.ForeignKey(to='vpi.VPI', on_delete=models.CASCADE)
    lower_limit = models.FloatField()
    upper_limit = models.FloatField()
    is_better = models.CharField(max_length=6, choices=CHOICES)
    project = models.ForeignKey(to='data.Project', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.project:
            return f'{str(self.project)}'
        else:
            return f'VPI: {str(self.vpi)}'
