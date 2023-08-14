# coding=utf-8
from lxutil_gui.qt.gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _gui_qt_wgt_entry_base, _utl_gui_qt_wgt_popup, _gui_qt_wgt_chart

import lxutil_gui.qt.abstracts as gui_qt_abstract


class QtPressItem(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtStatusBaseDef,
    #
    gui_qt_abstract.AbsQtSubProcessDef,
    gui_qt_abstract.AbsQtValidatorDef,
    #
    gui_qt_abstract.AbsQtIconBaseDef,
    gui_qt_abstract.AbsQtMenuBaseDef,
    gui_qt_abstract.AbsQtNameBaseDef,
    gui_qt_abstract.AbsQtProgressDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,
    gui_qt_abstract.AbsQtCheckBaseDef,
    gui_qt_abstract.AbsQtActionForOptionPressDef,
):
    clicked = qt_signal()
    checked = qt_signal()
    toggled = qt_signal(bool)
    option_clicked = qt_signal()
    #
    status_changed = qt_signal(int)
    #
    rate_status_update_at = qt_signal(int, int)
    rate_finished_at = qt_signal(int, int)
    rate_finished = qt_signal()
    #
    QT_MENU_CLS = _utl_gui_qt_wgt_utility.QtMenu
    def __init__(self, *args, **kwargs):
        super(QtPressItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        self.setFont(Font.NAME)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        self.installEventFilter(self)
        #
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_status_base_def_(self)
        self._set_sub_process_def_init_()
        self._set_validator_def_init_(self)
        #
        self._init_icon_base_def_(self)
        self._init_name_base_def_(self)
        self._init_menu_base_def_(self)
        self._set_progress_def_init_()
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_check_base_def_(self)
        self._init_action_for_option_press_def_(self)
        #
        self._refresh_check_draw_()
        #
        self._set_name_draw_font_(QtFonts.Button)
        #
        r, g, b = 167, 167, 167
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 151, 151, 151
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color

        self.status_changed.connect(
            self._set_status_
        )
        self.rate_status_update_at.connect(
            self._set_sub_process_status_at_
        )
        self.rate_finished_at.connect(
            self._set_sub_process_finished_at_
        )

        self._sub_process_timer = QtCore.QTimer(self)

        self._sub_process_timer.timeout.connect(
            self._refresh_sub_process_draw_
        )

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        check_enable = self._get_check_action_is_enable_()
        option_click_enable = self._get_option_click_is_enable_()
        status_is_enable = self._get_status_is_enable_()
        sub_process_is_enable = self._get_sub_process_is_enable_()
        validator_is_enable = self._get_validator_is_enable_()
        progress_enable = self._get_progress_is_enable_()
        #
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        #
        i_f_w, i_f_h = self._icon_draw_size
        i_c_w, i_c_h = self._icon_color_draw_size
        i_n_w, i_n_h = self._icon_name_draw_size
        #
        c_x, c_y = x, y
        c_w, c_h = w, h
        #
        c_icn_x, c_icn_y = x, y
        c_icn_w, c_icn_h = w, h
        #
        if check_enable is True:
            self._check_rect.setRect(
                c_icn_x, c_icn_y, icn_frm_w, icn_frm_h
            )
            self._check_icon_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_f_w)/2, c_icn_y+(icn_frm_h-i_f_h)/2, i_f_w, i_f_h
            )
            c_icn_x += icn_frm_h
            c_icn_w -= icn_frm_w
            c_x += icn_frm_h
            c_w -= icn_frm_w
        #
        if self._icon_is_enable is True:
            self._icon_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_f_w)/2, c_icn_y+(icn_frm_h-i_f_h)/2, i_f_w, i_f_h
            )
            self._icon_color_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_c_w)/2, c_icn_y+(icn_frm_h-i_c_h)/2, i_c_w, i_c_h
            )
            self._icon_name_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_n_w)/2, c_icn_y+(icn_frm_h-i_n_h)/2, i_n_w, i_n_h
            )
            c_icn_x += icn_frm_h
            c_icn_w -= icn_frm_w
        # option
        if self._get_option_click_is_enable_() is True:
            self._option_click_rect.setRect(
                w-icn_frm_w, y, icn_frm_w, icn_frm_h
            )
            self._option_click_icon_rect.setRect(
                (w-icn_frm_w)+(icn_frm_w-i_f_w)/2, y+(icn_frm_h-i_f_h)/2, i_f_w, i_f_h
            )
            c_icn_w -= icn_frm_w
            c_w -= icn_frm_w
        #
        self._frame_draw_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._status_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._name_draw_rect.setRect(
            c_icn_x, c_icn_y, c_icn_w, c_icn_h
        )
        # progress
        if progress_enable is True:
            progress_percent = self._get_progress_percent_()
            self._progress_rect.setRect(
                c_x, c_y, c_w * progress_percent, 4
            )
        #
        if status_is_enable is True:
            self._status_rect.setRect(
                c_x, c_y, c_w, c_h
            )
        #
        e_h = 2
        if sub_process_is_enable is True:
            self._sub_process_status_rect.setRect(
                c_x, c_h-e_h, c_w, e_h
            )
        #
        if validator_is_enable is True:
            self._validator_status_rect.setRect(
                c_x, c_h-e_h, c_w, e_h
            )

    def _set_sub_process_initialization_(self, count, status):
        super(QtPressItem, self)._set_sub_process_initialization_(count, status)
        if count > 0:
            self._set_status_(
                self.Status.Started
            )
            self._sub_process_timer.start(100)

    def _set_sub_process_finished_at_(self, index, status):
        super(QtPressItem, self)._set_sub_process_finished_at_(index, status)
        # check is finished
        if self._get_sub_process_is_finished_() is True:
            if self.Status.Failed in self._sub_process_statuses:
                self._set_status_(
                    self.Status.Failed
                )
            else:
                self._set_status_(
                    self.Status.Completed
                )
            self.rate_finished.emit()

            self._sub_process_timer.stop()

        self._refresh_widget_draw_()

    def _set_sub_process_finished_connect_to_(self, fnc):
        self.rate_finished.connect(fnc)

    def _set_sub_process_restore_(self):
        super(QtPressItem, self)._set_sub_process_restore_()

        self._set_status_(
            self.Status.Stopped
        )

    def _execute_(self):
        self.press_clicked.emit()

    def setText(self, text):
        self._name_text = text

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            # update rect first
            action_enable = self._get_action_is_enable_()
            check_enable = self._get_check_action_is_enable_()
            click_enable = self._get_action_press_is_enable_()
            option_click_enable = self._get_option_click_is_enable_()
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Show:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            #
            if action_enable is True:
                if event.type() == QtCore.QEvent.Enter:
                    self._is_hovered = True
                    self.update()
                elif event.type() == QtCore.QEvent.Leave:
                    self._is_hovered = False
                    self.update()
                # press
                elif event.type() in [QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick]:
                    self._action_flag = None
                    #
                    flag_raw = [
                        (check_enable, self._check_rect, self.ActionFlag.CheckClick),
                        (click_enable, self._frame_draw_rect, self.ActionFlag.PressClick),
                        (option_click_enable, self._option_click_rect, self.ActionFlag.OptionClick),
                    ]
                    if event.button() == QtCore.Qt.LeftButton:
                        pos = event.pos()
                        for i_enable, i_rect, i_flag in flag_raw:
                            if i_enable is True:
                                if i_rect.contains(pos) is True:
                                    self._action_flag = i_flag
                                    break
                    elif event.button() == QtCore.Qt.RightButton:
                        self._popup_menu_()
                    #
                    self._is_hovered = True
                    self.update()
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if self._action_flag == self.ActionFlag.CheckClick:
                        self._execute_check_swap_()
                        self.checked.emit()
                        self.press_clicked.emit()
                    elif self._action_flag == self.ActionFlag.PressClick:
                        self.clicked.emit()
                        self.press_clicked.emit()
                    elif self._action_flag == self.ActionFlag.OptionClick:
                        self.option_clicked.emit()
                    #
                    self._action_flag = None
                    self.update()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        if self._action_is_enable is True:
            border_color = [self._frame_border_color, self._hovered_frame_border_color][self._is_hovered]
            background_color = [self._frame_background_color, self._hovered_frame_background_color][self._is_hovered]
        else:
            border_color = QtBorderColors.ButtonDisable
            background_color = QtBackgroundColors.ButtonDisable
        #
        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=border_color,
            background_color=background_color,
            border_radius=4,
            offset=offset
        )
        # status
        if self._get_status_is_enable_() is True:
            status_rgba = [self._status_color, self._hover_status_color][self._is_hovered]
            # painter._set_status_draw_by_rect_(
            #     self._status_rect,
            #     color=status_rgba,
            #     border_radius=4,
            #     offset=offset
            # )
        # sub process
        if self._get_sub_process_is_enable_() is True:
            status_rgba = [self._status_color, self._hover_status_color][self._is_hovered]
            status_rgba_array = [self._sub_process_status_colors, self._hover_sub_process_status_colors][self._is_hovered]
            #
            r, g, b, a = status_rgba
            painter._draw_alternating_colors_by_rect_(
                rect=self._frame_draw_rect,
                colors=((r, g, b, 63), (0, 0, 0, 0)),
                offset=offset,
                border_radius=4,
                running=not self._get_sub_process_is_finished_()
            )
            #
            painter._draw_process_statuses_by_rect_(
                rect=self._sub_process_status_rect,
                colors=status_rgba_array,
                offset=offset,
                border_radius=1,
            )
        # validator
        elif self._get_validator_is_enable_() is True:
            status_rgba_array = [self._validator_status_colors, self._hover_validator_status_colors][self._is_hovered]
            painter._draw_process_statuses_by_rect_(
                self._validator_status_rect,
                colors=status_rgba_array,
                offset=offset,
                border_radius=1,
            )
        #
        if self._get_progress_is_enable_() is True:
            painter._draw_frame_by_rect_(
                rect=self._progress_rect,
                border_color=QtBackgroundColors.Transparent,
                background_color=Color.PROGRESS,
                border_radius=2,
                offset=offset
            )
        # check
        if self._get_check_action_is_enable_() is True:
            painter._draw_icon_file_by_rect_(
                self._check_icon_draw_rect,
                self._check_icon_file_path_current,
                offset=offset,
                is_hovered=self._is_hovered
            )
        # icon
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    self._icon_draw_rect,
                    self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered
                )
            elif self._icon_color_rgb is not None:
                painter._set_color_icon_draw_(
                    self._icon_color_draw_rect, self._icon_color_rgb, offset=offset
                )
            elif self._icon_name_text is not None:
                painter._draw_image_use_text_by_rect_(
                    self._icon_name_draw_rect,
                    self._icon_name_text,
                    offset=offset,
                    border_radius=2,
                    is_hovered=self._is_hovered
                )
        # name
        if self._name_text is not None:
            name_text = self._name_text
            if self._action_is_enable is True:
                text_color = [QtFontColors.Basic, QtFontColors.Light][self._is_hovered]
            else:
                text_color = QtFontColors.Disable
            #
            if self._get_sub_process_is_enable_() is True:
                name_text = '{} - {}'.format(
                    self._name_text, self._get_sub_process_status_text_()
                )
            #
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                text=name_text,
                font_color=text_color,
                font=self._name_draw_font,
                offset=offset
            )
        # option
        if self._get_option_click_is_enable_() is True:
            painter._draw_icon_file_by_rect_(
                self._option_click_icon_rect,
                self._option_icon_file_path,
                offset=offset,
                is_hovered=self._is_hovered
            )


class QtCheckItem(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtIconBaseDef,
    gui_qt_abstract.AbsQtNameBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtCheckBaseDef,
    #
    gui_qt_abstract.AbsQtValueDefaultDef,
):
    def __init__(self, *args, **kwargs):
        super(QtCheckItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        self.setFont(Font.NAME)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        self.installEventFilter(self)
        #
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_name_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_check_base_def_(self)
        self._set_check_enable_(True)
        #
        self._init_value_default_def_()
        #
        self._refresh_check_draw_()
        #
        self._set_name_draw_font_(QtFonts.Button)

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_w, icn_h = self._icon_draw_size
        #
        self._set_frame_draw_rect_(
            x, y, w-1, h-1
        )
        self._set_check_action_rect_(
            x, y, icn_frm_w, icn_frm_h
        )
        #
        self._set_check_icon_draw_rect_(
            x+(icn_frm_w-icn_w)/2, y+(icn_frm_h-icn_h)/2, icn_w, icn_h
        )
        x += icn_frm_w+spacing
        self._set_name_draw_rect_(
            x, y, w-x, h
        )

    def _get_value_(self):
        return self._get_is_checked_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckClick)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckClick:
                        self._send_check_emit_()
                    #
                    self.user_check_clicked.emit()
                    #
                    self._clear_all_action_flags_()
            # elif event.type() == QtCore.QEvent.ToolTip:
            #     pos = event.globalPos()
            #     QtWidgets.QToolTip.showText(
            #         pos, self._tool_tip_text, self, QtCore.QRect(pos.x(), pos.y(), 480, 160)
            #     )
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        if self._check_is_enable is True:
            if self._check_icon_file_path_current is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._check_icon_draw_rect,
                    file_path=self._check_icon_file_path_current,
                    offset=offset,
                    is_hovered=self._is_hovered
                )
        #
        if self._name_text is not None:
            name_text = self._name_text
            if self._action_is_enable is True:
                text_color = [QtFontColors.Basic, QtFontColors.Light][self._is_hovered]
            else:
                text_color = QtFontColors.Disable
            #
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=name_text,
                font=self._name_draw_font,
                font_color=text_color,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )


class _QtStatusItem(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtNameBaseDef,
    gui_qt_abstract.AbsQtIconBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtCheckBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtStatusItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        self.installEventFilter(self)
        #
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_name_base_def_(self)
        self._set_name_text_('status button')
        self._init_icon_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_check_base_def_(self)
        #
        self._refresh_check_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        icn_w, icn_h = self._icon_color_draw_size
        self._set_color_icon_rect_(
            x+(w-icn_w)/2, y+(h-icn_h)/2, icn_w, icn_h
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckClick)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckClick:
                        self._send_check_emit_()
                #
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        is_hovered = self._get_is_hovered_()
        #
        if self._get_is_checked_():
            background_color = [QtStatusColors.Warning, QtBackgroundColors.Hovered][is_hovered]
            painter._draw_image_use_text_by_rect_(
                rect=self._icon_color_draw_rect,
                text='l',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered,
                border_radius=1
            )
        else:
            background_color = [QtStatusColors.Normal, QtBackgroundColors.Hovered][is_hovered]
            painter._draw_image_use_text_by_rect_(
                rect=self._icon_color_draw_rect,
                text='d',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered,
                border_radius=1
            )


class _QtHContractItem(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtIconBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,
    gui_qt_abstract.AbsQtActionForExpandDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtHContractItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        #
        self._name_draw_font = Font.GROUP
        #
        self._init_icon_base_def_(self)
        self._icon_name_is_enable = True
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expanded = False
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('contract_v_l')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('contract_v_r')

        self._expand_sub_icon_file_path_0 = None
        self._expand_sub_icon_file_path_1 = None

        self._is_hovered = False
        #
        self._refresh_expand_()
        #
        r, g, b = 207, 207, 207
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._name_color = color
        self._hover_name_color = hover_color
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        # font
        self.setFont(Font.NAME)

        self._icon_frame_draw_size = 12, 24
        self._icon_draw_percent = 1
        self._icon_draw_size = 10, 20

    def _set_expand_direction_(self, direction):
        if direction == self.CollapseDirection.RightToLeft:
            self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('contract_v_l')
            self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('contract_v_r')
        elif direction == self.CollapseDirection.LeftToRight:
            self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('contract_v_r')
            self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('contract_v_l')
        #
        self._refresh_expand_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        #
        frm_w, frm_h = self._icon_frame_draw_size
        icn_w, icn_h = self._icon_draw_size
        self._set_icon_file_draw_rect_(
            c_x+(w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
        )

    def _set_expand_icon_file_path_(self, icon_file_path_0, icon_file_path_1):
        self._expand_icon_file_path_0 = icon_file_path_0
        self._expand_icon_file_path_1 = icon_file_path_1
        self._refresh_expand_()

    def _set_expand_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get(icon_name_0)
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get(icon_name_1)
        self._refresh_expand_()

    def _set_expand_sub_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_sub_icon_file_path_0 = utl_gui_core.RscIconFile.get(icon_name_0)
        self._expand_sub_icon_file_path_1 = utl_gui_core.RscIconFile.get(icon_name_1)
        self._refresh_expand_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.ExpandClick)
                    #
                    self.press_toggled.emit(True)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.ExpandClick:
                        self._execute_action_expand_()
                    #
                    self.press_toggled.emit(False)
                #
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._is_hovered
        )

    def set_expanded(self, boolean):
        self._is_expanded = boolean

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
        )
        self._set_icon_sub_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._is_expanded]
        )
        #
        self._set_action_hovered_(False)
        self._refresh_widget_draw_()


class _QtWindowHead(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtWindowHead, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
        #
        self._init_frame_base_def_(self)
        #
        self._frame_background_color = 71, 71, 71, 255
        self._frame_border_color = 95, 95, 95, 255
        #
        self._close_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._close_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('close')
        )
        self._close_button._set_hover_icon_file_path_(
            utl_gui_core.RscIconFile.get('close-hover')
        )
        #
        self._close_button.press_clicked.connect(
            self._set_window_close_
        )
        #
        self._orientation = QtCore.Qt.Horizontal

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

    def _set_window_close_(self):
        self.parent().close()
        self.parent().deleteLater()

    def _set_widget_geometries_update_(self):
        pos_x, pos_y = 0, 0
        width, height = self.width(), self.height()
        self._set_frame_draw_rect_(
            pos_x, pos_y, width, height
        )
        #
        side = 2
        i_x, i_y = width-side, pos_y+side
        i_w, i_h = 20, 20
        if self._orientation == QtCore.Qt.Horizontal:
            self._close_button.setGeometry(
                i_x-i_w, i_y, i_w, i_h
            )
