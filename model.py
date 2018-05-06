#!/usr/bin/python3

"""
The Model manages all the data of the Matrix.org client and returns it if the
API asks for it.
"""

import re
from matrix_client.client import MatrixClient
from matrix_client.errors import MatrixRequestError
from matrix_client.user import User

class Model(object):
    def __init__(self, controller):
        self._controller = controller
        self.version = 0.1
        self.service = "https://matrix.org"
        self.client = None
        self.token = None

    def auth(self, username, password, server, new):
        """
        Connects to the given Matrix server and authenticates the user.
        On success, the auth token is returned.

        __Parameters__

        - username: Matrix username for the given server
        - password: Matrix password for the given server
        - server: Matrix server URL
        - new: `True` = creates a new user account on the given server, `False`
        logs the user in on the server


        __Returns__

        - token: Matrix auth token
        """
        # Create a Matrix.org SDK client
        self.client = MatrixClient(server)

        # Register/login the user
        if new:
            # No captcha support in the Matrix.org Python SDK, see https://github.com/matrix-org/matrix-python-sdk/issues/82
            self.token = self.client.register_with_password(username=username, password=password)
        else:
            self.token = self.client.login_with_password(username=username, password=password)

        return self.token

    @property
    def rooms(self):
        """
        Retrieves the rooms from the user's address book as JSON.

        __Returns__

        - rooms: Python list of all rooms in dictionary format

        ```json
            {
                "id": string
                "name": string
                "avatar": string
                "last_seen": string
                "members": [
                    {
                        "id": string
                        "name": string
                        "last_seen": string
                        "avatar": string
                    },
                    ...
                ]
            }
        ```
        """
        data = []

        # Loop through each loop and retrieve it's meta data
        for key in self.client.get_rooms():
            room = self.client.get_rooms()[key]
            room_data = {
                "id": room.room_id,
                "name": room.name,
                "avatar": None, # unsupported by the Matrix.org Python SDK
                "last_seen": None, # unsupported by the Matrix.org Python SDK
                "members": []
            }

            # Add each member of the room to the members property
            for index, member in enumerate(room.get_joined_members()):
                if isinstance(member, User): # Riot-Bot is displayed as a string
                    room_data["members"].append({
                        "id": index,
                        "name": member.displayname,
                        "avatar": None, #member.get_avatar_url(), # Broken in the Matrix.org Python SDK
                        "last_seen": None # unsupported by the Matrix.org Python SDK
                    })

            # Add room to our data list
            data.append(room_data)

        return data

    def add_room(self, room_id):
        """
        Adds a room to the user address book if the `room_id` exists, if it doesn't
        exists, the room will be created and added to the user address book.

        __Raises__

        - MatrixRequestError: in case something goes wrong with the Matrix API,
        this exception will be raised.
        """
        # starts with '#' or '!' and a ':' will be in the string
        matrix_id_regex = re.compile("(^!)|(^#)|(:)")

        # room_id is a full ID for joining
        if matrix_id_regex.match(room_id):
            self.client.join_room(room_id)
        # new room since the room_id isn't a valid Matrix room ID but a room alias
        else:
            room = self.client.create_room(room_id)
            room.set_room_name(room_id) # set the room name to the room alias

    def remove_room(self, room_id):
        """
        Let the user leave a room in his address book.

        __Raises__

        - MatrixRequestError: leaving an unjoined is not possible.
        """
        success = False
        room = self._find_room(room_id)
        success = room.leave()

        if not success:
            raise MatrixRequestError(code=404, content="You can't leave a room \
            ({0}) if you haven't joined it yet.".format(room_id))

    def messages(self, room_id):
        """
        Returns a list of messages for a specific room_id

        __Parameters__

        - room_id: Matrix ID of the room

        __Returns__

        - messages: List of messages
        """
        events = []
        messages = []

        # Get room
        room = self._find_room(room_id)
        room.event_history_limit += 10 # increment limit and retrieve more messages on each call
        room.backfill_previous_messages(limit=10)
        events = room.events

        for event in events:
            if event.get("type") == "m.room.message":
                if event.get("content").get("msgtype") == "m.text":
                    messages.append({
                        "type": "text",
                        "from": event.get("sender"),
                        "content": event.get("content").get("body"),
                        "timestamp": None, # Not supported by the Matrix.org Python SDK
                        "read": None # Not supported by the Matrix.org Python SDK
                    })
                elif event.get("content").get("msgtype") == "m.image":
                    messages.append({
                        "type": "image",
                        "from": event.get("sender"),
                        "content": self.decode_download_link(event.get("content").get("url")),
                        "timestamp": None, # Not supported by the Matrix.org Python SDK
                        "read": None # Not supported by the Matrix.org Python SDK
                    })
            elif event.get("type") == "m.room.member":
                messages.append({
                    "type": "contact",
                    "from": event.get("sender"),
                    "content": "{0} {1} room".format(event.get("sender"), event.get("content").get("membership")),
                    "timestamp": None, # Not supported by the Matrix.org Python SDK
                    "read": None # Not supported by the Matrix.org Python SDK
                })

        return messages

    def send_text(self, room_id, text):
        """
        Sends a basic text message to the given room.

        __Parameters__

        - room_id: Matrix ID of the room
        - text: ASCII text to send

        __Raises__

        - MatrixRequestError: when something goes wrong while sending the message
        a MatrixRequestError is raised

        __Returns__

        - success: `True` if message was sended to the room
        """
        room = self._find_room(room_id)
        if room.send_text(text):
            return True
        return False

    def decode_download_link(self, link):
        """
        Converts a Matrix MXC link to a normal HTTP link.
        """
        return self.client.api.get_download_url(link)

    def _find_room(self, room_id):
        """
        Retrieve a Room object based on the room_id.
        """
        for key in self.client.get_rooms():
            room = self.client.get_rooms()[key]
            if room_id == room.room_id:
                return room
