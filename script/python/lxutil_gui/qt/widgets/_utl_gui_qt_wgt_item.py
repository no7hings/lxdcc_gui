# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

from lxutil_gui.qt import utl_gui_qt_abstract

from lxutil_gui.qt import utl_gui_qt_core


class _QtTextItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtNameDef,
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
):
    def _set_widget_update_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtTextItem, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(Font.NAME)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_name_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        self._name_rect.setRect(
            x, y, w, h
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_item_event_filter_(event)
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        self._set_widget_geometry_update_()
        # name
        if self._name_text is not None:
            text_color = [Color.TEXT_NORMAL, Color.TEXT_HOVERED][self._item_is_hovered]
            #
            painter._set_text_draw_by_rect_(
                self._name_rect,
                self._name_text,
                text_color,
                font=Font.NAME,
                text_option=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            )


class _QtIconPressItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtIconDef,
    utl_gui_qt_abstract._QtNameDef,
    utl_gui_qt_abstract._QtMenuDef,
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
):
    clicked = qt_signal()
    db_clicked = qt_signal()
    #
    QT_MENU_CLASS = _utl_gui_qt_wgt_utility.QtMenu
    def __init__(self, *args, **kwargs):
        super(_QtIconPressItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(Font.NAME)
        self.setMaximumSize(20, 20)
        self.setMinimumSize(20, 20)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_name_def_init_()
        self._set_icon_def_init_()
        self._set_menu_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_item_event_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_item_action_flag_(self.PRESS_CLICK_FLAG)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._item_is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self.db_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_item_is_click_flag_() is True:
                        self.clicked.emit()
                        self.press_clicked.emit()
                        self._set_menu_show_()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._set_item_action_flag_clear_()
                #
                self._item_is_hovered = False
                self.update()
        return False

    def paintEvent(self, event):
        w, h = self.width(), self.height()
        i_w, i_h = self._file_icon_size
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        self._set_widget_geometry_update_()
        #
        f_x, f_y = (w-i_w) / 2, (h-i_h) / 2
        offset = [0, 2][self._get_item_action_flag_() is not None]
        #
        bkg_color = [Color.TRANSPARENT, Color.ITEM_BACKGROUND_HOVER][self._item_is_hovered]
        painter._set_frame_draw_by_rect_(
            self._icon_frame_rect,
            border_color=bkg_color,
            background_color=bkg_color,
            border_radius=4,
            offset=offset
        )
        # icon
        if self._icon_enable is True:
            if self._file_icon_path is not None:
                painter._set_svg_image_draw_by_rect_(
                    self._file_icon_rect, self._file_icon_path, offset=offset
                )
            elif self._color_icon_rgb is not None:
                painter._set_color_icon_draw_(
                    self._color_icon_rect, self._color_icon_rgb, offset=offset
                )
            elif self._name_icon_text is not None:
                painter._set_name_icon_draw_by_rect_(
                    self._name_icon_rect, self._name_icon_text, offset=offset, border_radius=2,
                    is_hovered=self._item_is_hovered
                )

    def _set_widget_update_(self):
        # noinspection PyUnresolvedReferences
        self.update()

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        f_w, f_h = self._icon_frame_size
        #
        i_f_w, i_f_h = self._file_icon_size
        i_c_w, i_c_h = self._color_icon_size
        i_n_w, i_n_h = self._name_icon_size
        # check
        _w, _h = w, h
        _x, _y = x, y
        if self._icon_enable is True:
            _x, _y = _x + (w - f_w) / 2, _y + (h - f_h) / 2
            self._icon_frame_rect.setRect(
                _x, _y, f_w, f_h
            )
            self._file_icon_rect.setRect(
                _x + (f_w - i_f_w) / 2, _y + (f_h - i_f_h) / 2, i_f_w, i_f_h
            )
            self._color_icon_rect.setRect(
                _x + (f_w - i_c_w) / 2, _y + (f_h - i_c_h) / 2, i_c_w, i_c_h
            )
            self._name_icon_rect.setRect(
                _x + (f_w - i_n_w) / 2, _y + (f_h - i_n_h) / 2, i_n_w, i_n_h
            )
            _x += f_h
            _w -= f_w


class _QtPressItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtStatusDef,
    utl_gui_qt_abstract._QtStatusesDef,
    #
    utl_gui_qt_abstract._QtIconDef,
    utl_gui_qt_abstract._QtMenuDef,
    utl_gui_qt_abstract._QtNameDef,
    utl_gui_qt_abstract._QtProgressDef,
    #
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
    utl_gui_qt_abstract._QtItemCheckActionDef,
    utl_gui_qt_abstract._QtItemOptionPressActionDef,
):
    clicked = qt_signal()
    checked = qt_signal()
    toggled = qt_signal(bool)
    option_clicked = qt_signal()
    #
    QT_MENU_CLASS = _utl_gui_qt_wgt_utility.QtMenu
    def __init__(self, *args, **kwargs):
        super(_QtPressItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = QtDccMtd.get_qt_palette()
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
        self._set_statuses_def_init_()
        #
        self._set_icon_def_init_()
        self._set_name_def_init_()
        self._set_menu_def_init_()
        self._set_progress_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()
        self._set_item_check_action_def_init_()
        self._set_item_option_press_action_def_init_()
        #
        self._set_item_check_update_()
        #
        r, g, b = 143, 143, 143
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hover_frame_border_color = hover_color
        #
        r, g, b = 127, 127, 127
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hover_frame_background_color = hover_color

    def _set_widget_update_(self):
        self.update()

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        check_enable = self._get_item_is_check_enable_()
        option_click_enable = self._get_item_option_click_enable_()
        status_enable = self._get_is_status_enable_()
        element_status_enable = self._get_is_statuses_enable_()
        progress_enable = self._get_is_progress_enable_()
        #
        f_w, f_h = self._icon_frame_size
        #
        i_f_w, i_f_h = self._file_icon_size
        i_c_w, i_c_h = self._color_icon_size
        i_n_w, i_n_h = self._name_icon_size
        #
        _w, _h = w, h
        _x, _y = x, y
        #
        c_x, c_y = x, y
        c_w, c_h = w, h
        if check_enable is True:
            self._item_check_frame_rect.setRect(
                _x, _y, f_w, f_h
            )
            self._item_check_icon_rect.setRect(
                _x + (f_w - i_f_w) / 2, _y + (f_h - i_f_h) / 2, i_f_w, i_f_h
            )
            _x += f_h
            _w -= f_w
            c_x += f_h
            c_w -= f_w
        #
        if self._icon_enable is True:
            self._file_icon_rect.setRect(
                _x + (f_w - i_f_w) / 2, _y + (f_h - i_f_h) / 2, i_f_w, i_f_h
            )
            self._color_icon_rect.setRect(
                _x + (f_w - i_c_w) / 2, _y + (f_h - i_c_h) / 2, i_c_w, i_c_h
            )
            self._name_icon_rect.setRect(
                _x + (f_w - i_n_w) / 2, _y + (f_h - i_n_h) / 2, i_n_w, i_n_h
            )
            _x += f_h
            _w -= f_w
        # option
        if option_click_enable is True:
            self._option_click_rect.setRect(
                w - f_w, y, f_w, f_h
            )
            self._option_click_icon_rect.setRect(
                (w - f_w) + (f_w - i_f_w) / 2, y + (f_h - i_f_h) / 2, i_f_w, i_f_h
            )
            _w -= f_w
            c_w -= f_w
        #
        self._frame_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._status_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._name_rect.setRect(
            _x, _y, _w, _h
        )
        # progress
        if progress_enable is True:
            progress_percent = self._get_progress_percent_()
            self._progress_rect.setRect(
                c_x, c_y, c_w*progress_percent, 4
            )
        #
        if status_enable is True:
            self._status_rect.setRect(
                c_x, c_y, c_w, c_h
            )
        #
        e_h = 4
        if element_status_enable is True:
            self._element_status_rect.setRect(
                c_x, c_h-e_h, c_w, e_h
            )

    def setText(self, text):
        self._name_text = text

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            # update rect first
            enable = self._get_item_is_enable_()
            check_enable = self._get_item_is_check_enable_()
            click_enable = self._get_item_is_press_enable_()
            option_click_enable = self._get_item_option_click_enable_()
            if event.type() == QtCore.QEvent.Resize:
                pass
            #
            if enable is True:
                if event.type() == QtCore.QEvent.Enter:
                    self._item_is_hovered = True
                    self.update()
                elif event.type() == QtCore.QEvent.Leave:
                    self._item_is_hovered = False
                    self.update()
                # press
                elif event.type() in [QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick]:
                    self._action_flag = None
                    #
                    flag_raw = [
                        (check_enable, self._item_check_frame_rect, gui_configure.ActionFlag.CHECK_CLICK),
                        (click_enable, self._frame_rect, gui_configure.ActionFlag.PRESS_CLICK),
                        (option_click_enable, self._option_click_rect, gui_configure.ActionFlag.OPTION_CLICK),
                    ]
                    if event.button() == QtCore.Qt.LeftButton:
                        pos = event.pos()
                        for enable, rect, flag in flag_raw:
                            if enable is True:
                                if rect.contains(pos) is True:
                                    self._action_flag = flag
                                    break
                    elif event.button() == QtCore.Qt.RightButton:
                        self._set_menu_show_()
                    #
                    self._item_is_hovered = True
                    self.update()
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if self._action_flag == gui_configure.ActionFlag.CHECK_CLICK:
                        self._set_item_check_swap_()
                        self.checked.emit()
                    elif self._action_flag == gui_configure.ActionFlag.PRESS_CLICK:
                        self.clicked.emit()
                    elif self._action_flag == gui_configure.ActionFlag.OPTION_CLICK:
                        self.option_clicked.emit()
                    #
                    self._action_flag = None
                    self.update()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        self._set_widget_geometry_update_()
        #
        offset = self._get_item_action_offset_()
        #
        if self._item_is_enable is True:
            border_color = [self._frame_border_color, self._hover_frame_border_color][self._item_is_hovered]
            background_color = [self._frame_background_color, self._hover_frame_background_color][self._item_is_hovered]
        else:
            border_color = Color.BUTTON_BORDER_DISABLE
            background_color = Color.BUTTON_BACKGROUND_DISABLE
        #
        painter._set_frame_draw_by_rect_(
            self._frame_rect,
            border_color=border_color,
            background_color=background_color,
            border_radius=4,
            offset=offset
        )
        #
        if self._get_is_status_enable_() is True:
            status_color = [self._status_color, self._hover_status_color][self._item_is_hovered]
            painter._set_status_draw_by_rect_(
                self._status_rect,
                color=status_color,
                border_radius=4,
                offset=offset
            )
        #
        if self._get_is_statuses_enable_() is True:
            status_colors = [self._element_status_colors, self._hover_element_status_colors][self._item_is_hovered]
            painter._set_elements_status_draw_by_rect_(
                self._element_status_rect,
                colors=status_colors,
                offset=offset,
                border_radius=2,
            )
        #
        if self._get_is_progress_enable_() is True:
            painter._set_frame_draw_by_rect_(
                self._progress_rect,
                border_color=Color.TRANSPARENT,
                background_color=Color.PROGRESS,
                border_radius=2,
                offset=offset
            )
        # check
        if self._get_item_is_check_enable_() is True:
            painter._set_svg_image_draw_by_rect_(
                self._item_check_icon_rect,
                self._item_check_icon_file_path,
                offset=offset
            )
        # icon
        if self._icon_enable is True:
            if self._file_icon_path is not None:
                painter._set_svg_image_draw_by_rect_(
                    self._file_icon_rect, self._file_icon_path, offset=offset
                )
            elif self._color_icon_rgb is not None:
                painter._set_color_icon_draw_(
                    self._color_icon_rect, self._color_icon_rgb, offset=offset
                )
            elif self._name_icon_text is not None:
                painter._set_name_icon_draw_by_rect_(
                    self._name_icon_rect,
                    self._name_icon_text,
                    offset=offset,
                    border_radius=2,
                    is_hovered=self._item_is_hovered
                )
        # name
        if self._name_text is not None:
            if self._item_is_enable is True:
                text_color = [Color.TEXT_NORMAL, Color.TEXT_HOVERED][self._item_is_hovered]
            else:
                text_color = Color.TEXT_DISABLE
            #
            painter._set_text_draw_by_rect_(
                self._name_rect, self._name_text, text_color, font=Font.NAME, offset=offset
            )
        # option
        if self._get_item_option_click_enable_() is True:
            painter._set_svg_image_draw_by_rect_(self._option_click_icon_rect, self._option_icon_file_path, offset=offset)


class _QtCheckItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtIconDef,
    utl_gui_qt_abstract._QtNameDef,
    #
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemCheckActionDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtCheckItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = QtDccMtd.get_qt_palette()
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
        self._set_icon_def_init_()
        self._set_name_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_check_action_def_init_()
        #
        self._set_item_check_update_()

    def _set_widget_update_(self):
        self.update()

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        f_w, f_h = self._icon_frame_size
        i_w, i_h = self._file_icon_size
        #
        self._set_frame_rect_(
            x, y, w-1, h-1
        )
        #
        self._set_item_check_frame_rect_(
            x, y, f_w, f_h
        )
        self._set_item_check_icon_rect_(
            x + (f_w - i_w) / 2, y + (f_h - i_h) / 2, i_w, i_h
        )
        x += f_w+spacing
        self._set_name_rect_(
            x, y, w-x, h
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_item_event_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_item_action_flag_(self.CHECK_CLICK_FLAG)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_item_action_flag_() == self.CHECK_CLICK_FLAG:
                        self._set_item_check_action_run_()
                        #
                        self._set_item_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_widget_geometry_update_()
        #
        offset = self._get_item_action_offset_()
        #
        bkg_color = [Color.TRANSPARENT, Color.ITEM_BACKGROUND_HOVER][self._item_is_hovered]
        painter._set_frame_draw_by_rect_(
            self._item_check_frame_rect,
            border_color=bkg_color,
            background_color=bkg_color,
            border_radius=4,
            offset=offset
        )
        #
        if self._item_check_icon_file_path is not None:
            painter._set_file_icon_draw_by_rect_(
                rect=self._item_check_icon_rect,
                file_path=self._item_check_icon_file_path,
                offset=offset
            )
        if self._name_text is not None:
            painter._set_text_draw_by_rect_(
                self._name_rect,
                self._name_text,
                font=Font.NAME,
                color=Color.TEXT_NORMAL,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )


class _QtFilterBar(QtWidgets.QWidget):
    BTN_FRAME_SIZE = 18, 18
    BTN_ICON_SIZE = 16, 16
    #
    entry_changed = qt_signal()
    preOccurrenceClicked = qt_signal()
    nextOccurrenceClicked = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtFilterBar, self).__init__(*args, **kwargs)
        qt_layout_0 = QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        self._result_label = _utl_gui_qt_wgt_utility.QtLabel()
        qt_layout_0.addWidget(self._result_label)
        self._result_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        self._qt_entry_frame_0 = _QtEntryFrame()
        self._qt_entry_frame_0.setMaximumWidth(240)
        qt_layout_0.addWidget(self._qt_entry_frame_0)
        qt_layout_1 = QtHBoxLayout(self._qt_entry_frame_0)
        qt_layout_1.setContentsMargins(*[0]*4)
        qt_layout_1.setSpacing(2)
        #
        self._header_button = _QtIconPressItem()
        qt_layout_1.addWidget(self._header_button)
        self._header_button._set_file_icon_path_(
            utl_core.Icon.get(
                'search'
            )
        )
        #
        self._header_button._set_menu_raw_(
            [
                ('Option(s)', None, None),
                (),
                ('History(s)', None, None)
            ]
        )
        #
        self._qt_entry_0 = _QtEntryItem()
        qt_layout_1.addWidget(self._qt_entry_0)
        self._qt_entry_frame_0.setFocusProxy(self._qt_entry_0)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self._qt_entry_0.textChanged.connect(self._set_enter_changed_emit_send_)
        #
        self._entry_clear_button = _QtIconPressItem()
        qt_layout_1.addWidget(self._entry_clear_button)
        self._entry_clear_button.hide()
        self._entry_clear_button._set_file_icon_path_(
            utl_core.Icon.get(
                'entry_clear'
            )
        )
        self._entry_clear_button.clicked.connect(self._set_entry_clear_)
        #
        self._match_case_button = _QtIconPressItem()
        self._match_case_button.hide()
        qt_layout_0.addWidget(self._match_case_button)
        self._match_case_button.setFocusProxy(self._qt_entry_0)
        self._match_case_button.clicked.connect(self._set_match_case_swap_)
        self._match_case_icon_names = 'match_case_off', 'match_case_on'
        self._is_match_case = False
        #
        self._match_word_button = _QtIconPressItem()
        self._match_word_button.hide()
        qt_layout_0.addWidget(self._match_word_button)
        self._match_word_button.setFocusProxy(self._qt_entry_0)
        self._match_word_button.clicked.connect(self._set_match_word_swap_)
        self._match_word_icon_names = 'match_word_off', 'match_word_on'
        self._is_match_word = False
        #
        self._pre_occurrence_button = _QtIconPressItem()
        qt_layout_0.addWidget(self._pre_occurrence_button)
        self._pre_occurrence_button._set_file_icon_path_(
            utl_core.Icon.get(
                'pre_occurrence'
            )
        )
        self._pre_occurrence_button.clicked.connect(self._set_pre_occurrence_emit_send_)
        #
        self._next_occurrence_button = _QtIconPressItem()
        qt_layout_0.addWidget(self._next_occurrence_button)
        self._next_occurrence_button._set_file_icon_path_(
            utl_core.Icon.get(
                'next_occurrence'
            )
        )
        self._next_occurrence_button.clicked.connect(self._set_next_occurrence_emit_send_)
        #
        self._result_count = None
        self._result_index = None
        #
        self._set_update_()
    #
    def _set_update_(self):
        self._match_case_button._set_file_icon_path_(
            utl_core.Icon.get(self._match_case_icon_names[self._is_match_case])
        )
        #
        self._match_word_button._set_file_icon_path_(
            utl_core.Icon.get(self._match_word_icon_names[self._is_match_word])
        )
        #
        self._qt_entry_0.setPlaceholderText(
            ' and '.join([i for i in [[None, 'Match-case'][self._is_match_case], [None, 'Match-word'][self._is_match_word]] if i])
        )

    def _set_match_case_swap_(self):
        self._is_match_case = not self._is_match_case
        self._set_update_()
        self._set_enter_changed_emit_send_()

    def _set_match_word_swap_(self):
        self._is_match_word = not self._is_match_word
        self._set_update_()
        self._set_enter_changed_emit_send_()

    def _get_qt_entry_(self):
        return self._qt_entry_0

    def _set_entry_clear_(self):
        self._qt_entry_0.clear()
        self._set_enter_changed_emit_send_()

    def _get_is_match_case_(self):
        return self._is_match_case

    def _get_is_match_word_(self):
        return self._is_match_word

    def _set_enter_changed_emit_send_(self):
        # noinspection PyUnresolvedReferences
        self.entry_changed.emit()
        self._set_entry_clear_button_visible_update_()

    def _set_entry_clear_button_visible_update_(self):
        self._entry_clear_button.setVisible(
            not not self._qt_entry_0.text()
        )

    def _set_pre_occurrence_emit_send_(self):
        # noinspection PyUnresolvedReferences
        self.preOccurrenceClicked.emit()

    def _set_next_occurrence_emit_send_(self):
        # noinspection PyUnresolvedReferences
        self.nextOccurrenceClicked.emit()

    def _set_result_count_(self, value):
        self._result_count = value
        self._result_index = None
        self._set_result_update_()

    def _set_result_index_(self, value):
        self._result_index = value
        self._set_result_update_()

    def _set_result_update_(self):
        if self._result_count is not None:
            if self._result_index is not None:
                self._result_label.setText('{} / {}'.format(self._result_index+1, self._result_count))
            else:
                self._result_label.setText('{} results'.format(self._result_count))
        else:
            self._result_label.setText('')

    def _set_result_clear_(self):
        self._result_count = None
        self._result_index = None
        self._set_result_update_()

    def _set_entry_focus_(self, boolean):
        if boolean is True:
            self._qt_entry_0.setFocus(QtCore.Qt.MouseFocusReason)
        else:
            self._qt_entry_0.clearFocus()


class _QtEntryFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtStatusDef,
):
    def _set_widget_update_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtEntryFrame, self).__init__(*args, **kwargs)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._item_is_hovered = False
        self._is_focused = False
        self._entry_count = 1
        #
        self._set_status_def_init_()

    def paintEvent(self, event):
        pos_x, pos_y = 0, 0
        width, height = self.width(), self.height()
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        size = self._entry_count
        spacing = 2
        #
        d = width/size
        if size == 1:
            i_rect = QtCore.QRect(
                pos_x, pos_y, width, height
            )
            bkg_color = [Color.ENTRY_BACKGROUND_ENTRY_OFF, Color.ENTRY_BACKGROUND_ENTRY_ON][self._is_focused]
            bdr_color = [Color.ENTRY_BORDER_ENTRY_OFF, Color.ENTRY_BORDER_ENTRY_ON][self._is_focused]
            painter._set_frame_draw_by_rect_(
                i_rect,
                border_color=bdr_color,
                background_color=bkg_color,
                border_radius=4
            )
        elif size > 1:
            for i in range(size):
                if i == 0:
                    i_rect = QtCore.QRect(
                        i*d, pos_y, d-spacing, height
                    )
                elif (i+1) == size:
                    i_rect = QtCore.QRect(
                        i*d+(spacing*i), pos_y, d-spacing, height
                    )
                else:
                    i_rect = QtCore.QRect(
                        i*d+(spacing*i), pos_y, d-spacing, height
                    )
                bkg_color = [Color.ENTRY_BACKGROUND_ENTRY_OFF, Color.ENTRY_BACKGROUND_ENTRY_ON][self._is_focused]
                bdr_color = [Color.ENTRY_BORDER_ENTRY_OFF, Color.ENTRY_BORDER_ENTRY_ON][self._is_focused]
                painter._set_frame_draw_by_rect_(
                    i_rect,
                    border_color=bdr_color,
                    background_color=bkg_color,
                    border_radius=4
                )

    def _set_focus_(self, boolean):
        self._is_focused = boolean
        self.update()

    def _set_entry_count_(self, size):
        self._entry_count = size


class _QtEntryItem(QtWidgets.QLineEdit):
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtEntryItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setFont(Font.NAME)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet(
            'QLineEdit{background: rgba(0, 0, 0, 0) ; color: rgba(255, 255, 255, 255)}'
            'QLineEdit{border: none}'
            'QLineEdit{selection-color: rgba(255, 255, 255, 255) ; selection-background-color: rgba(0, 127, 127, 255)}'
        )
        #
        self._value_type = str
        self._is_use_as_storage = False
        #
        self._default_value = None
        #
        self._maximum = 1
        self._minimum = 0
        #
        self.textChanged.connect(self._set_enter_changed_emit_send_)
        #
        self.setToolTip(
            (
                '"LMB-click" to entry\n'
                '"MMB-wheel" to modify "int" or "float" value'
            )
        )

    def _set_wheel_update_(self, event):
        if self._value_type in [int, float]:
            delta = event.angleDelta().y()
            pre_value = self._get_value_()
            if delta > 0:
                self._set_value_(pre_value+1)
            else:
                self._set_value_(pre_value-1)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _QtEntryFrame):
                    parent._set_focus_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _QtEntryFrame):
                    parent._set_focus_(False)
                #
                self._set_value_completion_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._set_wheel_update_(event)
        return False

    def contextMenuEvent(self, event):
        menu_raw = [
            ('Basic', ),
            ('Copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
            ('Paste', None, (True, self.paste, False), QtGui.QKeySequence.Paste),
            ('Cut', None, (True, self.cut, False), QtGui.QKeySequence.Cut),
            ('Extend', ),
            ('Undo', None, (True, self.undo, False), QtGui.QKeySequence.Undo),
            ('Redo', None, (True, self.redo, False), QtGui.QKeySequence.Redo),
            ('Select All', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll),
        ]
        if self._is_use_as_storage is True:
            menu_raw.extend(
                [
                    ('System',),
                    ('Open', None, (True, self._set_open_in_system_, False), QtGui.QKeySequence.Open)
                ]
            )
        #
        if self.isReadOnly():
            menu_raw = [
                ('Basic',),
                ('Copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('Extend', ),
                ('Select All', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if menu_raw:
            self._qt_menu = _utl_gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_raw_(menu_raw)
            self._qt_menu._set_show_()

    def _set_enter_changed_emit_send_(self):
        # noinspection PyUnresolvedReferences
        self.entry_changed.emit()

    def _set_value_completion_(self):
        if self._value_type in [int, float]:
            if not self.text():
                self._set_value_(0)

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        if self._value_type is None:
            pass
        elif self._value_type is str:
            pass
            # self._set_use_as_string_()
        elif self._value_type is int:
            self._set_use_as_integer_()
        elif self._value_type is float:
            self._set_use_as_float_()

    def _get_value_type_(self):
        return self._value_type

    def _set_open_in_system_(self):
        _ = self.text()
        if _:
            bsc_core.StoragePathOpt(_).set_open_in_system()

    def _set_use_as_storage_(self, boolean):
        self._is_use_as_storage = boolean

    def _set_use_as_string_(self):
        reg = QtCore.QRegExp(r'^[a-zA-Z0-9_]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())
        self._set_value_completion_()

    def _set_use_as_float_(self):
        self.setValidator(QtGui.QDoubleValidator())
        self._set_value_completion_()

    def _set_value_maximum_(self, value):
        self._maximum = value

    def _get_value_maximum_(self):
        return self._maximum

    def _set_value_minimum_(self, value):
        self._minimum = value

    def _get_value_minimum_(self):
        return self._minimum

    def _set_value_range_(self, maximum, minimum):
        self._set_value_maximum_(maximum), self._set_value_minimum_(minimum)

    def _get_value_range_(self):
        return self._get_value_maximum_(), self._get_value_minimum_()

    def _get_value_(self):
        _ = self.text()
        if self._value_type == str:
            return _
        elif self._value_type == int:
            return int(_)
        elif self._value_type == float:
            return float(_)
        return _

    def _set_value_(self, value):
        if value is not None:
            self.setText(
                str(self._value_type(value)).encode("UTF8")
            )
        else:
            self.setText('')

    def _get_default_value_(self):
        return self._default_value

    def _set_focus_connect_to_(self, widget):
        pass
    #
    def _get_is_selected_(self):
        boolean = False
        if self.selectedText():
            boolean = True
        return boolean

    def _set_value_clear_(self):
        self._set_value_('')

    def _set_completer_values_(self, values):
        pass

    def _set_enter_enable_(self, boolean):
        self.setReadOnly(not boolean)


class _QtEnumerateConstantEntry(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super(_QtEnumerateConstantEntry, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setPalette(QtDccMtd.get_qt_palette())
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setItemDelegate(_utl_gui_qt_wgt_utility.QtStyledItemDelegate())
        self.view().setAlternatingRowColors(True)
        self.view().setPalette(QtDccMtd.get_qt_palette())
        self.setFont(Font.NAME)
        #
        self.setLineEdit(_QtEntryItem())
        #
        self.setStyleSheet(
            (
                'QComboBox{{background: rgba(0, 0, 0, 0);color: rgba(255, 255, 255, 255)}}'
                'QComboBox{{border: none}}'
                # 'QAbstractItemView{{background: rgba(63, 63, 63, 255);color: rgba(255, 255, 255, 255)}}'
                'QAbstractItemView{{border: 1px rgba(63, 127, 255, 255);border-radius: 3px;border-style: solid}}'
                'QComboBox::drop-down{{width=16px;height=16p}}'
                'QComboBox::down-arrow{{border-image: none;image: url({0});width=16px;height=16px}}'
            ).format(
                utl_core.Icon.get('arrow_down'),
            )
        )

    def _set_use_as_storage_(self, boolean):
        self.lineEdit()._set_use_as_storage_(boolean)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _QtEntryFrame):
                    parent._set_focus_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _QtEntryFrame):
                    parent._set_focus_(False)
        return False


class _QtChooseDropView(utl_gui_qt_abstract._QtAbsListWidget):
    def __init__(self, *args, **kwargs):
        super(_QtChooseDropView, self).__init__(*args, **kwargs)
        self.setDragDropMode(QtWidgets.QListWidget.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.ListMode)
        self.setPalette(QtDccMtd.get_qt_palette())

    def paintEvent(self, event):
        pass


class _QtChooseDropWidget(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtChooseDropWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self._set_frame_def_init_()
        #
        self.installEventFilter(self)
        self.setFocusProxy(self.parent())
        #
        self._view_rect = QtCore.QRect()
        #
        self._list_widget = _QtChooseDropView(self)
        #
        self._item_count_maximum = 20
        self._item_width, self._item_height = 20, 20
        self._list_widget.setGridSize(QtCore.QSize(self._item_width, self._item_height))
        self._list_widget.setSpacing(2)
        self._list_widget.setUniformItemSizes(True)
        #
        self._region = 0
        #
        self._choose_index = None
        #
        self._side = 2
        self._margin = 8
        self._shadow_radius = 4

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        painter._set_popup_frame_draw_(
            bck_rect,
            margin=self._margin,
            side=self._side,
            shadow_radius=self._shadow_radius,
            region=self._region,
            border_color=Color.ENTRY_BORDER_ENTRY_ON,
            background_color=Color.ENTRY_BACKGROUND_ENTRY_ON,
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self.parent():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_close_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._set_close_()
        elif widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._set_drop_end_()
        return False

    def _set_widget_update_(self):
        self.update()

    def _set_widget_geometry_update_(self):
        side = self._side
        margin = self._margin
        shadow_radius = self._shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius - 2
        #
        self._list_widget.setGeometry(
            v_x, v_y, v_w, v_h
        )
        self._list_widget.updateGeometries()

    def _get_choose_point_(self, widget):
        rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        p = widget.mapToGlobal(rect.bottomLeft())
        return p.x(), p.y()

    def _get_choose_size_(self, widget):
        rect = widget.rect()
        return rect.width(), rect.height()

    def _set_drop_start_at_(self, index):
        parent = self.parent()
        content_name_texts = parent._get_choose_item_content_name_texts_at_(index)
        if isinstance(content_name_texts, (tuple, list)):
            desktop_rect = get_qt_desktop_rect()
            #
            press_pos = parent._get_choose_pos_at_(index)
            press_size = parent._get_choose_size_at_(index)
            #
            current_name_text = parent._get_guide_item_name_text_at_(index)
            #
            for seq, i_name_text in enumerate(content_name_texts):
                item_widget = _QtHItem()
                item = QtListWidgetItem()
                item.setSizeHint(QtCore.QSize(self._item_width, self._item_height))
                #
                self._list_widget.addItem(item)
                self._list_widget.setItemWidget(item, item_widget)
                item._set_item_show_connect_()
                #
                item_widget._set_name_text_(i_name_text)
                item_widget._set_index_(seq)
                if current_name_text == i_name_text:
                    item.setSelected(True)
            #
            self.setFocus(QtCore.Qt.PopupFocusReason)
            #
            self._drop_fnc_(
                press_pos, press_size,
                desktop_rect,
                self._get_maximum_width_(content_name_texts),
                self._get_maximum_height_()
            )
            self._choose_index = index
            parent._set_choose_item_expand_at_(index)
            #
            self._list_widget._set_scroll_to_selected_item_top_()
            #
            self._list_widget.itemClicked.connect(
                self._set_close_
            )

    def _set_drop_start_(self):
        parent = self.parent()
        content_name_texts = ['A', 'B']
        if isinstance(content_name_texts, (tuple, list)):
            desktop_rect = get_qt_desktop_rect()
            #
            press_pos = self._get_choose_point_(parent)
            press_size = self._get_choose_size_(parent)
            #
            current_name_text = 'B'
            #
            for seq, i_name_text in enumerate(content_name_texts):
                item_widget = _QtHItem()
                item = QtListWidgetItem()
                item.setSizeHint(QtCore.QSize(self._item_width, self._item_height))
                #
                self._list_widget.addItem(item)
                self._list_widget.setItemWidget(item, item_widget)
                item._set_item_show_connect_()
                #
                item_widget._set_name_text_(i_name_text)
                item_widget._set_index_(seq)
                if current_name_text == i_name_text:
                    item.setSelected(True)
            #
            self.setFocus(QtCore.Qt.PopupFocusReason)
            #
            self._set_drop_(
                press_pos, press_size
            )
            # self._drop_fnc_(
            #     press_pos, press_size,
            #     desktop_rect,
            #     press_size[0],
            #     self._get_maximum_height_()
            # )
            #
            self._list_widget._set_scroll_to_selected_item_top_()
            #
            self._list_widget.itemClicked.connect(
                self._set_close_
            )

    def _set_drop_end_(self):
        if self._choose_index is not None:
            parent = self.parent()
            selected_item_widget = self._list_widget._get_selected_item_widget_()
            if selected_item_widget:
                name_text = selected_item_widget._get_name_text_()
                path_text = parent._get_guide_item_path_text_at_(
                    self._choose_index
                )
                path_opt = bsc_core.DccPathDagOpt(path_text)
                path_opt.set_name(name_text)
                #
                parent._set_guide_item_name_text_at_(
                    name_text,
                    self._choose_index
                )
                parent._set_guide_item_path_text_at_(
                    str(path_opt),
                    self._choose_index
                )
                parent._set_item_geometries_update_()
            #
            parent._set_choose_item_collapse_at_(self._choose_index)
            parent._set_guide_current_(self._choose_index)
            parent._set_guide_item_clicked_emit_send_()
            parent._set_guide_current_clear_()

    def _get_maximum_width_(self, texts):
        count = len(texts)
        texts.append(str(count))
        _ = max([self.fontMetrics().width(i) for i in texts]) + 16
        if count > self._item_count_maximum:
            return _ + 24
        return _

    def _get_maximum_height_(self):
        rects = [self._list_widget.visualItemRect(self._list_widget.item(i)) for i in range(self._list_widget.count())[:self._item_count_maximum]]
        rect = rects[-1]
        y = rect.y()
        h = rect.height()
        return y+h+1+4

    def _drop_fnc_(self, press_pos, press_size, desktop_rect, view_width, view_height):
        press_x, press_y = press_pos.x(), press_pos.y()
        press_w, press_h = press_size
        #
        maxWidth = desktop_rect.width()
        maxHeight = desktop_rect.height()
        #
        side = self._side
        margin = self._margin
        shadow_radius = self._shadow_radius
        #
        o_x = 0
        o_y = 0
        #
        width_ = view_width+margin*2+side*2+shadow_radius
        height_ = view_height+margin*2+side*2+shadow_radius
        #
        r_x, r_y, region = bsc_core.CoordMtd.set_region_to(
            position=(press_x, press_y),
            size=(width_, height_),
            maximum_size=(maxWidth, maxHeight),
            offset=(o_x, o_y)
        )
        self._region = region
        #
        if region in [0, 1]:
            y_ = r_y-side+press_h/2
        else:
            y_ = r_y+side+shadow_radius-press_h/2
        #
        if region in [0, 2]:
            x_ = r_x-margin*3
        else:
            x_ = r_x+margin*3+side+shadow_radius
        #
        self.setGeometry(
            x_, y_,
            width_, height_
        )
        #
        self._set_widget_geometry_update_()
        #
        self.show()
        #
        self.update()

    def _set_drop_(self, pos, size):
        x, y = pos
        w, h = size
        # desktop_rect = get_qt_desktop_rect()
        self.setGeometry(
            x, y,
            w, h
        )
        self._set_widget_geometry_update_()
        #
        self.show()
        #
        self.update()

    def _set_close_(self):
        self.close()
        self.deleteLater()


class _QtChooseDropWidget1(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtChooseDropWidget1, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self._set_frame_def_init_()
        #
        self.installEventFilter(self)
        self.setFocusProxy(self.parent())
        #
        self._list_widget = _QtChooseDropView(self)
        #
        self._item_count_maximum = 20
        self._item_width, self._item_height = 20, 20
        self._list_widget.setGridSize(QtCore.QSize(self._item_width, self._item_height))
        self._list_widget.setSpacing(2)
        self._list_widget.setUniformItemSizes(True)
        #
        self._region = 0
        #
        self._choose_index = None
        #
        self._side = 2
        self._margin = 8
        self._shadow_radius = 4

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        painter._set_frame_draw_by_rect_(
            self._frame_rect,
            border_color=Color.ENTRY_BORDER_ENTRY_ON,
            background_color=Color.ENTRY_BACKGROUND_ENTRY_ON,
            border_radius=4
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self.parent():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_close_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._set_close_()
        elif widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._set_drop_end_()
        return False

    def _set_widget_update_(self):
        self.update()

    def _set_widget_geometry_update_(self):
        side = self._side
        margin = self._margin
        shadow_radius = self._shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius - 2
        #
        self._frame_rect.setRect(
            x, y, w, h
        )
        self._list_widget.setGeometry(
            x+1, y+1, w-2, h-2
        )
        self._list_widget.updateGeometries()
    @classmethod
    def _get_choose_point_(cls, widget):
        rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        p = widget.mapToGlobal(rect.bottomLeft())
        return p.x(), p.y()
    @classmethod
    def _get_choose_size_(cls, widget):
        rect = widget.rect()
        return rect.width(), rect.height()

    def _set_drop_start_(self):
        parent = self.parent()
        content_name_texts = parent._get_values_()
        if isinstance(content_name_texts, (tuple, list)):
            press_pos = self._get_choose_point_(parent)
            width, height = self._get_choose_size_(parent)
            #
            current_name_text = parent._get_value_()
            #
            for seq, i_name_text in enumerate(content_name_texts):
                item_widget = _QtHItem()
                item = QtListWidgetItem()
                item.setSizeHint(QtCore.QSize(self._item_width, self._item_height))
                #
                self._list_widget.addItem(item)
                self._list_widget.setItemWidget(item, item_widget)
                item._set_item_show_connect_()
                #
                item_widget._set_name_text_(i_name_text)
                item_widget._set_index_(seq)
                if current_name_text == i_name_text:
                    item.setSelected(True)
            #
            self.setFocus(QtCore.Qt.PopupFocusReason)
            #
            self._set_drop_(
                press_pos,
                (width, self._get_maximum_height_())
            )
            #
            self._list_widget._set_scroll_to_selected_item_top_()
            #
            self._list_widget.itemClicked.connect(
                self._set_close_
            )
            parent._set_focus_(True)

    def _set_drop_end_(self):
        parent = self.parent()
        selected_item_widget = self._list_widget._get_selected_item_widget_()
        if selected_item_widget:
            name_text = selected_item_widget._get_name_text_()
            parent._set_value_(name_text)
        #
        parent._set_focus_(False)

    def _get_maximum_height_(self):
        rects = [self._list_widget.visualItemRect(self._list_widget.item(i)) for i in range(self._list_widget.count())[:self._item_count_maximum]]
        if rects:
            rect = rects[-1]
            y = rect.y()
            h = rect.height()
            return y+h+1+4
        return 20

    def _set_drop_(self, pos, size):
        x, y = pos
        w, h = size
        # desktop_rect = get_qt_desktop_rect()
        self.setGeometry(
            x, y,
            w, h
        )
        self._set_widget_geometry_update_()
        #
        self.show()
        #
        self.update()

    def _set_close_(self):
        self.close()
        self.deleteLater()


class _QtConstantValueEntryItem(
    _QtEntryFrame,
    utl_gui_qt_abstract._QtConstantValueEntryDef
):
    QT_VALUE_ENTRY_CLASS = _QtEntryItem
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtConstantValueEntryItem, self).__init__(*args, **kwargs)
        #
        self._set_constant_value_entry_def_init_()
        #
        self._layout = QtHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        #
        self._set_value_entry_build_(self._value_type)

    def _set_value_entry_build_(self, value_type):
        self._value_type = value_type
        #
        self._value_entry_widget = _QtEntryItem()
        self._layout.addWidget(self._value_entry_widget)
        self._value_entry_widget._set_value_type_(self._value_type)


class _QtEnumerateValueEntryItem(
    _QtEntryFrame,
    utl_gui_qt_abstract._QtEnumerateValueEntryDef,
    utl_gui_qt_abstract._QtItemChooseActionDef,
):
    QT_VALUE_ENTRY_CLASS = _QtEntryItem
    CHOOSE_DROP_WIDGET_CLS = _QtChooseDropWidget1
    def __init__(self, *args, **kwargs):
        super(_QtEnumerateValueEntryItem, self).__init__(*args, **kwargs)
        #
        self._set_enumerate_value_entry_def_init_()
        self._set_item_choose_def_init_()
        #
        self._layout = QtHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        #
        self._set_value_entry_build_(self._value_type)
        self._value_entry_widget._set_enter_enable_(False)
        #
        self._drop_button = _QtIconPressItem()
        self._layout.addWidget(self._drop_button)
        self._drop_button._set_file_icon_path_(
            utl_core.Icon.get('down')
        )
        self._drop_button._set_icon_frame_size_(16, 16)
        self._drop_button._set_file_icon_size_(12, 12)
        self._drop_button.press_clicked.connect(self._set_item_choose_drop_)

    def _set_value_entry_build_(self, value_type):
        self._value_type = value_type
        #
        self._value_entry_widget = self.QT_VALUE_ENTRY_CLASS()
        self._layout.addWidget(self._value_entry_widget)
        self._value_entry_widget._set_value_type_(self._value_type)

    def _set_item_choose_drop_(self):
        widget = self.CHOOSE_DROP_WIDGET_CLS(self)
        widget._set_drop_start_()


class _QtArrayValueEntryItem(
    _QtEntryFrame,
    utl_gui_qt_abstract._QtArrayValueEntryDef,
):
    QT_VALUE_ENTRY_CLASS = _QtEntryItem
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtArrayValueEntryItem, self).__init__(*args, **kwargs)
        #
        self._set_array_value_entry_def_init_()
        #
        self._layout = QtHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        #
        self._set_value_entry_build_(2, self._value_type)

    def _set_value_entry_build_(self, value_size, value_type):
        self._value_type = value_type
        #
        self._value_entry_widgets = []
        set_qt_layout_clear(self._layout)
        #
        self._set_entry_count_(value_size)
        if value_size:
            for i in range(value_size):
                _i_value_entry_widget = _QtEntryItem()
                _i_value_entry_widget._set_value_type_(self._value_type)
                self._layout.addWidget(_i_value_entry_widget)
                self._value_entry_widgets.append(_i_value_entry_widget)


class _QtHExpandItem0(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtNameDef,
    utl_gui_qt_abstract._QtIconDef,
    #
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
    utl_gui_qt_abstract._QtItemExpandActionDef,
):
    toggled = qt_signal(bool)
    def __init__(self, *args, **kwargs):
        super(_QtHExpandItem0, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self._set_frame_def_init_()
        self._set_name_def_init_()
        self._set_icon_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()
        self._set_item_expand_action_def_init_()
        #
        self._item_is_expanded = False
        self._item_expand_icon_file_path_0 = utl_core.Icon.get('arrow_up')
        self._item_expand_icon_file_path_1 = utl_core.Icon.get('arrow_down')
        self._item_is_hovered = False
        #
        self._set_item_expand_update_()
        # font
        self.setFont(Font.NAME)

    def _set_widget_update_(self):
        self.update()

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        #
        self._set_frame_rect_(
            x, y, w-1, h-1
        )
        f_w, f_h = self._icon_frame_size
        i_w, i_h = self._file_icon_size
        self._set_file_icon_rect_(
            x+(f_w-i_w)/2, y+(f_h-i_h)/2, i_w, i_h
        )
        #
        x += f_w+spacing
        #
        if self._name_icon_text is not None:
            i_w, i_h = self._name_icon_size
            self._set_name_icon_rect_(
                x+(f_w-i_w) / 2, y+(f_h-i_h) / 2, i_w, i_h
            )
            x += f_w+spacing
        #
        self._set_name_rect_(
            x, y, w-20, h
        )

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_widget_geometry_update_()
        #
        offset = self._get_item_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        bkg_color = [Color.BAR_NORMAL, Color.BAR_HIGHLIGHT][self._item_is_hovered]
        painter.setBrush(bkg_color)
        #
        painter._set_frame_draw_by_rect_(
            self._frame_rect,
            border_color=bkg_color,
            background_color=bkg_color,
            border_radius=1,
            offset=offset
        )
        # file-icon
        painter._set_file_icon_draw_by_rect_(
            self._file_icon_rect,
            self._file_icon_path,
            offset=offset
        )
        # name-icon
        if self._name_icon_text is not None:
            painter._set_name_icon_draw_by_rect_(
                self._name_icon_rect,
                self._name_icon_text,
                background_color=bkg_color,
                offset=offset,
                border_radius=8,
            )
        # text
        if self._name_text is not None:
            painter._set_text_draw_by_rect_(
                self._name_rect,
                self._name_text,
                font=Font.GROUP,
                color=Color.TEXT_NORMAL,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_item_event_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_item_action_flag_(self.EXPAND_CLICKED_FLAG)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_item_action_flag_() == self.EXPAND_CLICKED_FLAG:
                        self._set_item_expand_action_run_()
                        #
                        self._set_item_action_flag_clear_()
        return False

    def set_expanded(self, boolean):
        self._item_is_expanded = boolean

    def _set_item_expand_update_(self):
        self._set_file_icon_path_(
            [self._item_expand_icon_file_path_1, self._item_expand_icon_file_path_0][self._item_is_expanded]
        )
        #
        self._set_widget_update_()


class _QtHExpandItem1(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtNameDef,
    utl_gui_qt_abstract._QtIconDef,
    #
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
    utl_gui_qt_abstract._QtItemExpandActionDef,
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
        self._set_name_def_init_()
        self._set_icon_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()
        self._set_item_expand_action_def_init_()
        #
        self._item_is_expand_enable = True
        self._item_is_expanded = False
        self._item_expand_icon_file_path_0 = utl_core.Icon.get('arrow_up')
        self._item_expand_icon_file_path_1 = utl_core.Icon.get('arrow_down')
        #
        self._set_item_expand_update_()
        # font
        self.setFont(Font.NAME)

    def _set_widget_update_(self):
        self.update()

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_widget_geometry_update_()
        #
        offset = self._get_item_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        bkg_color = [Color.BAR_NORMAL, Color.BAR_HIGHLIGHT][self._item_is_hovered]
        painter.setBrush(bkg_color)
        painter._set_frame_draw_by_rect_(
            rect=self._frame_rect,
            border_color=bkg_color,
            background_color=bkg_color,
            border_radius=1,
            offset=offset
        )
        # icon
        painter._set_file_icon_draw_by_rect_(
            rect=self._file_icon_rect,
            file_path=self._file_icon_path,
            offset=offset
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_item_event_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_item_action_flag_(self.EXPAND_CLICKED_FLAG)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_item_action_flag_() == self.EXPAND_CLICKED_FLAG:
                        self._set_item_expand_action_run_()
                        #
                        self._set_item_action_flag_clear_()
        return False

    def _set_item_expand_update_(self):
        if self._item_is_expanded is True:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
            )
        else:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            )
        #
        if self._item_expand_direction == self.EXPAND_TOP_TO_BOTTOM:
            self._set_file_icon_path_(
                [self._item_expand_icon_file_path_1, self._item_expand_icon_file_path_0][self._item_is_expanded]
            )
        elif self._item_expand_direction == self.EXPAND_BOTTOM_TO_TOP:
            self._set_file_icon_path_(
                [self._item_expand_icon_file_path_0, self._item_expand_icon_file_path_1][self._item_is_expanded]
            )
        #
        self._set_widget_update_()

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._set_frame_rect_(
            x, y, w-1, h-1
        )
        #
        f_w, f_h = 12, 12
        i_w, i_h = 8, 8
        #
        if self._item_expand_direction == self.EXPAND_TOP_TO_BOTTOM:
            self._set_file_icon_rect_(
                x+(f_w-i_w) / 2, y+(f_h-i_h) / 2,
                i_w, i_h
            )
        elif self._item_expand_direction == self.EXPAND_BOTTOM_TO_TOP:
            self._set_file_icon_rect_(
                x+(f_w-i_w) / 2, y+h-f_h+(f_h-i_h) / 2,
                i_w, i_h
            )


class QtTreeWidgetItem(
    QtWidgets.QTreeWidgetItem,
    utl_gui_qt_abstract._QtIconDef,
    utl_gui_qt_abstract._QtItemShowDef,
    utl_gui_qt_abstract._QtMenuDef,
):
    visible = qt_signal(bool)
    expanded = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtTreeWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        )
        #
        self._is_check_enable = True
        self._emit_send_enable = False
        #
        self._set_icon_def_init_()
        self._set_menu_def_init_()

    def _set_widget_update_(self):
        pass

    def setCheckState(self, column, state):
        self.setData(column, QtCore.Qt.CheckStateRole, state, emit_send_enable=False)

    def checkState(self, column):
        if self._is_check_enable is True:
            return self.data(column, QtCore.Qt.CheckStateRole)
        return QtCore.Qt.Unchecked

    def setData(self, column, role, value, **kwargs):
        emit_send_enable = False
        tree_widget = self.treeWidget()
        if role == QtCore.Qt.CheckStateRole:
            if self._is_check_enable is False:
                value = QtCore.Qt.Unchecked
            #
            emit_send_enable = kwargs.get('emit_send_enable', True)
        #
        super(QtTreeWidgetItem, self).setData(column, role, value)
        #
        if emit_send_enable is True:
            self._set_check_state_extra_(column)
            #
            check_state = self.checkState(column)
            checked = [False, True][check_state == QtCore.Qt.Checked]
            #
            tree_widget._set_item_check_action_run_(self, column)
            tree_widget._set_item_toggle_emit_send_(self, column, checked)

    def _set_file_icon_path_(self, file_path, column=0):
        self._file_icon_path = file_path
        #
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(file_path),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.setIcon(column, icon)

    def _set_color_icon_rgb_(self, rgb, column=0):
        self.setIcon(
            column,
            utl_gui_qt_core.QtUtilMtd.get_color_icon(rgb)
        )

    def _set_name_icon_text_(self, text, column=0):
        self.setIcon(
            column,
            utl_gui_qt_core.QtUtilMtd.get_name_text_icon(text)
        )

    def _set_icon_state_update_(self, column):
        icon = QtGui.QIcon()
        pixmap = QtGui.QPixmap(self._file_icon_path)
        if self._icon_state in [gui_core.State.ENABLE, gui_core.State.DISABLE, gui_core.State.WARNING, gui_core.State.ERROR]:
            if self._icon_state == gui_core.State.ENABLE:
                background_color = Color.ENABLE
            elif self._icon_state == gui_core.State.DISABLE:
                background_color = Color.DISABLE
            elif self._icon_state == gui_core.State.WARNING:
                background_color = Color.WARNING
            elif self._icon_state == gui_core.State.ERROR:
                background_color = Color.ERROR
            else:
                raise TypeError()
            #
            painter = _utl_gui_qt_wgt_utility.QtPainter(pixmap)
            rect = pixmap.rect()
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            #
            border_color = Color.ICON_BORDER_NORMAL
            #
            state_rect = QtCore.QRect(
                x, y+h/2, w/2, h/2
            )
            painter._set_frame_draw_by_rect_(
                state_rect,
                border_color=border_color,
                background_color=background_color,
                border_radius=w/2
            )
            painter.end()
        #
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.setIcon(column, icon)

    def _set_state_(self, state, column):
        self._icon_state = state
        #
        self._set_icon_state_update_(column)
        #
        if state == gui_core.State.NORMAL:
            self.setForeground(column, QtGui.QBrush(Color.NORMAL))
        elif state == gui_core.State.ENABLE:
            self.setForeground(column, QtGui.QBrush(Color.ENABLE))
        elif state == gui_core.State.DISABLE:
            self.setForeground(column, QtGui.QBrush(Color.DISABLE))
        elif state == gui_core.State.WARNING:
            self.setForeground(column, QtGui.QBrush(Color.WARNING))
        elif state == gui_core.State.ERROR:
            self.setForeground(column, QtGui.QBrush(Color.ERROR))

    def _set_update_(self):
        tree_widget = self.treeWidget()
        tree_widget.update()

    def _set_user_data_(self, key, value, column=0):
        raw = self.data(column, QtCore.Qt.UserRole) or {}
        raw[key] = value
        self.setData(
            column, QtCore.Qt.UserRole, raw
        )

    def _get_user_data_(self, key, column=0):
        pass

    def _set_check_enable_(self, boolean, column=0):
        self._is_check_enable = boolean
        self.setData(column, QtCore.Qt.CheckStateRole, self.checkState(column))

    def _get_item_is_check_enable_(self):
        return self._is_check_enable

    def _set_emit_send_enable_(self, boolean):
        self._emit_send_enable = boolean

    def _get_emit_send_enable_(self):
        return self._emit_send_enable

    def _set_check_state_extra_(self, column):
        if self._is_check_enable is True:
            check_state = self.checkState(column)
            descendants = self._get_descendants_()
            [i.setData(column, QtCore.Qt.CheckStateRole, check_state, emit_send_enable=False) for i in descendants]
            ancestors = self._get_ancestors_()
            [i.setData(column, QtCore.Qt.CheckStateRole, i._get_check_state_by_descendants(column), emit_send_enable=False) for i in ancestors]

    def _get_check_state_by_descendants(self, column):
        for i in self._get_descendants_():
            if i.checkState(column) == QtCore.Qt.Checked:
                return QtCore.Qt.Checked
        return QtCore.Qt.Unchecked

    def _get_children_(self):
        lis = []
        count = self.childCount()
        for i_index in range(count):
            i_item = self.child(i_index)
            lis.append(i_item)
        return lis

    def _get_descendants_(self):
        def _rcs_fnc(item_):
            _child_count = item_.childCount()
            for _child_index in range(_child_count):
                _child_item = item_.child(_child_index)
                lis.append(_child_item)
                _rcs_fnc(_child_item)

        lis = []
        _rcs_fnc(self)
        return lis

    def _get_ancestors_(self):
        def _rcs_fnc(item_):
            _parent_item = item_.parent()
            if _parent_item is not None:
                lis.append(_parent_item)
                _rcs_fnc(_parent_item)

        lis = []
        _rcs_fnc(self)
        return lis

    def _get_is_hidden_(self, ancestors=False):
        if ancestors is True:
            if self.isHidden():
                return True
            qt_tree_widget, qt_tree_widget_item = self.treeWidget(), self
            return QtTreeMtd.get_item_is_ancestor_hidden(qt_tree_widget, qt_tree_widget_item)
        else:
            return self.isHidden()

    def _get_name_texts_(self):
        column_count = self.treeWidget().columnCount()
        return [self.text(i) for i in range(column_count)]
    # show
    def _set_view_(self, widget):
        self._tree_widget = widget

    def _set_item_show_connect_(self):
        self._set_item_show_def_init_(self.treeWidget())

    def _get_view_(self):
        return self.treeWidget()

    def _get_item_is_viewport_show_able_(self):
        _ = self.parent()
        if self.parent() is None:
            return True
        return _.isExpanded()

    def _set_item_widget_visible_(self, boolean):
        pass
        # self.setVisible(boolean)

    def _set_name_(self, text, column=0):
        self.setText(column, text)

    def _set_item_show_loading_update_(self):
        self._item_show_loading_index += 1
        #
        if self._item_show_loading_is_finish is False:
            self._set_name_(
                'loading .{}'.format('.'*(self._item_show_loading_index % 3))
            )

    def _get_item_widget_(self):
        pass

    def __str__(self):
        return '{}(names="{}")'.format(
            self.__class__.__name__, ', '.join(self._get_name_texts_())
        )

    def __repr__(self):
        return self.__str__()


class QtListWidgetItem(
    QtWidgets.QListWidgetItem,
    utl_gui_qt_abstract._QtItemShowDef,
):
    def __init__(self, *args, **kwargs):
        super(QtListWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        )
        self._visible_tgt_key = None

    def _set_widget_update_(self):
        item_widget = self._get_item_widget_()
        if item_widget is not None:
            item_widget.update()

    def setData(self, role, value):
        if role == QtCore.Qt.CheckStateRole:
            pass
        super(QtListWidgetItem, self).setData(role, value)

    def _set_item_widget_(self, widget):
        list_widget = self.listWidget()
        list_widget.setItemWidget(self, widget)

    def _get_item_widget_(self):
        list_widget = self.listWidget()
        return list_widget.itemWidget(self)

    def _set_visible_tgt_key_(self, key):
        self._visible_tgt_key = key

    def _get_visible_tgt_key_(self):
        return self._visible_tgt_key
    # show
    def _set_view_(self, widget):
        self._list_widget = widget

    def _set_item_show_connect_(self):
        self._set_item_show_def_init_(self.listWidget())

    def _get_view_(self):
        return self.listWidget()

    def _get_item_is_viewport_show_able_(self):
        item = self
        list_widget = self.listWidget()
        #
        self._set_item_show_loading_start_()
        return list_widget._get_item_is_viewport_show_able_at_(item)

    def _set_item_widget_visible_(self, boolean):
        self._get_item_widget_().setVisible(boolean)


class _QtHItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtIndexDef,
    utl_gui_qt_abstract._QtTypeDef,
    utl_gui_qt_abstract._QtNameDef,
    utl_gui_qt_abstract._QtPathDef,
    # action
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
    utl_gui_qt_abstract._QtItemSelectActionDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtHItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._set_frame_def_init_()
        self._set_index_def_init_()
        self._set_type_def_init_()
        self._set_name_def_init_()
        self._set_path_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()
        self._set_item_select_action_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_item_event_filter_(event)
            #
            if event.type() == QtCore.QEvent.Resize:
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                elif event.button() == QtCore.Qt.LeftButton:
                    self.clicked.emit()
                #
                self._item_is_hovered = True
                self.update()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_widget_geometry_update_()
        #
        bkg_color = painter._get_item_background_color_(
            self._frame_rect,
            is_hover=self._item_is_hovered,
            is_select=self._is_selected
        )
        painter._set_frame_draw_by_rect_(
            self._frame_rect,
            border_color=Color.TRANSPARENT,
            background_color=bkg_color,
            border_radius=1
        )
        if self._name_text is not None:
            painter._set_text_draw_by_rect_(
                self._name_rect,
                self._name_text,
                color=self._name_text_color,
                font=self._name_text_font,
                text_option=self._name_text_option
            )
        #
        if self._index is not None:
            painter._set_text_draw_by_rect_(
                self._index_rect,
                self._get_index_text_(),
                color=self._index_text_color,
                font=self._index_text_font,
                text_option=self._index_text_option
            )

    def _set_widget_update_(self):
        self.update()

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        side = 2
        #
        i_x, i_y = x+side, y
        i_w, i_h = w-side*2, h
        #
        self._set_frame_rect_(
            x, y, w, h
        )
        #
        self._set_name_rect_(
            i_x, i_y, i_w, i_h
        )
        #
        self._set_index_rect_(
            i_x, i_y, i_w, i_h
        )


class _QtListItemWidget(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtIndexDef,
    utl_gui_qt_abstract._QtImageDef,
    #
    utl_gui_qt_abstract._QtMenuDef,
    #
    utl_gui_qt_abstract._QtIconsDef,
    utl_gui_qt_abstract._QtNamesDef,
    #
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
    utl_gui_qt_abstract._QtItemSelectActionDef,
):
    clicked = qt_signal()
    viewport_show = qt_signal()
    viewport_hide = qt_signal()
    #
    QT_MENU_CLASS = _utl_gui_qt_wgt_utility.QtMenu
    def __init__(self, *args, **kwargs):
        super(_QtListItemWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._set_frame_def_init_()
        self._set_index_def_init_()
        self._set_icons_def_init_()
        self._set_image_def_init_()
        self._set_names_def_init_()
        self._set_menu_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()
        self._set_item_select_action_def_init_()
        #
        self._icons_frame_rect = QtCore.QRect()
        self._image_frame_rect = QtCore.QRect()
        self._names_frame_rect = QtCore.QRect()
        #
        self._file_type_icon = None
        #
        self._list_widget = None
        self._list_widget_item = None
        #
        self._frame_icon_width, self._frame_icon_height = 40, 128
        self._frame_image_width, self._frame_image_height = 128, 128
        self._frame_name_width, self._frame_name_height = 128, 40
        #
        self._is_viewport_show_enable = True

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_item_event_filter_(event)
            #
            if event.type() == QtCore.QEvent.Resize:
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                elif event.button() == QtCore.Qt.LeftButton:
                    self.clicked.emit()
                #
                self._item_is_hovered = True
                self.update()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_widget_geometry_update_()
        #
        w, h = self.width(), self.height()
        #
        bkg_rect = QtCore.QRect(1, 1, w-1, h-1)
        bkg_color = painter._get_item_background_color_(
            bkg_rect,
            is_hover=self._item_is_hovered,
            is_select=self._is_selected
        )
        #
        if self._get_item_()._item_show_loading_is_enable is True:
            painter._set_loading_draw_by_rect_(
                self._frame_rect,
                self._get_item_()._item_show_loading_index
            )
        else:
            painter._set_frame_draw_by_rect_(
                bkg_rect,
                border_color=Color.TRANSPARENT,
                background_color=bkg_color,
                border_radius=1
            )
            #
            if self._get_has_icons_():
                painter._set_frame_draw_by_rect_(
                    self._icons_frame_rect,
                    border_color=Color.TRANSPARENT,
                    background_color=Color.ITEM_BACKGROUND_NORMAL,
                )
            #
            painter._set_frame_draw_by_rect_(
                self._image_frame_rect,
                border_color=Color.TRANSPARENT,
                background_color=Color.ITEM_BACKGROUND_NORMAL,
            )
            painter._set_frame_draw_by_rect_(
                self._names_frame_rect,
                border_color=self._get_name_frame_border_color_(),
                background_color=self._get_name_frame_background_color_(),
            )
            #
            icon_indices = self._get_icon_indices_()
            if icon_indices:
                icons = self._get_pixmap_icons_()
                if icons:
                    for icon_index in icon_indices:
                        painter._set_pixmap_draw_by_rect_(
                            self._get_icon_rect_at_(icon_index),
                            self._get_pixmap_icon_at_(icon_index)
                        )
                else:
                    icon_file_paths = self._get_icon_file_paths_()
                    if icon_file_paths:
                        for icon_index in icon_indices:
                            painter._set_file_icon_draw_by_rect_(
                                self._get_icon_rect_at_(icon_index),
                                self._get_icon_file_path_at_(icon_index)
                            )
            #
            image_file_path = self._get_image_file_path_()
            if image_file_path:
                painter._set_any_image_draw_by_rect_(
                    self._get_image_rect_(), image_file_path
                )
            #
            painter._set_text_draw_by_rect_(
                self._get_index_rect_(),
                text=str(self._get_index_()),
                text_option=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
                color=Color.TEXT_DISABLE
            )
            #
            name_indices = self._get_name_indices_()
            if name_indices:
                if self._list_widget._get_is_grid_mode_():
                    name_indices_ = name_indices[:3]
                    qt_text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
                else:
                    name_indices_ = name_indices
                    qt_text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
                #
                for name_index in name_indices_:
                    painter._set_text_draw_by_rect_(
                        self._get_name_rect_at_(name_index),
                        text=self._get_name_text_at_(name_index),
                        text_option=qt_text_option
                    )
            #
            if self._get_item_()._item_show_image_loading_is_enable is True:
                painter._set_loading_draw_by_rect_(
                    self._image_frame_rect,
                    self._get_item_()._item_show_loading_index
                )

    def _set_frame_icon_size_(self, w, h):
        self._frame_icon_width, self._frame_icon_height = w, h

    def _set_frame_image_size_(self, w, h):
        self._frame_image_width, self._frame_image_height = w, h

    def _set_frame_name_size_(self, w, h):
        self._frame_name_width, self._frame_name_height = w, h

    def _set_list_widget_item_(self, widget):
        self._list_widget_item = widget

    def _get_list_widget_item_(self):
        return self._list_widget_item

    def _get_item_(self):
        return self._list_widget_item

    def _set_item_(self, item):
        self._list_widget_item = item

    def _set_view_(self, widget):
        self._list_widget = widget

    def _get_view_(self):
        return self._list_widget

    def _set_widget_geometry_update_(self):
        self._set_frame_geometry_update_()
        self._set_sub_icon_geometry_update_()
        self._set_sub_image_geometry_update_()
        self._set_sub_name_geometry_update_()

    def _set_frame_geometry_update_(self):
        if self._list_widget is not None:
            side = 4
            spacing = 2
            x, y = side, side
            w, h = self.width()-side*2, self.height()-side*2
            self._set_frame_rect_(x, y, w, h)
            if self._list_widget._get_is_grid_mode_():
                x_ = x
                w_0, h_0 = self._frame_icon_width, self._frame_image_height
                w_1, h_1 = w, self._frame_image_height
                #
                if self._get_has_icons_() is True:
                    self._icons_frame_rect.setRect(
                        x_, y, w_0, h_0
                    )
                    #
                    x_ += w_0+spacing
                    w_1, h_1 = self._frame_image_width, self._frame_image_height
                #
                self._image_frame_rect.setRect(
                    x_, y, w_1, h_1
                )
                #
                w_2, h_2 = w, self._frame_name_height
                y += h_1+spacing
                self._names_frame_rect.setRect(
                    x, y, w_2, h_2
                )
            else:
                w_0, h_0 = self._frame_icon_width, h
                self._icons_frame_rect.setRect(
                    x, y, w_0, h_0
                )
                #
                x += w_0+spacing
                w_1, h_1 = self._frame_image_width, h
                self._image_frame_rect.setRect(
                    x, y, w_1, h_1
                )
                #
                w_2, h_2 = w-h_1, h
                x += w_1+spacing
                self._names_frame_rect.setRect(
                    x, y, w_2, h_2
                )

    def _set_sub_icon_geometry_update_(self):
        rect = self._icons_frame_rect
        spacing = 2
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        f_w, f_h = 20, 20
        i_f_w, i_f_h = 16, 16
        icon_indices = self._get_icon_indices_()
        for icon_index in icon_indices:
            self._set_icon_rect_at_(
                x+(f_w-i_f_w)/2, y+(f_h-i_f_h)/2+icon_index*(f_h+spacing), i_f_w, i_f_h,
                icon_index
            )

    def _set_sub_image_geometry_update_(self):
        rect = self._image_frame_rect
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        image_file_path = self._get_image_file_path_()
        if image_file_path:
            x += 2
            y += 2
            w -= 4+1
            h -= 4+1
            i_w_0, i_h_0 = self._get_image_size_()
            if (i_w_0, i_h_0) != (0, 0):
                i_x, i_y, i_w, i_h = gui_core.SizeMethod.set_fit_to(
                    (i_w_0, i_h_0), (w, h)
                )
                self._set_image_rect_(
                    x+i_x, y+i_y, i_w, i_h
                )

    def _set_sub_name_geometry_update_(self):
        rect = self._names_frame_rect
        spacing = 2
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        t_w, t_h = 12, 12
        #
        self._set_index_rect_(
            x+2, y+h-t_h, w-4, t_h
        )
        #
        name_indices = self._get_name_indices_()
        for name_index in name_indices:
            self._set_name_rect_at_(
                x+2, y+2+name_index*t_h, w, t_h,
                name_index
            )

    def _set_widget_update_(self):
        # noinspection PyUnresolvedReferences
        self.update()

    def __str__(self):
        return '{}(names={})'.format(
            self.__class__.__name__,
            ', '.join(self._get_name_texts_())
        )

    def __repr__(self):
        return self.__str__()


class _AbsQtSplitterHandle(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef
):
    QT_ORIENTATION = None
    def _set_widget_update_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitterHandle, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._swap_enable = True
        #
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        #
        self._contract_icon_name_l = ['contract_h_l', 'contract_v_l'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._contract_icon_name_r = ['contract_h_r', 'contract_v_r'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._swap_icon_name = ['swap_h', 'swap_v'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        #
        self._contract_frame_size = [(20, 10), (10, 20)][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._contract_icon_size = [(16, 8), (8, 16)][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._contract_l_button = _QtIconPressItem()
        self._contract_l_button._set_icon_frame_size_(*self._contract_frame_size)
        self._contract_l_button._set_file_icon_size_(*self._contract_icon_size)
        self._contract_l_button.setMaximumSize(*self._contract_frame_size)
        self._contract_l_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._contract_l_button)
        self._contract_l_button.clicked.connect(self._set_contract_l_switch_)
        self._contract_l_button.setToolTip(
            '"LMB-click" to contact left/top.'
        )
        #
        self._swap_button = _QtIconPressItem()
        #
        self._swap_button._set_file_icon_path_(utl_core.Icon.get(self._swap_icon_name))
        self._swap_button._set_icon_frame_size_(*self._contract_frame_size)
        self._swap_button._set_file_icon_size_(*self._contract_icon_size)
        self._swap_button.setMaximumSize(*self._contract_frame_size)
        self._swap_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._swap_button)
        self._swap_button.clicked.connect(self._set_swap_)
        self._swap_button.setToolTip(
            '"LMB-click" to swap.'
        )
        #
        self._contract_r_button = _QtIconPressItem()
        self._contract_r_button._set_icon_frame_size_(*self._contract_frame_size)
        self._contract_r_button._set_file_icon_size_(*self._contract_icon_size)
        self._contract_r_button.setMaximumSize(*self._contract_frame_size)
        self._contract_r_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._contract_r_button)
        self._contract_r_button.clicked.connect(self._set_contract_r_switch_)
        self._contract_r_button.setToolTip(
            '"LMB-click" to contact right/bottom.'
        )
        #
        self._set_contract_buttons_update_()
        #
        self.installEventFilter(self)
        self._item_is_hovered = False
        #
        self._set_frame_def_init_()
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()
        #
        self._hover_frame_border_color = 95, 95, 95
        self._hover_frame_background_color = 95, 95, 95

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self.setCursor(QtCore.Qt.SplitHCursor)
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self.setCursor(QtCore.Qt.SplitVCursor)
                #
                self._set_item_hovered_(True)
            elif event.type() == QtCore.QEvent.Leave:
                self.setCursor(QtCore.Qt.ArrowCursor)
                #
                self._set_item_hovered_(False)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_move_started_(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_move_running_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._set_move_stopped_(event)
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_widget_geometry_update_()
        #
        offset = self._get_item_action_offset_()
        #
        if self._item_is_enable is True:
            border_color = [Color.TRANSPARENT, self._hover_frame_border_color][self._item_is_hovered]
            background_color = [Color.TRANSPARENT, self._hover_frame_background_color][self._item_is_hovered]
        else:
            border_color = Color.BUTTON_BORDER_DISABLE
            background_color = Color.BUTTON_BACKGROUND_DISABLE
        #
        painter._set_frame_draw_by_rect_(
            self._frame_rect,
            border_color=border_color,
            background_color=background_color,
            border_radius=1,
            offset=offset
        )

    def _set_widget_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            self._set_frame_rect_(x+1, y, w-3, h)
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            self._set_frame_rect_(x, y+1, w, h-3)

    def _set_contract_l_switch_(self):
        if self._is_contract_r is True:
            self._set_contract_r_switch_()
        else:
            splitter = self.splitter()
            index_l = splitter.indexOf(self)-1
            index_r = splitter.indexOf(self)
            indices = index_l, index_r
            # switch
            self._is_contract_l = not self._is_contract_l
            if self._is_contract_l is True:
                # record size
                self._sizes = splitter._get_sizes_(indices)
                #
                sizes = [0, sum(self._sizes)]
                splitter._set_adjacent_sizes_(indices, sizes, )
            else:
                splitter._set_adjacent_sizes_(indices, self._sizes)
            #
            self._set_contract_buttons_update_()

    def _set_contract_r_switch_(self):
        if self._is_contract_l is True:
            self._set_contract_l_switch_()
        else:
            splitter = self.splitter()
            index_l = splitter.indexOf(self)-1
            index_r = splitter.indexOf(self)
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
        splitter = self.splitter()
        index_l = splitter.indexOf(self) - 1
        index_r = splitter.indexOf(self)
        widgets = splitter._get_widgets_()
        widget_l = splitter._get_widget_(index_l)
        widget_r = splitter._get_widget_(index_r)
        widgets[index_l], widgets[index_r] = widget_r, widget_l
        splitter._set_update_()

    def _set_contract_buttons_update_(self):
        icon_name_l = [self._contract_icon_name_l, self._contract_icon_name_r][self._is_contract_l]
        self._contract_l_button._set_file_icon_path_(utl_core.Icon.get(icon_name_l))
        self._contract_l_button.update()
        icon_name_r = [self._contract_icon_name_r, self._contract_icon_name_l][self._is_contract_r]
        self._contract_r_button._set_file_icon_path_(utl_core.Icon.get(icon_name_r))
        self._contract_r_button.update()

    def _set_update_(self):
        pass

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def splitter(self):
        return self.parent()

    def _set_move_started_(self, event):
        pass

    def _set_move_running_(self, event):
        self._contract_l_button._set_item_action_flag_(self._contract_l_button.PRESS_MOVE_FLAG)
        self._contract_r_button._set_item_action_flag_(self._contract_r_button.PRESS_MOVE_FLAG)
        self._swap_button._set_item_action_flag_(self._swap_button.PRESS_MOVE_FLAG)
        p = event.pos()
        x, y = p.x(), p.y()
        splitter = self.splitter()
        index_l = splitter.indexOf(self) - 1
        index_r = splitter.indexOf(self)
        indices = index_l, index_r
        s_l_o, s_r_o = splitter._get_size_(index_l), splitter._get_size_(index_r)
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            s_l, s_r = s_l_o + x, s_r_o - x
            splitter._set_adjacent_sizes_(indices, [s_l, s_r])
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            s_l, s_r = s_l_o + y, s_r_o - y
            splitter._set_adjacent_sizes_(indices, [s_l, s_r])

    def _set_move_stopped_(self, event):
        self._contract_l_button._set_item_action_flag_clear_()
        self._contract_r_button._set_item_action_flag_clear_()
        self._swap_button._set_item_action_flag_clear_()


class _QtHSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitterHandle, self).__init__(*args, **kwargs)


class _QtVSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitterHandle, self).__init__(*args, **kwargs)
