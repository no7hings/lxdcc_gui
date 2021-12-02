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
            utl_prx_widgets.PrxIntegerArrayPort(
                'test_0',
                'Test-0'
            )
        )
        # p.set_value_type(float)
        p.set_value_size(2)
        p.set([1, 2])

        print p.get()

        p = n.set_port_add(
            utl_prx_widgets.PrxOpenFilePathPort('test_1', 'Test-1')
        )
        p.set('a')
        p.set_use_as_storage(True)


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
