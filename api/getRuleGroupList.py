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
cLog = cLogger.cLogger("/api/getRuleGroupList")
logger = cLog.set_logger()

#set variables
now_dt = con._NOW_DT
filename = con._YAML_DIR +"event.yaml"
method = "POST"
dataType = "selectData"


def send_api(param):
  path = "/cw_fea/real/cw/api/rule/group/ruleGrp/query"
  body = {}
  body['prodKey'] = param['prodKey']
  body['pageSize'] = param['pageSize']
  body['pageNum'] = param['pageNum']
  body['search'] = param['search']
  
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
def main(param):
  print(param)
  if 'prodKey' in param:
    param['pageNum'] = input("\n\n페이지 번호를 입력하세요.\n종료하려면 비어있는 채로 엔터키를 입력하세요 [input number or empty] : ")
  else:
    x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
    if x == 'ok':
      fnc.getSystemSchemaList()
    # end if
    
    param['prodKey'] = input("\n\nprodKey를 입력하세요.\n'*'를 입력하면 전체 입니다. [input 'prodKey'] : ")
    if param['prodKey'] != '': 
      param['search'] = input("\n\n검색어를 입력하세요. [input text] : ")
      param['pageSize'] = input("\n\n페이지 사이즈를 입력하세요. [input number] : ")
      param['pageNum'] = input("\n\n페이지 번호를 입력하세요.\n종료하려면 비어있는 채로 엔터키를 입력하세요 [input number or empty] : ")
    # end if
  # end if
  
  if param['pageNum'] == '':
    param['pageNum'] = 'exit'
  # end if
  
  objParam = {
    "prodKey": param['prodKey'],
    "search": param['search'],
    "pageSize": param['pageSize'],
    "pageNum": param['pageNum']
  }
  
  if objParam['pageNum'] != 'exit':
    if objParam['prodKey'] != '':
      result = send_api(objParam)
      print("result == %s" % result)
      
      rsltData = json.loads(result)
      listData = []
      for data in rsltData['data']['ruleGroups']:
        objData = {}
        objData['prodKey'] = data['prodKey']
        objData['id'] = data['id']
        if 'groupName' in data:
            objData['groupName'] = data['groupName']
        if 'groupDesc' in data:
          objData['groupDesc'] = data['groupDesc']
        #end if
        
        objData['monitorGroups'] = []
        for monitor in data['monitorGroups']:
          objMonitor = {}
          objMonitor['id'] = monitor['id']
          objMonitor['monitorGroupItemList'] = monitor['monitorGroupItemList']
          if 'groupName' in monitor:
            objMonitor['groupName'] = monitor['groupName']
          if 'groupDesc' in monitor:
            objMonitor['groupDesc'] = monitor['groupDesc']
          #end if
          objData['monitorGroups'].append(objMonitor)
        #end for
        
        objData['metricsGroups'] = []
        for metric in data['metricsGroups']:
          objMetric = {}
          objMetric['id'] = metric['id']
          objMetric['metrics'] = metric['metrics']
          if 'groupName' in metric:
            objMetric['groupName'] = metric['groupName']
          if 'groupDesc' in metric:
            objMetric['groupDesc'] = metric['groupDesc']
          #end if
          objData['metricsGroups'].append(objMetric)
        #end for
        listData.append(objData)
      # end for
      jsonData = json.dumps(listData, indent=2)
      print(jsonData)
      
      main(objParam)
    # end if
  # end if
# end def

if __name__ == "__main__":
  main({})
# end if