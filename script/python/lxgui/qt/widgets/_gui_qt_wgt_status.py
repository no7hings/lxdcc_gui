# coding=utf-8
from lxgui.qt.core import *

import lxgui.configure as gui_configure


class QtStatusBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(QtStatusBar, self).__init__(*args, **kwargs)

        self.setFixedHeight(gui_configure.Size.InputHeight)
