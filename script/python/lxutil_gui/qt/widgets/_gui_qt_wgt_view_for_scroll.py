# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

import lxutil_gui.qt.models as gui_qt_models


class QtHScrollView(QtWidgets.QWidget):
    def _refresh_widget_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_w = self._viewport.layout().minimumSize().width()
        # width use maximum
        abs_w = max(w, v_w)
        self._gui_scroll.set_w(w)
        self._gui_scroll.set_abs_w(abs_w)
        self._gui_scroll.update()
        btn_f_w, btn_f_h = h, h
        btn_w, btn_h = 20, 20
        if self._gui_scroll.get_is_valid():
            btn_w_1, btn_h_1 = btn_w/2, btn_h
            btn_f_w_r = btn_f_w
            c_x_1, c_y_1 = w-btn_f_w_r, y
            c_x_1 = max(c_x_1, btn_f_w_r)
            #
            self._scroll_button_frame.show()
            self._scroll_button_frame.setGeometry(
                c_x_1, c_y_1, btn_f_w_r, btn_f_h
            )
            #
            self._scroll_previous_button.show()
            self._scroll_previous_button.setGeometry(
                c_x_1+(btn_f_w-btn_w)/2, c_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
            )
            if self._gui_scroll.get_is_minimum():
                self._scroll_previous_button._set_icon_file_path_(
                    utl_gui_core.RscIconFile.get('scroll-left-disable')
                )
            else:
                self._scroll_previous_button._set_icon_file_path_(
                    utl_gui_core.RscIconFile.get('scroll-left')
                )
            #
            self._scroll_next_button.show()
            self._scroll_next_button.setGeometry(
                c_x_1+(btn_f_w-btn_w)/2+btn_w_1, c_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
            )
            if self._gui_scroll.get_is_maximum():
                self._scroll_next_button._set_icon_file_path_(
                    utl_gui_core.RscIconFile.get('scroll-right-disable')
                )
            else:
                self._scroll_next_button._set_icon_file_path_(
                    utl_gui_core.RscIconFile.get('scroll-right')
                )
        else:
            self._scroll_button_frame.hide()
            self._scroll_previous_button.hide()
            self._scroll_next_button.hide()
        #
        scroll_value = self._gui_scroll.get_value()
        self._viewport.setGeometry(
            x-scroll_value, y, abs_w, h
        )

    def __init__(self, *args, **kwargs):
        super(QtHScrollView, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self._viewport = QtWidgets.QWidget(self)
        self._viewport.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._viewport.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self._layout = QtWidgets.QHBoxLayout(self._viewport)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)

        self._gui_scroll = gui_qt_models.GuiScroll()
        self._gui_scroll.set_step(64)

        self._scroll_button_frame = _utl_gui_qt_wgt_utility.QtButtonFrame(self)
        self._scroll_button_frame.hide()

        self._scroll_previous_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._scroll_previous_button.hide()
        self._scroll_previous_button._set_icon_geometry_mode_(
            _utl_gui_qt_wgt_utility.QtIconPressButton.IconGeometryMode.Auto
        )
        self._scroll_previous_button.setFixedSize(10, 20)
        self._scroll_previous_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('scroll-left')
        )
        self._scroll_previous_button.press_clicked.connect(self._do_scroll_previous_)

        self._scroll_next_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._scroll_next_button.hide()
        self._scroll_next_button._set_icon_geometry_mode_(
            _utl_gui_qt_wgt_utility.QtIconPressButton.IconGeometryMode.Auto
        )
        self._scroll_next_button.setFixedSize(10, 20)
        self._scroll_next_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('scroll-right')
        )
        self._scroll_next_button.press_clicked.connect(self._do_scroll_next_)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_()
        return False

    def _get_viewport_(self):
        return self._viewport

    def _get_layout_(self):
        return self._layout

    def _do_scroll_previous_(self):
        if self._gui_scroll.step_to_previous():
            self._refresh_widget_()

    def _do_scroll_next_(self):
        if self._gui_scroll.step_to_next():
            self._refresh_widget_()
