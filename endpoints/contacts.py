#!/usr/bin/python3

import cherrypy
from .endpoint import RestAPIEndpoint

class ContactsEndpoint(RestAPIEndpoint):
    """
    __/contacts__ contains all the user it's Matrix.org rooms.

    Implemented HTTP REST methods:

    - __GET__: Reads all the rooms of the user
    - __POST__: Adds a new rooms of the user
    - __PUT__: Modifies a rooms of the user
    - __DELETE__: Deletes a rooms of the user
    """

    def __init__(self, controller):
        super().__init__(controller)

    @cherrypy.tools.json_out()
    def GET(self):
        """
        Reads all the rooms of the user and returns them.

        __Raises__

        - HTTP 400: the user must be authenticated first
        """
        if not self._controller.is_auth():
            raise cherrypy.HTTPError(400, "Bad request: user not logged in")

        return {
            "version": self._controller.get_version(),
            "service": self._controller.get_service(),
            "contacts": self._controller.get_contacts()
        }

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """
        Adds a new room to the user address book and returns all the rooms.
        Automatically handles the difference between a new room and joining an
        existing room. When the room doesn't exist, the room is created.

        __Raises__

        - HTTP 400: the user must be authenticated first
        """
        if not self._controller.is_auth():
            raise cherrypy.HTTPError(400, "Bad request: user not logged in")

        db = {
            "version": self._controller.get_version(),
            "service": self._controller.get_service(),
            "contacts": self._controller.get_contacts()
        }

        # Retrieve the JSON data
        data = cherrypy.request.json

        # Raise HTTP 400 when adding a room fails
        if not True:
            raise cherrypy.HTTPError(400, "Bad request.")

        # Add the room to the address book
        db["contacts"] = self._controller.get_contacts().append(data)

        return db

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        """
        Modifies a room from the user address book and returns all the rooms.

        __Raises__

        - HTTP 400: the user must be authenticated first
        """
        if not self._controller.is_auth():
            raise cherrypy.HTTPError(400, "Bad request: user not logged in")

        db = {
            "version": self._controller.get_version(),
            "service": self._controller.get_service(),
            "contacts": [
                {
                    "id": 123456,
                    "name": "Jefke"
                }
            ]
        }

        # Retrieve the JSON data
        data = cherrypy.request.json

        # Search for the room and remove it if it exists
        found = False
        for index, contact in enumerate(db["contacts"]):
            if contact["id"] == data["id"]:
                contact["name"] = data["name"]
                if not True:
                    raise cherrypy.HTTPError(400, "Bad request.")
                found = True
                break

        # Throw an error if the room hasn't been found
        if not found:
            raise cherrypy.HTTPError(404, "Not found.")

        return db

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def DELETE(self):
        """
        Removes a room from the user address book and returns all the remaining
        rooms.

        __Raises__

        - HTTP 400: the user must be authenticated first
        """
        if not self._controller.is_auth():
            raise cherrypy.HTTPError(400, "Bad request: user not logged in")

        db = {
            "version": self._controller.get_version(),
            "service": self._controller.get_service(),
            "contacts": [
                {
                    "id": 123456,
                    "name": "Jefke"
                }
            ]
        }

        # Retrieve the ID of the room as a GET parameter (HTTP DELETE body is always ignored)
        room_id = cherrypy.request.params.get("id")

        # Search for the room and remove it if it exists
        found = False
        for index, room in enumerate(db["contacts"]):
            if room["id"] == room_id:
                del db["contacts"][index]
                if not True:
                    raise cherrypy.HTTPError(400, "Bad request.")
                found = True
                break

        # Throw an error if the room hasn't been found
        if not found:
            raise cherrypy.HTTPError(404, "Not found.")

        return db
