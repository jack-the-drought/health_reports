import csv
from utils import get_collection_using_env

class Insertion:
    def __init__(self, collection, input_file_descriptor):
        self.collection = collection
        self.input_file_descriptor = input_file_descriptor

    def insert_all(self):

        try:
            reader = csv.reader(self.input_file_descriptor)
        except:
            return "could not open file for reading"

        for line in reader:
            self.insert_line(line)

    def insert_line(self, line):
        item = {}
        item["timestamp"] = line[0]
        item["id"] = line[1]
        item["type"] = line[2]
        item["status"] = line[3]
        return self.collection.insert(item)


if __name__ == "__main__":

    try:
        f = open("report.csv", "r")
    except Exception as e:
        print e

    part1 = Insertion(get_collection_using_env(), f)
    part1.insert_all()
