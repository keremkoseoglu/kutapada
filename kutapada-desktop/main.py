"""Main entry point"""
import os
from PyQt5.Qt import QApplication
import qdarkstyle
from gui.prime import Prime

def run_app():
    """ Runs the application """
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    _ = Prime()
    os._exit(app.exec_()) # pylint: disable=W0212

if __name__ == "__main__":
    run_app()
