# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

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


class QtGridLayoutView(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtMenuBaseDef,
):
    QT_MENU_CLS = _utl_gui_qt_wgt_utility.QtMenu
    def _refresh_widget_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        m_l, m_t, m_r, m_b = self._layout_margins
        v_x, v_y = m_l, m_t
        v_w, v_h = w-m_l-m_r, h-m_t-m_b
        #
        self._grid_layout_model.set_pos(v_x, v_y)
        self._grid_layout_model.set_size(v_w, v_h)
        self._grid_layout_model.set_item_size(self._item_w, self._item_h)
        self._grid_layout_model.set_item_count(self._item_count)
        self._grid_layout_model.update()
        #
        for i_index in self._indices:
            i_item = self._items[i_index]
            i_x, i_y, i_w, i_h = self._grid_layout_model.get_geometry_at(i_index)
            i_item.setGeometry(
                i_x, i_y, i_w, i_h
            )
            i_item.setFixedSize(i_w, i_h)
            i_item.show()
        #
        abs_w, abs_h = self._grid_layout_model.get_abs_size()
        frm_w, frm_h = abs_w+m_l+m_r, abs_h+m_t+m_b
        self.setMinimumHeight(frm_h)
        #
        self._viewport_rect.setRect(
            v_x, v_y, abs_w, abs_h
        )

        self._frame_draw_rect.setRect(
            x+1, y+1, w-2, frm_h-2
        )

    def _init_layout_base_def_(self, widget):
        self._widget = widget
        self._items = []
        self._indices = []
        self._item_count = 0
        self._item_w, self._item_h = 48, 48

        self._grid_layout_model = gui_qt_models.GuiGridLayout()

        self._column_count = 1

        self._layout_margins = 4, 4, 4, 4

        self._viewport_rect = QtCore.QRect()

    def __init__(self, *args, **kwargs):
        super(QtGridLayoutView, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self._init_frame_base_def_(self)
        self._init_action_base_def_(self)
        self._init_menu_base_def_(self)
        self._init_layout_base_def_(self)
        self._frame_draw_is_enable = False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                elif event.button() == QtCore.Qt.RightButton:
                    p = event.pos()
                    if not self._viewport_rect.contains(p):
                        self._popup_menu_()
                self._refresh_widget_draw_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._frame_draw_is_enable is True:
            painter._draw_frame_by_rect_(
                rect=self._frame_draw_rect,
                border_color=QtBorderColors.Basic,
                background_color=QtBackgroundColors.Dark,
                border_radius=4
            )

    def _set_item_size_(self, w, h):
        self._item_w, self._item_h = w, h

    def _add_item_(self, widget):
        widget.setParent(self)
        self._items.append(widget)
        self._indices.append(self._item_count)
        self._item_count += 1

        self._refresh_widget_()

    def _clear_all_items_(self):
        for i in self._items:
            i.close()
            i.deleteLater()
        #
        self._items = []
        self._indices = []
        self._item_count = 0
