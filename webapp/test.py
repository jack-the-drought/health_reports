from part1 import *
from part2 import *
import unittest
import mongomock


line_to_insert = ["2017-05-12T23:37:30Z","c702be7d","gateway","offline"]
Sample = [
{ "status" : "online", "timestamp" : "2017-05-01T00:17:50Z", "type" : "sensor", "id" : "a4a281ad" },
{ "status" : "online", "timestamp" : "2017-05-01T00:17:50Z", "type" : "sensor", "id" : "a4a281ad" },
{ "status" : "online", "timestamp" : "2017-05-01T00:17:50Z", "type" : "sensor", "id" : "a4a281ad" },
{ "status" : "online", "timestamp" : "2017-05-01T00:20:00Z", "type" : "sensor", "id" : "370ee49f" },
{ "status" : "online", "timestamp" : "2017-05-01T00:28:00Z", "type" : "sensor", "id" : "caedaaef" },
{ "status" : "online", "timestamp" : "2017-05-01T00:28:40Z", "type" : "sensor", "id" : "9c1060fc" },
{ "status" : "online", "timestamp" : "2017-05-01T00:32:50Z", "type" : "gateway", "id" : "9db3b7eb" },
{ "status" : "offline", "timestamp" : "2017-05-01T00:43:50Z", "type" : "gateway", "id" : "3831469f" },
{"status" : "offline", "timestamp" : "2017-05-01T00:50:10Z", "type" : "gateway", "id" : "3831469f" },
{ "status" : "online", "timestamp" : "2017-05-01T00:50:20Z", "type" : "sensor", "id" : "6e711d12" },
{  "status" : "online", "timestamp" : "2017-05-01T00:50:30Z", "type" : "gateway", "id" : "89987171" },
{ "status" : "online", "timestamp" : "2017-05-01T00:52:00Z", "type" : "sensor", "id" : "370ee49f" }
]

class TestFunctions(unittest.TestCase):
    def test_convert_to_datetime(self):
        self.assertEqual(convert_to_datetime('2017-06-16T13:24:31.390259'),datetime.datetime(2017, 6, 16, 13, 24, 31, 390259))
    def test_get_last_week_isodate(self):
        self.assertEqual(get_last_week_isodate("2017-05-13T23:58:40Z"),"2017-05-06T23:58:40+00:00")
    def test_decrement_day(self):
        self.assertEqual(decrement_day("2017-05-13T23:58:40Z"),"2017-05-12T23:58:40+00:00")
    def test_get_csv_lines(self):
        self.assertEqual(get_csv_lines("report.csv")[-1][0],"2017-05-13T23:58:40Z")
        self.assertEqual(get_csv_lines("report.csv")[-2][1],"361f2df5")
    def test_insert_to_db(self):
        collection = mongomock.MongoClient().db.collection
        returnedid = insert_to_db(line_to_insert,collection)
        stored_obj = collection.find_one({'_id' : returnedid})
        self.assertEqual(stored_obj["id"],"c702be7d")
    def test_fetch_top_from_day(self):
        collection = mongomock.MongoClient().db.collection
        for item in Sample:
            collection.insert(item)
        self.assertEqual(fetch_top_from_day("2017-05-01T00:17:50Z",collection)[0]["_id"],"a4a281ad")
    def test_get_percentage_change_from_last_week(self):
        collection = mongomock.MongoClient().db.collection
        for item in Sample:
            collection.insert(item)
        self.assertEqual(get_percentage_change_from_last_week("a4a281ad","2017-05-08T23:58:40Z",9,collection),"200.0%")
    def test_get_devices_per_day(self):
        collection = mongomock.MongoClient().db.collection
        for item in Sample:
            collection.insert(item)
        self.assertEqual(get_devices_per_day("2017-05-01T01:06:30Z","online","gateway",collection),2)
    def test_fetch_available_types_and_statuses(self):
        collection = mongomock.MongoClient().db.collection
        for item in Sample:
            collection.insert(item)
        self.assertEqual(fetch_available_types_and_statuses(collection),{'statuses': ['offline', 'online'], 'types': ['gateway', 'sensor']})




if __name__ == "__main__":
    unittest.main()
