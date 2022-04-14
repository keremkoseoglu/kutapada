import cProfile
from PyQt5.Qt import QApplication
import qdarkstyle
from gui.prime import Prime


APP = QApplication([])
APP.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
P = Prime()
#os._exit(APP.exec_()) # pylint: disable=W0212
#cProfile.run("5+5")
cProfile.run("APP.exec_()")