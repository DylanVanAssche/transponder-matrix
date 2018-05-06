#!/usr/bin/python3

import cherrypy
from .endpoint import RestAPIEndpoint, EndpointHelper

class MessagesEndpoint(RestAPIEndpoint):
    """
    __/{contact_id}/messages__ contains all the messages for the contact with the
    given ID.

    Implemented HTTP REST methods:

    - __GET__: Reads all the messages of the contact
    - __POST__: Sends a new message to the contact
    - __PUT__: Modifies a message (already sent)
    - __DELETE__: Deletes a message (already sent)
    """
    def __init__(self, controller):
        super().__init__(controller)

    @cherrypy.tools.json_out()
    @cherrypy.popargs("room_id")
    def GET(self, room_id):
        """
        __Raises__

        - HTTP 400: the user must be authenticated first
        """
        if not self._controller.is_auth:
            raise cherrypy.HTTPError(400, "User isn't logged in!")

        room_id = EndpointHelper.decode(room_id)

        payload = {
            "messages": self._controller.messages(room_id)
        }
        return EndpointHelper.prepare_payload(self._controller, payload)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.popargs("room_id")
    def POST(self, room_id):
        if not self._controller.is_auth:
            raise cherrypy.HTTPError(400, "User isn't logged in!")

        # Retrieve the JSON data
        data = cherrypy.request.json

        room_id = EndpointHelper.decode(room_id)
        payload = {
            "send": self._controller.send_text(room_id, data["content"])
        }
        return EndpointHelper.prepare_payload(self._controller, payload)
