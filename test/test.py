#import system library
import sys
import os
from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api

# import user library
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as con
import function as fnc

from api import commonApi


args = {
  'prodKey': '460438474722512896'
}
result = commonApi.getMetricDimension(args)
print(result)