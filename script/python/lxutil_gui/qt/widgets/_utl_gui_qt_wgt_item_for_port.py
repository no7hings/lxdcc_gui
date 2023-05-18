# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_entry_base, _utl_gui_qt_wgt_popup

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class QtValueEntryAsTextEdit(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsTextEdit, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_extra_def_(self)
        self._set_value_default_def_init_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._build_value_entry_(self._value_type)

    def _build_value_entry_(self, value_type):
        self._value_type = value_type
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(self._value_type)

    def _set_value_entry_validator_use_as_name_(self):
        self._value_entry._set_validator_use_as_name_()

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsTextEdit, self)._set_value_entry_enable_(boolean)

        self._value_entry.setReadOnly(not boolean)

        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dim
        ][boolean]
        self._refresh_widget_draw_()


class QtValueEntryAsContentEdit(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry_base.QtEntryAsContentEdit
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsContentEdit, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_extra_def_(self)
        self._set_value_default_def_init_()
        #
        self._build_value_entry_(self._value_type)

        # self._frame_background_color = QtBackgroundColors.Dark

    def _build_value_entry_(self, value_type):
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
        super(QtValueEntryAsContentEdit, self)._set_value_entry_enable_(boolean)

        self._value_entry.setReadOnly(not boolean)
        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dim
        ][boolean]
        self._refresh_widget_draw_()


class QtValueEntryAsTupleByChoose(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtRgbaDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit
    #
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForRgbaChoose
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsTupleByChoose, self).__init__(*args, **kwargs)
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
        self._init_value_entry_extra_def_(self)
        self._set_value_default_def_init_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(20, 0, 0, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._build_value_entry_(self._value_type)

    def _build_value_entry_(self, value_type):
        self._value_type = value_type
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(self._value_type)

    def _refresh_widget_draw_geometry_(self):
        super(QtValueEntryAsTupleByChoose, self)._refresh_widget_draw_geometry_()
        #
        x, y = 0, 0
        w, h = 20, self.height()
        c_w, c_h = 16, 16
        self._color_rect.setRect(
            x+2, y+(h-c_h)/2, c_w, c_h
        )

    def eventFilter(self, *args):
        super(QtValueEntryAsTupleByChoose, self).eventFilter(*args)
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
        super(QtValueEntryAsTupleByChoose, self).paintEvent(self)
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


class QtValueEntryAsTextEditByChoose(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForEntryDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryAsPopupChoose,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
    #
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtChooseExtraDef,
    utl_gui_qt_abstract.AbsQtCompletionExtraDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit
    #
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForChoose
    QT_POPUP_COMPLETION_CLASS = _utl_gui_qt_wgt_popup.QtPopupForCompletion
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
        super(QtValueEntryAsTextEditByChoose, self).__init__(*args, **kwargs)
        self._init_action_base_def_(self)
        self._init_set_action_for_entry_def_(self)
        #
        self._set_value_entry_enumerate_init_(self)
        self._set_value_default_def_init_()
        #
        self._init_choose_base_def_()
        self._init_choose_extra_def_(self)
        self._init_completion_extra_def_(self)
        #
        self._build_value_entry_(self._value_type)
        #
        self.installEventFilter(self)

    def eventFilter(self, *args):
        super(QtValueEntryAsTextEditByChoose, self).eventFilter(*args)
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

    def _build_value_entry_(self, value_type):
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
        self._value_choose_button.press_clicked.connect(self._start_choose_extra_fnc_)
        #
        self._build_choose_extra_(self._value_entry, self)
        # choose
        self.user_choose_finished.connect(self.choose_changed.emit)
        self.user_choose_finished.connect(self.user_choose_changed.emit)
        self.user_choose_text_accepted.connect(self._set_value_)
        # completion
        self._build_completion_extra_(self._value_entry, self)
        self.user_completion_text_accepted.connect(self._set_value_)

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsTextEditByChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._value_choose_button.setHidden(not boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_()

    def _set_value_entry_drop_enable_(self, boolean):
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
        super(QtValueEntryAsTextEditByChoose, self)._set_choose_values_(values, *args, **kwargs)
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

    def _set_choose_tag_filter_size_(self, w, h):
        pass

    def _set_value_clear_(self):
        self._choose_values = []
        self._value_entry._set_value_clear_()


class QtValueEntryAsCapsule(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
    utl_gui_qt_abstract.AbsQtNameBaseDef,
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
        self._init_name_base_def_(self)
        self._init_frame_base_def_(self)

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
    # noinspection PyUnusedLocal
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


class QtValueEntryAsTextEdits(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryAsTupleExtraDef,
):
    """
    use for multiply texts (str, int, float) entry, etc. float3, integer3
    """
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsTextEdits, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_as_tuple_def_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(8)
        #
        self._build_value_entry_(2, self._value_type)

    def _build_value_entry_(self, value_size, value_type):
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
                i_widget = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit()
                i_widget._set_value_type_(self._value_type)
                self._value_entry_layout.addWidget(i_widget)
                self._value_entries.append(i_widget)

    def _set_value_entry_enable_(self, boolean):
        pass


class QtValueEntryAsList(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtChooseExtraDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry_base.QtEntryAsList
    #
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForChoose
    #
    add_press_clicked = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsList, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_name_base_def_(self)
        self._init_value_entry_extra_def_(self)
        self._init_choose_base_def_()
        self._init_choose_extra_def_(self)
        #
        self._build_value_entry_(str)
        self._set_choose_extra_multiply_enable_(True)

    def _build_value_entry_(self, value_type):
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
        self._value_choose_button.press_clicked.connect(self._start_choose_extra_fnc_)
        # choose
        self._build_choose_extra_(self._value_entry, self)
        self.user_choose_finished.connect(self.choose_changed.emit)
        self.user_choose_finished.connect(self.user_choose_changed.emit)
        self.user_choose_texts_accepted.connect(self._extend_choose_current_values_)
        #
        self._resize_handle.raise_()

    def _get_value_entry_gui_(self):
        return self._value_entry

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsList, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)

    def _set_value_entry_choose_enable_(self, boolean):
        self._value_choose_button._set_action_enable_(boolean)

    def _set_value_entry_choose_visible_(self, boolean):
        self._value_choose_button._set_visible_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _append_value_(self, value):
        self._value_entry._append_value_(value)

    def _extend_values_(self, values):
        self._value_entry._extend_values_(values)

    def _set_values_(self, values):
        self._value_entry._set_values_(values)

    def _get_values_(self):
        return self._value_entry._get_values_()

    def _clear_all_values_(self):
        self._value_entry._clear_all_values_()

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
    # choose
    def _extend_choose_current_values_(self, values):
        self._extend_values_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()

    def _set_empty_icon_name_(self, text):
        self._value_entry._set_empty_icon_name_(text)


class QtValueEntryAsListWithChoose(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtChooseExtraDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_entry_base.QtEntryAsList
    QT_POPUP_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForChoose
    #
    add_press_clicked = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsListWithChoose, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_name_base_def_(self)
        self._init_value_entry_extra_def_(self)
        self._init_choose_base_def_()
        self._init_choose_extra_def_(self)
        #
        self._build_value_entry_(str)
        self._set_choose_extra_multiply_enable_(True)

    def _build_value_entry_(self, value_type):
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
        self._value_choose_button.press_clicked.connect(self._start_choose_extra_fnc_)
        # choose
        self._build_choose_extra_(self._value_entry, self)
        self.user_choose_finished.connect(self.choose_changed.emit)
        self.user_choose_finished.connect(self.user_choose_changed.emit)
        self.user_choose_texts_accepted.connect(self._extend_choose_current_values_)
        #
        self._resize_handle.raise_()

    def _get_value_entry_gui_(self):
        return self._value_entry
    #
    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsListWithChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()
    # drop
    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)

    def _set_value_entry_choose_enable_(self, boolean):
        self._value_choose_button._set_action_enable_(boolean)

    def _set_value_entry_choose_visible_(self, boolean):
        self._value_choose_button._set_visible_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _append_value_(self, value):
        self._value_entry._append_value_(value)

    def _extend_values_(self, values):
        self._value_entry._extend_values_(values)

    def _set_values_(self, values):
        self._value_entry._set_values_(values)

    def _get_values_(self):
        return self._value_entry._get_values_()

    def _clear_all_values_(self):
        self._value_entry._clear_all_values_()

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
    # choose
    def _extend_choose_current_values_(self, values):
        self._extend_values_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()


class QtValueEntryAsBubblesByChoose(
    _utl_gui_qt_wgt_entry_base.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtChooseExtraDef,
):
    def __init__(self, *args, **kwargs):
        #
        self._init_name_base_def_(self)
        self._init_value_entry_extra_def_(self)
        self._init_choose_base_def_()
        self._init_choose_extra_def_(self)
        #
        self._build_value_entry_(str)
        self._set_choose_extra_multiply_enable_(True)
