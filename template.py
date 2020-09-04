import requests
import json

page = requests.get('https://www.domofond.ru/prodazha-kvartiry-belgorod-c310?Rooms=Two%2CThree&PublicationTimeRange=OneDay', headers={'User-Agent': 'Mozilla'})
ss = page.text.split("<script")[8]
js = ss[27:-26]
obj = json.loads(js)
print(obj['metaInformationState']['current']['nextLink'])
