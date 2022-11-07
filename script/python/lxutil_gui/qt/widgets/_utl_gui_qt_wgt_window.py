# coding=utf-8
import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_view


class _QtWindow(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._main_layout = QtVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        #
        self._set_frame_def_init_()
        #
        self._frame_background_color = 63, 63, 63, 255
        self._hovered_frame_background_color = 63, 63, 63, 255
        #
        self._menu_bar = _utl_gui_qt_wgt_view._QtMenuBar()
        self._main_layout.addWidget(self._menu_bar)

    def _set_widget_geometries_update_(self):
        pos_x, pos_y = 0, 0
        width, height = self.width(), self.height()
        self._set_frame_draw_geometry_(
            pos_x, pos_y, width, height
        )

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._set_widget_geometries_update_()
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            background_color=self._frame_background_color,
            border_color=self._frame_border_color
        )


class _QtFramelessWindow(
    QtWidgets.QWidget
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtFramelessWindow, self).__init__(*args, **kwargs)
        #
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        #
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._main_layout = QtVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._header = _utl_gui_qt_wgt_item._QtWindowHead()
        self._main_layout.addWidget(self._header)
        #
        self._main_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._main_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self._main_layout.addWidget(self._main_widget)

