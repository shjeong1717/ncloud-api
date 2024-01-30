#import system library
import sys
import requests
import json
import time
import subprocess

# import user library
import config as con
import function as fnc


def main():
  exec(open("hello.py").read())
  # subprocess.Popen(["python3", "api/event/createRuleGroup.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
  # ev.main()
# end def

if __name__ == '__main__':
	main()