from enum import Enum

from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.managers import InheritanceManager

from data.models.other import DataContainer
from data.models.prestatiemeting import Prestatiemeting
from vpi import vpis


class VPIAction(Enum):
    AVG = 'average'
    HIGH = 'highest'
    LOW = 'lowest'
    SUM = 'total'


class VPIInterval(Enum):
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'
    NONE = 'none'


class VPISource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    model_name = models.CharField(max_length=100)
    datefield = models.CharField(max_length=100)
    projectfield = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class VPI(models.Model):
    name = models.CharField(max_length=100)
    question = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    measuring_unit = models.CharField(max_length=20, blank=True)
    function = models.CharField(max_length=30, null=True, blank=True)
    has_subset = models.BooleanField(default=False)
    decimal_amount = models.IntegerField(default=2)
    source = models.ForeignKey(VPISource, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    @property
    def detail_config(self):
        return self.vpidetailconfig

    def get_value(self, project):
        """
        Generic function which calls the related vpi function, returning the values for this specific vpi. Returns
        cached data if available.
        @param filters: (optional) filters
        @return: data can be dictionary or float
        """
        if self.function:
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

    def get_color(self, value):
        target = self.vpitarget_set.get(project__isnull=True)
        upper_limit = target.upper_limit
        lower_limit = target.lower_limit

        if lower_limit <= value <= upper_limit:
            return 'warning'
        elif target.is_better == 'higher':
            if value > upper_limit:
                return 'success'
            else:
                return 'danger'
        elif target.is_better == 'lower':
            if value < lower_limit:
                return 'success'
            else:
                return 'danger'


class VPIValue(models.Model):
    vpi = models.ForeignKey(VPI, on_delete=models.CASCADE)
    happened = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    project_number = models.CharField(max_length=8, null=True, blank=True)
    objects = InheritanceManager()


class VPIValueNumber(VPIValue):
    value = models.FloatField()


class VPIValueList(VPIValue):
    @property
    def value(self):
        return list(self.listvalue_set.values_list('value', flat=True))

    @value.setter
    def value(self, value_list):
        for item in value_list:
            ListValue(list=self, value=item).save()


class ListValue(models.Model):
    list = models.ForeignKey(VPIValueList, on_delete=models.CASCADE)
    value = models.FloatField()


class VPIValuePrestatiemeting(VPIValue):
    prestatiemeting = models.ForeignKey(Prestatiemeting, on_delete=models.CASCADE)

    @property
    def value(self):
        return self.prestatiemeting.prestatiemetingresult_set.all()

    @value.setter
    def value(self, prestatiemeting):
        self.prestatiemeting = prestatiemeting


class VPIData:
    # list of strings
    datetimes = []

    # list or nested lists. e.g. [1, 2, 3, 4] or [[1, 2, 3, 4],[5, 6, 7, 8]]
    data = []

    def __init__(self, data, labels):
        self.data = data
        self.datetimes = labels


class VPIDetailConfig(models.Model):
    LINE = 'line'
    BAR = 'bar'

    CHART_CHOICES = [
        (LINE, 'Line chart'),
        (BAR, 'Bar chart'),
    ]

    vpi = models.OneToOneField(VPI, on_delete=models.CASCADE)
    available_filters = models.CharField(max_length=10)
    chart_type = models.CharField(max_length=10, choices=CHART_CHOICES)


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


class VPIDetailObject(models.Model):
    AREA = 'area'
    CARD = 'card'
    BAR = 'bar'
    PIE = 'pie'
    TABLE = 'table'
    PROGRESS = 'progress'
    CHART_CHOICES = [
        (AREA, 'Area chart'),
        (CARD, 'Card'),
        (BAR, 'Bar chart'),
        (PIE, 'Pie chart'),
        (TABLE, 'Table'),
        (PROGRESS, 'Progress')
    ]

    vpi = models.ForeignKey(to='vpi.VPI', on_delete=models.CASCADE)
    chart_type = models.CharField(max_length=10, choices=CHART_CHOICES)
    width = models.IntegerField()
    _data = None

    @property
    def filters(self):
        """
        Return collection of filters in a dictionary format
        @return: Dict with filters
        """
        filter_dict = {}
        filters = FilterObject.objects.filter(vpi_detail_object=self).select_subclasses()
        for filter_object in filters:
            filter_dict[filter_object.filter_by] = filter_object.filter_value

        return filter_dict

    def get_data_test(self):
        container = DataContainer(self.vpi.source.model_name)
        container.apply_filters(self.filters)
        return container

    @property
    def targets(self):
        return self.vpi.vpitarget_set.all()

    @property
    def vpi_data(self):
        """
        Return data for vpi's included in this dashboard
        @return: VPI data in either a dictionary or float format.
        """
        if not self._data:
            self._data = self.vpi.get_value(self.filters)

        return self._data


class FilterObject(models.Model):
    vpi_detail_object = models.ForeignKey(VPIDetailObject, on_delete=models.CASCADE)
    filter_by = models.CharField(max_length=100)
    filter_value = None
    objects = InheritanceManager()


class FilterObjectBoolean(FilterObject):
    filter_value = models.BooleanField()


class FilterObjectString(FilterObject):
    filter_value = models.CharField(max_length=100)


class FilterObjectDateTime(FilterObject):
    filter_value = models.DateTimeField()