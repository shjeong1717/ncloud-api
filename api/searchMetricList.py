#import system library
import sys
import requests
import json
from datetime import datetime

# import user library
sys.path.append('/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api')
from _lib import config as con
from _lib import cLogger
from _lib import function as fnc

# set logger
cLog = cLogger.cLogger("/api/searchMetricList")
logger = cLog.set_logger()

#set variables
now_dt = con._NOW_DT
now_ts = str(con._NOW_TS)

# logger.info("now_dt == "+ str(now_dt))
# logger.info("now_ts == "+ str(now_ts))


def send_api(path, method):
  API_HOST = "https://cw.apigw.ntruss.com"
  url = API_HOST + path
  sign = fnc.make_signature(path, now_ts, method)
  
  headers = {}
  headers["Content-Type"] = "application/json"
  headers["x-ncp-apigw-signature-v2"] = sign
  headers["x-ncp-apigw-timestamp"] = now_ts
  headers["x-ncp-iam-access-key"] = con._ACCESS_KEY
  
  body = {}
  body["prodKey"] = "460438474722512896"
  body["query"] = ""    # Search in metrics
  body["dimValues"] = {"name": "type", "value": "svr"}   # metric type
  # body["dimValues"] = {}
  
  try:
    if method == 'GET':
      response = requests.get(url, headers=headers)
    elif method == 'POST':
      response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
    elif method == 'PUT':
      response = requests.put(url, headers=headers, data = json.dumps(body, ensure_ascii=False, indent="\t"))
    elif method == 'DELETE':
      response = requests.delete(url, headers=headers, data = json.dumps(body, ensure_ascii=False, indent="\t"))
    # end if
    
    # print("response status == %s" % response.status_code)
    # print("response text == %s" % response.text)
    
    rsltData = json.loads(response.text)
    objList = []
    for data in rsltData['metrics']:
      objData = {}
      objData['metric'] = data['metric']
      objData['desc'] = data['desc']
      objData['dimensions'] = data['dimensions']
      objData['calculation'] = data['options']['Min1']
      objList.append(objData)
      # print('==========================================')
      # print("metric == %s" % str(data['metric']))
      # print("desc == %s" % str(data['desc']))
      # print("dimensions == %s" % str(data['dimensions']))
      # print("options == %s" % str(data['options']['Min1']))
    # end for
    
    jsonData = json.dumps(objList)
    print(jsonData)
  except Exception as ex:
    print("exception [%s]" % ex)
  # end try
# end def

# 호출 예시
send_api("/cw_fea/real/cw/api/rule/group/metric/search", "POST")