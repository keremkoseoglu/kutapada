""" SAP connection module """
import os
from os import path
import time
from threading import Thread
from connection import ConnectionType


class SapConnection(ConnectionType):
    """ SAP connection class """
    KEY_CONN = "conn"
    KEY_CLNT = "clnt"
    KEY_USER = "user"
    KEY_LANG = "lang"
    FILE_NAME = "login.sapc"

    @property
    def args_template(self) -> dict:
        """ Returns a template for setup """
        return {
            SapConnection.KEY_CONN: "",
            SapConnection.KEY_CLNT: "",
            SapConnection.KEY_USER: "",
            SapConnection.KEY_LANG: "",
        }

    def connect(self, args: dict, credential: str):
        """ Opens a connection to the system """
        file_content = "conn=" + args[SapConnection.KEY_CONN]
        file_content += "&clnt=" + args[SapConnection.KEY_CLNT]
        file_content += "&user=" + args[SapConnection.KEY_USER]
        file_content += "&lang=" + args[SapConnection.KEY_LANG]
        file_content += "&expert=true&pass=" + credential

        file_path = path.join(os.getcwd(), SapConnection.FILE_NAME)
        with open(file_path, "w", encoding="utf-8") as tmp_file:
            tmp_file.write(file_content)

        open_thread = Thread(target=self._open_connection_file)
        open_thread.start()

    def _open_connection_file(self):
        file_path = path.join(os.getcwd(), SapConnection.FILE_NAME)
        try:
            os.system(f"open {file_path}")
            time.sleep(10)
        finally:
            os.remove(file_path)
