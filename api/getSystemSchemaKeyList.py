#import system library
import sys
import requests
import json
from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api

# import user library
sys.path.insert(0, '/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api')
from _lib import config as con
from _lib import cMysql
from _lib import cLogger
from _lib import function as fnc

# set logger
cLog = cLogger.cLogger("/api/getSystemSchemaKeyList")
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
  headers["x-ncp-apigw-signature-v2"] = sign
  headers["x-ncp-apigw-timestamp"] = now_ts
  headers["x-ncp-iam-access-key"] = con._ACCESS_KEY
  
  body = {}
  
  try:
    if method == 'GET':
      response = requests.get(url, headers=headers)
    elif method == 'POST':
      response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
    # end if
    
    # print("response status == %s" % response.status_code)
    # print("response text == %s" % response.text)
    
    objData = json.loads(response.text)
    
    for data in objData:
      print(data["prodName"] +" : "+ data["cw_key"])
    # end for
  except Exception as ex:
    print("exception [%s]" % ex)
  # end try
# end def

# 호출 예시
send_api("/cw_fea/real/cw/api/schema/system/list", "GET")