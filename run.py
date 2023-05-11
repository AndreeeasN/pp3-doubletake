import gspread
from termcolor import colored
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("PP3_sheet")

# page = SHEET.worksheet("unfinished_chains")
# data = page.get_all_values()

def open_main_menu():
    """
    Prints the main menu contents, offers options to play, view old chains or quit
    """
    print(
        f"Welcome to {colored('[game name]','yellow')}, a python-based game of telephone!\n"+
        f"In {colored('[game name]','yellow')} players will create chains of alternating questions and answers\n"+
        f"while attempting to guess what the previous person asked, get creative and have fun!\n\n"+
        f"Type {colored('1','light_green')} to {colored('Start playing','light_green')}\n"+
        f"Type {colored('2','cyan')} to {colored('View finished chains','cyan')}\n"+
        f"Type {colored('3','light_red')} to {colored('Quit the application','light_red')}\n"
        )
    
    while True:
        menu_input = input()
        if menu_input in ("1","2","3"):
            break
        else:
            print("Invalid input, please try again")

    if menu_input == "1":
        open_game()
    elif menu_input == "2":
        open_chain_viewer()
    elif menu_input == "3":
        quit_application()


open_main_menu()