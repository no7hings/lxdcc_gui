# coding:utf-8
import os

from lxbasic import bsc_core

import fnmatch

import lxutil_gui.proxy.widgets as utl_prx_widgets

y_f = '{}.yml'.format(os.path.splitext(__file__)[0])

c = bsc_core.StorageFileOpt(y_f).set_read()


class TestWindow(utl_prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([480, 960])
        f = utl_prx_widgets.PrxFilterBar()
        f.set_history_key('filter.test')
        self.set_widget_add(f)
        f.set_filter_completion_gain_fnc(self._value_completion_gain_fnc_)
        self._test_()

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        return fnmatch.filter(
            ['test'], '*{}*'.format(args[0])
        )

    def _test_(self):
        n = utl_prx_widgets.PrxNode_('root')
        self.set_widget_add(n)
        n.set_ports_create_by_configure(
            c
        )


if __name__ == '__main__':

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
