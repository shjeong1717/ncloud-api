#import system library
import os, sys
import json
import yaml

# import user library
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as con
import function as fnc

from api import commonApi


#set variables
filename = con._YAML_DIR +"/event.yaml"


# api 호출 실행
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
  
  print("result data == %s" % result)
  rsltData = json.loads(result)
  
  return rsltData
# end def


# eventCreate
def eventCreate(param):
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    commonApi.getSystemSchemaKeyList()
  # end if
  
  x = input("\n\nprodKey를 입력하세요.\n감시대상, 메트릭 그룹 키, 알림대상자 정보를 조회합니다 [input 'prodKey'] : ")
  if x != '':
    arg = {
      'prodKey': x
    }
    commonApi.getMonitorGrpKey(arg)
    commonApi.getMetricGrpKey(arg)
    commonApi.getNotiInfo()
  # end if
  
  x = input("\n\n이벤트 룰을 생성하시겠습니까??\n생성하려면 yaml파일을 작성하고 [ok] 를 누르세요 : ")
  if x == 'ok':
    with open(filename) as yamlfile:
      yamldata = yaml.full_load(yamlfile)
    #end with
    
    list = yamldata[param['dataType']]
    
    for data in list:
      arg['method'] = 'POST'
      arg['path'] = '/cw_fea/real/cw/api/rule/group/ruleGrp'
      
      # request body
      body = {}
      body["prodKey"] = data['prodKey']
      body["groupName"] = data['groupName']
      body["groupDesc"] = data['groupDesc']
      body["monitorGroupKey"] = data['monitorGroupKey']
      body["metricsGroupKey"] = data['metricsGroupKey']
      body['recipientNotifications'] = data['recipientNotifications']
      body['personalNotificationRecipients'] = data['personalNotificationRecipients']
      arg['requestBody'] = body
      
      result = send_api(arg)
      
      if result['status'] == 200:
        print("이벤트 룰 생성 완료 [ "+ body['groupName'] +" : %s ]" % result['data'])
      else:
        print("이벤트 룰 생성 실패 [ %s ]" % result['data']['msg'])
    # end for
  # end if
# end def


# eventSelect
def eventSelect(param):
  arg = param
  if 'prodKey' in param:
    arg['pageNum'] = input("\n\n페이지 번호를 입력하세요.\n종료하려면 비어있는 채로 엔터키를 입력하세요 [input number or empty] : ")
  else:
    x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
    if x == 'ok':
      commonApi.getSystemSchemaKeyList()
    # end if
    
    arg['prodKey'] = input("\n\nprodKey를 입력하세요.\n'*'를 입력하면 전체 입니다. [input 'prodKey'] : ")
    if arg['prodKey'] != '': 
      arg['search'] = input("\n\n검색어를 입력하세요. [input text] : ")
      arg['pageSize'] = input("\n\n페이지 사이즈를 입력하세요. [input number] : ")
      arg['pageNum'] = input("\n\n페이지 번호를 입력하세요.\n종료하려면 비어있는 채로 엔터키를 입력하세요 [input number or empty] : ")
    # end if
  # end if
  
  if arg['pageNum'] == '':
    arg['pageNum'] = 'exit'
  # end if
  
  objArg = {}
  objArg['method'] = 'POST'
  objArg['path'] = '/cw_fea/real/cw/api/rule/group/ruleGrp/query'
  
  body = {}
  body['prodKey'] = arg['prodKey']
  body['search'] = arg['search']
  body['pageSize'] = arg['pageSize']
  body['pageNum'] = arg['pageNum']
  objArg['requestBody'] = body
  
  if arg['pageNum'] != 'exit':
    if arg['prodKey'] != '':
      result = send_api(objArg)
      
      listData = []
      for data in result['data']['ruleGroups']:
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
      
      eventSelect(objArg['requestBody'])
    # end if
  # end if
# end def


# eventUpdate
def eventUpdate():
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    fnc.getSystemSchemaList()
  # end if
  
  prodKey = input("\n\nprodKey를 입력하세요. 이벤트 룰 ID를 조회합니다 [input 'prodKey'] : ")
  if prodKey != '':
    arg = {
      'prodKey': prodKey,
      'search': '',
      'pageSize': 100,
      'pageNum': 1
    }
    fnc.getRuleGroupIdList(arg)
  # end if
  
  ruleGroupId = input("\n\nruleGroupId를 입력하세요. 이벤트 룰 정보를 조회합니다 [input 'ruleGroupId'] : ")
  if ruleGroupId != '':
    arg = {
      'prodKey': prodKey,
      'search': ruleGroupId,
      'pageSize': 100,
      'pageNum': 1
    }
    fnc.getRuleGroupList(arg)
  # end if
  
  x = input("\n\nprodKey를 입력하세요. 감시대상, 메트릭 그룹, 알림대상자 정보를 조회합니다 [input 'prodKey'] : ")
  if x != '':
    arg = {
      'prodKey': x,
    }
    fnc.getMonitorGrpKey(arg)
    fnc.getMetricGrpKey(arg)
    fnc.getNotiInfo()
  # end if
  
  x = input("\n\n이벤트 룰을 수정하시겠습니까??\n생성하려면 yaml파일을 작성하고 [ok] 를 누르세요 : ")
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


# eventDelete
def eventDelete():
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

# main
def main():
  inputMsg = """
  이벤트 룰에서 진행할 작업을 선택하세요.
  1. 생성
  2. 조회
  3. 수정
  4. 삭제
  """
  x = input(inputMsg)
  arg = {}
  
  if x == '1':
    arg['dataType'] = 'createData'
    eventCreate(arg)
  elif x == '2':
    # arg['dataType'] = 'selectData'
    eventSelect(arg)
  elif x == '3':
    arg['dataType'] = 'updateData'
    eventUpdate(arg)
  elif x == '4':
    arg['dataType'] = 'deleteData'
    eventDelete(arg)
  # end if
# end def

if __name__ == "__main__":
  main()
# end if