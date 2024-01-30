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

# select
def select():
  x = input("\n\n클라우드 플랫폼 상품의 prodKey(cw_key)를 조회하시겠습니까? [ok] : ")
  if x == 'ok':
    commonApi.getSystemSchemaKeyList()
  # end if
  
  prodKey = input("\n\nprodKey를 입력하세요. [input 'prodKey'] : ")
  if prodKey != '':
    arg = {
      'prodKey': prodKey,
      'query': ''
    }
    listDim = commonApi.getMetricDimension(arg)
    dim = input("\n\n조회할 메트릭 디멘션을 입력하세요. 전체 검색은 'all'을 입력하세요. [input string]\n"+ listDim +" : ")
    query = input("\n\n메트릭 이름으로 검색어를 입력하세요. [input string] : ")
    
    if dim == 'all':
      arg['dim'] = ''
    else:
      arg['dim'] = dim
    # end if
    if query != '':
      arg['query'] = query
    # end if
    listMetric = commonApi.getMetricList(arg)
    clipboard.copy(listMetric)
    print(listMetric +'\n조회 결과가 클립보드에 복사되었습니다.')
  # end if
# end def


if __name__ == "__main__":
  select()
# end if