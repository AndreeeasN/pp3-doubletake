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


def main():
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
    
    # Checks for a non-empty input
    while True:
        menu_input = input()
        if menu_input in ("1","2","3"):
            break
        else:
            print("Invalid input, please try again")

    # 1 -> play game, 2 -> view old chains, 3 -> exit
    if menu_input == "1":
        start_game()
    elif menu_input == "2":
        open_chain_viewer()
    elif menu_input == "3":
        print("Exiting application...")
        exit()


def start_game():
    """
    Function that starts the game, looks for unfinished chains and if there's one
    available provide user with a question / answer to guess, otherwise start new chain
    """
    # Gets the last question of a random unfinished chain
    unfinished_chain_question = get_unfinished_chain_end(False)

    # Declares first and second question as UserData objects
    user_data_1 = user_data_2 = None

    # First question, if there's a chain to answer proceed normally otherwise start new chain
    if unfinished_chain_question:
        # Prints question/answer for user to answer
        print(f"It's your turn to {colored('answer a question!','yellow')}\n")
        print(f"{colored(f'Question: ','yellow')} {unfinished_chain_question[0].content}")
        
        # Creates UserData object based on player input
        user_data_1 = question_answer_input(True)
    
    # Gets the last answer of a random unfinished chain
    unfinished_chain_answer = get_unfinished_chain_end(True)

    # Second question, will always be guessing the question
    if unfinished_chain_answer:
        # Prints question/answer for user to answer
        print(f"It's your turn to {colored('guess the question!','magenta')}\n")
        print(f"{colored(f'Answer: ','magenta')} {unfinished_chain_answer[0].content}")
        
        # Creates UserData object based on player input
        user_data_2 = question_answer_input(False)
    else:
        print(f"You get to start a new chain! {colored('Ask a question!','magenta')}\n\n")
        
        # Creates UserData object based on player input
        user_data_2 = question_answer_input(False)


    # Appends user answer to chain
    if unfinished_chain_question:
        append_data_to_chain(user_data_1, unfinished_chain_question)
    
    # Appends question to chain, start new chain if assigned none
    if unfinished_chain_answer:
        append_data_to_chain(user_data_2, unfinished_chain_answer)
    else:
        create_new_chain(user_data_2)

    move_finished_chains()


def question_answer_input(is_answer):
    """
    Function that awaits player input and returns UserData object. 
    
    `is_answer` decides if the user is inputting answer or question
    """
    #Sets string and color to be printed before user input
    qa_string_input = "Answer" if is_answer else "Question"
    qa_string_color = "magenta" if is_answer else "yellow"
    while True:
        # Checks for non-empty input, loops while empty
        user_answer = input(colored(f'{qa_string_input}: ',qa_string_color))
        if user_answer:
            # Allows user to input signature, defaults to "Anonymous" if left blank
            print(f"\nAdd signature? (Leave blank to stay anonymous)")
            user_signature = input(colored('Signature: ', 'cyan'))
            if not user_signature: 
                user_signature = "Anonymous"

            # Returns new userData object based on user input
            return UserData(user_answer, user_signature, is_answer)
        else:
            print(colored(f"Please enter a valid {qa_string_input.lower()}.","light_red"))


def get_unfinished_chain_end(get_answer):
    """
    Returns last entry of a random unfinished chain as [UserData, row, column] 

    `get_answer` decides if an answer or question should be fetched.
    """
    print(colored(f'\n[Fetching data...]\n\n','dark_grey'))
    # The worksheet containing all unfinished chains
    worksheet = SHEET.worksheet("unfinished_chains")

    # List of last entries in chains
    chain_end_list = []

    # Iterate over each row in worksheet (Starts at 1, default length is 999)
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
    # else return none, will cause player to start new chain
    else:
        return None


def append_data_to_chain(user_data, unfinished_chain_end):
    """
    Appends `user_data` to the row of `unfinished_chain_end` 
    """
    worksheet = SHEET.worksheet("unfinished_chains")
    row = unfinished_chain_end[1]
    column = unfinished_chain_end[2]

    # Checks that the cell is empty before adding new UserData
    if len(worksheet.row_values(row)) < column + 1:
        worksheet.update_cell(row, column + 1, user_data.to_json())
    else:
        print("Question/Answer has already been answered")


def create_new_chain(user_data):
    """
    Creates new chain starting with provided UserData
    """
    worksheet = SHEET.worksheet("unfinished_chains")
    worksheet.append_row([user_data.to_json()])


def move_finished_chains():
    """
    Find all chains with 8 entries or more and move them to the page of finished chains 
    """
    unfinished_worksheet = SHEET.worksheet("unfinished_chains")
    finished_worksheet = SHEET.worksheet("finished_chains")

    # Iterate over each row in unfinished worksheet (Starts at 1, default length is 999)
    i = 1
    while i < unfinished_worksheet.row_count + 1:
        # Get the values of the current row
        row_values = unfinished_worksheet.row_values(i)
        
        # If row is empty, break
        if not row_values: 
            break

        # If the row has 8 entries or more, move to finished worksheet
        if len(row_values) >= 8:
            finished_worksheet.append_row(row_values)
            unfinished_worksheet.delete_rows(i)
            continue
        i += 1


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


main()