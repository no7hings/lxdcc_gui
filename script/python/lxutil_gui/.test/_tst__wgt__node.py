# coding:utf-8

import lxutil_gui.proxy.widgets as utl_prx_widgets


class TestWindow(utl_prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        n = utl_prx_widgets.PrxNode_()
        self.set_widget_add(n)
        # p = n.set_port_add(
        #     utl_prx_widgets.PrxIntegerArrayPort(
        #         'test_0',
        #         'Test-0'
        #     )
        # )
        # # p.set_value_type(float)
        # p.set_value_size(4)
        # p.set([1, 2, 3, 4])
        #
        # p = n.set_port_add(
        #     utl_prx_widgets.PrxDirectoryOpenPort('test_1', 'Test-1')
        # )
        # p.port_entry.set_history_show_latest()
        # p.set_use_as_storage(True)
        n.set_port_add(
            utl_prx_widgets.PrxStringPort(
                'main.test.test_0'
            )
        )
        n.set_port_add(
            utl_prx_widgets.PrxStringPort(
                'main.test.test_1'
            )
        )

        n.set_port_add(
            utl_prx_widgets.PrxStringPort(
                'test.test_2'
            )
        )

        print n.get_port('main.test.test_0')


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
