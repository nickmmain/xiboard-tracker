import csv
import os
import dateutil.parser as dparser

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


def get_all_customer_data():
    with open(_DATA_PATH, newline='') as csvfile:
        customer_data = list(csv.DictReader(csvfile))
        customer_data.sort(key=bydate)
        return customer_data


def bydate(row):
    return dparser.parse(row[_DATE]).timestamp()
