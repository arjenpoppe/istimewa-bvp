from django.db import models

from data.models.project import Project
from vpi.models import VPI


class Dashboard(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.project:
            return f'{self.project.number}: {self.project.name}'
        else:
            return self.name

    def get_ordered_objects(self):
        """
        Return dastboard objects ordered by row number and row order
        @return: Queryset of DashboardObjects
        """
        return DashboardObject.objects.order_by('row_number', 'row_order').filter(dashboard=self)

    def get_ordered_objects_by_row(self):
        """
        Returns DashboardObjects divided into a list per row
        @return: List of Querysets
        """
        row_amount = DashboardObject.objects.values('row_number').filter(dashboard=self).distinct().count()

        object_rows = []

        for row_number in range(1, row_amount + 1):
            object_rows.append(DashboardObject.objects.filter(dashboard=self, row_number=row_number).order_by('row_order'))

        return object_rows


class DashboardObject(models.Model):
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

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    vpi = models.ForeignKey(to='vpi.VPI', on_delete=models.CASCADE)
    chart_type = models.CharField(max_length=10, choices=CHART_CHOICES)
    col_width = models.IntegerField()
    row_number = models.IntegerField()
    row_order = models.IntegerField()
    vpi_data = None

    class Meta(object):
        unique_together = (('dashboard', 'row_number', 'row_order'),)

    def get_vpi_data(self):
        """
        Return data for vpi's included in this dashboard
        @return: VPI data in either a dictionary or float format.
        """
        if not self.vpi_data:
            self.vpi_data = self.vpi.get_value(self.dashboard.project)

        return self.vpi_data

    def get_vpi_target_color(self):
        """
        Returns the target color of a vpi value.
        @return: bootstrap color (danger/warning/success)
        """
        vpi_value = self.get_vpi_data()
        if not vpi_value is None:
            vpi_target = self.vpi.get_target(self.dashboard.project)
            upper_limit = vpi_target.upper_limit
            lower_limit = vpi_target.lower_limit

            if lower_limit <= vpi_value <= upper_limit:
                return 'warning'
            elif vpi_target.is_better == 'higher':
                if vpi_value > upper_limit:
                    return 'success'
                else:
                    return 'danger'
            elif vpi_target.is_better == 'lower':
                if vpi_value < lower_limit:
                    return 'success'
                else:
                    return 'danger'


class Report(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)


