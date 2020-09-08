#!/usr/bin/python3

import requests
import json
import sys
import time
import re
import os.path

# TODO: replace print statements with proper logging
# TODO: add standard argument handling

rooturl = 'https://www.domofond.ru'
basedir = '/home/amurashko/prealty/'

if len(sys.argv) > 1:
    baseurl = rooturl + sys.argv[1]
else:
    baseurl = rooturl + '/prodazha-kvartiry-belgorod-c310?PublicationTimeRange=OneDay'


def construct_whole_page_filename(basedir, pagenumber):
    return "{0}belgorod-{1}-{2}.html".format(basedir, time.strftime("%Y-%m-%d"), pagenumber)

def construct_json_filename(basedir, pagenumber):
    return "{0}belgorod-{1}-{2}.json".format(basedir, time.strftime("%Y-%m-%d"), pagenumber)

def store_content(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def get_content(filename):
    with open(filename) as f:
        return f.read()

def get_json(page_content):
    script_content = page_content.split("<script")[8]
    return script_content[27:-26]

def get_page_number(link):
    m = re.search("Page=(\d+)", link)
    return 1 if not m else int(m.group(1))

def get_base_url(json_content):
    page_object = json.loads(json_content)
    if 'nextLink' in page_object['metaInformationState']['current']:
        return rooturl + page_object['metaInformationState']['current']['nextLink']
    else:
        return None

if __name__ == "__main__":
    while True:
        page_number = get_page_number(baseurl)
        
        page_file = construct_whole_page_filename(basedir, page_number)
        json_file = construct_json_filename(basedir, page_number)
        page_was_uploaded = False

        if not os.path.isfile(page_file):
            print("uploading new page...")
            page = requests.get(baseurl, headers={'User-Agent': 'Mozilla'})
            page_content = page.text
            print("storing html file..." + page_file)
            store_content(page_file, page_content)
            page_was_uploaded = True
        else:
            page_content = get_content(page_file)

        json_content = get_json(page_content)

        if not os.path.isfile(json_file) or page_was_uploaded:
            print("storing json file..." + json_file)
            store_content(json_file, json_content)

        baseurl = get_base_url(json_content)
        if not baseurl:
            print("end of work...")
            break
