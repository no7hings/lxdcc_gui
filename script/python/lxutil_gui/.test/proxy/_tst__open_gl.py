# coding:utf-8
from lxbasic import bsc_core

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.core as gui_prx_core

import lxusd_gui.qt.widgets as usd_qt_widgets

bsc_core.Log.TEST = True


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.set_definition_window_size([512+4, 512+22])

        v = usd_qt_widgets.QtGLWidget()

        self.add_widget(v)


if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_setup

    utl_setup.OcioSetup(
        bsc_core.StgPathMapMtd.map_to_current(
            '/job/PLE/bundle/thirdparty/aces/1.2'
        )
    ).set_run()

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(W)

