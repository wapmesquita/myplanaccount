from google.appengine.ext import ndb

DEFAULT_DB_NAME = 'default_myplancount'

def database_key(name=DEFAULT_DB_NAME):
    return ndb.Key('MyPlanCount', name)

class Spreadsheet(ndb.Model):
    key = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=False)

class LastProjection(ndb.Model):
    sht = ndb.StringProperty(indexed=False)
    month = ndb.StringProperty(indexed=False)
    year = ndb.StringProperty(indexed=False)
