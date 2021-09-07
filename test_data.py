import csv
import os
import shutil
from tempfile import NamedTemporaryFile

_DATA_PATH = os.path.join(os.getcwd(), 'data', 'test_data.csv')
_FIELDS = ['Ticket #', 'Tracker', 'Status', 'Serial Number',
           'SW Version', 'Board Config', 'Assignee']


def initialize_trackers():
    return read_column_values(_FIELDS[1])


def initialize_states():
    return read_column_values(_FIELDS[2])


def initialize_versions():
    return read_column_values(_FIELDS[4])


def initialize_configs():
    return read_column_values(_FIELDS[5])


def read_column_values(columnTitle):
    columnValues = set()
    with open(_DATA_PATH, 'r') as csvfile:
        reader = csv.DictReader(csvfile, _FIELDS)
        # skipping the first row(headers):
        next(reader)
        for row in reader:
            columnValues.add(row[columnTitle])
    return columnValues


def get_all():
    with open(_DATA_PATH, newline='') as csvfile:
        return list(csv.DictReader(csvfile))


def move_ticket(ticket_number, destination_column):
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(_DATA_PATH, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, _FIELDS)
        writer = csv.DictWriter(tempfile, _FIELDS)
        for row in reader:
            if row['Ticket #'] == str(ticket_number):
                print('Updating: Ticket {t} to column {col}'.format(
                    t=ticket_number, col=destination_column))
                row['Status'] = destination_column
            writer.writerow(row)
    shutil.move(tempfile.name, _DATA_PATH)
