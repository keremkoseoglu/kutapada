"""Main entry point"""
import sys
from PyQt5.Qt import QApplication
import qdarkstyle
from gui.prime import Prime

APP = QApplication([])
APP.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
P = Prime()
sys.exit(APP.exec_())
