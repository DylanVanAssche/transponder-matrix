#!/usr/bin/python3

"""
The Controller starts the Matrix.org Python daemon and maintains control.
This script initialize the needed modules before it runs the daemon.
"""

import cherrypy
import matrix_client
import sys
from daemonator import Daemon
from model import Model
from api import API

__all__ = ["Controller"]

class Controller(Daemon):
    def run(self):
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
    # Define a PIDFile location (typically located in /tmp or /var/run)
    daemon = Controller("/tmp/transponder_matrix_daemon.pid")
    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            daemon.start()
        elif "stop" == sys.argv[1]:
            daemon.stop()
        elif "restart" == sys.argv[1]:
            daemon.restart()
        elif "status" == sys.argv[1]:
            daemon.status()
        else:
            sys.stdout.write("Unknown command\n")
            sys.exit(2)
        sys.exit(0)
    else:
        sys.stdout.write("Usage: %s start|stop|restart|status\n" % sys.argv[0])
        sys.exit(2)
