import csv
import json
import os

_DATA_PATH = os.path.join(os.getcwd(), 'data', 'test_data.csv')
_FIELDS = []


def get_all():
    with open(_DATA_PATH, newline='') as csvfile:
        return list(csv.DictReader(csvfile))


def get_new():
    with open(_DATA_PATH, newline='') as csvfile:
        for row in list(csv.DictReader(csvfile)):
            if (row['Status']) == 'New':
                print(row)
