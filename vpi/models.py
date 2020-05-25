from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.managers import InheritanceManager


class VPI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    measuring_unit = models.CharField(max_length=20, blank=True)
    function = models.CharField(max_length=30, null=True, blank=True)
    has_subset = models.BooleanField(default=False)
    decimal_amount = models.IntegerField(default=2)

    def __str__(self):
        return f'{self.name}'

    # def get_value(self, project=None):
    #     """
    #     Generic function which calls the related vpi function, returning the values for this specific vpi. Returns
    #     cached data if available.
    #     @param project: (optional) project object
    #     @return: data can be dictionary or float
    #     """
    #     if self.function:
    #         return getattr(vpis, f'{self.function}')(project)

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
    vpi = models.ForeignKey(VPI, on_delete=models.CASCADE)
    happened = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    project_number = models.CharField(max_length=8, null=True, blank=True)
    objects = InheritanceManager()


class VPIValueNumber(VPIValue):
    value = models.FloatField()


class VPIValueBoolean(VPIValue):
    value = models.BooleanField()


class VPITarget(models.Model):
    LOWER = 'lower'
    HIGHER = 'higher'
    CHOICES = [
        (LOWER, 'Lager is beter'),
        (HIGHER, 'Hoger is better')
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
