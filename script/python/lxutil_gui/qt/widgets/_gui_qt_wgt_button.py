# coding=utf-8
from lxutil_gui.qt.gui_qt_core import *

import lxutil_gui.qt.abstracts as gui_qt_abstract

from lxutil_gui import gui_core

from lxutil_gui.qt.widgets import _gui_qt_wgt_utility, _gui_qt_wgt_drag


class QtIconPressButton(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtNameBaseDef,
    gui_qt_abstract.AbsQtPathBaseDef,
    gui_qt_abstract.AbsQtIconBaseDef,
    gui_qt_abstract.AbsQtMenuBaseDef,
    #
    gui_qt_abstract.AbsQtStatusBaseDef,
    gui_qt_abstract.AbsQtStateDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,
    gui_qt_abstract.AbsQtActionForDragDef,
    #
    gui_qt_abstract.AbsQtThreadBaseDef,
    #
    gui_qt_abstract.AbsQtItemLayoutBaseDef,
):
    clicked = qt_signal()
    press_db_clicked = qt_signal()
    #
    QT_MENU_CLS = _gui_qt_wgt_utility.QtMenu

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        if self._icon_geometry_mode == self.IconGeometryMode.Square:
            icn_frm_w = icn_frm_h = w
        elif self._icon_geometry_mode == self.IconGeometryMode.Auto:
            icn_frm_w, icn_frm_h = w, h
        else:
            raise RuntimeError()
        #
        self._frame_draw_rect.setRect(
            x, y, w-1, h-1
        )
        #
        icn_w, icn_h = int(icn_frm_w*self._icon_draw_percent), int(icn_frm_h*self._icon_draw_percent)
        icn_x, icn_y = x+(icn_frm_w-icn_w)/2, y+(icn_frm_h-icn_h)/2
        #
        if self._icon_is_enable is True:
            # sub icon
            if self._icon_sub_file_path or self._icon_sub_text or self._icon_state_draw_is_enable:
                if self._icon_state_draw_is_enable is True:
                    icn_s_p = self._icon_sub_draw_percent
                    icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                    o_x, o_y = icn_x, icn_y
                    self._icon_draw_rect.setRect(
                        x+1, y+1, icn_w, icn_h
                    )
                    icn_s_w, icn_s_h = min(icn_s_w, 16), min(icn_s_h, 16)
                    self._icon_sub_draw_rect.setRect(
                        x+icn_frm_w-icn_s_w-1-o_x, y+icn_frm_h-icn_s_h-1-o_y, icn_s_w, icn_s_h
                    )
                    icn_sst_p = self._icon_state_draw_percent
                    icn_stt_w, icn_stt_h = icn_frm_w*icn_sst_p, icn_frm_h*icn_sst_p
                    #
                    self._icon_state_rect.setRect(
                        x+icn_frm_w-icn_stt_w-1, y+icn_frm_h-icn_stt_h-1, icn_stt_w, icn_stt_h
                    )
                    icn_stt_w, icn_stt_h = min(icn_stt_w, 8), min(icn_stt_h, 8)
                    self._icon_state_draw_rect.setRect(
                        x+icn_frm_w-icn_stt_w-1, y+icn_frm_h-icn_stt_h-1, icn_stt_w, icn_stt_h
                    )
                else:
                    icn_s_p = self._icon_sub_draw_percent
                    icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                    icn_s_w, icn_s_h = min(icn_s_w, 16), min(icn_s_h, 16)
                    self._icon_draw_rect.setRect(
                        icn_x, icn_y, icn_w, icn_h
                    )
                    self._icon_sub_draw_rect.setRect(
                        x+icn_frm_w-icn_s_w-1, y+icn_frm_h-icn_s_h-1, icn_s_w, icn_s_h
                    )
            else:
                self._icon_draw_rect.setRect(
                    icn_x, icn_y, icn_w, icn_h
                )

        self._name_draw_rect.setRect(
            x, y+icn_frm_h, w, h-icn_frm_w
        )

        s_w, s_h = w*.5, w*.5
        self._action_state_rect.setRect(
            x, y+h-s_h, s_w, s_h
        )

    def __init__(self, *args, **kwargs):
        super(QtIconPressButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(Font.NAME)
        self.setFixedSize(20, 20)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_path_base_def_(self)
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_menu_base_def_(self)
        self._init_status_base_def_(self)
        self._set_state_def_init_()
        #
        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_drag_def_(self)
        self._init_thread_base_def_(self)
        #
        self._init_item_layout_base_def_(self)
        #
        self._choose_enable = False
        self._choose_args = []

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                self._execute_action_hover_by_filter_(event)
                #
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    self._press_point = event.pos()
                    if event.button() == QtCore.Qt.LeftButton:
                        if self._choose_enable is True:
                            pass
                        self.pressed.emit()
                        self._set_action_flag_(self.ActionFlag.Press)
                    elif event.button() == QtCore.Qt.RightButton:
                        self._popup_menu_()
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_action_flag_(self.ActionFlag.PressDbClick)
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if event.button() == QtCore.Qt.LeftButton:
                        if self._get_action_flag_is_match_(self.ActionFlag.PressDbClick):
                            self.press_db_clicked.emit()
                        elif self._get_action_flag_is_match_(self.ActionFlag.Press):
                            p = event.pos()
                            if self._icon_state_draw_is_enable:
                                if self._icon_state_rect.contains(p):
                                    self._popup_menu_()
                                else:
                                    self.press_clicked.emit()
                            else:
                                self.press_clicked.emit()
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                    #
                    self._set_action_hovered_(False)
                    self._clear_all_action_flags_()
                # drag move
                elif event.type() == QtCore.QEvent.MouseMove:
                    if event.buttons() == QtCore.Qt.LeftButton:
                        if self._drag_is_enable is True:
                            if self._get_action_flag_is_match_(self.ActionFlag.Press):
                                self._drag_press_point = self._press_point
                                self._set_action_flag_(self.ActionFlag.DragPress)
                            elif self._get_action_flag_is_match_(self.ActionFlag.DragPress):
                                self._do_drag_press_(event)
                            elif self._get_action_flag_is_match_(self.ActionFlag.DragMove):
                                self._do_drag_move_(event)
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        self._refresh_widget_draw_geometry_()
        offset = self._get_action_offset_()
        if self._get_action_flag_is_match_(self.ActionFlag.DragMove):
            painter._draw_frame_by_rect_(
                    rect=self._frame_draw_rect,
                    border_color=QtBorderColors.Button,
                    background_color=QtBackgroundColors.ItemSelected,
                )

        if self._thread_draw_is_enable is True:
            painter._draw_alternating_colors_by_rect_(
                rect=self._frame_draw_rect,
                colors=((0, 0, 0, 63), (0, 0, 0, 0)),
                # border_radius=4,
                running=True
            )
        # icon
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered,
                    is_pressed=self._is_pressed
                )
            elif self._icon_name_text is not None:
                painter._draw_image_use_text_by_rect_(
                    rect=self._icon_draw_rect,
                    text=self._icon_name_text,
                    background_color=self._icon_name_rgba,
                    offset=offset,
                    border_radius=2,
                    is_hovered=self._is_hovered,
                    is_pressed=self._is_pressed
                )
            #
            if self._icon_sub_file_path:
                painter._draw_image_use_file_path_by_rect_(
                    rect=self._icon_sub_draw_rect,
                    file_path=self._icon_sub_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered,
                    #
                    draw_frame=True,
                    background_color=QtBorderColors.Icon,
                    border_color=QtBorderColors.Icon,
                    border_radius=4
                )
            #
            if self._icon_state_draw_is_enable is True:
                if self._icon_state_file_path is not None:
                    painter._draw_icon_file_by_rect_(
                        rect=self._icon_state_draw_rect,
                        file_path=self._icon_state_file_path,
                        offset=offset,
                        is_hovered=self._is_hovered
                    )
        #
        if self._action_state in [self.ActionState.Disable]:
            painter._draw_icon_file_by_rect_(
                self._action_state_rect,
                gui_core.RscIconFile.get('state-disable')
            )
        #
        if self._name_text:
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=self._name_text,
                font=get_font(),
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop,
                word_warp=self._name_word_warp,
                offset=offset,
                # is_hovered=self._is_hovered,
            )

    def _do_drag_press_(self, event):
        p = event.pos()
        p_d = p-self._drag_press_point
        x, y = p_d.x(), p_d.y()
        # enable when mouse moved more than 10 pixel
        if abs(x) > 10 or abs(y) > 10:
            self._set_action_flag_(self.ActionFlag.DragMove)

    def _do_drag_move_(self, event):
        self.__drag = _gui_qt_wgt_drag.QtWidgetDrag(self)

        item = self._get_layout_item_()
        if item is not None:
            key = item.get_drag_and_drop_key()
            self._set_drag_data_(
                {
                    'lynxi/drag-and-drop-key': key,
                    'lynxi/drag-and-drop-scheme': self._get_drag_and_drop_scheme_()
                }
            )
            item.start_drag_and_drop(self._get_drag_and_drop_scheme_())

            self.__drag.setMimeData(self._generate_drag_mime_data_())

            self.__drag._do_drag_move_(self._drag_press_point)

            self.__drag.released.connect(self._drag_release_cbk_)

            self._refresh_widget_draw_()

    def _drag_release_cbk_(self):
        self._clear_all_action_flags_()
        l_i = self._get_layout_item_()
        if l_i is not None:
            l_i.get_layout_view()._drag_release_cbk_()

    def _set_visible_(self, boolean):
        self.setVisible(boolean)

    def _execute_choose_start_(self):
        pass

    def _set_menu_data_(self, data):
        super(QtIconPressButton, self)._set_menu_data_(data)
        #
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = gui_core.RscIconFile.get(
            'state/popup'
        )

    def _set_menu_data_gain_fnc_(self, fnc):
        super(QtIconPressButton, self)._set_menu_data_gain_fnc_(fnc)
        #
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = gui_core.RscIconFile.get(
            'state/popup'
        )


class QtIconMenuButton(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtIconBaseDef,
    gui_qt_abstract.AbsQtNameBaseDef,
    gui_qt_abstract.AbsQtMenuBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,
):
    QT_MENU_CLS = _gui_qt_wgt_utility.QtMenu

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        icn_frm_w, icn_frm_h = w, h
        #
        icn_w, icn_h = int(icn_frm_w*self._icon_draw_percent), int(icn_frm_h*self._icon_draw_percent)
        icn_x, icn_y = x+(w-icn_w)/2, y+(h-icn_h)/2
        #
        if self._icon_is_enable is True:
            self._icon_draw_rect.setRect(
                icn_x, icn_y, icn_w, icn_h
            )

    def __init__(self, *args, **kwargs):
        super(QtIconMenuButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(Font.NAME)
        self.setFixedSize(20, 20)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_menu_base_def_(self)
        #
        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                self._execute_action_hover_by_filter_(event)
                #
                if event.type() == QtCore.QEvent.Resize:
                    self._refresh_widget_draw_geometry_()
                elif event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                    self._set_action_flag_(self.ActionFlag.Press)
                    self._refresh_widget_all_()
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if self._get_action_flag_is_match_(self.ActionFlag.Press):
                        self._popup_menu_()
                    self._clear_all_action_flags_()
                    self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        offset = self._get_action_offset_()
        # icon
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered,
                    is_pressed=self._is_pressed
                )


class QtIconEnableButton(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtWidgetBaseDef,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtIconBaseDef,
    gui_qt_abstract.AbsQtNameBaseDef,
    gui_qt_abstract.AbsQtMenuBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtCheckBaseDef,
    #
    gui_qt_abstract.AbsQtValueDefaultBaseDef,
):
    QT_MENU_CLS = _gui_qt_wgt_utility.QtMenu

    def __init__(self, *args, **kwargs):
        super(QtIconEnableButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        self.setFont(Font.NAME)
        #
        self.setFixedSize(20, 20)
        #
        self.installEventFilter(self)
        #
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_widget_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_name_base_def_(self)
        self._init_menu_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_check_base_def_(self)
        self._set_check_enable_(True)
        #
        self._init_value_default_base_def_()
        #
        self._refresh_check_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        r = min(w, h)
        icn_frm_w = icn_frm_h = min(w, h)-2
        icn_p = self._icon_draw_percent
        icn_w = icn_h = r*icn_p
        #
        self._frame_draw_rect.setRect(
            x, y, w-1, h-1
        )
        self._check_rect.setRect(
            x+(w-icn_frm_w)/2, y+(h-icn_frm_w)/2, icn_frm_w, icn_frm_h
        )
        #
        if self._icon_is_enable is True:
            if self._icon_sub_file_path or self._icon_sub_text:
                self._icon_draw_rect.setRect(
                    x+2, y+2, icn_w, icn_h
                )
                #
                icn_s_p = self._icon_sub_draw_percent
                icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                self._icon_sub_draw_rect.setRect(
                    x+w-icn_s_w-1, y+h-icn_s_h-1, icn_s_w, icn_s_h
                )
            # state
            elif self._icon_state_draw_is_enable is True:
                icn_s_p = self._icon_state_draw_percent
                icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                self._icon_state_draw_rect.setRect(
                    x+w-icn_s_w-1, y+h-icn_s_h-1, icn_s_w, icn_s_h
                )
                self._icon_draw_rect.setRect(
                    x+2, y+2, w-icn_s_w, h-icn_s_h
                )
            else:
                self._set_icon_file_draw_rect_(
                    x+(w-icn_w)/2, y+(h-icn_h)/2, icn_w, icn_h
                )
        #
        x += icn_frm_w+spacing
        self._set_name_draw_rect_(
            x, y, w-x, h
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckPress)
                elif event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckPress:
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
        #
        background_color = painter._get_item_background_color_by_rect_(
            self._check_rect,
            is_hovered=self._is_hovered,
            is_selected=self._is_checked,
            is_actioned=self._get_is_actioned_()
        )
        painter._draw_frame_by_rect_(
            self._check_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            border_radius=2,
            offset=offset
        )
        #
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered
                )
                if self._icon_sub_text:
                    painter._draw_image_use_text_by_rect_(
                        rect=self._icon_sub_draw_rect,
                        text=self._icon_sub_text,
                        border_radius=4,
                        offset=offset
                    )
                elif self._icon_sub_file_path:
                    painter._draw_icon_file_by_rect_(
                        rect=self._icon_sub_draw_rect,
                        file_path=self._icon_sub_file_path,
                        offset=offset,
                        is_hovered=self._is_hovered
                    )
                elif self._icon_state_draw_is_enable is True:
                    if self._icon_state_file_path is not None:
                        painter._draw_icon_file_by_rect_(
                            rect=self._icon_state_draw_rect,
                            file_path=self._icon_state_file_path,
                            offset=offset,
                            is_hovered=self._is_hovered
                        )
        #
        if self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=Font.NAME,
                font_color=QtFontColors.Basic,
                text_option=QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,
                offset=offset
            )

    def _get_value_(self):
        return self._get_is_checked_()

    def _set_menu_data_(self, data):
        super(QtIconEnableButton, self)._set_menu_data_(data)
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = gui_core.RscIconFile.get(
            'state/popup'
        )

    def _set_menu_data_gain_fnc_(self, fnc):
        super(QtIconEnableButton, self)._set_menu_data_gain_fnc_(fnc)
        #
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = gui_core.RscIconFile.get(
            'state/popup'
        )