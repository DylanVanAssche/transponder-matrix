#!/usr/bin/python3

import abc
import cherrypy
import json
import urllib

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

class EndpointHelper(object):
    """
    EndpointHelper provides several helper functions as static methods for all
    the endpoints.
    """

    @staticmethod
    def prepare_payload(controller, payload):
        """
        Adds the default properties to the given payload.

        __Parameters__

        - controller: the MVC controller instance
        - payload: the data required for the endpoint

        __Returns__

        - payload: the data required for the endpoint with the default
        properties added.
        """
        payload["version"] = controller.version
        payload["service"] = controller.service
        return payload

    @staticmethod
    def decode(text):
        """
        Encapsulates the `urllib.parse.unquote` to centralize the `urllib`
        dependency.

        __Parameters__

        - text: encoded text

        __Returns__

        - text: decoded text
        """
        return urllib.parse.unquote(text)

    @staticmethod
    def json_error_page(status, message, traceback, version):
        response = cherrypy.response
        response.headers["Content-Type"] = "application/json"
        return json.dumps({
            "status": status,
            "message": message,
            "traceback": traceback
        })
