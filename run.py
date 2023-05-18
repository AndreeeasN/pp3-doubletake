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
    Function called on startup, prints welcome message and offers options to play, view old chains or quit
    """
    print(
        f"\n\nWelcome to {colored('[DoubleTake]','yellow')}, a python-based game of telephone!\n"+
        f"In {colored('[DoubleTake]','yellow')} players will create chains of alternating questions and"+
        f" answers\nwhile attempting to guess what the previous person asked. \nGet creative and have fun!\n"
        )
    
    print_menu_options(True)


def print_menu_options(first_time_startup):
    play_string = "Start playing" if first_time_startup else "Play again"

    print(
        f"Type {colored('1','light_green')} to {colored(play_string,'light_green')}\n"+
        f"Type {colored('2','cyan')} to {colored('View finished chains','cyan')}\n"+
        f"Type {colored('3','light_red')} to {colored('Quit the application','light_red')}"
        )
    
    # Checks for a non-empty input
    while True:
        menu_input = input("\nInput: ")
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
        print(colored("[Exiting application...]", "dark_grey"))
        exit()


def start_game():
    """
    Function that starts the game, looks for unfinished chains and if there's one
    available provide user with a question / answer to guess, otherwise start new chain
    """
    # Gets the last question of a random unfinished chain
    unfinished_chain_question = get_unfinished_chain_end(False)

    # Declares first and second question for later use
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
    
    # Opens the post game menu
    open_post_game_menu(user_data_1, user_data_2, unfinished_chain_question, unfinished_chain_answer)


def open_post_game_menu(user_data_1, user_data_2, chain_question, chain_answer):
    """
    Opens the post-game menu, prints the chains the user has answered and appends
    their answers to their respective chains.
    """
    worksheet = SHEET.worksheet("unfinished_chains")
    
    # Prints the chains the user interacted with before they're altered or moved
    chain_1_values = worksheet.row_values(chain_question[1])
    if chain_answer:
        chain_2_values = worksheet.row_values(chain_answer[1])  

    print_chain(chain_1_values)
    print(
        f"{colored(f'Your answer: ', 'magenta')} "+
        f"{user_data_1.content} {colored('- ' + user_data_1.author, 'light_green')}"
        )
    
    # If user started a new chain, chain_answer will be empty
    if chain_answer:
        print_chain(chain_2_values)
        print(
            f"{colored(f'Your question: ', 'yellow')} "+
            f"{user_data_2.content} {colored('- ' + user_data_2.author, 'light_green')}\n"
            )
        
    print(
        "\nYou're all done! The chains you contributed to are shown above!\n"+
        f"\n\n{colored('[Saving data...]', 'dark_grey')}\n\n"
        )
    
    # Appends user answer to chain
    if chain_question:
        append_data_to_chain(worksheet, user_data_1, chain_question)
    
    # Appends question to chain, start new chain if assigned none
    if chain_answer:
        append_data_to_chain(worksheet, user_data_2, chain_answer)
    else:
        create_new_chain(worksheet, user_data_2)

    # Move all chains with 8 entries or more to finished worksheet
    move_finished_chains()
    
    # Print options to play again, view finished chains or quit
    print_menu_options(False)


def print_chain(chain):
    """
    Prints all questions/answers and authors in a chain
    """
    print(colored(f'\n\n[Printing chain...]\n\n','dark_grey'))
    entry_num = 1
    
    for entry in chain:
        # Tries loading json-string and if succesful prints question/answer + author
        try:
            user_data = json.loads(entry)
        except Exception as e:
            print(e.args[0])
            continue
        else:
            if entry_num == 1:
                print(f"Chain started by: {colored(user_data['author'], 'light_green')}!\n")

            qa_string = "Answer" if user_data["is_answer"] else "Question"
            qa_string_color = "magenta" if user_data["is_answer"] else "yellow"
            
            # [Number] Question/Answer: Text content - Author
            print(
                f"{colored(f'[{entry_num}] {qa_string}: ',qa_string_color)} "+
                f"{user_data['content']} {colored('- ' + user_data['author'], 'light_green')}"
                )
            entry_num+=1
            

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
    print(colored(f'\n\n[Fetching data...]\n\n','dark_grey'))
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

    # If on second player input with too few entries in worksheet return None
    # This will cause player to start new chain instead
    if get_answer and len(chain_end_list) < 4:
        return None
        
    # if chain_end_list has viable entries, return a random one
    if chain_end_list:
        return random.choice(chain_end_list)
    else:
        return None


def append_data_to_chain(worksheet, user_data, unfinished_chain_end):
    """
    Appends `user_data` to the row of `unfinished_chain_end` in `worksheet`
    """
    row = unfinished_chain_end[1]
    column = unfinished_chain_end[2]

    # Checks that the cell is empty before adding new UserData
    if len(worksheet.row_values(row)) < column + 1:
        worksheet.update_cell(row, column + 1, user_data.to_json())
    else:
        print("Question/Answer has already been answered")


def create_new_chain(worksheet, user_data):
    """
    Creates new chain starting with provided UserData
    """
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
    Opens a menu where users can fetch finished chains by entering specific chain IDs
    """
    print(f"\n\n{colored('[Fetching data...]', 'dark_grey')}\n\n")
    worksheet = SHEET.worksheet("finished_chains")

    # Gets the first entry of all finished chains
    first_chain_entries = worksheet.col_values(1)
    chain_len = len(first_chain_entries)
    
    # The amount of chains to preview at once, supports any positive integer
    num_of_chains = 8
    scroll_offset = 0
    menu_string = None
    temp_menu_string = f"Printed above are the {min(num_of_chains, chain_len)} latest finished chains!"

    while True:
        # Set start and end index of chains to print (Max set to 0 to prevent negative ints)
        start_index = max(chain_len - num_of_chains - scroll_offset, 0)
        end_index = chain_len - scroll_offset
        
        # Prints the last finished chains
        for index, question in enumerate(first_chain_entries[start_index:end_index], start=start_index + 1):
            # Check if the value is a valid JSON string
            try:
                user_data_dict = json.loads(question)
            except Exception as e:
                print(e.args[0])
                continue
            else:
                # Prints chain index and first question
                print(f"Chain {colored('#' + str(index),'yellow')}: {user_data_dict['content']}")

        # If there's a temporarary menu string it'll be printed and then reset to default
        if temp_menu_string:
            menu_string = temp_menu_string
            temp_menu_string = None
        else:
            menu_string = f"Viewing chains {colored('#'+ str(start_index + 1) +' to #'+ str(end_index),'yellow')}"

        print(f"\n{menu_string}\n")
        print_chain_viewer_options()

        # Checks for a non-empty input, sets as lowercase and removes "#"
        menu_input = input("\nInput: ").lower().replace("#","")

        if menu_input.isalpha:
            # u -> scroll up, d -> scroll down, q -> quit to menu
            if menu_input == "u":
                scroll_offset += num_of_chains
                if scroll_offset > chain_len - num_of_chains:
                    scroll_offset = chain_len - num_of_chains
                    temp_menu_string = "Reached top of list!"
            elif menu_input == "d":
                scroll_offset -= num_of_chains
                if scroll_offset < 0:
                    scroll_offset = 0
                    temp_menu_string = "Reached bottom of list!" 
            elif menu_input == "q":
                break

            # If string is numeric, convert to int 
            elif menu_input.isnumeric:
                try:
                    chain_id = int(menu_input)
                except Exception as e:
                    temp_menu_string = colored(e.args[0],"light_red")
                    continue
                else:
                    # If chain_id is valid, print chain
                    if chain_id >= 1 and chain_id <= chain_len:
                        print_chain(worksheet.row_values(chain_id))
                        input("\nPress enter to continue...\n")
                    else:
                        temp_menu_string = colored("Please enter a valid chain ID.","light_red")
            else:
                temp_menu_string = colored("Please enter a valid input.","light_red")
    main()
    

def print_chain_viewer_options():
    """
    Prints all the chain viewer options, select chain ID, scroll up/down or quit to menu
    """
    print(
        f"Enter a {colored('Chain #ID','light_green')} to {colored('View the chain','light_green')}\n"+
        f"Type {colored('U or D','cyan')} to {colored('Scroll Up or Down','cyan')}\n"+
        f"Type {colored('Q','light_red')} to {colored('Quit to main menu','light_red')}"
        )


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