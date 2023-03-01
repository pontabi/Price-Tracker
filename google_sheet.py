import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:
    def __init__(self):
        # --------- Authorize Google Sheets API --------- #
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
            ]
        file_name = 'Your json google cloud client key file'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
        client = gspread.authorize(creds)

        # --------- Fetch the sheet --------- #
        sheet = client.open('Price Tracker Target Data').sheet1
        python_sheet = sheet.get_all_records()
        self.records = python_sheet

