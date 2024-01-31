#import system library
import os, sys
import json
import yaml
import clipboard
import argparse

# import user library
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as con
import function as fnc

from api import commonApi


#set variables
filename = con._YAML_DIR +"/plugin.yaml"


# api 호출 실행
def send_api(param):
  API_HOST = "https://cw.apigw.ntruss.com"
  url = API_HOST + param['path']
  
  objHeader = {}
  objHeader['path'] = param['path']
  objHeader['method'] = param['method']
  headers = fnc.make_header(objHeader)
  # add header
  headers['x-ncp-dmn_cd'] = 'PUB'
  headers['x-ncp-region_code'] = 'KR'
  
  objApi = {}
  objApi['url'] = url
  objApi['headers'] = headers
  objApi['body'] = param['requestBody']
  objApi['method'] = param['method']
  result = fnc.call_api(objApi)
  
  rsltData = json.loads(result)
  
  return rsltData
# end def


# set process plugin
def setPlugin(param):
  prodKey = input("\n\n 서버 인스턴스 정보를 조회합니다. [press any key] : ")
  arg = {
    'pageIndex': 0,
    'pageSize': 100,
    'productName': 'VPCServer',
    'resourceType': 'Server'
  }
  result = commonApi.getResourceList(arg)
  listRsc = result['items']
  
  arg['productName'] = 'Server'
  result = commonApi.getResourceList(arg)
  
  listRsc = listRsc + result['items']
  listData = []
  for data in listRsc:
    objData = {}
    objData['platformType'] = data['platformType']
    objData['resourceName'] = data['resourceName']
    objData['resourceId'] = data['resourceId']
    listData.append(objData)
  # end for
  
  finData = json.dumps(listData, indent=2)
  clipboard.copy(finData)
  print(finData +'\n 클립보드에 복사되었습니다.')
  
  x = input("\n\n 플러그인을 설정하시겠습니까??\n yaml파일이 준비되면 [ok] 를 누르세요 : ")
  if x == 'ok':
    with open(filename) as yamlfile:
      yamldata = yaml.full_load(yamlfile)
    #end with
    
    list = yamldata[param['dataType']][param['kind']]
    
    for data in list:
      # request body
      body = {}
      body["instanceNo"] = data['instanceNo']
      body["configList"] = data['configList']
      
      arg = {}
      arg['method'] = 'POST'
      arg['path'] = param['path']
      arg['requestBody'] = body
      
      result = send_api(arg)
      
      if result['status'] == 200:
        print("플러그인 설정 완료")
      else:
        print("플러그인 설정 실패 : %s [ %s ]" % (result['status'], result['data']['msg']))
    # end for
  # end if
# end def


# get process plugin list
def selectPlugin(param):
  # request body
  body = {}
  
  arg = {}
  arg['method'] = 'GET'
  arg['path'] = param['path']
  arg['requestBody'] = body
  
  result = send_api(arg)
  finData = json.dumps(result['data'], indent=2, ensure_ascii=False)
  
  clipboard.copy(finData)
  print(finData +'\n 클립보드에 복사되었습니다.')
# end def


# delete process plugin
def deletePlugin(param):
  x = input("\n\n 플러그인을 삭제하시겠습니까??\n yaml파일이 준비되면 [ok] 를 누르세요 : ")
  if x == 'ok':
    with open(filename) as yamlfile:
      yamldata = yaml.full_load(yamlfile)
    #end with
    
    list = yamldata[param['dataType']][param['kind']]
    
    for data in list:
      # request body
      body = {}
      body["instanceNo"] = data['instanceNo']
      body["configList"] = data['configList']
      
      arg = {}
      arg['method'] = 'POST'
      arg['path'] = param['path']
      arg['requestBody'] = body
      
      result = send_api(arg)
      
      if result['status'] == 200:
        print("플러그인 삭제 완료")
      else:
        print("플러그인 삭제 실패 [ %s ]" % result)
    # end for
  # end if
# end def


# main
def main(param):
  dataType = ''
  if param == 'process':
    dataType = 'processPlugin'
  elif param == 'port':
    dataType = 'portPlugin'
  elif param == 'file':
    dataType = 'filePlugin'
  # end if
  
  inputMsg = """
  %s 진행할 작업을 선택하세요.
  1. 설정
  2. 조회
  3. 삭제
  [input number] : 
  """
  x = input(inputMsg % (dataType))
  
  arg = {'dataType': dataType}
  
  if x == '1':
    arg['kind'] = 'set'
    arg['path'] = '/cw_server/real/api/plugin/'+ param
    setPlugin(arg)
  elif x == '2':
    arg['path'] = '/cw_server/real/api/plugin/'+ param
    selectPlugin(arg)
  elif x == '3':
    arg['kind'] = 'delete'
    arg['path'] = '/cw_server/real/api/plugin/'+ param +'/remove'
    deletePlugin(arg)
  # end if
# end def

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog = "python3 execPluginProcess.py",
    description = "플러그인 컨트롤러 [process, port, file]\n 각 플러그인 별로 설정, 조회, 삭제 기능을 실행합니다."
  )
  parser.add_argument('-t', '--type', choices=['process', 'port', 'file'], help='process, port, file 중 입력', required=True)
  args = parser.parse_args()
  main(args.type)
# end if