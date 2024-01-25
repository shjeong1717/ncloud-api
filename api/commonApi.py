#import system library
import os, sys
import json
from datetime import datetime

# import user library
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as con
import function as fnc


def send_api(param):
  API_HOST = "https://cw.apigw.ntruss.com"
  url = API_HOST + param['path']
  
  objHeader = {}
  objHeader['path'] = param['path']
  objHeader['method'] = param['method']
  headers = fnc.make_header(objHeader)
  
  objApi = {}
  objApi['url'] = url
  objApi['headers'] = headers
  objApi['body'] = param['requestBody']
  objApi['method'] = param['method']
  result = fnc.call_api(objApi)
  
  return result
# end def


# 스키마 키 목록
def getSystemSchemaKeyList():
  arg = {}
  arg['method'] = 'GET'
  arg['path'] = '/cw_fea/real/cw/api/schema/system/list'
  arg['requestBody'] = {}
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  
  print("================= System Schema Info Start =================")
  for data in rsltData:
    print(data["prodName"] +" : "+ data["cw_key"])
  # end for
  print("================= System Schema Info End =================")
# end def


# 감시대상 그룹 아이디 목록
def getMonitorGrpKey(param):
  arg = {}
  arg['method'] = 'GET'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/monitor/'+ param['prodKey']
  arg['requestBody'] = {}
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  print("================= Monitor Group Key Start =================")
  for data in rsltData:
    print(data['groupName'] +" : "+ data['id'])
  #end for
  print("================= Monitor Group Key End =================")
# end def


# 메트릭 그룹 아이디 목록
def getMetricGrpKey(param):
  arg = {}
  arg['method'] = 'GET'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/metrics/query/'+ param['prodKey']
  arg['requestBody'] = {}
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']['metricsGroups']
  print("================= Metric Group Key Start =================")
  for data in rsltData:
    print(data['groupName'] +" : "+ data['id'])
  #end for
  print("================= Metric Group Key End =================")
# end def


# 알림대상자 정보 조회
def getNotiInfo():
  arg = {}
  arg['method'] = 'GET'
  arg['path'] = '/cw_fea/real/cw/api/rule/notify/groups'
  arg['requestBody'] = {}
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  print("================= Notification Info Start =================")
  for data in rsltData:
    print(data)
  # end for
  print("================= Notification Info End =================")
#end def


# 이벤트 룰 그룹 아이디 조회
def getRuleGroupIdList(param):
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/ruleGrp/query'
  arg['requestBody'] = {
    'prodKey': param['prodKey'],
    'search': '',
    'pageSize': 100,
    'pageNum': 1
  }
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  print("================= Rule Group ID Info Start =================")
  # finData = []
  for data in rsltData['ruleGroups']:
    # objData = {}
    # objData['prodKey'] = data['prodKey']
    # objData['groupName'] = data['groupName']
    # objData['ruleGroupId'] = data['id']
    # finData.append(objData)
    print(data)
  # end for
  # print(json.dumps(finData, indent=2))
  print("================= Rule Group ID Info End =================")
# end def


# 이벤트 룰 그룹 조회
def getRuleGroupList(param):
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/ruleGrp/query'
  arg['requestBody'] = {
    'prodKey': param['prodKey'],
    'search': '',
    'pageSize': 100,
    'pageNum': 1
  }
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  print("================= Rule Group Info Start =================")
  finData = []
  for data in rsltData['ruleGroups']:
    objData = {}
    objData['prodKey'] = data['prodKey']
    objData['groupName'] = data['groupName']
    objData['ruleGroupId'] = data['id']
    
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
      if 'groupName' in metric:
        objMetric['groupName'] = metric['groupName']
      # end if
      if 'groupDesc' in metric:
        objMetric['groupDesc'] = metric['groupDesc']
      #end if
      
      objMetric['metrics'] = []
      for metricItem in metric['metrics']:
        objItem = {}
        objItem['metric'] = metricItem['metric']
        objItem['metricGroupItemId'] = metricItem['metricGroupItemId']
        objMetric['metrics'].append(objItem)
      #end for
      objData['metricsGroups'].append(objMetric)
    #end for
    finData.append(objData)
    print(objData)
  # end for
  print("================= Rule Group Info End =================")
  # print(json.dumps(finData, indent=2))
# end def