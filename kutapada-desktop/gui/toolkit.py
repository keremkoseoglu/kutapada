""" QT toolkit """

from PyQt5.Qt import QStandardItemModel, QHBoxLayout, QTreeView, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from data.database import Database
from config.config import ConfigFactory

class GuiToolkit:
    """ QT toolkit """

    @staticmethod
    def are_you_sure(question: str) -> bool:
        """Asks the user if he/she wants to continue"""
        reply = QMessageBox(QMessageBox.Question,
                            "Error",
                            question,
                            QMessageBox.Yes | QMessageBox.No).exec_()
        return reply == QMessageBox.Yes

    @staticmethod
    def create_tree_model(parent: QWidget, title: str) -> QStandardItemModel:
        """ Creates a new tree model within the given parent """
        output = QStandardItemModel(0, 1, parent)
        output.setHeaderData(0, Qt.Horizontal, title)
        return output

    @staticmethod
    def create_tree_view(model: QStandardItemModel,
                         select_event_handler,
                         change_event_handler) -> QTreeView:
        """ Creates a new tree view """
        conf = ConfigFactory.get_instance()

        output = QTreeView()
        output.setRootIsDecorated(False)
        output.setAlternatingRowColors(True)
        output.setModel(model)
        output.selectionModel().selectionChanged.connect(select_event_handler)
        output.setStyleSheet("QTreeView { font-size: " + str(conf.font_size) + "pt; }")
        model.dataChanged.connect(change_event_handler)
        return output

    @staticmethod
    def get_selected_tree_row_index(tree: QTreeView) -> int:
        """Get index of selected row"""
        indexes = tree.selectedIndexes()
        if indexes is None or len(indexes) <= 0:
            raise Exception("No index selected")
        return int(indexes[0].row())


class WidgetState: # pylint: disable=R0903
    """Common widget variables"""
    def __init__(self, database: Database, main_widget: QWidget, main_layout: QHBoxLayout):
        self.database = database
        self.main_widget = main_widget
        self.main_layout = main_layout
