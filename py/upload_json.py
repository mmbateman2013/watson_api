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
WATSON_COLLECT = 'b8ee0ff0-ef39-46be-bcdb-9c83372083c4'

#Open Weather API variables
WEATHR_KEY    = '6f8891f3067e19f621126c13f291b368'
WEATHR_APPEND = '&appid='
WEATHR_URL = 'http://api.openweathermap.org/data/2.5/weather?id='

#Other Variables
#Houston, TX ; Dallas,TX ; Austin,TX ; Paris,FR ; London,GB ; Montreal,CA ; Toronto,CA
cities = ['4699066','4684888','4671654','2988507','2643741','6077243','6167865'] 


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
  contents["dt"] = datetime.datetime.fromtimestamp(contents["dt"]).strftime('%B-%d-%Y %H:%M:%S')
  
  #convert country values to full names
  if contents["sys"]["country"] == "US":
    contents["sys"]["country"] = "United States"
  elif contents["sys"]["country"] == "GB":
    contents["sys"]["country"] = "Great Britain"
  elif contents["sys"]["country"] == "CA":
    contents["sys"]["country"] = "Canada"
  elif contents["sys"]["country"] == "FR":
    contents["sys"]["country"] = "France"
  
  #flatten the JSON
  contents["country"] = contents["sys"]["country"]
  contents["city"] = contents["name"]
  contents["date"] = contents["dt"]
  contents["temperature"] = contents["main"]["temp"]
  contents["low"] = contents["main"]["temp_min"]
  contents["high"] = contents["main"]["temp_max"]
  contents["forecast"] = contents["weather"][0]["main"]
  contents["description"] = contents["weather"][0]["description"]
  
  #remove the crap
  del contents["clouds"]
  del contents["visibility"]
  del contents["name"]
  del contents["sys"]
  del contents["weather"]
  del contents["coord"]
  del contents["base"]
  del contents["main"]
  del contents["dt"]
  del contents["id"]
  del contents["wind"]
  del contents["cod"]
  
  print "Creating JSON file for "+city
  
  #create the JSON file
  cityname = contents["city"]
  date = contents["date"]
  country = contents["country"]
  fn = country + '-' + cityname + '-' + date + '.json'
  with open(fn,'w') as wf:
      json.dump(contents,wf)
     
  #call the Watson API and upload wf
  with open(fn,'r') as fileinfo:
      add_doc = discovery.add_document(WATSON_ENV, WATSON_COLLECT, file_info=fileinfo)
  print city+" uploaded successfully"
  
  #Delete the file
  os.remove(fn)
  print "Deleted file for "+city
print "Finished processing files. :)"