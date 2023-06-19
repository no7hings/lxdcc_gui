# coding=utf-8
import collections

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui import utl_gui_core

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility


class _AbsQtSplitterHandle(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
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
        s = 8
        # split as horizontal, handle is vertical
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            r_w, r_h = 8, 16
            h_h = (h-r_h*3-s*2)/2
            self._handle_draw_rects[0].setRect(
                x+(w-r_w)/2, y+(h_h-r_h)/2,
                r_w, r_h
            )
            self._handle_draw_rects[1].setRect(
                x+(w-r_w)/2, h-h_h+(h_h-r_h)/2,
                r_w, r_h
            )
            # contract
            self._contract_l_rect.setRect(
                x, y+(h-r_h)/2-r_h-s,
                w, r_h
            )
            self._contract_l_draw_rect.setRect(
                x+(w-r_w)/2, y+(h-r_h)/2-r_h-s,
                r_w, r_h
            )
            self._contract_r_rect.setRect(
                x, y+(h-r_h)/2+r_h+s,
                w, r_h
            )
            self._contract_r_draw_rect.setRect(
                x+(w-r_w)/2, y+(h-r_h)/2+r_h+s,
                r_w, r_h
            )
            # swap
            self._swap_rect.setRect(
                x, y+(h-r_h)/2,
                w, r_h
            )
            self._swap_draw_rect.setRect(
                x+(w-r_w)/2, y+(h-r_h)/2,
                r_w, r_h
            )
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            r_w, r_h = 16, 8
            h_w = (w-r_w*3-s*2)/2
            self._handle_draw_rects[0].setRect(
                x+(h_w-r_w)/2, y+(h-r_h)/2,
                r_w, r_h
            )
            self._handle_draw_rects[1].setRect(
                w-h_w+(h_w-r_w)/2, y+(h-r_h)/2,
                r_w, r_h
            )
            # contract
            self._contract_l_rect.setRect(
                x+(w-r_w)/2-r_w-s, y,
                r_w, h
            )
            self._contract_l_draw_rect.setRect(
                x+(w-r_w)/2-r_w-s, y+(h-r_h)/2,
                r_w, r_h
            )
            self._contract_r_rect.setRect(
                x+(w-r_w)/2+r_w+s, y,
                r_w, h
            )
            self._contract_r_draw_rect.setRect(
                x+(w-r_w)/2+r_w+s, y+(h-r_h)/2,
                r_w, r_h
            )
            # swap
            self._swap_rect.setRect(
                x+(w-r_w)/2, y,
                r_w, h
            )
            self._swap_draw_rect.setRect(
                x+(w-r_w)/2, y+(h-r_h)/2,
                r_w, r_h
            )

    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitterHandle, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
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
        self._sizes_moving = []
        #
        self._index = 0
        #
        self._splitter_press_pos = 0, 0
        #
        self._contract_l_rect = QtCore.QRect()
        self._contract_l_draw_rect = QtCore.QRect()
        self._contract_l_draw_icon_file_path = utl_gui_core.RscIconFile.get(self._contract_icon_name_l)
        self._contract_r_rect = QtCore.QRect()
        self._contract_r_draw_rect = QtCore.QRect()
        self._contract_r_draw_icon_file_path = utl_gui_core.RscIconFile.get(self._contract_icon_name_r)
        self._swap_rect = QtCore.QRect()
        self._swap_draw_rect = QtCore.QRect()
        self._swap_icon_file_path = utl_gui_core.RscIconFile.get(self._swap_icon_name)
        #
        self._action_is_hovered = False
        #
        self._init_frame_base_def_(self)
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
        self._handle_draw_rects = [
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
            elif event.type() == QtCore.QEvent.Leave:
                self.unsetCursor()
                self._clear_all_action_flags_()
            #
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.buttons() == QtCore.Qt.LeftButton:
                    p = event.pos()
                    if self._contract_l_rect.contains(p):
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeLeft, self.ActionFlag.ResizeRight][self._is_contract_l]
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeUp, self.ActionFlag.ResizeDown][self._is_contract_l]
                            )
                    elif self._contract_r_rect.contains(p):
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeRight, self.ActionFlag.ResizeLeft][self._is_contract_r]
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeDown, self.ActionFlag.ResizeUp][self._is_contract_r]
                            )
                    elif self._swap_rect.contains(p):
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                self.ActionFlag.SwapH
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                self.ActionFlag.SwapV
                            )
                    else:
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                self.ActionFlag.SplitHPress
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                self.ActionFlag.SplitVPress
                            )
                        self._execute_action_split_move_start_(event)
            # hover move or press move
            elif event.type() == QtCore.QEvent.MouseMove:
                # hove move
                if event.buttons() == QtCore.Qt.NoButton:
                    p = event.pos()
                    if self._contract_l_rect.contains(p):
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeLeft, self.ActionFlag.ResizeRight][self._is_contract_l]
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeUp, self.ActionFlag.ResizeDown][self._is_contract_l]
                            )
                    elif self._contract_r_rect.contains(p):
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeRight, self.ActionFlag.ResizeLeft][self._is_contract_r]
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                [self.ActionFlag.ResizeDown, self.ActionFlag.ResizeUp][self._is_contract_r]
                            )
                    elif self._swap_rect.contains(p):
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                self.ActionFlag.SwapH
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                self.ActionFlag.SwapV
                            )
                    else:
                        if self._get_orientation_() == QtCore.Qt.Horizontal:
                            self._set_action_flag_(
                                self.ActionFlag.SplitHHover
                            )
                        elif self._get_orientation_() == QtCore.Qt.Vertical:
                            self._set_action_flag_(
                                self.ActionFlag.SplitVHover
                            )
                # press move
                elif event.buttons() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.SplitHPress, self.ActionFlag.SplitVPress
                    ):
                        self._execute_action_split_move_(event)
                else:
                    pass
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                # resize
                if self._get_action_flag_is_match_(
                        self.ActionFlag.ResizeLeft, self.ActionFlag.ResizeUp
                ):
                    self._execute_contract_left_or_top_()
                elif self._get_action_flag_is_match_(
                        self.ActionFlag.ResizeRight, self.ActionFlag.ResizeDown
                ):
                    self._execute_contract_right_or_bottom_()
                # swap
                elif self._get_action_flag_is_match_(
                    self.ActionFlag.SwapH, self.ActionFlag.SwapV
                ):
                    self._execute_swap_()
                else:
                    self._execute_action_split_move_stop_(event)
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        offset = [0, 2][
            self._action_flag in {
                self.ActionFlag.SplitHPress, self.ActionFlag.SplitHMove,
                self.ActionFlag.SplitVPress, self.ActionFlag.SplitVMove
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
        for i_handle_rect in self._handle_draw_rects:
            painter._draw_icon_file_by_rect_(
                rect=i_handle_rect,
                file_path=self._resize_icon_file_path,
                offset=offset,
            )
        # contract
        c_c = self._is_contract_l, self._is_contract_r
        if c_c == (False, False):
            painter._draw_icon_file_by_rect_(
                rect=self._contract_l_draw_rect,
                file_path=self._contract_l_draw_icon_file_path,
                is_hovered=self._action_flag in {
                    self.ActionFlag.ResizeLeft, self.ActionFlag.ResizeUp,
                }
            )
            painter._draw_icon_file_by_rect_(
                rect=self._contract_r_draw_rect,
                file_path=self._contract_r_draw_icon_file_path,
                is_hovered=self._action_flag in {
                    self.ActionFlag.ResizeRight, self.ActionFlag.ResizeDown,
                }
            )
        elif c_c == (True, False):
            painter._draw_icon_file_by_rect_(
                rect=self._contract_l_draw_rect,
                file_path=self._contract_r_draw_icon_file_path,
                is_hovered=self._action_flag in {
                    self.ActionFlag.ResizeRight, self.ActionFlag.ResizeDown,
                }
            )
            painter._draw_icon_file_by_rect_(
                rect=self._contract_r_draw_rect,
                file_path=self._contract_r_draw_icon_file_path,
                is_hovered=self._action_flag in {
                    self.ActionFlag.ResizeRight, self.ActionFlag.ResizeDown,
                }
            )
        elif c_c == (False, True):
            painter._draw_icon_file_by_rect_(
                rect=self._contract_l_draw_rect,
                file_path=self._contract_l_draw_icon_file_path,
                is_hovered=self._action_flag in {
                    self.ActionFlag.ResizeLeft, self.ActionFlag.ResizeUp,
                }
            )
            painter._draw_icon_file_by_rect_(
                rect=self._contract_r_draw_rect,
                file_path=self._contract_l_draw_icon_file_path,
                is_hovered=self._action_flag in {
                    self.ActionFlag.ResizeLeft, self.ActionFlag.ResizeUp,
                }
            )
        # swap
        painter._draw_icon_file_by_rect_(
            rect=self._swap_draw_rect,
            file_path=self._swap_icon_file_path,
            is_hovered=self._action_flag in {
                self.ActionFlag.SwapH, self.ActionFlag.SwapV
            }
        )

    def _execute_contract_left_or_top_(self, size_mark=None):
        if self._is_contract_r is True:
            self._execute_contract_right_or_bottom_()
        else:
            splitter = self._get_splitter_()
            index_l = splitter._get_handle_index_(self)-1
            index_r = splitter._get_handle_index_(self)
            indices = index_l, index_r
            # switch
            self._is_contract_l = not self._is_contract_l
            # collapse to left
            if self._is_contract_l is True:
                # record size
                size_l = splitter._get_size_at_(index_l)
                size_r = splitter._get_size_at_(index_r)
                splitter._sizes_contracted_dict[index_l] = size_l
                if size_mark is not None:
                    splitter._size_fixed_dict[index_l] = size_mark
                    splitter._sizes_contracted_dict[index_l] = size_mark
                else:
                    if index_l in splitter._size_fixed_dict:
                        size_fixed = splitter._size_fixed_dict[index_l]
                        splitter._sizes_contracted_dict[index_l] = size_fixed
                #
                splitter._update_contracted_at_(index_l, True)
                splitter._accept_split_sizes_between_(indices, (0, size_l+size_r))
            # expand
            else:
                size_l = splitter._sizes_contracted_dict[index_l]
                size_r = splitter._get_size_at_(index_r)
                splitter._update_contracted_at_(index_l, False)
                splitter._accept_split_sizes_between_(indices, (size_l, (size_r-size_l)))
        #
        self._refresh_widget_draw_()

    def _execute_contract_right_or_bottom_(self, size_mark=None):
        if self._is_contract_l is True:
            self._execute_contract_left_or_top_()
        else:
            splitter = self._get_splitter_()
            index_l = splitter._get_handle_index_(self)-1
            index_r = splitter._get_handle_index_(self)
            indices = index_l, index_r
            # switch
            self._is_contract_r = not self._is_contract_r
            # collapse to right
            if self._is_contract_r is True:
                # record size
                size_l = splitter._get_size_at_(index_l)
                size_r = splitter._get_size_at_(index_r)
                splitter._sizes_contracted_dict[index_r] = size_r
                if size_mark is not None:
                    splitter._size_fixed_dict[index_r] = size_mark
                    splitter._sizes_contracted_dict[index_r] = size_mark
                else:
                    if index_r in splitter._size_fixed_dict:
                        size_fixed = splitter._size_fixed_dict[index_r]
                        splitter._sizes_contracted_dict[index_r] = size_fixed
                #
                splitter._update_contracted_at_(index_r, True)
                splitter._accept_split_sizes_between_(indices, (size_l+size_r, 0))
            else:
                size_l = splitter._get_size_at_(index_l)
                size_r = splitter._sizes_contracted_dict[index_r]
                splitter._update_contracted_at_(index_r, False)
                splitter._accept_split_sizes_between_(indices, ((size_l-size_r), size_r))
        #
        self._refresh_widget_draw_()

    def _execute_swap_(self):
        splitter = self._get_splitter_()
        index_l = splitter._get_handle_index_(self)-1
        index_r = splitter._get_handle_index_(self)
        splitter._update_by_swap_((index_l, index_r))

    def _refresh_widget_(self):
        pass

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def _get_splitter_(self):
        return self.parent()

    def _execute_action_split_move_start_(self, event):
        p = event.pos()
        self._splitter_press_pos = p.x(), p.y()
        splitter = self._get_splitter_()
        index_l = splitter._get_handle_index_(self)-1
        index_r = splitter._get_handle_index_(self)
        self._sizes_moving = [splitter._get_size_at_(index_l), splitter._get_size_at_(index_r)]
        splitter._start_split_move_at_((index_l, index_r))

    def _execute_action_split_move_(self, event):
        p = event.pos()
        x, y = p.x(), p.y()
        x_p, y_p = self._splitter_press_pos
        x -= x_p
        y -= y_p
        #
        splitter = self._get_splitter_()
        index_l, index_r = splitter._indices_moving
        indices = index_l, index_r
        s_l_o, s_r_o = splitter._get_size_at_(index_l), splitter._get_size_at_(index_r)
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            s_l, s_r = s_l_o+x, s_r_o-x
            # move left, when right is contracted ignore
            if x < 0:
                if splitter._has_index_(index_r):
                    if splitter._get_is_contracted_at_(index_r) is False:
                        # when left is first widget ignore
                        if index_l == 0:
                            if s_l <= 0:
                                return
                        splitter._accept_split_sizes_between_(indices, [s_l, s_r])
            # move right, when left is contracted ignore
            elif x > 0:
                if splitter._has_index_(index_l):
                    if splitter._get_is_contracted_at_(index_l) is False:
                        # when right is last widget ignore
                        if index_r == splitter._get_index_maximum_():
                            if s_r <= self.width():
                                return
                        splitter._accept_split_sizes_between_(indices, [s_l, s_r])
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            s_l, s_r = s_l_o+y, s_r_o-y
            # move up, same as move left
            if y < 0:
                if splitter._has_index_(index_r):
                    if splitter._get_is_contracted_at_(index_r) is False:
                        if index_l == 0:
                            if s_l <= 0:
                                return
                        splitter._accept_split_sizes_between_(indices, [s_l, s_r])
            # move down, same as move right
            elif y > 0:
                if splitter._has_index_(index_l):
                    if splitter._get_is_contracted_at_(index_l) is False:
                        if index_r == splitter._get_index_maximum_():
                            if s_r <= self.height():
                                return
                        splitter._accept_split_sizes_between_(indices, [s_l, s_r])

    def _execute_action_split_move_stop_(self, event):
        self._splitter_press_pos = 0, 0
        splitter = self._get_splitter_()
        splitter._finish_split_move_()


class _QtHSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitterHandle, self).__init__(*args, **kwargs)


class _QtVSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitterHandle, self).__init__(*args, **kwargs)


class _AbsQtSplitter(QtWidgets.QWidget):
    QT_HANDLE_CLS = None
    #
    QT_ORIENTATION = None
    #
    QT_HANDLE_WIDTH = 10
    #
    user_space_pressed = qt_signal()
    def _start_split_move_at_(self, indices):
        self._is_split_moving = True
        self._indices_moving = indices
        for i in self._indices_moving:
            self._widget_list[i].hide()
        self._refresh_widget_draw_()

    def _finish_split_move_(self):
        for i in self._indices_moving:
            self._widget_list[i].show()
        #
        self._is_split_moving = False
        self._indices_moving = []
        self._refresh_widget_draw_()

    def _update_by_swap_(self, indices):
        index_l, index_r = indices
        # swap widget
        self._widget_list[index_l], self._widget_list[index_r] = self._widget_list[index_r], self._widget_list[index_l]
        # swap contract
        for i in indices:
            self._widget_list[i].setVisible(not self._is_contracted_dict[i])
        self._refresh_widget_()

    def _accept_split_sizes_between_(self, indices, sizes):
        w, h = self.width(), self.height()
        indices_l, indices_r = indices[:indices[0]], indices[indices[1]:]
        #
        h_f_w = self.QT_HANDLE_WIDTH
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            size_min, size_max = 0+len(indices_l)*h_f_w, w-len(indices_r)*h_f_w
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            size_min, size_max = 0+len(indices_l)*h_f_w, h-len(indices_r)*h_f_w
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
            if idx in self._size_fixed_dict:
                self._size_fixed_dict[idx] = i_size
            #
            self._size_dict[idx] = i_size
        #
        self._refresh_widget_()

    def _update_contracted_at_(self, index, boolean):
        self._is_contracted_dict[index] = boolean
        self._widget_list[index].setVisible(not boolean)

    def _refresh_widget_draw_geometry_(self):
        c_pos = 0
        w, h = self.width(), self.height()
        c = len(self._handle_list)
        h_f_w = self.QT_HANDLE_WIDTH

        for idx in range(c):
            i_handle = self._handle_list[idx]
            i_widget = self._widget_list[idx]
            i_handle_rect = self._handle_rect_list[idx]
            i_widget_rect = self._widget_rect_list[idx]
            #
            i_pos = c_pos
            i_size = self._size_dict[idx]
            ns = self._size_dict.get(idx+1)
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                # handle
                hx, hy = i_pos, 0
                hw, hh = h_f_w, h
                if idx == 0:
                    hx, hy = i_pos-h_f_w, 0
                else:
                    if i_size == 0 and idx != self._index_maximum:
                        hx, hy = i_pos-h_f_w, 0
                #
                i_handle.show()
                i_handle.setGeometry(
                    hx, hy, hw, hh
                )
                #
                i_handle_rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = i_pos+h_f_w, 0
                ww, wh = i_size-h_f_w, h
                if idx == 0:
                    wx, wy = i_pos, 0
                    ww, wh = i_size, h
                if ns == 0:
                    ww, wh = i_size-h_f_w, h
                #
                i_widget_rect.setRect(
                    wx+1, wy+1, ww-2, wh-2
                )
                #
                i_widget.setGeometry(
                    wx, wy, ww, wh
                )
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                # handle
                hx, hy = 0, i_pos
                hw, hh = w, h_f_w
                if idx == 0:
                    hx, hy = 0, i_pos-h_f_w
                else:
                    if i_size == 0 and idx != self._index_maximum:
                        hx, hy = 0, i_pos-h_f_w
                #
                i_handle.show()
                i_handle.setGeometry(
                    hx, hy, hw, hh
                )
                #
                i_handle_rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = 0, i_pos+h_f_w
                ww, wh = w, i_size-h_f_w
                if idx == 0:
                    wx, wy = 0, i_pos
                    ww, wh = w, i_size
                if ns == 0:
                    ww, wh = w, i_size-h_f_w
                #
                i_widget_rect.setRect(
                    wx+1, wy+1, ww-2, wh-2
                )
                #
                i_widget.setGeometry(
                    wx, wy, ww, wh
                )
            #
            c_pos += i_size

    def _set_update_by_size_(self):
        sizes_all = [v for k, v in self._size_dict.items()]
        indices_fixed, sizes_fixed = self._get_fixed_args_()
        size_fixed = sum(sizes_fixed)

        maximum_size = sum(sizes_all)
        if maximum_size > 0:
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                w, h = self.width(), self.height()
                indices_free, sizes_free = self._get_free_args_()
                size_free_maximum = w - size_fixed
                size_free = sum(sizes_free)
                if size_free > 0:
                    for idx in self._indices:
                        if idx in indices_fixed:
                            i_size = sizes_fixed[idx]
                        else:
                            i_size = size_free_maximum*(float(sizes_free[idx])/float(size_free))
                        #
                        self._size_dict[idx] = i_size
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                w, h = self.width(), self.height()
                indices_free = [i for i in self._indices if i not in indices_fixed]
                size_free_maximum = h-size_fixed
                size_free = sum([sizes_all[i] for i in indices_free])
                if size_free > 0:
                    for idx in self._indices:
                        if idx in indices_fixed:
                            i_size = sizes_fixed[idx]
                        else:
                            i_size = size_free_maximum*(float(sizes_all[idx])/float(size_free))
                        #
                        self._size_dict[idx] = i_size
            else:
                raise TypeError()

    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitter, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._handle_list = []
        self._widget_list = []
        self._handle_rect_list = []
        self._widget_rect_list = []
        self._is_contracted_dict = {}
        self._indices = []
        self._index_maximum = 0
        self._indices_moving = ()
        self._is_split_moving = False
        #
        self._spacing = 4
        self._contents_margins = 0, 0, 0, 0
        #
        self._stretch_factor_dict = {}
        self._size_dict = collections.OrderedDict()
        self._size_draw_dict = {}
        self._size_fixed_dict = collections.OrderedDict()
        #
        self._sizes_contracted_dict = {}
        #
        self._window = None
        #
        self._is_full_size_mode = False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_()
                self._update_all_widgets_visible_()
        elif widget in self._widget_list:
            if event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Space:
                    self._update_by_widget_full_size_(widget)
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._is_split_moving:
            for i_index in self._indices_moving:
                i_is_contracted = self._is_contracted_dict[i_index]
                if i_is_contracted is False:
                    i_widget_rect = self._widget_rect_list[i_index]
                    #
                    painter._draw_frame_by_rect_(
                        rect=i_widget_rect,
                        background_color=QtBackgroundColors.Transparent,
                        border_color=QtBorderColors.SplitMoving,
                        border_width=2,
                        border_radius=1
                    )
                    painter._draw_alternating_frame_by_rect_(
                        rect=i_widget_rect,
                        colors=((31, 31, 31, 255), (35, 35, 35, 255)),
                        border_radius=1
                    )

    def _set_window_(self, widget):
        self._window = widget

    def _update_by_widget_full_size_(self, widget):
        def full_fnc_():
            widget.setGeometry(
                x_e, y_e, w_e, h_e
            )
            widget.show()
            widget.raise_()
        #
        self._is_full_size_mode = not self._is_full_size_mode
        ss = self._get_spliter_stack_()
        if self._is_full_size_mode is True:
            s_max = ss[-1]
            x_e, y_e = 0, 0
            w_e, h_e = s_max.width(), s_max.height()
            for i_s in ss:
                i_s.setGeometry(
                    0, 0, w_e, h_e
                )
                i_s.raise_()
                i_s._hide_all_handles_and_widgets_([widget, widget.parent()])
            #
            full_fnc_()
        else:
            for i_s in ss:
                i_s._refresh_widget_()
                i_s._update_all_widgets_visible_()

    def _update_all_widgets_visible_(self):
        for i in self._indices:
            if self._is_contracted_dict[i] is True:
                self._widget_list[i].hide()
            else:
                self._widget_list[i].show()

    def _hide_all_handles_and_widgets_(self, excludes):
        for i in self._widget_list:
            if i in excludes:
                continue
            i.hide()

    def _get_spliter_stack_(self):
        def rcs_fnc_(w_):
            _p = w_.parent()
            if isinstance(_p, _AbsQtSplitter):
                list_.append(_p)
                rcs_fnc_(_p)
        #
        list_ = [self]
        rcs_fnc_(self)
        return list_

    def _refresh_widget_(self):
        self._set_update_by_size_()
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _get_fixed_args_(self):
        indices = []
        sizes = [0 for _ in self._indices]
        for idx in self._indices:
            # when contracted use 0
            is_contracted = self._is_contracted_dict[idx]
            if is_contracted is False:
                if idx in self._size_fixed_dict:
                    i_size = self._size_fixed_dict[idx]
                    indices.append(idx)
                    sizes[idx] = i_size
            else:
                sizes[idx] = self.QT_HANDLE_WIDTH
        return indices, sizes

    def _get_free_args_(self):
        indices = []
        sizes = [0 for _ in self._indices]
        for idx in self._indices:
            is_contracted = self._is_contracted_dict[idx]
            if is_contracted is False:
                if idx not in self._size_fixed_dict:
                    indices.append(idx)
                    i_size = self._size_dict[idx]
                    sizes[idx] = i_size
        return indices, sizes

    def _add_widget_(self, widget):
        index = len(self._handle_list)
        #
        w_parent = widget.parent()
        if w_parent is None:
            widget.setParent(self)
        #
        self._widget_list.append(widget)
        #
        handle = self.QT_HANDLE_CLS()
        handle.setParent(self)
        self._handle_list.append(handle)
        #
        if index not in self._size_dict:
            self._size_dict[index] = 1
            self._size_draw_dict[index] = 1
            self._indices.append(index)
            self._index_maximum = len(self._indices) - 1
            self._is_contracted_dict[index] = False
        #
        self._handle_rect_list.append(QtCore.QRect())
        self._widget_rect_list.append(QtCore.QRect())
        #
        if not isinstance(widget, _AbsQtSplitter):
            widget.installEventFilter(self)

    def _get_widget_at_(self, index):
        return self._widget_list[index]

    def _get_size_at_(self, index):
        return self._size_dict[index]

    def _set_size_at_(self, index, size):
        self._size_dict[index] = size
        #
        self._refresh_widget_()

    def _get_sizes_(self, indices=None):
        if indices is not None:
            return [self._size_dict[i] for i in indices]
        return [i for i in self._size_dict.values()]

    def _set_fixed_size_at_(self, index, value):
        self._size_fixed_dict[index] = value

    def _get_indices_(self):
        return self._size_dict.keys()

    def _get_widgets_(self):
        return self._widget_list

    def _get_widget_(self, index):
        return self._widget_list[index]

    def _has_index_(self, index):
        return index in self._indices

    def _get_index_maximum_(self):
        return self._index_maximum

    def _set_widget_hide_at_(self, index):
        handle = self._get_handle_at_(index+1)
        handle._execute_contract_left_or_top_()
    
    def _set_contract_left_or_top_at_(self, index, size=None):
        self._is_contracted_dict[index] = True
        handle = self._get_handle_at_(index+1)
        handle._execute_contract_left_or_top_(size)

    def _set_contract_right_or_bottom_at_(self, index, size=None):
        self._is_contracted_dict[index] = True
        handle = self._get_handle_at_(index)
        handle._execute_contract_right_or_bottom_(size)

    def _get_is_contracted_at_(self, index):
        return self._is_contracted_dict[index]

    def _get_cur_index_(self, qt_point):
        for idx, i_handle_rect in enumerate(self._handle_rect_list):
            if i_handle_rect.contains(qt_point) is True:
                return idx

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def _set_stretch_factors_(self, values):
        for seq, i in enumerate(values):
            self._set_stretch_factor_at_(seq, i)
        # self._set_update_by_size_()

    def _set_stretch_factor_at_(self, index, size):
        self._stretch_factor_dict[index] = size
        self._size_dict[index] = size

    def _get_stretch_factor_at_(self, index):
        return self._stretch_factor_dict[index]

    def _get_handle_at_(self, index):
        return self._handle_list[index]

    def _get_handle_index_(self, handle):
        return self._handle_list.index(handle)


class QtHSplitter(_AbsQtSplitter):
    QT_HANDLE_CLS = _QtHSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(QtHSplitter, self).__init__(*args, **kwargs)


class QtVSplitter(_AbsQtSplitter):
    QT_HANDLE_CLS = _QtVSplitterHandle
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
