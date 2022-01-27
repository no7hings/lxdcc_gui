# coding:utf-8

import lxutil_gui.proxy.widgets as utl_prx_widgets


class TestWindow(utl_prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        n = utl_prx_widgets.PrxNode()
        self.set_widget_add(n)

        p = n.set_port_add(
            utl_prx_widgets.PrxRsvProjectChoosePort('project', 'Project')
        )
        p.port_entry.set_history_show_latest()


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
    #
    sys.exit(app.exec_())
