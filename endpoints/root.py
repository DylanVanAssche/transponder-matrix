#!/usr/bin/python3

import cherrypy

__all__ = ["Root"]

class RootEndpoint(object):
    @cherrypy.expose
    def index(self):
        return "Hello world"
