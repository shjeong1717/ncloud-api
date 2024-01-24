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
cLog = cLogger.cLogger("/api/event/deleteRuleGroup")
logger = cLog.set_logger()

#set variables
now_dt = con._NOW_DT
now_ts = str(con._NOW_TS)
filename = con._YAML_DIR +"/event.yaml"
method = "POST"
dataType = "deleteData"


def send_api(param):
  path = "/cw_fea/real/cw/api/rule/group/ruleGrp/del"
  
  # request body
  body = {}
  body["items"] = param
  
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
    print("이벤트 룰 삭제 완료")
  else:
    print("이벤트 룰 삭제 실패 [ %s ]" % rsltData['data']['msg'])
# end def

# main
def main():
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    fnc.getSystemSchemaList()
  # end if
  
  x = input("\n\nprodKey를 입력하세요.\n이벤트 룰 정보를 조회합니다 [input 'prodKey'] : ")
  if x != '':
    data = {
      'prodKey': x,
      'search': '',
      'pageSize': 100,
      'pageNum': 1
    }
    fnc.getRuleGroupIdList(data)
  # end if
  
  x = input("\n\n이벤트 룰을 삭제하시겠습니까??\n삭제하려면 yaml파일을 작성하고 [ok] 를 누르세요 : ")
  if x == 'ok':
    with open(filename) as yamlfile:
      yamldata = yaml.full_load(yamlfile)
    #end with
    
    list = yamldata[dataType]
    
    for data in list:
      send_api(data)
    # end for
  # end if
# end def

if __name__ == "__main__":
  main()
# end if