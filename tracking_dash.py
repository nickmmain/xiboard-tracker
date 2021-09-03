import os
from flask import Flask, app, render_template, url_for
from test_data import get_all
from glob import glob


app = Flask(__name__)
_STATES = ['New', 'Testing: Inspection', 'Testing: HW Tests',
           'Testing: Automated Functional', 'Testing: Thermal Tests', 'In Inventory']


@app.route('/')
def welcome():
    test_data = get_all()
    return render_template('dash.html', states=_STATES, test_data=test_data)


@app.context_processor
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
