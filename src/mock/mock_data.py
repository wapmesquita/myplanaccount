import json
import sys
import codecs
import os

def load():
  path = os.path.dirname(os.path.abspath(__file__)) + "/db-finance-structure.json"

  jsonfile = file(path, "r")
  jsondata = json.loads(jsonfile.read().decode("utf-8-sig"))

  return jsondata
