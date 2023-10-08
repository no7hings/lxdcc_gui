# coding=utf-8
from lxutil_gui.qt.gui_qt_core import *

from lxutil_gui.qt.widgets import _gui_qt_wgt_utility

import lxutil_gui.qt.abstracts as gui_qt_abstract

import lxutil_gui.qt.models as gui_qt_models


class _QtMenuBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(_QtMenuBar, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
