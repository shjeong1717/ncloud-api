import os
from datetime import datetime

_HOME_DIR = os.path.dirname(os.path.realpath(__file__))
_UPLOAD_DIR = _HOME_DIR +"/_upload"
_YAML_DIR = _HOME_DIR +"/yaml"

_NOW_DT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_NOW_TS = int(datetime.now().timestamp() * 1000)

_ACCESS_KEY = ""
_SECRET_KEY = ""
