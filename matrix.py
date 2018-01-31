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

import sys
sys.path.append("./matrix/matrix-python-sdk") # make matrix_client visible
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from requests.exceptions import MissingSchema

client = None
room = None

def authenticate(username, password, host):
    client = MatrixClient(host)
    try:
        client.login_with_password(username, password)
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
        
def get_contacts():
    return client.get_rooms()
        
def start_conversation(room_id):
    room = client.join_room(room_id)
    room.add_listener(on_message_received)
    client.start_listener_thread()
    
def send_message(message):
    room.send_text(message)
    
def on_message_received(room, event):
    pass