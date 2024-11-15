# ***************  IMPORTANT ***************
# ***************  IMPORTANT ***************
# ***************  IMPORTANT ***************
# If you face any issue by importing private key replace \n by \\n  that should fix the issue
# If you face any issue by importing private key replace \n by \\n  that should fix the issue
# If you face any issue by importing private key replace \n by \\n  that should fix the issue
# ***************  IMPORTANT ***************
# ***************  IMPORTANT ***************
# ***************  IMPORTANT ***************

GSHEET_CREDENTIALS = '''
{
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "your-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\\nYOUR-PRIVATE-KEY\\n-----END PRIVATE KEY-----\\n",
    "client_email": "your-service-account-email",
    "client_id": "your-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/YOUR-SERVICE-ACCOUNT-EMAIL"
}
'''
GSHEET_FOLDER_ID = 'INSERT FOLDER ID WHERE FILE WILL BE LOCATED, USUALLY IS WHAT IS NEXT TO https://drive.google.com/drive/folders/.......'
SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']