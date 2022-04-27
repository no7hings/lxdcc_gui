# coding:utf-8
import threading

from lxutil import utl_core

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_node, _utl_gui_prx_wgt_window


def yes_method():
    # _w = utl_core.DialogWindow.set_create(
    #     'Test-2',
    #     use_exec=False
    # )
    # print _w
    import time
    w.set_content('stated')
    print 'AAA'
    print w.get_options_as_kwargs()
    time.sleep(5)
    print 'BBB'
    w.set_content_add('test')
    w.set_content_add('completed')


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
                use_exec=False,
                options_configure={
                    'user/description': {
                        'widget': 'script',
                        'value': u'测试',
                        'enable': False,
                        'tool_tip': '...'
                    }
                }

            )
    #
    sys.exit(app.exec_())
