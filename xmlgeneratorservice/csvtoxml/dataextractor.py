from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import csv
from cleaner import Cleaner


class DataExtractor(ABC):

    @abstractmethod
    def extract_data(self, data: List):
        pass


class CsvDataExtractor(DataExtractor):
    def extract_data(self, filename):
        csv_file = filename
        csv_data = csv.reader(open(csv_file, 'r'), delimiter=',')
        csv_data = list(csv_data)
        c = Cleaner()
        csv_data = c.clean(csv_data)
        return csv_data
