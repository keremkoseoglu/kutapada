""" Connection protocol module """
from typing import Protocol


class ConnectionType(Protocol):
    """ Connection type abstract class """
    @property
    def args_template(self) -> dict:
        """ Returns a template for setup """

    def connect(self, args: dict, credential: str):
        """ Opens a connection to the system """
