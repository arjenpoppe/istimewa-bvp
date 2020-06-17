from django.apps import apps
from django.db import models
from django.db.models import QuerySet


class DataContainer:
    model: models.Model = None
    _data: QuerySet = None
    tmp_data: QuerySet = None

    def __init__(self, model_name):
        self.model = apps.get_model(app_label='data', model_name=model_name)

    def apply_filters(self, filters):
        """
        Apply filters so Datacontainer object
        @param filters: Filters in dictionary format
        """
        self._data = self.model.objects.filter(**filters)

    def annotate(self, annotation):
        """
        Apply annotation to datacontainer object
        @param annotation: annotation in dictionary format
        """
        self._data = self._data.annotate(**annotation)

    def aggregate(self, aggregation):
        """
        Apply aggregation to datacontainer object
        @param aggregation: aggregation in dictionary format
        """
        self._data = self._data.aggregate(**aggregation)

    @property
    def data(self):
        """
        data property of datacontainer object
        @return: Queryset
        """
        return self._data
