# coding:utf-8

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wdt_node

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_chart


class TestWindow(_utl_gui_prx_wdt_utility.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        wdt = _utl_gui_qt_wgt_chart._QtColorChooseChart()
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
