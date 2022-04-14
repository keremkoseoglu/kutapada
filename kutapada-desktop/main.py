"""Main entry point"""
import os
from PyQt5.Qt import QApplication
import qdarkstyle
from gui.prime import Prime

def run_app():
    """ Runs the application """
    APP = QApplication([])
    APP.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    P = Prime()
    os._exit(APP.exec_()) # pylint: disable=W0212

if __name__ == "__main__":
    run_app()
