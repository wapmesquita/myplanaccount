import json
from handler import request_handler, http_handler
from helper import projection_helper, spreadsheet_helper, last_projection_helper
from gac import oauth_checker
import datetime

class CurrentProjectionService(request_handler.Request):

    @request_handler.json
    def get(self):
        projectionHelper = projection_helper.ProjectionHelper()
        return projectionHelper.getCurrentMonthProjection()


class ProjectionByMonthService(request_handler.Request):

    @request_handler.json
    def get(self):
        projectionHelper = projection_helper.ProjectionHelper()
        initial_amount=self.param('initial_amount')
        if initial_amount == '':
            initial_amount = 0
        else:
            initial_amount=float(initial_amount)
        start_dayOfMonth=int(self.param('start_dayOfMonth'))
        month=int(self.param('month'))
        year=int(self.param('year'))
        return projectionHelper.getProjectionByMonth(initial_amount, start_dayOfMonth, month, year)

class LastProjectionRequestedService(request_handler.Request):

    @request_handler.json
    def get(self):
        return last_projection_helper.LastProjectionHelper().load()

class ProjectionFromTodayToMonthService(request_handler.Request):

    @request_handler.json
    def get(self):
        end_month=int(self.param('month'))
        end_year=int(self.param('year'))

        credentials = oauth_checker.getCredentials(self.request.cookies)

        db = spreadsheet_helper.SpreadsheetHelper(key=self.param('sht_key'), creds=credentials)
        ps = projection_helper.ProjectionHelper(db);

        return ps.projectFromNowTo(end_month, end_year)
