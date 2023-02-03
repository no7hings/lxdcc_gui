# coding=utf-8
import collections
#
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui import utl_gui_core


class _AbsQtSplitter(QtWidgets.QWidget):
    QT_HANDLE_CLASS = None
    #
    QT_ORIENTATION = None
    #
    HANDLE_WIDTH = 12
    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitter, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._handle_list = []
        self._widget_list = []
        self._rect_list = []
        #
        self._spacing = 4
        self._contents_margins = 0, 0, 0, 0
        #
        self._size_dict = collections.OrderedDict()
        self._pos_dict = collections.OrderedDict()
        self._sizes = []

    def addWidget(self, widget):
        index = len(self._handle_list)
        #
        widget.setParent(self)
        self._widget_list.append(widget)
        # widget.hide()
        #
        handle = self.QT_HANDLE_CLASS()
        handle.setParent(self)
        self._handle_list.append(handle)
        #
        if index not in self._size_dict:
            self._size_dict[index] = 1
        #
        self._rect_list.append(QtCore.QRect())

    def resizeEvent(self, event):
        self._set_update_()

    def paintEvent(self, event):
        # painter = QtPainter(self)
        # painter._set_background_color_(255, 0, 0)
        # painter.drawRect(
        #     QtCore.QRect(
        #         0, 0, self.width(), self.height()
        #     )
        # )
        pass

    def _set_update_(self):
        self._set_update_by_size_()
        self._refresh_widget_draw_geometry_()

    def _set_update_by_size_(self):
        ss = self._size_dict
        maximum_size = sum(ss.values())
        # print self.QT_ORIENTATION, maximum_size, self._widget_list, self._handle_list
        if maximum_size > 0:
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [w*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, i_size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx]) + x
                    self._size_dict[idx] = i_size
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [h*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, i_size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx]) + y
                    self._size_dict[idx] = i_size
            else:
                raise TypeError()

    def _refresh_widget_draw_geometry_(self):
        w, h = self.width(), self.height()
        c = len(self._handle_list)
        h_f_w = self.HANDLE_WIDTH
        for idx in range(c):
            i_handle = self._handle_list[idx]
            widget = self._widget_list[idx]
            i_rect = self._rect_list[idx]
            #
            p = self._pos_dict[idx]
            s = self._size_dict[idx]
            ps = self._size_dict.get(idx-1)
            ns = self._size_dict.get(idx+1)
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                # i_handle
                hx, hy = p, 0
                hw, hh = h_f_w, h
                if idx == 0:
                    hx, hy = p-h_f_w, 0
                else:
                    if s == 0:
                        hx, hy = p-h_f_w, 0
                i_handle.setGeometry(
                    hx, hy, hw, hh
                )
                # print hx, hy, hw, hh
                i_rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = p+h_f_w, 0
                ww, wh = s-h_f_w, h
                if idx == 0:
                    wx, wy = p, 0
                    ww, wh = s, h
                if ns == 0:
                    ww, wh = s-h_f_w, h
                #
                widget.setGeometry(
                    wx, wy, ww, wh
                )
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                # i_handle
                hx, hy = 0, p
                hw, hh = w, h_f_w
                if idx == 0:
                    hx, hy = 0, p-h_f_w
                if s == 0:
                    hx, hy = 0, p-h_f_w
                i_handle.setGeometry(
                    hx, hy, hw, hh
                )
                # print i_handle.geometry()
                i_rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = 0, p+h_f_w
                ww, wh = w, s-h_f_w
                if idx == 0:
                    wx, wy = 0, p
                    ww, wh = w, s
                if ns == 0:
                    ww, wh = w, s-h_f_w
                #
                widget.setGeometry(
                    wx, wy, ww, wh
                )

    def _get_size_(self, index):
        return self._size_dict[index]

    def _set_size_(self, index, size):
        self._size_dict[index] = size
        #
        self._set_update_()

    def _get_sizes_(self, indices=None):
        if indices is not None:
            return [self._size_dict[i] for i in indices]
        return [i for i in self._size_dict.values()]

    def _set_adjacent_sizes_(self, indices, sizes):
        i_l, i_r = indices[:indices[0]], indices[indices[1]:]
        #
        h_f_w = self.HANDLE_WIDTH
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            size_min, size_max = 0 + len(i_l)*h_f_w, self.width() - len(i_r)*h_f_w
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            size_min, size_max = 0 + len(i_l)*h_f_w, self.height() - len(i_r)*h_f_w
        else:
            raise TypeError()

        for seq, i_size in enumerate(sizes):
            # clamp size
            if i_size <= size_min:
                i_size = size_min
            elif i_size >= size_max:
                i_size = size_max
            #
            idx = indices[seq]
            self._size_dict[idx] = i_size
        #
        self._set_update_()

    def _get_indices_(self):
        return self._size_dict.keys()

    def _get_widgets_(self):
        return self._widget_list

    def _get_widget_(self, index):
        return self._widget_list[index]

    def _set_widget_hide_at_(self, index):
        handle = self._get_handle_at_(index+1)
        handle._set_contract_l_switch_()

    def _get_cur_index_(self, qt_point):
        for idx, i_rect in enumerate(self._rect_list):
            if i_rect.contains(qt_point) is True:
                return idx

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def _set_stretch_factor_(self, index, size):
        self._size_dict[index] = size

    def _get_stretch_factor_(self, index):
        return self._size_dict[index]

    def setSizes(self, sizes):
        pass

    def _set_sizes_(self, sizes):
        self._sizes = sizes

    def _get_handle_at_(self, index):
        return self._handle_list[index]

    def widget(self, index):
        return self._widget_list[index]

    def indexOf(self, handle):
        return self._handle_list.index(handle)

    def setCollapsible(self, index, boolean):
        pass


class _QtHSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _utl_gui_qt_wgt_item._QtHSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitter, self).__init__(*args, **kwargs)


class _QtVSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _utl_gui_qt_wgt_item._QtVSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitter, self).__init__(*args, **kwargs)


class AbsQtItemsDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_items_def_init_(self, widget):
        self._widget = widget

        self._items = []
        self._item_index_current = 0
        self._item_index_hovered = None

        self._item_rects = []
        self._item_name_texts = []
        self._item_icon_name_texts = []

    def _set_item_current_index_(self, index):
        pass


class QtTabView(
    QtWidgets.QWidget,
    AbsQtItemsDef,
    utl_gui_qt_abstract.AbsQtWgtDef,
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
        self._set_widget_def_init_(self)

        self._tab_w, self._tab_h = 48, 24

        self.setFont(
            get_font(size=10)
        )

    def _set_item_add_(self, widget, *args, **kwargs):
        widget.setParent(self)
        #
        self._items.append(widget)
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
        self._set_wgt_update_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _set_wgt_update_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        spacing = 4
        t_w, t_h = self._tab_w, self._tab_h
        #
        c_x = x
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

    def _set_item_hovered_clear_(self):
        self._item_index_hovered = None
        self._refresh_widget_draw_()

    def _set_item_current_index_(self, index):
        if index != self._item_index_current:
            self._item_index_current = index
            self._refresh_widget_()
            self.current_changed.emit()

    def _set_item_current_changed_connect_to_(self, fnc):
        self.current_changed.connect(fnc)

    def _execute_action_hover_(self, event):
        point = event.pos()
        self._item_index_hovered = None

        for i_index, i in enumerate(self._item_rects):
            if i.contains(point):
                self._item_index_hovered = i_index
                break

        self._refresh_widget_draw_()

    def _get_current_name_text_(self):
        return self._item_name_texts[self._item_index_current]

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
                    pass
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
                    self._execute_action_hover_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._item_index_hovered is not None:
                        self._set_item_current_index_(self._item_index_hovered)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
        else:
            if event.type() == QtCore.QEvent.Enter:
                self._set_item_hovered_clear_()
            if event.type() == QtCore.QEvent.Leave:
                self._set_item_hovered_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)

        painter.setRenderHints(
            painter.Antialiasing
        )
        for i_index, i_item_rect in enumerate(self._item_rects):
            i_name_text = self._item_name_texts[i_index]
            i_icon_name_text = self._item_icon_name_texts[i_index]
            is_selected = i_index == self._item_index_current
            is_hovered = i_index == self._item_index_hovered
            if is_selected is False:
                painter._set_tab_button_draw_(
                    i_item_rect,
                    icon_name_text=i_icon_name_text,
                    name_text=i_name_text,
                    is_hovered=is_hovered,
                    is_selected=is_selected,
                )

        for i_index, i_item_rect in enumerate(self._item_rects):
            i_name_text = self._item_name_texts[i_index]
            i_icon_name_text = self._item_icon_name_texts[i_index]
            is_selected = i_index == self._item_index_current
            is_hovered = i_index == self._item_index_hovered
            if is_selected is True:
                painter._set_tab_button_draw_(
                    i_item_rect,
                    icon_name_text=i_icon_name_text,
                    name_text=i_name_text,
                    is_hovered=is_hovered,
                    is_selected=is_selected,
                )


class _QtGuideBar(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtEntryActionDef,
    #
    utl_gui_qt_abstract.AbsQtGuideActionDef,
    utl_gui_qt_abstract.AbsQtActionChooseForGuideDef,
):
    CHOOSE_RECT_CLS = _utl_gui_qt_wgt_item._QtGuideRect
    POPUP_CHOOSE_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtPopupForGuide
    #
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit_
    #
    up_key_pressed = qt_signal()
    down_key_pressed = qt_signal()
    enter_key_pressed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtGuideBar, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setFont(Font.title)
        #
        self.setMaximumHeight(24)
        self.setMinimumHeight(24)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self._set_value_entry_def_init_(self)
        self._build_entry_(str)
        #
        self._choose_item_icon_file_path = utl_core.Icon.get('choose_close')
        #
        self._set_menu_def_init_()
        #
        self._set_action_hover_def_init_()
        self._init_action_def_(self)
        self._set_action_press_def_init_()
        self._set_action_entry_def_init_()
        #
        self._set_guide_action_def_init_()
        self._init_set_action_choose_for_guide_def_(self)

        self._enter_is_enable = False

    def eventFilter(self, *args):
        super(_QtGuideBar, self).eventFilter(*args)
        #
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_guide_draw_geometry_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._action_is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._action_is_hovered = False
                self._clear_guide_choose_current_()
                self._clear_guide_current_()
                self.update()
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._enter_is_enable is False:
                    self._refresh_guide_current_(event)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._refresh_guide_current_(event)
                    #
                    if self._guide_choose_current_index is not None:
                        self._set_action_flag_(self.ActionFlag.ChooseClick)
                    elif self._guide_current_index is not None:
                        self._set_action_flag_(self.ActionFlag.PressClick)
                    else:
                        self._set_entry_enable_(True)
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self.db_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_press_flag_is_click_() is True:
                        self._send_action_press_click_emit_()
                        self._send_action_guide_item_press_clicked_emit_()
                    elif self._get_is_choose_flag_() is True:
                        self._start_guide_choose_item_popup_at_(self._guide_choose_current_index)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._set_action_flag_clear_()
                #
                self._action_is_hovered = False
                self._refresh_widget_draw_()
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._set_focused_(False)
                self._set_entry_enable_(False)

            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Up:
                    self.up_key_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Down:
                    self.down_key_pressed.emit()
                elif event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                    self.enter_key_pressed.emit()
        return False

    def paintEvent(self, event):
        super(_QtGuideBar, self).paintEvent(event)
        painter = QtPainter(self)
        if self._enter_is_enable is True:
            pass
            # if self._get_guide_choose_item_indices_():
            #     painter._draw_text_by_rect_(
            #         self._entry_frame_draw_rect,
            #         text=self._get_guide_choose_item_at_(-1)._path_text,
            #         text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            #         font_color=QtFontColors.Basic,
            #         font=get_font(size=10)
            #     )
        else:
            for index in self._get_guide_choose_item_indices_():
                i_item = self._get_guide_choose_item_at_(index)
                i_icon_offset = 0
                name_offset = 0
                choose_is_hovered = index == self._guide_choose_current_index
                guide_is_hovered = index == self._guide_current_index
                if index == self._guide_choose_current_index:
                    i_icon_offset = [0, 2][self._get_action_flag_() is not None]
                    background_color = painter._get_item_background_color_1_by_rect_(
                        i_item._icon_frame_draw_rect,
                        is_hovered=choose_is_hovered,
                        is_actioned=self._get_is_actioned_(),
                    )
                    painter._draw_frame_by_rect_(
                        i_item._icon_frame_draw_rect,
                        border_color=QtBackgroundColors.Transparent,
                        background_color=background_color,
                        border_radius=3,
                        offset=i_icon_offset
                    )
                elif index == self._guide_current_index:
                    background_color = painter._get_item_background_color_1_by_rect_(
                        i_item._name_frame_draw_rect,
                        is_hovered=guide_is_hovered,
                        is_actioned=self._get_is_actioned_(),
                    )
                    name_offset = [0, 2][self._get_action_flag_() is not None]
                    painter._draw_frame_by_rect_(
                        i_item._name_frame_draw_rect,
                        border_color=QtBackgroundColors.Transparent,
                        background_color=background_color,
                        border_radius=3,
                        offset=name_offset
                    )
                #
                painter._draw_icon_file_by_rect_(
                    i_item._icon_file_draw_rect,
                    file_path=i_item._get_icon_file_path_(),
                    offset=i_icon_offset
                )
                #
                i_type_text = i_item._type_text
                painter._draw_text_by_rect_(
                    rect=i_item._type_rect,
                    text=i_type_text,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                    font_color=bsc_core.RawTextOpt(i_type_text).to_rgb(),
                    font=get_font(size=10, italic=True),
                    offset=name_offset,
                    is_hovered=guide_is_hovered,
                )
                #
                i_name_text = i_item._name_text
                painter._draw_text_by_rect_(
                    rect=i_item._name_draw_rect,
                    text=i_name_text,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                    font=get_font(size=12),
                    offset=name_offset,
                    is_hovered=guide_is_hovered,
                )

    def _set_entry_enable_(self, boolean):
        self._enter_is_enable = boolean
        if self._value_entry is not None:
            self._value_entry.setVisible(boolean)
            self._value_entry._set_value_(
                self._get_guide_path_()
            )
        #
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _build_entry_(self, *args, **kwargs):
        self._value_type = args[0]
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(0, 0, 0, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry.hide()
        self._value_entry.setFocusProxy(self)
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(self._value_type)
        #
        self._value_history_button = _utl_gui_qt_wgt_utility.QtIconPressItem(self)
        #
        self._value_history_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('history'))
        self._value_history_button._set_sub_icon_file_path_(utl_gui_core.RscIconFile.get('down'))
        self._value_history_button._set_icon_frame_draw_size_(18, 18)

    def _refresh_guide_current_(self, event):
        p = event.pos()
        #
        self._clear_guide_choose_current_()
        self._clear_guide_current_()
        if self._enter_is_enable is False:
            for index in self._get_guide_choose_item_indices_():
                i_item = self._get_guide_choose_item_at_(index)
                if i_item._icon_frame_draw_rect.contains(p) is True:
                    self._set_guide_choose_current_index_(index)
                    break
                elif i_item._name_frame_draw_rect.contains(p) is True:
                    self._set_view_guide_current_index_(index)
                    break
        #
        self._refresh_widget_draw_()

    def _set_view_path_args_(self, path_args):
        self._set_guide_choose_clear_()
        self._set_view_guide_clear_()
        #
        path_values = path_args.values()
        for index, (i_name, i_type) in enumerate(path_args.items()):
            i_item = self._set_guide_choose_item_create_()
            #
            i_path = '/' + '/'.join(path_values[:index+1])
            i_item._set_path_text_(i_path)
            i_item._set_type_text_(i_type)
            i_item._set_name_text_(i_name)
        #
        self._refresh_guide_draw_geometry_()
        self.update()

    def _refresh_guide_draw_geometry_(self):
        side = 2
        spacing = 2
        x, y = 0, 0
        w, h = self.width()-1, self.height()-1
        self._set_entry_frame_draw_rect_(x, y, w, h)
        #
        i_f_w, i_f_h = h-4, h-4
        i_i_w, i_i_h = 16, 16
        #
        i_x, i_y = x + 1, (h-i_f_h)/2

        frm_w, frm_h = 20, 20

        self._value_history_button.setGeometry(
            w-frm_w, y+(h-frm_h)/2, frm_w, frm_h
        )
        #
        for index in self._get_guide_choose_item_indices_():
            i_item = self._get_guide_choose_item_at_(index)
            i_item._set_icon_frame_draw_rect_(
                i_x, i_y, i_f_w, i_f_h
            )
            i_item._set_icon_file_draw_rect_(
                i_x+(i_f_w-i_i_w)/2, i_y+(i_f_h-i_i_h)/2, i_i_w, i_i_h
            )
            i_x += i_f_w + spacing
            #
            i_path_key = i_item._type_text
            i_path_value = i_item._name_text
            #
            i_path_w_0, i_path_h_0 = RawTextMtd.get_size(10, i_path_key)
            i_path_w_1, i_path_h_1 = RawTextMtd.get_size(12, i_path_value)
            i_path_w = i_path_w_0 + i_path_w_1 + spacing*8
            i_item._set_name_frame_rect_(
                i_x-spacing*2, i_y, i_path_w, i_f_h
            )
            #
            i_path_key_w = i_path_w_0 + spacing*4
            i_item._set_type_rect_(
                i_x, i_y, i_path_key_w, i_f_h
            )
            i_x += i_path_key_w
            #
            i_path_value_w = i_path_w_1 + spacing*4
            i_item._set_name_draw_geometry_(
                i_x, i_y, i_path_value_w, i_f_h
            )
            #
            i_x += i_path_value_w

    def _set_view_guide_and_choose_clear_(self):
        self._set_view_path_args_({})

    def _get_view_guide_items_(self):
        return self._get_guide_choose_items_()

    def _get_guide_choose_item_point_at_(self, index=0):
        item = self._get_guide_choose_item_at_(index)
        rect = item._icon_frame_draw_rect
        return self.mapToGlobal(rect.center())

    def _get_guide_choose_item_rect_at_(self, index=0):
        item = self._get_guide_choose_item_at_(index)
        rect = item._icon_frame_draw_rect
        return rect

    def _get_guide_path_(self):
        item = self._get_guide_choose_item_at_(-1)
        if item:
            return item._path_text


class _QtMenuBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(_QtMenuBar, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
