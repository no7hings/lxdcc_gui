# coding:utf-8
import os

import six

from lxbasic import bsc_core

import fnmatch

import lxgui.proxy.widgets as prx_widgets

y_f = '{}.yml'.format(os.path.splitext(__file__)[0])

c = bsc_core.StgFileOpt(y_f).set_read()


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([480, 720])
        f = prx_widgets.PrxFilterBar()
        f.set_history_key('filter.test')
        self.add_widget(f)
        f.set_completion_gain_fnc(self._value_completion_gain_fnc_)
        self._test_()

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        k = args[0]
        if isinstance(k, six.text_type):
            k = k.encode('utf-8')
        return fnmatch.filter(
            ['test'], '*{}*'.format(k)
        )

    def _test_(self):
        s = prx_widgets.PrxVScrollArea()
        self.add_widget(s)
        n = prx_widgets.PrxNode('root')
        s.add_widget(n)
        n.create_ports_by_data(
            c
        )

        # n.get_port('files.list').set_root('/data/e/workspace/lynxi/script/python/.resources/icons')
        # n.set('files.list', ['/data/e/workspace/lynxi/script/python/.resources/icons/add.svg'])
        #
        # n.get_port('files.tree').set_root('/data/e/workspace/lynxi/script/python/.resources/icons')
        # n.set('files.tree', ['/data/e/workspace/lynxi/script/python/.resources/icons/add.svg'])


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
