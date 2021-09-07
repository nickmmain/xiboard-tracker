import os
import json
from flask import Flask, app, render_template, url_for, request, redirect
from test_data import initialize_versions, initialize_configs, initialize_trackers, get_all, move_ticket, new_ticket
from glob import glob


app = Flask(__name__)
_STATES = ['New', 'Testing: Inspection', 'Testing: HW Tests',
           'Testing: Automated Functional', 'Testing: Thermal Tests', 'In Inventory']
_SUBMISSION_ERROR = ''


@app.route('/')
def welcome():
    _VERSIONS = initialize_versions()
    _CONFIGS = initialize_configs()
    _TRACKERS = initialize_trackers()

    test_data = get_all()
    return render_template('dash.html', test_data=test_data, states=_STATES, versions=_VERSIONS, configs=_CONFIGS, trackers=_TRACKERS, sub_error=_SUBMISSION_ERROR)


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
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except ValueError as error:
            global _SUBMISSION_ERROR
            _SUBMISSION_ERROR = error.args[0]
            return redirect(url_for('welcome'))


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
