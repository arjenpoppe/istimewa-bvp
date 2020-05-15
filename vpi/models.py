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
    value = None

    def __str__(self):
        return f'{self.name}'

    def get_value(self, project_number=None):
        """
        generic function which calls the function that returns the values for this specific vpi
        @param project_number: (optional) project number
        @return: data in json format
        """
        # TODO fix caching; problem caused by get_vpi_target
        if self.function:
            if not self.value:
                self.value = getattr(vpis, f'{self.function}')(project_number)
                return self.value
            else:
                return self.value

    def get_target(self, project_id=None):
        """
        Returns the targat which is set for a vpi in de database
        @param project_id: (optional) get target for specific project
        @return: VPITarget object
        """
        return self.vpitarget_set.get(project_id=project_id)

    def get_target_color(self, project_id=None):
        """
        Returns the target related color (green/yellow/res)
        @param project_id: (optional) get target color for specific project
        @return: color as string
        """
        target = self.get_target()
        upper_limit = target.upper_limit
        lower_limit = target.lower_limit

        if lower_limit <= self.get_value() <= upper_limit:
            return 'warning'
        elif target.is_better == 'higher':
            if self.get_value() > upper_limit:
                return 'success'
            else:
                return 'danger'
        elif target.is_better == 'lower':
            if self.get_value() < lower_limit:
                return 'success'
            else:
                return 'danger'


class VPIDataContainer:
    def __init__(self, vpi, data):
        self.vpi = vpi
        self.data = data


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
