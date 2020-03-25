"""Primary GUI module"""

from PyQt5.Qt import QHBoxLayout, QWidget
from data.database import DatabaseFactory
from gui.credential import CredentialWidget
from gui.account import AccountWidget
from gui.system import SystemWidget
from gui.toolkit import WidgetState


class Prime(QWidget):
    """ Main GUI window """

    def __init__(self):
        super().__init__()
        self._widget_state = WidgetState(DatabaseFactory.get_instance(), self, QHBoxLayout())
        self._system_widget = SystemWidget(self._widget_state, self._system_selected)
        self._account_widget = AccountWidget(self._widget_state, self._account_selected)
        self._credential_widget = CredentialWidget(self._widget_state)
        self.setLayout(self._widget_state.main_layout)
        self.setWindowTitle("Kutapada")
        self.show()

    def _account_selected(self):
        self._credential_widget.selected_account = self._account_widget.selected_account

    def _system_selected(self):
        self._account_widget.selected_system = self._system_widget.selected_system
        self._credential_widget.selected_system = self._system_widget.selected_system
