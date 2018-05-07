#!/usr/bin/python3

import cherrypy
from .endpoint import RestAPIEndpoint, EndpointHelper
from .messages import MessagesEndpoint
from matrix_client.errors import MatrixRequestError

__all__ = ["ContactsEndpoint"]

@cherrypy.popargs("room_id") # /contacts/{room_id} global available for subendpoints as /contacts/{room_id}/messages
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
        self.messages = MessagesEndpoint(self._controller)

    @cherrypy.tools.json_out()
    def GET(self, room_id=None):
        """
        Reads all the rooms of the user and returns them.

        __Raises__

        - HTTP 400: the user must be authenticated first
        """
        if not self._controller.is_auth:
            raise cherrypy.HTTPError(400, "User isn't logged in!")

        payload = {
            "contacts": self._controller.contacts
        }

        return EndpointHelper.prepare_payload(self._controller, payload)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, room_id):
        """
        Adds a new room to the user address book and returns all the rooms.
        Automatically handles the difference between a new room and joining an
        existing room. When the room doesn't exist, the room is created.

        __Raises__

        - HTTP 400: the user must be authenticated first
        - HTTP 500: internal server error with traceback
        """
        if not self._controller.is_auth:
            raise cherrypy.HTTPError(400, "User isn't logged in!")

        # Retrieve the room_id
        room_id = EndpointHelper.decode(room_id) # URL decoding

        # Raise HTTP 400 when adding a room fails
        try:
            self._controller.add_room(room_id)
        except MatrixRequestError as e:
            cherrypy.HTTPError(e.code, e.content)
        except Exception as e:
            cherrypy.HTTPError(500, str(e))

        payload = {
            "contacts": self._controller.contacts
        }

        return EndpointHelper.prepare_payload(self._controller, payload)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def DELETE(self, room_id=None):
        """
        Removes a room from the user address book and returns all the remaining
        rooms.

        __Raises__

        - HTTP 400: the user must be authenticated first
        """
        if not self._controller.is_auth:
            raise cherrypy.HTTPError(400, "User isn't logged in!")

        try:
            room_id = EndpointHelper.decode(room_id) # URL decoding
            self._controller.remove_room(room_id)
        except MatrixRequestError as e:
            raise cherrypy.HTTPError(e.code, e.content)
        except Exception as e:
            raise cherrypy.HTTPError(500, str(e))

        payload = {
            "contacts": self._controller.contacts
        }
        return EndpointHelper.prepare_payload(self._controller, payload)
