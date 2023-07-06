# coding=utf-8
import fnmatch

import collections
#
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui import utl_gui_core


class VirtualItem(object):
    def __init__(self, widget):
        self._widget = widget
        self._name_text = None
        self._icon_text = None
        self._rect = QtCore.QRect()
        self._popup_rect = QtCore.QRect()

    def get_widget(self):
        return self._widget
    widget = property(get_widget)

    def set_name_text(self, text):
        self._name_text = text

    def get_name_text(self):
        return self._name_text
    name_text = property(get_name_text)

    def set_icon_text(self, text):
        self._icon_text = text

    def get_icon_text(self):
        return self._icon_text
    icon_text = property(get_icon_text)

    def get_rect(self):
        return self._rect
    rect = property(get_rect)

    def get_popup_rect(self):
        return self._popup_rect
    rect_popup = property(get_popup_rect)

    def delete(self):
        self._widget.close()
        self._widget.deleteLater()


class VirtualItemStack(object):
    def __init__(self):
        self._count = 0
        self._item_list = []

    def create_item(self, widget):
        item = VirtualItem(widget)
        self._item_list.append(item)
        #
        self._count += 1
        return item

    def get_item_at(self, index):
        if self._item_list:
            return self._item_list[index]

    def delete_item_at(self, index):
        item = self._item_list[index]
        item.delete()
        self._item_list.pop(index)
        self._count -= 1

    def delete_item(self, item):
        index = self._item_list.index(item)
        item.delete()
        self._item_list.pop(index)
        self._count -= 1

    def set_current_index(self, index):
        pass

    def get_index_by_name_text(self, text):
        for i_index, i_item in enumerate(self._item_list):
            if i_item.name_text == text:
                return i_index

    def get_name_text_at(self, index):
        item = self.get_item_at(index)
        if item:
            return self.get_item_at(index).name_text

    def get_count(self):
        return self._count

    def get_items(self):
        return self._item_list


class ScrollMode(object):
    def __init__(self):
        self._w = 0
        self._abs_w = 0
        self._offset = 0
        #
        self._is_valid = False

    def set_w(self, v):
        self._w = v

    def set_abs_w(self, v):
        self._abs_w = v

    def get_is_valid(self):
        return self._is_valid

    def update(self):
        if self._abs_w > self._w:
            self._is_valid = True
        else:
            self._is_valid = False


class AbsQtItemsDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_items_base_def_(self, widget):
        self._widget = widget

        self._virtual_items = []
        self._virtual_item_stack = VirtualItemStack()
        #
        self._item_count = 0
        self._item_index_current = 0
        self._item_index_temp = None
        self._item_index_hovered = None
        self._item_index_pressed = None

    def _set_item_current_at_(self, index):
        pass


class QtTabView(
    QtWidgets.QWidget,
    AbsQtItemsDef,
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
    utl_gui_qt_abstract.AbsQtWidgetBaseDef,
    #
    utl_gui_qt_abstract.AbsQtMenuBaseDef,
):
    current_changed = qt_signal()

    tab_delete_accepted = qt_signal(str)

    QT_MENU_CLS = _utl_gui_qt_wgt_utility.QtMenu
    def __init__(self, *args, **kwargs):
        super(QtTabView, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_items_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_widget_base_def_(self)
        self._init_menu_base_def_(self)

        self._tab_bar_rect = QtCore.QRect()
        self._tab_bar_draw_rect = QtCore.QRect()
        self._tab_left_tool_box_rect = QtCore.QRect()
        self._tab_left_tool_box_draw_rect = QtCore.QRect()
        self._tab_right_tool_box_rect = QtCore.QRect()
        self._tab_right_tool_box_draw_rect = QtCore.QRect()

        self._tab_add_is_enable = False
        self._tab_add_button = _utl_gui_qt_wgt_utility.QtIconMenuButton(self)
        self._tab_add_button.hide()
        self._tab_add_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('tab/tab-add')
        )

        self._tab_choose_button = _utl_gui_qt_wgt_utility.QtIconMenuButton(self)
        self._tab_choose_button.hide()
        self._tab_choose_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('tab/tab-choose')
        )

        self._tab_menu_is_enable = False
        self._tab_menu_button = _utl_gui_qt_wgt_utility.QtIconMenuButton(self)
        self._tab_menu_button.hide()
        self._tab_menu_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('tab/tab-menu-v')
        )

        self._tab_view_margins = 2, 2, 2, 2

        self._tab_w, self._tab_h = 48, 24

        self._tab_offset = 0

        self.setFont(
            get_font(size=10)
        )

        self._scroll_model = ScrollMode()
        self._set_menu_data_gain_fnc_(
            self._tab_item_menu_gain_fnc_
        )

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_(self):
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        self._frame_draw_rect.setRect(
            x, y, w, h
        )
        side = 2
        m_l, m_t, m_r, m_b = self._tab_view_margins
        t_w, t_h = self._tab_w, self._tab_h
        self._tab_bar_rect.setRect(
            x, y, w, t_h
        )
        self._tab_bar_draw_rect.setRect(
            x, y, w, t_h-1
        )
        scroll_w = w
        c_x, c_y = x, y
        btn_f_w, btn_f_h = t_h, t_h
        btn_w, btn_h = 20, 20
        if self._tab_add_is_enable is True:
            self._tab_left_tool_box_rect.setRect(
                x, y, btn_f_w, t_h
            )
            self._tab_left_tool_box_draw_rect.setRect(
                x, y, btn_f_w, t_h-1
            )
            self._tab_add_button.show()
            self._tab_add_button.setGeometry(
                x+(btn_f_w-btn_w)/2, y+(btn_f_h-btn_h)/2, btn_w, btn_h
            )
            c_x += t_h+self._tab_offset
            scroll_w -= t_h
        #
        scroll_abs_w = 0
        for i_index, i_virtual_item in enumerate(self._virtual_item_stack.get_items()):
            i_name_text = i_virtual_item.name_text
            if i_name_text is not None:
                i_text_width = self._get_text_draw_width_(
                    i_name_text
                )
            else:
                i_text_width = t_w
            #
            i_t_w = i_text_width+t_h*2
            scroll_abs_w += i_t_w
        #
        self._scroll_model.set_w(scroll_w)
        self._scroll_model.set_abs_w(scroll_abs_w)
        self._scroll_model.update()
        #
        # if self._tab_menu_is_enable is True:
        #     self._tab_menu_button.show()
        #     self._tab_menu_button.setGeometry(
        #         w-btn_f_w+(btn_f_w-btn_w)/2, c_y+(btn_f_h-btn_h)/2, btn_w, btn_h
        #     )
        if self._scroll_model.get_is_valid():
            self._tab_right_tool_box_rect.setRect(
                w-btn_f_w, y, btn_f_w, t_h
            )
            self._tab_right_tool_box_draw_rect.setRect(
                w-btn_f_w, y, btn_f_w, t_h-1
            )
            self._tab_choose_button.show()
            self._tab_choose_button.setGeometry(
                w-btn_f_w+(btn_f_w-btn_w)/2, c_y+(btn_f_h-btn_h)/2, btn_w, btn_h
            )
        else:
            self._tab_choose_button.hide()

        for i_index, i_virtual_item in enumerate(self._virtual_item_stack.get_items()):
            i_widget = i_virtual_item.widget
            i_rect = i_virtual_item.rect
            i_name_text = i_virtual_item.name_text
            if i_name_text is not None:
                i_text_width = self._get_text_draw_width_(
                    i_name_text
                )
            else:
                i_text_width = t_w
            #
            if i_index == self._item_index_current:
                i_widget.show()
                i_widget.setGeometry(
                    x+m_l, y+t_h+m_t, w-m_l-m_r, h-t_h-m_t-m_b
                )
            else:
                i_widget.hide()
            #
            i_t_w = i_text_width+t_h*2
            #
            i_rect.setRect(
                c_x, y, i_t_w, t_h
            )
            c_x += i_t_w

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
                self._item_index_temp = self._get_current_item_loc_(
                    event.pos()
                )
                if event.button() == QtCore.Qt.LeftButton:
                    if self._item_index_temp is not None:
                        self._set_item_pressed_at_(self._item_index_temp)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    if self._item_index_temp is not None:
                        self._popup_menu_()
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._item_index_temp = self._get_current_item_loc_(
                        event.pos()
                    )
                    if self._item_index_temp is not None:
                        self._set_item_pressed_at_(self._item_index_temp)
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
                    if self._item_index_temp is not None:
                        self._set_item_current_at_(
                            self._item_index_temp
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
            self._tab_bar_draw_rect,
            virtual_items=self._virtual_item_stack.get_items(),
            index_hovered=self._item_index_hovered,
            index_pressed=self._item_index_pressed,
            current_index=self._item_index_current,
        )
        #
        if self._tab_add_is_enable:
            painter._draw_tab_left_tool_box_by_rect_(
                rect=self._tab_left_tool_box_draw_rect
            )
        if self._scroll_model.get_is_valid():
            painter._draw_tab_right_tool_box_by_rect_(
                rect=self._tab_right_tool_box_draw_rect
            )

    def _delete_item_at_(self, index):
        item = self._virtual_item_stack.get_item_at(index)
        self._virtual_item_stack.delete_item(item)
        self.tab_delete_accepted.emit(item.name_text)
        count = self._virtual_item_stack.get_count()
        maximum = count-1
        if self._item_index_current > maximum:
            index = count-1
            index = max(min(index, maximum), 0)
            self._set_item_current_at_(index)
        self._refresh_widget_()

    def _add_item_(self, widget, *args, **kwargs):
        widget.setParent(self)
        virtual_item = self._virtual_item_stack.create_item(
            widget
        )
        if 'name' in kwargs:
            virtual_item.set_name_text(kwargs['name'])
        if 'icon_name_text' in kwargs:
            virtual_item.set_icon_text(kwargs['name'])
        #
        widget.installEventFilter(self)
        self._refresh_widget_()

    def _set_tab_add_enable_(self, boolean):
        self._tab_add_is_enable = boolean
        self._refresh_widget_()

    def _set_tab_add_menu_data_(self, data):
        self._tab_add_button._set_menu_data_(data)

    def _set_tab_add_menu_gain_fnc_(self, fnc):
        self._tab_add_button._set_menu_data_gain_fnc_(fnc)

    def _set_tab_menu_enable_(self, boolean):
        self._tab_menu_is_enable = boolean
        self._refresh_widget_()

    def _set_tab_menu_data_(self, data):
        self._tab_menu_button._set_menu_data_(data)

    def _set_tab_menu_data_gain_fnc_(self, fnc):
        self._tab_menu_button._set_menu_data_gain_fnc_(fnc)

    def _set_item_hovered_clear_(self):
        self._item_index_hovered = None
        self._refresh_widget_draw_()

    def _set_item_pressed_at_(self, index):
        if index != self._item_index_pressed:
            self._item_index_pressed = index
            #
            self._refresh_widget_()

    def _set_item_current_at_(self, index):
        if index != self._item_index_current:
            self._item_index_current = index
            self.current_changed.emit()
        #
        self._item_index_pressed = None
        self._refresh_widget_()

    def _set_item_current_by_name_text_(self, text):
        index = self._virtual_item_stack.get_index_by_name_text(
            text
        )
        if index is not None:
            self._set_item_current_at_(index)

    def _set_item_current_changed_connect_to_(self, fnc):
        self.current_changed.connect(fnc)

    def _execute_action_hover_move_(self, event):
        point = event.pos()
        self._item_index_hovered = None
        for i_index, i_virtual_item in enumerate(self._virtual_item_stack.get_items()):
            if i_virtual_item.rect.contains(point):
                self._item_index_hovered = i_index
                break

        self._refresh_widget_draw_()

    def _get_current_item_loc_(self, point):
        for i_index, i_virtual_item in enumerate(self._virtual_item_stack.get_items()):
            if i_virtual_item.rect.contains(point):
                return i_index

    def _execute_action_wheel_(self, event):
        p = event.pos()
        if self._tab_bar_rect.contains(p):
            delta = event.angleDelta().y()
            item_count = self._virtual_item_stack.get_count()
            if item_count > 1:
                maximum, minimum = item_count-1, 0
                index_cur = self._item_index_current
                if delta > 0:
                    index = bsc_core.RawIndexMtd.to_previous(maximum, minimum, index_cur)
                else:
                    index = bsc_core.RawIndexMtd.to_next(maximum, minimum, index_cur)
                #
                self._set_item_current_at_(index)

    def _get_current_name_text_(self):
        return self._virtual_item_stack.get_name_text_at(self._item_index_current)

    def _tab_item_menu_gain_fnc_(self):
        if self._item_index_temp is not None:
            return [
                ('close tab', 'close-hover', functools.partial(self._delete_item_at_, self._item_index_temp))
            ]
        return []


class _QtMenuBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(_QtMenuBar, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)


class GridBase(object):
    @staticmethod
    def _to_column_count(w, item_w):
        if item_w > 0:
            return max(int(w/item_w), 1)
        return 1
    @staticmethod
    def _to_row_count(h, item_h):
        if item_h > 0:
            return max(int(h/item_h), 1)
        return 1
    @staticmethod
    def _get_row_count(item_count, column_count):
        return int((item_count+column_count-1)/column_count)
    @staticmethod
    def _get_index_between(column, row, column_count):
        return int(column+row*column_count)
    @staticmethod
    def _get_column_loc(x, item_w):
        return int(x/item_w)
    @staticmethod
    def _get_column_at(index, column_count):
        return int(index % column_count)
    @staticmethod
    def _get_row_loc(y, item_h):
        return int(y/item_h)
    @staticmethod
    def _get_row_at(index, column_count):
        return int(index/column_count)
    @staticmethod
    def _map_to_item_pos(x, y, item_w, item_h, offset_x, offset_y, column, row):
        return int(x+offset_x-column*item_w), int(y+offset_y-row*item_h)
    @classmethod
    def _get_abs_size(cls, item_w, item_h, column_count, row_count):
        return column_count*item_w, row_count*item_h


class GridModel(GridBase):
    def __init__(self):
        self._item_count = 0
        self._x, self._y = 0, 0
        self._w, self._h = 48, 48
        self._item_w, self._item_h = 48, 48
        self._column_count, self._row_count = 1, 1
        self._abs_w, self._abs_h = 48, 48
        # left，top，right，bottom
        self._item_margins = 2, 2, 2, 2

    def get_item_column_at(self, index):
        return self._get_column_at(index, self._column_count)

    def get_item_row_at(self, index):
        return self._get_row_at(index, self._column_count)

    def get_pos_at(self, index, offset_x=0, offset_y=0):
        m_l, m_t, m_r, m_b = self._item_margins
        item_w, item_h = self._item_w+m_l+m_r, self._item_h+m_t+m_b
        return (
            self._x+self.get_item_column_at(index)*item_w-offset_x+m_l,
            self._y+self.get_item_row_at(index)*item_h-offset_y+m_t
        )

    def set_item_count(self, value):
        self._item_count = value

    def set_item_size(self, item_w, item_h):
        self._item_w, self._item_h = item_w, item_h

    def set_pos(self, x, y):
        self._x, self._y = x, y

    def set_size(self, w, h):
        self._w, self._h = w, h

    def update(self):
        # left，top，right，bottom
        if self._item_count:
            m_l, m_t, m_r, m_b = self._item_margins
            item_w, item_h = self._item_w+m_l+m_r, self._item_h+m_t+m_b
            self._column_count = self._to_column_count(self._w, item_w)
            self._column_count = min(self._column_count, self._item_count)
            self._row_count = self._get_row_count(self._item_count, self._column_count)
            self._abs_w, self._abs_h = self._get_abs_size(item_w, item_h, self._column_count, self._row_count)

    def get_geometry_at(self, index):
        x, y = self.get_pos_at(index)
        w, h = self._item_w, self._item_h
        return x, y, w, h

    def get_abs_size(self):
        return self._abs_w, self._abs_h


class QtLayoutView(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtMenuBaseDef,
):
    QT_MENU_CLS = _utl_gui_qt_wgt_utility.QtMenu
    def _refresh_widget_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        pass

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        m_l, m_t, m_r, m_b = self._layout_margins
        v_x, v_y = m_l, m_t
        v_w, v_h = w-m_l-m_r, h-m_t-m_b
        #
        self._grid_model.set_pos(v_x, v_y)
        self._grid_model.set_size(v_w, v_h)
        self._grid_model.set_item_size(self._item_w, self._item_h)
        self._grid_model.set_item_count(self._item_count)
        self._grid_model.update()
        #
        for i_index in self._indices:
            i_item = self._items[i_index]
            i_x, i_y, i_w, i_h = self._grid_model.get_geometry_at(i_index)
            i_item.setGeometry(
                i_x, i_y, i_w, i_h
            )
            i_item.setFixedSize(i_w, i_h)
            i_item.show()
        #
        abs_w, abs_h = self._grid_model.get_abs_size()
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

        self._grid_model = GridModel()

        self._column_count = 1

        self._layout_margins = 4, 4, 4, 4

        self._viewport_rect = QtCore.QRect()

    def __init__(self, *args, **kwargs):
        super(QtLayoutView, self).__init__(*args, **kwargs)
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
