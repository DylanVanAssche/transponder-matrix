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
        self.client = MatrixClient(self.service) #None
        self.token = "MDAxOGxvY2F0aW9uIG1hdHJpeC5vcmcKMDAxM2lkZW50aWZpZXIga2V5CjAwMTBjaWQgZ2VuID0gMQowMDJkY2lkIHVzZXJfaWQgPSBARHlsYW5WYW5Bc3NjaGU6bWF0cml4Lm9yZwowMDE2Y2lkIHR5cGUgPSBhY2Nlc3MKMDAyMWNpZCBub25jZSA9IERpWENaRnd1ZDVOI0YqODQKMDAyZnNpZ25hdHVyZSAlyUdvFOyXRYsxUEM1w3D41Q7poQdU8_I2v6aTFw28rQo" #None

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
        for key in self.client.get_rooms():
            room = self.client.get_rooms()[key]
            if room_id == room.room_id:
                success = room.leave()
                break

        if not success:
            raise MatrixRequestError(code=404, content="You can't leave a room \
            ({0}) if you haven't joined it yet.".format(room_id))
