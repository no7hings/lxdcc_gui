# coding=utf-8
from lxutil_gui.qt.gui_qt_core import *

from lxutil_gui import gui_configure

from lxutil_gui.qt.widgets import _gui_qt_wgt_utility, _gui_qt_wgt_button, _gui_qt_wgt_entry_base, _gui_qt_wgt_popup

import lxutil_gui.qt.abstracts as gui_qt_abstract


# any constant, etc. integer, float, string/text/name, ...
class QtValueEntryAsConstant(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtValueEntryBaseDef,
    gui_qt_abstract.AbsQtValueDefaultBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsTextEdit

    entry_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsConstant, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_base_def_(self)
        self._init_value_default_base_def_()
        #
        self._build_value_entry_(self._value_type)

    def _build_value_entry_(self, value_type):
        self._value_type = value_type
        #
        entry_layout = QtHBoxLayout(self)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(4)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        entry_layout.addWidget(self._value_entry)
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


# any content, etc. script, xml, doc
class QtValueEntryAsContentEdit(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtValueEntryBaseDef,
    gui_qt_abstract.AbsQtValueDefaultBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsContentEdit

    entry_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsContentEdit, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_base_def_(self)
        self._init_value_default_base_def_()
        #
        self._external_editor_ext = '.txt'
        #
        self._external_editor_is_enable = False
        self._external_editor_file_path = None
        #
        self._build_value_entry_(self._value_type)

        # self._frame_background_color = QtBackgroundColors.Dark

    def _build_value_entry_(self, value_type):
        self._value_type = value_type
        #
        main_layout = QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #
        entry_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        self._value_entry._set_entry_frame_(self)
        # self._value_entry.setReadOnly(False)
        entry_layout.addWidget(self._value_entry)
        #
        self._button_widget = _gui_qt_wgt_utility.QtLineWidget()
        self._button_widget.hide()
        self._button_widget._set_line_styles_(
            [self._button_widget.Style.Null, self._button_widget.Style.Null, self._button_widget.Style.Solid,
             self._button_widget.Style.Null]
        )
        entry_layout.addWidget(self._button_widget)
        self._button_layout = QtVBoxLayout(self._button_widget)
        self._button_layout._set_align_top_()
        self._button_layout.setContentsMargins(2, 0, 0, 0)
        self._button_layout.setSpacing(2)
        #
        self._open_in_external_editor_button = _gui_qt_wgt_button.QtIconEnableButton()
        self._button_layout.addWidget(self._open_in_external_editor_button)
        self._open_in_external_editor_button._set_icon_file_path_(
            gui_core.RscIconFile.get('application/sublime-text')
            )
        self._open_in_external_editor_button._set_name_text_('open in external editor')
        self._open_in_external_editor_button._set_tool_tip_('"LMB-click" to open in external editor')
        self._open_in_external_editor_button.check_toggled.connect(self._start_open_in_external_editor_fnc_)
        #
        self._value_entry.focus_in.connect(
            self._update_from_external_editor_fnc_
        )
        #
        self._resize_handle.raise_()

    def _get_tmp_text_file_path_(self):
        return six.u('{}/editor/untitled-{}{}').format(
            bsc_core.SystemMtd.get_home_directory(),
            bsc_core.TimeExtraMtd.get_time_tag_36(),
            self._external_editor_ext
        )

    def _set_external_editor_ext_(self, ext):
        self._external_editor_ext = ext

    def _update_from_external_editor_fnc_(self):
        if self._external_editor_is_enable is True:
            text = bsc_core.StgFileOpt(self._external_editor_file_path).set_read()
            self._value_entry._set_value_(text)

    def _start_open_in_external_editor_fnc_(self, boolean):
        if boolean is True:
            self._external_editor_is_enable = True
            self._external_editor_file_path = self._get_tmp_text_file_path_()
            text = self._value_entry._get_value_()
            bsc_core.StgFileOpt(self._external_editor_file_path).set_write(
                text
            )
            import lxbasic.extra.methods as bsc_etr_methods

            bsc_etr_methods.EtrBase.open_ide(self._external_editor_file_path)
        else:
            self._external_editor_is_enable = False
            if self._external_editor_file_path:
                text = bsc_core.StgFileOpt(self._external_editor_file_path).set_read()
                self._value_entry._set_value_(text)

    def _set_item_value_entry_enable_(self, boolean):
        self._value_entry._set_entry_enable_(not boolean)
        if boolean is True:
            self._button_widget.show()
        else:
            self._button_widget.hide()

    def _set_resize_enable_(self, boolean):
        self._resize_handle.setVisible(boolean)

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsContentEdit, self)._set_value_entry_enable_(boolean)

        self._value_entry.setReadOnly(not boolean)
        # self._frame_background_color = [
        #     QtBackgroundColors.Basic, QtBackgroundColors.Dim
        # ][boolean]
        # self._refresh_widget_draw_()

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)
        self._frame_border_draw_style = QtCore.Qt.DashLine

    def _set_empty_text_(self, text):
        self._value_entry._set_empty_text_(text)


# any constant entry and choose, etc. enumerate, file open/save, directory open/save, ...
class QtValueEntryAsConstantChoose(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtValueEntryBaseDef,
    gui_qt_abstract.AbsQtValueDefaultBaseDef,

    gui_qt_abstract.AbsQtChooseBaseDef,
    gui_qt_abstract.AbsQtChooseAsPopupBaseDef,

    gui_qt_abstract.AbsQtCompletionAsPopupBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsTextEdit

    QT_POPUP_CHOOSE_CLS = _gui_qt_wgt_popup.QtPopupAsAnyChoose
    QT_POPUP_COMPLETION_CLS = _gui_qt_wgt_popup.QtPopupAsCompletion

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_choose_index_()
        self._refresh_widget_draw_()

    def _refresh_choose_index_(self):
        self._value_index_label.hide()
        if self._choose_index_show_enable is True:
            if self._value_entry_is_enable is True:
                values = self._get_choose_values_()
                if values:
                    self._value_index_label.show()
                    maximum = len(values)
                    value_cur = self._get_value_()
                    if value_cur in values:
                        index_cur = values.index(value_cur)+1
                        text = '{}/{}'.format(index_cur, maximum)
                    else:
                        text = str(maximum)
                    #
                    self._value_index_label._set_name_text_(text)
                    width = self._value_index_label._get_name_text_draw_width_(text)
                    self._value_index_label.setMinimumWidth(width+4)

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsConstantChoose, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_base_def_(self)
        self._init_value_default_base_def_()
        #
        self._init_choose_base_def_()
        self._init_choose_as_popup_base_def_(self)
        self._init_completion_as_popup_base_def_(self)
        #
        self._build_value_entry_(self._value_type)
        #
        self.installEventFilter(self)

    def eventFilter(self, *args):
        super(QtValueEntryAsConstantChoose, self).eventFilter(*args)
        #
        widget, event = args
        if widget == self:
            if hasattr(self, '_action_is_enable') is True:
                if self._action_is_enable is True:
                    if event.type() == QtCore.QEvent.Wheel:
                        self._do_wheel_(event)
                        return True
        return False

    def _do_wheel_(self, event):
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
            #
            cur_index = max(min(cur_index, maximum), 0)
            if cur_index != pre_index:
                self._set_value_(values[cur_index])
                # set value before
                self.choose_changed.emit()
                self.user_choose_changed.emit()
                event.accept()

    def _build_value_entry_(self, value_type):
        self._value_type = value_type
        #
        main_layout = QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        entry_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        # entry
        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        entry_layout.addWidget(self._value_entry)
        self._value_entry._set_entry_frame_(self)
        self._value_entry._set_value_type_(self._value_type)
        self._value_entry._set_entry_enable_(False)
        #   connect tab key
        self._value_entry.user_key_tab_pressed.connect(
            self.user_key_tab_pressed.emit
        )
        #
        self._value_index_label = _gui_qt_wgt_utility.QtTextItem()
        self._value_index_label.hide()
        entry_layout.addWidget(self._value_index_label)
        self._value_index_label._set_name_color_(QtFontColors.Disable)
        self._value_index_label.hide()
        #
        self._button_widget = _gui_qt_wgt_utility.QtLineWidget()
        self._button_widget._set_line_styles_(
            [self._button_widget.Style.Null, self._button_widget.Style.Null, self._button_widget.Style.Solid,
             self._button_widget.Style.Null]
        )
        entry_layout.addWidget(self._button_widget)
        self._button_layout = QtHBoxLayout(self._button_widget)
        self._button_layout.setContentsMargins(2, 0, 0, 0)
        self._button_layout.setSpacing(2)
        #
        self._value_add_button = _gui_qt_wgt_button.QtIconPressButton()
        self._value_add_button.hide()
        self._button_layout.addWidget(self._value_add_button)
        self._value_add_button._set_icon_file_path_(gui_core.RscIconFile.get('file/file'))
        self._value_add_button._set_icon_frame_draw_size_(18, 18)
        #
        self._value_choose_button = _gui_qt_wgt_button.QtIconPressButton()
        self._button_layout.addWidget(self._value_choose_button)
        self._value_choose_button._set_icon_file_path_(gui_core.RscIconFile.get('down'))
        self._value_choose_button._set_icon_frame_draw_size_(18, 18)
        self._value_choose_button._set_name_text_('choose value')
        self._value_choose_button._set_tool_tip_('"LMB-click" to choose value from popup view')
        self._value_choose_button.press_clicked.connect(self._do_popup_choose_start_)
        #
        self._build_popup_choose_(self._value_entry, self)
        # choose
        self.user_choose_finished.connect(self.choose_changed.emit)
        self.user_choose_finished.connect(self.user_choose_changed.emit)
        self.user_choose_text_accepted.connect(self._set_value_)
        # completion
        self._build_popup_completion_(self._value_entry, self)
        self.user_completion_text_accepted.connect(self._set_value_)
        #
        self._set_popup_completion_gain_fnc_(
            self._choose_value_completion_gain_fnc_
        )

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsConstantChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._value_choose_button.setHidden(not boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_all_()

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)

    def _set_value_validation_fnc_(self, fnc):
        self._value_entry._set_value_validation_fnc_(fnc)

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry._set_use_as_storage_(boolean)

    def _set_value_entry_finished_connect_to_(self, fnc):
        self._value_entry.user_entry_finished.connect(fnc)

    def _set_value_entry_changed_connect_to_(self, fnc):
        self._value_entry.entry_changed.connect(fnc)

    def _set_value_choose_button_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_file_path_(file_path)

    def _set_value_choose_button_name_text_(self, text):
        self._value_choose_button._set_name_text_(text)

    def _set_choose_button_state_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_state_file_path_(file_path)

    def _get_value_choose_button_(self):
        return self._value_choose_button

    def _get_value_add_button_(self):
        return self._value_add_button

    def _add_value_entry_button_(self, widget):
        self._button_layout.addWidget(widget)

    def _create_value_entry_button_(self, name_text, icon_name=None, sub_icon_name=None, tool_tip=None):
        button = _gui_qt_wgt_button.QtIconPressButton()
        self._button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(gui_core.RscIconFile.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(gui_core.RscIconFile.get(sub_icon_name))
        if tool_tip:
            button._set_tool_tip_(tool_tip)
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_choose_values_(self, values, *args, **kwargs):
        super(QtValueEntryAsConstantChoose, self)._set_choose_values_(values, *args, **kwargs)
        #
        self._refresh_choose_index_()

    def _get_choose_current_values_(self):
        return [self._get_value_()]

    def _extend_choose_current_values_(self, values):
        self._set_value_(values[-1])
        #
        self._refresh_widget_all_()

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
        self._restore_all_()
        self.user_value_entry_cleared.emit()

    def _restore_all_(self):
        self._value_index_label.hide()
        #
        self._choose_values = []
        self._choose_popup_image_url_dict = {}
        self._choose_popup_keyword_filter_dict = {}
        self._choose_popup_tag_filter_dict = {}
        self._value_entry._set_value_clear_()

    def _set_value_(self, value):
        super(QtValueEntryAsConstantChoose, self)._set_value_(value)
        self._refresh_choose_index_()


# rgba entry and choose
class QtValueEntryAsRgbaByChoose(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtValueEntryAsOtherBaseDef,

    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,

    gui_qt_abstract.AbsQtValueDefaultBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsTextEdit

    QT_POPUP_CHOOSE_CLS = _gui_qt_wgt_popup.QtPopupAsRgbaChoose
    QT_POPUP_COMPLETION_CLS = _gui_qt_wgt_popup.QtPopupAsCompletion

    def _refresh_widget_draw_geometry_(self):
        super(QtValueEntryAsRgbaByChoose, self)._refresh_widget_draw_geometry_()
        #
        x, y = 0, 0
        w = h = self.height()
        c_w, c_h = w, h
        v_w, v_h = self._value_draw_width, self._value_draw_height
        self._value_rect.setRect(
            x, y, c_w, c_h
        )
        self._value_draw_rect.setRect(
            x+(c_w-v_w)/2, y+(c_h-v_h)/2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsRgbaByChoose, self).__init__(*args, **kwargs)
        self.setFixedHeight(gui_configure.Size.ENTRY_HEIGHT)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._init_value_entry_as_other_base_def_(self)
        self._init_value_default_base_def_()

        self._build_value_entry_()

    def _get_value_rect_(self):
        return self._value_rect

    def _build_value_entry_(self):
        entry_layout = QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width+2, 0, 0, 0)
        entry_layout.setSpacing(2)

        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(str)
        self._value_entry._set_use_as_rgba_255_(True)
        self._value_entry.user_entry_finished.connect(self._refresh_widget_draw_)

        self._build_popup_choose_(self._value_entry, self)

    def eventFilter(self, *args):
        super(QtValueEntryAsRgbaByChoose, self).eventFilter(*args)

        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._value_entry_is_enable is True:
                        if self._value_rect.contains(event.pos()):
                            self._set_action_flag_(self.ActionFlag.ChoosePress)

                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.ChoosePress
                    ) is True:
                        self.press_clicked.emit()
                        self._do_popup_choose_start_()

                self._clear_all_action_flags_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtValueEntryAsRgbaByChoose, self).paintEvent(self)
        #
        painter = QtPainter(self)

        rgba = self._get_value_()
        offset = self._get_action_offset_()
        painter._draw_frame_by_rect_(
            self._value_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=rgba,
            offset=offset
        )

    def _build_popup_choose_(self, entry_gui, entry_frame_gui):
        self._popup_choose_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._popup_choose_widget._set_popup_entry_(entry_gui)
        self._popup_choose_widget._set_popup_entry_frame_(entry_frame_gui)
        self._popup_choose_widget.hide()

    def _do_popup_choose_start_(self):
        self._popup_choose_widget._do_popup_start_()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self.update()

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsRgbaByChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_all_()

    def _set_value_(self, value):
        self._value_entry._set_value_as_rgba_255_(value)

    def _get_value_(self):
        return self._value_entry._get_value_as_rgba_255_()


# icon entry and choose
class QtValueEntryAsIconChoose(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtValueEntryAsOtherBaseDef,

    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,

    gui_qt_abstract.AbsQtChooseBaseDef,
    gui_qt_abstract.AbsQtChooseAsPopupBaseDef,

    gui_qt_abstract.AbsQtValueDefaultBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsTextEdit

    QT_POPUP_CHOOSE_CLS = _gui_qt_wgt_popup.QtPopupAsIconChoose

    def _refresh_widget_draw_geometry_(self):
        super(QtValueEntryAsIconChoose, self)._refresh_widget_draw_geometry_()
        #
        x, y = 0, 0
        w = h = self.height()
        c_w, c_h = w, h
        v_w, v_h = self._value_draw_width, self._value_draw_height
        self._value_rect.setRect(
            x, y, c_w, c_h
        )
        self._value_draw_rect.setRect(
            x+(c_w-v_w)/2, y+(c_h-v_h)/2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsIconChoose, self).__init__(*args, **kwargs)
        self.setFixedHeight(gui_configure.Size.ENTRY_HEIGHT)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._init_choose_base_def_()
        self._init_choose_as_popup_base_def_(self)

        self._init_value_entry_as_other_base_def_(self)
        self._init_value_default_base_def_()

        self._build_value_entry_()

        self._set_choose_values_(
            [
                'application/katana',
                'application/maya',
                'application/houdini',
                'application/clarisse',
            ]*20
        )

    def eventFilter(self, *args):
        super(QtValueEntryAsIconChoose, self).eventFilter(*args)

        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._value_entry_is_enable is True:
                        if self._value_rect.contains(event.pos()):
                            self._set_action_flag_(self.ActionFlag.ChoosePress)

                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.ChoosePress
                    ) is True:
                        self.press_clicked.emit()
                        self._do_popup_choose_start_()

                self._clear_all_action_flags_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtValueEntryAsIconChoose, self).paintEvent(self)
        #
        painter = QtPainter(self)

        icon_name = self._get_value_()
        if icon_name == '':
            icon_name = 'state-disable'

        icon_file_path = bsc_core.RscIconFileMtd.get(icon_name)
        if icon_file_path:
            offset = self._get_action_offset_()

            painter._draw_icon_file_by_rect_(
                rect=self._value_draw_rect,
                file_path=icon_file_path,
                offset=offset
            )

    def _build_value_entry_(self):
        entry_layout = QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width+2, 0, 0, 0)
        entry_layout.setSpacing(2)

        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(str)
        self._value_entry.user_entry_finished.connect(self._refresh_widget_draw_)

        self._build_popup_choose_(self._value_entry, self)

    def _build_popup_choose_(self, entry_gui, entry_frame_gui):
        self._popup_choose_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._popup_choose_widget._set_popup_entry_(entry_gui)
        self._popup_choose_widget._set_popup_entry_frame_(entry_frame_gui)
        self._popup_choose_widget.hide()

        self._popup_choose_widget.user_popup_choose_text_accepted.connect(
            self._do_choose_text_accept_
        )

    def _do_choose_text_accept_(self, text):
        self._set_value_(text)
        self._refresh_widget_draw_()

    def _get_choose_current_values_(self):
        return [self._get_value_()]

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryAsIconChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_all_()


# any tuple, etc. float2, float3, ...
class QtValueEntryAsTuple(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtValueEntryAsTupleBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsTextEdit

    entry_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsTuple, self).__init__(*args, **kwargs)
        #
        self._init_value_entry_as_tuple_base_def_()
        # create entry layout first
        self._entry_layout = QtHBoxLayout(self)
        self._entry_layout.setContentsMargins(2, 2, 2, 2)
        self._entry_layout.setSpacing(8)
        self._build_value_entry_(2, self._value_type)

    def _build_value_entry_(self, value_size, value_type):
        self._value_type = value_type
        #
        if self._value_entries:
            set_qt_layout_clear(self._entry_layout)
        #
        self._value_entries = []
        #
        self._set_entry_count_(value_size)
        if value_size:
            for i in range(value_size):
                i_widget = _gui_qt_wgt_entry_base.QtEntryAsTextEdit()
                i_widget._set_value_type_(self._value_type)
                self._entry_layout.addWidget(i_widget)
                self._value_entries.append(i_widget)

    def _set_value_entry_enable_(self, boolean):
        pass


class QtValueEntryAsList(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtNameBaseDef,

    gui_qt_abstract.AbsQtValueEntryBaseDef,

    gui_qt_abstract.AbsQtChooseBaseDef,
    gui_qt_abstract.AbsQtChooseAsPopupBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsList
    #
    QT_POPUP_CHOOSE_CLS = _gui_qt_wgt_popup.QtPopupAsAnyChoose
    #
    add_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsList, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_name_base_def_(self)
        self._init_value_entry_base_def_(self)
        self._init_choose_base_def_()
        self._init_choose_as_popup_base_def_(self)
        #
        self._build_value_entry_(str)
        self._set_popup_choose_multiply_enable_(True)

    def _build_value_entry_(self, value_type):
        self._value_type = value_type
        #
        main_layout = QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #
        entry_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        entry_layout.addWidget(self._value_entry)
        self._value_entry._set_entry_frame_(self)
        #
        self._button_widget = _gui_qt_wgt_utility.QtLineWidget()
        self._button_widget._set_line_styles_(
            [self._button_widget.Style.Null, self._button_widget.Style.Null, self._button_widget.Style.Solid,
             self._button_widget.Style.Null]
        )
        entry_layout.addWidget(self._button_widget)
        self._button_layout = QtVBoxLayout(self._button_widget)
        self._button_layout._set_align_top_()
        self._button_layout.setContentsMargins(2, 0, 0, 0)
        self._button_layout.setSpacing(2)

        self._value_choose_button = _gui_qt_wgt_button.QtIconPressButton()
        self._button_layout.addWidget(self._value_choose_button)
        self._value_choose_button._set_icon_file_path_(gui_core.RscIconFile.get('file/file'))
        self._value_choose_button._set_icon_state_name_('state/popup')
        self._value_choose_button._set_icon_frame_draw_size_(18, 18)
        self._value_choose_button._set_name_text_('choose value')
        self._value_choose_button._set_tool_tip_('"LMB-click" to choose value from popup view')
        self._value_choose_button.press_clicked.connect(self._do_popup_choose_start_)
        # choose
        self._build_popup_choose_(self._value_entry, self)
        self.user_choose_finished.connect(self.choose_changed.emit)
        self.user_choose_finished.connect(self.user_choose_changed.emit)
        self.user_choose_list_accepted.connect(self._extend_choose_current_values_)
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
        self._frame_border_draw_style = QtCore.Qt.DashLine

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

    def _set_clear_(self):
        self._clear_all_values_()

    def _clear_all_values_(self):
        self._value_entry._clear_all_values_()

    def _set_entry_item_icon_file_path_(self, file_path):
        self._value_entry._set_item_icon_file_path_(file_path)

    def _add_value_entry_button_(self, widget):
        self._button_layout.addWidget(widget)

    def _create_value_entry_button_(self, name_text, icon_name=None, sub_icon_name=None):
        button = _gui_qt_wgt_button.QtIconPressButton()
        self._button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(gui_core.RscIconFile.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(gui_core.RscIconFile.get(sub_icon_name))
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry._set_use_as_storage_(boolean)

    def _set_value_choose_button_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_file_path_(file_path)

    def _set_value_choose_button_name_text_(self, text):
        self._value_choose_button._set_name_text_(text)

    def _set_choose_button_state_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_state_file_path_(file_path)

    # choose
    def _extend_choose_current_values_(self, values):
        self._extend_values_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()

    def _set_empty_icon_name_(self, text):
        self._value_entry._set_empty_icon_name_(text)

    def _set_empty_text_(self, text):
        self._value_entry._set_empty_text_(text)


class QtValueEntryAsListWithChoose(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtNameBaseDef,

    gui_qt_abstract.AbsQtValueEntryBaseDef,

    gui_qt_abstract.AbsQtChooseBaseDef,
    gui_qt_abstract.AbsQtChooseAsPopupBaseDef,
):
    QT_VALUE_ENTRY_CLS = _gui_qt_wgt_entry_base.QtEntryAsList
    QT_POPUP_CHOOSE_CLS = _gui_qt_wgt_popup.QtPopupAsAnyChoose
    #
    add_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsListWithChoose, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_name_base_def_(self)
        self._init_value_entry_base_def_(self)
        self._init_choose_base_def_()
        self._init_choose_as_popup_base_def_(self)
        #
        self._build_value_entry_(str)
        self._set_popup_choose_multiply_enable_(True)

    def _build_value_entry_(self, value_type):
        self._value_type = value_type

        main_layout = QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        entry_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        entry_layout.addWidget(self._value_entry)
        self._value_entry._set_entry_frame_(self)
        #
        self._button_widget = _gui_qt_wgt_utility.QtLineWidget()
        self._button_widget._set_line_styles_(
            [self._button_widget.Style.Null, self._button_widget.Style.Null, self._button_widget.Style.Solid,
             self._button_widget.Style.Null]
        )
        entry_layout.addWidget(self._button_widget)
        self._button_layout = QtVBoxLayout(self._button_widget)
        self._button_layout._set_align_top_()
        self._button_layout.setContentsMargins(2, 0, 0, 0)
        self._button_layout.setSpacing(2)

        self._value_choose_button = _gui_qt_wgt_button.QtIconPressButton()
        self._button_layout.addWidget(self._value_choose_button)
        self._value_choose_button._set_icon_file_path_(gui_core.RscIconFile.get('file/file'))
        self._value_choose_button._set_icon_state_name_('state/popup')
        self._value_choose_button._set_icon_frame_draw_size_(18, 18)
        self._value_choose_button._set_name_text_('choose value')
        self._value_choose_button._set_tool_tip_('"LMB-click" to choose value from popup view')
        self._value_choose_button.press_clicked.connect(self._do_popup_choose_start_)
        # choose
        self._build_popup_choose_(self._value_entry, self)
        self.user_choose_finished.connect(self.choose_changed.emit)
        self.user_choose_finished.connect(self.user_choose_changed.emit)
        self.user_choose_list_accepted.connect(self._extend_choose_current_values_)
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
        self._value_entry._set_item_icon_file_path_(file_path)

    def _add_value_entry_button_(self, widget):
        self._button_layout.addWidget(widget)

    def _create_value_entry_button_(self, name_text, icon_name=None, sub_icon_name=None):
        button = _gui_qt_wgt_button.QtIconPressButton()
        self._button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(gui_core.RscIconFile.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(gui_core.RscIconFile.get(sub_icon_name))
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry._set_use_as_storage_(boolean)

    def _set_value_choose_button_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_file_path_(file_path)

    def _set_value_choose_button_name_text_(self, text):
        self._value_choose_button._set_name_text_(text)

    def _set_choose_button_state_icon_file_path_(self, file_path):
        self._value_choose_button._set_icon_state_file_path_(file_path)

    # choose
    def _extend_choose_current_values_(self, values):
        self._extend_values_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()


class QtValueEntryAsBubblesChoose(
    _gui_qt_wgt_entry_base.QtEntryFrame,

    gui_qt_abstract.AbsQtNameBaseDef,

    gui_qt_abstract.AbsQtValueEntryBaseDef,

    gui_qt_abstract.AbsQtChooseBaseDef,
    gui_qt_abstract.AbsQtChooseAsPopupBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(QtValueEntryAsBubblesChoose, self).__init__(*args, **kwargs)
        self._init_name_base_def_(self)
        self._init_value_entry_base_def_(self)
        self._init_choose_base_def_()
        self._init_choose_as_popup_base_def_(self)
        #
        self._build_value_entry_(str)
        self._set_popup_choose_multiply_enable_(True)
