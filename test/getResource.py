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
  API_HOST = "https://resourcemanager.apigw.ntruss.com"
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


# 리소스 목록
def getResourceList():
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/api/v1/resources'
  
  # request body
  # productName, resourceType 참고 페이지 : https://guide.ncloud-docs.com/docs/management-rmgr-1-1-2#NRNNcloudResourceNames
  body = {
    "pageIndex": 0,
    "pageSize": 100,
    "productName": "VPCServer",
    "resourceType": "Server"
  }
  arg['requestBody'] = body
  
  result = send_api(arg)
  clipboard.copy(result)
  print(result)
  # rsltData = json.loads(result)['data']
  # print("================= Resource Info Start =================")
  # listData = []
  # for data in rsltData:
  #   objData = {data['prodName'] : data['cw_key']}
  #   listData.append(objData)
  # # end for
  # finData = json.dumps(listData, indent=2, ensure_ascii=False)
  # clipboard.copy(finData)
  # print(finData)
  # print("================= Resource Info End =================")
# end def


if __name__ == "__main__":
  getResourceList()
# end if