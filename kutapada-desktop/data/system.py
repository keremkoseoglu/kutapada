""" Systems with passwords """
from dataclasses import dataclass
from typing import List

@dataclass
class Account: # pylint: disable=R0903
    """ An account within a system """
    name: str = ""
    credential: str = ""

@dataclass
class System: # pylint: disable=R0903
    """ A system with passwords """
    name: str = ""
    connection: str = ""
    accounts: List[Account] = None

    def __post_init__(self):
        if self.accounts is None:
            self.accounts = []
