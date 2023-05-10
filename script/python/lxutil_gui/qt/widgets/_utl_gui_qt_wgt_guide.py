# coding=utf-8
import fnmatch

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_entry, _utl_gui_qt_wgt_popup

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class QtGuideRect(
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtTypeDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtPathDef,
    utl_gui_qt_abstract.AbsQtFrameDef,
    #
    utl_gui_qt_abstract.AbsQtChooseDef,
):
    def _refresh_widget_draw_(self):
        pass

    def __init__(self, *args, **kwargs):
        self._init_icon_def_()
        self._init_type_def_()
        self._init_name_def_()
        self._set_path_def_init_()
        self._set_frame_def_init_()
        self._set_choose_def_init_()
        #
        self._set_icon_file_path_(
            self._choose_collapse_icon_file_path
        )

    def _get_icon_file_path_(self):
        return [
            self._choose_collapse_icon_file_path,
            self._choose_expand_icon_file_path
        ][self._get_choose_is_activated_()]


class QtGuideEntry(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    #
    utl_gui_qt_abstract.AbsQtFocusDef,
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
    #
    utl_gui_qt_abstract.AbsQtGuideEntryDef,
):
    def _refresh_focus_draw_geometry_(self):
        pass

    QT_CHOOSE_RECT_CLS = QtGuideRect
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForGuideChoose
    #
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtConstantEntry
    #
    entry_started = qt_signal()
    # for popup choose
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()
    key_enter_pressed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtGuideEntry, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setFont(Font.title)
        #
        self.setMaximumHeight(22)
        self.setMinimumHeight(22)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        #
        self._init_name_def_()
        self._init_value_entry_def_(self)
        self._init_entry_base_def_(self)
        self._init_focused_def_(self)
        #
        self._choose_item_icon_file_path = utl_core.Icon.get('choose_close')
        #
        self._init_menu_def_()
        #
        self._init_action_hover_def_()
        self._init_action_def_(self)
        self._set_action_press_def_init_()
        #
        self._init_guide_entry_def_(self)

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_guide_draw_geometry_(self):
        side = 2
        spacing = 2
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        frm_w, frm_h = 18, 18
        icn_w, icn_h = 16, 16
        #
        c_x, c_y = x, (h-frm_h)/2
        #
        for i_index in self._get_guide_item_indices_():
            i_item = self._get_guide_item_at_(i_index)
            i_item._set_icon_frame_draw_rect_(
                c_x, c_y, frm_w, frm_h
            )
            i_item._set_icon_file_draw_rect_(
                c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
            )
            c_x += frm_w + spacing
            #
            i_path_key = i_item._type_text
            i_path_value = i_item._name_text
            #
            i_path_w_0, i_path_h_0 = RawTextMtd.get_size(10, i_path_key)
            i_path_w_1, i_path_h_1 = RawTextMtd.get_size(12, i_path_value)
            i_path_w = i_path_w_0 + i_path_w_1 + spacing*8
            i_item._set_name_frame_rect_(
                c_x-spacing*2, c_y, i_path_w, frm_h
            )
            #
            i_path_key_w = i_path_w_0 + spacing*4
            i_item._set_type_rect_(
                c_x, c_y, i_path_key_w, frm_h
            )
            c_x += i_path_key_w
            #
            i_path_value_w = i_path_w_1 + spacing*4
            i_item._set_name_draw_rect_(
                c_x, c_y, i_path_value_w, frm_h
            )
            #
            c_x += i_path_value_w

    def eventFilter(self, *args):
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
                self._update_guide_current_(event)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._update_guide_current_(event)
                    self._restore_guide_choose_()
                    # root
                    # choose
                    if self._guide_choose_index_current is not None:
                        self._set_action_flag_(self.ActionFlag.ChooseClick)
                    # press
                    elif self._guide_index_current is not None:
                        self._set_action_flag_(self.ActionFlag.PressClick)
                    else:
                        self.entry_started.emit()
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
                    # choose
                    if self._get_is_guide_choose_flag_() is True:
                        self._start_guide_choose_item_popup_at_(self._guide_choose_index_current)
                    # press
                    elif self._get_action_press_flag_is_click_() is True:
                        self.guide_user_entry_changed.emit(self._get_guide_path_text_at_(self._guide_index_current))
                        self.guide_press_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._set_action_flag_clear_()
                #
                self._action_is_hovered = False
                self._refresh_widget_draw_()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                if self._guide_index_current is not None:
                    self._execute_action_guide_choose_wheel_(event)
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility.QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility.QtEntryFrame):
                    entry_frame._set_focused_(False)
            #
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Up:
                    self.key_up_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Down:
                    self.key_down_pressed.emit()
                elif event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                    self.key_enter_pressed.emit()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)

        for i_index in self._get_guide_item_indices_():
            i_item = self._get_guide_item_at_(i_index)
            i_icon_offset = 0
            name_offset = 0
            choose_is_hovered = i_index == self._guide_choose_index_current
            guide_is_hovered = i_index == self._guide_index_current
            if i_index == self._guide_choose_index_current:
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
            elif i_index == self._guide_index_current:
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
                font_color=bsc_core.RawTextOpt(i_type_text).to_rgb_0(s_p=100, v_p=100),
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

    def _update_guide_current_(self, event):
        p = event.pos()
        #
        self._clear_guide_choose_current_()
        self._clear_guide_current_()
        # choose or press
        for i_index in self._get_guide_item_indices_():
            i_item = self._get_guide_item_at_(i_index)
            # popup choose
            if i_item._icon_frame_draw_rect.contains(p) is True:
                self._set_guide_choose_current_index_(i_index)
                break
            # execute press
            elif i_item._name_frame_draw_rect.contains(p) is True:
                self._set_guide_current_index_(i_index)
                break
        #
        if self._guide_choose_index_current is not None:
            self._set_tool_tip_text_(
                'LMB-click to popup a choose frame'
            )
        elif self._guide_index_current is not None:
            self._set_tool_tip_text_(
                (
                    '1, LMB-click to jump to current\n'
                    '2, MMB-wheel to jump to previous or next'
                )
            )
        else:
            self.setToolTip('')
        #
        self._refresh_widget_draw_()

    def _execute_action_guide_choose_wheel_(self, event):
        index = self._guide_index_current
        delta = event.angleDelta().y()
        values = self._get_guide_choose_item_values_at_(index)
        pre_value = self._get_guide_name_text_at_(index)
        maximum = len(values)-1
        if pre_value in values:
            pre_index = values.index(pre_value)
            if delta > 0:
                cur_index = pre_index-1
            else:
                cur_index = pre_index+1
            #
            cur_index = max(min(cur_index, maximum), 0)
            if cur_index != pre_index:
                value_cur = values[cur_index]
                self._set_guide_name_text_at_(value_cur, index)
                self.guide_user_entry_changed.emit(self._get_guide_path_text_at_(self._guide_index_current))

    def _get_guide_choose_item_point_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        rect = item._icon_frame_draw_rect
        return self.mapToGlobal(rect.center())

    def _get_guide_choose_item_rect_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        rect = item._icon_frame_draw_rect
        return rect

    def _get_guide_valid_path_texts_(self):
        # todo, fnc "get_is_enable" is from proxy
        return [k for k, v in self._guide_dict.items() if v is None or v.get_is_enable() is True]

    def _get_guide_choose_item_values_(self, item):
        return bsc_core.DccPathDagMtd.get_dag_sibling_names(
            item._path_text, self._get_guide_valid_path_texts_()
        )

    def _get_guide_path_text_(self):
        item = self._get_guide_item_at_(-1)
        if item:
            return item._path_text

    def _set_guide_path_text_(self, path):
        self._restore_guide_()
        #
        path_opt = bsc_core.DccPathDagOpt(path)
        components = path_opt.get_components()
        if components:
            components.reverse()
            for i_index, i_path_opt in enumerate(components[1:]):
                i_item = self._create_guide_item_()
                #
                i_type_text = self._guide_type_texts[i_index]
                i_path_text = i_path_opt.get_path()
                i_name_text = i_path_opt.get_name()
                #
                i_item._set_type_text_(i_type_text)
                i_item._set_path_text_(i_path_text)
                i_item._set_name_text_(i_name_text)
        #
        self._refresh_guide_draw_geometry_()
        self._refresh_widget_draw_()


class QtGuideBar(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    utl_gui_qt_abstract.AbsQtCompletionAsPopupDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry.QtConstantEntry
    QT_POPUP_COMPLETION_CLASS = _utl_gui_qt_wgt_popup.QtPopupForCompletion

    QT_POPUP_PROXY_CLS = _utl_gui_qt_wgt_popup.QtPopupProxy

    FILTER_MAXIMUM = 50
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtGuideBar, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self._init_value_entry_def_(self)
        self._init_completion_as_popup_def_(self)

        self._guide_entry_mode = 0

        qt_layout_0 = QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self._value_entry_frame = _utl_gui_qt_wgt_utility.QtEntryFrame()
        qt_layout_0.addWidget(self._value_entry_frame)
        #
        self._value_entry_frame.setMinimumHeight(24)
        self._value_entry_frame.setMaximumHeight(24)

        self._value_entry_layout = QtHBoxLayout(self._value_entry_frame)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(2)

        self._guide_tree = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._value_entry_layout.addWidget(self._guide_tree)
        self._guide_tree._set_icon_file_path_(utl_gui_core.RscIconFile.get('tree'))

        self._guide_entry = QtGuideEntry()
        self._value_entry_layout.addWidget(self._guide_entry)

        self._guide_entry.entry_started.connect(
            self._guide_entry_started_cbk_
        )
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry.hide()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry.key_escape_pressed.connect(self._guide_entry_finished_cbk_)
        self._value_entry.focus_out.connect(self._set_guide_entry_finish_)
        self._value_entry.setMinimumHeight(22)
        self._value_entry.setMaximumHeight(22)
        self._value_entry.setFont(get_font(size=10))
        #
        self._build_popup_completion_(self._value_entry, self._value_entry_frame)

        self._set_popup_completion_gain_fnc_(
            self._guide_value_popup_completion_gain_fnc_
        )
        self.completion_finished.connect(self._guide_entry_cbk_)

    def _guide_entry_started_cbk_(self):
        self._guide_entry_mode = 1
        self._guide_entry.hide()
        self._value_entry.show()
        self._value_entry._set_value_(self._guide_entry._get_guide_path_text_())
        self._value_entry._set_focused_(True)
        self._value_entry._set_all_selected_()

    def _set_guide_entry_finish_(self):
        self._guide_entry_mode = 0
        self._value_entry.hide()
        self._guide_entry.show()

    def _guide_entry_finished_cbk_(self):
        self._set_guide_entry_finish_()
        self._guide_entry._set_focused_(True)

    def _guide_value_popup_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            texts = self._guide_entry._get_guide_valid_path_texts_()
            _ = fnmatch.filter(
                texts, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.set_sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def _guide_entry_cbk_(self):
        text = self._value_entry._get_value_()
        if text:
            texts = self._guide_entry._get_guide_valid_path_texts_()
            if text in texts:
                path_text_pre = self._guide_entry._get_guide_path_text_()
                if text != path_text_pre:
                    self._guide_entry._set_guide_path_text_(text)
                    self._guide_entry.guide_user_entry_changed.emit(
                        text
                    )
                self._guide_entry_finished_cbk_()