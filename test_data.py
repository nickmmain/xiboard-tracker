import csv
import os
import shutil
from tempfile import NamedTemporaryFile

_DATA_PATH = os.path.join(os.getcwd(), 'data', 'test_data.csv')
_TICKET = 'Ticket #'
_TRACKER = 'Tracker'
_STATUS = 'Status'
_SERIAL = 'Serial Number'
_VERSION = 'SW Version'
_CONFIG = 'Board Config'
_ASSIGNEE = 'Assignee'

_FIELDS = [_TICKET, _TRACKER, _STATUS, _SERIAL, _VERSION, _CONFIG, _ASSIGNEE]


def initialize_trackers():
    return read_column_values(_TRACKER)


def initialize_versions():
    return read_column_values(_VERSION)


def initialize_configs():
    return read_column_values(_CONFIG)


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


def new_ticket(assignee, serial, version, tracker, config):
    if(not assignee):
        raise ValueError('Empty assignee.')
    if(not serial):
        raise ValueError('Empty serial number.')
    if(not valid_serial(serial)):
        raise ValueError('Invalid serial number(duplicate?).')
    ticket_number = new_ticket_number()
    with open(_DATA_PATH, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, _FIELDS)
        writer.writerow({_TICKET: str(ticket_number), _TRACKER: tracker,
                        _STATUS: 'New', _SERIAL: serial, _VERSION: version, _CONFIG: config, _ASSIGNEE: assignee})


def move_ticket(ticket_number, destination_column):
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(_DATA_PATH, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, _FIELDS)
        writer = csv.DictWriter(tempfile, _FIELDS)
        for row in reader:
            if row[_TICKET] == str(ticket_number):
                print('Updating: Ticket {t} to column {col}'.format(
                    t=ticket_number, col=destination_column))
                row[_STATUS] = destination_column
            writer.writerow(row)
    shutil.move(tempfile.name, _DATA_PATH)


def new_ticket_number():
    max_val = 0
    with open(_DATA_PATH, 'r') as csvfile:
        reader = csv.DictReader(csvfile, _FIELDS)
        # skipping the first row(headers):
        next(reader)
        for row in reader:
            if(int(row[_TICKET]) > max_val):
                max_val = int(row[_TICKET])
    return max_val+1


def valid_serial(serial):
    with open(_DATA_PATH, 'r') as csvfile:
        reader = csv.DictReader(csvfile, _FIELDS)
        for row in reader:
            if(row[_SERIAL] == serial):
                return False
    return True
