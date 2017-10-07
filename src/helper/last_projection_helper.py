from google.appengine.api import users
from model import model
from google.appengine.ext import db

class LastProjectionHelper:

    def load(self):
        user = users.get_current_user()
        db_key = model.database_key(user.user_id())
        o = model.LastProjection.query(ancestor=db_key).get()
        if o:
            return {'month':o.month,'year':o.year,'sht':o.sht}

        return {}

    def save(self, month, year, key):
        user = users.get_current_user()
        db_key = model.database_key(user.user_id())

        o = model.LastProjection.query(ancestor=db_key).get()
        if o:
            db.delete(o.key)

        obj = model.LastProjection(parent=db_key)
        obj.sht=key
        obj.year=str(year)
        obj.month=str(month)
        print obj
        obj.put()
