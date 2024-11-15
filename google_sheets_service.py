import gspread
from google.oauth2.service_account import Credentials
import json
from constants import GSHEET_CREDENTIALS, SCOPE, GSHEET_FOLDER_ID

class SimpleGoogleSheetsService:
    def __init__(self):
        self.credentials = self.load_credentials()
        self.gc = gspread.authorize(self.credentials)

    def load_credentials(self):
        credentials_dict = json.loads(GSHEET_CREDENTIALS)
        return Credentials.from_service_account_info(credentials_dict, scopes=SCOPE)

    def open_or_create_spreadsheet(self, sheet_name):
        existing_spreadsheets = self.gc.list_spreadsheet_files(folder_id=GSHEET_FOLDER_ID)
        spreadsheet_exists = any(sheet_name == sheet['name'] for sheet in existing_spreadsheets)

        if spreadsheet_exists:
            print(f"Spreadsheet '{sheet_name}' found. Opening existing spreadsheet.")
            return self.gc.open(sheet_name)
        else:
            print(f"Spreadsheet '{sheet_name}' not found. Creating a new spreadsheet.")
            return self.gc.create(sheet_name, folder_id=GSHEET_FOLDER_ID)

    def add_worksheet_with_static_data(self, spreadsheet, worksheet_name="StaticDataSheet"):
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            print(f"Worksheet '{worksheet_name}' found. Updating existing worksheet.")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=10, cols=10)
            print(f"Worksheet '{worksheet_name}' created.")

        worksheet.update('A1', [['Header1', 'Header2'], [1, 2], [3, 4]])
        print(f"Static data added to the worksheet '{worksheet_name}'.")
        return worksheet

    def delete_existing_named_ranges(self, spreadsheet, range_names):
        """Delete named ranges with specified names if they already exist."""
        existing_named_ranges = spreadsheet.list_named_ranges()
        update_requests = []

        for named_range in existing_named_ranges:
            if named_range['name'] in range_names:
                delete_request = {
                    "deleteNamedRange": {
                        "namedRangeId": named_range['namedRangeId']
                    }
                }
                update_requests.append(delete_request)
                print(f"Deleting existing named range: {named_range['name']}")

        if update_requests:
            spreadsheet.batch_update({"requests": update_requests})

    def setup_named_ranges(self, spreadsheet, worksheet):
        sheet_id = worksheet._properties['sheetId']
        range_definitions = [
            {
                "name": "Range1",
                "startRowIndex": 1,
                "endRowIndex": 2,
                "startColumnIndex": 0,
                "endColumnIndex": 2
            },
            {
                "name": "Range2",
                "startRowIndex": 2,
                "endRowIndex": 3,
                "startColumnIndex": 0,
                "endColumnIndex": 2
            }
        ]
        
        range_names = [range_def["name"] for range_def in range_definitions]
        self.delete_existing_named_ranges(spreadsheet, range_names)
        
        update_requests = []
        for range_def in range_definitions:
            named_range_request = {
                "addNamedRange": {
                    "namedRange": {
                        "name": range_def["name"],
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": range_def["startRowIndex"],
                            "endRowIndex": range_def["endRowIndex"],
                            "startColumnIndex": range_def["startColumnIndex"],
                            "endColumnIndex": range_def["endColumnIndex"]
                        }
                    }
                }
            }
            update_requests.append(named_range_request)

        spreadsheet.batch_update({"requests": update_requests})
        print(f"Named ranges created: {', '.join([r['name'] for r in range_definitions])}")

    def setup_sheet_with_data_and_ranges(self, sheet_name):
        spreadsheet = self.open_or_create_spreadsheet(sheet_name)
        worksheet = self.add_worksheet_with_static_data(spreadsheet, worksheet_name="StaticDataSheet")
        self.setup_named_ranges(spreadsheet, worksheet)
