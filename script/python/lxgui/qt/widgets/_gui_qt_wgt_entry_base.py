# coding=utf-8
import functools

import six
from lxgui.qt.core import *

from lxgui.qt.widgets import _gui_qt_wgt_utility, _gui_qt_wgt_resize

import lxgui.qt.abstracts as gui_qt_abstract


# base entry for constant
class QtEntryAsTextEdit(
    QtWidgets.QLineEdit,
    gui_qt_abstract.AbsQtEntryExtraDef,
    #
    gui_qt_abstract.AbsQtEntryBaseDef,
    gui_qt_abstract.AbsQtDropBaseDef,
):
    entry_changed = qt_signal()
    entry_cleared = qt_signal()
    #
    user_entry_changed = qt_signal()
    user_entry_cleared = qt_signal()
    user_entry_finished = qt_signal()
    #
    user_entry_text_accepted = qt_signal(str)
    #
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()
    key_escape_pressed = qt_signal()
    key_backspace_pressed = qt_signal()
    #
    user_key_tab_pressed = qt_signal()
    #
    key_backspace_extra_pressed = qt_signal()
    #
    focus_in = qt_signal()
    focus_out = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryAsTextEdit, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setPalette(GuiQtDcc.generate_qt_palette())
        self.setFont(QtFonts.NameNormal)
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
        self.returnPressed.connect(self.__execute_text_change_accepted_)
        # emit send by setText
        self.textChanged.connect(self._send_enter_changed_emit_)
        # user enter
        self.textEdited.connect(self._send_user_enter_changed_emit_)
        #
        self.setStyleSheet(
            GuiQtStyle.get('QLineEdit')
        )
        self._init_entry_extra_def_(self)
        self._init_entry_base_def_(self)
        self._init_drop_base_def_(self)
        self.setAcceptDrops(self._action_drop_is_enable)

        # self.setPlaceholderText()

        # self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def __execute_text_change_accepted_(self):
        self.user_entry_text_accepted.emit(self.text())

    def _set_entry_tip_(self, text):
        self.setPlaceholderText(text)

    def _do_wheel_(self, event):
        if self._value_type in [int, float]:
            delta = event.angleDelta().y()
            pre_value = self._get_value_()
            if delta > 0:
                self._set_value_(pre_value+1)
            else:
                self._set_value_(pre_value-1)
            #
            self._send_enter_changed_emit_()
            event.accept()

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
                self._completion_value_auto_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)
                # break event passthrough
                return True
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
                elif event.key() == QtCore.Qt.Key_Tab:
                    self.user_key_tab_pressed.emit()
                elif event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    # self.self.user_entry_finished.emit()
                    self._completion_value_auto_()
        return False

    def dropEvent(self, event):
        if self._execute_action_drop_(event) is True:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        menu_raw = [
            ('basic',),
            ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
            ('paste', None, (True, self.paste, False), QtGui.QKeySequence.Paste),
            ('cut', None, (True, self.cut, False), QtGui.QKeySequence.Cut),
            ('extend',),
            ('undo', None, (True, self.undo, False), QtGui.QKeySequence.Undo),
            ('redo', None, (True, self.redo, False), QtGui.QKeySequence.Redo),
            ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll),
        ]
        #
        if self.isReadOnly():
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('extend',),
                ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if self._entry_use_as_storage is True:
            menu_raw.extend(
                [
                    ('system',),
                    ('open folder', 'file/open-folder', (True, self._execute_open_in_system_, False),
                     QtGui.QKeySequence.Open)
                ]
            )
        #
        if menu_raw:
            self._qt_menu = _gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _set_drop_enable_(self, boolean):
        super(QtEntryAsTextEdit, self)._set_drop_enable_(boolean)
        self.setAcceptDrops(boolean)

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

    def _completion_value_auto_(self):
        if self._value_type in {int, float}:
            if not self.text():
                self._set_value_(0)
        elif self._entry_use_as_rgba is True:
            self._set_value_as_rgba_255_(self._get_value_as_rgba_255_())

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
            bsc_core.StgSystem.open(_)

    def _set_use_as_storage_(self, boolean=True):
        super(QtEntryAsTextEdit, self)._set_use_as_storage_(boolean)
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

    def _set_use_as_rgba_255_(self, boolean=False):
        super(QtEntryAsTextEdit, self)._set_use_as_rgba_255_(boolean)
        if boolean is True:
            self._set_validator_use_as_rgba_()

    def _set_validator_use_as_rgba_(self):
        reg = QtCore.QRegExp(r'^[0-9,]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_validator_use_as_name_(self):
        reg = QtCore.QRegExp(r'^[a-zA-Z0-9_]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_validator_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())
        self._completion_value_auto_()

    def _set_validator_use_as_float_(self):
        self.setValidator(QtGui.QDoubleValidator())
        self._completion_value_auto_()

    def _set_value_validator_use_as_frames_(self):
        self._set_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9-,:]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_value_validator_use_as_rgba_(self):
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
        # do not encode output, use original data
        if self._value_type == str:
            # if isinstance(_, six.text_type):
            #     _ = _.encode('utf-8')
            return _
        elif self._value_type == int:
            return int(_ or 0)
        elif self._value_type == float:
            return float(_ or 0)
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

    def _set_value_as_rgba_255_(self, rgba):
        if isinstance(rgba, (tuple, list)):
            text = ','.join(map(lambda x: str(int(x)), rgba))
            self.setText(text)

    def _get_value_as_rgba_255_(self):
        text = self.text()
        _ = map(lambda x: max(min(int(x), 255), 0) if x else 255, map(lambda x: str(x).strip(), text.split(',')))
        c = len(_)
        if c == 4:
            return tuple(_)
        elif c > 4:
            return tuple(_[:4])
        elif c < 4:
            return tuple([_[i] if i < c else 255 for i in range(4)])
        return 255, 255, 255, 255

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
        super(QtEntryAsTextEdit, self)._set_entry_enable_(boolean)
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


# base entry for content
class QtEntryAsContentEdit(
    QtWidgets.QTextEdit,
    gui_qt_abstract.AbsQtEntryBaseDef,
    gui_qt_abstract.AbsQtDropBaseDef,
):
    focus_in = qt_signal()
    focus_out = qt_signal()
    focus_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryAsContentEdit, self).__init__(*args, **kwargs)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.installEventFilter(self)
        # self.setAcceptRichText(False)
        # self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        #
        self.setFont(QtFonts.Content)
        qt_palette = GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self._print_signals = QtPrintSignals(self)
        #
        self._print_signals.print_add_accepted.connect(self._add_value_)
        self._print_signals.print_over_accepted.connect(self._set_value_)
        #
        self.setStyleSheet(
            GuiQtStyle.get('QTextEdit')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            GuiQtStyle.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            GuiQtStyle.get('QScrollBar')
        )
        self._init_entry_base_def_(self)
        self._init_drop_base_def_(self)

        self._empty_icon_name = None
        self._empty_text = None

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
                #
                self.focus_in.emit()
                self.focus_changed.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(False)
                #
                self.focus_out.emit()
                self.focus_changed.emit()
            elif event.type() == QtCore.QEvent.Wheel:
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    self._execute_font_scale_(event)
                    return True
        return False

    def paintEvent(self, event):
        if not self.toPlainText():
            painter = QtPainter(self.viewport())
            if self._empty_text:
                painter._draw_empty_text_by_rect_(
                    rect=self.rect(),
                    text=self._empty_text,
                    draw_drop_icon=True,
                )
            else:
                painter._draw_empty_image_by_rect_(
                    rect=self.rect(),
                    icon_name=self._empty_icon_name,
                )

        super(QtEntryAsContentEdit, self).paintEvent(event)

    def contextMenuEvent(self, event):
        menu_raw = [
            ('basic',),
            ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
            ('paste', None, (True, self.paste, False), QtGui.QKeySequence.Paste),
            ('cut', None, (True, self.cut, False), QtGui.QKeySequence.Cut),
            ('extend',),
            ('undo', None, (True, self.undo, False), QtGui.QKeySequence.Undo),
            ('redo', None, (True, self.redo, False), QtGui.QKeySequence.Redo),
            ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll),
        ]
        if self.isReadOnly():
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('extend',),
                ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if menu_raw:
            self._qt_menu = _gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _execute_font_scale_(self, event):
        delta = event.angleDelta().y()
        font = self.font()
        size_pre = font.pointSize()
        if delta > 0:
            size_cur = size_pre+1
        else:
            size_cur = size_pre-1
        #
        size_cur = max(min(size_cur, 64), 6)
        font.setPointSize(size_cur)
        self.setFont(font)
        self.update()

    def _append_content_(self, text):
        def add_fnc_(text_):
            if isinstance(text_, six.text_type):
                text_ = text_.encode('utf-8')

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

    def _add_value_with_thread_(self, text):
        self._print_signals.print_add_accepted.emit(text)

    def _set_value_with_thread_(self, text):
        self._print_signals.print_over_accepted.emit(text)

    def _get_value_(self):
        return self.toPlainText()

    def _add_value_(self, value):
        def add_fnc_(value_):
            if isinstance(value_, six.text_type):
                value_ = value_.encode('utf-8')
            #
            self.moveCursor(QtGui.QTextCursor.End)
            self.insertPlainText(value_+'\n')

        #
        if isinstance(value, (tuple, list)):
            [add_fnc_(i) for i in value]
        else:
            add_fnc_(value)
        #
        self.update()

    def _set_value_(self, value):
        if value is not None:
            if isinstance(value, six.text_type):
                value = value.encode('utf-8')
            #
            self.setText(
                value
            )
        else:
            self.setText('')

    def _set_empty_text_(self, text):
        self._empty_text = text

    def _set_entry_enable_(self, boolean):
        super(QtEntryAsContentEdit, self)._set_entry_enable_(boolean)
        self.setReadOnly(not boolean)

    def dropEvent(self, event):
        self._execute_action_drop_(event)

    def _execute_action_drop_(self, event):
        if self._action_drop_is_enable is True:
            data = event.mimeData()
            if data.hasUrls():
                urls = event.mimeData().urls()
                if urls:
                    for i_url in urls:
                        i_path = i_url.toLocalFile()
                        if bsc_core.StgPathMtd.get_is_file(i_path) is True:
                            i_file_opt = bsc_core.StgFileOpt(i_path)
                            i_data = i_file_opt.set_read()
                            self.insertPlainText(i_data)
                    event.accept()
        else:
            event.ignore()

    def insertFromMimeData(self, data):
        # add data as clear
        if data.text():
            self.insertPlainText(data.text())


class QtEntryAsConstantChoose(gui_qt_abstract.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(QtEntryAsConstantChoose, self).__init__(*args, **kwargs)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.ListMode)
        self.setPalette(GuiQtDcc.generate_qt_palette())

    def paintEvent(self, event):
        pass

    def _compute_height_maximum_(self, row_maximum, includes=None):
        adjust = 1+8
        if includes is not None:
            rects = [self.visualItemRect(i) for i in includes[:row_maximum]]
        else:
            rects = [self.visualItemRect(self.item(i)) for i in range(self.count())[:row_maximum]]
        if rects:
            return sum([i.height() for i in rects])+adjust
        return 20+adjust


class QtEntryAsIconChoose(gui_qt_abstract.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(QtEntryAsIconChoose, self).__init__(*args, **kwargs)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setPalette(GuiQtDcc.generate_qt_palette())

    def _compute_height_maximum_(self, row_maximum, includes=None):
        # w, h = self.viewport().width(), self.viewport().height()
        c_w, c_h = self.gridSize().width(), self.gridSize().height()
        # print w, c_w
        # row_count = int(w/c_w)
        # print row_count
        adjust = 1+5
        return c_h*row_maximum+adjust


# base entry for list
class QtEntryAsList(
    gui_qt_abstract.AbsQtListWidget,
    gui_qt_abstract.AbsQtHelpDef,
    #
    gui_qt_abstract.AbsQtEntryExtraDef,
    gui_qt_abstract.AbsQtValuesDef,
    #
    gui_qt_abstract.AbsQtEntryBaseDef,
    #
    gui_qt_abstract.AbsQtDropBaseDef,
):
    entry_changed = qt_signal()
    entry_added = qt_signal()
    entry_deleted = qt_signal()
    #
    user_entry_changed = qt_signal()
    user_entry_cleared = qt_signal()
    user_entry_finished = qt_signal()
    # for popup choose
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()
    key_enter_pressed = qt_signal()
    #
    user_input_method_event_changed = qt_signal(object)

    #
    def _get_value_(self):
        pass

    def __init__(self, *args, **kwargs):
        super(QtEntryAsList, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.viewport().installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
        self.setSelectionMode(self.ExtendedSelection)
        #
        self._item_width, self._item_height = 20, 20
        self._grid_size = 20, 20

        self._set_help_def_init_(self)
        #
        self._init_entry_extra_def_(self)
        self._set_values_def_init_(self)
        #
        self._init_entry_base_def_(self)
        self._init_drop_base_def_(self)

        self.setAcceptDrops(self._action_drop_is_enable)

        self._set_shortcut_register_()

        self._item_icon_file_path = None

        self._empty_icon_name = 'placeholder/default'
        self._empty_text = None

    def contextMenuEvent(self, event):
        if self._entry_is_enable is True:
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self._do_action_copy_, False), QtGui.QKeySequence.Copy),
                ('paste', None, (True, self._do_action_paste_, False), QtGui.QKeySequence.Paste),
                ('cut', None, (True, self._do_action_cut_, False), QtGui.QKeySequence.Cut),
                ('extend',),
                ('select all', None, (True, self._do_action_select_all_, False), QtGui.QKeySequence.SelectAll),
            ]
        else:
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self._do_action_copy_, False), QtGui.QKeySequence.Copy),
                ('extend',),
                ('select all', None, (True, self._do_action_select_all_, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        items = self._get_selected_items_()
        if items:
            menu_raw.append(
                ('open folder', 'file/open-folder', (True, self._execute_open_in_system_, False),
                 QtGui.QKeySequence.Open)
            )
        #
        if menu_raw:
            self._qt_menu = _gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

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
            elif event.type() == QtCore.QEvent.Resize:
                pass
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
        #
        elif widget == self.verticalScrollBar():
            pass
        #
        elif widget == self.viewport():
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_viewport_showable_auto_()
                self._refresh_all_item_widgets_()
        return False

    def paintEvent(self, event):
        if not self.count():
            painter = QtPainter(self.viewport())
            if self._empty_text:
                painter._draw_empty_text_by_rect_(
                    rect=self.rect(),
                    text=self._empty_text,
                    text_sub=self._empty_sub_text,
                    draw_drop_icon=self._action_drop_is_enable
                )
            else:
                painter._draw_empty_image_by_rect_(
                    rect=self.rect(),
                    icon_name=self._empty_icon_name,
                )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self._entry_use_as_storage is True:
            if event.mimeData().hasUrls:
                # event.setDropAction(QtCore.Qt.CopyAction)
                event.accept()
                return
            event.ignore()
            return
        event.ignore()
        return

    def dropEvent(self, event):
        self._execute_action_drop_(event)

    def _execute_open_in_system_(self):
        item = self._get_item_current_()
        if item is not None:
            item_widget = self.itemWidget(item)
            if item_widget is not None:
                value = item_widget._get_value_()
                bsc_core.StgPathOpt(value).open_in_system()

    def _set_shortcut_register_(self):
        actions = [
            (self._do_action_copy_, 'Ctrl+C'),
            (self._do_action_paste_, 'Ctrl+V'),
            (self._do_action_cut_, 'Ctrl+X'),
            (self._do_action_select_all_, 'Ctrl+A')
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

    def _do_action_copy_(self):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            values = [i._get_value_() for i in selected_item_widgets]
            QtWidgets.QApplication.clipboard().setText(
                '\n'.join(values)
            )

    def _do_action_cut_(self):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            values = [i._get_value_() for i in selected_item_widgets]
            QtWidgets.QApplication.clipboard().setText(
                '\n'.join(values)
            )
            [self._delete_value_(i) for i in values]

    def _do_action_paste_(self):
        text = QtWidgets.QApplication.clipboard().text()
        if text:
            values = [i.strip() for i in text.split('\n')]
            for i_value in values:
                if self._get_value_is_valid_(i_value):
                    self._append_value_(i_value)

    def _do_action_select_all_(self):
        self._set_all_items_selected_(True)

    def _get_selected_item_widgets_(self):
        return [self.itemWidget(i) for i in self.selectedItems()]

    def _set_drop_enable_(self, boolean):
        super(QtEntryAsList, self)._set_drop_enable_(boolean)
        self.setAcceptDrops(boolean)
        # self.setDragDropMode(self.DropOnly)
        # self.setDropIndicatorShown(True)

    def _execute_action_drop_(self, event):
        data = event.mimeData()
        if self._entry_use_as_storage is True:
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
                    if self._entry_use_as_file_multiply is True:
                        values = bsc_core.StgFileMultiplyMtd.merge_to(
                            values,
                            ['*.<udim>.####.*', '*.####.*']
                        )
                    #
                    [self._append_value_(i) for i in values]
                    event.accept()
        else:
            event.ignore()

    # noinspection PyUnusedLocal
    def _execute_action_delete_(self, event):
        item_widgets_selected = self._get_selected_item_widgets_()
        if item_widgets_selected:
            for i in item_widgets_selected:
                i_value = i._get_value_()
                self._delete_value_(i_value, False)
            #
            self._refresh_viewport_showable_auto_()

    def _delete_values_(self, values):
        [self._delete_value_(i, False) for i in values]
        self._refresh_viewport_showable_auto_()

    def _delete_value_(self, value, auto_refresh_showable=True):
        if value:
            if self._entry_is_enable is True:
                index = self._values.index(value)
                self._values.remove(value)
                #
                item = self.item(index)
                # delete item widget
                self._delete_item_widget_(item)
                # delete item
                self.takeItem(index)
                self.entry_deleted.emit()
        #
        if auto_refresh_showable is True:
            self._refresh_viewport_showable_auto_()

    def _append_value_(self, value):
        # use original value, do not encode
        if value and value not in self._values:
            self._values.append(value)
            self._create_value_item_(value)
            self.entry_added.emit()

    def _insert_value_(self, value, index):
        # use original value, do not encode
        if value and value not in self._values:
            pass

    def _extend_values_(self, values):
        if values:
            for i_value in values:
                self._append_value_(i_value)

    def _clear_all_values_(self):
        self._values = []
        self._set_clear_()

    def _item_show_deferred_fnc_(self, data):
        item_widget, value = data
        item_widget._set_name_text_(value)
        item_widget._set_tool_tip_(value)
        if self._item_icon_file_path is not None:
            item_widget._set_icon_file_path_(self._item_icon_file_path)
        else:
            item_widget._set_icon_name_text_(value)

    def _create_value_item_(self, value):
        def cache_fnc_():
            return [item_widget, value]

        def build_fnc_(data):
            self._item_show_deferred_fnc_(data)

        def delete_fnc_():
            self._delete_value_(value)

        item_widget = _gui_qt_wgt_utility._QtHItem()
        item_widget._set_value_(value)
        item_widget._set_delete_enable_(True)
        item_widget.delete_press_clicked.connect(delete_fnc_)
        item = _gui_qt_wgt_utility.QtListWidgetItem()
        w, h = self._grid_size
        item.setSizeHint(QtCore.QSize(w, h))
        self.addItem(item)
        item._connect_item_show_()
        self.setItemWidget(item, item_widget)
        item._set_item_show_fnc_(
            cache_fnc_, build_fnc_
        )
        item_widget._refresh_widget_all_()

    def _set_clear_(self):
        super(QtEntryAsList, self)._set_clear_()
        self._values = []

    def _set_values_(self, values):
        self._set_clear_()
        [self._append_value_(i) for i in values]

    def _set_item_icon_file_path_(self, file_path):
        self._item_icon_file_path = file_path

    def _set_use_as_storage_(self, boolean):
        super(QtEntryAsList, self)._set_use_as_storage_(boolean)
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


# base entry as bubbles
class QtEntryAsBubbles(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtWidgetBaseDef
):
    bubble_text_change_accepted = qt_signal(str)
    bubble_text_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryAsBubbles, self).__init__(*args, **kwargs)
        self._bubble_layout = _gui_qt_wgt_utility.QtHBoxLayout(self)
        self._bubble_layout.setContentsMargins(*[0]*4)
        self._bubble_layout.setSpacing(1)

        self._bubble_constant_entry = None
        self._bubble_texts = []

    def _set_bubble_constant_entry_(self, widget):
        self._bubble_constant_entry = widget

    def _create_value_item_(self, text):
        texts = self._get_all_bubble_texts_()
        if text and text not in texts:
            self._append_value_(text)
            #
            bubble = _gui_qt_wgt_utility.QtTextBubble()
            self._bubble_layout.addWidget(bubble)
            bubble._set_bubble_text_(text)
            bubble.delete_text_accepted.connect(self._delete_value_)

            if self._bubble_constant_entry is not None:
                self._bubble_constant_entry._set_clear_()

    def _append_value_(self, text):
        self._bubble_texts.append(text)
        #
        self.bubble_text_change_accepted.emit(text)
        self.bubble_text_changed.emit()

    def _delete_value_(self, text):
        self._bubble_texts.remove(text)
        #
        self.bubble_text_change_accepted.emit(text)
        self.bubble_text_changed.emit()

    def _execute_bubble_backspace_(self):
        # when bubble text widget delete, send emit do self._delete_value_(text)
        self._bubble_layout._delete_latest_()

    def _get_all_bubble_texts_(self):
        return self._bubble_texts

    def _clear_all_values_(self):
        self._bubble_texts = []
        self._bubble_layout._clear_all_widgets_()


# base entry as capsule, can be select one and more
class QtEntryAsCapsule(
    QtWidgets.QWidget,

    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtNameBaseDef,

    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,

    gui_qt_abstract.AbsQtEntryExtraDef,
    gui_qt_abstract.AbsQtValueDefaultBaseDef,
):
    value_changed = qt_signal()
    user_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryAsCapsule, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.installEventFilter(self)
        #
        self._init_name_base_def_(self)
        self._init_frame_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._init_entry_extra_def_(self)
        self._init_value_default_base_def_()

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
        self._capsule_checked_indices = []

        self._capsule_height = 18

    def _set_capsule_strings_(self, texts):
        self._capsule_texts = texts
        c = len(texts)
        self._capsule_indices = range(c)
        self._capsule_draw_rects = []
        self._capsule_draw_texts = []
        self._capsule_checked_indices = []
        for i_index in self._capsule_indices:
            self._capsule_draw_rects.append(QtCore.QRect())
            # noinspection PyArgumentEqualDefault
            self._capsule_draw_texts.append(
                bsc_core.RawTextMtd.to_prettify(texts[i_index], capitalize=True)
            )
            self._capsule_checked_indices.append(False)
        #
        self._refresh_widget_draw_()

    def _set_value_(self, value):
        if self._capsule_use_exclusive:
            index = self._capsule_texts.index(value)
            self._capsule_index_current = index
            self._capsule_checked_indices = [True if i in [index] else False for i in self._capsule_indices]
        else:
            if value:
                indices = [self._capsule_texts.index(i) for i in value if i in self._capsule_texts]
                self._capsule_index_current = indices[0]
                self._capsule_checked_indices = [True if i in indices else False for i in self._capsule_indices]

        self._update_value_current_()
        #
        self._refresh_widget_draw_()

    def _get_value_(self):
        return self._capsule_value_current

    def _get_value_fnc_(self):
        _ = [self._capsule_texts[i] for i in self._capsule_indices if self._capsule_checked_indices[i] is True]
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
            self._capsule_per_width = w+(w%2)+4
            for i, i_text in enumerate(self._capsule_texts):
                i_x, i_y = x+i*self._capsule_per_width, y
                i_w, i_h = self._capsule_per_width, h
                self._capsule_draw_rects[i].setRect(
                    x+i_x, y+(h-c_h)/2, i_w, c_h
                )

    def _do_capsule_hover_move_(self, event):
        if self._action_is_enable is False:
            return
        if not self._capsule_per_width:
            return
        p = event.pos()
        x, y = p.x(), p.y()
        self._capsule_hovered_index = int(x/self._capsule_per_width)
        self._refresh_widget_draw_()

    def _do_capsule_press_start_(self, event):
        if self._action_is_enable is False:
            return
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
                    self._capsule_checked_indices[index_pre] = False
                self._capsule_checked_indices[self._capsule_index_current] = True
            else:
                self._capsule_checked_indices[self._capsule_index_current] = not self._capsule_checked_indices[
                    self._capsule_index_current]

            self._capsule_press_state = self._capsule_checked_indices[self._capsule_index_current]

            self._update_value_current_()

    def _do_capsule_press_move_(self, event):
        if self._action_is_enable is False:
            return
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
                        self._capsule_checked_indices[index_pre] = False
                    self._capsule_checked_indices[self._capsule_index_current] = True
                else:
                    self._capsule_checked_indices[self._capsule_index_current] = self._capsule_press_state
                #
                self._update_value_current_()

    def _do_capsule_press_end_(self, event):
        if self._action_is_enable is False:
            return
        self._capsule_pressed_index = None
        event.accept()

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
            # press
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_capsule_press_start_(event)
                    self._set_action_flag_(
                        self.ActionFlag.Press
                    )
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_capsule_press_start_(event)
                    self._set_action_flag_(
                        self.ActionFlag.Press
                    )
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._get_action_flag_is_match_(self.ActionFlag.Press):
                    self._do_capsule_press_move_(event)
                #
                self._do_capsule_hover_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._do_capsule_press_end_(event)
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._capsule_texts:
            painter._draw_capsule_by_rects_(
                rects=self._capsule_draw_rects,
                texts=self._capsule_draw_texts,
                checked_indices=self._capsule_checked_indices,
                index_hover=self._capsule_hovered_index,
                index_press=self._capsule_pressed_index,
                use_exclusive=self._capsule_use_exclusive,
                is_enable=self._action_is_enable
            )

    def _set_value_entry_enable_(self, boolean):
        self._set_action_enable_(boolean)


# base entry frame
class QtEntryFrame(
    QtWidgets.QWidget,
    #
    gui_qt_abstract.AbsQtNameBaseDef,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtStatusBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtThreadBaseDef,
):
    geometry_changed = qt_signal(int, int, int, int)
    entry_focus_in = qt_signal()
    entry_focus_out = qt_signal()
    entry_focus_changed = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        # int left， int top， int right， int bottom
        m_l, m_t, m_r, m_b = self._frame_draw_margins
        #
        c = self._entry_count
        #
        frm_x, frm_y = x+m_l+1, y+m_t+1
        frm_w, frm_h = w-m_l-m_r-2, h-m_t-m_b-2
        #
        self._frame_draw_rect.setRect(
            frm_x, frm_y, frm_w, frm_h
        )
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
        #
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
        self._is_hovered = False
        self._is_focused = False
        self._entry_count = 1
        #
        self._value_entry = None
        self._value_entries = []
        #
        self._init_name_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_status_base_def_(self)
        self._init_action_base_def_(self)
        self._init_thread_base_def_(self)
        #
        self._frame_border_color = QtBorderColors.Light
        self._hovered_frame_border_color = QtBorderColors.Hovered
        self._selected_frame_border_color = QtBorderColors.Selected
        self._frame_background_color = QtBackgroundColors.Dim

        self._resize_handle = _gui_qt_wgt_resize.QtVResizeHandle(self)
        self._resize_handle.hide()

        self._tip_draw_enable = False
        self._tip_text = None
        self._tip_draw_rect = QtCore.QRect()
        # self._resize_handle._set_resize_target_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
                self.geometry_changed.emit(
                    self.x(), self.y(), self.width(), self.height()
                )
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        is_selected = self._is_focused
        background_color = self._frame_background_color
        bdr_color = [QtBorderColors.Basic, QtBorderColors.HighLight][is_selected]
        bdr_w = [self._frame_border_draw_width, self._frame_border_draw_width+1][is_selected]
        for i_rect in self._frame_draw_rects:
            painter._draw_frame_by_rect_(
                i_rect,
                border_color=bdr_color,
                background_color=background_color,
                # border_radius=1,
                border_width=bdr_w,
                border_style=self._frame_border_draw_style
            )
        #
        if self._tip_draw_enable is True:
            if self._tip_text is not None:
                painter._draw_text_by_rect_(
                    rect=self._tip_draw_rect,
                    text=self._tip_text,
                    font_color=QtColors.TextDisable,
                    font=QtFonts.DefaultItalic,
                    text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                )
        #
        if self._thread_draw_is_enable is True:
            painter._draw_alternating_colors_by_rect_(
                rect=self._frame_draw_rect,
                colors=((0, 0, 0, 63), (0, 0, 0, 0)),
                # border_radius=4,
                running=True
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
