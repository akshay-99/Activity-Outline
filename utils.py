import csv
import json

def readcsv(path):
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        line_count = 0
        cols = []
        for row in reader:
            if line_count == 0:
                cols = row
                line_count += 1
            data.append(dict(row))
            line_count += 1

    return data

def readjson(path):
    data = {}
    with open(path, 'r') as f:
        data = json.load(f)
    return data



