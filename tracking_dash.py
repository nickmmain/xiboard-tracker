import os
import json
from flask import Flask, app, render_template, url_for, request, redirect
from test_data import initialize_versions, initialize_configs, initialize_trackers, get_all_test_data, move_ticket, new_ticket, get_inventory, remove_ticket_by_serial
from customer_data import get_all_customer_data, assign_boards
from glob import glob


app = Flask(__name__)
_STATES = ['New', 'Testing: Inspection', 'Testing: HW Tests',
           'Testing: Automated Functional', 'Testing: Thermal Tests', 'In Inventory']
_CUSTOMER_DISPLAY_HEADERS = ['Assembly #', 'Status', 'Delivery Date',
                             'Desired Units', 'Unit Config', 'DUT SN', 'DUT-DB SN']
_SUBMISSION_ERROR = ''


@app.route('/')
def welcome():
    _VERSIONS = initialize_versions()
    _CONFIGS = initialize_configs()
    _TRACKERS = initialize_trackers()

    test_data = get_all_test_data()
    customer_data = get_all_customer_data()
    return render_template('dash.html', test_data=test_data, states=_STATES, versions=_VERSIONS,
                           configs=_CONFIGS, trackers=_TRACKERS, sub_error=_SUBMISSION_ERROR, customer_data=customer_data,
                           customer_headers=_CUSTOMER_DISPLAY_HEADERS)


@app.route('/data', methods=['PUT', 'POST'])
def test_data():
    if(request.method == 'PUT'):
        payload = request.json
        move_ticket(payload['ticketId'], payload['targetColumn'])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    if(request.method == 'POST'):
        try:
            new_ticket(request.form['assignee'], request.form['serial'],
                       request.form['version'], request.form['board'], request.form['config'])
        except ValueError as error:
            global _SUBMISSION_ERROR
            _SUBMISSION_ERROR = error.args[0]
            return redirect(url_for('welcome'))
        clear_error()
        return redirect(url_for('welcome'))


@app.route('/orders', methods=['POST'])
def assign_inventory():
    orders = get_all_customer_data()
    for order in orders:
        # if the order does not already have units assigned.
        if(not(order['DUT SN'] or order['DUT-DB SN'])):
            inventory = get_inventory()
            # a double-board order
            if(',' in order['Desired Units']):
                dut = filter_inventory(
                    inventory, 'DUT', order['Unit Config'])
                dut_db = filter_inventory(
                    inventory, 'DUT-Daughterboard', order['Unit Config'])
                if(dut is not None and dut_db is not None):
                    assign_boards(
                        order['Assembly #'], dut['Serial Number'], dut_db['Serial Number'])
                    remove_ticket_by_serial(dut['Serial Number'])
                    remove_ticket_by_serial(dut_db['Serial Number'])
            elif('DUT-DB' in order['Desired Units']):
                dut_db = filter_inventory(
                    inventory, 'DUT-Daughterboard', order['Unit Config'])
                if(dut_db is not None):
                    assign_boards(
                        order['Assembly #'], None,  dut_db['Serial Number'])
                    remove_ticket_by_serial(dut_db['Serial Number'])
            else:
                dut = filter_inventory(
                    inventory, 'DUT', order['Unit Config'])
                if(dut is not None):
                    assign_boards(
                        order['Assembly #'], dut,  None)
                    remove_ticket_by_serial(dut['Serial Number'])
    return redirect(url_for('welcome'))


def filter_inventory(inventory, tracker, config):
    return next((x for x in inventory if x['Tracker'] == tracker and config in x['Board Config']), None)


@ app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def clear_error():
    global _SUBMISSION_ERROR
    _SUBMISSION_ERROR = ''


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


def glob_assets(target):
    root = app.static_folder
    return [f[len(root)+1:] for f in glob(os.path.join(root, target))]


app.jinja_env.globals.update(get_assets=glob_assets)
