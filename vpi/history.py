import abc


class History:
    vpi = None
    model = None
    filters = []

    def __init__(self, vpi, model, interval='month', **filters):
        self.vpi = vpi
        self.model = model
        self.filters = filters

    @abc.abstractmethod
    def get_data(self):
        return


class UltimoHistory(History):
    def get_data(self):
        pass
