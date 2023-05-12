import json
import random
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
    
    # Checks for a valid input
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
        exit()


def open_game():
    """
    Function that starts the game, looks for unfinished chains and if there's one
    available provide user with a question / answer to guess, otherwise start new chain
    """
    # Gets the last question of a random unfinished chain
    unfinished_chain = get_unfinished_chain_end(False)
    print(unfinished_chain[0].to_json())
    
    print(f"It's your turn to {colored('answer a question!','yellow')}\n")


def get_unfinished_chain_end(get_answer):
    """
    Returns list of last entry of a random unfinished chain as [UserData, row, column] 

    `get_answer` decides if an answer or question should be fetched.
    """
    # The worksheet containing all unfinished chains
    worksheet = SHEET.worksheet("unfinished_chains")
    # List of last entries in chains
    chain_end_list = []

    # Iterate over each row in worksheet (Starts at 1)
    for row in range(1, worksheet.row_count + 1):
        # Get the values of the current row
        row_values = worksheet.row_values(row)
        
        # If the row is empty, exit loop
        if not row_values:
            break

        # Get the value of the last column
        last_chain_value = row_values[-1]

        # Check if the last column value is a valid JSON string
        try:
            user_data_dict = json.loads(last_chain_value)
        except Exception as e:
            print(e.args[0])
            continue
        else:
            # Create a UserData object from the fetched JSON string
            user_data = UserData(
                user_data_dict["content"], 
                user_data_dict["author"], 
                user_data_dict["is_answer"]
            )

            # Appends [userData, row, column] to our list
            if user_data.is_answer == get_answer:
                chain_end_list.append([user_data, row, len(row_values)])
    
    # if chain_end_list has viable entries, return a random one
    if chain_end_list:
        return random.choice(chain_end_list)
    else:
        return None
        

def create_new_chain(data):
    """
    Creates new chain starting with provided UserData
    """
    

def open_chain_viewer():
    """
    Opens the chain viewer where users can 
    fetch finished chains by entering the finished chain IDs
    """


class UserData:
    """
    The data that will be submitted to our spreadsheet, contains the string content,
    author and bool if it's a question or answer
    """
    def __init__(self, content, author, is_answer):
        self.content = content
        self.author = author
        self.is_answer = is_answer

    def to_json(self):
        """
        Convert the object to a JSON-formatted string
        """
        return json.dumps(self.__dict__)


open_main_menu()