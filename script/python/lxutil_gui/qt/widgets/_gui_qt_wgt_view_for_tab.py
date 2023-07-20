# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

import lxutil_gui.qt.abstracts as gui_qt_abstract

import lxutil_gui.qt.models as gui_qt_models

from lxutil_gui import utl_gui_core


class AbsQtItemsDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_items_base_def_(self, widget):
        self._widget = widget

        self._virtual_items = []
        self._virtual_item_stack = gui_qt_models.GuiItemStack()
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
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtWidgetBaseDef,
    #
    gui_qt_abstract.AbsQtMenuBaseDef,
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

        self._tab_scroll_previous_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._tab_scroll_previous_button.hide()
        self._tab_scroll_previous_button._set_icon_geometry_mode_(
            _utl_gui_qt_wgt_utility.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_previous_button.setFixedSize(10, 20)
        self._tab_scroll_previous_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('scroll-left')
        )
        self._tab_scroll_previous_button.press_clicked.connect(self._do_scroll_previous_)

        self._tab_scroll_next_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._tab_scroll_next_button.hide()
        self._tab_scroll_next_button._set_icon_geometry_mode_(
            _utl_gui_qt_wgt_utility.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_next_button.setFixedSize(10, 20)
        self._tab_scroll_next_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('scroll-right')
        )
        self._tab_scroll_next_button.press_clicked.connect(self._do_scroll_next_)

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

        self.setFont(
            get_font(size=10)
        )

        self._gui_scroll = gui_qt_models.GuiScroll()
        self._gui_scroll.set_step(64)
        self._set_menu_data_gain_fnc_(
            self._tab_item_menu_gain_fnc_
        )

    def _refresh_widget_(self):
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        self._frame_draw_rect.setRect(
            x, y, w, h
        )
        m_l, m_t, m_r, m_b = self._tab_view_margins
        t_w, t_h = self._tab_w, self._tab_h
        c_t_f_x, c_t_f_y = x, y
        c_t_f_w, c_t_f_h = w, t_h
        self._tab_bar_draw_rect.setRect(
            x, y, w, t_h-1
        )
        scroll_w = w
        c_x, c_y = x, y
        #
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
            c_x += t_h
            scroll_w -= t_h
            #
            c_t_f_x += btn_f_w
            c_t_f_w -= btn_f_w
        #
        scroll_abs_w = 0
        virtual_items = self._virtual_item_stack.get_items()
        if virtual_items:
            for i_index, i_virtual_item in enumerate(virtual_items):
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
            self._gui_scroll.set_w(scroll_w)
            self._gui_scroll.set_abs_w(scroll_abs_w+btn_f_w*3)
            self._gui_scroll.update()
            #
            # if self._tab_menu_is_enable is True:
            #     self._tab_menu_button.show()
            #     self._tab_menu_button.setGeometry(
            #         w-btn_f_w+(btn_f_w-btn_w)/2, c_y+(btn_f_h-btn_h)/2, btn_w, btn_h
            #     )
            if self._gui_scroll.get_is_valid():
                btn_w_1, btn_h_1 = btn_w/2, btn_h
                btn_f_w_r = btn_f_w*2
                c_x_1, c_y_1 = w-btn_f_w_r, y
                c_x_1 = max(c_x_1, btn_f_w_r)
                self._tab_right_tool_box_rect.setRect(
                    c_x_1, c_y_1, btn_f_w_r, btn_f_h
                )
                self._tab_right_tool_box_draw_rect.setRect(
                    c_x_1, c_y_1, btn_f_w_r, btn_f_h-1
                )
                #
                self._tab_scroll_previous_button.show()
                self._tab_scroll_previous_button.setGeometry(
                    c_x_1+(btn_f_w-btn_w)/2, c_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
                )
                self._tab_scroll_next_button.show()
                self._tab_scroll_next_button.setGeometry(
                    c_x_1+(btn_f_w-btn_w)/2+btn_w_1, c_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
                )
                self._tab_choose_button.show()
                self._tab_choose_button.setGeometry(
                    c_x_1+btn_f_w+(btn_f_w-btn_w)/2, c_y_1+(btn_f_h-btn_h)/2, btn_w, btn_h
                )
                #
                c_t_f_w -= btn_f_w_r
            else:
                self._tab_scroll_previous_button.hide()
                self._tab_scroll_next_button.hide()
                self._tab_choose_button.hide()

            scroll_value = self._gui_scroll.get_value()
            for i_index, i_virtual_item in enumerate(virtual_items):
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
                    c_x-scroll_value, y, i_t_w, t_h
                )
                c_x += i_t_w

        self._tab_bar_rect.setRect(
            c_t_f_x, c_t_f_y, c_t_f_w, c_t_f_h
        )

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
                if event.button() == QtCore.Qt.LeftButton:
                    self._item_index_temp = self._get_current_item_loc_(
                        event.pos()
                    )
                    if self._item_index_temp is not None:
                        self._set_item_pressed_at_(self._item_index_temp)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                elif event.button() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
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
                self._do_wheel_(event)
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
        #
        if self._gui_scroll.get_is_valid():
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
        #
        self._item_index_current = self._virtual_item_stack.get_index_maximum()
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

    def _get_current_item_loc_(self, p):
        if self._tab_bar_rect.contains(p):
            for i_index, i_virtual_item in enumerate(self._virtual_item_stack.get_items()):
                if i_virtual_item.rect.contains(p):
                    return i_index

    def _do_hover_move_(self, event):
        p = event.pos()
        self._item_index_hovered = None
        if self._tab_bar_rect.contains(p):
            for i_index, i_virtual_item in enumerate(self._virtual_item_stack.get_items()):
                if i_virtual_item.rect.contains(p):
                    self._item_index_hovered = i_index
                    break

        self._refresh_widget_draw_()

    def _do_wheel_(self, event):
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
                self._do_scroll_to_(index)
                self._set_item_current_at_(index)

    def _get_current_name_text_(self):
        return self._virtual_item_stack.get_name_text_at(self._item_index_current)

    def _tab_item_menu_gain_fnc_(self):
        if self._item_index_temp is not None:
            return [
                ('close tab', 'close-hover', functools.partial(self._delete_item_at_, self._item_index_temp))
            ]
        return []

    def _do_scroll_to_(self, index):
        item = self._virtual_item_stack.get_item_at(index)
        if item:
            x = item.get_rect().x()
            self._gui_scroll.accept_value(x-24)

    def _do_scroll_previous_(self):
        if self._gui_scroll.step_to_previous():
            self._refresh_widget_()
    
    def _do_scroll_next_(self):
        if self._gui_scroll.step_to_next():
            self._refresh_widget_()
