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
        self._data = self.model.objects.filter(**filters)

    def annotate(self, annotation):
        self._data = self._data.annotate(**annotation)

    def aggregate(self, aggregation):
        self._data = self._data.aggregate(**aggregation)

    @property
    def data(self):
        return self._data
