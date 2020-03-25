""" Module for credential based GUI elements """

import pyperclip
from PyQt5.Qt import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox, QPlainTextEdit, QPushButton
from data.database import Account, System
from gui.toolkit import WidgetState


class CredentialWidget:
    """ Main class """
    def __init__(self, state: WidgetState):
        self._state = state
        self._credential = QPlainTextEdit(self._state.main_widget)
        self._selected_account = Account()
        self._selected_system = System()
        self._internal_value = ""
        self._displayed_value = ""
        self._masked = True

        toggle_mask = QPushButton("Toggle")
        toggle_mask.clicked.connect(self._toggle_clicked)
        copy_pwd = QPushButton("Copy")
        copy_pwd.clicked.connect(self._copy_clicked)
        credential_save = QPushButton("Save")
        credential_save.clicked.connect(self._credential_save_clicked)
        button_layout = QHBoxLayout()
        button_layout.addWidget(toggle_mask)
        button_layout.addWidget(copy_pwd)
        button_layout.addWidget(credential_save)

        credential_layout = QVBoxLayout()
        credential_layout.addWidget(self._credential)
        credential_layout.addLayout(button_layout)

        self._state.main_layout.addLayout(credential_layout)

    @property
    def masked(self) -> bool:
        """Are credentials hidden"""
        return self._masked

    @masked.setter
    def masked(self, new_masked: bool):
        """Are credentials hidden"""
        self._masked = new_masked
        self._build_displayed_value()

    @property
    def selected_account(self) -> Account:
        """ selected account """
        return self._selected_account

    @selected_account.setter
    def selected_account(self, account: Account):
        """ selected account """
        self._selected_account = account
        self._repaint_credential()

    @property
    def selected_system(self) -> System:
        """ selected system """
        return self._selected_system

    @selected_system.setter
    def selected_system(self, system: System):
        """ selected system """
        self._selected_system = system
        self.selected_account = Account()

    @property
    def value(self) -> str:
        """ Credential value """
        return self._internal_value

    @value.setter
    def value(self, val: str):
        """ Credential value """
        self._internal_value = val
        self._build_displayed_value()

    def _copy_clicked(self):
        pyperclip.copy(self.value)

    def _build_displayed_value(self):
        if self.masked:
            self._displayed_value = ""
            for internal_char in self._internal_value:
                self._displayed_value += "*"
        else:
            self._displayed_value = self._internal_value
        self._credential.setPlainText(self._displayed_value)

    def _credential_save_clicked(self):
        if self.masked:
            QMessageBox(QMessageBox.Critical, "Error", "Unmask before saving").exec_()
            return
        self.value = self._credential.toPlainText()
        self._selected_account.credential = self.value
        self._state.database.update_system(self._selected_system)

    def _repaint_credential(self):
        self.value = self._selected_account.credential

    def _toggle_clicked(self):
        if self._masked:
            self.masked = False
        else:
            self.masked = True
