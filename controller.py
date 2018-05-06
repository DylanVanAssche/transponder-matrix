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

    def add_room(self, room_id):
        return self._model.add_room(room_id)

    def remove_room(self, room_id):
        return self._model.remove_room(room_id)

    def messages(self, room_id):
        return self._model.messages(room_id)

    def send_text(self, room_id, text):
        return self._model.send_text(room_id, text)

    @property
    def is_auth(self):
        return self._model.token is not None

    @property
    def version(self):
        return self._model.version

    @property
    def service(self):
        return self._model.service

    @property
    def contacts(self):
        return self._model.rooms

if __name__ == "__main__":
    c = Controller()
