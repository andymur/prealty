#!/usr/bin/python3

import argparse
import json
import csv
import os
import os.path

def append_data(basedir, jsonfilename, csvfilename):
    jsonfile = os.path.sep.join((basedir, jsonfilename))
    csvfile = os.path.sep.join((basedir, csvfilename))
    with open(jsonfile) as fjson, open(csvfile, "a") as fcsv:
        fieldnames = ["id", "price", "published", "updated", "title", "floor", "details", "description", 
                      "url", "rooms", "isfreeplan", "location", "address", "agency_id", "agency_name", 
                      "source_started", "source_finished", "sale_type"]
        csvwriter = csv.DictWriter(fcsv, fieldnames = fieldnames)
        json_content = fjson.read()
        obj = json.loads(json_content)
        for item in obj["itemsState"]["items"]:
            ditem = {}
            ditem["id"] = item["id"]
            ditem["price"] = item["priceValue"]
            ditem["published"] = item["publishDate"]
            ditem["updated"] = item["sourceUpdateTime"]
            ditem["title"] = item["title"]
            ditem["floor"] = item["floorInt"]
            ditem["details"] = item["details"]
            ditem["description"] = item["description"]
            ditem["url"] = item["itemUrl"]
            ditem["rooms"] = item.get("roomsOrdinal", None)
            ditem["isfreeplan"] = item["isFreePlan"]
            ditem["location"] = item.get("location", None)
            ditem["address"] = item["address"]
            ditem["agency_id"] = item["agencyId"]
            ditem["agency_name"] = item["agencyName"]
            ditem["source_started"] = item["sourceStartTime"]
            ditem["source_finished"] = item["sourceFinishTime"]
            ditem["sale_type"] = item["apartmentSaleType"]
            csvwriter.writerow(ditem)


csvfilename = "prealty.csv"

argparser = argparse.ArgumentParser()
argparser.add_argument("-b", "--basedir", type=str, required=True)

args = argparser.parse_args()
basedir = args.basedir

for jsonfilename in list(filter(lambda x: x.endswith("json"), os.listdir(basedir))):
    append_data(basedir, jsonfilename, csvfilename)
    os.rename(os.path.sep.join((basedir, jsonfilename)), os.path.sep.join((basedir, jsonfilename + "_")))
