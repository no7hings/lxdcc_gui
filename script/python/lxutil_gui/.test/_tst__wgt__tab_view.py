# coding:utf-8

import lxutil_gui.proxy.widgets as utl_prx_widgets

import lxresolver.commands as rsv_commands


class TestWindow(utl_prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        n = utl_prx_widgets.PrxTabView()
        self.add_widget(n)
        v_0 = utl_prx_widgets.PrxTreeView()
        n.set_item_add(
            v_0.widget, name='test - 0', icon_name_text='test - 0'
        )
        v_1 = utl_prx_widgets.PrxListView()
        n.set_item_add(
            v_1.widget, name='test - aaaaaaaaaaaa'
        )


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
