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


def open_game():
    """
    Function that starts the game, looks for unfinished chains and if there's one
    available provide user with a question / answer to guess, otherwise start new chain
    """
    print(f"It's your turn to {colored('answer a question!','yellow')}\n")


def get_unfinished_chain(is_answer):
    """
    Returns random unfinished chain, parameter decides if chain should end with answer or question
    """

def create_new_chain():
    """
    Creates new chain starting with provided UserData
    """

def open_chain_viewer():
    """
    Opens the chain viewer where users can 
    fetch finished chains by entering the finished chain IDs
    """


def quit_application():
    """
    Quits the application
    """


class UserData:
    """
    The data that will be submitted to our spreadsheet, contains bool for if it's a question/answer,
    the string content and name/signature of person who wrote it
    """
    def __init__(self, is_answer, string_content, author, chain_id):
        self.is_answer = is_answer
        self.string_content = string_content
        self.author = author
        self.chain_id = chain_id
    

open_main_menu()