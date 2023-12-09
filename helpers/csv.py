import csv


def csv_writer(file, fields: list[str]) -> csv.DictWriter:
    return csv.DictWriter(file, fieldnames=fields)
