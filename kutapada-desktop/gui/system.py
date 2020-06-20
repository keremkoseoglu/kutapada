"""System widget module"""
from PyQt5.Qt import QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPlainTextEdit, QPushButton
from data.database import System
from gui.crud_tree import CrudTree
from gui.toolkit import GuiToolkit, WidgetState


class SystemWidget(CrudTree):
    """System widget main class"""
    def __init__(self, state: WidgetState, system_selected_handler, login_handler):

        super().__init__(state,
                         system_selected_handler,
                         self._system_select,
                         self._system_add,
                         self._system_del,
                         self._system_change,
                         "System")

        self._repainting = False
        connection_label = QLabel("Connection")
        self._connection = QPlainTextEdit()
        connection_login = QPushButton("SAP Login")
        connection_login.clicked.connect(login_handler)
        connection_save = QPushButton("Save")
        connection_save.clicked.connect(self._connection_save_clicked)
        connection_layout = QVBoxLayout()
        connection_layout.addWidget(connection_label)
        connection_layout.addWidget(self._connection)
        connection_layout.addWidget(connection_save)
        connection_layout.addWidget(connection_login)
        self.crud_layout.addLayout(connection_layout)

        self.flush_layout()
        self._selected_system = System()
        self._repaint_systems()

    @property
    def selected_system(self) -> System:
        """Returns the selected system on the GUI"""
        return self._selected_system

    @property
    def connection_text(self) -> str:
        """ Returns the current text in the connection box """
        return self._connection.toPlainText()

    def _connection_save_clicked(self):
        self.selected_system.connection = self.connection_text
        self.state.database.update_system(self.selected_system)

    def _repaint_systems(self):
        self._repainting = True
        self.clear_model()
        for system in self.state.database.systems:
            index = self.model.rowCount()
            self.model.insertRow(index)
            self.model.setData(self.model.index(index, 0), system.name)
        self.tree.repaint()
        self._selected_system = System()
        self._connection.setPlainText("")
        self._repainting = False

    def _system_add(self):
        self.state.database.create_system()
        self._repaint_systems()

    def _system_change(self, selected_row):
        if self._repainting:
            return
        new_name = selected_row.data()
        if new_name == self._selected_system.name:
            return
        if self.state.database.does_system_exist(new_name):
            self._repaint_systems()
            return
        self.state.database.rename_system(self._selected_system.name, new_name)
        self._repaint_systems()

    def _system_del(self):
        self.state.database.delete_system(self.selected_system.name)
        self._repaint_systems()

    def _system_select(self):
        try:
            selected_row = GuiToolkit.get_selected_tree_row_index(self.tree)
        except Exception: # pylint: disable=W0703
            return

        self._selected_system = self.state.database.get_system_by_index(selected_row)
        self._connection.setPlainText(self._selected_system.connection)
        self.external_selected_handler()
