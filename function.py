#import system library
import os, sys
from datetime import datetime
from PIL import Image			# 이미지처리
import hashlib
import hmac
import base64
import json
import requests

# import user library
import config as con

#####################################################################################
### common function
#####################################################################################
# 폴더생성
# description : 해당 경로에 폴더가 없으면 생성
# param
# 	location - 생성할 폴더 경로
def MAKE_FOLDER(location) :
  if not os.path.isdir(location) :
    os.mkdir(location)
  #end if
#end def


# 썸네일만들기
# param
# 	src - 원본이미지
# 	savefile - 저장될 파일명(경로포함)
# 	arr_size - 가로/세로 사이즈(리스트형식)
def MAKE_THUMB(src, savefile, arr_size) :
  im = Image.open(src)
  size = (arr_size[0], arr_size[1])
  im.thumbnail(size)
  im.save(savefile)
#end def


# 이미지파일명 추출
# description : 전체URL에서 파일명만 추출
def GET_FILENAME_FROM_URL(src) :
  cnt = src.rfind("/") + 1				# 파일명 시작위치
  fullfilename = src[cnt:]				# 전체파일명

  return fullfilename
#end def


# 파일명만 추출
def GET_FILENAME(src) :
  filename = src.split(".")[0]		# 파일명

  return filename
#end def


# 확장자만 추출
def GET_EXT(src) :
  ext = src.split(".")[1]		# 확장자

  return ext
#end def


# json default : datetime
def JSON_DEFAULT(pa) :
  if isinstance(pa, datetime) :
    return pa.__str__()
  #end if
#end def


#####################################################################################
### project function
#####################################################################################
# Make signature key
def	make_signature(uri, now_ts, method):
  access_key = con._ACCESS_KEY				# access key id (from portal or Sub Account)
  secret_key = con._SECRET_KEY				# secret key (from portal or Sub Account)
  secret_key = bytes(secret_key, 'UTF-8')

  # method = "GET"

  message = method + " " + uri + "\n" + now_ts + "\n" + access_key
  message = bytes(message, 'UTF-8')
  signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
  return signingKey
# end def

# make header
def make_header(params):
  now_ts = int(datetime.now().timestamp() * 1000)
  sign = make_signature(params['path'], str(now_ts), params['method'])
  
  headers = {}
  headers["Content-Type"] = "application/json"
  headers["x-ncp-apigw-signature-v2"] = sign
  headers["x-ncp-apigw-timestamp"] = str(now_ts)
  headers["x-ncp-iam-access-key"] = con._ACCESS_KEY
  
  return headers
# end def

# Call API
def call_api(params):
  try:
    if params['method'] == 'GET':
      response = requests.get(params['url'], headers=params['headers'])
    elif params['method'] == 'POST':
      response = requests.post(params['url'], headers=params['headers'], data=json.dumps(params['body']))
    elif params['method'] == 'PUT':
      response = requests.put(params['url'], headers=params['headers'], data = json.dumps(params['body']))
    elif params['method'] == 'DELETE':
      response = requests.delete(params['url'], headers=params['headers'], data = json.dumps(params['body']))
    # end if
    
    # print("response status == %s" % response.status_code)
    # print("response text == %s" % response.text)
    
    rsltData = {}
    if response.text != "":
      rsltData = json.loads(response.text)
    # end if
    
    objData = {}
    objData['status'] = response.status_code
    objData['data'] = rsltData
    
    return json.dumps(objData, indent=2)
  except Exception as ex:
    print("exception [%s]" % ex)
  # end try
# end def

