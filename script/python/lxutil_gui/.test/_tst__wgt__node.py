# coding:utf-8
import time

import lxutil_gui.proxy.widgets as utl_prx_widgets

import lxresolver.commands as rsv_commands


class TestWindow(utl_prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        f = utl_prx_widgets.PrxFilterBar()
        f.set_history_key('filter.test')
        self.set_widget_add(f)
        n = utl_prx_widgets.PrxNode_('root')
        self.set_widget_add(n)
        p = n.set_port_add(
            utl_prx_widgets.PrxDirectoryOpenPort(
                'test_0'
            )
        )
        p = n.set_port_add(
            utl_prx_widgets.PrxMediasPort(
                'test_1'
            )
        )
        # p.set(
        #     '/l/temp/td/dongchangbao/texture_manager'
        # )


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

    # c = 2
    # c2 = 20
    # with w.set_progress_create(maximum=c) as p:
    #     for i in range(c):
    #         p.set_update()
    #         time.sleep(1)
    #         with w.set_progress_create(maximum=c2) as p2:
    #             for j in range(c2):
    #                 time.sleep(1)
    #                 p2.set_update()

    #
    sys.exit(app.exec_())
