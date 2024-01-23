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
cLog = cLogger.cLogger("/api/template/updateMonitorGrp")
logger = cLog.set_logger()

#set variables
now_dt = con._NOW_DT
now_ts = str(con._NOW_TS)
filename = con._YAML_DIR +"monitor.yaml"
method = "PUT"
dataType = "updateData"


def send_api(param):
  path = "/cw_fea/real/cw/api/rule/group/monitor"
  
  # request body
  body = {}
  body["prodKey"] = param['prodKey']
  body["id"] = param['id']
  body["groupName"] = param['groupName']
  body["groupDesc"] = param['groupDesc']
  body["monitorGroupItemList"] = param['monitorGroupItemList']
  
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
  
  print("result data == %s" % result)
  rsltData = json.loads(result)
  
  if rsltData['status'] == 200:
    print("감시대상그룹 수정 완료")
  else:
    print("감시대상그룹 수정 실패 [ %s ]" % rsltData['data']['msg'])
# end def

# main
def main():
  with open(filename) as yamlfile:
    yamldata = yaml.full_load(yamlfile)
  #end with
  
  list = yamldata[dataType]
  
  for data in list:
    send_api(data)
  # end for
# end def

if __name__ == "__main__":
  main()
# end if