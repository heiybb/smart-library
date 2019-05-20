import json
import re
import socket

import socket_utils
from database_utils import DatabaseUtils
from pwd_encrypt import encrypt as flower_pass

with open("config.json", "r") as file:
    data = json.load(file)

# The server's hostname or IP address.
HOST = data["MasterPi_IP"]
# The port used by the server.
PORT = 6067
ADDRESS = (HOST, PORT)


class Menu:
    def __init__(self):
        self.userDB = DatabaseUtils()

    def main(self):
        self.run_menu()

    def run_menu(self):
        """
        Provide the console menu
        -- Login
        -- Register
        -- Quit
        """
        while True:
            print()
            print("1. Login")
            print("2. Register")
            print("3. Quit")
            selection = input("Select an option: ")
            print()

            if selection == "1":
                self.login()
            elif selection == "2":
                self.register()
            elif selection == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def login(self):
        """
        Provide text login and face login option
        """
        print("--- Login ---")
        print("1. Text Login")
        print("2. Face Login")
        selection = input("Select an option: ")
        if selection == "1":
            self.text_login()
        if selection == "2":
            self.face_login()
        else:
            print("Invalid input - please try again.")

        # TODO add face login function
        # print("{:<15} {}".format("Person ID", "Name"))
        # with DatabaseUtils() as db:
        #     for person in db.getPeople():
        #         print("{:<15} {}".format(person[0], person[1]))

    def register(self):
        """
        Sub menu option, accept the register input and check if it satisfy the demand
        :rtype: object
        """
        print("--- Registration  ---")
        username = self.register_input("Input your username", 0)
        if self.userDB.check_is_exist(username):
            # go back to register process
            self.register()
        else:
            password = self.register_input("Input your password", 0)
            first_name = self.register_input("Input your first name", 0)
            last_name = self.register_input("Input your last name", 0)
            email_address = self.register_input("Input your email address", 1)

            if self.userDB.insert_user(username, flower_pass(password), first_name, last_name, email_address):
                print("{} register successful.".format(username))
            else:
                print("System error, can't finish the register")

    def register_input(self, prompt_msg, check_type):
        """
        Validate the input, @check_type refers to 0,1

        :ivar prompt_msg the prompt message show in the input
        :ivar check_type 0 refers to the normal input check; 1 refers to the email input check
        :rtype: str
        """
        while True:
            inline = input(prompt_msg)
            if check_type == 0:
                if self.input_check(inline):
                    return inline
                else:
                    print("Invalid input, check it and try again")
            if check_type == 1:
                if self.email_check(inline):
                    return inline
                else:
                    print("Your email address is invalid, try again")

    @staticmethod
    def input_check(income_input):
        """
        Check if the input is valid include the username, password, first name, last name
        Only the letters and numbers and dash and underscore are allowed
        :return True if the income string is valid
        :rtype bool
        """
        if income_input:
            if re.match(r'[\w-]*$', income_input):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def email_check(email_address):
        """
        Check if the email address is valid
        :return: True if income address is valid
        :rtype: bool
        """
        if email_address:
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_address):
                return True
            else:
                return False
        else:
            return False

    def text_login(self):
        username = self.register_input("Input your username", 0)
        if self.userDB.check_is_exist(username):
            # TODO SOCKET MSG SEND
            # TODO LOGIN SUB MENU

            print("Login successful")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Connecting to {}...".format(ADDRESS))
                try:
                    s.connect(ADDRESS)
                except socket.error:
                    s.close()
                    print("Socket connect fail")
                else:
                    print("Connection Established")
                    print("Logging in as {}".format(username))
                    socket_utils.send_json(s, self.userDB.get_user_detail(username))

                    print("Waiting for Master Pi...")
                    while True:
                        income_msg = socket_utils.recv_json(s)
                        if "logout" in income_msg:
                            print("Master Pi logged out")
                            break

        else:
            print("{} not exist, register first".format(username))

    def face_login(self):
        return


if __name__ == "__main__":
    Menu().main()
