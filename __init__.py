# -*- coding: utf-8 -*-
#
#   This file is part of Transponder.
#
#   Matrix Python SDK is licensed under Apache License 2.0 see their repo for
#   more information. The Transponder bridge is also licensed under Apache
#   License 2.0

"""
Transponder is a Sailfish OS application that provide access to different 
messaging providers using Python plugins.
"""

__version__ = "0.0.2"

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "requests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "matrix-python-sdk"))

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from requests.exceptions import MissingSchema

class Client():
    def __init__(self):
        self.client = None
        self.room = None

    def authenticate(self, username, password, host):
        self.client = MatrixClient(host)
        try:
            self.client.login_with_password(username, password)
        except MatrixRequestError as e:
            if e.code == 403:
                print("Bad username or password.")
            else:
                print("Check your sever details are correct.")
                return False
        except MissingSchema as e:
            print("Bad URL format.")
            print(e)
            return False
            
    def get_contacts(self):
        return self.client.get_rooms()
        
    def get_messages(self, contact):
        pass
            
    def start_conversation(self, room_id):
        self.room = self.client.join_room(room_id)
        self.room.add_listener(event_listener)
        self.client.start_listener_thread()
        
    def send_message(self, message):
        self.room.send_text(message)
    
    def event_listener(self, room, event):
        global app
        app.send_signal("matrix", {"contact": room, "event": event})
        
client = Client()
