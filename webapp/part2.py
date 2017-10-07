from __future__ import division
import re
import itertools
from utils import get_last_week_isodate, decrement_day


class Fetcher:
    def __init__(self, collection):
        self.collection = collection

    def fetch_top_from_day(self, date):
        pipeline = [
            {"$match": {"timestamp": re.compile("^" + date[:10])}},
            {"$group": {"_id": "$id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        filtered = self.collection.aggregate(pipeline)

        top10 = itertools.islice(filtered, 10)
        l = []
        for i in top10:
            l.append(i)
        return l

    def get_percentage_change_from_last_week(self, deviceid, date, new_count):
        pipeline = [
            {"$match": {"timestamp": re.compile(
                "^" + get_last_week_isodate(date)[:10]), "id":deviceid}},
            {"$group": {"_id": "$id", "count": {"$sum": 1}}},
        ]

        filtered = self.collection.aggregate(pipeline)

        try:
            info = filtered.next()
            last_week_count = info["count"]
        except StopIteration:
            print("Empty cursor!")
            return "didnt exist last week"

        return str(round((new_count / last_week_count - 1) * 100, 2)) + '%'

    def get_devices_per_day(self, date, status, device_type):
        return self.collection.find(
            {"timestamp": re.compile("^" + date[:10]),
             "status": status, "type": device_type}
        ).count()

    # loop for previous func==>no need to test
    def get_devices_last_thirty_days(self, date, status, device_type):
        day_count = []
        for i in range(30):
            day_count.append(
                {"date": date[:10], "count": self.get_devices_per_day(
                    date, status, device_type)}
            )
            date = decrement_day(date)
        return day_count

    def fetch_available_types_and_statuses(self):
        pipeline = [
            {"$group": {"_id": "$status"}},
        ]
        statuses = []
        filtered = self.collection.aggregate(pipeline)
        for i in filtered:
            statuses.append(i["_id"])

        pipeline = [
            {"$group": {"_id": "$type"}},
        ]
        types = []
        filtered = self.collection.aggregate(pipeline)
        for i in filtered:
            types.append(i["_id"])
        return {"types": types, "statuses": statuses}
