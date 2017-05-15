import os
import requests
import datetime
import time
import sys
import os
import json
import decimal
from watson_developer_cloud import DiscoveryV1
from bs4 import BeautifulSoup, Comment

#AL Websi
AL_URL_STRING = 'http://airliquidehandbook.bitnamiapp.com/tiki/tiki-index.php?page=ASU+Handbook+Ch'
AL_NUM = "00"

#IBM Watson Variables
WATSON_ENV = '14c63c16-d8f1-4a51-8594-37955d774f78'
WATSON_UN  = '18435b75-abda-4cd4-accc-0784b829575a'
WATSON_PW  = 'cS08ZQb4WHp2'
WATSON_COLLECT = 'a9355c7d-301a-4adc-a8e1-bbfb6f955be0'

#declare Watson discovery object
discovery = DiscoveryV1(
  username=WATSON_UN,
  password=WATSON_PW,
  version="2016-12-01"
)

#loop through Chapters 00 - 33 of the ASU Handbook
for i in range(0,34):
    if i < 10:
        AL_NUM = '0'+str(i)
    else:
        AL_NUM = str(i)
    
    print "Pulling chapter "+AL_NUM
    
    #open the URL
    request = requests.get(AL_URL_STRING+AL_NUM)
    data = request.text
    soup = BeautifulSoup(data,"html5lib")
    
    #remove script, style, meta, noscript, link and filler tags
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    [s.extract() for s in soup('meta')]
    [s.extract() for s in soup('noscript')]
    [s.extract() for s in soup('link')]
    [s.extract() for s in soup('div',id='page-header')]
    
    #remove comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    
    #write the file
    print "Creating html file for chapter "+AL_NUM
    html = soup.prettify("utf-8")
    fn = 'ASU_HANDBOOK_CH'+ AL_NUM + '.html'
    with open(fn,'w') as wf:
        wf.write(str(html))
        
    print "Finished creating files :)"

    #call the Watson API and upload wf
    with open(fn,'r') as fileinfo:
        add_doc = discovery.add_document(WATSON_ENV, WATSON_COLLECT, file_info=fileinfo)
    print "Chapter "+AL_NUM+" uploaded successfully"
  
    #Delete the file
    os.remove(fn)
    print "Deleted file for chapter "+AL_NUM