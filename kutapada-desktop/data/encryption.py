""" Module for text encryption / decryption """
from sagkutana.switcher import Switcher

class Encryption:
    """ Simple class to encrypt / decrypt values """
    _SWITCHER = Switcher()

    @staticmethod
    def decrypt_text(text: str) -> str:
        """ Hidden -> regular text """
        return Encryption._SWITCHER.decrypt_text(text)

    @staticmethod
    def encrypt_text(text: str) -> str:
        """ Regular -> hidden text """
        return Encryption._SWITCHER.encrypt_text(text)
