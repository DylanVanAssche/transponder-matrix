#!/usr/bin/python3

"""
The Model manages all the data of the Matrix.org client and returns it if the
API asks for it.
"""

from matrix_client.client import MatrixClient
from matrix_client.user import User

class Model(object):
    def __init__(self, controller):
        self._controller = controller
        self.version = 0.1
        self.service = "matrix.org"
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
