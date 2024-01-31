#import system library
import os, sys
import json
import clipboard
from datetime import datetime

# import user library
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as con
import function as fnc


def send_api(param):
  API_HOST = "https://cw.apigw.ntruss.com"
  if 'apiHost' in param:
    API_HOST = param['apiHost']
  # end if
  
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
  listData = []
  for data in rsltData:
    objData = {data['prodName'] : data['cw_key']}
    listData.append(objData)
  # end for
  finData = json.dumps(listData, indent=2, ensure_ascii=False)
  clipboard.copy(finData)
  print(finData)
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
  listData = []
  for data in rsltData:
    objData = {data['groupName'] : data['id']}
    listData.append(objData)
  #end for
  finData = json.dumps(listData, indent=2, ensure_ascii=False)
  clipboard.copy(finData)
  print(finData)
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
  listData = []
  for data in rsltData:
    objData = {data['groupName'] : data['id']}
    listData.append(objData)
  #end for
  finData = json.dumps(listData, indent=2, ensure_ascii=False)
  clipboard.copy(finData)
  print(finData)
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
  listData = []
  for data in rsltData:
    listData.append(data)
  # end for
  finData = json.dumps(listData, indent=2, ensure_ascii=False)
  clipboard.copy(finData)
  print(finData)
  print("================= Notification Info End =================")
#end def


# 이벤트 룰 그룹 아이디 조회
def getRuleGroupIdList(param):
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/ruleGrp/query'
  arg['requestBody'] = {
    'prodKey': param['prodKey'],
    'search': param['search'],
    'pageSize': param['pageSize'],
    'pageNum': param['pageNum']
  }
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  print("================= Rule Group ID Info Start =================")
  listData = []
  for data in rsltData['ruleGroups']:
    objData = {}
    objData['prodKey'] = data['prodKey']
    objData['groupName'] = data['groupName']
    objData['ruleGroupId'] = data['id']
    listData.append(objData)
  # end for
  finData = json.dumps(listData, indent=2, ensure_ascii=False)
  clipboard.copy(finData)
  print(finData)
  print("================= Rule Group ID Info End =================")
# end def


# 이벤트 룰 그룹 조회
def getRuleGroupList(param):
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/ruleGrp/query'
  arg['requestBody'] = {
    'prodKey': param['prodKey'],
    'search': param['search'],
    'pageSize': param['pageSize'],
    'pageNum': param['pageNum']
  }
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  print("================= Rule Group Info Start =================")
  listData = []
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
    listData.append(objData)
    # print(objData)
  # end for
  finData = json.dumps(listData, indent=2, ensure_ascii=False)
  clipboard.copy(finData)
  print(finData)
  print("================= Rule Group Info End =================")
# end def


# 메트릭 디멘션 조회
def getMetricDimension(param):
  # request body
  body = {}
  body["prodKey"] = param['prodKey']
  
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/metric/search'
  arg['requestBody'] = body
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  
  listData = []
  for metric in rsltData['metrics']:
    for dim in metric['dimensions']:
      if dim['dim'] == 'type':
        listData.append(dim['val'])
      # end if
    # end for
  # end for
  setData = set(listData)
  listData = list(setData)
  listData.sort()
  finData = json.dumps(listData, indent=2, ensure_ascii=False)
  
  return finData
# end def


# 메트릭 리소스 조회
def getMetricList(param):
  # request body
  body = {}
  body["prodKey"] = param['prodKey']
  body["query"] = param['query']    # Search in metrics
  body["dimValues"] = {
    "name": "type",
    "value": param['dim']
  }
  
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/metric/search'
  arg['requestBody'] = body
  
  result = send_api(arg)
  
  return result
# end def


# get server instance
def getResourceList(param):
  # request body
  body = {}
  body["pageIndex"] = param['pageIndex']
  body["pageSize"] = param['pageSize']
  body["productName"] = param['productName']
  body["resourceType"] = param['resourceType']
  
  arg = {}
  arg['apiHost'] = 'https://resourcemanager.apigw.ntruss.com'
  arg['method'] = 'POST'
  arg['path'] = '/api/v1/resources'
  arg['requestBody'] = body
  
  result = send_api(arg)
  rsltData = json.loads(result)['data']
  
  return rsltData
# end def