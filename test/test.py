#import system library
import sys
import requests
import json
import time
from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api

# import user library
sys.path.insert(0, '/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api')
from _lib import config as con
from _lib import cMysql
from _lib import cLogger
from _lib import function as fnc

# set logger
cLog = cLogger.cLogger("test")
logger = cLog.set_logger()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
  a = datetime.now()
  b = a.timestamp()
  c = a.timestamp() * 1000
  z = "now == "+ str(a) +" // timestampmilli == "+ str(b) +" // timestamp == "+ str(c)
  return z

if __name__ == '__main__':
	app.run(host="0.0.0.0", port="8000", debug=True)


# def send_api(path, method):
#   API_HOST = "http://www.example.com"
#   url = API_HOST + path
#   headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
#   body = {
#     "key1": "value1",
#     "key2": "value2"
#   }
  
#   try:
#     if method == 'GET':
#       response = requests.get(url, headers=headers)
#     elif method == 'POST':
#       response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
#     print("response status %r" % response.status_code)
#     print("response text %r" % response.text)
#   except Exception as ex:
#     print(ex)
#   # end try
# # end def

# # 호출 예시
# send_api("/test", "POST")