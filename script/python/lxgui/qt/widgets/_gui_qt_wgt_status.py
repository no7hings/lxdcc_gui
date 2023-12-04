# coding=utf-8
from lxgui.qt.wrap import *

import lxgui.core as gui_core


class QtStatusBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(QtStatusBar, self).__init__(*args, **kwargs)

        self.setFixedHeight(gui_core.GuiSize.InputHeight)
