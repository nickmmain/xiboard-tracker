import csv
import json
import os

_DATA_PATH = os.path.join(os.getcwd(), 'data', 'customer_data.csv')


def getAll():
    with open(_DATA_PATH, newline='') as csvfile:
        for row in list(csv.DictReader(csvfile)):
