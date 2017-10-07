import json
from helper import spreadsheet_helper
from handler import request_handler, http_handler
from google.appengine.api import users
from model import model
from gac import oauth_checker

class StorageService(request_handler.Request):

    @request_handler.json
    def get(self):
        list = []
        user = users.get_current_user()
        db_key = model.database_key(user.user_id())
        entity = model.Spreadsheet
        for s in entity.query(ancestor=db_key).fetch(1000):
            list.append({'name':s.name, 'key':s.key})
        return list

    @request_handler.json
    def put(self):
        params = self.read_json()
        user = users.get_current_user()
        db_key = model.database_key(user.user_id())
        spreadsheet = model.Spreadsheet(parent=db_key)
        spreadsheet.key=params['key']
        spreadsheet.name=params['name']
        spreadsheet.put()
        return {'success': True}

    @request_handler.json
    def post(self):
        params = self.read_json()
        url = params['url']

        credentials = oauth_checker.getCredentials(self.request.cookies)
        db = spreadsheet_helper.SpreadsheetHelper(url=url, creds=credentials)
        db.config()

        user = users.get_current_user()
        db_key = model.database_key(user.user_id())
        spreadsheet = model.Spreadsheet(parent=db_key)
        spreadsheet.key=db.getKey()
        spreadsheet.name=db.getTitle()
        spreadsheet.put()
        return {'success': True}
