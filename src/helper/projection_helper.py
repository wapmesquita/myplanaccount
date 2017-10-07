from helper import day_register_helper, account_helper, spends_helper, revenue_helper, spreadsheet_helper, investiment_helper
import datetime
import logging
import copy

class ProjectionHelper:

    def __init__(self, db=None):
        self.db = db
        if self.db == None:
            self.db = spreadsheet_helper.SpreadsheetHelper()
        self.db.loadData()

    def getCurrentMonthProjection(self):
        accountsPosition = account_helper.AccountHelper(self.db).getAccountsPosition()
        now = datetime.datetime.now()
        projection = {}
        projection['accounts'] = accountsPosition
        projection['projection'] = self.getProjectionByMonth(accountsPosition['totalValue'], now.day, now.month, now.year)
        return projection

    def getProjectionByMonth(self, initial_amount, start_dayOfMonth, month, year, lastProjection=None):
        p = {}
        p['initialAmount'] = initial_amount
        p['finalAmount'] = initial_amount
        p['month'] = month
        p['year'] = year
        p['transactionsByDay'] = {}

        logging.info(" =================== BEGIN ================")
        logging.info('Projection \n %s ', p)

        dayRegisterHelper = day_register_helper.DayRegisterHelper()
        spendsHelper = spends_helper.SpendsHelper(self.db)

        spends = spendsHelper.getSpendsByMonth(month, year)
        self.addRegisterToDays(start_dayOfMonth, p['transactionsByDay'], 'spends', dayRegisterHelper.createList(spends, 'name', 'value', 'expirationDay', 'group'))

        proportionalSpends = spendsHelper.getProportionalSpendsByMonth(month, year, start_dayOfMonth)
        self.addRegisterToDays(start_dayOfMonth, p['transactionsByDay'], 'spends', dayRegisterHelper.createList(proportionalSpends, 'name', 'estimateSpend', 'expirationDay', 'group'))

        revenues = revenue_helper.RevenueHelper(self.db).getRevenuesByMonth(month, year)
        self.addRegisterToDays(start_dayOfMonth, p['transactionsByDay'], 'revenues', dayRegisterHelper.createList(revenues, 'name', 'value', 'day'))

        investimentHelper = investiment_helper.InvestimentHelper(self.db)
        investimentsToDo = investimentHelper.getInvestimentsToDoByMonth(month, year)
        self.addRegisterToDays(start_dayOfMonth, p['transactionsByDay'], 'spends', dayRegisterHelper.createList(investimentsToDo, 'name', 'value', 'expirationDay', 'target'))

        if lastProjection is None:
            p['investiments'] = self.calculateInvestimentPosition(investimentsToDo, investimentHelper.getInvestimentsPosition(), start_dayOfMonth)
        else:
            p['investiments'] = self.calculateInvestimentPosition(investimentsToDo, investimentHelper.getInvestimentsPosition(), start_dayOfMonth, lastProjection['investiments'])

        return self.calculateProjection(p)

    def calculateInvestimentPosition(self, investimentsToDo, realPosition, start_dayOfMonth, estimatedPosition=None):
        if estimatedPosition is None:
            position = copy.deepcopy(realPosition)
        else:
            position = copy.deepcopy(estimatedPosition)

        for investimentToDo in investimentsToDo:
            if investimentToDo['expirationDay'] > start_dayOfMonth:
                self.updateInvestimentValue(investimentToDo, position)

        return position

    def updateInvestimentValue(self, investimentToDo, position):
        toUpdate=None
        for investiment in position:
            if investiment['target'] == investimentToDo['target'] and investiment['endDate'] == '':
                toUpdate = investiment
                break

        if toUpdate is None:
            toUpdate = {}
            toUpdate['target']=investimentToDo['target']
            toUpdate['value']=0.0
            toUpdate['endDate']=''
            position.append(toUpdate)

        toUpdate['value'] = float(toUpdate['value']) + float(investimentToDo['value'])

    def addRegisterToDays(self, dayOfMonth, days, attr, list):
        for item in list:
            day = item['dayOfMonth']
            if day >= dayOfMonth:
                if not day in days:
                    days[day] = {'day': day, 'spends': [], 'revenues': []}

                days[day][attr].append(item)

    def calculateProjection(self, p):
        for day in range(1,32):
            if day in p['transactionsByDay']:
                self.calculateDay(p, day)
        return p

    def calculateDay(self, p, dayOfMonth):
        day = p['transactionsByDay'][dayOfMonth]
        trnasactionEOD = 0
        for item in day['revenues']:
            trnasactionEOD = trnasactionEOD + item['value']

        for item in day['spends']:
            trnasactionEOD = trnasactionEOD - item['value']

        day['trnasactionEOD'] = trnasactionEOD
        p['finalAmount'] = p['finalAmount'] + trnasactionEOD
        day['amountEOD'] = p['finalAmount']

    def projectFromNowTo(self, end_month, end_year):
        now = datetime.datetime.now()
        start_month = now.month
        start_year = now.year
        delta = end_year * 100 + end_month

        result = {}
        current = self.getCurrentMonthProjection();
        result[str((start_year * 100) + start_month)] = current['projection'];

        if end_month > start_month or end_year > start_year:
            last = result[str((start_year * 100) + start_month)]
            for month in range(start_month+1, 13):
                result[str((start_year * 100) + month)] = self.getProjectionByMonth(last['finalAmount'], 1, month, start_year, last)
                last = result[str((start_year * 100) + month)]

            for year in range(start_year+1, end_year+1):
                for month in range(1, 13):
                    if (year * 100 + month) > delta:
                        return result
                    result[str((year * 100) + month)] = self.getProjectionByMonth(last['finalAmount'], 1, month, year, last)
                    last = result[str((year * 100) + month)]

        return result

def printProjection(projection):
    print 'Month: ', projection['month'], '/', projection['year']
    for day in range(1,32):
        if day in projection['transactionsByDay']:
            print '# ', day, ':'
            transactions = projection['transactionsByDay'][day]
            for r in transactions['revenues']:
                print '* ', r['value'], '\t\t', r['name'], '\n---'
            for s in transactions['spends']:
                print '* (',s['value'],')', '\t\t', s['name'], '\n---'
            print '## End of the day: ', transactions['amountEOD'], '\n---'

    print '### End of Month: ', projection['finalAmount'], '\n----------------\n'

if __name__ == "__main__":
    print '\n\n\n'

    ps = ProjectionHelper();
    current = ps.getCurrentMonthProjection();
    print 'Money Available: ', current['accounts']['totalValue']
    print '---'
    printProjection(current['projection'])

    last = ps.getProjectionByMonth(current['projection']['finalAmount'], 1, current['projection']['month']+1, current['projection']['year'])
    printProjection(last)

    for m in range(5,13):
        last = ps.getProjectionByMonth(last['finalAmount'], 1, m, 2016)
        printProjection(last)

    for m in range(1,13):
        last = ps.getProjectionByMonth(last['finalAmount'], 1, m, 2017)
        printProjection(last)
