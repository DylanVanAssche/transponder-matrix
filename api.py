#!/usr/bin/python3

"""
The API starts the CherryPy webserver and exposes the needed endpoints on the
localhost.
"""

import cherrypy
from endpoints import RootEndpoint, AuthEndpoint, ContactsEndpoint, MessagesEndpoint, EndpointHelper

__all__ = ["API"]

class API(object):
    def __init__(self, controller):
        self._controller = controller

        cherrypy.config.update({
            "global": {
                "server.socket_host": "127.0.0.1",
                "server.socket_port": 3000,
            }
        })

        cherrypy.tree.mount(RootEndpoint())
        cherrypy.tree.mount(AuthEndpoint(self._controller), "/auth",
            {"/":
                {
                    "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                    "error_page.default": EndpointHelper.json_error_page
                }
            }
        )
        cherrypy.tree.mount(ContactsEndpoint(self._controller), "/contacts",
            {"/":
                {
                    "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                    "error_page.default": EndpointHelper.json_error_page
                }
            }
        )

        cherrypy.engine.start()
        cherrypy.engine.block()
