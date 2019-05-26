#!/usr/bin/env python3
"""
Menu for Master Pi
"""
import socket, json, sys
sys.path.append("..")
import socket_utils
import time
import datetime
from database_utils import DatabaseUtils
from lms_calendar import LmsCalendar
from BarcodeRecognise import BarcodeRecognise
from VoiceRecognise import VoiceRecognise
HOST = ""
PORT = 63000
ADDRESS = (HOST, PORT)


class Menu:
    """
    Master Pi Menu Class
    """

    def main(self, lms):
        # calling create table from database
        with DatabaseUtils() as db:
            db.create_table()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # set up the serve
            s.bind(ADDRESS)
            s.listen()

            # Make sure that socket can receive in a  fixed IP address
            print("Listening on {}...".format(ADDRESS))

            # Receive the user name from reception pi
            while True:
                print("Waiting for Reception Pi...")
                conn, addr = s.accept()
                with conn:
                    print("Connected to {}".format(addr))
                    print()

                    user = socket_utils.recvJson(conn)
                    user_name = user['Username']
                    name = user['Name']
                    print("Hi " + user_name + " Welcome to Smart Library")
                    self.menu(user_name, name, lms)
                    socket_utils.sendJson(conn, {"logout": True})

    def search_books(self, user):
        # search book
        while True:
            print()
            print("1. Search by Typing")
            print("2. Search by Barcode")
            print("3. Search by Voice")
            print("0. Back to Main Page")

            print()
            text = input("Select an option: ")
            print()

            if text == '1':
                self.search_by_typing()
            elif text == '2':
                result = self.search_by_barcode()
                if result is not None:
                    self.search_books_by_property('isbn', result)
            elif text == '3':
                voice = self.search_by_voice()
                if voice is not None:
                    self.search_books_by_property('title', voice)
            elif text == '0':
                print("Goodbye.")
                print()
                break
            else:
                print("Invalid input, try again.")
                print()

    def search_by_voice(self):
        # voice search
        vr = VoiceRecognise()
        return vr.recognise()

    def search_by_barcode(self):
        # Barcode search
        br = BarcodeRecognise()
        return br.recognise()

    def search_by_typing(self):
        """
        Typing search
        show the item list
        """
        while True:
            print("1. Search by Title")
            print("2. Search by Author")
            print("3. Search by Published Date")
            print("4. Search by ISBN")
            print("5. Show All Books")
            print("0. Back to Main Menu")
            print()

            text = input("Select an option: ")
            print()

            if text == "1":
                # search by title
                print()
                print("--- Search Books by Title ---")
                print()
                title = input("Input Book Title: ")
                print()
                self.search_books_by_property('title', title)
            elif text == "2":
                # Search by author
                print()
                print("--- Search Books by Author ---")
                print()
                author = input("Input Book Author: ")
                print()
                self.search_books_by_property('author', author)

            elif text == "3":
                # Search by published date
                print()
                print("--- Search Books by Published Date ---")
                print()
                publish_date = input("Input Book Published Date: ")
                print()
                self.search_books_by_property('publish_date', publish_date)

            elif text == "4":
                # Search by ISBN
                print()
                print("--- Search Books by ISBN ---")
                print()
                isbn = input("Input Book ISBN: ")
                print()
                self.search_books_by_property('isbn', isbn)

            elif text == "5":
                self.list_book()
                print()

            elif text == "0":
                print("Goodbye.")
                print()
                break

            else:
                # Invalid input
                print("Invalid input, try again.")
                print()

    def list_book(self):
        # List all the searching results
        print("--- Search Books Result ---")
        print()
        print("{:<6}{:<40} {:<20} {:<20} {:<15}".format('No.', 'Title', 'Author', 'Published Date', 'ISBN'))
        with DatabaseUtils() as db:
            for item in db.get_book():
                print("{:<6}{:<40} {:<20} {:<20} {:<15}".
                      format(item[0], item[1], item[2], item[3].strftime("%Y-%m-%d"), item[4]))

    def search_books_by_property(self,search_type, value):
        # search the book using different type
        if search_type == 'title':
            search_index = 1
        elif search_type == 'author':
            search_index = 2
        elif search_type == 'publish_date':
            search_index = 3
        elif search_type == 'isbn':
            search_index = 4
        else:
            print("Search not found")
            return

        print("--- Search Books Result ---")
        # show the result of the search
        print()
        is_find = True
        print("{:<6}{:<40} {:<20} {:<20}{:<15}".format('No.', 'Title', 'Author', 'Published Date', 'ISBN'))
        with DatabaseUtils() as db:
            for item in db.get_book():
                if search_index == 3:
                    if item[search_index].strftime("%Y-%m-%d") == value:
                        print("{:<6}{:<40} {:<20} {:<20}{:<15}".format(item[0], item[1], item[2],
                                                                       item[3].strftime("%Y-%m-%d"), item[4]))
                        is_find = False
                else:
                    if item[search_index].lower() == value.lower():
                        print("{:<6}{:<40} {:<20} {:<20}{:<15}".format(item[0], item[1], item[2],
                                                                       item[3].strftime("%Y-%m-%d"), item[4]))
                        is_find = False
            if is_find:
                print()
                print("{:<16} {}".format("Searching result:", "The book title: " + value + ", is not found."))
        print()

    def borrowed_books(self, user, lms):
        while True:
            print("1. Continue to borrow a book")
            print("0. Back to Main Menu")
            print()

            text = input("Select an option: ")
            print()
            if text == '0':
                print()
                break
            elif text == '1':
                title = input("Input book title: ")
                print()
                author = input("Input book author: ")
                print()
                print("publish date format is 2019-05-31")
                publish_date = input("Input book publish date: ")
                print()
                isbn = input("Input book ISBN: ")
                print()
                self.borrowed_by_detail(title, author, publish_date, isbn, user, lms)
            else:
                print("Invalid input, try again.")
                print()
                continue

    def check_book_exist(self, title, author, publish_date, isbn, check_type):
        # This is used for borrow books and return book, depend on check_type
        with DatabaseUtils() as db:
            for item in db.get_book():
                if item[1] == title and item[2] == author and \
                        item[3].strftime("%Y-%m-%d") == publish_date and item[4] == isbn:
                    if len(db.get_specify_book_borrowed(item[0])) == 0:
                        return False
                    else:
                        for book in db.get_specify_book_borrowed(item[0]):
                            if book[3] == 'borrowed':
                                if check_type == 'borrow':
                                    print("### Sorry, This book is borrowed by other.")
                                    print()
                                    return True
                                elif check_type == 'return':
                                    return False
                            elif book[3] == 'returned':
                                if check_type == 'borrow':
                                    return False
                                elif check_type == 'return':
                                    print("### Sorry, This book has been returned")
                                    print()
                                    return True

        print(
            "You search book : " + title + ", author is: " + author + ", publish date is: " + publish_date + ',ISBN:' + isbn)
        print("This book is not exist. Try again")
        return True

    def borrowed_by_detail(self,title, author, publish_date, isbn, user, lms):
        if self.check_book_exist(title, author, publish_date, isbn, 'borrow'):
            return

        with DatabaseUtils() as db:
            lmsUserID = db.get_lms_user(user)[0][0]
            bookID = db.get_book_id(title, author, publish_date, isbn)[0][0]
            status = 'borrowed'
            borrowedDate = datetime.datetime.now().date().strftime('%Y-%m-%d')
            returnedDate = (datetime.datetime.now() + datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
            db.insert_book_borrowed(lmsUserID, bookID, status, borrowedDate, returnedDate)

            print('The book ' + title + ", you borrow successfully.")
            event_id = lms.insert(title, author, publish_date, isbn)
            db.insert_event_id(bookID, event_id)
            print('The return date is ' + returnedDate + ", which is added into your google calendar.")
            print()

    def check_reg(self,user, name):
        # check the register is exist in the database
        with DatabaseUtils() as db:
            if len(db.get_lms_user(user)) == 0:
                db.insert_lms_user(user, name)

    def return_books(self,user, lms):
        while (True):
            print("1. Continue to return a book")
            print("0. Back to Main Menu")
            print()

            text = input("Select an option: ")
            print()
            if text == '0':
                print()
                break
            elif text == '1':
                title = input("Input book title: ")
                print()
                author = input("Input book author: ")
                print()
                print("publish date format is 2019-05-31")
                publish_date = input("Input book publish date: ")
                print()
                print()
                isbn = input("Input book ISBN: ")
                print()

                self.return_by_detail(title, author, publish_date, user, isbn, lms)

            else:
                print("Invalid input, try again.")
                print()
                continue

    def return_by_detail(self,title, author, publish_date, user, isbn, lms):
        if self.check_book_exist(title, author, publish_date, isbn, 'return'):
            return

        # going to delete this event
        with DatabaseUtils() as db:
            lmsUserID = db.get_lms_user(user)[0][0]
            bookID = db.get_book_id(title, author, publish_date, isbn)[0][0]
            status = 'returned'
            returnedDate = (datetime.datetime.now() + datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')

            db.update_book_borrowed(lmsUserID, bookID, status)

            print('The book ' + title + ", you return successfully.")
            event_id = db.get_event_id(bookID)[0][0]
            print('what is event_id ' + event_id)
            db.delete_event_id(bookID)
            lms.delete(event_id)
            print('The return date is ' + returnedDate + ", which is deleted into your google calendar.")
            print()

    def menu(self, user, name, lms):
        while True:
            # check if register, if not, register the user
            self.check_reg(user, name)

            # print("Welcome {}".format(user["username"]))
            # show the menu list
            print("1. Search a book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("0. Logout")
            print()

            text = input("Select an option: ")
            print()

            if text == "1":
                self.search_books(user)
                print()

            elif text == "2":
                self.borrowed_books(user, lms)
                print()

            elif text == "3":
                self.return_books(user, lms)
                print()

            elif text == "0":
                print("Goodbye.")
                print()
                break
            else:
                print("Invalid input, try again.")
                print()


# Execute program.
if __name__ == "__main__":
    lms = LmsCalendar()
    lms_menu = Menu()
    lms_menu.main(lms)
