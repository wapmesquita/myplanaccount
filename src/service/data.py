import json
from handler import request_handler
from helper import spreadsheet_helper
from google.appengine.api import users
from model import model


class DataService(request_handler.Request):

    @request_handler.json
    def get(self):
        db = spreadsheet_helper.SpreadsheetHelper(key="13UDQ_kXzybroSIlMwNGqanh-i1xV5qDwsM9GbOK6OO8")
        db.loadData()
        return db.getFullJson()

class SampleService(request_handler.Request):

    @request_handler.json
    def get(self):
        user = users.get_current_user()
        db_key = model.database_key(user.user_id())
        spreadsheet = model.Spreadsheet(parent=db_key)
        spreadsheet.key='13UDQ_kXzybroSIlMwNGqanh-i1xV5qDwsM9GbOK6OO8'
        spreadsheet.name='Sample'
        spreadsheet.put()
        return {'succes': True}
