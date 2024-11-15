# Named Range Google Sheets Program

This Python program interacts with Google Sheets to create and manage named ranges using the `gspread` library. The program includes functionality to handle specific scenarios, such as managing named ranges when a sheet is manually deleted in Google Sheets, which can lead to errors due to orphaned `#REF` named ranges.

## Features

- Creates a Google Sheet and adds named ranges to a specified worksheet.
- Checks for existing named ranges and deletes them if they are duplicates or references (`#REF`) due to manually deleted sheets.
- Automatically handles the creation of a new Google Sheet or opens an existing one by name.
- Includes a set of unit tests to validate each functionality in the program.

## Purpose

The purpose of this program is to automate the creation and management of named ranges in Google Sheets, and to handle potential errors caused by orphaned named ranges. If a Google Sheet is deleted manually, any named ranges associated with that sheet may remain, resulting in `#REF` errors. This program aims to identify and manage these cases gracefully.

## Requirements

- Python 3.10+
- Google Sheets API credentials (stored as a service account JSON)

## Setup

1. **Clone this repository**:
   ```bash
   git clone https://github.com/makubexD/namedRangesGSBug
   cd namedRangesGSBug
   code .
   ```

2. **Install Dependencies**

    Ensure you have `pip` installed, then install the required libraries listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file includes the following libraries:
    - **gspread**: For accessing and interacting with Google Sheets.
    - **google-auth**: For handling authentication using a Google service account.
    - **pytest**: For testing the functionality of the program.
    - **pytest-mock** (optional): Provides support for mocking during tests.
3. **Google API Setup**

    To interact with Google Sheets, you need to set up the Google Sheets API and create a service account.

    - **Enable the Google Sheets API**:
        - Go to the [Google Cloud Console](https://console.cloud.google.com/).
        - Create a new project (or use an existing one).
        - Enable the Google Sheets API for your project.

    - **Create a Service Account**:
        - In the Google Cloud Console, go to **IAM & Admin** > **Service Accounts**.
        - Create a new service account and download the JSON credentials file.

    - **Share Access to the Google Sheet**:
        - Open the target Google Sheet in your Google Drive.
        - Share it with the service account email (found in the JSON credentials file) and give it **Editor** permissions.
4. **Configure Constants**

    Update the `constants.py` file to include your Google Sheets credentials and folder ID.

    - **GSHEET_CREDENTIALS**: Store your Google Sheets API credentials as a JSON string or dictionary.
    - **GSHEET_FOLDER_ID**: Set this to the Google Drive folder ID where the sheets will be created.

    The `constants.py` file should look something like this:

    ```python
    GSHEET_CREDENTIALS = '''
    {
        "type": "service_account",
        "project_id": "your_project_id",
        "private_key_id": "your_private_key_id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
        "client_email": "your_service_account_email",
        "client_id": "your_client_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your_service_account_email"
    }
    '''

## Usage

To run the main program, which creates a Google Sheet, adds a worksheet, and sets up named ranges, use:

```bash
python main.py
```

### Expected Workflow

1. The program will open or create a Google Sheet with the specified name.
2. It will add a worksheet with static data if it doesn’t already exist.
3. Named ranges will be set up in the worksheet, checking for and deleting any pre-existing named ranges with `#REF` errors or duplicates.

## Testing

This project uses `pytest` for testing. All test files are located in the `tests/` directory.

### Running Tests

To run all tests, execute `pytest` in the command line. This command will automatically discover and run all test files prefixed with `test_` or suffixed with `_test.py` within the `tests` directory.

## Troubleshooting Common Issues

1. **Empty Array when Listing Named Ranges**:
- When a sheet is deleted manually, the named ranges associated with it may still be present but inaccessible through the API, returning an empty array.
- This program is designed to detect and handle these cases, but if issues persist, ensure that all sheets and named ranges are properly synchronized.

2. **Invalid Named Range Error (`#REF`)**:
- If a named range contains `#REF`, it may cause errors during subsequent operations. Ensure that named ranges are checked and deleted if they are not associated with valid cells.

3. **Google Sheets API Access Error**:
- If you encounter an API access error, verify that:
  - The service account email has edit access to the target Google Sheet.
  - The credentials are correctly stored in `constants.py`.

## Contribution Guidelines

If you’d like to contribute to this project:

1. **Fork the repository**.
2. **Create a new branch** with your feature or bug fix.
3. **Ensure all tests pass** and add new tests if applicable.
4. **Submit a pull request** for review.

Contributions are welcome and appreciated!
