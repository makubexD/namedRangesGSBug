import pytest
import gspread 
from unittest.mock import MagicMock, patch

def test_open_or_create_spreadsheet_existing(sheets_service):
    """Test opening an existing spreadsheet."""
    sheets_service.gc.list_spreadsheet_files.return_value = [{'name': 'TestSheet'}]
    sheets_service.gc.open.return_value = 'Mocked Spreadsheet'
    
    with patch('google_sheets_service.GSHEET_FOLDER_ID', 'mock_folder_id'):
        spreadsheet = sheets_service.open_or_create_spreadsheet('TestSheet')
        sheets_service.gc.open.assert_called_once_with('TestSheet')
        assert spreadsheet == 'Mocked Spreadsheet'

def test_open_or_create_spreadsheet_new(sheets_service):
    """Test creating a new spreadsheet when it doesn't exist."""
    sheets_service.gc.list_spreadsheet_files.return_value = []
    sheets_service.gc.create.return_value = 'New Mocked Spreadsheet'
    
    with patch('google_sheets_service.GSHEET_FOLDER_ID', 'mock_folder_id'):
        spreadsheet = sheets_service.open_or_create_spreadsheet('NewSheet')
        sheets_service.gc.create.assert_called_once_with('NewSheet', folder_id='mock_folder_id')
        assert spreadsheet == 'New Mocked Spreadsheet'

def test_add_worksheet_with_static_data_existing(sheets_service):
    """Test updating an existing worksheet with static data."""
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.worksheet.return_value = MagicMock()
    worksheet = sheets_service.add_worksheet_with_static_data(mock_spreadsheet, worksheet_name="StaticDataSheet")
    mock_spreadsheet.worksheet.assert_called_once_with("StaticDataSheet")
    worksheet.update.assert_called_once_with('A1', [['Header1', 'Header2'], [1, 2], [3, 4]])

def test_add_worksheet_with_static_data_new(sheets_service):
    """Test creating a new worksheet and adding static data."""
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.worksheet.side_effect = gspread.exceptions.WorksheetNotFound  # Use gspread exception here
    mock_worksheet = mock_spreadsheet.add_worksheet.return_value
    worksheet = sheets_service.add_worksheet_with_static_data(mock_spreadsheet, worksheet_name="StaticDataSheet")
    mock_spreadsheet.add_worksheet.assert_called_once_with(title="StaticDataSheet", rows=10, cols=10)
    mock_worksheet.update.assert_called_once_with('A1', [['Header1', 'Header2'], [1, 2], [3, 4]])

def test_delete_existing_named_ranges(sheets_service):
    """Test deleting existing named ranges."""
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.list_named_ranges.return_value = [
        {'name': 'Range1', 'namedRangeId': 'id1'},
        {'name': 'Range2', 'namedRangeId': 'id2'}
    ]
    sheets_service.delete_existing_named_ranges(mock_spreadsheet, ['Range1', 'Range2'])
    mock_spreadsheet.batch_update.assert_called_once_with({
        "requests": [
            {"deleteNamedRange": {"namedRangeId": 'id1'}},
            {"deleteNamedRange": {"namedRangeId": 'id2'}}
        ]
    })

def test_setup_named_ranges(sheets_service):
    """Test creating new named ranges after deleting existing ones."""
    mock_spreadsheet = MagicMock()
    mock_worksheet = MagicMock()
    mock_worksheet._properties = {'sheetId': 'sheet_id'}
    
    # Mock delete_existing_named_ranges to skip actual deletion
    with patch.object(sheets_service, 'delete_existing_named_ranges') as mock_delete:
        sheets_service.setup_named_ranges(mock_spreadsheet, mock_worksheet)
        mock_delete.assert_called_once_with(mock_spreadsheet, ['Range1', 'Range2'])
        mock_spreadsheet.batch_update.assert_called_once_with({
            "requests": [
                {
                    "addNamedRange": {
                        "namedRange": {
                            "name": "Range1",
                            "range": {
                                "sheetId": 'sheet_id',
                                "startRowIndex": 1,
                                "endRowIndex": 2,
                                "startColumnIndex": 0,
                                "endColumnIndex": 2
                            }
                        }
                    }
                },
                {
                    "addNamedRange": {
                        "namedRange": {
                            "name": "Range2",
                            "range": {
                                "sheetId": 'sheet_id',
                                "startRowIndex": 2,
                                "endRowIndex": 3,
                                "startColumnIndex": 0,
                                "endColumnIndex": 2
                            }
                        }
                    }
                }
            ]
        })

def test_setup_sheet_with_data_and_ranges(sheets_service):
    """Test the full workflow of setting up a sheet with data and named ranges."""
    mock_spreadsheet = MagicMock()
    sheets_service.open_or_create_spreadsheet = MagicMock(return_value=mock_spreadsheet)
    sheets_service.add_worksheet_with_static_data = MagicMock(return_value='Mock Worksheet')
    sheets_service.setup_named_ranges = MagicMock()

    sheets_service.setup_sheet_with_data_and_ranges("TestSheet")
    sheets_service.open_or_create_spreadsheet.assert_called_once_with("TestSheet")
    sheets_service.add_worksheet_with_static_data.assert_called_once_with(mock_spreadsheet, worksheet_name="StaticDataSheet")
    sheets_service.setup_named_ranges.assert_called_once_with(mock_spreadsheet, 'Mock Worksheet')
