import gspread
from mock import mock_data
import os
from oauth2client.service_account import ServiceAccountCredentials
import json
import logging

class Spreadsheet():

    def __init__(self, credentials, url=None, key=None):
        self.worksheet_names = ['revenues', 'proportional_spends', 'recurrent_spends', 'spends', 'accounts', 'credit_cards', 'recurrent_investiments', 'investiments']
        self.full_json_loaded = False
        if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            self.loadMock()

        if not self.full_json_loaded:
            self.credentials = credentials
            gc = gspread.authorize(credentials)
            logging.info('Opening Spreadsheet')
            self.url = url
            if url is None and key is not None:
                self.url = 'https://docs.google.com/spreadsheets/d/' + key + '/edit'

            if self.url is not None:
                self.sht = gc.open_by_url(self.url)

    def loadMock(self):
        self.full_json_loaded = True
        self.json_data = mock_data.load()

    def getKey(self):
        return self.sht.get_id_fields()['spreadsheet_id']

    def getTitle(self):
        return self.sht.title

    def getJson(self):
        return self.json_data

    def getWorkSheetJson(self, wsht_name):
        logging.info('###### => Start parsing ' + wsht_name)
        if self.full_json_loaded:
            return self.json_data[wsht_name]

        json = []
        wsht = self.sht.worksheet(wsht_name)
        types = wsht.row_values(1)
        columns = wsht.row_values(2)
        rows = wsht.get_all_values()
        del rows[0]
        del rows[0]

        for row in rows:
            json.append(self.rowToJson(row, columns, types))
        return json

    def loadWholeJson(self):
        if self.full_json_loaded:
            return self.json_data
        self.json_data = {}
        for wsht_name in self.worksheet_names:
            self.json_data[wsht_name] = self.getWorkSheetJson(wsht_name)
        self.full_json_loaded = True

    def rowToJson(self, row, columns, types):
        col_num = 0
        obj = {}
        for column in columns:
            try:
                obj[column] = self.parseValue(row[col_num], types[col_num])
                col_num+=1
            except ValueError:
                logging.error('Error parsing col (' + str(col_num) + ') with value(' + row[col_num] + ')')
                raise

        return obj

    def parseValue(self, value, type):
        if value is None:
            return None
        if value.strip() == '':
            return None
        if type == 'int':
            return int(value)
        if type == 'float':
            return float(value.replace(',','.'))
        return value

    def _deleteWorkSheet(self, title):
        try:
            ws = self.sht.worksheet(title)
            self.sht.del_worksheet(ws)
        except Exception,e:
            logging.error(str(e))

    def _getMapRange(self, row_number, col_len):
        cols = 'ABCDEFGHIJKLMNOPQRSTUVXWYZ'
        return 'A' + str(row_number) + ':' + cols[col_len-1] + str(row_number)

    def _getWorksheet(self, title, cols):
        logging.info('Creating %s', title)
        error = True
        while error:
            try:
                return self.sht.add_worksheet(title=title, rows="100", cols=cols)
                error = False
            except Exception,e:
                str_error = str(e)
                logging.warn('Error getting worksheet')
                logging.warn(str_error)
                if 'Insira outro nome' in str_error:
                    self._deleteWorkSheet(title)

    def _getCellList(self, worksheet, range):
        logging.info('Getting Cells  from %s - %s', worksheet.title, range)
        error = True
        while error:
            try:
                return worksheet.range(range)
                error = False
            except Exception,e:
                logging.warn(str(e))
                logging.warn('Error getting cell list')

    def _updateCells(self, worksheet, cellList):
        logging.info('Updating cells')
        error = True
        while error:
            try:
                worksheet.update_cells(cellList)
                error = False
            except Exception,e:
                logging.warn(str(e))
                logging.warn('Error updating cell list')

    def createFromTemplate(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/template.json') as data_file:
            data = json.load(data_file)

        for i in data:
            ws = self._getWorksheet(i['title'], str(len(i['rows'][0])))
            row_number = 1

            for row in i['rows']:
                col_len = len(row)
                cell_list = self._getCellList(ws, self._getMapRange(row_number, col_len))
                col_number = 0

                for cell in cell_list:
                    cell.value = row[col_number]
                    col_number += 1

                self._updateCells(ws, cell_list)

                row_number += 1

def getOnlineTemplateToJson():
    scope = ['https://spreadsheets.google.com/feeds']
    creds_file = os.path.dirname(os.path.abspath(__file__)) + '/../credentials/service.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    gc = gspread.authorize(creds)
    url = 'https://docs.google.com/spreadsheets/d/13UDQ_kXzybroSIlMwNGqanh-i1xV5qDwsM9GbOK6OO8/edit'
    sht = gc.open_by_url(url)
    worksheet_list = sht.worksheets()
    json_template = []
    for ws in worksheet_list:
        print 'getting ', ws.title
        if ws.title == 'config':
            item = {'title':ws.title, 'rows':[ws.get_all_values()]}
        else:
            item = {'title':ws.title, 'rows':[ws.row_values(1), ws.row_values(2)]}
        json_template.append(item)

    return json_template

def saveOnlineTemplateInFile(file):
    with open(file, 'w') as outfile:
        json.dump(getOnlineTemplateToJson(), outfile)
