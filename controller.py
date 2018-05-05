#!/usr/bin/python3

"""
The Controller starts the Matrix.org Python daemon and maintains control.
This script initialize the needed modules before it runs the daemon.
"""

import cherrypy
import matrix_client
from model import Model
from api import API

class Controller(object):
    def __init__(self):
        self._model = Model(self)
        self._api = API(self)

    def auth(self, username, password, server, new):
        return self._model.auth(username, password, server, new)

    def is_auth(self):
        return self._model.token is not None

    def get_version(self):
        return self._model.version

    def get_service(self):
        return self._model.service

    def get_contacts(self):
        return self._model.rooms

if __name__ == "__main__":
    c = Controller()
