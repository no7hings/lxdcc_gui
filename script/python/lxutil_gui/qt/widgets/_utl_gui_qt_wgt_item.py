# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_entry, _utl_gui_qt_wgt_popup, _utl_gui_qt_wgt_chart

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class QtPressItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtStatusDef,
    #
    utl_gui_qt_abstract.AbsQtSubProcessDef,
    utl_gui_qt_abstract.AbsQtValidatorDef,
    #
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtMenuDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtProgressDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForCheckDef,
    utl_gui_qt_abstract.AbsQtActionForOptionPressDef,
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
    QT_MENU_CLASS = _utl_gui_qt_wgt_utility.QtMenu
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
        self._set_frame_def_init_()
        self._set_status_def_init_()
        self._set_sub_process_def_init_()
        self._set_validator_def_init_(self)
        #
        self._init_icon_def_(self)
        self._init_name_def_(self)
        self._init_menu_def_()
        self._set_progress_def_init_()
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_check_def_(self)
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
            self._set_sub_process_update_draw_
        )

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        check_enable = self._get_check_action_is_enable_()
        option_click_enable = self._get_item_option_click_enable_()
        status_is_enable = self._get_status_is_enable_()
        sub_process_is_enable = self._get_sub_process_is_enable_()
        validator_is_enable = self._get_validator_is_enable_()
        progress_enable = self._get_progress_is_enable_()
        #
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        #
        i_f_w, i_f_h = self._icon_file_draw_size
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
            self._check_action_rect.setRect(
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
            self._icon_file_draw_rect.setRect(
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
        if option_click_enable is True:
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
        e_h = 4
        if sub_process_is_enable is True:
            self._sub_process_status_rect.setRect(
                c_x, c_h-e_h, c_w, e_h
            )
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
            self._sub_process_timer.start(1000)

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
            option_click_enable = self._get_item_option_click_enable_()
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            #
            if action_enable is True:
                if event.type() == QtCore.QEvent.Enter:
                    self._action_is_hovered = True
                    self.update()
                elif event.type() == QtCore.QEvent.Leave:
                    self._action_is_hovered = False
                    self.update()
                # press
                elif event.type() in [QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick]:
                    self._action_flag = None
                    #
                    flag_raw = [
                        (check_enable, self._check_action_rect, self.ActionFlag.CheckClick),
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
                        self._set_menu_show_()
                    #
                    self._action_is_hovered = True
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
        #
        offset = self._get_action_offset_()
        #
        if self._action_is_enable is True:
            border_color = [self._frame_border_color, self._hovered_frame_border_color][self._action_is_hovered]
            background_color = [self._frame_background_color, self._hovered_frame_background_color][self._action_is_hovered]
        else:
            border_color = QtBorderColors.ButtonDisable
            background_color = QtBackgroundColors.ButtonDisable
        #
        # print self._frame_draw_rect
        # painter.fillRect(
        #     self._frame_draw_rect, QtGui.QColor(255, 0, 0, 255)
        # )
        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=border_color,
            background_color=background_color,
            border_radius=4,
            offset=offset
        )
        #
        if self._get_status_is_enable_() is True:
            status_color = [self._status_color, self._hover_status_color][self._action_is_hovered]
            painter._set_status_draw_by_rect_(
                self._status_rect,
                color=status_color,
                border_radius=4,
                offset=offset
            )
        # sub process
        if self._get_sub_process_is_enable_() is True:
            status_colors = [self._sub_process_status_colors, self._hover_sub_process_status_colors][self._action_is_hovered]
            painter._set_elements_status_draw_by_rect_(
                self._sub_process_status_rect,
                colors=status_colors,
                offset=offset,
                border_radius=2,
            )
        # validator
        elif self._get_validator_is_enable_() is True:
            status_colors = [self._validator_status_colors, self._hover_validator_status_colors][self._action_is_hovered]
            painter._set_elements_status_draw_by_rect_(
                self._validator_status_rect,
                colors=status_colors,
                offset=offset,
                border_radius=2,
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
                is_hovered=self._action_is_hovered
            )
        # icon
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    self._icon_file_draw_rect,
                    self._icon_file_path,
                    offset=offset,
                    is_hovered=self._action_is_hovered
                )
            elif self._icon_color_rgb is not None:
                painter._set_color_icon_draw_(
                    self._icon_color_draw_rect, self._icon_color_rgb, offset=offset
                )
            elif self._icon_name_text is not None:
                painter._draw_icon_with_name_text_by_rect_(
                    self._icon_name_draw_rect,
                    self._icon_name_text,
                    offset=offset,
                    border_radius=2,
                    is_hovered=self._action_is_hovered
                )
        # name
        if self._name_text is not None:
            name_text = self._name_text
            if self._action_is_enable is True:
                text_color = [QtFontColors.Basic, QtFontColors.Light][self._action_is_hovered]
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
        if self._get_item_option_click_enable_() is True:
            painter._draw_icon_file_by_rect_(
                self._option_click_icon_rect,
                self._option_icon_file_path,
                offset=offset,
                is_hovered=self._action_is_hovered
            )


class QtCheckItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForCheckDef,
    #
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
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
        self._set_frame_def_init_()
        self._init_icon_def_(self)
        self._init_name_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)
        self._set_check_enable_(True)
        #
        self._set_value_default_def_init_()
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
        icn_w, icn_h = self._icon_file_draw_size
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
            self._set_action_hover_filter_execute_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckClick)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckClick:
                        self._send_check_emit_()
                    #
                    self.user_check_clicked.emit()
                    #
                    self._clear_action_flag_()
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
                    is_hovered=self._action_is_hovered
                )
        #
        if self._name_text is not None:
            name_text = self._name_text
            if self._action_is_enable is True:
                text_color = [QtFontColors.Basic, QtFontColors.Light][self._action_is_hovered]
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


class _QtEnableItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtWidgetDef,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForCheckDef,
    #
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtEnableItem, self).__init__(*args, **kwargs)
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
        self._init_widget_def_(self)
        self._set_frame_def_init_()
        self._init_icon_def_(self)
        self._init_name_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)
        self._set_check_enable_(True)
        #
        self._set_value_default_def_init_()
        #
        self._refresh_check_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_w, icn_h = self._icon_file_draw_size
        #
        self._set_frame_draw_rect_(
            x, y, w-1, h-1
        )
        self._set_check_action_rect_(
            x, y, icn_frm_w, icn_frm_h
        )
        #
        if self._icon_is_enable is True:
            self._set_icon_file_draw_rect_(
                x+(icn_frm_w-icn_w)/2, y+(icn_frm_h-icn_h)/2, icn_w, icn_h
            )
        #
        x += icn_frm_w+spacing
        self._set_name_draw_rect_(
            x, y, w-x, h
        )

    def _get_value_(self):
        return self._get_is_checked_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_action_hover_filter_execute_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckClick)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckClick:
                        self._send_check_emit_()
                    #
                    self._clear_action_flag_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        background_color = painter._get_item_background_color_by_rect_(
            self._check_action_rect,
            is_hovered=self._action_is_hovered,
            is_selected=self._is_checked,
            is_actioned=self._get_is_actioned_()
        )
        painter._draw_frame_by_rect_(
            self._check_action_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            border_radius=2,
            offset=offset
        )
        #
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_file_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._action_is_hovered
                )
        #
        if self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=Font.NAME,
                font_color=QtFontColors.Basic,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )


class _QtStatusItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForCheckDef,
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
        self._set_frame_def_init_()
        self._init_icon_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)
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
            self._set_action_hover_filter_execute_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckClick)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckClick:
                        self._send_check_emit_()
                #
                self._clear_action_flag_()
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
            background_color = [(255, 255, 63), (255, 127, 63)][is_hovered]
            painter._draw_icon_with_name_text_by_rect_(
                rect=self._icon_color_draw_rect,
                text='l',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered
            )
        else:
            background_color = [(71, 71, 71), (255, 127, 63)][is_hovered]
            painter._draw_icon_with_name_text_by_rect_(
                rect=self._icon_color_draw_rect,
                text='d',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered
            )


class QtValueEntryAsConstant(
    _utl_gui_qt_wgt_entry.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryBaseDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtConstantEntry
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsConstant, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_base_def_(self)
        self._set_value_default_def_init_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._build_entry_(self._value_type)

    def _build_entry_(self, value_type):
        self._value_type = value_type
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(self._value_type)

    def _set_value_entry_validator_use_as_name_(self):
        self._value_entry._set_validator_use_as_name_()

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsConstant, self)._set_value_entry_enable_(boolean)

        self._value_entry.setReadOnly(not boolean)

        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dim
        ][boolean]
        self._refresh_widget_draw_()


class QtValueEntryAsScript(
    _utl_gui_qt_wgt_entry.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryBaseDef,
    #
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtContentEntry
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsScript, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_base_def_(self)
        self._set_value_default_def_init_()
        #
        self._build_entry_(self._value_type)

        # self._frame_background_color = QtBackgroundColors.Dark

    def _build_entry_(self, value_type):
        self._value_type = value_type
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(2)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry._set_entry_frame_(self)
        # self._value_entry.setReadOnly(False)
        self._value_entry_layout.addWidget(self._value_entry)

        self._resize_handle.raise_()

    def _set_item_value_entry_enable_(self, boolean):
        self._value_entry.setReadOnly(not boolean)

    def _set_resize_enable_(self, boolean):
        self._resize_handle.setVisible(boolean)

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsScript, self)._set_value_entry_enable_(boolean)

        self._value_entry.setReadOnly(not boolean)
        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dim
        ][boolean]
        self._refresh_widget_draw_()


class QtValueEntryAsPopupRgbaChoose(
    _utl_gui_qt_wgt_entry.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtRgbaDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryBaseDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtConstantEntry
    #
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForRgbaChoose
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsPopupRgbaChoose, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        self._set_rgba_def_init_()
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        #
        self._init_value_entry_base_def_(self)
        self._set_value_default_def_init_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(20, 0, 0, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._build_entry_(self._value_type)

    def _build_entry_(self, value_type):
        self._value_type = value_type
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(self._value_type)

    def _refresh_widget_draw_geometry_(self):
        super(QtValueEntryAsPopupRgbaChoose, self)._refresh_widget_draw_geometry_()
        #
        x, y = 0, 0
        w, h = 20, self.height()
        c_w, c_h = 16, 16
        self._color_rect.setRect(
            x+2, y+(h-c_h)/2, c_w, c_h
        )

    def eventFilter(self, *args):
        super(QtValueEntryAsPopupRgbaChoose, self).eventFilter(*args)
        #
        widget, event = args
        if widget == self:
            self._set_action_hover_filter_execute_(event)
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressClick)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._action_is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self.press_db_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_press_flag_is_click_() is True:
                        self.press_clicked.emit()
                        self._set_color_choose_drop_()
                #
                self._clear_action_flag_()
                #
                self._action_is_hovered = False
                self.update()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtValueEntryAsPopupRgbaChoose, self).paintEvent(self)
        #
        painter = QtPainter(self)
        self._refresh_widget_draw_geometry_()
        # name
        if self._color_rgba is not None:
            offset = self._get_action_offset_()
            background_color = self._get_color_rgba_255_()
            painter._draw_frame_by_rect_(
                self._color_rect,
                border_color=QtBorderColors.Transparent,
                background_color=background_color,
                offset=offset
            )

    def _set_color_choose_drop_(self):
        widget = self.QT_POPUP_CHOOSE_CLS(self)
        # widget._set_popup_offset_(0, 22)
        widget._execute_popup_start_()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self.update()

    def _set_value_entry_enable_(self, boolean):
        pass


class QtValueEntryAsPopupConstantChoose(
    _utl_gui_qt_wgt_entry.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForEntryDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryAsPopupChoose,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
    #
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtChooseAsPopupDef,
    utl_gui_qt_abstract.AbsQtCompletionAsPopupDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtConstantEntry
    #
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForChoose
    QT_POPUP_COMPLETION_CLASS = _utl_gui_qt_wgt_popup.QtPopupForCompletion
    def _execute_popup_choose_(self):
        self._popup_choose_frame._execute_popup_start_()

    def _refresh_widget_(self):
        self._refresh_choose_index_()
        self._refresh_widget_draw_()

    def _refresh_choose_index_(self):
        if self._choose_index_showable is True:
            values = self._get_choose_values_()
            if values:
                if self._value_entry_is_enable is True:
                    value = self._get_value_()
                    if value in values:
                        self._value_index_label.show()
                        maximum = len(values)
                        value = values.index(value) + 1
                        text = '{}/{}'.format(value, maximum)
                        self._value_index_label._set_name_text_(text)
                        width = self._value_index_label._get_name_text_draw_width_(text)
                        self._value_index_label.setMinimumWidth(width + 4)
                    else:
                        self._value_index_label.hide()
            else:
                self._value_entry._set_value_clear_()
                self._value_index_label.hide()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsPopupConstantChoose, self).__init__(*args, **kwargs)
        self._init_action_base_def_(self)
        self._init_set_action_for_entry_def_(self)
        #
        self._set_value_entry_enumerate_init_(self)
        self._set_value_default_def_init_()
        #
        self._set_choose_def_init_()
        self._init_choose_as_popup_def_(self)
        self._init_completion_as_popup_def_(self)
        #
        self._build_entry_(self._value_type)
        #
        self.installEventFilter(self)

    def eventFilter(self, *args):
        super(QtValueEntryAsPopupConstantChoose, self).eventFilter(*args)
        #
        widget, event = args
        if widget == self:
            if hasattr(self, '_action_is_enable') is True:
                if self._action_is_enable is True:
                    if event.type() == QtCore.QEvent.Wheel:
                        self._execute_action_wheel_(event)
        return False

    def _execute_action_wheel_(self, event):
        delta = event.angleDelta().y()
        values = self._get_choose_values_()
        pre_value = self._get_value_()
        maximum = len(values)-1
        if pre_value in values:
            pre_index = values.index(pre_value)
            if delta > 0:
                cur_index = pre_index-1
            else:
                cur_index = pre_index+1
            cur_index = max(min(cur_index, maximum), 0)
            if cur_index != pre_index:
                self._set_value_(values[cur_index])
                # set value before
                self.user_choose_changed.emit()

    def _build_entry_(self, value_type):
        self._value_type = value_type
        #
        self._main_layout = QtVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        entry_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._main_layout.addWidget(entry_widget)
        #
        self._value_entry_layout = QtHBoxLayout(entry_widget)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(2)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_entry_frame_(self)
        self._value_entry._set_value_type_(self._value_type)
        self._value_entry._set_entry_enable_(False)
        #
        self._value_index_label = _utl_gui_qt_wgt_utility.QtTextItem()
        self._value_index_label.hide()
        self._value_entry_layout.addWidget(self._value_index_label)
        self._value_index_label._set_name_color_(QtFontColors.Disable)
        self._value_index_label.hide()
        #
        button_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._value_entry_layout.addWidget(button_widget)
        self._entry_button_layout = QtHBoxLayout(button_widget)
        self._entry_button_layout.setContentsMargins(0, 0, 0, 0)
        self._entry_button_layout.setSpacing(2)
        #
        self._value_add_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._value_add_button.hide()
        self._entry_button_layout.addWidget(self._value_add_button)
        self._value_add_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('file/file'))
        self._value_add_button._set_icon_frame_draw_size_(18, 18)
        #
        self._value_choose_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._entry_button_layout.addWidget(self._value_choose_button)
        self._value_choose_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('down'))
        self._value_choose_button._set_icon_frame_draw_size_(18, 18)
        self._value_choose_button._set_name_text_('choose value')
        self._value_choose_button._set_tool_tip_('"LMB-click" to popup choose view')
        self._value_choose_button.press_clicked.connect(self._execute_popup_choose_)
        #
        self._build_popup_choose_(self._value_entry, self)
        self._build_popup_completion_(self._value_entry, self)

    def _set_choose_popup_auto_resize_enable_(self, boolean):
        self._popup_choose_frame._set_popup_auto_resize_enable_(boolean)

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsPopupConstantChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._value_choose_button.setHidden(not boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_()

    def _set_value_entry_popup_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)

    def _set_value_validation_fnc_(self, fnc):
        self._value_entry._set_value_validation_fnc_(fnc)

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry._set_validator_use_as_storage_(boolean)

    def _set_value_entry_finished_connect_to_(self, fnc):
        self._value_entry.user_entry_finished.connect(fnc)

    def _set_value_entry_changed_connect_to_(self, fnc):
        self._value_entry.entry_changed.connect(fnc)

    def _set_choose_button_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_file_path_(file_path)

    def _set_choose_button_sub_icon_file_path_(self, file_path):
        self._value_choose_button._set_sub_icon_file_path_(file_path)

    def _get_value_choose_button_(self):
        return self._value_choose_button

    def _get_value_add_button_(self):
        return self._value_add_button

    def _set_value_entry_button_add_(self, widget):
        self._entry_button_layout.addWidget(widget)

    def _create_entry_icon_button_(self, name_text, icon_name=None, sub_icon_name=None, tool_tip=None):
        button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._entry_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(utl_gui_core.RscIconFile.get(icon_name))
        if sub_icon_name is not None:
            button._set_sub_icon_file_path_(utl_gui_core.RscIconFile.get(sub_icon_name))
        if tool_tip:
            button._set_tool_tip_(tool_tip)
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_value_index_visible_(self, boolean):
        pass

    def _set_choose_values_(self, values, *args, **kwargs):
        super(QtValueEntryAsPopupConstantChoose, self)._set_choose_values_(values, *args, **kwargs)
        #
        self._refresh_choose_index_()

    def _get_choose_current_values_(self):
        return [self._get_value_()]

    def _extend_choose_current_values_(self, values):
        self._set_value_(values[-1])
        #
        self._refresh_widget_()

    def _set_choose_value_by_index_(self, index):
        self._set_value_(
            self._get_choose_values_()[index]
        )

    def _set_choose_value_default_by_index_(self, index):
        self._set_value_default_(
            self._get_choose_value_at_(index)
        )

    def _set_choose_tag_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_tag_filter_enable_(boolean)

    def _set_choose_keyword_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_keyword_filter_enable_(boolean)

    def _set_choose_tag_filter_size_(self, w, h):
        pass

    def _set_choose_item_size_(self, w, h):
        self._popup_choose_frame._set_popup_item_size_(w, h)

    def _set_value_clear_(self):
        self._choose_values = []
        self._value_entry._set_value_clear_()


class QtValueEntryAsCapsule(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    #
    utl_gui_qt_abstract.AbsQtValueDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    value_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsCapsule, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.installEventFilter(self)
        #
        self._init_name_def_(self)
        self._set_frame_def_init_()

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._set_value_def_init_(self)
        self._set_value_default_def_init_()

        self._capsule_per_width = 0

        self._capsule_use_exclusive = True

        self._capsule_hovered_index = None
        self._capsule_pressed_index = None
        self._capsule_index_current = None

        self._capsule_value_current = None

        self._capsule_texts = []
        self._capsule_indices = []
        #
        self._capsule_draw_texts = []
        self._capsule_draw_rects = []
        #
        self._capsule_states = []

        self._capsule_height = 18

    def _set_capsule_strings_(self, texts):
        self._capsule_texts = texts
        c = len(texts)
        self._capsule_indices = range(c)
        self._capsule_draw_rects = []
        self._capsule_draw_texts = []
        self._capsule_states = []
        for i_index in self._capsule_indices:
            self._capsule_draw_rects.append(QtCore.QRect())
            # noinspection PyArgumentEqualDefault
            self._capsule_draw_texts.append(
                bsc_core.RawTextMtd.to_prettify(texts[i_index], capitalize=True)
            )
            self._capsule_states.append(False)
        #
        self._refresh_widget_draw_()

    def _set_value_(self, value):
        if self._capsule_use_exclusive:
            index = self._capsule_texts.index(value)
            self._capsule_index_current = index
            self._capsule_states = [True if i in [index] else False for i in self._capsule_indices]
        else:
            if value:
                indices = [self._capsule_texts.index(i) for i in value if i in self._capsule_texts]
                self._capsule_index_current = indices[0]
                self._capsule_states = [True if i in indices else False for i in self._capsule_indices]

        self._update_value_current_()
        #
        self._refresh_widget_draw_()

    def _get_value_(self):
        return self._capsule_value_current

    def _get_value_fnc_(self):
        _ = [self._capsule_texts[i] for i in self._capsule_indices if self._capsule_states[i] is True]
        if self._capsule_use_exclusive:
            if _:
                return _[0]
            return ''
        return _

    def _update_value_current_(self):
        value_pre = self._capsule_value_current
        self._capsule_value_current = self._get_value_fnc_()
        if value_pre != self._capsule_value_current:
            self.value_changed.emit()

    def _set_capsule_use_exclusive_(self, boolean):
        self._capsule_use_exclusive = boolean

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._set_frame_draw_rect_(
            x+1, y+1, w-2, h-2
        )
        #
        if self._capsule_texts:
            c_h = self._capsule_height
            w = int(max([self.fontMetrics().width(i) for i in self._capsule_texts]))
            self._capsule_per_width = w+(w % 2)+20
            for i, i_text in enumerate(self._capsule_texts):
                i_x, i_y = x+i*self._capsule_per_width, y
                i_w, i_h = self._capsule_per_width, h
                self._capsule_draw_rects[i].setRect(
                    x+i_x, y+(h-c_h)/2, i_w, c_h
                )

    def _execute_capsule_action_hover_move_(self, event):
        if not self._capsule_per_width:
            return
        p = event.pos()
        x, y = p.x(), p.y()
        self._capsule_hovered_index = int(x/self._capsule_per_width)
        self._refresh_widget_draw_()

    def _execute_capsule_action_press_start_(self, event):
        if not self._capsule_per_width:
            return
        p = event.pos()
        x, y = p.x(), p.y()
        index_pre = self._capsule_index_current
        index = int(x/self._capsule_per_width)
        if index in self._capsule_indices:
            self._capsule_index_current = index
            self._capsule_pressed_index = self._capsule_index_current
            if self._capsule_use_exclusive is True:
                if index_pre is not None:
                    self._capsule_states[index_pre] = False
                self._capsule_states[self._capsule_index_current] = True
            else:
                self._capsule_states[self._capsule_index_current] = not self._capsule_states[self._capsule_index_current]

            self._capsule_press_state = self._capsule_states[self._capsule_index_current]

            self._update_value_current_()

    def _execute_capsule_action_press_move_(self, event):
        if not self._capsule_per_width:
            return
        p = event.pos()
        x, y = p.x(), p.y()
        index_pre = self._capsule_index_current
        index = int(x/self._capsule_per_width)
        if index in self._capsule_indices:
            self._capsule_index_current = index
            self._capsule_pressed_index = self._capsule_index_current
            if index_pre != self._capsule_index_current:
                if self._capsule_use_exclusive is True:
                    if index_pre is not None:
                        self._capsule_states[index_pre] = False
                    self._capsule_states[self._capsule_index_current] = True
                else:
                    self._capsule_states[self._capsule_index_current] = self._capsule_press_state
                #
                self._update_value_current_()

    def _execute_capsule_action_press_end_(self, event):
        self._capsule_pressed_index = None

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._capsule_hovered_index = None
                self._refresh_widget_draw_()
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._execute_capsule_action_press_start_(event)
                    self._set_action_flag_(
                        self.ActionFlag.PressClick
                    )
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._execute_capsule_action_press_start_(event)
                    self._set_action_flag_(
                        self.ActionFlag.PressClick
                    )
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._get_action_flag_is_match_(self.ActionFlag.PressClick):
                    self._execute_capsule_action_press_move_(event)
                #
                self._execute_capsule_action_hover_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._execute_capsule_action_press_end_(event)
                self._clear_action_flag_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._capsule_texts:
            painter._draw_capsule_by_rects_(
                rects=self._capsule_draw_rects,
                texts=self._capsule_draw_texts,
                states=self._capsule_states,
                hovered_index=self._capsule_hovered_index,
                pressed_index=self._capsule_pressed_index,
                use_exclusive=self._capsule_use_exclusive
            )


class QtValueEntryAsTuple(
    _utl_gui_qt_wgt_entry.QtEntryFrame,
    utl_gui_qt_abstract.AbsQtValueEntryAsTupleDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtConstantEntry
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsTuple, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_as_tuple_def_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(8)
        #
        self._build_entry_(2, self._value_type)

    def _build_entry_(self, value_size, value_type):
        self._value_type = value_type
        #
        if self._value_entries:
            set_qt_layout_clear(self._value_entry_layout)
        #
        self._value_entries = []
        #
        self._set_entry_count_(value_size)
        if value_size:
            for i in range(value_size):
                i_widget = _utl_gui_qt_wgt_entry.QtConstantEntry()
                i_widget._set_value_type_(self._value_type)
                self._value_entry_layout.addWidget(i_widget)
                self._value_entries.append(i_widget)

    def _set_value_entry_enable_(self, boolean):
        pass


class QtValueEntryAsArray(
    _utl_gui_qt_wgt_entry.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryBaseDef,
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtChooseAsPopupDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtListEntry
    #
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForChoose
    #
    add_press_clicked = qt_signal()
    def _execute_popup_choose_(self):
        self._popup_choose_frame._execute_popup_start_()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsArray, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_name_def_(self)
        self._init_value_entry_base_def_(self)
        self._set_choose_def_init_()
        self._init_choose_as_popup_def_(self)
        #
        self._build_entry_(str)
        self._set_choose_multiply_enable_(True)

    def _build_entry_(self, value_type):
        self._value_type = value_type

        self._main_layout = QtVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        #
        entry_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._main_layout.addWidget(entry_widget)
        #
        self._value_entry_layout = QtHBoxLayout(entry_widget)
        self._value_entry_layout.setContentsMargins(2, 2, 2, 2)
        self._value_entry_layout.setSpacing(0)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_entry_frame_(self)
        #
        button_widget = _utl_gui_qt_wgt_utility.QtLineWidget()
        button_widget._set_line_styles_(
            [button_widget.Style.Null, button_widget.Style.Null, button_widget.Style.Solid, button_widget.Style.Null]
        )
        self._value_entry_layout.addWidget(button_widget)
        self._entry_button_layout = QtVBoxLayout(button_widget)
        self._entry_button_layout._set_align_top_()
        self._entry_button_layout.setContentsMargins(2, 0, 0, 0)
        self._entry_button_layout.setSpacing(2)

        self._value_choose_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._entry_button_layout.addWidget(self._value_choose_button)
        self._value_choose_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('file/file'))
        self._value_choose_button._set_sub_icon_file_path_(utl_gui_core.RscIconFile.get('down'))
        self._value_choose_button._set_icon_frame_draw_size_(18, 18)
        self._value_choose_button._set_name_text_('choose value')
        self._value_choose_button._set_tool_tip_('"LMB-click" to popup choose view')
        self._value_choose_button.press_clicked.connect(self._execute_popup_choose_)
        #
        self._build_popup_choose_(self._value_entry, self)

        self._resize_handle.raise_()

    def _get_value_entry_gui_(self):
        return self._value_entry

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsArray, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_value_entry_popup_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)

    def _set_value_entry_choose_enable_(self, boolean):
        self._value_choose_button._set_action_enable_(boolean)

    def _set_value_entry_choose_visible_(self, boolean):
        self._value_choose_button._set_visible_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _set_value_append_(self, value):
        self._value_entry._set_value_append_(value)

    def _set_value_extend_(self, values):
        self._value_entry._set_value_extend_(values)

    def _set_values_(self, values):
        self._value_entry._set_values_(values)

    def _get_values_(self):
        return self._value_entry._get_values_()

    def _set_values_clear_(self):
        self._value_entry._set_values_clear_()

    def _set_entry_item_icon_file_path_(self, file_path):
        self._value_entry._set_entry_item_icon_file_path_(file_path)

    def _set_value_entry_button_add_(self, widget):
        self._entry_button_layout.addWidget(widget)

    def _create_entry_icon_button_(self, name_text, icon_name=None, sub_icon_name=None):
        button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._entry_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(utl_gui_core.RscIconFile.get(icon_name))
        if sub_icon_name is not None:
            button._set_sub_icon_file_path_(utl_gui_core.RscIconFile.get(sub_icon_name))
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry._set_validator_use_as_storage_(boolean)

    def _set_choose_button_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_file_path_(file_path)

    def _get_popup_choose_gui_(self):
        return self._popup_choose_frame
    # choose
    def _extend_choose_current_values_(self, values):
        self._set_value_extend_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()

    def _set_choose_tag_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_tag_filter_enable_(boolean)

    def _set_choose_keyword_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_keyword_filter_enable_(boolean)

    def _set_choose_item_size_(self, w, h):
        self._popup_choose_frame._set_popup_item_size_(w, h)

    def _set_choose_multiply_enable_(self, boolean):
        super(QtValueEntryAsArray, self)._set_choose_multiply_enable_(boolean)
        self._popup_choose_frame._set_popup_multiply_enable_(boolean)


class QtValueEntryAsArrayChoose(
    _utl_gui_qt_wgt_entry.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryBaseDef,
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtChooseAsPopupDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtListEntry
    #
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForChoose
    #
    add_press_clicked = qt_signal()
    def _execute_popup_choose_(self):
        self._popup_choose_frame._execute_popup_start_()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsArrayChoose, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_name_def_(self)
        self._init_value_entry_base_def_(self)
        self._set_choose_def_init_()
        self._init_choose_as_popup_def_(self)
        #
        self._build_entry_(str)
        self._set_choose_multiply_enable_(True)

    def _build_entry_(self, value_type):
        self._value_type = value_type

        self._main_layout = QtVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        entry_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._main_layout.addWidget(entry_widget)
        #
        self._value_entry_layout = QtHBoxLayout(entry_widget)
        self._value_entry_layout.setContentsMargins(2, 2, 2, 2)
        self._value_entry_layout.setSpacing(0)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_entry_frame_(self)
        #
        button_widget = _utl_gui_qt_wgt_utility.QtLineWidget()
        button_widget._set_line_styles_(
            [button_widget.Style.Null, button_widget.Style.Null, button_widget.Style.Solid, button_widget.Style.Null]
        )
        self._value_entry_layout.addWidget(button_widget)
        self._entry_button_layout = QtVBoxLayout(button_widget)
        self._entry_button_layout._set_align_top_()
        self._entry_button_layout.setContentsMargins(2, 0, 0, 0)
        self._entry_button_layout.setSpacing(2)

        self._value_choose_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._entry_button_layout.addWidget(self._value_choose_button)
        self._value_choose_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('file/file'))
        self._value_choose_button._set_sub_icon_file_path_(utl_gui_core.RscIconFile.get('down'))
        self._value_choose_button._set_icon_frame_draw_size_(18, 18)
        self._value_choose_button._set_name_text_('choose value')
        self._value_choose_button._set_tool_tip_('"LMB-click" to popup choose view')
        self._value_choose_button.press_clicked.connect(self._execute_popup_choose_)
        #
        self._build_popup_choose_(self._value_entry, self)
        #
        self._resize_handle.raise_()

    def _get_value_entry_gui_(self):
        return self._value_entry

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsArrayChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_value_entry_popup_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)

    def _set_value_entry_choose_enable_(self, boolean):
        self._value_choose_button._set_action_enable_(boolean)

    def _set_value_entry_choose_visible_(self, boolean):
        self._value_choose_button._set_visible_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _set_value_append_(self, value):
        self._value_entry._set_value_append_(value)

    def _set_value_extend_(self, values):
        self._value_entry._set_value_extend_(values)

    def _set_values_(self, values):
        self._value_entry._set_values_(values)

    def _get_values_(self):
        return self._value_entry._get_values_()

    def _set_values_clear_(self):
        self._value_entry._set_values_clear_()

    def _set_entry_item_icon_file_path_(self, file_path):
        self._value_entry._set_entry_item_icon_file_path_(file_path)

    def _set_value_entry_button_add_(self, widget):
        self._entry_button_layout.addWidget(widget)

    def _create_entry_icon_button_(self, name_text, icon_name=None, sub_icon_name=None):
        button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._entry_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(utl_gui_core.RscIconFile.get(icon_name))
        if sub_icon_name is not None:
            button._set_sub_icon_file_path_(utl_gui_core.RscIconFile.get(sub_icon_name))
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry._set_validator_use_as_storage_(boolean)

    def _set_choose_button_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_file_path_(file_path)

    def _get_popup_choose_gui_(self):
        return self._popup_choose_frame
    # choose
    def _extend_choose_current_values_(self, values):
        self._set_value_extend_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()

    def _set_choose_tag_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_tag_filter_enable_(boolean)

    def _set_choose_keyword_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_keyword_filter_enable_(boolean)

    def _set_choose_item_size_(self, w, h):
        self._popup_choose_frame._set_popup_item_size_(w, h)

    def _set_choose_multiply_enable_(self, boolean):
        super(QtValueEntryAsArrayChoose, self)._set_choose_multiply_enable_(boolean)
        self._popup_choose_frame._set_popup_multiply_enable_(boolean)


class _QtHExpandItem0(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForExpandDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtHExpandItem0, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self._set_frame_def_init_()
        self._init_name_def_(self)
        self._name_draw_font = Font.GROUP
        #
        self._init_icon_def_(self)
        self._icon_name_is_enable = True
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expanded = False
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('expandopen')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('expandclose')

        self._expand_sub_icon_file_path_0 = None
        self._expand_sub_icon_file_path_1 = None

        self._action_is_hovered = False
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

        self._icon_file_draw_percent = .65

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        #
        self._set_frame_draw_rect_(
            c_x+1, c_y+1, w-2, h-2
        )
        frm_w = frm_h = h
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_frm_m_w, icn_frm_m_h = (frm_w-icn_frm_w)/2, (frm_h-icn_frm_h)/2
        icn_w, icn_h = icn_frm_w*self._icon_file_draw_percent, icn_frm_h*self._icon_file_draw_percent

        if self._sub_icon_file_path is not None:
            frm_x, frm_y = c_x+(frm_w-icn_frm_w)/2, c_y+(frm_h-icn_frm_h)/2
            sub_icn_w, sub_icn_h = icn_frm_w*self._sub_icon_file_draw_percent, icn_frm_h*self._sub_icon_file_draw_percent
            self._set_icon_file_draw_rect_(
                 c_x+icn_frm_m_w, c_y+icn_frm_m_h, icn_w, icn_h
            )
            self._set_sub_icon_file_draw_rect_(
                frm_x+frm_w-sub_icn_w-icn_frm_m_w, frm_y+frm_h-sub_icn_h-icn_frm_m_h, sub_icn_w, sub_icn_h
            )
        else:
            self._set_icon_file_draw_rect_(
                c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
            )
        #
        c_x += icn_frm_w+spacing
        # if self._icon_name_is_enable is True:
        #     if self._icon_name_text is not None:
        #         icn_w, icn_h = self._icon_name_draw_size
        #         self._set_icon_name_draw_rect_(
        #             c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
        #         )
        #         c_x += icn_frm_w+spacing
        #
        self._set_name_draw_rect_(
            c_x, c_y, w-c_x, frm_h
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
            self._set_action_hover_filter_execute_(event)
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
                self._clear_action_flag_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        background_color = self._frame_background_color
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            # border_radius=1,
            offset=offset
        )
        # name-icon
        if self._icon_name_is_enable is True:
            if self._icon_name_text is not None:
                painter._draw_frame_color_with_name_text_by_rect_(
                    rect=self._frame_draw_rect,
                    text=self._icon_name_text,
                    offset=offset,
                )
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_file_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._action_is_hovered
        )
        # text
        if self._name_text is not None:
            color = self._name_color
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=self._name_draw_font,
                font_color=color,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )

    def set_expanded(self, boolean):
        self._is_expanded = boolean

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
        )
        self._set_sub_icon_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._is_expanded]
        )
        #
        self._refresh_widget_draw_()


class _QtHExpandItem1(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForExpandDef,
):
    toggled = qt_signal(bool)
    def __init__(self, *args, **kwargs):
        super(_QtHExpandItem1, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self._set_frame_def_init_()
        self._init_name_def_(self)
        self._init_icon_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expand_enable = True
        self._is_expanded = False
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
        self._expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-up')
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        #
        self._refresh_expand_()
        # font
        self.setFont(Font.NAME)

    def _refresh_widget_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=self._frame_background_color,
            # border_radius=self._frame_border_radius,
            offset=offset
        )
        # icon
        painter._draw_icon_file_by_rect_(
            rect=self._icon_file_draw_rect,
            file_path=self._icon_file_path,
            offset=offset,
            is_hovered=self._action_is_hovered
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_action_hover_filter_execute_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.ExpandClick)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.ExpandClick:
                        self._execute_action_expand_()
                #
                self._clear_action_flag_()
        return False

    def _refresh_expand_(self):
        if self._is_expanded is True:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
            )
        else:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            )
        #
        if self._expand_direction == self.EXPAND_TOP_TO_BOTTOM:
            self._set_icon_file_path_(
                [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
            )
        elif self._expand_direction == self.EXPAND_BOTTOM_TO_TOP:
            self._set_icon_file_path_(
                [self._expand_icon_file_path_1, self._expand_icon_file_path_2][self._is_expanded]
            )
        #
        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._set_frame_draw_rect_(
            x+1, y+1, w-2, h-2
        )
        #
        icn_frm_w, icn_frm_h = 12, 12
        i_w, i_h = 8, 8
        #
        if self._expand_direction == self.EXPAND_TOP_TO_BOTTOM:
            self._set_icon_file_draw_rect_(
                x+(icn_frm_w-i_w)/2, y+(icn_frm_h-i_h)/2,
                i_w, i_h
            )
        elif self._expand_direction == self.EXPAND_BOTTOM_TO_TOP:
            self._set_icon_file_draw_rect_(
                x+(icn_frm_w-i_w)/2, y+h-icn_frm_h+(icn_frm_h-i_h)/2,
                i_w, i_h
            )


class _QtVExpandItem1(
    _QtHExpandItem1
):
    def __init__(self, *args, **kwargs):
        super(_QtVExpandItem1, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-left')


class _QtHExpandItem2(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForExpandDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtHExpandItem2, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        #
        self._name_draw_font = Font.GROUP
        #
        self._init_icon_def_(self)
        self._icon_name_is_enable = True
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expanded = False
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('bar-open')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('bar-close')

        self._expand_sub_icon_file_path_0 = None
        self._expand_sub_icon_file_path_1 = None

        self._action_is_hovered = False
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
        self._icon_file_draw_percent = 1

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        #
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_w, icn_h = icn_frm_w, icn_frm_h
        self._set_icon_file_draw_rect_(
            c_x+(icn_frm_w-icn_w)/2, c_y+(icn_frm_h-icn_h)/2, icn_w, icn_h
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
            self._set_action_hover_filter_execute_(event)
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
                self._clear_action_flag_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_file_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._action_is_hovered
        )

    def set_expanded(self, boolean):
        self._is_expanded = boolean

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
        )
        self._set_sub_icon_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._is_expanded]
        )
        #
        self._refresh_widget_draw_()


class _QtHContractItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForExpandDef,
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
        self._init_icon_def_(self)
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

        self._action_is_hovered = False
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
        self._icon_file_draw_percent = 1
        self._icon_file_draw_size = 10, 20

    def _set_expand_direction_(self, direction):
        if direction == self.ContractDirection.RightToLeft:
            self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('contract_v_l')
            self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('contract_v_r')
        elif direction == self.ContractDirection.LeftToRight:
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
        icn_w, icn_h = self._icon_file_draw_size
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
            self._set_action_hover_filter_execute_(event)
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
                self._clear_action_flag_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_file_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._action_is_hovered
        )

    def set_expanded(self, boolean):
        self._is_expanded = boolean

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
        )
        self._set_sub_icon_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._is_expanded]
        )
        #
        self._set_action_hovered_(False)
        self._refresh_widget_draw_()


class _QtWindowHead(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtWindowHead, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
        #
        self._set_frame_def_init_()
        #
        self._frame_background_color = 71, 71, 71, 255
        self._frame_border_color = 95, 95, 95, 255
        #
        self._close_button = _utl_gui_qt_wgt_utility.QtIconPressItem(self)
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
