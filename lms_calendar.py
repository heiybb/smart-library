#!/usr/bin/env python3
# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
# python3 add_event.py --noauth_local_webserver

# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Be sure to enable the Google Calendar API on your Google account by following the reference link above and
# download the credentials.json file and place it in the same directory as this file.

from __future__ import print_function
from datetime import datetime
from datetime import timedelta

import SCOPES as SCOPES
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class LmsCalendar:
    """
    Add and remove borrow book events on Google Calendar
    """
    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/calendar"

    def __init__(self, service=None):
        """
        Constructor
        Check the token is validate or not
        :param service:
        """
        store = file.Storage("token.json")
        creds = store.get()
        if (not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
        service = build("calendar", "v3", http=creds.authorize(Http()))
        self.service = service

    def insert(self, title, author, publish_date, isbn):
        """
        Insert an new borrow book event on Google Calendar
        event details, borrow time, return time and offer reminders
        :param title: book title
        :param author: book author
        :param publish_date: book publish date
        :param isbn: book ISBN
        :return: eventID
        """
        date = datetime.now()
        return_day = (date + timedelta(days=7)).strftime("%Y-%m-%d")
        time_start = "{}T10:00:00+10:00".format(return_day)
        time_end = "{}T11:00:00+10:00".format(return_day)
        event = {
            "summary": "Book title: " + title,
            "location": "RMIT Building 10 Library",
            "description": "Title: " + title + '\n' + "Author: " + author + '\n' +
                           "Publish Date:" + publish_date + '\n' + 'ISBN:' + isbn,
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 5},
                    {"method": "popup", "minutes": 10},
                ],
            }
        }

        event = self.service.events().insert(calendarId="primary", body=event).execute()
        print("Event created: {}".format(event.get("htmlLink")))
        return event.get('id')

    def delete(self, event_id):
        """
        Delete borrow events event on Google Calender
        :param event_id: eventID
        """
        self.service.events().delete(calendarId="primary", eventId=event_id).execute()
        print("done")
