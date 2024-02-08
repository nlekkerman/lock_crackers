import gspread
from google.oauth2.service_account import Credentials



# Google Sheets credentials and API setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the specific spreadsheet
SPREADSHEET = 'lock_crackers'
SHEET = GSPREAD_CLIENT.open(SPREADSHEET)

# Specify the worksheet to use
WORKSHEET_NAME = 'info'
worksheet = SHEET.worksheet(WORKSHEET_NAME)

# Displaying rules
print("Welcome to the Password Guessing Game!")
print("Rules:")
print("- You need to guess a password which consists of 6 numbers.")
print("- Each '?' represents one number from 0 to 9.")
print("- You have to guess the password by entering 6 numbers.")
print("- If your guess matches the correct number, it will be revealed.")
print()