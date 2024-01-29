#import system library
import os, sys
import json
import yaml
import clipboard

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
  
  rsltData = json.loads(result)
  
  return rsltData
# end def

def select():
  # 1. input prodKey
  # 2. select
  #     - all
  #     - dimension type
  # 3. select dimension type
  #     - cpu
  #     - svr
  #     - disk
  #     ...
  # 4. search query string
  
  arg = {}
  arg['method'] = 'POST'
  arg['path'] = '/cw_fea/real/cw/api/rule/group/metric/search'
  
  body = {}
  body["prodKey"] = "460438474722512896"
  body["query"] = ""    # Search in metrics
  # body["dimValues"] = {
  #   "name": "type",
  #   "value": "disk"
  # }   # metric type
  arg['requestBody'] = body
  
  result = send_api(arg)
  tmp = json.dumps(result, indent=2, ensure_ascii=False)
  clipboard.copy(tmp)
  print(tmp +"\n\n결과가 클립보드에 저장되었습니다.")
  # listData = []
  # for data in result['data']:
  #   objData = {}
  #   objData['metric'] = data['metric']
  #   objData['desc'] = data['desc']
  #   objData['dimensions'] = data['dimensions']
  #   objData['calculation'] = data['options']['Min1']
  #   listData.append(objData)
  #   # print('==========================================')
  #   # print("metric == %s" % str(data['metric']))
  #   # print("desc == %s" % str(data['desc']))
  #   # print("dimensions == %s" % str(data['dimensions']))
  #   # print("options == %s" % str(data['options']['Min1']))
  # # end for
  
  # finData = json.dumps(listData, indent=2, ensure_ascii=False)
  # print(finData)
# end def


if __name__ == "__main__":
  select()
# end if