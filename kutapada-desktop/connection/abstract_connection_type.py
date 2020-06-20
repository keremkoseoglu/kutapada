""" Abstract connection type module """
from abc import ABC, abstractmethod


class AbstractConnectionType(ABC):
    """ Connection type abstract class """

    @property
    @abstractmethod
    def args_template(self) -> dict:
        """ Returns a template for setup """

    @abstractmethod
    def connect(self, args: dict, credential: str):
        """ Opens a connection to the system """
