import os
import requests
import datetime
import time
import sys
import os
import json
import decimal
import sqlobject
from watson_developer_cloud import DiscoveryV1

#IBM Watson Variables
WATSON_ENV = '14c63c16-d8f1-4a51-8594-37955d774f78'
WATSON_UN  = '18435b75-abda-4cd4-accc-0784b829575a'
WATSON_PW  = 'cS08ZQb4WHp2'
WATSON_COLLECT = '6579a959-ed81-458a-bfeb-fdbeabe42862'

#declare Watson discovery object
discovery = DiscoveryV1(
  username=WATSON_UN,
  password=WATSON_PW,
  version="2016-12-01"
)

