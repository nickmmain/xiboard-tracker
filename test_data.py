import csv
import os
import shutil
from tempfile import NamedTemporaryFile

_DATA_PATH = os.path.join(os.getcwd(), 'data', 'test_data.csv')
_FIELDS = ['Ticket #', 'Tracker', 'Status', 'Serial Number',
           'SW Version', 'Board Config', 'Assignee']


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
