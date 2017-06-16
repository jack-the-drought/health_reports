from __future__ import division
import datetime
import dateutil.parser
from pymongo import MongoClient
import re
import itertools

Development = True
client = MongoClient(host="mongo")

if Development == True:
    db = client.kiwitest_dev
else:
    db = client.kiwitest_prod

health_reports = db.health_reports

def convert_to_datetime(isodate):
    return dateutil.parser.parse(isodate)

def fetch_top_from_day(date,collection=None):
    pipeline = [
                     { "$match": { "timestamp":re.compile("^"+date[:10]) } },
                     { "$group": { "_id": "$id", "count": { "$sum": 1 } } },
                     { "$sort" : { "count": -1 } }
               ]
    if collection:
        b = collection.aggregate(pipeline)
    else:
        b = health_reports.aggregate(pipeline)
    top10 = itertools.islice(b, 10)
    l = []
    for i in top10:
        l.append(i)
    return l
def get_last_week_isodate(date):
    return (convert_to_datetime(date)-datetime.timedelta(days=7)).isoformat()


def get_percentage_change_from_last_week(deviceid, date, new_count, collection=None):
        pipeline = [
                         { "$match": { "timestamp":re.compile("^"+get_last_week_isodate(date)[:10]) , "id":deviceid} },
                         { "$group": { "_id": "$id", "count": { "$sum": 1 } } },
                   ]
        if collection:
            info = collection.aggregate(pipeline)
        else:
            info = health_reports.aggregate(pipeline)
        try:
            info = info.next()
            last_week_count = info["count"]
        except StopIteration:
            print("Empty cursor!")
            return "didnt exist last week"

        return str(round((new_count/last_week_count-1)*100 , 2))+'%'

def decrement_day(date):
    return (convert_to_datetime(date)-datetime.timedelta(days=1)).isoformat()

def get_devices_per_day(date,status,device_type,collection=None):
    if collection:
        return collection.find({"timestamp":re.compile("^"+date[:10]) , "status":status, "type":device_type}).count()
    return health_reports.find({"timestamp":re.compile("^"+date[:10]) , "status":status, "type":device_type}).count()


def get_devices_last_thirty_days(date,status,device_type):#loop for previous func==>no need to test
    day_count = []
    for i in range(30):
        day_count.append({"date":date[:10], "count":get_devices_per_day(date,status,device_type)})
        date = decrement_day(date)
    return day_count

def fetch_available_types_and_statuses(collection=None):
    pipeline = [
                     { "$group": { "_id": "$status" } },
               ]
    statuses = []
    if collection:
        info = collection.aggregate(pipeline)
    else:
        info = health_reports.aggregate(pipeline)
    for i in info:
        statuses.append(i["_id"])

    pipeline = [
                     { "$group": { "_id": "$type" } },
               ]
    types = []
    if collection:
        info = collection.aggregate(pipeline)
    else:
        info = health_reports.aggregate(pipeline)
    for i in info:
        types.append(i["_id"])

    return {"types":types,"statuses":statuses}
