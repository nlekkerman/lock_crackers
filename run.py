import os
import random
import time
import shutil
from colorama import init, Fore, Back, Style
import gspread
from google.oauth2.service_account import Credentials

init()
def print_colored_title_centered(text, colors, background_color, top_padding=2, bottom_padding=2):
    """
    Print a title with multicolored letters and background, centered horizontally.

    Parameters:
    text (str): The title text to be printed.
    colors (list): A list of foreground colors for each character in the text.
    background_color (int): The background color code (0-255) for the background (e.g., 231 for white).
    top_padding (int): The number of lines of padding to add above the text (default is 1).
    bottom_padding (int): The number of lines of padding to add below the text (default is 1).
    """
    terminal_width = shutil.get_terminal_size().columns
    left_padding = (terminal_width - len(text)) // 2
    
    # Print top padding
    print("\n" * top_padding, end="")
    
    # Print top white background
    print('\033[48;5;231m' + ' ' * terminal_width)
    
    # Print the colored text with background
    print(' ' * left_padding, end=" ")
    for char, color in zip(text, colors):
        print(f"\033[1m\033[38;5;{color}m\033[48;5;{background_color}m" + char, end="")
    print(' ' * left_padding + '\033[0m')
    
    # Print bottom white background
    print('\033[48;5;231m' + ' ' * terminal_width)
    
   

input_string = "??? LOCK CRACKERS ???"
colors = [196, 46, 33, 226, 201, 51] * ((len(input_string) // 6) + 1)  # ANSI color codes for Red, Green, Blue, Yellow, Magenta, Cyan
background_color = 231  # ANSI color code for White
print_colored_title_centered(input_string, colors, background_color, top_padding=2, bottom_padding=2)


def print_colored_background_centered(text, foreground_color, background_color):
    """
    Print text with colored foreground and background, centered horizontally.

    Parameters:
    text (str): The text to be printed.
    foreground_color (str): The foreground color (e.g., 'WHITE', 'GREEN', etc. from colorama).
    background_color (str): The background color (e.g., 'WHITE', 'GREEN', etc. from colorama).
    """
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    print(f"{Style.BRIGHT}{foreground_color}{background_color}{' ' * padding}{text}{' ' * padding}{Style.RESET_ALL}")

def validate_name_country(input_string):
    """
    Validates whether the input string contains only alphabetic characters"
    " or spaces.

    Parameters:
    input_string (str): The string to be validated.

    Returns:
    bool: True if all characters in the input string are alphabetic or spaces,"
    " False otherwise.
    """
    return all(char.isalpha() or char.isspace() for char in input_string)


def validate_game_mode(mode):
    """
    Validate the game mode.

    Parameters:
    mode (str): The game mode to validate.

    Returns:
    bool: True if the mode is valid ('C', 'E', or 'H'), False otherwise.
    """
    return mode in ['C', 'E', 'H']


def validate_password(input_string, mode):
    """
    Validate the password input based on the difficulty level.

    Parameters:
    - input_string (str): The password input to be validated.
    - mode (str): The difficulty level of the password validation ('C' for Easy, 'E' for Medium, 'H' for Hard).

    Returns:
    - bool: True if the password input is valid according to the specified difficulty level, False otherwise.
    """
    if mode == 'C':
        return all(char.isdigit() and int(char) <= 3 for char in input_string.strip().split())
    if mode == 'E':
        return all(char.isdigit() and int(char) <= 5 for char in input_string.strip().split())
    if mode == 'H':
        return all(char.isdigit() and int(char) <= 9 for char in input_string.strip().split())
    return False


def clear_screen():
    """
    Clears the terminal screen.
    """
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')


def validate_confirmation_input(input_string):
    """
    Validate whether the input string is either 'y' or 'n'.

    Parameters:
    input_string (str): The input string to be validated.

    Returns:
    bool: True if the input string is 'y' or 'n', False otherwise.
    """
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


# Print the colored text centered horizontally on a white background
print()
print_colored_background_centered("Welcome to the Password Guessing Game!", Fore.WHITE, Back.BLUE)
print()
print("Rules:")
print("- You need to guess a password, which consists of 6 numbers.")
print("- The numbers in the password are within a specific range depending on the difficulty level:")
print("  - For 'C' (Child) mode, the numbers range from 0 to 3.")
print("  - For 'E' (Easy) mode, the numbers range from 0 to 5.")
print("  - For 'H' (Hard) mode, the numbers range from 0 to 9.")
print("- Each '??' represents one number from the corresponding range.")
print("- Your task is to guess the password by entering 6 numbers.")
print("- If your guess contains the correct number at the correct position, it will be revealed.")
print("- For example, if the password is '123456' and your guess is '143256',")
print("  the revealed password will be '1*3*5*'.")
print("- Use the revealed parts of the password to make subsequent guesses.")
print("- Keep guessing until you reveal the entire password.")
print()

# Get player's name
while True:
    player_name = input("What's your name? ")
    if validate_name_country(player_name):
        break
    print(Fore.RED + "Please enter a valid name with only letters from 'a' to 'z'." + Fore.RESET)

# Get player's country
while True:
    player_country = input("Where are you from? ")
    if validate_name_country(player_country):
        break
    print(Fore.RED + "Please enter a valid country with only letters from 'a' to 'z'." + Fore.RESET)


# Display welcome message
print(f"Welcome, {player_name} from {player_country}!")

# Ask for game mode and start the timer
start_time = time.time()
while True:
    user_mode = input("Choose the game mode - 'C' for child, 'E' for easy, or 'H' for hard: ").strip().upper()

    if validate_game_mode(user_mode):
        break
    print(Fore.RED + "Invalid input. Please enter 'C', 'E', or 'H'." + Fore.RESET)


# Generate a random password based on game mode
if user_mode == 'C':
    password = [random.randint(0, 3) for _ in range(6)]
    DIFFICULTY_RANGE = '0-3'
elif user_mode == 'E':
    password = [random.randint(0, 5) for _ in range(6)]
    DIFFICULTY_RANGE = '0-5'
elif user_mode == 'H':
    password = [random.randint(0, 9) for _ in range(6)]
    DIFFICULTY_RANGE = '0-9'

clear_screen()

hidden_password = ['?' for _ in range(6)]


print()
print()



# Main game loop
while True:
    GAME_OUTCOME = 'Ongoing'
    # Reset correct_numbers for each guess
    CORRECT_NUMBERS = 0
    correct_positions = []  # List to store positions of correct numbers

    # Display hidden password
    TERMINAL_WIDTH = 80
    hidden_password_str = " ".join(str(x) for x in hidden_password)
    padding = " " * ((TERMINAL_WIDTH - len(hidden_password_str)) // 2)
    print(padding + "\033[1m" + hidden_password_str + "\033[0m")

    # Get user's guess
    guess = input("Enter your guess (6 numbers separated by spaces, or press 'q' to quit): ").strip()

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
                    GAME_OUTCOME = 'Quit'
                    break
                if confirm_quit == 'n':
                    break
            else:
                print(Fore.RED + "Invalid input. Please enter 'Y' or 'N'." + Fore.RESET)
        if GAME_OUTCOME == 'Quit':
            break
        continue

    # Check if the guess has 6 numbers
    guess_list = guess.split()
    if len(guess_list) != 6:
        print(Fore.RED + "Please enter 6 numbers or 'q' to quit." + Fore.RESET)
        continue

    # Validate the password input based on difficulty level
    if not validate_password(guess, user_mode):
        print(Fore.RED + f"Please enter valid numbers within the difficulty range {DIFFICULTY_RANGE}." + Fore.RESET)
        continue

    # Convert the guess to integers
    guess = [int(x) for x in guess_list]

    # Check the guess against the password
    for i in range(6):
        if guess[i] == password[i]:
            hidden_password[i] = str(password[i])
            CORRECT_NUMBERS += 1
            correct_positions.append(i + 1)

    if CORRECT_NUMBERS == 6:
        print("Congratulations! You guessed the password correctly!")
        GAME_OUTCOME = 'Won'
        break
    else:
        print("Incorrect guess. Try again.")
        if correct_positions:
            print(f"Correct number/s found at position/s: {', '.join(map(str, correct_positions))}")
        else:
            print("No correct number found. Try again.")
        GAME_OUTCOME = 'Lost'

# Stop stopwatch
end_time = time.time()
elapsed_time = round(end_time - start_time, 1)
print(f"Elapsed time: {int(elapsed_time)} seconds")

# Saving player's information and game outcome to Google Sheets
if GAME_OUTCOME != 'Quit':
    player_info = [player_name, player_country, user_mode, GAME_OUTCOME, elapsed_time]
    worksheet.append_row(player_info)


# Printing the leaderboard based on the best times of players
print("Leaderboard (Sorted by Best Time):")
print("Name        Country      Level     Status    Time")
leaderboard_data = worksheet.get_all_values()[1:]
leaderboard_data.sort(key=lambda x: float(x[-1]))

for i, row in enumerate(leaderboard_data):
    if i == 0:
        medal_color = Fore.YELLOW  # Gold for first place
    elif i == 1:
        medal_color = Fore.CYAN  # Silver for second place
    elif i == 2:
        medal_color = Fore.RED  # Bronze for third place
    else:
        medal_color = Fore.RESET  # Reset color for other positions

    print(f"{medal_color}{row[0]:<10} {row[1]:<14} {row[2]:<8} {row[3]:<8} {row[4]}")

