# coding:utf-8
from lxutil_gui.qt import gui_qt_core

import lxutil_gui.proxy.widgets as prx_widgets


def process_fnc_(w_):
    from lxutil import utl_process
    w_.start(
        utl_process.PythonProcess.generate_command(
            'method=test'
        )
    )


w = gui_qt_core.show_prx_window_auto(
    prx_widgets.PrxProcessingWindow, process_fnc=process_fnc_, show_kwargs=dict(exclusive=False)
)
