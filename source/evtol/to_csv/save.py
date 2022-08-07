import re, csv
from collections import OrderedDict
from evtol.utils import parameters
from .convert import Convert

class LimitVTOL:
    def __init__(self):
        self.analyzer = TextAnalyzer()
        self.params = [var for var in dir(parameters) if not var.startswith('__')]

    def limit_by_params(self, data):
        converted_data = {}
        for title, vtol_pair in data.items():
            converted_data[title] = {}
            for vtol, detail in vtol_pair.items():
                converted_data[title][vtol] = self.populate_params()
                for detail_key, detail_value in detail.items():
                    for param in self.params:
                        attr = getattr(parameters, param)
                        if detail_key in attr:
                            converted_data[title][vtol][param] = detail_value
        return converted_data

    def limit_capacity(self, converted_data, min_cap, max_cap):
        limited_result = dict()
        for title, vtol_pair in converted_data.items():
            limited_result[title] = dict()
            for vtol, detail in vtol_pair.items():
                for detail_key, detail_value in detail.items():
                    if detail_key == 'capacity':
                        if self.analyzer.has_numbers(detail_value):
                            detail_numbers = self.analyzer.get_numbers(detail_value)
                            if len(detail_numbers)==1:
                                if detail_numbers[0]<min_cap:
                                    continue
                            if max(detail_numbers)<=min_cap:
                                continue
                            if detail_value.find('No passengers')>=0:
                                continue
                            if max(detail_numbers)<=max_cap:
                                limited_result[title][vtol] = converted_data[title][vtol]
                                limited_result[title][vtol]['capacity'] = detail_value
        return limited_result

    def populate_params(self):
        result = OrderedDict()
        for param in self.params:
            result[param] = None
        return result

    @staticmethod
    def get_vtol_count(full_data):
        count = 0
        for vtol_pair in full_data.values():
            count += len(vtol_pair)
        return count


class TextAnalyzer:
    @staticmethod
    def has_numbers(inputString):
        if inputString is not None:
            return any(char.isdigit() for char in inputString)

    @staticmethod
    def get_numbers(text):
        result = []
        numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)', text)
        for number in numbers:
            int_number = int(number.replace(',', ''))
            result.append(int_number)
        return result


class CSVHandler:
    def __init__(self):
        self._writer = None
        self.fieldnames = list()
        self.params = [var for var in dir(parameters) if not var.startswith('__')]

    def write(self, file_name:str, converted_data:dict):
        with open(file_name + '.csv', mode='w') as csv_file:
            self._create_headers(csv_file)
            for title, vtol_pair in converted_data.items():
                for vtol, detail in vtol_pair.items():
                    self._create_row(vtol, detail)

    def _create_headers(self, csv_file):
        self._add_vtol_name()
        self.writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def _create_row(self, vtol, data):
        data['vtol'] = vtol
        self.writer.writerow(data)

    def _add_vtol_name(self):
        self.fieldnames = ['vtol']
        self.fieldnames.extend(self.params)
