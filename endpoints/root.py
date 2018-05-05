#!/usr/bin/python3

import cherrypy

class RootEndpoint(object):
    @cherrypy.expose
    def index(self):
        return "Hello world"
