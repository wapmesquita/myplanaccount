import spreadsheet_helper

class AccountHelper:

    def __init__(self, db=None):
        self.db = db
        if self.db is None:
            self.db = spreadsheet_helper.SpreadsheetHelper()

    def getAccountsPosition(self):
        position = {}
        position['accounts'] = self.db.getAccounts()
        position['totalValue'] = 0
        for account in position['accounts']:
            position['totalValue'] = position['totalValue'] + account['balance']

        return position
