#!/usr/bin/python3

"""
The endpoints submodule contains all the exposed HTTP REST endpoints code.
All endpoints are inheritted from the RestAPIEndpoint abstract base class.
"""

from .root import RootEndpoint
from .auth import AuthEndpoint
from .contacts import ContactsEndpoint
