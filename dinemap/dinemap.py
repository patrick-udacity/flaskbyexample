from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json


app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():
    try:
        diningEvents = DB.get_all_diningEvents()
        diningEvents = json.dumps(diningEvents)
    except Exception as e:
        print e
        data = e
    return render_template("home.html", diningEvents=diningEvents)


@app.route("/add", methods=["POST","GET"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print e
    return home()

@app.route("/submitDiningEvent", methods=['POST'])
def submitDiningEvent():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_diningEvent(category, date, latitude, longitude, description)
    return home()

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print e
    return home()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
