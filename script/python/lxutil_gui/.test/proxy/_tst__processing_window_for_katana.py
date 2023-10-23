# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as prx_widgets


def process_fnc_(w_):
    from lxutil import utl_process
    w_.start(
        utl_process.PythonProcess.generate_command(
            'method=test'
        )
    )


w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    prx_widgets.PrxProcessingWindow, process_fnc=process_fnc_, show_kwargs=dict(exclusive=False)
)
