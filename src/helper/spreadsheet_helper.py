from mock import mock_data
from gac import spreadsheet
from oauth2client.service_account import ServiceAccountCredentials
import os
from oauth2client import client

class SpreadsheetHelper:
    def __init__(self, key=None, url=None, creds=None):
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.creds = creds
        if creds is None:
            cred_file = os.path.dirname(os.path.realpath(__file__)) + '/myplancount.json'
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, self.scope)
        self.sht = spreadsheet.Spreadsheet(credentials=self.creds, key=key, url=url)

    def getAccounts(self):
        return self.sht.getWorkSheetJson('accounts')

    def getRecurrentSpends(self):
        return self.sht.getWorkSheetJson('recurrent_spends')

    def getRecurrentInvestiments(self):
        return self.sht.getWorkSheetJson('recurrent_investiments')

    def getInvestiments(self):
        return self.sht.getWorkSheetJson('investiments')

    def getSpends(self):
        return self.sht.getWorkSheetJson('spends')

    def getRevenues(self):
        return self.sht.getWorkSheetJson('revenues')

    def getProportionalSpends(self):
        return self.sht.getWorkSheetJson('proportional_spends')

    def getCreditCards(self):
        return self.sht.getWorkSheetJson('credit_cards')

    def loadData(self):
        self.sht.loadWholeJson()

    def getFullJson(self):
        return self.sht.getJson()

    def config(self):
        self.sht.createFromTemplate()

    def getTitle(self):
        return self.sht.getTitle()

    def getKey(self):
        return self.sht.getKey()
