""" Systems with passwords """
from typing import List


class Account:
    """ An account within a system """
    def __init__(self, name: str = None, credential: str = None):
        if name is None:
            self.name = ""
        else:
            self.name = name

        if credential is None:
            self.credential = ""
        else:
            self.credential = credential


class System:
    """ A system with passwords """
    def __init__(self, name: str = None, connection: str = None, accounts: List[Account] = None):
        if name is None:
            self.name = ""
        else:
            self.name = name

        if connection is None:
            self.connection = ""
        else:
            self.connection = connection

        if accounts is None:
            self.accounts = []
        else:
            self.accounts = accounts
