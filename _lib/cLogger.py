# import library
import logging
import logging.handlers
from _lib import config as con


# logging class
# level : DEBUG, INFO, WARNING, ERROR, CRITICAL
class cLogger :
  def __init__(self, name) :
    self.logger = logging.getLogger(name)
    self.logger.setLevel(logging.DEBUG)


  def set_logger(self) :
    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] => %(message)s")

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    self.logger.addHandler(sh)

    filename = "/Users/sanghoonjeong/Work/cloud/workspace/ncloud-api/_log/ncloud-api.log"
    fileMaxByte = 1024 * 1024 * 1000	#1.0GB
    fh = logging.handlers.TimedRotatingFileHandler(filename, when='d', interval=1, encoding='utf-8')
    #fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    fh.suffix = "-%Y%m%d"
    self.logger.addHandler(fh)

    return self.logger