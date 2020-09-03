"""Widget for CRUD tree"""
from abc import ABC
from PyQt5.Qt import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from incubus import IncubusFactory
from gui.toolkit import GuiToolkit, WidgetState


class CrudTree(ABC):
    """Abstract tree class"""
    def __init__(self, # pylint: disable=R0913
                 state: WidgetState,
                 external_selected_handler,
                 internal_selected_handler,
                 add_handler,
                 del_handler,
                 change_handler,
                 title: str):
        self.state = state
        self.external_selected_handler = external_selected_handler
        self.model = GuiToolkit.create_tree_model(self.state.main_widget, title)

        self.tree = GuiToolkit.create_tree_view(
            self.model,
            internal_selected_handler,
            change_handler)

        self._del_handler = del_handler

        add_button = QPushButton("+")
        add_button.clicked.connect(add_handler)
        del_button = QPushButton("-")
        del_button.clicked.connect(self._del_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(del_button)

        self.crud_layout = QVBoxLayout()
        self.crud_layout.addWidget(self.tree)
        self.crud_layout.addLayout(button_layout)

        self._incubus = IncubusFactory.get_instance()

    def clear_model(self):
        """Removes all items from model"""
        self._incubus.user_event()
        self.model.removeRows(0, self.model.rowCount())

    def flush_layout(self):
        """Sends CRUD layout to main layout"""
        self._incubus.user_event()
        self.state.main_layout.addLayout(self.crud_layout)

    def locate(self, pattern: str):
        """ Locates the element matching the given name """
        self._incubus.user_event()
        upper_pattern = pattern.upper()
        for row_index in range(0, self.model.rowCount()-1):
            row = self.model.item(row_index)
            row_text = row.data(0).upper()
            if upper_pattern in row_text:
                index = self.model.index(row_index, 0)
                self.tree.setCurrentIndex(index)
                return

    def _del_clicked(self):
        self._incubus.user_event()
        if GuiToolkit.are_you_sure("Delete item?"):
            self._del_handler()
