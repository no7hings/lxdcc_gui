# coding=utf-8
import copy

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_resize, _utl_gui_qt_wgt_entry_base, _utl_gui_qt_wgt_popup

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class QtFilterBar(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForEntryDef,
    #
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
    utl_gui_qt_abstract.AbsQtHistoryExtraDef,
    utl_gui_qt_abstract.AbsQtCompletionExtraDef,
):
    occurrence_previous_press_clicked = qt_signal()
    occurrence_next_press_clicked = qt_signal()
    #
    QT_VALUE_ENTRY_CLS = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit
    #
    QT_POPUP_HISTORY_CLS = _utl_gui_qt_wgt_popup.QtPopupForHistory
    QT_POPUP_COMPLETION_CLS = _utl_gui_qt_wgt_popup.QtPopupForCompletion
    def _start_choose_extra_fnc_(self):
        self._history_extra_widget._execute_popup_start_()

    def _refresh_widget_(self):
        self.update()

    def _refresh_widget_draw_(self):
        pass

    def __init__(self, *args, **kwargs):
        super(QtFilterBar, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        qt_layout_0 = QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        self._init_value_entry_extra_def_(self)
        #
        self._init_action_base_def_(self)
        self._init_set_action_for_entry_def_(self)
        #
        self._init_choose_base_def_()
        #
        self._init_completion_extra_def_(self)
        #
        self._result_label = _utl_gui_qt_wgt_utility.QtTextItem()
        # todo: fix result show bug
        # self._result_label.hide()
        qt_layout_0.addWidget(self._result_label)
        #
        self._resize_handle = _utl_gui_qt_wgt_resize.QtHResizeHandle()
        self._resize_handle._set_resize_icon_file_paths_(
            [
                utl_gui_core.RscIconFile.get('resize-handle-v'), utl_gui_core.RscIconFile.get('resize-handle-v')
            ]
        )
        self._resize_handle._resize_frame_draw_size = 10, 20
        self._resize_handle._resize_icon_draw_size = 8, 16
        self._resize_handle._set_resize_alignment_(self._resize_handle.ResizeAlignment.Left)
        qt_layout_0.addWidget(self._resize_handle)
        self._resize_handle.setFixedWidth(8)
        #
        self._value_entry_frame = _utl_gui_qt_wgt_entry_base.QtEntryFrame()
        self._value_entry_frame.setFixedWidth(200)
        self._value_entry_frame.setFixedHeight(24)
        self._resize_handle._set_resize_target_(self._value_entry_frame)
        qt_layout_0.addWidget(self._value_entry_frame)
        #
        self._build_value_entry_(str)
        #
        self._match_case_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._match_case_button.hide()
        qt_layout_0.addWidget(self._match_case_button)
        self._match_case_button.setFocusProxy(self._value_entry)
        self._match_case_button.clicked.connect(self._execute_filter_match_case_swap_)
        self._match_case_icon_names = 'match_case_off', 'match_case_on'
        self._is_match_case = False
        #
        self._match_word_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._match_word_button.hide()
        qt_layout_0.addWidget(self._match_word_button)
        self._match_word_button.setFocusProxy(self._value_entry)
        self._match_word_button.clicked.connect(self._execute_filter_match_word_swap_)
        self._match_word_icon_names = 'match_word_off', 'match_word_on'
        self._is_match_word = False
        #
        self._pre_occurrence_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        qt_layout_0.addWidget(self._pre_occurrence_button)
        self._pre_occurrence_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'pre_occurrence'
            )
        )
        self._pre_occurrence_button.clicked.connect(
            self._send_pre_occurrence_emit_
        )
        #
        self._next_occurrence_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        qt_layout_0.addWidget(self._next_occurrence_button)
        self._next_occurrence_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'next_occurrence'
            )
        )
        self._next_occurrence_button.clicked.connect(
            self._send_next_occurrence_emit_
        )
        #
        self._init_history_as_extra_def_(self)
        #
        self._filter_result_count = None
        self._filter_index_current = None
        #
        self.__refresh_filter_()
        self._execute_refresh_filter_tip_()

    def _build_value_entry_(self, value_type):
        self._value_type = value_type
        self._value_entry_layout = QtHBoxLayout(self._value_entry_frame)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(0)
        #
        self._header_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._header_button._set_icon_frame_draw_size_(18, 18)
        self._value_entry_layout.addWidget(self._header_button)
        self._header_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'search'
            )
        )
        #
        self._bubble_entry = _utl_gui_qt_wgt_entry_base.QtEntryAsBubbles()
        self._value_entry_layout.addWidget(self._bubble_entry)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        self._value_entry_layout.addWidget(self._value_entry)
        #
        self._value_entry.entry_changed.connect(
            self._send_enter_changed_emit_
        )
        self._value_entry.user_entry_changed.connect(
            self._send_user_enter_changed_emit_
        )
        #
        self._entry_clear_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._value_entry_layout.addWidget(self._entry_clear_button)
        self._entry_clear_button.hide()
        self._entry_clear_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'entry_clear'
            )
        )
        self._entry_clear_button._icon_draw_percent = .6
        self._entry_clear_button.clicked.connect(self._execute_user_entry_clear_)
        #
        self._value_history_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._value_entry_layout.addWidget(self._value_history_button)
        self._value_history_button._set_icon_frame_draw_size_(18, 18)
        #
        self._value_history_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('history'))
        self._value_history_button._set_icon_sub_file_path_(utl_gui_core.RscIconFile.get('down'))
        self._value_history_button.press_clicked.connect(
            self._start_choose_extra_fnc_
        )
        self._value_history_button.hide()
        #
        self._build_history_extra_(self._value_entry, self._value_entry_frame)
        self._build_completion_extra_(self._value_entry, self._value_entry_frame)
        #
        self.user_completion_text_accepted.connect(self._add_history_extra_value_)
        self.user_completion_text_accepted.connect(self._set_value_)
        #
        self._bubble_entry._set_bubble_constant_entry_(self._value_entry)
        self._value_entry.textEdited.connect(self._execute_refresh_filter_tip_)
        self._value_entry.user_entry_text_accepted.connect(self._bubble_entry._create_value_item_)
        self._value_entry.key_backspace_extra_pressed.connect(self._bubble_entry._execute_bubble_backspace_)
        #
        self._bubble_entry.bubble_text_changed.connect(self._execute_refresh_filter_tip_)
        self._bubble_entry.bubble_text_changed.connect(self.user_entry_changed)
        #
        self._entry_clear_button.press_clicked.connect(self._execute_refresh_filter_tip_)
        self.user_history_text_accepted.connect(self._bubble_entry._create_value_item_)

    def _execute_refresh_filter_tip_(self):
        if self._value_entry_frame._tip_text:
            if self._get_all_filter_keyword_texts_():
                self._value_entry_frame._tip_draw_enable = False
            else:
                self._value_entry_frame._tip_draw_enable = True

            self._value_entry_frame._refresh_widget_draw_()
    #
    def _get_all_filter_keyword_texts_(self):
        _ = copy.copy(self._bubble_entry._get_all_bubble_texts_())
        if self._value_entry._get_value_():
            _.append(self._value_entry._get_value_())
        return list(_)

    def __refresh_filter_(self):
        self._match_case_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(self._match_case_icon_names[self._is_match_case])
        )
        #
        self._match_word_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(self._match_word_icon_names[self._is_match_word])
        )

    def _execute_filter_match_case_swap_(self):
        self._is_match_case = not self._is_match_case
        self.__refresh_filter_()
        #
        self._send_enter_changed_emit_()

    def _execute_filter_match_word_swap_(self):
        self._is_match_word = not self._is_match_word
        self.__refresh_filter_()
        self._send_enter_changed_emit_()

    def _execute_entry_clear_(self):
        self._value_entry._set_clear_()
        self._value_entry.entry_cleared.emit()
        self._send_enter_changed_emit_()

    def _execute_user_entry_clear_(self):
        self._value_entry._set_clear_()
        self._value_entry.user_entry_cleared.emit()
        self._send_user_enter_changed_emit_()
    #
    def _set_filter_tip_(self, text):
        self._value_entry_frame._set_tip_text_(text)
        self._execute_refresh_filter_tip_()

    def _get_is_match_case_(self):
        return self._is_match_case

    def _get_is_match_word_(self):
        return self._is_match_word

    def _send_enter_changed_emit_(self):
        # noinspection PyUnresolvedReferences
        self.entry_changed.emit()
        self._refresh_entry_clear_button_visible_()

    def _send_user_enter_changed_emit_(self):
        self.user_entry_changed.emit()
        self._refresh_entry_clear_button_visible_()

    def _send_pre_occurrence_emit_(self):
        # noinspection PyUnresolvedReferences
        self.occurrence_previous_press_clicked.emit()

    def _send_next_occurrence_emit_(self):
        # noinspection PyUnresolvedReferences
        self.occurrence_next_press_clicked.emit()

    def _refresh_entry_clear_button_visible_(self):
        self._entry_clear_button.setVisible(
            not not self._value_entry.text()
        )

    def _set_filter_result_count_(self, value):
        self._filter_result_count = value
        self._filter_index_current = None
        self._refresh_filter_result_()

    def _set_filter_result_index_current_(self, value):
        self._filter_index_current = value
        self._refresh_filter_result_()

    def _refresh_filter_result_(self):
        if self._filter_result_count is not None:
            if self._filter_index_current is not None:
                self._result_label._set_name_text_('{} / {}'.format(self._filter_index_current+1, self._filter_result_count))
            else:
                self._result_label._set_name_text_('1 / {}'.format(self._filter_result_count))
        else:
            self._result_label._set_name_text_('')

    def _set_result_clear_(self):
        self._filter_result_count = None
        self._filter_index_current = None
        self._refresh_filter_result_()

    def _restore_(self):
        self._value_entry._set_clear_()

    def _set_entry_focus_(self, boolean):
        self._value_entry._set_focused_(boolean)

    def _set_history_extra_key_(self, key):
        super(QtFilterBar, self)._set_history_extra_key_(key)
        #
        self._value_history_button.show()

    def _add_history_extra_value_(self, value):
        if self._history_extra_key is not None:
            if value:
                if self._get_history_extra_value_is_valid_(value) is True:
                    utl_core.History.append(
                        self._history_extra_key,
                        value
                    )
            #
            self._refresh_history_extra_()

    def _setup_history_extra_(self):
        if self._history_extra_key is not None:
            value = self._get_value_()
            if value:
                if self._get_history_extra_value_is_valid_(value) is True:
                    utl_core.History.append(
                        self._history_extra_key,
                        value
                    )
            #
            self._refresh_history_extra_()

    def _refresh_history_extra_(self):
        if self._history_extra_key is not None:
            values = utl_core.History.get(
                self._history_extra_key
            )
            if values:
                # latest show on top
                values.reverse()
                # value validation
                values = [i for i in values if self._get_history_extra_value_is_valid_(i) is True]
                #
                self._set_choose_values_(values)
                #
                self._value_history_button._set_action_enable_(
                    True
                )
            else:
                self._clear_choose_values_()
                self._value_history_button._set_action_enable_(
                    False
                )

    def _extend_choose_current_values_(self, values):
        self._set_value_(values[-1])