import csv


class CSVLib:

    def __init__(self, file, fields):
        self._writer = csv.DictWriter(file, fieldnames=fields)
