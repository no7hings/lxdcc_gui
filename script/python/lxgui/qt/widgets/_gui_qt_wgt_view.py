# coding=utf-8
from lxgui.qt.wrap import *


class _QtMenuBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(_QtMenuBar, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
