#!/usr/bin/python3
import requests
import json
import sys

rooturl = 'https://www.domofond.ru'

if len(sys.argv) > 1:
    baseurl = rooturl + sys.argv[1]
else:
    baseurl = rooturl + '/prodazha-kvartiry-belgorod-c310?PublicationTimeRange=OneDay'

if __name__ == "__main__":
    while True:
        print("requesting url...", baseurl)
        page = requests.get(baseurl, headers={'User-Agent': 'Mozilla'})
        ss = page.text.split("<script")[8]
        js = ss[27:-26]
        obj = json.loads(js)
        if 'nextLink' in obj['metaInformationState']['current']:
            baseurl = rooturl + obj['metaInformationState']['current']['nextLink']
        else:
            print('last page')
            break
