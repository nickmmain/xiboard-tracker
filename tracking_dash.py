from flask import Flask, app, render_template
from test_data import get_all

app = Flask(__name__)
_STATES = ['New', 'Testing: Inspection', 'Testing: HW tests',
           'Testing: Automated Functional', 'Testing: Thermal Tests', 'In Inventory']


@app.route('/')
def welcome():
    test_data = get_all()
    return render_template('dash.html', states=_STATES, test_data=test_data)
