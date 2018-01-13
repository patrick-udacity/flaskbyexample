import os  
os.environ['PYTHON_EGG_CACHE'] = '/tmp' # a writable directory
from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import dateparser
import datetime
import json
import string

app = Flask(__name__)
DB = DBHelper()
categories = dict([
    ('Asian','Asian'),
    ('Breakfast','Breakfast'),
    ('BBQ','BBQ'),
    ('Cajun','Cajun'),
    ('Deli','Deli'),
    ('Italian','Italian'),
    ('Mexican','Mexican'),
    ('PubGrub','PubGrub'),
    ('Seafood','Seafood'),
    ('Southern','Southern'),
    ('Other','Other/Unspecified'),
    ('Burger','Burger')
])


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None

def sanitize_string(userinput):
    whitelist = string.letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput)


@app.route("/")
def home(error_message=None):
    try:
        diningEvents = DB.get_all_diningEvents()
        diningEvents = json.dumps(diningEvents)
    except Exception as e:
        print e
        data = e
    return render_template("home.html", 
        diningEvents=diningEvents,
        categories=categories,
        error_message=error_message
    )


@app.route("/submitDiningEvent", methods=['POST'])
def submitDiningEvent():
    category = request.form.get("category")
    if category not in categories:
        return home()
    
    #Retrive and validate the date.
    date = request.form.get("date")
    date = format_date(date)
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")

    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()

    description = sanitize_string(request.form.get("description"))
    DB.add_diningEvent(category, date, latitude, longitude, description)
    return home()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
