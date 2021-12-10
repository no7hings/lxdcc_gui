# coding:utf-8
from lxutil import utl_core

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_node, _utl_gui_prx_wgt_window


def yes_method():
    _w = utl_core.DialogWindow.set_create(
        'Test-2',
        use_exec=False
    )
    print _w


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    for i in range(20):
        if i == 10:
            w = utl_core.DialogWindow.set_create(
                'Test-1',
                yes_method=yes_method,
                use_exec=False
            )
    #
    sys.exit(app.exec_())
