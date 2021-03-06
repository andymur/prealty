#!/usr/bin/python3

import argparse
import requests
import json
import sys
import time
import re
import os.path
import logging

# TODO: testing & mocking

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

argparser = argparse.ArgumentParser()
argparser.add_argument("-b", "--basedir", type=str, required=True)
argparser.add_argument("-u", "--urlending", type=str, required=False)

args = argparser.parse_args()
urlending = args.urlending

rooturl = 'https://www.domofond.ru'
basedir = args.basedir

if urlending:
    baseurl = rooturl + sys.argv[1]
else:
    baseurl = rooturl + '/prodazha-kvartiry-belgorod-c310?PublicationTimeRange=OneDay'

logger = logging.getLogger("template" if __name__ == "__main__" else __name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == "__main__":
    while True:
        page_number = get_page_number(baseurl)
        
        page_file = construct_whole_page_filename(basedir, page_number)
        json_file = construct_json_filename(basedir, page_number)
        page_was_uploaded = False

        if not os.path.isfile(page_file):
            logger.info("uploading new page from {}".format(baseurl))
            page = requests.get(baseurl, headers={'User-Agent': 'Mozilla'})
            page_content = page.text
            logger.info("storing html file {}".format(page_file))
            
            store_content(page_file, page_content)
            page_was_uploaded = True
        else:
            page_content = get_content(page_file)

        json_content = get_json(page_content)

        if not os.path.isfile(json_file) or page_was_uploaded:
            logger.info("storing json file {}".format(json_file))
            store_content(json_file, json_content)

        baseurl = get_base_url(json_content)
        if not baseurl:
            logger.info("End of work...")
            break
