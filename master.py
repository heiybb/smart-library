#!/usr/bin/env python3


import socket, json, sys
sys.path.append("..")
import socket_utils
from database_utils import DatabaseUtils
from lms_calendar import LmsCalendar
import time
import datetime

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)


def main(lms):
    with DatabaseUtils() as db:
        db.createTable()
    #
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind(ADDRESS)
    #     s.listen()
    #
    #     print("Listening on {}...".format(ADDRESS))
    #     while True:
    #         print("Waiting for Reception Pi...")
    #         conn, addr = s.accept()
    #         with conn:
    #             print("Connected to {}".format(addr))
    #             print()
    #
    #             user = socket_utils.recvJson(conn)
    #             menu(user)
    #
    #             socket_utils.sendJson(conn, { "logout": True })


    menu("Testing",lms)


def searchBooks(user):
    while (True):
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Published Date")
        print("4. Search randomly")
        print("0. Back to Main Menu")
        print()

        text = input("Select an option: ")
        print()

        if (text == "1"):
            print()
            print("--- Search Books by Title ---")
            print()
            title = input("Input Book Title: ")
            print()
            searchBooksByProperty('title', title)


        elif (text == "2"):
            print()
            print("--- Search Books by Author ---")
            print()
            author = input("Input Book Author: ")
            print()
            searchBooksByProperty('author', author)

        elif (text == "3"):
            print()
            print("--- Search Books by Published Date ---")
            print()
            publish_date = input("Input Book Published Date: ")
            print()
            searchBooksByProperty('publish_date', publish_date)

        elif (text == "4"):
            listBook()
            print()

        elif (text == "0"):
            print("Goodbye.")
            print()
            break

        else:
            print("Invalid input, try again.")
            print()


def listBook():
    print("--- Search Books Result ---")
    print()
    print("{:<6}{:<40} {:<20} {}".format('No.', 'Title', 'Author', 'Published Date'))
    with DatabaseUtils() as db:
        for item in db.getBook():
            print("{:<6}{:<40} {:<20} {}".format(item[0], item[1], item[2], item[3]))


def searchBooksByProperty(search_type, value):
    if search_type == 'title':
        search_index = 1
    elif search_type == 'author':
        search_index = 2
    elif search_type == 'publish_date':
        search_index = 3
    else:
        print("Search not found")
        return

    print("--- Search Books By Title Result ---")
    print()
    is_find = True
    print("{:<6}{:<40} {:<20} {}".format('No.', 'Title', 'Author', 'Published Date'))
    with DatabaseUtils() as db:
        for item in db.getBook():
            if item[search_index] == value:
                print("{:<6}{:<40} {:<20} {}".format(item[0], item[1], item[2], item[3]))
                is_find = False
        if is_find:
            print()
            print("{:<16} {}".format("Searching result:", "The book title: " + value + ", is not found."))
    print()


def borrowedBooks(user, lms):
    while(True):
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

            # title = 'The gap in research'
            # author = 'Clara'
            # publish_date = '2000-01-01'

            borrowedBooksByDetail(title, author, publish_date, user, lms)

        else:
            print("Invalid input, try again.")
            print()
            continue


def checkBookIfExist(title, author, publish_date, check_type):
    with DatabaseUtils() as db:
        for item in db.getBook():
            if item[1] == title and item[2] == author and item[3].strftime("%Y-%m-%d") == publish_date:
                if len(db.getSpecifyBookBorrowed(item[0])) == 0:
                    return False
                else:
                    for book in db.getSpecifyBookBorrowed(item[0]):
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


    print("You search book : " + title + ", author is: " + author + ", publish date is: " + publish_date)
    print("This book is not exist. Try again")
    return True


def borrowedBooksByDetail(title, author, publish_date,user, lms):
    # if checkBookIfExist(title, author, publish_date, 'borrow'):
    #     return

    with DatabaseUtils() as db:
        lmsUserID = db.getLmsUser(user)[0][0]
        bookID = db.getSpecifyBookID(title, author, publish_date)[0][0]
        status = 'borrowed'
        borrowedDate = datetime.datetime.now().date().strftime('%Y-%m-%d')
        returnedDate = (datetime.datetime.now() + datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
        db.insertBookBorrowed(lmsUserID, bookID, status, borrowedDate, returnedDate)

        print('The book ' + title + ", you borrow successfully.")
        event_id = lms.insert(title,author,publish_date)
        db.insertEventId(bookID,event_id)
        print('The return date is ' + returnedDate + ", which is added into your google calendar.")
        print()


def checkReg(user):
    with DatabaseUtils() as db:
        if len(db.getLmsUser(user)) == 0:
            db.insertLmsUser(user,user)


def returnBooks(user, lms):
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

            # title = 'The gap in research'
            # author = 'Clara'
            # publish_date = '2000-01-01'

            returnBooksByDetail(title, author, publish_date, user, lms)

        else:
            print("Invalid input, try again.")
            print()
            continue


def returnBooksByDetail(title, author, publish_date, user, lms):
    if checkBookIfExist(title, author, publish_date, 'return'):
        return

    # going to delete this event
    with DatabaseUtils() as db:
        lmsUserID = db.getLmsUser(user)[0][0]
        bookID = db.getSpecifyBookID(title, author, publish_date)[0][0]
        status = 'borrowed'
        borrowedDate = datetime.datetime.now().date().strftime('%Y-%m-%d')
        returnedDate = (datetime.datetime.now() + datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
        db.insertBookBorrowed(lmsUserID, bookID, status, borrowedDate, returnedDate)

        print('The book ' + title + ", you return successfully.")
        event_id = db.getEventId(bookID)[0][0]
        print('what is event_id ' + event_id)
        db.deleteEventIdr(bookID)
        lms.delete(event_id)
        print('The return date is ' + returnedDate + ", which is deleted into your google calendar.")
        print()





def menu(user, lms):
    while(True):

        # check if reg, if not, reg
        checkReg(user)

        # print("Welcome {}".format(user["username"]))
        print("1. Search a book")
        print("2. Borrow a book")
        print("3. Return a book")
        print("0. Logout")
        print()

        text = input("Select an option: ")
        print()

        if(text == "1"):
            searchBooks(user)
            print()

        elif(text == "2"):
            borrowedBooks(user, lms)
            print()

        elif(text == "3"):
            returnBooks(user, lms)
            print()

        elif(text == "0"):
            print("Goodbye.")
            print()
            break

        else:
            print("Invalid input, try again.")
            print()


# Execute program.
if __name__ == "__main__":
    lms = LmsCalendar()
    # lms.prepare()
    # lms.insert()

    main(lms)
