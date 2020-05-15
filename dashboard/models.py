from django.db import models

from data.models.project import Project
from vpi.models import VPIDataContainer
from vpi.models import VPI


class Dashboard(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

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

        print(object_rows)

        return object_rows


class DashboardObject(models.Model):
    AREA = 'area'
    CARD = 'card'
    BAR = 'bar'
    PIE = 'pie'
    CHART_CHOICES = [
        (AREA, 'Area chart'),
        (CARD, 'Card'),
        (BAR, 'Bar chart'),
        (PIE, 'Pie chart')
    ]

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    vpi = models.ForeignKey(to='vpi.VPI', on_delete=models.CASCADE)
    chart_type = models.CharField(max_length=10, choices=CHART_CHOICES)
    col_width = models.IntegerField()
    row_number = models.IntegerField()
    row_order = models.IntegerField()

    def get_vpi_data(self):
        """
        Return data for vpi's included in this dashboard
        @return: list of VPIDataContainer
        """
        vpi_data = None
        if self.dashboard.project:
            vpi_data = self.vpi.get_value(self.dashboard.project.number)
        else:
            vpi_data = self.vpi.get_value()

        print('dashboard get_vpi_data called', vpi_data)

        return vpi_data


# class ProjectDashboard(GeneralDashboard):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#
#     def get_vpi_data(self):
#         """
#         Return data for vpi's included in this dashboard
#         @return: list of VPIDataContainer
#         """
#         vpi_data_list = []
#
#         for vpi in self.vpis.all():
#             vpi_data = vpi.get_value(self.project.number)
#             vpi_data_list.append(VPIDataContainer(vpi, vpi_data))
#
#         return vpi_data_list





class Report(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)


