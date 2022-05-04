"""Primary GUI module"""
import json
from PyQt5.Qt import QHBoxLayout, QWidget
from data.database import DatabaseFactory
from gui.credential import CredentialWidget
from gui.account import AccountWidget
from gui.system import SystemWidget
from gui.toolkit import WidgetState
from connection.sap_connection import SapConnection
from config.config import ConfigFactory


class Prime(QWidget):
    """ Main GUI window """

    def __init__(self):
        super().__init__()
        conf = ConfigFactory.get_instance()

        self._widget_state = WidgetState(DatabaseFactory.get_instance(), self, QHBoxLayout())

        self._system_widget = SystemWidget(
            self._widget_state,
            self._system_selected,
            self._login_clicked)

        self._account_widget = AccountWidget(self._widget_state, self._account_selected)
        self._credential_widget = CredentialWidget(self._widget_state)
        self.setLayout(self._widget_state.main_layout)
        self.setWindowTitle("Kutapada")
        self._system_widget.focus_on_locate()
        self.resize(conf.prime_width, conf.prime_height)
        self.show()

    def _account_selected(self):
        self._credential_widget.selected_account = self._account_widget.selected_account

    def _system_selected(self):
        self._credential_widget.selected_system = self._system_widget.selected_system
        self._account_widget.selected_system = self._system_widget.selected_system

    def _login_clicked(self):
        conn_text = self._system_widget.connection_text
        if conn_text is None or conn_text == "":
            return
        conn_dict = json.loads(conn_text)
        credential = self._credential_widget.value
        SapConnection().connect(conn_dict, credential)
