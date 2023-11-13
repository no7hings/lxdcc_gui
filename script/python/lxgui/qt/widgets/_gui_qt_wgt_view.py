# coding=utf-8
from lxgui.qt.core import *

from lxgui.qt.widgets import _gui_qt_wgt_utility

import lxgui.qt.abstracts as gui_qt_abstracts

import lxgui.qt.models as gui_qt_models


class _QtMenuBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(_QtMenuBar, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
