import tkinter as tk
from PIL import Image, ImageTk
import random
import time
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

# Create a list of questions
questions = [
    "Hello player, what is your name?",
    "Where are you from?",
    "Choose difficulty level: c for child, e for easy, and h for hard."
]

# Function to handle the input
def get_info(event=None):
    global current_question, name, place, difficulty, password, correct_guesses
    answer = info_entry.get().strip()
    if answer:
        if answer.lower() == 'q':
            confirm_quit()  # Trigger quit confirmation
            return  # Return to avoid further processing
        if current_question == 0:
            if answer.replace(" ", "").isalpha():
                name = answer
                message_label.config(text=f"Hi {name}, where are you from?")
                info_entry.delete(0, tk.END)  # Clear the input field
                current_question += 1
            else:
                message_label.config(text="Please enter a valid name.")
        elif current_question == 1:
            if answer.replace(" ", "").isalpha():
                place = answer
                message_label.config(text=f"Hi {name} from {place}, now choose difficulty level: c for child, e for easy, and h for hard.")
                info_entry.delete(0, tk.END)  # Clear the input field
                current_question += 1
            else:
                message_label.config(text="Please enter a valid place.")
        elif current_question == 2:
            if answer.lower() in ['c', 'e', 'h']:
                difficulty = answer.lower()
                password = generate_password(difficulty)
                message_label.config(text=f"Hi {name} from {place}, you chose difficulty level: {difficulty}.")
                info_entry.delete(0, tk.END)  # Clear the input field
                current_question += 1
                # Display the additional message and question marks for 3 seconds
                start_game()
            else:
                message_label.config(text="Please choose a valid difficulty level: c for child, e for easy, and h for hard.")
        elif current_question == 3:
            guess_password(answer)

# Function to confirm quitting the game
def confirm_quit():
    info_entry.delete(0, tk.END)  # Clear the input field
    message_label.config(text="Do you really want to quit? (y/n)")
    info_entry.bind("<Return>", quit_game)

# Function to quit the game
def quit_game(event=None):
    response = info_entry.get().strip()
    info_entry.delete(0, tk.END)  # Clear the input field
    if response.lower() == 'y':
        stop_timer()
        reveal_guessed_numbers()
        hide_timer()
        message_label.config(text="You have quit the game.")
    elif response.lower() == 'n':
        message_label.config(text="Please enter 6 numbers separated by space to crack this lock")
        info_entry.bind("<Return>", get_info)  # Bind the Enter key to get_info function
    else:
        message_label.config(text="Invalid response. Please enter 'y' or 'n'.")

# Function to reveal the guessed numbers
def reveal_guessed_numbers():
    global password, correct_guesses
    revealed_numbers = " | ".join([num for num in password])
    question_marks_label.config(text=revealed_numbers, font=("Helvetica", 30))
    question_marks_label.place(relx=0.5, rely=0.3, anchor="center")

# Function to end the game
def end_game(status):
    print(f"The game has ended with status: {status}")

# Function to generate the random password based on difficulty level
def generate_password(difficulty):
    if difficulty == 'c':
        return [str(random.randint(0, 3)) for _ in range(6)]
    elif difficulty == 'e':
        return [str(random.randint(0, 5)) for _ in range(6)]
    elif difficulty == 'h':
        return [str(random.randint(0, 9)) for _ in range(6)]

# Function to display the crack message with question marks
# Function to display the crack message with question marks
def start_game():
    global start_time
    start_time = time.time()
    message_label.config(text="Please enter 6 numbers separated by space to crack this lock")
    initial_question_marks = "? | ? | ? | ? | ? | ? "
    question_marks_label.config(text=initial_question_marks, font=("Helvetica", 30))
    question_marks_label.place(relx=0.5, rely=0.3, anchor="center")
    update_timer()


# Function to update the timer every second
def update_timer():
    elapsed_time = int(time.time() - start_time)
    timer_label.config(text=f"Time: {elapsed_time} seconds")
    timer_label.after(1000, update_timer)

# Function to handle the guessing process
def guess_password(guess):
    global password, correct_guesses, start_time
    guess_list = guess.split()
    if len(guess_list) == 6 and all(num.isdigit() for num in guess_list):
        correct_guesses = sum(1 for a, b in zip(guess_list, password) if a == b)
        message = f"You have {correct_guesses} correct numbers."
        reveal_numbers(guess_list)
        message_label.config(text=message)
        info_entry.delete(0, tk.END)  # Clear the input field
        if correct_guesses == 6:
            elapsed_time = int(time.time() - start_time)
            message_label.config(text=f"Congratulations! You cracked the lock in {elapsed_time} seconds!")
            stop_timer()
            save_game()
            hide_timer()
    else:
        message_label.config(text="Please enter 6 valid numbers separated by space.")
        info_entry.delete(0, tk.END)  # Clear the input field


# Function to reveal the correctly guessed numbers
def reveal_numbers(guess_list):
    global correct_guesses
    revealed_numbers = " | ".join([num if num == guess else '?' for num, guess in zip(password, guess_list)])
    question_marks_label.config(text=revealed_numbers, font=("Helvetica", 30))
    question_marks_label.place(relx=0.5, rely=0.3, anchor="center")
# Function to stop the timer
def stop_timer():
    timer_label.after_cancel(update_timer)

# Function to hide the timer label
def hide_timer():
    timer_label.place_forget()

# Function to save the game details to Google Sheets
def save_game():
    global name, place, difficulty, start_time, correct_guesses
    elapsed_time = int(time.time() - start_time)
    status = "Won" if correct_guesses == 6 else "Lost"
    game_data = [name, place, difficulty.upper(), status, elapsed_time]
    worksheet.append_row(game_data)
# Create the main window
root = tk.Tk()
root.title("Lock Cracker")
# Load the background image
bg_image = Image.open("lock_crackers/assets/images/turbo-background.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set window size to match the size of the background image
root.geometry(f"{bg_image.width}x{bg_image.height}")

# Create a label for question marks with rounded corners and border lines
question_marks_label = tk.Label(root, font=("Helvetica", 18), bg="white", text="", bd=2, relief="solid")
question_marks_label.place(relx=0.5, rely=0.45, anchor="center")

# Display rules at the top
rules_text = "Welcome to the Password Guessing Game!\n"
rules_text += "Rules:\n"
rules_text += "- You need to guess a password which consists of 6 numbers.\n"
rules_text += "- Each '?' represents one number from 0 to 9.\n"
rules_text += "- You have to guess the password by entering 6 numbers.\n"
rules_text += "- If your guess matches the correct number, it will be revealed.\n"
rules_label = tk.Label(root, text=rules_text, font=("Helvetica", 14), bg="white")
rules_label.place(relx=0.5, rely=0.05, anchor="n")

# Create the label for the message with rounded corners and border lines
message_label = tk.Label(root, font=("Helvetica", 18), bg="white", text=questions[0], bd=2, relief="solid")
message_label.place(relx=0.5, rely=0.4, anchor="center")

# Create the input field with rounded corners and border lines
info_entry = tk.Entry(root, font=("Helvetica", 18), bg="white", bd=2, relief="solid")
info_entry.place(relx=0.5, rely=0.5, anchor="center")

# Bind the Enter key to get_info function
info_entry.bind("<Return>", get_info)

# Create the timer label
timer_label = tk.Label(root, font=("Helvetica", 12), bg="white")
timer_label.place(relx=0.5, rely=0.35, anchor="center")

# Initialize current question index
current_question = 0
name = ""
place = ""
difficulty = ""
password = []
correct_guesses = 0
start_time = 0

root.mainloop()