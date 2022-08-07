from .to_csv.convert import Convert
from .to_csv.save import LimitVTOL, CSVHandler
from .utils.config import DETAIL_PATH

class SaveToCsv:
    def __init__(self):
        self.csv = CSVHandler()
        self.limit = LimitVTOL()
        self.converter = self.get_converter()

    @property
    def data(self):
        data = self.converter.converted_data
        return data

    @property
    def limited_by_params(self):
        limited_data = self.limit.limit_by_params(
            self.converter.converted_data
        )
        return limited_data

    @property
    def limited_by_capacity(self):
        limited_data = self.limit.limit_capacity(
            self.converter.converted_data,
            min_cap=3,
            max_cap=6
        )
        return limited_data

    @property
    def limited_by_params_by_capacity(self):
        limited_data = self.limit.limit_capacity(
            self.limited_by_params,
            min_cap=3,
            max_cap=6
        )
        return limited_data

    def save(self, name, data):
        self.csv.write(name, data)

    @staticmethod
    def get_converter():
        converter = Convert(DETAIL_PATH)
        converter.execute()
        return converter
