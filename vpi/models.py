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
    default_measure = models.CharField(max_length=10, choices=MEASURE_CHOICES)

    def __str__(self):
        return f'{self.name}'

    def get_value(self, *args):
        if self.function:
            result = getattr(vpis, f'{self.function}_{self.default_measure}')(args)
            return result

    def get_target(self, project_id=None):
        return self.vpitarget_set.get(project_id=project_id)

    # def get_target_color(self):
    #     target = self.get_target()
    #     upper_limit = target.upper_limit
    #     lower_limit = target.lower_limit
    #
    #     if lower_limit <= self.get_value() <= upper_limit:
    #         return 'warning'
    #     elif target.is_better == 'higher':
    #         if self.get_value() > upper_limit:
    #             return 'success'
    #         else:
    #             return 'danger'
    #     elif target.is_better == 'lower':
    #         if self.get_value() < lower_limit:
    #             return 'success'
    #         else:
    #             return 'danger'


class CombinedVPI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    chart_type = models.CharField(max_length=2, choices=VPI.CHART_CHOICES)
    vpis = models.ManyToManyField(VPI)

    def get_last_value_list(self, *args):
        data = []
        for vpi in self.vpis.all():
            data.append(vpi.get_value(*args))

        return data

    def get_labels_list(self):
        labels = []
        for vpi in self.vpis.all():
            labels.append(vpi.label)

        return labels


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
