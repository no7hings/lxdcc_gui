# coding:utf-8
from ..qt import gui_qt_core


def get_gui_proxy_by_class(gui_class):
    lis = []
    # noinspection PyArgumentList
    widgets = gui_qt_core.QtWidgets.QApplication.topLevelWidgets()
    if widgets:
        for w in widgets:
            if hasattr(w, 'gui_proxy'):
                gui_proxy = w.gui_proxy
                if gui_proxy.__class__.__name__ == gui_class.__name__:
                    lis.append(gui_proxy)
    return lis


class State(object):
    WARNING = 'warning'
    ERROR = 'error'
    NORMAL = 'normal'
