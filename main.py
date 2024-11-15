from google_sheets_service import SimpleGoogleSheetsService

if __name__ == "__main__":
    service = SimpleGoogleSheetsService()
    service.setup_sheet_with_data_and_ranges("namedRangeDemo")
