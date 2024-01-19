#import system library
import sys
import requests
import json
import time
from datetime import datetime

# import user library
sys.path.insert(0, '/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api')
from _lib import config as con
from _lib import cMysql
from _lib import cLogger
from _lib import function as fnc

# set logger
cLog = cLogger.cLogger("test")
logger = cLog.set_logger()

def hello():
  try :
    # set db
    sql = cMysql.cMysql(con.DB_INFO)
    sql.db_conn()

    arParam = []
    qry = """
      SELECT * FROM TB_BOARD
    """
    #arParam.append(p_cd)
    result = sql.exec('list', qry, arParam)
    cnt = result['cnt']
    ds = result['data']
    logger.info("ds == "+ str(ds))
    return ds
  #end try
  except Exception as err :
    logger.error("find error : "+ str(err))
  #end except
  finally :
    sql.close()
  #end finally
#end def

hello()