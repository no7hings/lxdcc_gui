# coding:utf-8
from lxusd import usd_setup

# usd_setup.UsdSetup(
#     '/data/e/myworkspace/td/lynxi/workspace/resource/linux/usd'
# ).set_run()

import os

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.qt import gui_qt_core


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.set_definition_window_size([512+4, 512+22])

        v = qt_widgets.QtGLWidget()

        v._save_image_('/data/f/image_render/test_1.jpg')

        self.add_widget(v)


if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_setup

    utl_setup.OcioSetup(
        bsc_core.StgPathMapMtd.map_to_current(
            '/job/PLE/bundle/thirdparty/aces/1.2'
        )
    ).set_run()

    gui_qt_core.show_prx_window_auto(W)

