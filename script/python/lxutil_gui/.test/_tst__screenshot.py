# coding:utf-8
from lxutil_gui.qt.widgets import _gui_qt_wgt_utility

import lxutil_gui.proxy.widgets as prx_widgets


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = prx_widgets.PrxScreenshotFrame()
    w.set_start()
    #
    sys.exit(app.exec_())
