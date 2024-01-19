from datetime import datetime
from datetime import timezone

_HOME_DIR = "/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api"
_UPLOAD_DIR = _HOME_DIR +"/_upload"
_NOW_DT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_NOW_TS = int(datetime.now().timestamp() * 1000)
_ACCESS_KEY = "E7F12FC35D78208D549F"
_SECRET_KEY = "A2F4A986F53819ADD599803D52BB66595E319263"

DB_INFO = {'host': '192.168.70.145', 'user': 'root', 'passwd': '123qwe!@#', 'db': 'jsh17', 'charset': 'utf8'}
