import gspread
from google.oauth2.service_account import Credentials
import random
import time


# Function to validate input
def validate_name_country(input_string):
    return all(char.isalpha() for char in input_string)

# Function to validate game mode input
def validate_game_mode(mode):
    return mode in ['C', 'E', 'H']

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

# Get player's name
while True:
    player_name = input("What's your name? ")
    if validate_name_country(player_name):
        break
    else:
        print("Please enter a valid name with only letters from 'a' to 'z'.")

# Get player's country
while True:
    player_country = input("Where are you from? ")
    if validate_name_country(player_country):
        break
    else:
        print("Please enter a valid country with only letters from 'a' to 'z'.")

# Display welcome message
print(f"Welcome, {player_name} from {player_country}!")

# Ask for game mode and start the timer
start_time = time.time()
while True:
    mode = input("Choose the game mode - 'C' for child, 'E' for easy, or 'H' for hard: ").strip().upper()
    if validate_game_mode(mode):
        break
    else:
        print("Invalid input. Please enter 'C', 'E', or 'H'.")
        
# Generate a random password based on game mode
if mode == 'C':
    password = [random.randint(0, 3) for _ in range(6)]
    difficulty_range = '0-3'
elif mode == 'E':
    password = [random.randint(0, 5) for _ in range(6)]
    difficulty_range = '0-5'
elif mode == 'H':
    password = [random.randint(0, 9) for _ in range(6)]
    difficulty_range = '0-9'