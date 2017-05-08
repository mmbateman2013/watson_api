import os
import requests
import datetime
import time
import sys
import os
import json
import decimal
from watson_developer_cloud import DiscoveryV1

#IBM Watson Variables
WATSON_ENV = '14c63c16-d8f1-4a51-8594-37955d774f78'
WATSON_UN  = '18435b75-abda-4cd4-accc-0784b829575a'
WATSON_PW  = 'cS08ZQb4WHp2'
WATSON_COLLECT = '6579a959-ed81-458a-bfeb-fdbeabe42862'

#Open Weather API variables
WEATHR_KEY    = '6f8891f3067e19f621126c13f291b368'
WEATHR_APPEND = ',us&appid='
WEATHR_URL = 'http://api.openweathermap.org/data/2.5/weather?q='

#Other Variables
cities = ['Houston','Dallas','Austin','Paris','London','Montreal','Toronto']

#declare Watson discovery object
discovery = DiscoveryV1(
  username=WATSON_UN,
  password=WATSON_PW,
  version="2016-12-01"
)

for city in cities:
  #call the Weather API and convert result to text
  print "Requesting weather for "+city
  obj = requests.get(WEATHR_URL+city+WEATHR_APPEND+WEATHR_KEY)
  contents = json.loads(obj.text)
  
  print "Transforming weather data for "+city
  #convert temps to fahrenheit
  contents["main"]["temp"]     = (contents["main"]["temp"]*9/5.0) - 459.67
  contents["main"]["temp_min"] = (contents["main"]["temp_min"]*9/5.0) - 459.67
  contents["main"]["temp_max"] = (contents["main"]["temp_max"]*9/5.0) - 459.67
  
  #convert UNIX timestamps to datetimes
  contents["sys"]["sunset"] = datetime.datetime.fromtimestamp(contents["sys"]["sunset"]).strftime('%Y-%m-%d %H:%M:%S')
  contents["sys"]["sunrise"] = datetime.datetime.fromtimestamp(contents["sys"]["sunrise"]).strftime('%Y-%m-%d %H:%M:%S')
  contents["dt"] = datetime.datetime.fromtimestamp(contents["dt"]).strftime('%Y-%m-%d %H:%M:%S')
  
  #rename "name" key to "city"
  #rename "dt" key to "date"
  #rename "temp" to "temperature"
  #rename "temp_min" to "low"
  #rename "temp_max" to "high"
  for key in contents.iterkeys():
    if key == "name":
      contents["city"] = contents["name"]
      del contents["name"]
    if key == "dt":
      contents["date"] = contents["dt"]
      del contents["dt"]
    if key == "main":
      for k2 in contents["main"].iterkeys():
        if k2 == "temp":
          contents["main"]["temperature"] = contents["main"]["temp"]
          del contents["main"]["temp"]
        elif k2 == "temp_min":
          contents["main"]["low"] = contents["main"]["temp_min"]
          del contents["main"]["temp_min"]
        elif k2 == "temp_max":
          contents["main"]["high"] = contents["main"]["temp_max"]
          del contents["main"]["temp_max"]
  
  print "Creating JSON file for "+city
  #create the JSON file
  fn = city+'.json'
  with open(fn,'w') as wf:
      json.dump(contents,wf)
      
  #call the Watson API and upload wf
  with open(fn,'r') as fileinfo:
      add_doc = discovery.add_document(WATSON_ENV, WATSON_COLLECT, file_info=fileinfo)
  print city+" uploaded successfully"
  
  #Delete the file
  os.remove(fn)
  print "Deleted file for "+city