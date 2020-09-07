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


def construct_whole_page_filename(pagenumber):
    return "belgorod-{0}-{1}.html".format(time.strftime("%Y-%m-%d"), pagenumber)

def construct_json_filename(pagenumber):
    return "belgorod-{0}-{1}.json".format(time.strftime("%Y-%m-%d"), pagenumber)

def store_content(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def get_page_number(link):
    m = re.search("Page=(\d+)", link)
    return 1 if not m else int(m.group(1))

if __name__ == "__main__":
    while True:
        print("requesting url...", baseurl)
        page_number = get_page_number(baseurl)
	#TODO: no need to make requests if file exists
        page = requests.get(baseurl, headers={'User-Agent': 'Mozilla'})
        
        page_file = basedir + construct_whole_page_filename(page_number)
        json_file = basedir + construct_json_filename(page_number)
        print("page file: " + page_file)

        if not os.path.isfile(page_file):
            store_content(page_file, page.text)
        
        script_content = page.text.split("<script")[8]
        json_content = script_content[27:-26]

        if not os.path.isfile(json_file):
            store_content(json_file, json_content)

        page_object = json.loads(json_content)
        if 'nextLink' in page_object['metaInformationState']['current']:
            baseurl = rooturl + page_object['metaInformationState']['current']['nextLink']
        else:
            print('last page')
            break
