# coding:utf-8
from lxutil import utl_configure

import lxgui.proxy.widgets as prx_widgets

from lxgui.qt.widgets import _gui_qt_wgt_chart


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        c = _gui_qt_wgt_chart.QtChartAsWaiting()
        self.add_widget(c)
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
