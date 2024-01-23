#import system library
import sys
import requests
import json
import time
from datetime import datetime
from flask import Flask, request
import subprocess

# import user library
sys.path.insert(0, '/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api')
from _lib import config as con
from _lib import cLogger
from _lib import function as fnc

# set logger
cLog = cLogger.cLogger("main")
logger = cLog.set_logger()

app = Flask(__name__)

@app.route("/")
def hello():
  # arg = "getSystemSchemaKeyList.py"+ request.args.get('arg')
  arg = "api/getSystemSchemaKeyList.py"
  p = subprocess.Popen(arg , stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()
  
  return output

if __name__ == '__main__':
	app.run(host="0.0.0.0", port="30080", debug=True)