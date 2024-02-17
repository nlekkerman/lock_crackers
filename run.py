"""
Module: lock_cracker_game

This module contains functions related to the Lock Cracker game.
"""
import os
import random
import shutil
import time
from colorama import init, Fore, Back, Style
import gspread
from google.oauth2.service_account import Credentials

init(autoreset=True)
TERMINAL_WIDTH = 113

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


def validate_confirmation_input(input_string):
    """
    Validate whether the input string is either 'y' or 'n'.

    Parameters:
    input_string (str): The input string to be validated.

    Returns:
    bool: True if the input string is 'y' or 'n', False otherwise.
    """
    return input_string.lower() in ['y', 'n']


def validate_game_mode(mode):
    """
    Validate the game mode.

    Parameters:
    mode (str): The game mode to validate.

    Returns:
    bool: True if the mode is valid ('C', 'E', or 'H'), False otherwise.
    """
    return mode in ['C', 'E', 'H']


def print_congratulations_text(text, background_color=None):
    """
    Print the text "Congratulations!" with each letter in a different color.

    Args:
        text (str): The text to print.

    Returns:
        None
    """
    colors = [
        Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    centered_text = text.center(TERMINAL_WIDTH)
    colored_text = ""
    for insx, char in enumerate(centered_text):
        colored_text += f"{colors[insx % len(colors)]}{char}"
    # Apply background color if provided
    if background_color:
        print(f"{background_color}{colored_text}{Style.RESET_ALL}")
    else:
        print(colored_text)


def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def print_welcome_message():
    """
    Prints a welcome message for the Lock Cracker game with colored letters.

    This function retrieves the terminal width,"
    " creates a centered welcome message,
    and prints it with colored background.

    Returns:
        None
    """
    terminal_width = shutil.get_terminal_size().columns
    welcome_text = "Welcome to the Lock Cracker game!"
    centered_welcome_text = welcome_text.center(terminal_width)
    print(
        f"\033[43m{'=' * terminal_width}\033[0m" +
        f"\033[43m{centered_welcome_text}\033[0m" +
        f"\033[43m{'=' * terminal_width}\033[0m"
    )


def print_title():
    """
    Prints a welcome message for the Lock Cracker game with colored letters.

    This function retrieves the terminal width,"
    " creates a centered welcome message,
    and prints it with colored background.

    Returns:
        None
    """
    init(autoreset=True)
    terminal_width = shutil.get_terminal_size().columns
    welcome_text = "???Lock Crackers???"
    centered_welcome_text = welcome_text.center(terminal_width)
    line = " " * terminal_width
    print(
        f"{Back.BLACK}{line}",
        f"{Back.WHITE}{Fore.RED}{centered_welcome_text}{Style.RESET_ALL}",
        f"{Back.BLACK}{line}",
        sep="\n"
    )


def print_input_instructions(instructions, color=Fore.WHITE):
    """
    Print input instructions with a specified color.

    Args:
        instructions (str): The instructions to be displayed.
        color (str, optional): The color of the instructions."
        " Defaults to Fore.MAGENTA.

    Returns:
        None
    """
    print(
        f"{Back.RED}{Fore.WHITE}{color}{' ' * 3} "
        f"{instructions.center(len(instructions) + 6)}"
        f"{' ' * 3}{Fore.RESET}{Back.RESET}"
    )


def get_input_password(input_message, color):
    """
    Get input from the user.

    Args:
        input_message (str): The message prompt.
        color (str): The color of the prompt.

    Returns:
        str: The user input.
    """

    while True:
        

        password_instructions_message = "Enter your password guess, 6 numbers separated by space or Q for quit! "
        print_input_instructions(password_instructions_message, Fore.WHITE)
        user_input = input(f"{color}{input_message} {Fore.GREEN}")
        if user_input.lower() == 'q':
            return 'q'
        if user_input and all(
            char.isdigit() or char.isspace() for char in user_input
        ):
            return user_input

        # Print the centered message
        message_invalid_input = "Invalid input. Please enter only numbers and spaces, or 'q' to quit."
        padding_inv_inp = (TERMINAL_WIDTH - len(MESSAGE)) // 2
        centered_invalid_input = (
                f"{' ' * padding_inv_inp}"  # Left padding
                f"{Fore.WHITE}"        # Red color
                f"{message_invalid_input}"         # Message content
                f"{Fore.RESET}"      # Reset color
                f"{' ' * padding_inv_inp}"   # Right padding
            )
        clear_screen()

        print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
        print(centered_invalid_input)

        # Print empty red line below the message
        print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
        print()

        print_password(HIDDEN_PASSWORD_STRING)


def get_input(input_message, color):
    """
    Get input from the user.

    Args:
        input_message (str): The message prompt.
        color (str): The color of the prompt.

    Returns:
        str: The user input.
    """
    while True:
        user_input = input(f"{color}{input_message}{Fore.GREEN} ")
        if user_input and all(
            char.isalpha() or char.isspace() for char in user_input
        ):
            return user_input
        print(Fore.RED + "Invalid input. Please enter only letters and spaces. " + Fore.RESET)


def print_centered_text(text, color):
    """
    Print centered text with specified color.

    Args:
        text (str): The text to be centered and printed.
        color (str): The color of the text.

    Returns:
        None
    """
    padding = (TERMINAL_WIDTH - len(text)) // 2
    print(f"{color}{' ' * padding}{text}{' ' * padding}{Style.RESET_ALL}")


def validate_password(input_string, mode):
    """
    Validate the password input based on the difficulty level.

    Parameters:
    - input_string (str): The password input to be validated.
    - mode (str): The difficulty level of the password validation "
    "('C' for Easy, 'E' for Medium, 'H' for Hard).

    Returns:
    - bool: True if the password input is valid according "
    "to the specified difficulty level, False otherwise.
    """
    if mode == 'C':
        return all(
            char.isdigit() and int(char) <= 3
            for char in input_string.strip().split()
        )
    if mode == 'E':
        return all(
            char.isdigit() and int(char) <= 5
            for char in input_string.strip().split()
        )
    if mode == 'H':
        return all(
            char.isdigit() and int(char) <= 9
            for char in input_string.strip().split()
        )
    return False


def print_game_rules():
    """
    Print the game rules with alternating colors.

    Returns:
        None
    """
    colors = [Fore.RED, Fore.BLUE]
    rules = [
        "- You need to guess a password, which consists of 6 numbers.",
        "- The numbers in the password are within a specific range "
        " depending on the difficulty level:",
        "  - For 'C' (Child) mode, the numbers range from 0 to 3.",
        "  - For 'E' (Easy) mode, the numbers range from 0 to 5.",
        "  - For 'H' (Hard) mode, the numbers range from 0 to 9.",
        "- Each '??' represents one number from the corresponding range.",
        "- Your task is to guess the password by entering 6 numbers.",
        "- If your guess contains the correct number at the correct position,"
        " it will be revealed.",
        "-Ensure that any numbers already revealed in previous guesses are "
        " entered in the correct position for each subsequent guess."
        "  For example, if the password is '123456'"
        " and your guess is '143256',",
        "  the revealed password will be '1*3*5*'.",
        "- Use the revealed parts of the password to make subsequent guesses.",
        "- Keep guessing until you reveal the entire password."
    ]

    for index, rule in enumerate(rules):
        color = colors[index % len(colors)]
        padding_rule = (TERMINAL_WIDTH - len(rule)) // 2
        centered_rule = f"{'' * padding_rule}{rule}{' ' * padding_rule}"
        print(f"{color}{Style.BRIGHT}{centered_rule}{Fore.RESET}{Back.RESET}")


def print_password(password_guess):
    """
    Print the hidden password with centered alignment.

    Args:
        password_guess (str): The hidden password to be printed.

    Returns:
        None
    """
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(password_guess)) // 2

    # Convert revealed numbers to green and question marks to red
    formatted_guess = ""
    for char in password_guess:
        if char.isdigit():
            formatted_guess += f"{Fore.GREEN}{char}"
        else:
            formatted_guess += f"{Fore.WHITE}{char}"
    print()
    print_congratulations_text("CRACK THIS PASSWORD", background_color=Back.BLACK)

    # Print the formatted password
    print(f"{Back.WHITE}{' ' * terminal_width}")
    print(
        f"{Back.BLACK}{Fore.WHITE}{' ' * padding}"
        F"{formatted_guess}{' ' * padding}"
        f"{Style.RESET_ALL}"
    )
    print(f"{Back.WHITE}{' ' * terminal_width}")


def choose_difficulty_level():
    """
    Ask the player to choose the difficulty level.

    Returns:
        str: The difficulty level chosen by the player.
    """
    while True:
        print_input_instructions("Choose difficulty level:", Fore.YELLOW)
        print_input_instructions("Enter 'C' for Child mode (0-3)")
        print_input_instructions("Enter 'E' for Easy mode (0-5)")
        print_input_instructions("Enter 'H' for Hard mode (0-9)")
        difficulty = get_input("Choose mode level:", Fore.YELLOW).upper()
        print(Style.RESET_ALL)
        if difficulty in ['C', 'E', 'H']:
            return difficulty
        print(f"{Fore.RED}Invalid input."
              " Please choose from 'C', 'E', or 'H'.{Style.RESET_ALL}")


print_welcome_message()


# Delay for 2 seconds
time.sleep(2)
# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Print the title
print("\033[1;37m" + " " * TERMINAL_WIDTH + "\033[0m")
print_title()
print("\033[1;37m" + " " * TERMINAL_WIDTH + "\033[0m")


print()


def main():
    """
    Main function to run the Lock Cracker game.
    """


# Set color and background for input instructions
INPUT_INSTRUCTIONS = "Enter your name:"

# Greeting the player with red background and white letters
print_input_instructions("Hi player, what is your name? ", )
player_name = get_input("Enter your name ", Fore.YELLOW)
clear_screen()
print_title()
print(Style.RESET_ALL)
print()

print_input_instructions("Where are you from?")
player_country = get_input("Your location: ", Fore.YELLOW)

clear_screen()
print_title()
print()  # Empty line

name_part = f"{Fore.YELLOW}{player_name}{Fore.RESET}"
country_part = (
    f"{Fore.RED} from{Fore.RESET} "
    f"{Fore.YELLOW}{player_country}{Fore.RESET}"
)

TERMINAL_WIDTH = 113
print(Back.WHITE + '=' * TERMINAL_WIDTH + Style.RESET_ALL)
print(Back.GREEN + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
print_congratulations_text("*||| WELCOME |||*", background_color=Back.BLACK)
print(Back.BLACK + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
print_congratulations_text(player_name, background_color=Back.BLACK)
print(Back.BLACK + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
print_congratulations_text("~ OF ~", background_color=Back.BLACK)
print(Back.BLACK + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
print_congratulations_text(player_country, background_color=Back.BLACK)
print(Back.GREEN + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
print(Back.WHITE + '=' * TERMINAL_WIDTH + Style.RESET_ALL)


time.sleep(3)

# Clear the screen again
clear_screen()

print_title()
print()
# Ask for game mode and start the timer
start_time = time.time()


while True:

    TEXT_TO_CENTER = "RULES:"
    CENTERED_TITLE = TEXT_TO_CENTER.center(TERMINAL_WIDTH)
    print_congratulations_text(CENTERED_TITLE)
    print_game_rules()
    print()

    print_input_instructions(
        "Choose the game mode - 'C' for child, "
        "'E' for easy, or 'H' for hard: ",
        color=Fore.WHITE
        )

    user_mode = get_input("Your level:", f"{Fore.YELLOW}").strip().upper()

    if validate_game_mode(user_mode):
        break
    print(
        Fore.RED + "Invalid input. Please enter 'C', 'E', or 'H'." + Fore.RESET
        )


# Generate a random password based on game mode
if user_mode == 'C':
    password = [random.randint(0, 3) for _ in range(6)]
    DIFFICULTY_RANGE = '0 - 3'
elif user_mode == 'E':
    password = [random.randint(0, 5) for _ in range(6)]
    DIFFICULTY_RANGE = '0 - 5'
elif user_mode == 'H':
    password = [random.randint(0, 9) for _ in range(6)]
    DIFFICULTY_RANGE = '0 - 9'

clear_screen()

hidden_password = ['?' for _ in range(6)]
correctly_guessed_positions = [False] * 6  # Track correctly guessed positions

# Main game loop
while True:
    GAME_OUTCOME = 'Ongoing'
    # Reset correct_numbers for each guess
    CORRECT_NUMBERS = 0
    correct_positions = []  # List to store positions of correct numbers

    # Display hidden password
    TERMINAL_WIDTH = 113
    HIDDEN_PASSWORD_STRING = " ".join(str(x) for x in hidden_password)

    print_password(HIDDEN_PASSWORD_STRING)

    print()
    print()
   
    # Get user's guess
    guess = get_input_password(
        "Your guess: ", f"{Fore.YELLOW}"
        ).strip()
    # Reset color
    clear_screen()

    # Check if user wants to quit
    if guess.lower() == 'q':
        while True:
            print()
            print(
                Back.RED + Fore.WHITE +
                "Are you sure you want to quit? (Y/N): "
                + Fore.RESET + Back.RESET)
            confirm_quit = input(
                Fore.YELLOW + "(Y/N): " + Fore.RESET + Back.RESET + Fore.GREEN
                ).strip().lower()
            print(Fore.RESET)
            if validate_confirmation_input(confirm_quit):
                if confirm_quit == 'y':
                    end_time = time.time()
                    elapsed_time = round(end_time - start_time, 1)
                    print(f"Elapsed time: {int(elapsed_time)} seconds")
                    print("The password was:"
                          "", " ".join(str(x) for x in password))
                    GAME_OUTCOME = 'Quit'
                    break
                if confirm_quit == 'n':
                    break
            clear_screen()
            print(Fore.RED + "Invalid input."
                  " Please enter 'Y' or 'N'." + Fore.RESET)

        if GAME_OUTCOME == 'Quit':
            break
        continue

    # Check if the guess has 6 numbers
    guess_list = guess.split()
    if len(guess_list) != 6:
        TERMINAL_WIDTH = 113
        # Print empty red lines above the message

        print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)

        # Print the centered message
        MESSAGE = "Please enter 6 numbers separated by space or 'q' to quit."
        padding = (TERMINAL_WIDTH - len(MESSAGE)) // 2
        centered_message = (
                f"{' ' * padding}"  # Left padding
                f"{Fore.WHITE}"        # Red color
                f"{MESSAGE}"         # Message content
                f"{Fore.RESET}"      # Reset color
                f"{' ' * padding}"   # Right padding
            )
        print(centered_message)

        # Print empty red line below the message
        print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
        print()
        continue

    # Validate the password input based on difficulty level
    if not validate_password(guess, user_mode):
        TERMINAL_WIDTH = 113

        # Print empty red lines above the message
        print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)

        # Print the centered message
        MESSAGE = (
            f"Enter valid numbers within the difficulty range: "
            f"{Fore.YELLOW} {DIFFICULTY_RANGE}{Fore.RESET}."
        )

        padding = (TERMINAL_WIDTH - len(MESSAGE)) // 2
        centered_message = (
            f"{' ' * padding}"  # Left padding
            f"{Fore.RED}"  # Red color
            f"{MESSAGE}"  # Message content
            f"{Fore.RESET}"  # Reset color
            f"{' ' * padding}"  # Right padding
        )
        print(centered_message)

        # Print empty red line below the message
        print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
        continue

    # Convert the guess to integers
    guess = [int(x) for x in guess_list]

    # Check if any number in the guess is,
    # already correctly guessed on the same position
    # Check if any number in the guess is already correctly guessed
    # Check if any revealed numbers are in the correct position,
    # but not yet revealed
    REVEALED_NUMBERS_IN_CORRECT_POSITION = False
    for i, digit in enumerate(guess):
        if correctly_guessed_positions[i] and digit != password[i]:
            TERMINAL_WIDTH = 113
            padding = (
                TERMINAL_WIDTH - len(f"Please enter {password[i]} for position {i + 1}")) // 2
            centered_message = (
                f"{Fore.RED}Please enter"
                f"{Fore.YELLOW} {password[i]}"
                f"{Fore.RED} on position"
                f"{Fore.YELLOW} {i + 1}"
                f"{Fore.RESET}"
            )

            # Print empty red line Above the message
            print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)

            print(' ' * padding + centered_message)
            # Print empty red line below the message
            print(Back.RED + ' ' * TERMINAL_WIDTH + Style.RESET_ALL)
            REVEALED_NUMBERS_IN_CORRECT_POSITION = True
            break
        # If there are revealed numbers in the correct
        # position but not yet revealed,
        # prompt the user to enter their guess again
        if REVEALED_NUMBERS_IN_CORRECT_POSITION:
            MESSAGE = ("Some revealed numbers are in the correct "
                       "position but not yet revealed. "
                       "Please enter your guess again.")
            print(MESSAGE)
            continue

# Restart the loop to prompt the user again
    else:
        # Check the guess against the password
        for i in range(6):
            if guess[i] == password[i]:
                hidden_password[i] = str(password[i])
                correctly_guessed_positions[i] = True
                CORRECT_NUMBERS += 1
                correct_positions.append(i + 1)

        if CORRECT_NUMBERS == 6:
            # Handling winning logic here
            # ...
            break

        # Check if there are revealed numbers but not in the correct positions
        if any(correctly_guessed_positions) and CORRECT_NUMBERS == 0:
            print("Revealed numbers are not in the correct positions.")
            print("Please try again.")
            continue  # Prompt user to guess again

        # Display incomplete guess message
        INCOPLETE_MESSAGE = "Keep trying until you crack them all..."
        TERMINAL_WIDTH = 113
        PADDING = (TERMINAL_WIDTH - len(INCOPLETE_MESSAGE)) // 2
        centered_incomplete_message = (
            f"{Fore.GREEN}{' ' * PADDING}"
            f"{INCOPLETE_MESSAGE}"
            f"{' ' * PADDING}{Style.RESET_ALL}"
        )
        print(centered_incomplete_message)

        # Display correct positions message
        if correct_positions:
            CORRECT_MESSAGE = "Correct number/s found at position/s:"
            CORRECT_POSITIONS_STRING = ', '.join(map(str, correct_positions))
            combined_message = f"{CORRECT_MESSAGE} {CORRECT_POSITIONS_STRING}"
            PADDING = (TERMINAL_WIDTH - len(combined_message)) // 2
            centered_correct_message = (
                f"{' ' * PADDING}"
                f"{combined_message}"
                f"{' ' * PADDING}")
            print(f"{Fore.YELLOW}{centered_correct_message}{Style.RESET_ALL}")

        GAME_OUTCOME = 'Lost'

# Stop stopwatch
end_time = time.time()
elapsed_time = round(end_time - start_time, 1)
TERMINAL_WIDTH = 113
print()
print()
print()
clear_screen()
print_title()
print()
print(Back.RESET)
TEXT_TO_CENTER = "LOCK CRACKER!"

# Calculate the centered text
CENTERED_TEXT = TEXT_TO_CENTER.center(TERMINAL_WIDTH)

# Print the centered text
print_congratulations_text(CENTERED_TEXT)
print()
TEXT_PASWORD_WAS_CENTER = "PASSWORD WAS:"

# Calculate the centered text
CENTERED_PASWORD_WAS_TEXT = TEXT_PASWORD_WAS_CENTER.center(TERMINAL_WIDTH)

# Print the centered text
print_congratulations_text(CENTERED_PASWORD_WAS_TEXT)
# Print the centered output line
print_congratulations_text(' '.join(str(x) for x in password))
print()  # Print an empty line after the centered output

# Saving player's information and game outcome to Google Sheets
if GAME_OUTCOME != 'Quit':
    player_info = [
        player_name, player_country, user_mode, GAME_OUTCOME, elapsed_time
        ]
    worksheet.append_row(player_info)


# Printing the leaderboard based on the best times of players
print("Leaderboard (Sorted by Best Time):")
print("Name        Country      Level     Status    Time")
leaderboard_data = worksheet.get_all_values()[1:]
leaderboard_data.sort(key=lambda x: float(x[-1]))

for i, row in enumerate(leaderboard_data[:10]):
    if i == 0:
        MEDAL_COLOR = Fore.YELLOW  # Gold for first place
    elif i == 1:
        MEDAL_COLOR = Fore.CYAN  # Silver for second place
    elif i == 2:
        MEDAL_COLOR = Fore.RED  # Bronze for third place
    else:
        MEDAL_COLOR = Fore.RESET  # Reset color for other positions

    print(
        f"{MEDAL_COLOR}{row[0]:<10} {row[1]:<14} {row[2]:<8} "
        f"{row[3]:<8} {row[4]}"
    )

if __name__ == "__main__":
    main()
