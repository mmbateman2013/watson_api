import os
import requests
import datetime
import time
import sys
import os
import json
from watson_developer_cloud import DiscoveryV1

WATSON_ENV = '14c63c16-d8f1-4a51-8594-37955d774f78'
WATSON_UN  = '18435b75-abda-4cd4-accc-0784b829575a'
WATSON_PW  = 'cS08ZQb4WHp2'
WATSON_COLLECT = 'a55d4b02-c285-4429-a614-428ba8a370ea'
WEATHR_KEY    = '6f8891f3067e19f621126c13f291b368'
WEATHR_APPEND = ',us&appid='
WEATHR_URL = 'http://api.openweathermap.org/data/2.5/weather?q='

discovery = DiscoveryV1(
  username=WATSON_UN,
  password=WATSON_PW,
  version="2016-12-01"
)


    
#Variables
city = 'Austin'

#call the Weather API and convert result to text
obj = requests.get(WEATHR_URL+city+WEATHR_APPEND+WEATHR_KEY)
contents = obj.text
fn = city+'.json'

#create the JSON file
with open(fn,'w') as wf:
    wf.write(contents)
    
#call the Watson API and upload wf
with open(fn,'r') as fileinfo:
    add_doc = discovery.add_document(WATSON_ENV, WATSON_COLLECT, file_info=fileinfo)
    print(json.dumps(add_doc, indent=2))

#Delete the file
os.remove(fn)