# coding:utf-8

from lxgui.proxy.widgets import _gui_prx_wdt_utility, _gui_prx_wdt_node, _

from lxgui.qt.widgets import _gui_qt_wgt_chart


class TestWindow(_gui_prx_wdt_utility.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        wdt = _gui_qt_wgt_chart.QtChartAsRgbaChoose()
        self.set_qt_widget_add(wdt)


if __name__ == '__main__':
    import time
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()
    w._test_()
    #
    sys.exit(app.exec_())
