#import system library
import sys
import requests
import json
import yaml
from datetime import datetime

# import user library
sys.path.append('/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api')
from _lib import config as con
from _lib import cLogger
from _lib import function as fnc

# set logger
cLog = cLogger.cLogger("/api/getAllMonitorGrp")
logger = cLog.set_logger()

#set variables
now_dt = con._NOW_DT
now_ts = str(con._NOW_TS)
filename = con._YAML_DIR +"/monitor.yaml"
method = "GET"
dataType = "selectData"

def send_api(param):
  path = "/cw_fea/real/cw/api/rule/group/monitor/"+ param['prodKey']
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
  with open(filename) as yamlfile:
    yamldata = yaml.full_load(yamlfile)
  #end with
  
  list = yamldata[dataType]
  
  for data in list:
    result = send_api(data)
    print("result data == %s" % result)
  # end for
# end def

if __name__ == "__main__":
  main()
# end if