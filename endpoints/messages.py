#!/usr/bin/python3

import cherrypy

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
    pass
