# coding=utf-8
import collections

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui import utl_gui_core

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility


class _AbsQtSplitterHandle(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    #
    utl_gui_qt_abstract.AbsQtStateDef,
):
    QT_ORIENTATION = None
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            r_w, r_h = 8, 16
            self._frame_draw_rects[0].setRect(
                x+(w-r_w)/2, y+h/4,
                r_w, r_h
            )
            self._frame_draw_rects[1].setRect(
                x+(w-r_w)/2, h-h/4-r_h,
                r_w, r_h
            )
            self._set_frame_draw_rect_(x+1, y, w-3, h)
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            r_w, r_h = 16, 8
            self._frame_draw_rects[0].setRect(
                x+w/4, y+(h-r_h)/2,
                r_w, r_h
            )
            self._frame_draw_rects[1].setRect(
                w-w/4-r_w, y+(h-r_h)/2,
                r_w, r_h
            )
            self._set_frame_draw_rect_(x, y+1, w, h-3)

    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitterHandle, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._swap_enable = True
        #
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        #
        self._contract_icon_name_l = ['contract_h_l', 'contract_v_l'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._contract_icon_name_r = ['contract_h_r', 'contract_v_r'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._swap_icon_name = ['swap_h', 'swap_v'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        #
        self._contract_frame_size = [(16, 8), (8, 16)][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        #
        self._is_contract_l = False
        self._is_contract_r = False
        #
        self._qt_layout_class = [
            _utl_gui_qt_wgt_utility.QtHBoxLayout, _utl_gui_qt_wgt_utility.QtVBoxLayout
        ][
            self.QT_ORIENTATION == QtCore.Qt.Horizontal
        ]
        #
        self._size_l = 0
        self._size_r = 0
        self._sizes = []
        #
        self._index = 0
        #
        layout = self._qt_layout_class(self)
        layout.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        layout.setContentsMargins(*[0]*4)
        layout.setSpacing(2)
        self._contract_l_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._contract_l_button._set_name_text_('contact')
        self._contract_l_button._set_icon_frame_draw_size_(*self._contract_frame_size)
        self._contract_l_button._set_icon_file_draw_percent_(1.0)
        self._contract_l_button.setMaximumSize(*self._contract_frame_size)
        self._contract_l_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._contract_l_button)
        self._contract_l_button.clicked.connect(self._set_contract_l_switch_)
        self._contract_l_button._set_tool_tip_text_(
            '"LMB-click" to contact left/top.'
        )
        #
        self._swap_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._swap_button._set_name_text_('swap')
        self._swap_button._set_icon_file_path_(utl_gui_core.RscIconFile.get(self._swap_icon_name))
        self._swap_button._set_icon_frame_draw_size_(*self._contract_frame_size)
        self._swap_button._set_icon_file_draw_percent_(1.0)
        self._swap_button.setMaximumSize(*self._contract_frame_size)
        self._swap_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._swap_button)
        self._swap_button.clicked.connect(self._set_swap_)
        self._swap_button._set_tool_tip_text_(
            '"LMB-click" to swap.'
        )
        #
        self._contract_r_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._contract_r_button._set_name_text_('contact')
        self._contract_r_button._set_icon_frame_draw_size_(*self._contract_frame_size)
        self._contract_r_button._set_icon_file_draw_percent_(1.0)
        self._contract_r_button.setMaximumSize(*self._contract_frame_size)
        self._contract_r_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._contract_r_button)
        self._contract_r_button.clicked.connect(self._set_contract_r_switch_)
        self._contract_r_button._set_tool_tip_text_(
            '"LMB-click" to contact right/bottom.'
        )
        #
        self._set_contract_buttons_update_()
        #
        self.installEventFilter(self)
        self._action_is_hovered = False
        #
        self._set_frame_def_init_()
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        #
        self._set_state_def_init_()
        #
        self._hovered_frame_border_color = QtBorderColors.Button
        self._hovered_frame_background_color = QtBackgroundColors.Button

        self._actioned_frame_border_color = QtBorderColors.Actioned
        self._actioned_frame_background_color = QtBackgroundColors.Actioned
        #
        self._frame_draw_rects = [
            QtCore.QRect(), QtCore.QRect()
        ]
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            self._resize_icon_file_path = utl_gui_core.RscIconFile.get('resize-handle-v')
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            self._resize_icon_file_path = utl_gui_core.RscIconFile.get('resize-handle-h')

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self._set_action_flag_(
                        self.ActionFlag.SplitHHover
                    )
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self._set_action_flag_(
                        self.ActionFlag.SplitVHover
                    )
                #
                self._set_action_hovered_(True)
            elif event.type() == QtCore.QEvent.Leave:
                self.setCursor(QtCore.Qt.ArrowCursor)
                #
                self._set_action_hovered_(False)
            #
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self._set_action_flag_(
                        self.ActionFlag.SplitHPess
                    )
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self._set_action_flag_(
                        self.ActionFlag.SplitVPess
                    )
                self._set_action_split_move_start_(event)
                self._set_pressed_(True)
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self._set_action_flag_(
                        self.ActionFlag.SplitHMove
                    )
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self._set_action_flag_(
                        self.ActionFlag.SplitVMove
                    )
                self._set_action_split_move_execute_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._set_action_split_move_stop_(event)
                self._set_pressed_(False)
                self._clear_action_flag_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        offset = [0, 2][
            self._action_flag in {
                self.ActionFlag.SplitHPess, self.ActionFlag.SplitHMove,
                self.ActionFlag.SplitVPess, self.ActionFlag.SplitVMove
            }
        ]
        #
        if self._action_is_enable is True:
            condition = self._action_is_hovered, self._is_pressed
            if condition == (False, False):
                border_color = QtBackgroundColors.Transparent
                background_color = QtBackgroundColors.Transparent
            elif condition == (False, True):
                border_color = self._actioned_frame_border_color
                background_color = self._actioned_frame_background_color
            elif condition == (True, True):
                border_color = self._actioned_frame_border_color
                background_color = self._actioned_frame_background_color
            elif condition == (True, False):
                border_color = self._hovered_frame_border_color
                background_color = self._hovered_frame_background_color
            else:
                raise SyntaxError()
        else:
            border_color = QtBackgroundColors.ButtonDisable
            background_color = QtBackgroundColors.ButtonDisable
        #
        for i_rect in self._frame_draw_rects:
            painter._draw_icon_file_by_rect_(
                rect=i_rect,
                file_path=self._resize_icon_file_path,
                offset=offset,
            )

    def _set_contract_l_switch_(self):
        if self._is_contract_r is True:
            self._set_contract_r_switch_()
        else:
            splitter = self._get_splitter_()
            index_l = splitter._get_handle_index_(self)-1
            index_r = splitter._get_handle_index_(self)
            indices = index_l, index_r
            # switch
            self._is_contract_l = not self._is_contract_l
            if self._is_contract_l is True:
                # record size
                self._sizes = splitter._get_sizes_(indices)
                #
                sizes = [0, sum(self._sizes)]
                splitter._set_adjacent_sizes_(indices, sizes)
            else:
                splitter._set_adjacent_sizes_(indices, self._sizes)
            #
            self._set_contract_buttons_update_()

    def _set_contract_r_switch_(self):
        if self._is_contract_l is True:
            self._set_contract_l_switch_()
        else:
            splitter = self._get_splitter_()
            index_l = splitter._get_handle_index_(self)-1
            index_r = splitter._get_handle_index_(self)
            indices = index_l, index_r
            # switch
            self._is_contract_r = not self._is_contract_r
            if self._is_contract_r is True:
                # record size
                self._sizes = splitter._get_sizes_(indices)
                #
                sizes = [sum(self._sizes), 0]
                splitter._set_adjacent_sizes_(indices, sizes)
            else:
                splitter._set_adjacent_sizes_(indices, self._sizes)
            #
            self._set_contract_buttons_update_()

    def _set_swap_(self):
        splitter = self._get_splitter_()
        index_l = splitter._get_handle_index_(self)-1
        index_r = splitter._get_handle_index_(self)
        widgets = splitter._get_widgets_()
        widget_l = splitter._get_widget_(index_l)
        widget_r = splitter._get_widget_(index_r)
        widgets[index_l], widgets[index_r] = widget_r, widget_l
        splitter._set_update_()

    def _set_contract_buttons_update_(self):
        icon_name_l = [self._contract_icon_name_l, self._contract_icon_name_r][self._is_contract_l]
        self._contract_l_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(icon_name_l)
        )
        self._contract_l_button.update()
        icon_name_r = [self._contract_icon_name_r, self._contract_icon_name_l][self._is_contract_r]
        self._contract_r_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(icon_name_r)
        )
        self._contract_r_button.update()

    def _set_update_(self):
        pass

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def _get_splitter_(self):
        return self.parent()

    def _set_action_split_move_start_(self, event):
        pass

    def _set_action_split_move_execute_(self, event):
        # self._contract_l_button._set_action_flag_(self.ActionFlag.PressMove)
        # self._contract_r_button._set_action_flag_(self.ActionFlag.PressMove)
        # self._swap_button._set_action_flag_(self.ActionFlag.PressMove)
        p = event.pos()
        x, y = p.x(), p.y()
        splitter = self._get_splitter_()
        index_l = splitter._get_handle_index_(self)-1
        index_r = splitter._get_handle_index_(self)
        indices = index_l, index_r
        s_l_o, s_r_o = splitter._get_size_(index_l), splitter._get_size_(index_r)
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            s_l, s_r = s_l_o+x, s_r_o-x
            splitter._set_adjacent_sizes_(indices, [s_l, s_r])
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            s_l, s_r = s_l_o+y, s_r_o-y
            splitter._set_adjacent_sizes_(indices, [s_l, s_r])

    def _set_action_split_move_stop_(self, event):
        pass
        # self._contract_l_button._clear_action_flag_()
        # self._contract_r_button._clear_action_flag_()
        # self._swap_button._clear_action_flag_()


class _QtHSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitterHandle, self).__init__(*args, **kwargs)


class _QtVSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitterHandle, self).__init__(*args, **kwargs)


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

    def _set_widget_add_(self, widget):
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

    def _get_widget_at_(self, index):
        return self._widget_list[index]

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

    def _get_handle_index_(self, handle):
        return self._handle_list.index(handle)


class QtHSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _QtHSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(QtHSplitter, self).__init__(*args, **kwargs)


class QtVSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _QtVSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(QtVSplitter, self).__init__(*args, **kwargs)


class QtHSplitter_(QtWidgets.QSplitter):
    def __init__(self, *args, **kwargs):
        super(QtHSplitter_, self).__init__(*args, **kwargs)
        self.setHandleWidth(2)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QSplitter')
        )
