# coding:utf-8
from lxutil import utl_configure

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_chart


class W(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        a = [('deletion', 41, 10), ('addition', 41, 40), ('name-changed', 41, 0), ('path-changed', 41, 0),
             ('path-exchanged', 41, 0), ('face-vertices-changed', 41, 0), ('points-changed', 41, 0),
             ('geometry-changed', 41, 0)]
        b = [('geometry', 41, 400), ('shell', 41, 41), ('area', 324.800048828125, 324.800048828125),
             ('face', 53489.937469401586, 16456), ('edge', 106979.87493880317, 33328),
             ('vertex', 53768.530893721385, 16842)]
        #
        c = _utl_gui_qt_wgt_chart._QtWaitingChart()
        self.set_widget_add(c)
        c._set_waiting_start_()

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
