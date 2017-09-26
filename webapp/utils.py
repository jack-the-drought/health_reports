
import json
import dateutil.parser
import datetime
from pymongo import MongoClient
import os

def convert_to_datetime(isodate):
    return dateutil.parser.parse(isodate)

def get_last_week_isodate(date):
    return (convert_to_datetime(date)-datetime.timedelta(days=7)).isoformat()

def decrement_day(date):
    return (convert_to_datetime(date)-datetime.timedelta(days=1)).isoformat()

def return_data_as_json(data):
    return json.dumps(data)

def get_collection_using_env():
    try:
        development = os.environ['DEV']
    except:
        development = "True" #todo: invert when env set properly from docker-compose


    try:
        is_dockerized = os.environ['DOCKERENV']
        print is_dockerized

    except:
        is_dockerized = "True" #todo: invert when env set properly from docker-compose


    if is_dockerized == "False":

        client = MongoClient()
    else:
        client = MongoClient(host="mongo")
    if development == "True":
        db = client.kiwitest_dev
    else:
        db = client.kiwitest_prod
    return db.health_reports
