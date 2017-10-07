from part1 import Insertion
from part2 import Fetcher
from utils import (
    convert_to_datetime,
    datetime,
    get_last_week_isodate,
    decrement_day
)
import io
import unittest
import mongomock


class TestFunctions(unittest.TestCase):

    def fill_collection_and_init_fetcher(foo):
        def func(self):
            for item in self.Sample:
                self.collection.insert(item)
            self.fetcher = Fetcher(self.collection)
            foo(self)
        return func

    def setUp(self):
        self.line_to_insert = ["2017-05-12T23:37:30Z",
                               "c702be7d", "gateway", "offline"]
        self.collection = mongomock.MongoClient().db.collection
        self.Sample = [
            {"status": "online", "timestamp": "2017-05-01T00:17:50Z",
                "type": "sensor", "id": "a4a281ad"},
            {"status": "online", "timestamp": "2017-05-01T00:17:50Z",
                "type": "sensor", "id": "a4a281ad"},
            {"status": "online", "timestamp": "2017-05-01T00:17:50Z",
                "type": "sensor", "id": "a4a281ad"},
            {"status": "online", "timestamp": "2017-05-01T00:20:00Z",
                "type": "sensor", "id": "370ee49f"},
            {"status": "online", "timestamp": "2017-05-01T00:28:00Z",
                "type": "sensor", "id": "caedaaef"},
            {"status": "online", "timestamp": "2017-05-01T00:28:40Z",
                "type": "sensor", "id": "9c1060fc"},
            {"status": "online", "timestamp": "2017-05-01T00:32:50Z",
                "type": "gateway", "id": "9db3b7eb"},
            {"status": "offline", "timestamp": "2017-05-01T00:43:50Z",
                "type": "gateway", "id": "3831469f"},
            {"status": "offline", "timestamp": "2017-05-01T00:50:10Z",
                "type": "gateway", "id": "3831469f"},
            {"status": "online", "timestamp": "2017-05-01T00:50:20Z",
                "type": "sensor", "id": "6e711d12"},
            {"status": "online", "timestamp": "2017-05-01T00:50:30Z",
                "type": "gateway", "id": "89987171"},
            {"status": "online", "timestamp": "2017-05-01T00:52:00Z",
                "type": "sensor", "id": "370ee49f"}
        ]

    def test_convert_to_datetime(self):
        self.assertEqual(convert_to_datetime('2017-06-16T13:24:31.390259'),
                         datetime.datetime(2017, 6, 16, 13, 24, 31, 390259))

    def test_get_last_week_isodate(self):
        self.assertEqual(get_last_week_isodate(
            "2017-05-13T23:58:40Z"), "2017-05-06T23:58:40+00:00")

    def test_decrement_day(self):
        self.assertEqual(decrement_day("2017-05-13T23:58:40Z"),
                         "2017-05-12T23:58:40+00:00")

    def test_insert_line(self):
        inserter = Insertion(self.collection, io.BytesIO('testing'))
        returned_id = inserter.insert_line(self.line_to_insert)
        stored_obj = self.collection.find_one({'_id': returned_id})
        self.assertEqual(stored_obj["id"], "c702be7d")
        self.assertEqual(stored_obj["timestamp"], "2017-05-12T23:37:30Z")
        self.assertEqual(stored_obj["type"], "gateway")
        self.assertEqual(stored_obj["status"], "offline")

    @fill_collection_and_init_fetcher
    def test_fetch_top_from_day(self):
        self.assertEqual(self.fetcher.fetch_top_from_day(
            "2017-05-01T00:17:50Z")[0]["_id"], "a4a281ad")

    @fill_collection_and_init_fetcher
    def test_get_percentage_change_from_last_week(self):
        self.assertEqual(self.fetcher.get_percentage_change_from_last_week(
            "a4a281ad", "2017-05-08T23:58:40Z", 9), "200.0%")

    @fill_collection_and_init_fetcher
    def test_get_devices_per_day(self):
        self.assertEqual(self.fetcher.get_devices_per_day(
            "2017-05-01T01:06:30Z", "online", "gateway"), 2)

    @fill_collection_and_init_fetcher
    def test_fetch_available_types_and_statuses(self):
        self.assertEqual(
            self.fetcher.fetch_available_types_and_statuses(),
            {
                'statuses': ['offline', 'online', 'booha'],
                'types': ['gateway', 'sensor']
            }
        )


if __name__ == "__main__":
    unittest.main()
