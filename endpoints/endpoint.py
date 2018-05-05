#!/usr/bin/python3

import abc
import cherrypy

class RestAPIEndpoint(object):
    """
    MethodDispatcher for the JSON RestAPI.
    You should override the inheritted HTTP methods, the methods that aren't
    supported by the endpoint will raise a HTTP 405 error.

    Implemented HTTP REST methods:

    - __GET__: Reads data on the endpoint
    - __POST__: Creates data on the endpoint
    - __PUT__: Updates data on the endpoint
    - __DELETE__: Removes data on the endpoint
    """
    __metaclass__ = abc.ABCMeta # Instantiation is NOT allowed
    exposed = True # Makes the MethodDispatcher visible
    @cherrypy.tools.accept(media="application/json") # Make sure we are receiving a JSON request

    def __init__(self, controller):
        self._controller = controller

    def GET(self):
        """
        Handles a HTTP GET request for the endpoint.
        """
        raise cherrypy.HTTPError(405, "Method not implemented.")

    def POST(self):
        """
        Handles a HTTP POST request for the endpoint.
        """
        raise cherrypy.HTTPError(405, "Method not implemented.")

    def PUT(self):
        """
        Handles a HTTP PUT request for the endpoint.
        """
        raise cherrypy.HTTPError(405, "Method not implemented.")

    def DELETE(self):
        """
        Handles a HTTP DELETE request for the endpoint.
        """
        raise cherrypy.HTTPError(405, "Method not implemented.")
