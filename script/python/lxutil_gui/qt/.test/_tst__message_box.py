# coding:utf-8
from lxutil_gui.qt.gui_qt_core import *

app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QMessageBox()

w.setSizeGripEnabled(True)

w.setSizeIncrement(800, 600)

w.exec_()
sys.exit(app.exec_())
