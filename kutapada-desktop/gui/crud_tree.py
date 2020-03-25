"""Widget for CRUD tree"""
from abc import ABC
from PyQt5.Qt import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from gui.toolkit import GuiToolkit, WidgetState


class CrudTree(ABC):
    """Abstract tree class"""
    def __init__(self,
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
        self.tree = GuiToolkit.create_tree_view(self.model, internal_selected_handler, change_handler)
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

    def clear_model(self):
        """Removes all items from model"""
        self.model.removeRows(0, self.model.rowCount())

    def flush_layout(self):
        """Sends CRUD layout to main layout"""
        self.state.main_layout.addLayout(self.crud_layout)

    def _del_clicked(self):
        if GuiToolkit.are_you_sure("Delete item?"):
            self._del_handler()

