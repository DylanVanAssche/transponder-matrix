#!/usr/bin/python3

import cherrypy
from .endpoint import RestAPIEndpoint, EndpointHelper
from matrix_client.errors import MatrixRequestError

__all__ = ["AuthEndpoint"]

class AuthEndpoint(RestAPIEndpoint):
    """
    __/auth__ creates user accounts or logs the user in on a given server

    Implemented HTTP REST methods:

    - __POST__: Adds a new rooms of the user
    """
    def __init__(self, controller):
        super().__init__(controller)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """
        Authenticates the user on the given server, if the `new` property is
        set to `true` then a new account is created for the user, otherwise the
        user is logged in on the given server.

        __Parameters__

        - username: Matrix username for the given server
        - password: Matrix password for the given server
        - server: Matrix server URL
        - new: `true` = creates a new user account on the given server, `false`
        logs the user in on the server

        __Raises__

        - HTTP 400: Wrong username/password or other issues with the authentication flow.
        """
        # Retrieve the JSON data
        data = cherrypy.request.json

        # Perform authentication
        try:
            token = self._controller.auth(
                data["username"],
                data["password"],
                data["server"],
                data["new"]
            )
        except MatrixRequestError as e:
            # HTTP 401 when captcha is required for registration
            if e.code == 401:
                raise cherrypy.HTTPError(400, "Authentication failed due missing captcha support, create an account on the server via a webbrowser first.\n {0}".format(e))

             # HTTP 403 when password/username is wrong
            elif e.code == 403:
                raise cherrypy.HTTPError(403, "Username or password is wrong!")

            # Unknown HTTP error
            raise cherrypy.HTTPError(e.code, e.content)

        # Return the token and meta data on success.
        payload = {
            "token": token
        }
        return EndpointHelper.prepare_payload(self._controller, payload)
