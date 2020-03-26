""" Account widget module """
from data.database import Account, System
from gui.crud_tree import CrudTree
from gui.toolkit import GuiToolkit, WidgetState


class AccountWidget(CrudTree):
    """ System widget main class """
    def __init__(self, state: WidgetState, account_selected_handler):
        super().__init__(state,
                         account_selected_handler,
                         self._account_select,
                         self._account_add,
                         self._account_del,
                         self._account_change,
                         "Account")
        self._repainting = False
        self.flush_layout()
        self._selected_system = System()
        self._selected_account = Account()
        self._repaint_accounts()

    @property
    def selected_account(self) -> Account:
        """ Returns the selected system on the GUI """
        return self._selected_account

    @property
    def selected_system(self) -> System:
        """ Returns the selected system """
        return self._selected_system

    @selected_system.setter
    def selected_system(self, sys: System):
        """ Setter for selected system """
        self._selected_system = sys
        self._repaint_accounts()

    def _repaint_accounts(self):
        self._repainting = True
        self.clear_model()
        for account in self._selected_system.accounts:
            index = self.model.rowCount()
            self.model.insertRow(index)
            self.model.setData(self.model.index(index, 0), account.name)
        self.tree.repaint()
        self._selected_account = Account()
        self._repainting = False

    def _repaint_selected_system(self):
        self.selected_system = self.state.database.get_system_by_name(self.selected_system.name)

    def _account_add(self):
        self.state.database.create_account(self.selected_system.name)
        self._repaint_selected_system()

    def _account_change(self, selected_row):
        if self._repainting:
            return
        new_name = selected_row.data()
        if new_name == self._selected_account.name:
            return
        if self.state.database.does_account_exist(self._selected_system.name, new_name):
            self._repaint_selected_system()
            return
        self.state.database.rename_account(self._selected_system.name,
                                           self._selected_account.name,
                                           new_name)
        selected_account_backup = self._selected_account
        self._repaint_selected_system()
        self._selected_account = selected_account_backup

    def _account_del(self):
        self.state.database.delete_account(self.selected_system.name, self.selected_account.name)
        self._repaint_selected_system()

    def _account_select(self):
        try:
            selected_row = GuiToolkit.get_selected_tree_row_index(self.tree)
        except Exception:
            return

        if selected_row > len(self._selected_system.accounts) - 1:
            return

        self._selected_account = self._selected_system.accounts[selected_row]
        self.external_selected_handler()
