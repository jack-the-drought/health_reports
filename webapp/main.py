from flask import Flask, render_template , request
import json
from part2 import *
import os
app = Flask(__name__)
development = os.environ['DEV']
client = MongoClient(host="mongo")

if development == "True":
    db = client.kiwitest_dev
else:
    db = client.kiwitest_prod

health_reports = db.health_reports

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/view1')
def view1():
    day = request.args.get('day')#add check if isset to avoid crush
    top_devices = fetch_top_from_day(day)
    for device in top_devices:
        device["change"] = get_percentage_change_from_last_week(device["_id"],day,device["count"])
        device["id"] = device["_id"]
        device.pop("_id")
    return json.dumps(top_devices)


@app.route('/view2')
def view2():
    status = request.args.get('status')
    device_type = request.args.get('type')
    day = datetime.datetime.now().isoformat()
    return json.dumps(get_devices_last_thirty_days(day,status,device_type))


@app.route('/statusesntypes')
def statusesntypes():
    return json.dumps(fetch_available_types_and_statuses())


if __name__ == "__main__":
    app.run('0.0.0.0',5000,debug = True)
