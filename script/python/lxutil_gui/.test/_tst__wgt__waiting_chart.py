# coding:utf-8
from lxutil import utl_configure

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_chart


class W(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        c = _utl_gui_qt_wgt_chart.QtWaitingChart()
        self.set_widget_add(c)
        c._start_waiting_()

    def test(self):
        pass


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((800, 800))
    w.set_window_show()
    #
    sys.exit(app.exec_())
