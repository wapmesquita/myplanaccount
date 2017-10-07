import spreadsheet_helper

class RevenueHelper():

    def __init__(self, db=None):
        self.db = db
        if self.db is None:
            self.db = spreadsheet_helper.SpreadsheetHelper()

    def getRevenuesByMonth(self, month, year):
        list = []
        for r in self.db.getRevenues():
            if (r['month'] is not None) and (month != r['month']):
                continue

            if (r['year'] is not None) and (year != r['year']):
                continue

            list.append(r)

        return list
