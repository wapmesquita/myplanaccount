import spreadsheet_helper
import recurrent_events_helper
import datetime
from datetime import date
import dateutil.relativedelta
import copy
import logging

class SpendsHelper():

    def __init__(self, db=None):
        self.db = db
        if self.db is None:
            self.db = spreadsheet_helper.SpreadsheetHelper()

    def getSpendsByMonth(self, month, year):
        spends = []
        spends.extend(self.getRecurrentSpends(month, year))
        spends.extend(self.getSpends(month, year))

        for cc in self.db.getCreditCards():
            if (cc['month'] == month) and (cc['year'] == year):
                spends.append({
                    'name' : cc['name'],
                    'expirationDay': cc['expirationDay'],
                    'value' : cc['balance'],
                    'group' : 'credit_card'
                })

        return spends

    def getRecurrentSpends(self, m, y):
        logging.debug("$$$$ Retrieving recurrent spends: %s-%s", m, y)
        return recurrent_events_helper.filterRecurrentEvent(m, y, self.db.getRecurrentSpends())

    def getSpends(self, month, year):
        list = []
        for s in self.db.getSpends():
            m = s['month']
            y = s['year']
            if (m is not None) and (month != m):
                continue

            if (y is not None) and (year != y):
                continue

            list.append(s)

        return list

    def calculateSpendPercentual(self, month, year, spend):
        today = date.today()
        firstDay = spend['firstDay']
        expirationDay = spend['expirationDay']
        nextDate = datetime.date(year, month, firstDay)
        logging.debug("Calculating percentual: %s ", spend)
        logging.debug("percentualLog: today: %s", today)
        logging.debug("percentualLog: fistDay: %s", firstDay)
        logging.debug("percentualLog: expirationDay: %s", expirationDay)
        logging.debug("percentualLog: nextDate: %s", nextDate)

        if expirationDay < firstDay:
            nextDate = nextDate - dateutil.relativedelta.relativedelta(months=1)
            logging.debug("percentualLog: nextDate changed: %s", nextDate)

        if nextDate > today:
            deltaDays = nextDate - today
            logging.debug("percentualLog: deltaDays: %s", deltaDays)

            deltaPercent = ((deltaDays.days * 100.0) / 30.0)
            logging.debug("percentualLog: deltaPercent: %s", deltaPercent)

            delta = (deltaPercent / 100.0)
            logging.debug("percentualLog: delta: %s", delta)
            if delta < 1:
                spend['estimateSpend'] = spend['estimateSpend'] * delta


        if nextDate < today:
            spend['estimateSpend'] = 0

        logging.debug("percentualLog: new spend value: %s", spend['estimateSpend'])
        logging.debug(" ============= END PROPORTIONAL ================")

    def getProportionalSpendsByMonth(self, month, year, start_dayOfMonth):
        spends = self.db.getProportionalSpends()
        proportionalSpends = []
        if spends is not None:
            for s in spends:
                if s['firstDay'] > start_dayOfMonth:
                    spend = copy.deepcopy(s)
                    proportionalSpends.append(spend)
                    self.calculateSpendPercentual(month, year, spend)

        return proportionalSpends
