#!/usr/bin/env python3
"""
Reception Pi Console Menu
"""
import json
import re
import socket
from os import system, name

import Socket_Utils
from Database_Utils import DatabaseUtils
from FaceDataCapture import FaceDataCapture
from FaceDataEncode import FaceDataEncode
from FaceRecognise import FaceRecognise
from PWD_Encrypt import encrypt as flower_pass

with open("config.json", "r") as file:
    CONF = json.load(file)

# The server's hostname or IP address.
SOCKET_HOST = CONF["MasterPi_IP"]
# The port used by the server.
PORT = 6067
ADDRESS = (SOCKET_HOST, PORT)


class Menu:
    """
    Menu Class
    """

    def __init__(self):
        self.user_db_util = DatabaseUtils()

    def main(self):
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
                self.clear()
                self.login()
            elif selection == "2":
                self.clear()
                self.register()
            elif selection == "3":
                self.clear()
                print("Goodbye!")
                break
            elif selection == "":
                self.clear()

    def login(self):
        """
        Provide text login and face login option
        """
        print("--- Login ---")
        print("1. Password Login")
        print("2. Face Login")
        selection = input("Select an option: ")
        if selection == "1":
            self.clear()
            self.password_login()
        elif selection == "2":
            self.clear()
            self.face_login()

    def register(self):
        """
        Sub register menu, accept the register input and check if it satisfy the rules
        :rtype: object
        """
        print("--- Registration  ---")
        username = self.input_validate("Input your username: ")
        if self.user_db_util.check_is_exist(username):
            self.clear()
            print("username {} is already used by others, try another one".format(username))
            # go back to register process
            self.register()
        else:
            password = self.input_validate("Input your password: ")
            first_name = self.input_validate("Input your first name: ")
            last_name = self.input_validate("Input your last name: ")
            email_address = self.email_validate("Input your email address: ")

            if self.user_db_util.insert_user(username,
                                             flower_pass(password),
                                             first_name, last_name,
                                             email_address):
                print("{} register successful.".format(username))
            else:
                print("System error, can't finish the register")

    @staticmethod
    def input_validate(prompt_msg):
        """
        Check if the input is valid include the username, password, first name, last name
        Only the letters and numbers and dash and underscore are allowed
        :return True if the income string is valid
        :rtype str
        """
        while True:
            income_input = input(prompt_msg)
            if re.match(r'[\w-]*$', income_input):
                return income_input
            print("Invalid input, check it and try again")

    @staticmethod
    def email_validate(prompt_msg):
        """
        Check if the email address is valid
        :return: True if income address is valid
        :rtype: bool
        """
        while True:
            email_address = input(prompt_msg)
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_address):
                return email_address
            print("Your email address is invalid, try again")

    def password_login(self):
        """
        Use traditional username & password to login
        """
        print()
        print("Input your username and password to login")
        username = self.input_validate("Input your username: ")
        password = self.input_validate("Input your password: ")
        print()
        print("Please wait for validating the password...")
        print()

        if self.user_db_util.check_password(str(username), str(password)):
            print("Login successful")
            while True:
                print("1. Directly Login")
                print("2. Add face data")
                print("3. Back to homepage")

                selection = input("Select an option: ")
                if selection == "1":
                    self.clear()
                    self.send_socket_login(username)

                elif selection == "2":
                    self.clear()
                    # pass the username as the user face data folder
                    FaceDataCapture.capture(username)
                    FaceDataEncode.encode()

                elif selection == "3":
                    self.clear()
                    break
        else:
            print("Username or Password not match, try again")

    def face_login(self):
        """
        Use face recognise module to login
        """
        print()
        print("Input your username to match the face data")
        username = self.input_validate("Input your username: ")

        if FaceRecognise.recognise(username):
            print("Face login successful")
            self.send_socket_login(username)
        else:
            print("No face data found")

    @staticmethod
    def clear():
        """
        Clear the screen output
        Compatible for both WIN and *unix
        """
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def send_socket_login(self, username):
        """
        Use socket to send the username and related details to the Master Pi
        :param username: Refers to the user details
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_connection:
            print("Connecting to {}...".format(ADDRESS))
            try:
                socket_connection.connect(ADDRESS)
            except Exception:
                print("Can not connect to the Master Server")
                socket_connection.close()
            else:
                print("Connection Established")
                print("Logging in as {}".format(username))
                Socket_Utils.send_json(socket_connection, self.user_db_util.get_user_detail(username))

                print("Waiting for message from Master Pi...")
                try:
                    while True:
                        # loop the handle the log out msg from the master pi
                        income_msg = Socket_Utils.recv_json(socket_connection)
                        if income_msg and "logout" in income_msg:
                            print("Master Pi logged out")
                            break
                except Exception as e:
                    print("Remote server error -> Connection end")


if __name__ == "__main__":
    MENU = Menu()
    MENU.main()
