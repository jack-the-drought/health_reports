from flask import Flask, render_template, request
from utils import return_data_as_json, get_collection_using_env
from part2 import Fetcher
import datetime


app = Flask(__name__)
fetcher = Fetcher(get_collection_using_env())


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/view1')
def view1():
    day = request.args.get('day')  # add check if isset to avoid crush
    top_devices = fetcher.fetch_top_from_day(day)
    for device in top_devices:
        device["change"] = fetcher.get_percentage_change_from_last_week(
            device["_id"], day, device["count"])
        device["id"] = device["_id"]
        device.pop("_id")
    return return_data_as_json(top_devices)


@app.route('/view2')
def view2():
    status = request.args.get('status')
    device_type = request.args.get('type')
    day = datetime.datetime.now().isoformat()
    day = "2017-06-01T02:49:25.992621"
    return return_data_as_json(
        fetcher.get_devices_last_thirty_days(day, status, device_type)
    )


@app.route('/statusesntypes')
def statusesntypes():
    return return_data_as_json(fetcher.fetch_available_types_and_statuses())


if __name__ == "__main__":

    app.run('0.0.0.0', 5000, debug=True)
