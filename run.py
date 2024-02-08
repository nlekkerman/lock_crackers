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

# Function to validate password input based on difficulty level
def validate_password(input_string, mode):
    if mode == 'C':
        return all(char.isdigit() and int(char) <= 3 for char in input_string.strip().split())
    elif mode == 'E':
        return all(char.isdigit() and int(char) <= 5 for char in input_string.strip().split())
    elif mode == 'H':
        return all(char.isdigit() and int(char) <= 9 for char in input_string.strip().split())
    else:
        return False

# Function to validate confirmation input
def validate_confirmation_input(input_string):
    return input_string.lower() in ['y', 'n']

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
    
hidden_password = ['?' for _ in range(6)]

# Main game loop
while True:
    # Display hidden password
    print(" ".join(str(x) for x in hidden_password))

    # Get user's guess
    guess = input(f"Enter your guess (6 numbers separated by spaces, or press 'q' to quit): ").strip()

    # Check if user wants to quit
    if guess.lower() == 'q':
        while True:
            confirm_quit = input("Are you sure you want to quit? (Y/N): ").strip().lower()
            if validate_confirmation_input(confirm_quit):
                if confirm_quit == 'y':
                    end_time = time.time()
                    elapsed_time = round(end_time - start_time, 1)
                    print(f"Elapsed time: {int(elapsed_time)} seconds")
                    print("The password was:", " ".join(str(x) for x in password))
                    break
                elif confirm_quit == 'n':
                    break
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
        if confirm_quit == 'y':
            break
        else:
            continue

    # Check if the guess has 6 numbers
    guess_list = guess.split()
    if len(guess_list) != 6:
        print("Please enter 6 numbers or 'q' to quit.")
        continue

    # Validate the password input based on difficulty level
    if not validate_password(guess, mode):
        print(f"Please enter valid numbers within the difficulty range {difficulty_range}.")
        continue

    # Convert the guess to integers
    guess = [int(x) for x in guess_list]

    # Check the guess against the password
    correct_numbers = 0
    for i in range(6):
        if guess[i] == password[i]:
            hidden_password[i] = str(password[i])
            correct_numbers += 1

    if correct_numbers == 6:
        print("Congratulations! You guessed the password correctly!")
        game_outcome = 'Won'
        break
    else:
        print("Incorrect guess. Try again.")
        game_outcome = 'Lost'
