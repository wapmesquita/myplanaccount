import spreadsheet_helper
import recurrent_events_helper
import logging
import math
import copy
import datetime

class InvestimentHelper():

    def __init__(self, db=None):
        self.db = db
        if self.db is None:
            self.db = spreadsheet_helper.SpreadsheetHelper()

    def getInvestimentsPosition(self):
        items = []
        for investiment in  self.db.getInvestiments():
            item = {}
            item['target'] = investiment['target']
            item['value'] = investiment['value']
            item['endDate'] = investiment['endDate']
            items.append(item)
        return items


    def getInvestimentsToDoByMonth(self, month, year):
        logging.debug('$$$$ Retrieving investiments: %s-%s', month, year)
        items = copy.deepcopy(recurrent_events_helper.filterRecurrentEvent(month, year, self.db.getRecurrentInvestiments()))
        for i in items:
            self.applyInterestRateYear(i, month, year)
            self.applyInterestRateMonth(i, month, year)
        logging.info('============== END RECURRENT INVESTIMENTS ================')
        return items

    def applyInterestRateYear(self, item, month, year):
        i = item['interestRateYear']
        if i is not None and i > 0:
            i = 1.0 + i / 100.0
            startYear = item['firstYear']
            if startYear is None:
                startYear = datetime.datetime.now().year

            n = year - startYear
            if n > 0 :
                logging.debug("$$$$$ Applying rate(year) to investiment: %s", item)
                logging.debug("$$$$$$ f=%s*(%s ^ %s)", item['value'], i, n)
                item['value'] = item['value'] * math.pow(i, n)
                logging.debug("$$$$$$$ ===== %s", item['value'])

    def applyInterestRateMonth(self, item, month, year):
        i = item['interestRateMonth']
        if i is not None and i > 0:
            i = 1.0 + i / 100.0

            startMonth = item['firstMonth']
            if startMonth is None:
                startMonth = datetime.datetime.now().month

            startYear = item['firstYear']
            if startYear is None:
                startYear = datetime.datetime.now().year

            startDate=datetime.date(startYear, startMonth, 1)
            endDate=datetime.date(year, month, 1)

            n = (year - startYear)*12 + month - startMonth
            if n > 0:
                logging.debug("$$$$$ Applying rate(month) to investiment: %s", item)
                logging.debug("$$$$$$ f=%s*(%s ^ %s)", item['value'], i, n)
                item['value'] = item['value'] * math.pow(i, n)
                logging.debug("$$$$$$$ ===== %s", item['value'])
