#import system library
import sys
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
filename = ""
method = "GET"

def send_api():
  path = "/cw_fea/real/cw/api/schema/system/list"
  body = {}
  
  API_HOST = "https://cw.apigw.ntruss.com"
  url = API_HOST + path
  
  objHeader = {}
  objHeader['path'] = path
  objHeader['method'] = method
  headers = fnc.make_header(objHeader)
  
  objApi = {}
  objApi['url'] = url
  objApi['headers'] = headers
  objApi['body'] = body
  objApi['method'] = method
  result = fnc.call_api(objApi)
  
  return result
# end def

# main
def main():
  result = send_api()
  
  rsltData = json.loads(result)
  
  objList = []
  for data in rsltData['data']:
    objData = {}
    objData[data['prodName']] = data['cw_key']
    objList.append(objData)
    # print('==========================================')
    # print(data["prodName"] +" : "+ data["cw_key"])
  # end for
  
  jsonData = json.dumps(objList, indent=2)
  print("result == %s" % jsonData)
# end def

if __name__ == "__main__":
  main()
# end if