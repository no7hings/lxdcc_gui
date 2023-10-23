# coding:utf-8
from lxgui.qt.core import *

app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QMessageBox()

w.setSizeGripEnabled(True)

w.setSizeIncrement(800, 600)

w.exec_()
sys.exit(app.exec_())
