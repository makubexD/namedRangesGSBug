import pytest
from google_sheets_service import SimpleGoogleSheetsService
import gspread
from unittest.mock import patch

@pytest.fixture
def sheets_service():
    """Fixture for initializing SimpleGoogleSheetsService."""
    with patch('google_sheets_service.gspread.authorize') as mock_auth:
        mock_gc = mock_auth.return_value
        service = SimpleGoogleSheetsService()
        service.gc = mock_gc
        yield service
