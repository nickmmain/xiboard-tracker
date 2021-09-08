import csv
import os
import shutil
import dateutil.parser as dparser
from tempfile import NamedTemporaryFile

_DATA_PATH = os.path.join(os.getcwd(), 'data', 'customer_data.csv')
_ASSEMBLY_NO = 'Assembly #'
_ASSEMBLY_NAME = 'Assembly Name'
_STATUS = 'Status'
_NAME = 'Customer Name'
_UNITS = 'Desired Units'
_CONFIG = 'Unit Config'
_DATE = 'Delivery Date'
_DUT = 'DUT SN'
_DUT_DB = 'DUT-DB SN'


_FIELDS = [_ASSEMBLY_NO, _ASSEMBLY_NAME, _STATUS,
           _NAME, _UNITS, _CONFIG, _DATE, _DUT, _DUT_DB]


def get_all_customer_data(grouped_by_date=False):
    with open(_DATA_PATH, newline='', encoding='utf-8-sig') as csvfile:
        customer_data = list(csv.DictReader(csvfile))
        customer_data.sort(key=bydate)
        if(grouped_by_date):
            return group_by_date(customer_data)
        return customer_data


def group_by_date(orders_list):
    date = ''
    grouped_orders = {}
    for order in orders_list:
        if(order[_DATE] == date):
            grouped_orders[date].append(order)
        else:
            date = order[_DATE]
            grouped_orders[date] = []
            grouped_orders[date].append(order)
    return grouped_orders


def bydate(row):
    return dparser.parse(row[_DATE]).timestamp()


def assign_boards(assembly_no, dut_serial, dut_db_serial):
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(_DATA_PATH, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, _FIELDS)
        writer = csv.DictWriter(tempfile, _FIELDS)
        for row in reader:
            if row[_ASSEMBLY_NO] == str(assembly_no):
                print('Updating: Assembly number {a} with boards {dut} and {dut_db}'.format(
                    a=assembly_no, dut=dut_serial, dut_db=dut_db_serial))
                if(dut_serial):
                    row[_DUT] = dut_serial
                if(dut_db_serial):
                    row[_DUT_DB] = dut_db_serial
            writer.writerow(row)
    shutil.move(tempfile.name, _DATA_PATH)
