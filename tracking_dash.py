import os
import json
from flask import Flask, app, render_template, url_for, request
from test_data import get_all, move_ticket
from glob import glob


app = Flask(__name__)
_STATES = ['New', 'Testing: Inspection', 'Testing: HW Tests',
           'Testing: Automated Functional', 'Testing: Thermal Tests', 'In Inventory']


@app.route('/')
def welcome():
    test_data = get_all()
    return render_template('dash.html', states=_STATES, test_data=test_data)


@app.route('/data', methods=['PUT', 'POST'])
def test_data():
    if(request.method == 'PUT'):
        payload = request.json
        move_ticket(payload['ticketId'], payload['targetColumn'])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    if(request.method == 'POST'):
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@ app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


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
