# coding:utf-8
import threading

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets


def yes_method():
    import time
    w.set_content('stated')
    print 'AAA'
    # print A
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
    w = prx_widgets.PrxToolWindow()
    w.set_window_show()
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
