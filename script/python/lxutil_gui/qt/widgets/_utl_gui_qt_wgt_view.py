# coding=utf-8
import fnmatch

import collections
#
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui import utl_gui_core


class AbsQtItemsDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_items_def_init_(self, widget):
        self._widget = widget

        self._items = []
        self._item_count = 0
        self._item_index_current = 0
        self._item_index_hovered = None
        self._item_index_pressed = None

        self._item_rects = []
        self._item_name_texts = []
        self._item_icon_name_texts = []

    def _set_item_index_current_(self, index):
        pass


class QtTabView(
    QtWidgets.QWidget,
    AbsQtItemsDef,
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
    utl_gui_qt_abstract.AbsQtWidgetBaseDef,
):
    current_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtTabView, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._set_items_def_init_(self)
        self._init_frame_base_def_(self)
        self._init_widget_base_def_(self)

        self._tab_rect = QtCore.QRect()

        self._tab_w, self._tab_h = 48, 24

        self.setFont(
            get_font(size=10)
        )

    def _set_item_add_(self, widget, *args, **kwargs):
        widget.setParent(self)
        #
        self._items.append(widget)
        self._item_count += 1
        self._item_rects.append(QtCore.QRect())
        if 'name' in kwargs:
            self._item_name_texts.append(kwargs['name'])
        else:
            self._item_name_texts.append(None)
        #
        if 'icon_name_text' in kwargs:
            self._item_icon_name_texts.append(kwargs['icon_name_text'])
        else:
            self._item_icon_name_texts.append(None)
        #
        widget.installEventFilter(self)

        self._refresh_widget_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_(self):
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        self._set_frame_draw_rect_(
            x, y, w, h
        )
        spacing = 4
        t_w, t_h = self._tab_w, self._tab_h
        self._tab_rect.setRect(
            x, y, w, t_h
        )
        #
        c_x = x
        #
        for i_index, i_item_rect in enumerate(self._item_rects):
            i_name_text = self._item_name_texts[i_index]
            if i_name_text is not None:
                i_text_width = self._get_text_draw_width_(
                    i_name_text
                )
            else:
                i_text_width = t_w
            #
            i_icon_name_text = self._item_icon_name_texts[i_index]
            if i_icon_name_text is not None:
                i_icon_w = t_h
            else:
                i_icon_w = 0
            #
            i_t_w = i_text_width+i_icon_w+t_h*2
            #
            i_item_rect.setRect(
                c_x, y, i_t_w, t_h
            )
            c_x += i_t_w
        # widget
        for i_index, i_item in enumerate(self._items):
            if i_index == self._item_index_current:
                if i_item is not None:
                    i_item.show()
                    i_item.setGeometry(
                        x, y+t_h+spacing, w, h-t_h-spacing
                    )
            else:
                i_item.hide()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._set_item_hovered_clear_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._item_index_hovered is not None:
                        self._set_item_index_pressed_(self._item_index_hovered)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    pass
                elif event.button() == QtCore.Qt.NoButton:
                    self._execute_action_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._item_index_hovered is not None:
                        self._set_item_index_current_(
                            self._item_index_hovered
                        )
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.Wheel:
                self._execute_action_wheel_(event)
        else:
            if event.type() == QtCore.QEvent.Enter:
                self._set_item_hovered_clear_()
            if event.type() == QtCore.QEvent.Leave:
                self._set_item_hovered_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)

        painter._draw_tab_buttons_by_rects_(
            self._frame_draw_rect,
            self._item_rects,
            self._item_name_texts,
            self._item_icon_name_texts,
            self._item_index_hovered,
            self._item_index_pressed,
            self._item_index_current,
        )

    def _set_item_hovered_clear_(self):
        self._item_index_hovered = None
        self._refresh_widget_draw_()

    def _set_item_index_pressed_(self, index):
        if index != self._item_index_pressed:
            self._item_index_pressed = index
        #
        self._refresh_widget_()

    def _set_item_index_current_(self, index):
        if index != self._item_index_current:
            self._item_index_current = index
            self.current_changed.emit()
        #
        self._item_index_pressed = None
        self._refresh_widget_()

    def _set_item_current_changed_connect_to_(self, fnc):
        self.current_changed.connect(fnc)

    def _execute_action_hover_move_(self, event):
        point = event.pos()
        self._item_index_hovered = None

        for i_index, i in enumerate(self._item_rects):
            if i.contains(point):
                self._item_index_hovered = i_index
                break

        self._refresh_widget_draw_()

    def _execute_action_wheel_(self, event):
        p = event.pos()
        if self._tab_rect.contains(p):
            delta = event.angleDelta().y()
            if self._item_count > 1:
                maximum, minimum = self._item_count-1, 0
                index_cur = self._item_index_current
                if delta > 0:
                    index = bsc_core.RawIndexMtd.to_previous(maximum, minimum, index_cur)
                else:
                    index = bsc_core.RawIndexMtd.to_next(maximum, minimum, index_cur)
                #
                self._set_item_index_current_(index)

    def _get_current_name_text_(self):
        return self._item_name_texts[self._item_index_current]


class _QtMenuBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(_QtMenuBar, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
