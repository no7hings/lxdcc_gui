# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_resize

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class QtConstantEntry(
    QtWidgets.QLineEdit,
    utl_gui_qt_abstract.AbsQtValueDef,
    #
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
    utl_gui_qt_abstract.AbsQtActionDropDef,
):
    entry_changed = qt_signal()
    entry_cleared = qt_signal()
    #
    user_entry_changed = qt_signal()
    user_entry_cleared = qt_signal()
    user_entry_finished = qt_signal()
    #
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()
    key_escape_pressed = qt_signal()
    key_backspace_pressed = qt_signal()
    #
    key_backspace_extra_pressed = qt_signal()
    #
    focus_in = qt_signal()
    focus_out = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtConstantEntry, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setPalette(QtDccMtd.get_palette())
        self.setFont(Font.NAME)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._value_type = str
        #
        self._item_value_default = None
        #
        self._maximum = 1
        self._minimum = 0
        #
        self.returnPressed.connect(self.user_entry_finished.emit)
        # emit send by setText
        self.textChanged.connect(self._send_enter_changed_emit_)
        # user enter
        self.textEdited.connect(self._send_user_enter_changed_emit_)
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QLineEdit')
        )
        self._set_value_def_init_(self)
        self._init_entry_base_def_(self)
        self._init_action_drop_def_(self)
        self.setAcceptDrops(self._action_popup_is_enable)

        # self.setPlaceholderText()

    def _set_entry_tip_(self, text):
        self.setPlaceholderText(text)

    def _execute_action_wheel_(self, event):
        if self._value_type in [int, float]:
            delta = event.angleDelta().y()
            pre_value = self._get_value_()
            if delta > 0:
                self._set_value_(pre_value+1)
            else:
                self._set_value_(pre_value-1)
            #
            self._send_enter_changed_emit_()

    def _execute_action_drop_(self, event):
        data = event.mimeData()
        if data.hasUrls():
            urls = event.mimeData().urls()
            if urls:
                value = urls[0].toLocalFile()
                if self._get_value_is_valid_(value):
                    self._set_value_(value)
                    return True
        return False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
                self.focus_in.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(False)
                #
                self.focus_out.emit()
                #
                self._set_value_completion_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._execute_action_wheel_(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Up:
                    self.key_up_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Down:
                    self.key_down_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Escape:
                    self.key_escape_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Backspace:
                    self.key_backspace_pressed.emit()
                    if not self.text():
                        self.key_backspace_extra_pressed.emit()
        return False

    def _set_drop_enable_(self, boolean):
        super(QtConstantEntry, self)._set_drop_enable_(boolean)
        self.setAcceptDrops(boolean)

    def dropEvent(self, event):
        if self._execute_action_drop_(event) is True:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        menu_raw = [
            ('basic', ),
            ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
            ('paste', None, (True, self.paste, False), QtGui.QKeySequence.Paste),
            ('cut', None, (True, self.cut, False), QtGui.QKeySequence.Cut),
            ('extend', ),
            ('undo', None, (True, self.undo, False), QtGui.QKeySequence.Undo),
            ('redo', None, (True, self.redo, False), QtGui.QKeySequence.Redo),
            ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll),
        ]
        #
        if self.isReadOnly():
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('extend', ),
                ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if self._entry_use_as_storage is True:
            menu_raw.extend(
                [
                    ('system',),
                    ('open folder', 'file/folder', (True, self._execute_open_in_system_, False), QtGui.QKeySequence.Open)
                ]
            )
        #
        if menu_raw:
            self._qt_menu = _utl_gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _send_enter_changed_emit_(self):
        # noinspection PyUnresolvedReferences
        self.entry_changed.emit()
        text = self.text()
        if not text:
            self.entry_cleared.emit()

    def _send_user_enter_changed_emit_(self):
        # noinspection PyUnresolvedReferences
        self.user_entry_changed.emit()
        text = self.text()
        if not text:
            self.user_entry_cleared.emit()

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
            # self._set_validator_use_as_name_()
        elif self._value_type is int:
            self._set_validator_use_as_integer_()
        elif self._value_type is float:
            self._set_validator_use_as_float_()

    def _get_value_type_(self):
        return self._value_type

    def _execute_open_in_system_(self):
        _ = self.text()
        if _:
            _exist_comp = bsc_core.StgExtraMtd.get_exists_component(_)
            if _exist_comp is not None:
                bsc_core.StgExtraMtd.set_directory_open(
                    _exist_comp
                )

    def _set_validator_use_as_storage_(self, boolean=True):
        super(QtConstantEntry, self)._set_validator_use_as_storage_(boolean)
        if boolean is True:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                self._execute_open_in_system_
            )
            i_action.setShortcut(
                QtGui.QKeySequence.Open
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)

    def _set_validator_use_as_name_(self):
        reg = QtCore.QRegExp(r'^[a-zA-Z0-9_]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #     )
        # )

    def _set_validator_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())
        self._set_value_completion_()
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         '"MMB-wheel" to modify "int" value'
        #     )
        # )

    def _set_validator_use_as_float_(self):
        self.setValidator(QtGui.QDoubleValidator())
        self._set_value_completion_()
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         '"MMB-wheel" to modify "float" value'
        #     )
        # )

    def _set_validator_use_as_frames_(self):
        self._set_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9-,:]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         'etc:\n'
        #         '   1\n'
        #         '   1-2\n'
        #         '   1-5,7,50-100,101'
        #     )
        # )

    def _set_validator_use_as_rgba_(self):
        self._set_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9.,]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

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
            if isinstance(_, six.text_type):
                _ = _.encode('utf-8')
            return _
        elif self._value_type == int:
            return int(_)
        elif self._value_type == float:
            return float(_)
        return _

    def _set_value_(self, value):
        pre_value = self.text()
        if value is not None:
            if isinstance(value, six.text_type):
                value = value.encode('utf-8')

            if isinstance(pre_value, six.text_type):
                pre_value = pre_value.encode('utf-8')

            if self._value_type is not None:
                value = self._value_type(value)
            #
            if value != pre_value:
                self.setText(str(value))
                # self._send_enter_changed_emit_()
        else:
            self.setText('')

    def _get_value_default_(self):
        return self._item_value_default

    def _connect_focused_to_(self, widget):
        pass
    #
    def _get_is_selected_(self):
        boolean = False
        if self.selectedText():
            boolean = True
        return boolean

    def _set_value_clear_(self):
        self._set_value_('')

    def _set_entry_enable_(self, boolean):
        self.setReadOnly(not boolean)

    def _set_all_selected_(self):
        self.selectAll()

    def _set_focused_(self, boolean):
        if boolean is True:
            self.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self.setFocus(
                QtCore.Qt.NoFocusReason
            )

    def _get_is_focused_(self):
        return self.hasFocus()

    def _set_clear_(self):
        self.clear()


class QtContentEntry(
    QtWidgets.QTextBrowser,
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(QtContentEntry, self).__init__(*args, **kwargs)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.installEventFilter(self)
        # self.setAcceptRichText(False)
        # self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        #
        self.setFont(Font.CONTENT)
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self._print_signals = QtPrintSignals(self)
        self._print_signals.added.connect(self._set_content_add_)
        self._print_signals.overed.connect(self._set_content_)
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QTextBrowser')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        self._init_entry_base_def_(self)

    def _set_content_add_(self, text):
        def add_fnc_(text_):
            self.moveCursor(QtGui.QTextCursor.End)
            self.insertPlainText(text_+'\n')
        #
        if isinstance(text, (tuple, list)):
            [add_fnc_(i) for i in text]
        else:
            add_fnc_(text)
        #
        self.update()

    def _set_content_(self, text):
        self.setText(text)

    def _set_content_add_use_thread_(self, text):
        self._print_signals.added.emit(text)

    def _set_print_over_use_thread_(self, text):
        self._print_signals.overed.emit(text)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(False)
        return False

    def contextMenuEvent(self, event):
        menu_raw = [
            ('basic', ),
            ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
            ('paste', None, (True, self.paste, False), QtGui.QKeySequence.Paste),
            ('cut', None, (True, self.cut, False), QtGui.QKeySequence.Cut),
            ('extend', ),
            ('undo', None, (True, self.undo, False), QtGui.QKeySequence.Undo),
            ('redo', None, (True, self.redo, False), QtGui.QKeySequence.Redo),
            ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll),
        ]
        if self.isReadOnly():
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('extend', ),
                ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if menu_raw:
            self._qt_menu = _utl_gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _get_value_(self):
        return self.toPlainText()

    def _set_value_(self, value):
        if value is not None:
            self.setText(
                unicode(value).encode('utf-8')
            )
        else:
            self.setText('')

    def insertFromMimeData(self, data):
        if data.text():
            self.setText(data.text())


class QtListEntryForPopup(utl_gui_qt_abstract.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(QtListEntryForPopup, self).__init__(*args, **kwargs)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.ListMode)
        self.setPalette(QtDccMtd.get_palette())

    def paintEvent(self, event):
        pass

    def _get_maximum_height_(self, count_maximum, includes=None):
        adjust = 1+8
        if includes is not None:
            rects = [self.visualItemRect(i) for i in includes[:count_maximum]]
        else:
            rects = [self.visualItemRect(self.item(i)) for i in range(self.count())[:count_maximum]]
        if rects:
            return sum([i.height() for i in rects])+adjust
        return 20+adjust


class QtListEntry(
    utl_gui_qt_abstract.AbsQtListWidget,
    utl_gui_qt_abstract.AbsQtHelpDef,
    #
    utl_gui_qt_abstract.AbsQtValueDef,
    utl_gui_qt_abstract.AbsQtValuesDef,
    #
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
    #
    utl_gui_qt_abstract.AbsQtActionDropDef,
):
    entry_changed = qt_signal()
    entry_added = qt_signal()
    #
    user_entry_changed = qt_signal()
    user_entry_cleared = qt_signal()
    user_entry_finished = qt_signal()
    # for popup choose
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()
    key_enter_pressed = qt_signal()
    def _get_value_(self):
        pass

    def __init__(self, *args, **kwargs):
        super(QtListEntry, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
        self.setSelectionMode(self.ExtendedSelection)
        #
        self._item_width, self._item_height = 20, 20

        self._set_help_def_init_(self)
        #
        self._set_value_def_init_(self)
        self._set_values_def_init_(self)
        #
        self._init_entry_base_def_(self)
        self._init_action_drop_def_(self)

        self.setAcceptDrops(self._action_popup_is_enable)

        self._set_shortcut_register_()

        self._item_icon_file_path = None

        self._icon_name = None

    def contextMenuEvent(self, event):
        if self._entry_is_enable is True:
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self._set_action_copy_, False), QtGui.QKeySequence.Copy),
                ('paste', None, (True, self._set_action_paste_, False), QtGui.QKeySequence.Paste),
                ('cut', None, (True, self._set_action_cut_, False), QtGui.QKeySequence.Cut),
                ('extend',),
                ('select all', None, (True, self._set_action_select_all_, False), QtGui.QKeySequence.SelectAll),
            ]
        else:
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self._set_action_copy_, False), QtGui.QKeySequence.Copy),
                ('extend',),
                ('select all', None, (True, self._set_action_select_all_, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        items = self._get_selected_items_()
        if items:
            menu_raw.append(
                ('open folder', 'file/folder', (True, self._execute_open_in_system_, False), QtGui.QKeySequence.Open)
            )
        #
        if menu_raw:
            self._qt_menu = _utl_gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _execute_open_in_system_(self):
        item = self._get_item_current_()
        if item is not None:
            item_widget = self.itemWidget(item)
            if item_widget is not None:
                _ = item_widget._get_name_text_()
                bsc_core.StgPathOpt(_).set_open_in_system()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = True
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = False
                elif event.key() == QtCore.Qt.Key_Delete:
                    self._execute_action_delete_(event)
            elif event.type() == QtCore.QEvent.Wheel:
                pass
                # self._execute_action_wheel_(event)
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_view_all_items_viewport_showable_()
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(False)
        if widget == self.verticalScrollBar():
            pass
        return False

    def paintEvent(self, event):
        if not self.count():
            painter = QtPainter(self.viewport())
            painter._set_empty_draw_by_rect_(
                rect=self.rect(), icon_name=self._icon_name
            )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            # event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self._execute_action_drop_(event)

    def _set_shortcut_register_(self):
        actions = [
            (self._set_action_copy_, 'Ctrl+C'),
            (self._set_action_paste_, 'Ctrl+V'),
            (self._set_action_cut_, 'Ctrl+X'),
            (self._set_action_select_all_, 'Ctrl+A')
        ]
        for i_fnc, i_shortcut in actions:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                i_fnc
            )
            i_action.setShortcut(
                QtGui.QKeySequence(
                    i_shortcut
                )
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)

    def _set_action_copy_(self):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            values = [i._get_name_text_() for i in selected_item_widgets]
            QtWidgets.QApplication.clipboard().setText(
                '\n'.join(values)
            )

    def _set_action_paste_(self):
        text = QtWidgets.QApplication.clipboard().text()
        if text:
            values = [i.strip() for i in text.split('\n')]
            [self._set_value_append_(i) for i in values]

    def _set_action_cut_(self):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            values = [i._get_name_text_() for i in selected_item_widgets]
            QtWidgets.QApplication.clipboard().setText(
                '\n'.join(values)
            )
            [self._set_value_delete_(i) for i in values]

    def _set_action_select_all_(self):
        self._set_all_items_selected_(True)

    def _get_selected_item_widgets_(self):
        return [self.itemWidget(i) for i in self.selectedItems()]

    def _set_drop_enable_(self, boolean):
        super(QtListEntry, self)._set_drop_enable_(boolean)
        self.setAcceptDrops(boolean)
        # self.setDragDropMode(self.DropOnly)
        # self.setDropIndicatorShown(True)

    def _execute_action_drop_(self, event):
        data = event.mimeData()
        # for i in data.formats():
        #     print i, data.data(i).data()
        if data.hasUrls():
            urls = event.mimeData().urls()
            if urls:
                values = []
                #
                for i_url in urls:
                    i_value = i_url.toLocalFile()
                    if self._get_value_is_valid_(i_value):
                        values.append(i_value)
                #
                cs = bsc_core.StgFileMultiplyMtd.set_merge_to(
                    values,
                    ['*.####.*']
                )
                [self._set_value_append_(i) for i in cs]
    # noinspection PyUnusedLocal
    def _execute_action_delete_(self, event):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            for i in selected_item_widgets:
                i_value = i._get_name_text_()
                self._set_value_delete_(i_value)

    def _set_value_delete_(self, value):
        if value:
            if self._entry_is_enable is True:
                index = self._values.index(value)
                self._values.remove(value)
                #
                item = self.item(index)
                self._set_item_widget_delete_(item)
                self.takeItem(index)
        #
        self._refresh_view_all_items_viewport_showable_()

    def _set_value_append_(self, value):
        if value:
            if value not in self._values:
                self._values.append(value)
                self._set_item_add_(value)
                self.entry_added.emit()

    def _set_value_extend_(self, values):
        if values:
            for i_value in values:
                self._set_value_append_(i_value)

    def _set_values_clear_(self):
        self._values = []
        self._set_clear_()

    def _set_item_show_deferred_(self, data):
        item_widget, value = data
        item_widget._set_name_text_(value)
        item_widget._set_tool_tip_(value)
        if self._item_icon_file_path is not None:
            item_widget._set_icon_file_path_(self._item_icon_file_path)
        else:
            item_widget._set_icon_name_text_(value)

    def _set_item_add_(self, value):
        def cache_fnc_():
            return [item_widget, value]

        def build_fnc_(data):
            self._set_item_show_deferred_(data)

        def delete_fnc_():
            self._set_value_delete_(value)

        item_widget = _utl_gui_qt_wgt_utility._QtHItem()
        item_widget._set_delete_enable_(True)
        item_widget.delete_press_clicked.connect(delete_fnc_)
        item = _utl_gui_qt_wgt_utility.QtListWidgetItem()
        item.setSizeHint(QtCore.QSize(self._item_width, self._item_height))
        self.addItem(item)
        item._set_item_show_connect_()
        self.setItemWidget(item, item_widget)

        item._set_item_show_fnc_(
            cache_fnc_, build_fnc_
        )

    def _set_values_(self, values):
        self._set_clear_()
        [self._set_value_append_(i) for i in values]

    def _set_entry_item_icon_file_path_(self, file_path):
        self._item_icon_file_path = file_path

    def _set_validator_use_as_storage_(self, boolean):
        super(QtListEntry, self)._set_validator_use_as_storage_(boolean)
        if boolean is True:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                self._execute_open_in_system_
            )
            i_action.setShortcut(
                QtGui.QKeySequence.Open
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)


class QtEntryFrame(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtStatusDef,
):
    geometry_changed = qt_signal(int, int, int, int)
    entry_focus_in = qt_signal()
    entry_focus_out = qt_signal()
    entry_focus_changed = qt_signal()
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        # int left， int top， int right， int bottom
        m_l, m_t, m_r, m_b = self._frame_draw_margins

        c = self._entry_count

        frm_x, frm_y = x+m_l+1, y+m_t+1
        frm_w, frm_h = w-m_l-m_r-2, h-m_t-m_b-2
        if c > 1:
            for i in range(c):
                i_widget = self._value_entries[i]
                i_p = i_widget.pos()
                i_r = i_widget.rect()
                i_x, i_y = i_p.x(), i_p.y()
                i_w, i_h = i_r.width(), i_r.height()
                self._frame_draw_rects[i].setRect(
                    i_x, frm_y, i_w, frm_h
                )
        else:
            self._frame_draw_rects[0].setRect(
                frm_x, frm_y, frm_w, frm_h
            )
        #
        if self._tip_draw_enable is True:
            self._tip_draw_rect.setRect(
                x, y, w, h
            )

        if self._resize_handle is not None:
            frm_w, frm_h = 24, 24
            r_x, r_y = x+(w-frm_w), y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )

    def __init__(self, *args, **kwargs):
        super(QtEntryFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._action_is_hovered = False
        self._is_focused = False
        self._entry_count = 1
        #
        self._value_entry = None
        self._value_entries = []
        #
        self._init_name_def_(self)
        self._set_frame_def_init_()
        self._set_status_def_init_()
        #
        self._frame_border_color = QtBorderColors.Light
        self._hovered_frame_border_color = QtBorderColors.Hovered
        self._selected_frame_border_color = QtBorderColors.Selected
        self._frame_background_color = QtBackgroundColors.Dim

        self._resize_handle = _utl_gui_qt_wgt_resize.QtVResizeHandle(self)
        self._resize_handle.hide()

        self._tip_draw_enable = False
        self._tip_text = None
        self._tip_draw_rect = QtCore.QRect()
        # self._resize_handle._set_resize_target_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
                self.geometry_changed.emit(
                    self.x(), self.y(), self.width(), self.height()
                )
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        # is_hovered = self._action_is_hovered
        is_selected = self._is_focused
        background_color = self._frame_background_color
        bdr_color = [QtBorderColors.Basic, QtBorderColors.HighLight][is_selected]
        bdr_w = [1, 2][is_selected]
        for i_rect in self._frame_draw_rects:
            painter._draw_frame_by_rect_(
                i_rect,
                border_color=bdr_color,
                background_color=background_color,
                # border_radius=1,
                border_width=bdr_w,
            )
        #
        if self._tip_draw_enable is True:
            if self._tip_text is not None:
                painter._draw_text_by_rect_(
                    rect=self._tip_draw_rect,
                    text=self._tip_text,
                    font_color=QtFontColors.Disable,
                    font=get_font(size=8, italic=True),
                    text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                )
    # resize
    def _get_resize_handle_(self):
        return self._resize_handle

    def _set_resize_enable_(self, boolean):
        self._resize_handle.setVisible(boolean)

    def _set_resize_minimum_(self, value):
        self._resize_handle._set_resize_minimum_(value)

    def _set_resize_target_(self, widget):
        self._resize_handle._set_resize_target_(widget)

    def _update_background_color_by_locked_(self, boolean):
        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dim
        ][boolean]

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self._refresh_widget_draw_()
        self.entry_focus_changed.emit()

    def _set_focus_in_(self):
        self._set_focused_(True)
        self.entry_focus_in.emit()

    def set_focus_out_(self):
        self._set_focused_(False)
        self.entry_focus_out.emit()

    def _set_entry_count_(self, size):
        self._entry_count = size
        self._frame_draw_rects = [QtCore.QRect() for _ in range(size)]

    def _set_size_policy_height_fixed_mode_(self):
        self._value_entry.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )

    def _set_tip_text_(self, text):
        self._tip_text = text

    def _set_tip_draw_enable_(self, boolean):
        self._tip_draw_enable = boolean
