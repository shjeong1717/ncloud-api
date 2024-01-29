#import system library
import os, sys
import json
import yaml
import clipboard

# import user library
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as con
import function as fnc

from api import commonApi


#set variables
filename = con._YAML_DIR +"/metric.yaml"


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
  
  rsltData = json.loads(result)
  
  return rsltData
# end def


# metricsCreate
def metricsCreate(param):
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    commonApi.getSystemSchemaKeyList()
  # end if
  
  x = input("\n\메트릭그룹을 생성하시겠습니까??\n생성하려면 yaml파일을 작성하고 [ok] 를 누르세요 : ")
  if x == 'ok':
    with open(filename) as yamlfile:
      yamldata = yaml.full_load(yamlfile)
    #end with
    
    list = yamldata[param['dataType']]
    
    for data in list:
      arg = {}
      arg['method'] = 'POST'
      arg['path'] = '/cw_fea/real/cw/api/rule/group/metrics'
      
      # request body
      body = {}
      body["prodKey"] = data['prodKey']
      body["groupName"] = data['groupName']
      body["groupDesc"] = data['groupDesc']
      body["metricsGroupItems"] = data['metricsGroupItems']
      arg['requestBody'] = body
      
      result = send_api(arg)
      
      if result['status'] == 200:
        print("메트릭그룹 생성 완료 [ "+ body['groupName'] +" : %s ]" % result['data'])
      else:
        print("메트릭그룹 생성 실패 [ %s ]" % result['data']['msg'])
    # end for
  # end if
# end def


# metricsSelect
def metricsSelect(param):
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    commonApi.getSystemSchemaKeyList()
  # end if
  
  prodKey = input("\n\nprodKey를 입력하세요. 메트릭그룹을 조회합니다. [input 'prodKey'] : ")
  if prodKey != '':
    arg = {}
    arg['method'] = 'GET'
    arg['path'] = '/cw_fea/real/cw/api/rule/group/metrics/query/'+ prodKey
    
    body = {}
    arg['requestBody'] = body
    
    result = send_api(arg)
    listData = []
    for data in result['data']['metricsGroups']:
      objData = data
      listData.append(objData)
    # end for
    finData = json.dumps(listData, indent=2, ensure_ascii=False)
    clipboard.copy(finData)
    print(finData +"\n\n결과가 클립보드에 저장되었습니다.")
  # end if
  
# end def


# metricsUpdate
def metricsUpdate(param):
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    commonApi.getSystemSchemaKeyList()
  # end if
  
  prodKey = input("\n\nprodKey를 입력하세요. 감시대상그룹 ID를 조회합니다. [input 'prodKey'] : ")
  if prodKey != '':
    arg = {
      'prodKey': prodKey,
    }
    commonApi.getMonitorGrpKey(arg)
  # end if
  
  x = input("\n\n감시대상그룹을 수정하시겠습니까??\n수정하려면 yaml파일을 작성하고 [ok] 를 누르세요 : ")
  if x == 'ok':
    with open(filename) as yamlfile:
      yamldata = yaml.full_load(yamlfile)
    #end with
    
    list = yamldata[param['dataType']]
    
    for data in list:
      arg = {}
      arg['method'] = 'PUT'
      arg['path'] = '/cw_fea/real/cw/api/rule/group/monitor'
      
      # request body
      body = {}
      body["prodKey"] = data['prodKey']
      body["id"] = data['id']
      body["groupName"] = data['groupName']
      body["groupDesc"] = data['groupDesc']
      body["monitorGroupItemList"] = data['monitorGroupItemList']
      arg['requestBody'] = body
      
      result = send_api(arg)
      
      if result['status'] == 200:
        print("감시대상그룹 수정 완료")
      else:
        print("감시대상그룹 수정 실패 [ %s ]" % result['data']['msg'])
    # end for
  # end if
# end def


# metricsDelete
def metricsDelete(param):
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    commonApi.getSystemSchemaKeyList()
  # end if
  
  prodKey = input("\n\nprodKey를 입력하세요. 감시대상그룹 ID를 조회합니다. [input 'prodKey'] : ")
  if prodKey != '':
    arg = {
      'prodKey': prodKey,
    }
    commonApi.getMonitorGrpKey(arg)
  # end if
  
  x = input("\n\n감시대상그룹을 삭제하시겠습니까??\n삭제하려면 yaml파일을 작성하고 [ok] 를 누르세요 : ")
  if x == 'ok':
    with open(filename) as yamlfile:
      yamldata = yaml.full_load(yamlfile)
    #end with
    
    list = yamldata[param['dataType']]
    
    for data in list:
      arg = {}
      arg['method'] = 'DELETE'
      arg['path'] = '/cw_fea/real/cw/api/rule/group/monitor?prodKey='+ data['prodKey']
      
      # requestBody
      body = []
      for id in data['groupIds']:
        body.append(id)
      # end for
      arg['requestBody'] = body
      
      result = send_api(arg)
      
      if result['status'] == 200:
        print("감시대상그룹 삭제 완료")
      else:
        print("감시대상그룹 삭제 실패 [ %s ]" % result['data']['msg'])
    # end for
  # end if
# end def

# main
def main():
  inputMsg = """
  진행할 작업을 선택하세요.
  1. 생성
  2. 조회
  3. 수정
  4. 삭제
  """
  x = input(inputMsg)
  arg = {}
  
  if x == '1':
    arg['dataType'] = 'createData'
    metricsCreate(arg)
  elif x == '2':
    # arg['dataType'] = 'selectData'
    metricsSelect(arg)
  elif x == '3':
    arg['dataType'] = 'updateData'
    metricsUpdate(arg)
  elif x == '4':
    arg['dataType'] = 'deleteData'
    metricsDelete(arg)
  # end if
# end def

if __name__ == "__main__":
  main()
# end if