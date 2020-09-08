#!/usr/bin/python3
import json

#jsobj["itemsState"]["items"][0]["priceValue"]
#/home/amurashko/prealty/belgorod-2020-09-08-1.json

filename = "/home/amurashko/prealty/belgorod-2020-09-08-1.json"
with open(filename) as f:
    json_content = f.read()
    obj = json.loads(json_content)
    for item in obj["itemsState"]["items"]:
        id = item["id"]
        price = item["priceValue"]
        published = item["publishDate"]
        updated = item["sourceUpdateTime"]
        title = item["title"]
        floor = item["floorInt"]
        details = item["details"]
        description = item["description"]
        url = item["itemUrl"]
        rooms = item["roomsOrdinal"]
        isfreeplan = item["isFreePlan"]
        location = item["location"]
        address = item["address"]
        agency_id = item["agencyId"]
        agency_name = item["agencyName"]
        source_started = item["sourceStartTime"]
        source_finished = item["sourceFinishTime"]
        sale_type = item["apartmentSaleType"]
        print("{:40}\t{}\t{}\t{}".format(title, price, published, updated))
