import csv
from pymongo import MongoClient

Development = True
client = MongoClient(host="mongo")

if Development == True:
    db = client.kiwitest_dev
else:
    db = client.kiwitest_prod

health_reports = db.health_reports

#change input to csv data
def get_csv_lines(filename):

    try:
        f = open(filename,"r")
    except Exception as e:
        print e

    try:
        reader = csv.reader(f)
        lines = []
        for line in reader:#make the insert happen here
            lines.append(line)
    except:
        print "error reading csv file"
    finally:
        f.close()
    return lines

def insert_to_db(line,collection=None):
    item = {}
    item["timestamp"] = line[0]
    item["id"] = line[1]
    item["type"] = line[2]
    item["status"] = line[3]
    if collection:
        return collection.insert(item)
    else:
        return health_reports.insert(item)


if __name__=="__main__":
    for item in get_csv_lines("report.csv"):
        insert_to_db(item)
