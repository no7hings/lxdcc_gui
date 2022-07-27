# coding=utf-8
import functools

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_chart

from lxutil_gui.qt import utl_gui_qt_abstract

from lxutil_gui.qt import utl_gui_qt_core


class QtLineEdit_(
    QtWidgets.QLineEdit,
    utl_gui_qt_abstract.AbsQtValueDef,
    #
    utl_gui_qt_abstract.AbsQtEntryDef,
    utl_gui_qt_abstract.AbsQtEntryDropDef,
):
    entry_changed = qt_signal()
    user_entry_changed = qt_signal()
    entry_finished = qt_signal()
    up_key_pressed = qt_signal()
    down_key_pressed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtLineEdit_, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setFont(Font.NAME)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._item_value_type = str
        #
        self._item_value_default = None
        #
        self._maximum = 1
        self._minimum = 0
        #
        self.returnPressed.connect(self._set_enter_finished_emit_send_)
        self.textEdited.connect(self._set_user_enter_changed_emit_send_)
        self.textChanged.connect(self._set_enter_changed_emit_send_)
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QLineEdit')
        )
        self._set_value_def_init_(self)
        self._set_entry_def_init_(self)
        self._set_entry_drop_def_init_(self)
        self.setAcceptDrops(self._entry_drop_is_enable)

    def _set_action_wheel_update_(self, event):
        if self._item_value_type in [int, float]:
            delta = event.angleDelta().y()
            pre_value = self._get_item_value_()
            if delta > 0:
                self._set_item_value_(pre_value+1)
            else:
                self._set_item_value_(pre_value-1)
            #
            self._set_enter_changed_emit_send_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    entry_frame._set_focused_(False)
                #
                self._set_value_completion_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._set_action_wheel_update_(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Up:
                    self.up_key_pressed.emit()
                if event.key() == QtCore.Qt.Key_Down:
                    self.down_key_pressed.emit()
        return False

    def _set_entry_drop_enable_(self, boolean):
        super(QtLineEdit_, self)._set_entry_drop_enable_(boolean)
        self.setAcceptDrops(boolean)

    def _set_action_drop_execute_(self, event):
        data = event.mimeData()
        if data.hasUrls():
            urls = event.mimeData().urls()
            if urls:
                value = urls[0].toLocalFile()
                if self._get_value_is_valid_(value):
                    self._set_item_value_(value)
                    return True
        return False

    def dropEvent(self, event):
        if self._set_action_drop_execute_(event) is True:
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
                    ('show in system', None, (True, self._set_open_in_system_, False), QtGui.QKeySequence.Open)
                ]
            )
        #
        if menu_raw:
            self._qt_menu = _utl_gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_raw_(menu_raw)
            self._qt_menu._set_show_()

    def _set_enter_finished_emit_send_(self):
        # noinspection PyUnresolvedReferences
        self.entry_finished.emit()

    def _set_enter_changed_emit_send_(self):
        # noinspection PyUnresolvedReferences
        self.entry_changed.emit()

    def _set_user_enter_changed_emit_send_(self):
        # noinspection PyUnresolvedReferences
        self.user_entry_changed.emit()

    def _set_value_completion_(self):
        if self._item_value_type in [int, float]:
            if not self.text():
                self._set_item_value_(0)

    def _set_item_value_type_(self, value_type):
        self._item_value_type = value_type
        if self._item_value_type is None:
            pass
        elif self._item_value_type is str:
            pass
            # self._set_use_as_string_()
        elif self._item_value_type is int:
            self._set_use_as_integer_()
        elif self._item_value_type is float:
            self._set_use_as_float_()

    def _get_item_value_type_(self):
        return self._item_value_type

    def _set_open_in_system_(self):
        _ = self.text()
        if _:
            bsc_core.StoragePathOpt(_).set_open_in_system()

    def _set_entry_use_as_storage_(self, boolean=True):
        super(QtLineEdit_, self)._set_entry_use_as_storage_(boolean)
        if boolean is True:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                self._set_open_in_system_
            )
            i_action.setShortcut(
                QtGui.QKeySequence.Open
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)

    def _set_use_as_string_(self):
        reg = QtCore.QRegExp(r'^[a-zA-Z0-9_]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #     )
        # )

    def _set_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())
        self._set_value_completion_()
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         '"MMB-wheel" to modify "int" value'
        #     )
        # )

    def _set_use_as_float_(self):
        self.setValidator(QtGui.QDoubleValidator())
        self._set_value_completion_()
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         '"MMB-wheel" to modify "float" value'
        #     )
        # )

    def _set_use_as_frames_(self):
        self._set_item_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9-,]+$')
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

    def _set_use_as_rgba_(self):
        self._set_item_value_type_(str)
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

    def _get_item_value_(self):
        _ = self.text()
        if self._item_value_type == str:
            return _
        elif self._item_value_type == int:
            return int(_)
        elif self._item_value_type == float:
            return float(_)
        return _

    def _set_item_value_(self, value):
        if value is not None:
            self.setText(
                str(
                    self._item_value_type(value)
                ).encode("UTF8")
            )
        else:
            self.setText('')

    def _get_item_value_default_(self):
        return self._item_value_default

    def _set_focused_connect_to_(self, widget):
        pass
    #
    def _get_is_selected_(self):
        boolean = False
        if self.selectedText():
            boolean = True
        return boolean

    def _set_item_value_clear_(self):
        self._set_item_value_('')

    def _set_enter_enable_(self, boolean):
        self.setReadOnly(not boolean)

    def _set_focused_(self, boolean):
        if boolean is True:
            self.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self.setFocus(
                QtCore.Qt.NoFocusReason
            )


class _QtListWidget(
    utl_gui_qt_abstract.AbsQtListWidget,
    utl_gui_qt_abstract.AbsQtHelpDef,
    #
    utl_gui_qt_abstract.AbsQtValueDef,
    utl_gui_qt_abstract.AbsQtValuesDef,
    #
    utl_gui_qt_abstract.AbsQtEntryDef,
    utl_gui_qt_abstract.AbsQtEntryDropDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtListWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setSelectionMode(self.ExtendedSelection)
        #
        self._item_width, self._item_height = 20, 20

        self._set_help_def_init_(self)
        #
        self._set_value_def_init_(self)
        self._set_values_def_init_(self)
        #
        self._set_entry_def_init_(self)
        self._set_entry_drop_def_init_(self)

        self.setAcceptDrops(self._entry_drop_is_enable)

        self._set_shortcut_register_()

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
        item_current = self._get_item_current_()
        if item_current:
            menu_raw.append(
                ('show in system', None, (True, self._set_open_in_system_, False), QtGui.QKeySequence.Open)
            )
        #
        if menu_raw:
            self._qt_menu = _utl_gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_raw_(menu_raw)
            self._qt_menu._set_show_()

    def _set_open_in_system_(self):
        item = self._get_item_current_()
        if item is not None:
            item_widget = self.itemWidget(item)
            if item_widget is not None:
                _ = item_widget._get_name_text_()
                bsc_core.StoragePathOpt(_).set_open_in_system()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = True
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = False
                elif event.key() == QtCore.Qt.Key_Delete:
                    self._set_action_delete_execute_(event)
            elif event.type() == QtCore.QEvent.Wheel:
                pass
                # self._set_action_wheel_update_(event)
            elif event.type() == QtCore.QEvent.Resize:
                self._set_show_view_items_update_()
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    entry_frame._set_focused_(False)
        if widget == self.verticalScrollBar():
            pass
        return False

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
        self._set_action_drop_execute_(event)

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
            [self._set_values_append_(i) for i in values]

    def _set_action_cut_(self):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            values = [i._get_name_text_() for i in selected_item_widgets]
            QtWidgets.QApplication.clipboard().setText(
                '\n'.join(values)
            )
            [self._set_values_remove_(i) for i in values]

    def _set_action_select_all_(self):
        self._set_all_items_selected_(True)

    def _get_selected_item_widgets_(self):
        return [self.itemWidget(i) for i in self.selectedItems()]

    def _set_entry_drop_enable_(self, boolean):
        super(_QtListWidget, self)._set_entry_drop_enable_(boolean)
        self.setAcceptDrops(boolean)
        # self.setDragDropMode(self.DropOnly)
        # self.setDropIndicatorShown(True)

    def _set_action_drop_execute_(self, event):
        data = event.mimeData()
        if data.hasUrls():
            urls = event.mimeData().urls()
            if urls:
                for i_url in urls:
                    i_value = i_url.toLocalFile()
                    if self._get_value_is_valid_(i_value):
                        self._set_values_append_(i_value)

    def _set_action_delete_execute_(self, event):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            for i in selected_item_widgets:
                i_value = i._get_name_text_()
                self._set_values_remove_(i_value)

    def _set_values_remove_(self, value):
        if value:
            if self._entry_is_enable is True:
                if value in self._values:
                    index = self._values.index(value)
                    self._values.remove(value)
                    #
                    item = self.item(index)
                    self._set_item_widget_delete_(item)
                    self.takeItem(index)

                # print self._values

    def _set_item_show_deferred_(self, data):
        item_widget, value = data
        item_widget._set_name_text_(value)
        # item_widget._set_icon_name_text_(value)
        item_widget._set_tool_tip_(value)

    def _set_item_add_(self, value):
        def cache_fnc_():
            return [item_widget, value]

        def build_fnc_(data):
            self._set_item_show_deferred_(data)

        def delete_fnc_():
            self._set_values_remove_(value)

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

    def _set_values_append_(self, value):
        if value:
            if self._entry_is_enable is True:
                if value not in self._values:
                    self._values.append(value)
                    #
                    self._set_item_add_(value)

        # print self._values

    def _set_values_(self, values):
        self._set_clear_()
        [self._set_values_append_(i) for i in values]

    def _set_value_icon_file_path_(self, file_path):
        pass

    def _set_entry_use_as_storage_(self, boolean):
        super(_QtListWidget, self)._set_entry_use_as_storage_(boolean)
        if boolean is True:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                self._set_open_in_system_
            )
            i_action.setShortcut(
                QtGui.QKeySequence.Open
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)


class QtTextBrowser_(
    QtWidgets.QTextBrowser,
    utl_gui_qt_abstract.AbsQtEntryDef,
):
    def __init__(self, *args, **kwargs):
        super(QtTextBrowser_, self).__init__(*args, **kwargs)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.installEventFilter(self)
        # self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        #
        self.setFont(Font.CONTENT)
        qt_palette = QtDccMtd.get_qt_palette()
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
        self._set_entry_def_init_(self)

    def _set_content_add_(self, text):
        def add_fnc_(text_):
            self.moveCursor(QtGui.QTextCursor.End)
            self.insertPlainText(text_ + '\n')
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
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility._QtEntryFrame):
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
            self._qt_menu._set_menu_raw_(menu_raw)
            self._qt_menu._set_show_()

    def _get_item_value_(self):
        return self.toPlainText()

    def _set_item_value_(self, value):
        if value is not None:
            self.setText(
                unicode(value).encode('utf-8')
            )
        else:
            self.setText('')


class _QtTextItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
):
    def _set_wgt_update_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtTextItem, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_name_def_init_()
        self.setFont(self._name_text_font)
        self._name_text_option = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        if self._name_align == self.AlignRegion.Top:
            f_w, f_h = self._name_frame_size
            t_w, t_h = self._name_draw_size
            self._name_draw_rect.setRect(
                x, y+(f_h-t_h)/2, w, t_h
            )
        else:
            self._name_draw_rect.setRect(
                x, y, w, h
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_action_hover_filter_execute_(event)
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        self._set_wgt_update_geometry_()
        # name
        if self._name_text is not None:
            text_color = [self._name_color, self._hover_name_color][self._action_is_hovered]
            #
            painter._set_text_draw_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font_color=text_color,
                font=self._name_text_font,
                text_option=self._name_text_option,
            )


class _QtInfoItem(QtWidgets.QWidget):
    pass


class _QtIconPressItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
):
    clicked = qt_signal()
    db_clicked = qt_signal()
    #
    QT_MENU_CLASS = _utl_gui_qt_wgt_utility.QtMenu
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        f_w, f_h = self._icon_frame_size
        #
        i_f_w, i_f_h = self._icon_file_draw_size
        s_i_f_w, s_i_f_h = self._sub_icon_file_draw_size
        i_c_w, i_c_h = self._icon_color_draw_size
        i_n_w, i_n_h = self._icon_name_draw_size
        # check
        _w, _h = w, h
        _x, _y = x, y
        if self._icon_is_enable is True:
            _x, _y = _x + (w - f_w)/2, _y + (h - f_h)/2
            self._icon_frame_rect.setRect(
                _x, _y, f_w, f_h
            )
            self._icon_file_draw_rect.setRect(
                _x+(f_w-i_f_w)/2, _y+(f_h-i_f_h)/2, i_f_w, i_f_h
            )
            self._sub_icon_file_draw_rect.setRect(
                _x+_w-s_i_f_w, _y+_h-s_i_f_h, s_i_f_w, s_i_f_h
            )
            self._icon_color_draw_rect.setRect(
                _x + (f_w - i_c_w)/2, _y + (f_h - i_c_h)/2, i_c_w, i_c_h
            )
            self._icon_name_draw_rect.setRect(
                _x + (f_w - i_n_w)/2, _y + (f_h - i_n_h)/2, i_n_w, i_n_h
            )
            _x += f_h
            _w -= f_w

        s_w, s_h = w*.5, w*.5
        self._action_state_rect.setRect(
            x, y+h-s_h, s_w, s_h
        )

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
        self._set_action_def_init_(self)
        self._set_action_hover_def_init_()
        self._set_action_press_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                self._set_action_hover_filter_execute_(event)
                #
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_action_pressed_(True)
                        self._set_action_flag_(self.ActionFlag.PressClick)
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_action_pressed_(True)
                        self.db_clicked.emit()
                        self._set_action_flag_(self.ActionFlag.PressDbClick)
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if event.button() == QtCore.Qt.LeftButton:
                        if self._get_action_press_flag_is_click_() is True:
                            self.clicked.emit()
                            self.press_clicked.emit()
                            self._set_menu_show_()
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                    #
                    self._set_action_hovered_(False)
                    self._set_action_pressed_(False)
                    self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        w, h = self.width(), self.height()
        i_w, i_h = self._icon_file_draw_size
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        self._set_wgt_update_geometry_()

        if self._get_action_is_enable_() is True:
            offset = self._get_action_offset_()
            #
            background_color = painter._get_item_background_color_1_by_rect_(
                self._icon_frame_rect,
                is_hovered=self._action_is_hovered,
                is_actioned=self._get_is_actioned_()
            )
            painter._set_frame_draw_by_rect_(
                self._icon_frame_rect,
                border_color=QtBorderColor.Transparent,
                background_color=background_color,
                border_radius=4,
                offset=offset
            )
        else:
            offset = 0
        # icon
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                icon_file_path = self._icon_file_path
                if self._action_is_hovered is True:
                    if self._hover_icon_file_path is not None:
                        icon_file_path = self._hover_icon_file_path
                #
                painter._set_icon_file_draw_by_rect_(
                    rect=self._icon_file_draw_rect,
                    file_path=icon_file_path,
                    offset=offset
                )
            elif self._icon_color_rgb is not None:
                painter._set_color_icon_draw_(
                    self._icon_color_draw_rect,
                    self._icon_color_rgb,
                    offset=offset
                )
            elif self._icon_name_text is not None:
                painter._set_icon_name_text_draw_by_rect_(
                    self._icon_name_draw_rect,
                    self._icon_name_text,
                    offset=offset,
                    border_radius=2,
                    is_hovered=self._action_is_hovered
                )
            #
            if self._sub_icon_file_path is not None:
                painter._set_icon_file_draw_by_rect_(
                    rect=self._sub_icon_file_draw_rect,
                    file_path=self._sub_icon_file_path,
                    offset=offset
                )
        #
        if self._action_state in [self.ActionState.Disable]:
            painter._set_icon_file_draw_by_rect_(
                self._action_state_rect,
                utl_gui_core.RscIconFile.get('state-disable')
            )


class _QtPressItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract._QtStatusDef,
    #
    utl_gui_qt_abstract.AbsQtSubProcessDef,
    utl_gui_qt_abstract.AbsQtValidatorDef,
    #
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtMenuDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract._QtProgressDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtActionCheckDef,
    utl_gui_qt_abstract._QtItemOptionPressActionDef,
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
        self._set_sub_process_def_init_()
        self._set_validator_def_init_(self)
        #
        self._set_icon_def_init_()
        self._set_name_def_init_()
        self._set_menu_def_init_()
        self._set_progress_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        self._set_action_check_def_init_()
        self._set_item_option_press_action_def_init_()
        #
        self._set_item_check_update_()
        #
        r, g, b = 167, 167, 167
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 151, 151, 151
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s*.75, v*.75)
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

        self._rate_timer = QtCore.QTimer(self)

        self._rate_timer.timeout.connect(self._set_sub_process_update_draw_)

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        check_enable = self._get_action_check_is_enable_()
        option_click_enable = self._get_item_option_click_enable_()
        status_is_enable = self._get_status_is_enable_()
        sub_process_is_enable = self._get_sub_process_is_enable_()
        validator_is_enable = self._get_validator_is_enable_()
        progress_enable = self._get_progress_is_enable_()
        #
        f_w, f_h = self._icon_frame_size
        #
        i_f_w, i_f_h = self._icon_file_draw_size
        i_c_w, i_c_h = self._icon_color_draw_size
        i_n_w, i_n_h = self._icon_name_draw_size
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
                _x + (f_w - i_f_w)/2, _y + (f_h - i_f_h)/2, i_f_w, i_f_h
            )
            _x += f_h
            _w -= f_w
            c_x += f_h
            c_w -= f_w
        #
        if self._icon_is_enable is True:
            self._icon_file_draw_rect.setRect(
                _x + (f_w - i_f_w)/2, _y + (f_h - i_f_h)/2, i_f_w, i_f_h
            )
            self._icon_color_draw_rect.setRect(
                _x + (f_w - i_c_w)/2, _y + (f_h - i_c_h)/2, i_c_w, i_c_h
            )
            self._icon_name_draw_rect.setRect(
                _x + (f_w - i_n_w)/2, _y + (f_h - i_n_h)/2, i_n_w, i_n_h
            )
            _x += f_h
            _w -= f_w
        # option
        if option_click_enable is True:
            self._option_click_rect.setRect(
                w - f_w, y, f_w, f_h
            )
            self._option_click_icon_rect.setRect(
                (w - f_w) + (f_w - i_f_w)/2, y + (f_h - i_f_h)/2, i_f_w, i_f_h
            )
            _w -= f_w
            c_w -= f_w
        #
        self._frame_draw_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._status_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._name_draw_rect.setRect(
            _x, _y, _w, _h
        )
        # progress
        if progress_enable is True:
            progress_percent = self._get_progress_percent_()
            self._progress_rect.setRect(
                c_x, c_y, c_w*progress_percent, 4
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
                c_x, c_h - e_h, c_w, e_h
            )

    def _set_sub_process_initialization_(self, count, status):
        super(_QtPressItem, self)._set_sub_process_initialization_(count, status)
        if count > 0:
            self._set_status_(
                self.Status.Started
            )
            self._rate_timer.start(1000)

    def _set_sub_process_finished_at_(self, index, status):
        super(_QtPressItem, self)._set_sub_process_finished_at_(index, status)
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

            self._rate_timer.stop()

        self._set_wgt_update_draw_()

    def _set_sub_process_finished_connect_to_(self, fnc):
        self.rate_finished.connect(fnc)

    def _set_sub_process_restore_(self):
        super(_QtPressItem, self)._set_sub_process_restore_()

        self._set_status_(
            self.Status.Stopped
        )

    def setText(self, text):
        self._name_text = text

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            # update rect first
            action_enable = self._get_action_is_enable_()
            check_enable = self._get_action_check_is_enable_()
            click_enable = self._get_action_press_is_enable_()
            option_click_enable = self._get_item_option_click_enable_()
            if event.type() == QtCore.QEvent.Resize:
                pass
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
                        (check_enable, self._item_check_frame_rect, self.ActionFlag.CheckClick),
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
                        self._set_item_check_swap_()
                        self.checked.emit()
                    elif self._action_flag == self.ActionFlag.PressClick:
                        self.clicked.emit()
                    elif self._action_flag == self.ActionFlag.OptionClick:
                        self.option_clicked.emit()
                    #
                    self._action_flag = None
                    self.update()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        self._set_wgt_update_geometry_()
        #
        offset = self._get_action_offset_()
        #
        if self._action_is_enable is True:
            border_color = [self._frame_border_color, self._hovered_frame_border_color][self._action_is_hovered]
            background_color = [self._frame_background_color, self._hovered_frame_background_color][self._action_is_hovered]
        else:
            border_color = QtBorderColor.ButtonDisable
            background_color = QtBackgroundColor.ButtonDisable
        #
        painter._set_frame_draw_by_rect_(
            self._frame_draw_rect,
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
        #
        if self._get_sub_process_is_enable_() is True:
            status_colors = [self._sub_process_status_colors, self._hover_sub_process_status_colors][self._action_is_hovered]
            painter._set_elements_status_draw_by_rect_(
                self._sub_process_status_rect,
                colors=status_colors,
                offset=offset,
                border_radius=2,
            )
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
            painter._set_frame_draw_by_rect_(
                self._progress_rect,
                border_color=QtBackgroundColor.Transparent,
                background_color=Color.PROGRESS,
                border_radius=2,
                offset=offset
            )
        # check
        if self._get_action_check_is_enable_() is True:
            painter._set_icon_file_draw_by_rect_(
                self._item_check_icon_rect,
                self._item_check_icon_file_path,
                offset=offset
            )
        # icon
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._set_icon_file_draw_by_rect_(
                    self._icon_file_draw_rect, self._icon_file_path, offset=offset
                )
            elif self._icon_color_rgb is not None:
                painter._set_color_icon_draw_(
                    self._icon_color_draw_rect, self._icon_color_rgb, offset=offset
                )
            elif self._icon_name_text is not None:
                painter._set_icon_name_text_draw_by_rect_(
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
                text_color = [QtFontColor.Basic, QtFontColor.Light][self._action_is_hovered]
            else:
                text_color = QtFontColor.Disable
            #
            if self._get_sub_process_is_enable_() is True:
                name_text = '{} - {}'.format(
                    self._name_text, self._get_sub_process_status_text_()
                )
            #
            painter._set_text_draw_by_rect_(
                self._name_draw_rect,
                text=name_text,
                font_color=text_color,
                font=Font.NAME,
                offset=offset
            )
        # option
        if self._get_item_option_click_enable_() is True:
            painter._set_icon_file_draw_by_rect_(
                self._option_click_icon_rect,
                self._option_icon_file_path,
                offset=offset
            )


class _QtCheckItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionCheckDef,
    #
    utl_gui_qt_abstract.AbsQtItemValueDefaultDef,
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
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_check_def_init_()
        #
        self._set_item_value_default_def_init_()
        #
        self._set_item_check_update_()

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        f_w, f_h = self._icon_frame_size
        i_w, i_h = self._icon_file_draw_size
        #
        self._set_frame_rect_(
            x, y, w-1, h-1
        )
        #
        self._set_item_check_frame_rect_(
            x, y, f_w, f_h
        )
        self._set_item_check_icon_rect_(
            x + (f_w - i_w)/2, y + (f_h - i_h)/2, i_w, i_h
        )
        x += f_w+spacing
        self._set_name_rect_(
            x, y, w-x, h
        )

    def _get_item_value_(self):
        return self._get_item_is_checked_()

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
                        self._set_item_check_action_run_()
                    #
                    self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_wgt_update_geometry_()
        #
        offset = self._get_action_offset_()
        #
        background_color = painter._get_item_background_color_1_by_rect_(
            self._item_check_frame_rect,
            is_hovered=self._action_is_hovered,
            is_actioned=self._get_is_actioned_()
        )
        painter._set_frame_draw_by_rect_(
            self._item_check_frame_rect,
            border_color=QtBorderColor.Transparent,
            background_color=background_color,
            border_radius=4,
            offset=offset
        )
        #
        if self._item_check_icon_file_path is not None:
            painter._set_icon_file_draw_by_rect_(
                rect=self._item_check_icon_rect,
                file_path=self._item_check_icon_file_path,
                offset=offset
            )
        #
        if self._name_text is not None:
            painter._set_text_draw_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=Font.NAME,
                font_color=QtFontColor.Basic,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )


class _QtStatusItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionCheckDef,
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
        self._set_icon_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_check_def_init_()
        #
        self._set_item_check_update_()

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        i_w, i_h = self._icon_color_draw_size
        self._set_color_icon_rect_(
            x + (w - i_w)/2, y + (h - i_h)/2, i_w, i_h
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
                        self._set_item_check_action_run_()
                #
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_wgt_update_geometry_()
        #
        offset = self._get_action_offset_()
        is_hovered = self._get_is_hovered_()
        #
        if self._get_item_is_checked_():
            background_color = [(255, 255, 63), (255, 127, 63)][is_hovered]
            painter._set_icon_name_text_draw_by_rect_(
                rect=self._icon_color_draw_rect,
                text='l',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered
            )
        else:
            background_color = [(71, 71, 71), (255, 127, 63)][is_hovered]
            painter._set_icon_name_text_draw_by_rect_(
                rect=self._icon_color_draw_rect,
                text='d',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered
            )


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
        self.setLineEdit(QtLineEdit_())
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
                utl_gui_core.RscIconFile.get('arrow_down'),
            )
        )

    def _set_entry_use_as_storage_(self, boolean=True):
        self.lineEdit()._set_entry_use_as_storage_(boolean)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    parent._set_focused_(False)
        return False


class _QtPopupListView(utl_gui_qt_abstract.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(_QtPopupListView, self).__init__(*args, **kwargs)
        self.setDragDropMode(QtWidgets.QListWidget.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.ListMode)
        self.setPalette(QtDccMtd.get_qt_palette())

    def paintEvent(self, event):
        pass

    def _get_maximum_height_(self, count_maximum):
        rects = [self.visualItemRect(self.item(i)) for i in range(self.count())[:count_maximum]]
        if rects:
            rect = rects[-1]
            y = rect.y()
            h = rect.height()
            return y+h+1+4
        return 20


class _QtItemRgbaChooseDropFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    def _set_wgt_update_draw_(self):
        self.update()
        self._chart.update()

    def __init__(self, *args, **kwargs):
        super(_QtItemRgbaChooseDropFrame, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setFocusProxy(self.parent())
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        #
        self._set_frame_def_init_()
        self._set_popup_def_init_(self)
        #
        self._frame_border_color = QtBackgroundColor.Light
        self._hovered_frame_border_color = QtBackgroundColor.Hovered
        self._selected_frame_border_color = QtBackgroundColor.Selected
        self._frame_background_color = QtBackgroundColor.Dark

        self._chart = _utl_gui_qt_wgt_chart._QtColorChooseChart(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self.parent():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_popup_close_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._set_popup_close_()
        elif widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._set_popup_end_()
            elif event.type() == QtCore.QEvent.Resize:
                self._set_wgt_update_geometry_()
            elif event.type() == QtCore.QEvent.Show:
                self._set_wgt_update_geometry_()
        return False

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w - 1, h - 1
        )
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        painter._set_popup_frame_draw_(
            bck_rect,
            margin=self._popup_margin,
            side=self._popup_side,
            shadow_radius=self._popup_shadow_radius,
            region=self._popup_region,
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
        )

    def _set_wgt_update_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius - 2
        #
        self._chart.setGeometry(
            v_x, v_y, v_w, v_h
        )
        self._chart.update()

    def _set_popup_start_(self):
        parent = self.parent()
        press_rect = parent._get_color_rect_()
        press_point = self._get_popup_press_point_(parent, press_rect)
        desktop_rect = get_qt_desktop_rect()
        self._set_popup_fnc_0_(
            press_point,
            press_rect,
            desktop_rect,
            320, 320
        )
        self._chart._set_color_rgba_(*parent._get_color_rgba_())
        parent._set_focused_(True)

    def _set_popup_end_(self, *args, **kwargs):
        r, g, b, a = self._chart._get_color_rgba_()
        self.parent()._set_color_rgba_(r, g, b, a)


class _QtConstantValueEntryItem(
    _utl_gui_qt_wgt_utility._QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    #
    utl_gui_qt_abstract.AbsQtItemValueTypeConstantEntryDef,
    utl_gui_qt_abstract.AbsQtItemValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = QtLineEdit_
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtConstantValueEntryItem, self).__init__(*args, **kwargs)
        #
        self._set_value_entry_def_init_(self)
        #
        self._set_item_value_type_constant_entry_def_init_()
        self._set_item_value_default_def_init_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(0, 0, 0, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._set_value_entry_widget_build_(self._item_value_type)

    def _set_value_entry_widget_build_(self, value_type):
        self._item_value_type = value_type
        #
        self._value_entry_widget = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry_widget)
        self._value_entry_widget._set_item_value_type_(self._item_value_type)

    def _set_value_entry_enable_(self, boolean):
        self._value_entry_widget.setReadOnly(not boolean)


class _QtScriptValueEntryItem(
    _utl_gui_qt_wgt_utility._QtEntryFrame,
    utl_gui_qt_abstract.AbsQtItemValueTypeConstantEntryDef,
    utl_gui_qt_abstract.AbsQtItemValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = QtTextBrowser_
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtScriptValueEntryItem, self).__init__(*args, **kwargs)
        self._frame_draw_margins = 0, 0, 0, 10
        #
        self._set_item_value_type_constant_entry_def_init_()
        self._set_item_value_default_def_init_()
        #
        self._set_value_entry_widget_build_(self._item_value_type)

    def _set_value_entry_widget_build_(self, value_type):
        self._item_value_type = value_type
        #
        self._main_layout = QtVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        entry_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._main_layout.addWidget(entry_widget)
        #
        self._value_entry_layout = QtHBoxLayout(entry_widget)
        self._value_entry_layout.setContentsMargins(2, 2, 2, 2)
        self._value_entry_layout.setSpacing(2)
        #
        self._value_entry_widget = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_widget._set_entry_frame_(self)
        # self._value_entry_widget.setReadOnly(False)
        self._value_entry_layout.addWidget(self._value_entry_widget)
        #
        self._resize_frame = _utl_gui_qt_wgt_utility._QtVResizeFrame()
        self._main_layout.addWidget(self._resize_frame)

    def _set_item_value_entry_enable_(self, boolean):
        self._value_entry_widget.setReadOnly(not boolean)

    def _get_resize_frame_(self):
        return self._resize_frame


class _QtRgbaValueEntryItem(
    _utl_gui_qt_wgt_utility._QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtRgbaDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    #
    utl_gui_qt_abstract.AbsQtItemValueTypeConstantEntryDef,
    utl_gui_qt_abstract.AbsQtItemValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = QtLineEdit_
    #
    CHOOSE_DROP_FRAME_CLASS = _QtItemRgbaChooseDropFrame
    def _set_wgt_update_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtRgbaValueEntryItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        self._set_rgba_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        #
        self._set_item_value_type_constant_entry_def_init_()
        self._set_item_value_default_def_init_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(20, 0, 0, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._set_value_entry_widget_build_(self._item_value_type)

    def _set_value_entry_widget_build_(self, value_type):
        self._item_value_type = value_type
        #
        self._value_entry_widget = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry_widget)
        self._value_entry_widget._set_item_value_type_(self._item_value_type)

    def _set_wgt_update_geometry_(self):
        super(_QtRgbaValueEntryItem, self)._set_wgt_update_geometry_()
        #
        x, y = 0, 0
        w, h = 20, self.height()
        c_w, c_h = 16, 16
        self._color_rect.setRect(
            x+2, y+(h-c_h)/2, c_w, c_h
        )

    def eventFilter(self, *args):
        super(_QtRgbaValueEntryItem, self).eventFilter(*args)
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
                self._set_action_flag_clear_()
                #
                self._action_is_hovered = False
                self.update()
            elif event.type() == QtCore.QEvent.Resize:
                self._set_wgt_update_geometry_()
        return False

    def paintEvent(self, event):
        super(_QtRgbaValueEntryItem, self).paintEvent(self)
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        self._set_wgt_update_geometry_()
        # name
        if self._color_rgba is not None:
            offset = self._get_action_offset_()
            background_color = self._get_color_rgba_255_()
            painter._set_frame_draw_by_rect_(
                self._color_rect,
                border_color=QtBorderColor.Transparent,
                background_color=background_color,
                offset=offset
            )

    def _set_color_choose_drop_(self):
        widget = self.CHOOSE_DROP_FRAME_CLASS(self)
        widget._set_popup_start_()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self.update()


class _QtEnumerateValueEntryItem(
    _utl_gui_qt_wgt_utility._QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    #
    utl_gui_qt_abstract.AbsQtValueEnumerateEntryDef,
    utl_gui_qt_abstract.AbsQtItemValueDefaultDef,
    #
    utl_gui_qt_abstract.AbsQtChooseDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    #
    utl_gui_qt_abstract.AbsQtActionEntryDef,
):
    QT_VALUE_ENTRY_CLASS = QtLineEdit_
    #
    CHOOSE_DROP_FRAME_CLASS = _utl_gui_qt_wgt_utility._QtPopupChooseFrame
    COMPLETION_DROP_FRAME_CLASS = _utl_gui_qt_wgt_utility._QtPopupCompletionFrame
    def __set_choose_popup_(self):
        self._value_entry_choose_frame._set_popup_start_()

    def __set_completion_popup_(self):
        self._value_entry_completion_frame._set_popup_start_()

    def _set_wgt_update_(self):
        values = self._get_item_values_()
        if values:
            value = self._get_item_value_()
            if value in values:
                self._value_index_label.show()
                maximum = len(values)
                value = values.index(value)+1
                text = '{}/{}'.format(value, maximum)
                self._value_index_label._set_name_text_(text)
                width = self._value_index_label._get_name_text_draw_width_(text)
                self._value_index_label.setMinimumWidth(width+4)
            else:
                self._value_index_label.hide()
        else:
            self._value_index_label.hide()

    def __init__(self, *args, **kwargs):
        super(_QtEnumerateValueEntryItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        # self._frame_draw_margins = 0, 0, 22, 0
        #
        self._set_value_enumerate_entry_def_init_()
        self._set_item_value_default_def_init_()
        #
        self._set_value_entry_def_init_(self)
        #
        self._set_action_def_init_(self)
        #
        self._set_action_entry_def_init_(self)
        self._set_choose_def_init_()
        #
        self._set_value_entry_widget_build_(self._item_value_type)

    def eventFilter(self, *args):
        super(_QtEnumerateValueEntryItem, self).eventFilter(*args)
        #
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                if event.type() == QtCore.QEvent.Wheel:
                    self._set_action_wheel_update_(event)
        return False

    def _set_action_wheel_update_(self, event):
        delta = event.angleDelta().y()
        values = self._get_item_values_()
        pre_value = self._get_item_value_()
        maximum = len(values) - 1
        if pre_value in values:
            pre_index = values.index(pre_value)
            if delta > 0:
                cur_index = pre_index - 1
            else:
                cur_index = pre_index + 1
            cur_index = max(min(cur_index, maximum), 0)
            if cur_index != pre_index:
                self._set_item_value_(values[cur_index])
                # set value before
                self._set_choose_changed_emit_send_()

    def _set_value_entry_widget_build_(self, value_type):
        self._item_value_type = value_type
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
        self._value_entry_widget = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry_widget)
        self._value_entry_widget._set_entry_frame_(self)
        self._value_entry_widget._set_item_value_type_(self._item_value_type)
        self._value_entry_widget._set_enter_enable_(False)
        self._value_entry_widget.user_entry_changed.connect(
            self.__set_completion_popup_
        )
        #
        self._value_index_label = _QtTextItem()
        self._value_entry_layout.addWidget(self._value_index_label)
        self._value_index_label._set_name_color_(QtFontColor.Disable)
        self._value_index_label.hide()
        #
        button_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._value_entry_layout.addWidget(button_widget)
        self._button_layout = QtHBoxLayout(button_widget)
        self._button_layout._set_align_top_()
        self._button_layout.setContentsMargins(0, 0, 0, 0)
        self._button_layout.setSpacing(2)
        #
        self._choose_button = _QtIconPressItem()
        self._button_layout.addWidget(self._choose_button)
        self._choose_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('down')
        )
        # self._choose_button._set_icon_frame_size_(16, 16)
        # self._choose_button._set_file_icon_size_(12, 12)
        self._choose_button.press_clicked.connect(
            self.__set_choose_popup_
        )
        #
        self._value_entry_choose_frame = self.CHOOSE_DROP_FRAME_CLASS(self)
        self._value_entry_choose_frame._set_popup_target_entry_(self._value_entry_widget)
        self._value_entry_choose_frame._set_popup_target_entry_frame_(self)
        self._value_entry_choose_frame.hide()
        self._value_entry_widget.up_key_pressed.connect(
            self._value_entry_choose_frame._set_popup_scroll_to_pre_
        )
        self._value_entry_widget.down_key_pressed.connect(
            self._value_entry_choose_frame._set_popup_scroll_to_next_
        )
        self._value_entry_widget.entry_finished.connect(
            self._value_entry_choose_frame._set_popup_end_
        )
        #
        self._value_entry_completion_frame = self.COMPLETION_DROP_FRAME_CLASS(self)
        self._value_entry_completion_frame._set_popup_target_entry_(self._value_entry_widget)
        self._value_entry_completion_frame._set_popup_target_entry_frame_(self)
        self._value_entry_completion_frame.hide()
        self._value_entry_widget.up_key_pressed.connect(
            self._value_entry_completion_frame._set_popup_scroll_to_pre_
        )
        self._value_entry_widget.down_key_pressed.connect(
            self._value_entry_completion_frame._set_popup_scroll_to_next_
        )
        self._value_entry_widget.entry_finished.connect(
            self._value_entry_completion_frame._set_popup_end_
        )

    def _set_value_entry_enable_(self, boolean):
        self._value_entry_widget._set_enter_enable_(boolean)
        self._choose_button.setHidden(not boolean)
        self._value_index_label.setHidden(not boolean)

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry_widget._set_entry_drop_enable_(boolean)

    def _set_value_entry_filter_fnc_(self, fnc):
        self._value_entry_widget._set_value_validation_fnc_(fnc)

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry_widget._set_entry_use_as_storage_(boolean)

    def _set_value_entry_finished_connect_to_(self, fnc):
        self._value_entry_widget.entry_finished.connect(fnc)

    def _set_value_entry_changed_connect_to_(self, fnc):
        self._value_entry_widget.entry_changed.connect(fnc)

    def _set_value_entry_choose_button_icon_file_path_(self, file_path):
        self._choose_button._set_icon_file_path_(file_path)

    def _set_value_entry_button_add_(self, widget):
        self._button_layout.addWidget(widget)

    def _set_value_index_visible_(self, boolean):
        pass

    def _get_choose_values_(self):
        return self._get_item_values_()

    def _get_choose_current_(self):
        return self._get_item_value_()

    def _set_choose_current_(self, value):
        self._set_item_value_(value)

    def _get_choose_icon_file_paths_(self):
        return self._get_item_value_icon_file_paths_()


class _QtArrayValueEntryItem(
    _utl_gui_qt_wgt_utility._QtEntryFrame,
    utl_gui_qt_abstract._QtArrayValueEntryDef,
):
    QT_VALUE_ENTRY_CLASS = QtLineEdit_
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtArrayValueEntryItem, self).__init__(*args, **kwargs)
        #
        self._set_array_value_entry_def_init_()
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(0, 0, 0, 0)
        self._value_entry_layout.setSpacing(8)
        #
        self._set_value_entry_widget_build_(2, self._item_value_type)

    def _set_value_entry_widget_build_(self, value_size, value_type):
        self._item_value_type = value_type
        #
        self._value_entry_widgets = []
        set_qt_layout_clear(self._value_entry_layout)
        #
        self._set_entry_count_(value_size)
        if value_size:
            for i in range(value_size):
                _i_value_entry_widget = QtLineEdit_()
                _i_value_entry_widget._set_item_value_type_(self._item_value_type)
                self._value_entry_layout.addWidget(_i_value_entry_widget)
                self._value_entry_widgets.append(_i_value_entry_widget)


class _QtValuesEntryItem(
    _utl_gui_qt_wgt_utility._QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    utl_gui_qt_abstract.AbsQtChooseDef,
    #
    utl_gui_qt_abstract.AbsQtEntryHistoryDef,
):
    QT_VALUE_ENTRY_CLASS = _QtListWidget
    #
    CHOOSE_DROP_FRAME_CLASS = _utl_gui_qt_wgt_utility._QtPopupChooseFrame
    #
    add_press_clicked = qt_signal()
    def __set_choose_popup_(self):
        self._value_entry_choose_frame._set_popup_start_()

    def __init__(self, *args, **kwargs):
        super(_QtValuesEntryItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._frame_draw_margins = 0, 0, 0, 10
        #
        self._set_value_entry_def_init_(self)
        self._set_choose_def_init_()
        self._set_entry_history_def_init_(self)
        #
        self._set_value_entry_widget_build_(str)

    def _set_value_entry_widget_build_(self, value_type):
        self._item_value_type = value_type

        self._main_layout = QtVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        entry_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._main_layout.addWidget(entry_widget)
        #
        self._value_entry_layout = QtHBoxLayout(entry_widget)
        self._value_entry_layout.setContentsMargins(2, 2, 2, 2)
        self._value_entry_layout.setSpacing(2)
        #
        self._value_entry_widget = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry_widget)
        self._value_entry_widget._set_entry_frame_(self)
        #
        button_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        self._value_entry_layout.addWidget(button_widget)
        self._button_layout = QtVBoxLayout(button_widget)
        self._button_layout._set_align_top_()
        self._button_layout.setContentsMargins(0, 0, 0, 0)
        self._button_layout.setSpacing(2)

        self._choose_button = _QtIconPressItem()
        self._button_layout.addWidget(self._choose_button)
        self._choose_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('down')
        )
        self._choose_button.press_clicked.connect(
            self.__set_choose_popup_
        )
        #
        self._value_entry_choose_frame = self.CHOOSE_DROP_FRAME_CLASS(self)
        self._value_entry_choose_frame._set_popup_target_entry_(self._value_entry_widget)
        self._value_entry_choose_frame._set_popup_target_entry_frame_(self)
        self._value_entry_choose_frame.hide()
        # self._value_entry_widget.up_key_pressed.connect(
        #     self._value_entry_choose_frame._set_popup_scroll_to_pre_
        # )
        # self._value_entry_widget.down_key_pressed.connect(
        #     self._value_entry_choose_frame._set_popup_scroll_to_next_
        # )
        # self._value_entry_widget.entry_finished.connect(
        #     self._value_entry_choose_frame._set_popup_end_
        # )

        self._resize_frame = _utl_gui_qt_wgt_utility._QtVResizeFrame()
        self._main_layout.addWidget(self._resize_frame)

    def _get_value_entry_widget_(self):
        return self._value_entry_widget

    def _set_value_entry_enable_(self, boolean):
        self._value_entry_widget._set_entry_enable_(boolean)

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry_widget._set_entry_drop_enable_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _set_values_append_(self, value):
        self._value_entry_widget._set_values_append_(value)

    def _set_values_(self, values):
        self._value_entry_widget._set_values_(values)

    def _get_values_(self):
        return self._value_entry_widget._get_values_()

    def _set_value_icon_file_path_(self):
        pass

    def _set_value_entry_button_add_(self, widget):
        self._button_layout.addWidget(widget)

    def _set_value_entry_use_as_storage_(self, boolean):
        self._value_entry_widget._set_entry_use_as_storage_(boolean)

    def _set_entry_history_key_(self, key):
        super(_QtValuesEntryItem, self)._set_entry_history_key_(key)
        #
        self._choose_button.show()

    def _set_entry_history_update_(self):
        if self._entry_history_key is not None:
            #
            histories = utl_core.History.get(
                self._entry_history_key
            )
            if histories:
                histories.reverse()
            #
            histories = [i for i in histories if self._get_entry_history_value_is_valid_(i) is True]
            #
            self._set_choose_values_(
                histories
            )

    def _set_value_entry_choose_button_icon_file_path_(self, file_path):
        self._choose_button._set_icon_file_path_(file_path)

    def _set_choose_current_(self, value):
        self._set_values_append_(value)

    def _get_resize_frame_(self):
        return self._resize_frame


class _QtFilterBar(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtChooseDef,
    #
    utl_gui_qt_abstract.AbsQtValueEnumerateEntryDef,
    #
    utl_gui_qt_abstract.AbsQtActionEntryDef,
    #
    utl_gui_qt_abstract.AbsQtEntryHistoryDef,
):
    BTN_FRAME_SIZE = 18, 18
    BTN_ICON_SIZE = 16, 16
    #
    entry_changed = qt_signal()
    preOccurrenceClicked = qt_signal()
    nextOccurrenceClicked = qt_signal()
    #
    QT_VALUE_ENTRY_CLASS = QtLineEdit_
    #
    CHOOSE_DROP_FRAME_CLASS = _utl_gui_qt_wgt_utility._QtPopupChooseFrame
    COMPLETION_DROP_FRAME_CLASS = _utl_gui_qt_wgt_utility._QtPopupCompletionFrame
    def __set_choose_popup_(self):
        self._entry_history_choose_drop_frame._set_popup_start_()

    def _set_wgt_update_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtFilterBar, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        qt_layout_0 = QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        self._set_value_enumerate_entry_def_init_()
        #
        self._set_choose_def_init_()
        self._set_action_entry_def_init_(self)
        #
        self._result_label = _utl_gui_qt_wgt_utility.QtLabel()
        qt_layout_0.addWidget(self._result_label)
        self._result_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        self._entry_frame = _utl_gui_qt_wgt_utility._QtEntryFrame()
        self._entry_frame.setMaximumWidth(240)
        qt_layout_0.addWidget(self._entry_frame)
        #
        self._set_value_entry_widget_build_(str)
        #
        self._match_case_button = _QtIconPressItem()
        self._match_case_button.hide()
        qt_layout_0.addWidget(self._match_case_button)
        self._match_case_button.setFocusProxy(self._value_entry_widget)
        self._match_case_button.clicked.connect(self._set_match_case_swap_)
        self._match_case_icon_names = 'match_case_off', 'match_case_on'
        self._is_match_case = False
        #
        self._match_word_button = _QtIconPressItem()
        self._match_word_button.hide()
        qt_layout_0.addWidget(self._match_word_button)
        self._match_word_button.setFocusProxy(self._value_entry_widget)
        self._match_word_button.clicked.connect(self._set_match_word_swap_)
        self._match_word_icon_names = 'match_word_off', 'match_word_on'
        self._is_match_word = False
        #
        self._pre_occurrence_button = _QtIconPressItem()
        qt_layout_0.addWidget(self._pre_occurrence_button)
        self._pre_occurrence_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'pre_occurrence'
            )
        )
        self._pre_occurrence_button.clicked.connect(self._set_pre_occurrence_emit_send_)
        #
        self._next_occurrence_button = _QtIconPressItem()
        qt_layout_0.addWidget(self._next_occurrence_button)
        self._next_occurrence_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'next_occurrence'
            )
        )
        self._next_occurrence_button.clicked.connect(self._set_next_occurrence_emit_send_)
        #
        self._set_entry_history_def_init_(self)
        #
        self._result_count = None
        self._result_index = None
        #
        self._set_update_()
    #
    def _set_update_(self):
        self._match_case_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(self._match_case_icon_names[self._is_match_case])
        )
        #
        self._match_word_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(self._match_word_icon_names[self._is_match_word])
        )
        #
        self._value_entry_widget.setPlaceholderText(
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
        return self._value_entry_widget

    def _set_entry_clear_(self):
        self._value_entry_widget.clear()
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
            not not self._value_entry_widget.text()
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
        self._value_entry_widget._set_focused_(boolean)

    def _set_value_entry_widget_build_(self, value_type):
        self._item_value_type = value_type
        self._value_entry_layout = QtHBoxLayout(self._entry_frame)
        self._value_entry_layout.setContentsMargins(*[0]*4)
        self._value_entry_layout.setSpacing(2)
        #
        self._header_button = _QtIconPressItem()
        # self._header_button._set_icon_frame_size_(16, 16)
        # self._header_button._set_file_icon_size_(12, 12)
        self._value_entry_layout.addWidget(self._header_button)
        self._header_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'search'
            )
        )
        #
        self._header_button._set_menu_raw_(
            [
                ('option', None, None),
                (),
                ('history', None, None)
            ]
        )
        #
        self._value_entry_widget = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry_layout.addWidget(self._value_entry_widget)
        #
        self._value_entry_widget.entry_changed.connect(self._set_enter_changed_emit_send_)
        self._value_entry_widget.entry_finished.connect(self._set_entry_history_update_)
        #
        self._entry_clear_button = _QtIconPressItem()
        # self._entry_clear_button._set_icon_frame_size_(16, 16)
        # self._entry_clear_button._set_file_icon_size_(12, 12)
        self._value_entry_layout.addWidget(self._entry_clear_button)
        self._entry_clear_button.hide()
        self._entry_clear_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(
                'entry_clear'
            )
        )
        self._entry_clear_button.clicked.connect(self._set_entry_clear_)
        #
        self._history_button = _QtIconPressItem()
        self._value_entry_layout.addWidget(self._history_button)
        #
        self._history_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('history')
        )
        # self._history_button._set_icon_frame_size_(16, 16)
        # self._history_button._set_file_icon_size_(12, 12)
        self._history_button.press_clicked.connect(
            self.__set_choose_popup_
        )
        self._history_button.hide()
        #
        self._entry_history_choose_drop_frame = self.CHOOSE_DROP_FRAME_CLASS(self)
        self._entry_history_choose_drop_frame._set_popup_target_entry_(self._value_entry_widget)
        self._entry_history_choose_drop_frame._set_popup_target_entry_frame_(self._entry_frame)
        self._value_entry_widget.up_key_pressed.connect(
            self._entry_history_choose_drop_frame._set_popup_scroll_to_pre_
        )
        self._value_entry_widget.down_key_pressed.connect(
            self._entry_history_choose_drop_frame._set_popup_scroll_to_next_
        )
        self._value_entry_widget.entry_finished.connect(
            self._entry_history_choose_drop_frame._set_popup_end_
        )
        self._entry_history_choose_drop_frame.hide()

    def _set_entry_history_key_(self, key):
        super(_QtFilterBar, self)._set_entry_history_key_(key)
        #
        self._history_button.show()

    def _set_entry_history_update_(self):
        if self._entry_history_key is not None:
            value = self._get_item_value_()
            if value:
                if self._get_entry_history_value_is_valid_(value) is True:
                    utl_core.History.set_append(
                        self._entry_history_key,
                        value
                    )
            #
            histories = utl_core.History.get(
                self._entry_history_key
            )
            if histories:
                histories.reverse()
            #
            histories = [i for i in histories if self._get_entry_history_value_is_valid_(i) is True]
            #
            self._set_choose_values_(
                histories
            )

    def _set_choose_current_(self, value):
        self._set_item_value_(value)


class _QtHExpandItem0(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract._QtItemExpandActionDef,
):
    toggled = qt_signal(bool)
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
        self._set_name_def_init_()
        self._name_text_font = Font.GROUP
        #
        self._set_icon_def_init_()
        self._icon_name_is_enable = True
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        self._set_item_expand_action_def_init_()
        #
        self._item_is_expanded = False
        self._item_expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('expandopen')
        self._item_expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('expandclose')
        self._action_is_hovered = False
        #
        self._set_item_expand_update_()
        #
        r, g, b = 207, 207, 207
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._name_color = color
        self._hover_name_color = hover_color
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        # font
        self.setFont(Font.NAME)

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        #
        self._set_frame_rect_(
            x+1, y+1, w-2, h-2
        )
        f_w, f_h = self._icon_frame_size
        i_w, i_h = self._icon_file_draw_size
        self._set_icon_file_draw_rect_(
            x + (f_w - i_w)/2, y + (f_h - i_h)/2, i_w, i_h
        )
        #
        x += f_w + spacing
        if self._icon_name_is_enable is True:
            if self._icon_name_text is not None:
                i_w, i_h = self._icon_name_draw_size
                self._set_icon_name_draw_rect_(
                    x+(f_w-i_w)/2, y+(f_h-i_h)/2, i_w, i_h
                )
                x += f_w+spacing
        #
        self._set_name_rect_(
            x, y, w-20, h
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
                        self._set_item_expand_action_run_()
                #
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_wgt_update_geometry_()
        #
        offset = self._get_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        background_color = [self._frame_background_color, self._hovered_frame_background_color][self._action_is_hovered]
        # painter.setBrush(background_color)
        #
        painter._set_frame_draw_by_rect_(
            self._frame_draw_rect,
            border_color=background_color,
            background_color=background_color,
            border_radius=1,
            offset=offset
        )
        # file-icon
        painter._set_icon_file_draw_by_rect_(
            self._icon_file_draw_rect,
            self._icon_file_path,
            offset=offset
        )
        # name-icon
        if self._icon_name_is_enable is True:
            if self._icon_name_text is not None:
                painter._set_icon_name_text_draw_by_rect_(
                    self._icon_name_draw_rect,
                    self._icon_name_text,
                    # background_color=background_color,
                    offset=offset,
                    border_radius=2,
                )
        # text
        if self._name_text is not None:
            color = [self._name_color, self._hover_name_color][self._action_is_hovered]
            painter._set_text_draw_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=self._name_text_font,
                font_color=color,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )

    def set_expanded(self, boolean):
        self._item_is_expanded = boolean

    def _set_item_expand_update_(self):
        self._set_icon_file_path_(
            [self._item_expand_icon_file_path_1, self._item_expand_icon_file_path_0][self._item_is_expanded]
        )
        #
        self._set_wgt_update_draw_()


class _QtHExpandItem1(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
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
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        self._set_item_expand_action_def_init_()
        #
        self._item_is_expand_enable = True
        self._item_is_expanded = False
        self._item_expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._item_expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
        self._item_expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-up')
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        #
        self._set_item_expand_update_()
        # font
        self.setFont(Font.NAME)

    def _set_wgt_update_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_wgt_update_geometry_()
        #
        offset = self._get_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        background_color = [self._frame_background_color, self._hovered_frame_background_color][self._action_is_hovered]
        painter._set_frame_draw_by_rect_(
            rect=self._frame_draw_rect,
            border_color=background_color,
            background_color=background_color,
            border_radius=self._frame_border_radius,
            offset=offset
        )
        # icon
        painter._set_icon_file_draw_by_rect_(
            rect=self._icon_file_draw_rect,
            file_path=self._icon_file_path,
            offset=offset
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
                        self._set_item_expand_action_run_()
                #
                self._set_action_flag_clear_()
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
            self._set_icon_file_path_(
                [self._item_expand_icon_file_path_1, self._item_expand_icon_file_path_0][self._item_is_expanded]
            )
        elif self._item_expand_direction == self.EXPAND_BOTTOM_TO_TOP:
            self._set_icon_file_path_(
                [self._item_expand_icon_file_path_1, self._item_expand_icon_file_path_2][self._item_is_expanded]
            )
        #
        self._set_wgt_update_draw_()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._set_frame_rect_(
            x+1, y+1, w-2, h-2
        )
        #
        f_w, f_h = 12, 12
        i_w, i_h = 8, 8
        #
        if self._item_expand_direction == self.EXPAND_TOP_TO_BOTTOM:
            self._set_icon_file_draw_rect_(
                x+(f_w-i_w)/2, y+(f_h-i_h)/2,
                i_w, i_h
            )
        elif self._item_expand_direction == self.EXPAND_BOTTOM_TO_TOP:
            self._set_icon_file_draw_rect_(
                x+(f_w-i_w)/2, y+h-f_h+(f_h-i_h)/2,
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
        self._item_expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
        self._item_expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._item_expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-left')


class AbsQtItemDagLoading(object):
    def _set_item_dag_loading_def_init_(self, widget):
        self._widget = widget

        self._loading_item = None

    def _set_item_dag_loading_start_(self):
        self._loading_item = self._widget._set_child_add_()
        self._loading_item.setText(0, 'loading ...')

    def _set_item_dag_loading_end_(self):
        if self._loading_item is not None:
            self._loading_item._set_item_show_kill_all_()
            self._loading_item._set_item_show_stop_all_()
            self._widget.takeChild(
                self._widget.indexOfChild(self._loading_item)
            )
            self._loading_item = None


class _QtTreeSignals(
    QtCore.QObject
):
    visible = qt_signal(bool)
    expanded = qt_signal()
    press_db_clicked = qt_signal(object, int)
    press_clicked = qt_signal(object, int)


class QtTreeWidgetItem(
    QtWidgets.QTreeWidgetItem,
    AbsQtItemDagLoading,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsShowItemDef,
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtItemFilterTgtDef,
    #
    utl_gui_qt_abstract.AbsQtItemStateDef,
    #
    utl_gui_qt_abstract.AbsQtDagDef,
    utl_gui_qt_abstract.AbsQtVisibleDef,
    #
    utl_gui_qt_abstract.AbsQtItemVisibleConnectionDef,
):
    def __init__(self, *args, **kwargs):
        super(QtTreeWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        )
        #
        self._set_item_dag_loading_def_init_(self)
        self._set_show_item_def_init_(self)
        #
        self._is_check_enable = True
        self._emit_send_enable = False
        #
        self._set_name_def_init_()
        self._set_icon_def_init_()
        self._set_menu_def_init_()
        #
        self._set_item_filter_tgt_def_init_()
        #
        self._set_item_state_def_init_()
        #
        self._set_dag_def_init_()
        self._set_visible_def_init_()
        #
        self._set_item_visible_connection_def_init_()

        self._signals = _QtTreeSignals()

    def _set_child_add_(self):
        item = self.__class__()
        self.addChild(item)
        item._set_item_show_connect_()
        return item

    def _get_item_is_hidden_(self):
        return self.isHidden()

    def _set_wgt_update_draw_(self):
        self._get_view_().update()

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

    def _set_icon_file_path_(self, file_path, column=0):
        self._icon_file_path = file_path
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

    def _set_icon_name_text_(self, text, column=0):
        self._icon_name_text = text
        self.setIcon(
            column,
            utl_gui_qt_core.QtUtilMtd.get_name_text_icon_(text)
        )

    def _set_icon_state_update_(self, column=0):
        if column == 0:
            icon = QtGui.QIcon()
            pixmap = None
            if self._icon_file_path is not None:
                pixmap = QtGui.QPixmap(self._icon_file_path)
            elif self._icon_name_text is not None:
                pixmap = QtPixmapMtd.get_by_name(self._icon_name_text)
            #
            if pixmap:
                if self._icon_state in [
                    utl_gui_core.State.ENABLE,
                    utl_gui_core.State.DISABLE,
                    utl_gui_core.State.WARNING,
                    utl_gui_core.State.ERROR,
                    utl_gui_core.State.LOCKED,
                    utl_gui_core.State.LOST
                ]:
                    if self._icon_state == utl_gui_core.State.ENABLE:
                        background_color = Color.ENABLE
                    elif self._icon_state == utl_gui_core.State.DISABLE:
                        background_color = Color.DISABLE
                    elif self._icon_state == utl_gui_core.State.WARNING:
                        background_color = Color.WARNING
                    elif self._icon_state == utl_gui_core.State.ERROR:
                        background_color = Color.ERROR
                    elif self._icon_state == utl_gui_core.State.LOCKED:
                        background_color = Color.LOCKED
                    elif self._icon_state == utl_gui_core.State.LOST:
                        background_color = Color.LOST
                    else:
                        raise TypeError()
                    #
                    painter = _utl_gui_qt_wgt_utility.QtPainter(pixmap)
                    rect = pixmap.rect()
                    x, y = rect.x(), rect.y()
                    w, h = rect.width(), rect.height()
                    #
                    border_color = QtBorderColor.Icon
                    #
                    s_w, s_h = w*.5, h*.5
                    state_rect = QtCore.QRect(
                        x, y+h-s_h, s_w, s_h
                    )
                    if self._icon_state == utl_gui_core.State.LOCKED:
                        painter._set_icon_file_draw_by_rect_(
                            state_rect,
                            file_path=utl_gui_core.RscIconFile.get(
                                'state-locked'
                            )
                        )
                        painter.end()
                    elif self._icon_state == utl_gui_core.State.LOST:
                        painter._set_icon_file_draw_by_rect_(
                            state_rect,
                            file_path=utl_gui_core.RscIconFile.get(
                                'state-lost'
                            )
                        )
                        painter.end()
                    else:
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

    def _set_state_(self, state, column=0):
        self._icon_state = state
        #
        self._set_icon_state_update_(column)
        #
        if state == utl_gui_core.State.NORMAL:
            self.setForeground(
                column, QtGui.QBrush(Color.NORMAL)
            )
        elif state == utl_gui_core.State.ENABLE:
            self.setForeground(column, QtGui.QBrush(Color.ENABLE))
        elif state == utl_gui_core.State.DISABLE:
            self.setForeground(column, QtGui.QBrush(Color.DISABLE))
        elif state == utl_gui_core.State.WARNING:
            self.setForeground(column, QtGui.QBrush(Color.WARNING))
        elif state == utl_gui_core.State.ERROR:
            self.setForeground(column, QtGui.QBrush(Color.ERROR))
        elif state == utl_gui_core.State.LOCKED:
            self.setForeground(column, QtGui.QBrush(Color.LOCKED))
        elif state == utl_gui_core.State.LOST:
            self.setForeground(column, QtGui.QBrush(Color.LOST))

    def _set_status_(self, status, column=0):
        pass

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

    def _get_action_check_is_enable_(self):
        return self._is_check_enable

    def _set_emit_send_enable_(self, boolean):
        self._emit_send_enable = boolean

    def _get_emit_send_enable_(self):
        return self._emit_send_enable

    def _set_check_state_(self, boolean, column=0):
        self.setCheckState(
            column, [utl_gui_qt_core.QtCore.Qt.Unchecked, utl_gui_qt_core.QtCore.Qt.Checked][boolean]
        )

    def _set_check_state_extra_(self, column=0):
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

    def _get_name_text_(self, column=0):
        return self.text(column)

    def _get_item_keyword_filter_tgt_keys_(self):
        return self._get_name_texts_()
    # show
    def _set_view_(self, widget):
        self._tree_widget = widget

    def _set_item_show_connect_(self):
        self._set_item_show_def_setup_(self.treeWidget())

    def _get_view_(self):
        return self.treeWidget()

    def _get_item_is_viewport_show_able_(self):
        item = self
        view = self.treeWidget()
        parent = self.parent()
        if parent is None:
            return view._get_show_view_item_showable_(item)
        else:
            if parent.isExpanded():
                return view._get_show_view_item_showable_(item)
        return False

    def _set_item_widget_visible_(self, boolean):
        pass
        # self.setVisible(boolean)

    def _set_name_text_(self, text, column=0):
        if text is not None:
            if isinstance(text, (tuple, list)):
                if len(text) > 1:
                    _ = '; '.join(('{}.{}'.format(seq+1, i) for seq, i in enumerate(text)))
                elif len(text) == 1:
                    _ = text[0]
                else:
                    _ = ''
            else:
                _ = unicode(text)
            #
            self.setText(column, _)
            self.setFont(column, utl_gui_qt_core.Font.NAME)

    def _set_tool_tip_(self, raw, column=0, as_markdown_style=False):
        if raw is not None:
            if isinstance(raw, (tuple, list)):
                _ = u'\n'.join(raw)
            elif isinstance(raw, (str, unicode)):
                _ = raw
            else:
                raise TypeError()
            #
            self._set_tool_tip_text_(
                _,
                column,
                as_markdown_style
            )

    def _set_tool_tip_text_(self, text, column=0, markdown_style=False):
        if hasattr(self, 'setToolTip'):
            if markdown_style is True:
                import markdown
                html = markdown.markdown(text)
                # noinspection PyCallingNonCallable
                self.setToolTip(column, html)
            else:
                name_text_orig = self._get_name_text_orig_()
                if name_text_orig is not None:
                    text = name_text_orig
                else:
                    text = self._get_name_text_()
                #
                text = text.replace('<', '&lt;').replace('>', '&gt;')
                html = '<html>\n<body>\n'
                html += '<h3>{}</h3>\n'.format(text)
                for i in text.split('\n'):
                    html += '<ul>\n<li><i>{}</i></li>\n</ul>\n'.format(i)
                html += '</body>\n</html>'
                # noinspection PyCallingNonCallable
                self.setToolTip(column, html)

    def _get_item_widget_(self):
        pass

    def _get_item_state_color_(self):
        return self.foreground(0)

    def _set_hidden_(self, boolean, ancestors=False):
        self.setHidden(boolean)
        if ancestors is True:
            [i.set_visible_by_has_visible_children() for i in self.get_ancestors()]
        #
        self._set_item_visible_connection_refresh_()
        if hasattr(self, 'gui_proxy'):
            self.gui_proxy.set_visible_connection_refresh()

    def _set_expanded_(self, boolean, ancestors=False):
        self.setExpanded(boolean)
        self._set_item_show_start_auto_()
        #
        if ancestors is True:
            [i._set_expanded_(boolean) for i in self._get_ancestors_()]

    def __str__(self):
        return '{}(names="{}")'.format(
            self.__class__.__name__, ', '.join(self._get_name_texts_())
        )

    def __repr__(self):
        return self.__str__()


class _QtListItemWidget(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIndexDef,
    utl_gui_qt_abstract.AbsQtImageDef,
    utl_gui_qt_abstract.AbsQtMovieDef,
    #
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract._QtIconsDef,
    utl_gui_qt_abstract.AbsQtNamesDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtActionSelectDef,
    #
    utl_gui_qt_abstract.AbsQtItemStateDef,
    #
    utl_gui_qt_abstract.AbsQtItemMovieActionDef,
):
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
        self._set_movie_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        self._set_action_select_def_init_()
        #
        self._set_item_movie_action_def_init_()
        #
        self._set_item_state_def_init_()
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
        self._frame_side = 4
        self._frame_spacing = 2
        #
        self._frame_size = 128, 128
        #
        self._frame_background_color = QtBackgroundColor.Light
        #
        self._is_viewport_show_enable = True
        #
        self.setFont(get_font())

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_action_hover_filter_execute_(event)
            #
            if event.type() == QtCore.QEvent.Resize:
                self.update()
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                elif event.button() == QtCore.Qt.LeftButton:
                    self._set_action_pressed_(True)
                    self._set_action_flag_(self.ActionFlag.PressClick)
            #
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_pressed_(True)
                    self._set_action_flag_(self.ActionFlag.PressDbClick)
            #
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if self._get_action_flag_is_match_(self.ActionFlag.PressClick):
                    self._set_action_press_click_emit_send_()
                elif self._get_action_flag_is_match_(self.ActionFlag.PressDbClick):
                    self._set_action_press_db_click_emit_send_()
                #
                self._set_action_pressed_(False)
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_wgt_update_geometry_()
        #
        w, h = self.width(), self.height()
        #
        offset = self._get_action_offset_()
        #
        bkg_rect = QtCore.QRect(1, 1, w-2, h-2)
        background_color = painter._get_item_background_color_by_rect_(
            bkg_rect,
            is_hovered=self._action_is_hovered,
            is_selected=self._item_is_selected,
            is_actioned=self._get_is_actioned_()
        )
        #
        item = self._get_item_()
        if item._item_show_status in [item.ShowStatus.Loading, item.ShowStatus.Waiting]:
            painter._set_loading_draw_by_rect_(
                self._frame_draw_rect,
                item._item_show_loading_index
            )
        else:
            painter._set_frame_draw_by_rect_(
                bkg_rect,
                border_color=QtBackgroundColor.Transparent,
                background_color=background_color,
                border_radius=1,
                offset=offset
            )
            # icon frame
            if self._icon_frame_draw_enable is True:
                if self._get_has_icon_():
                    painter._set_frame_draw_by_rect_(
                        self._icon_frame_rect,
                        border_color=self._frame_background_color,
                        background_color=self._frame_background_color,
                        offset=offset
                    )
            #
            if self._name_frame_draw_enable is True:
                if self._get_has_name_():
                    painter._set_frame_draw_by_rect_(
                        self._name_frame_rect,
                        border_color=self._get_name_frame_border_color_(),
                        background_color=self._get_name_frame_background_color_(),
                        offset=offset
                    )
            #
            if self._image_frame_draw_enable is True:
                if self._get_has_image_():
                    painter._set_frame_draw_by_rect_(
                        self._image_frame_rect,
                        border_color=self._frame_background_color,
                        background_color=self._frame_background_color,
                        offset=offset
                    )
            # icon
            if self._get_has_icon_() is True:
                icon_indices = self._get_icon_indices_()
                if icon_indices:
                    icons = self._get_icons_as_pixmap_()
                    if icons:
                        for icon_index in icon_indices:
                            painter._set_pixmap_draw_by_rect_(
                                self._get_icon_rect_at_(icon_index),
                                self._get_icon_as_pixmap_at_(icon_index),
                                offset=offset
                            )
                    else:
                        icon_file_paths = self._get_icon_file_paths_()
                        if icon_file_paths:
                            for icon_index in icon_indices:
                                painter._set_icon_file_draw_by_rect_(
                                    self._get_icon_rect_at_(icon_index),
                                    self._get_icon_file_path_at_(icon_index),
                                    offset=offset
                                )
            # name
            if self._get_has_name_() is True:
                name_indices = self._get_name_indices_()
                if name_indices:
                    text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
                    #
                    name_text_dict = self._get_name_text_dict_()
                    if name_text_dict:
                        painter.setFont(get_font())
                        key_text_width = utl_gui_qt_core.QtTextMtd.get_draw_width_maximum(
                            painter, self._name_text_dict.keys()
                        )
                        for i_name_index, (i_key, i_value) in enumerate(name_text_dict.items()):
                            painter._set_text_draw_by_rect_use_key_value_(
                                self._get_name_rect_at_(i_name_index),
                                key_text=i_key,
                                value_text=i_value,
                                key_text_width=key_text_width,
                                offset=offset,
                                is_hovered=self._action_is_hovered,
                                is_selected=self._item_is_selected
                            )
                    else:
                        for i_name_index in name_indices:
                            painter._set_text_draw_by_rect_(
                                self._get_name_rect_at_(i_name_index),
                                text=self._get_name_text_at_(i_name_index),
                                font=get_font(),
                                text_option=text_option,
                                word_warp=self._name_word_warp,
                                offset=offset,
                                is_hovered=self._action_is_hovered,
                                is_selected=self._item_is_selected
                            )
            # image
            if self._get_has_image_() is True:
                image_file_path = self._image_file_path
                # draw by image file
                if image_file_path:
                    painter._set_any_image_draw_by_rect_(
                        self._get_image_rect_(),
                        image_file_path,
                        offset=offset
                    )
                else:
                    image_name_text = self._image_name_text
                    # draw by text
                    if image_name_text:
                        painter._set_icon_name_text_draw_by_rect_(
                            self._get_image_rect_(),
                            image_name_text,
                            border_radius=4,
                            offset=offset
                        )
            #
            if self._get_movie_enable_():
                painter._set_movie_play_button_draw_by_rect_(
                    self._movie_rect,
                    offset=offset,
                    is_hovered=self._action_is_hovered,
                    is_selected=self._item_is_selected,
                    is_actioned=self._get_is_actioned_()
                )
            #
            if item._item_show_image_status in [item.ShowStatus.Loading, item.ShowStatus.Waiting]:
                painter._set_loading_draw_by_rect_(
                    self._image_frame_rect,
                    item._item_show_image_loading_index
                )

    def _set_frame_icon_size_(self, w, h):
        self._frame_icon_width, self._frame_icon_height = w, h

    def _set_frame_image_size_(self, w, h):
        self._frame_image_width, self._frame_image_height = w, h

    def _set_frame_name_size_(self, w, h):
        self._frame_name_width, self._frame_name_height = w, h

    def _get_item_(self):
        return self._list_widget_item

    def _set_item_(self, item):
        self._list_widget_item = item

    def _set_view_(self, widget):
        self._list_widget = widget

    def _get_view_(self):
        return self._list_widget

    def _set_wgt_update_geometry_(self):
        self._set_widget_frame_geometries_update_()
        self._set_widget_icon_sub_geometries_update_()
        self._set_widget_image_sub_geometries_update_()
        self._set_widget_name_sub_geometries_update_()

    def _set_widget_frame_geometries_update_(self):
        if self._list_widget is not None:
            side = 4
            spacing = 2
            x, y = side, side
            w, h = self._frame_size
            self._set_frame_rect_(x, y, w, h)
            if self._list_widget._get_is_grid_mode_():
                self._set_widget_frame_geometry_update_as_grid_mode_(
                    (x, y), (w, h)
                )
            else:
                self._set_widget_frame_geometry_update_as_list_mode_(
                    (x, y), (w, h)
                )

    def _set_widget_frame_geometry_update_as_grid_mode_(self, pos, size):
        x, y = pos
        w, h = size
        f_spacing = self._frame_spacing
        if self._get_has_name_() is True:
            name_f_w, name_f_h = self._name_frame_size
            n_c = len(self._get_name_indices_())
            #
            name_w_, name_h_ = w, n_c*name_f_h
            name_x_, name_y_ = x, y+h-name_h_
            #
            self._name_frame_rect.setRect(
                name_x_, name_y_,
                name_w_, name_h_
            )
        else:
            name_w_, name_h_ = 0, -f_spacing
        #
        if self._get_has_icon_() is True:
            icon_f_w, icon_f_h = self._icon_frame_size
            # grid to
            icon_count_ = self._get_icon_count_()
            icon_h_ = h - name_h_ - f_spacing
            c_0 = int(float(icon_h_)/icon_f_h)
            c_1 = math.ceil(float(icon_count_)/c_0)

            icon_x_, icon_y_ = x, y
            icon_w_, icon_h_ = icon_f_w*c_1, icon_h_
            #
            self._icon_frame_rect.setRect(
                icon_x_, icon_y_,
                icon_w_, icon_h_
            )
        else:
            icon_w_, icon_h_ = -f_spacing, 0
        #
        if self._get_has_image_() is True:
            image_x_, image_y_ = x+icon_w_+f_spacing, y
            image_w_, image_h_ = w-(icon_w_+f_spacing), h-(name_h_+f_spacing)
            self._image_frame_rect.setRect(
                image_x_, image_y_, image_w_, image_h_
            )

    def _set_widget_frame_geometry_update_as_list_mode_(self, pos, size):
        x, y = pos
        w, h = size
        width, height = self.width(), self.height()
        f_side = self._frame_side
        f_spacing = self._frame_spacing
        if self._get_has_icon_() is True:
            icon_f_w, icon_f_h = self._icon_frame_size
            icon_x_, icon_y_ = x, y
            icon_w_, icon_h_ = icon_f_w, h
            #
            self._icon_frame_rect.setRect(
                icon_x_, icon_y_,
                icon_w_, icon_h_
            )
        else:
            icon_w_, icon_h_ = -f_spacing, 0
        #
        if self._get_has_image_() is True:
            image_x_, image_y_ = x+(icon_w_+f_spacing), y
            image_w_, image_h_ = w-(icon_w_+f_spacing), h
            self._image_frame_rect.setRect(
                image_x_, image_y_, image_w_, image_h_
            )
        else:
            image_w_, image_h_ = -f_spacing, 0
        #
        if self._get_has_name_() is True:
            name_x_, name_y_ = x+(icon_w_+f_spacing)+(image_w_+f_spacing), y
            name_w_, name_h_ = width-(icon_w_+f_spacing)-(image_w_+f_spacing)-f_side*2, h
            #
            self._name_frame_rect.setRect(
                name_x_, name_y_,
                name_w_, name_h_
            )

    def _set_widget_icon_sub_geometries_update_(self):
        if self._get_has_icon_() is True:
            icon_indices = self._get_icon_indices_()
            if icon_indices:
                rect = self._icon_frame_rect
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                #
                side = 2
                spacing = 0
                #
                f_w, f_h = self._icon_frame_size
                i_w, i_h = self._icon_size
                #
                c_0 = int(float(h)/f_h)
                for i_icon_index in icon_indices:
                    c_1 = int(float(i_icon_index)/c_0)
                    if c_1 > 0:
                        i_icon_index_ = i_icon_index % c_0
                    else:
                        i_icon_index_ = i_icon_index
                    #
                    self._set_icon_rect_at_(
                        x+(f_w-i_w)/2+f_w*c_1, y+(f_h-i_h)/2+i_icon_index_*(f_h+spacing), i_w, i_h,
                        i_icon_index
                    )

    def _set_widget_image_sub_geometries_update_(self):
        if self._get_has_image_() is True:
            image_file_path = self._get_image_file_path_()
            rect = self._image_frame_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            i_w_0, i_h_0 = self._get_image_size_()
            if (i_w_0, i_h_0) != (0, 0):
                i_x, i_y, i_w, i_h = utl_gui_core.SizeMtd.set_fit_to(
                    (i_w_0, i_h_0), (w, h)
                )
                if self._get_movie_enable_() is True:
                    m_f_w, m_f_h = 32, 32
                    self._set_movie_rect_(
                        x + i_x + (i_w-m_f_w)/2, y + i_y + (i_h-m_f_h)/2,
                        m_f_w, m_f_h
                    )
                #
                if image_file_path is not None:
                    self._set_image_rect_(
                        x+i_x+2, y+i_y+2, i_w-4, i_h-4
                    )
                else:
                    image_name_text = self._image_name_text
                    if image_name_text is not None:
                        self._set_image_rect_(
                            x + i_x, y + i_y, i_w, i_h
                        )

    def _set_widget_name_sub_geometries_update_(self):
        if self._get_has_name_():
            name_indices = self._get_name_indices_()
            #
            rect = self._name_frame_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            #
            side = 2
            spacing = 0
            #
            f_w, f_h = self._name_frame_size
            i_w, i_h = self._name_size
            #
            self._set_index_rect_(
                x + 2, y + h - i_h, w - 4, i_h
            )
            for i_name_index in name_indices:
                i_x, i_y = x+(f_w-i_w)/2+side, y+(f_h-i_h)/2+i_name_index*(f_h+spacing)
                self._set_name_text_rect_at_(
                    i_x, i_y, w-(i_x-x)-side, i_h,
                    i_name_index
                )

    def _set_wgt_update_draw_(self):
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
    utl_gui_qt_abstract.AbsQtFrameDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    #
    utl_gui_qt_abstract.AbsQtItemStateDef,
):
    QT_ORIENTATION = None
    def _set_wgt_update_draw_(self):
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
        self._swap_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(self._swap_icon_name)
        )
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
        self._action_is_hovered = False
        #
        self._set_frame_def_init_()
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        #
        self._set_item_state_def_init_()
        #
        self._hovered_frame_border_color = QtBorderColor.Button
        self._hovered_frame_background_color = QtBackgroundColor.Button

        self._actioned_frame_border_color = QtBorderColor.Actioned
        self._actioned_frame_background_color = QtBackgroundColor.Actioned

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self._set_action_flag_(
                        self.ActionFlag.SplitHHover
                    )
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self._set_action_flag_(
                        self.ActionFlag.SplitVHover
                    )
                #
                self._set_action_hovered_(True)
            elif event.type() == QtCore.QEvent.Leave:
                self.setCursor(QtCore.Qt.ArrowCursor)
                #
                self._set_action_hovered_(False)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self._set_action_flag_(
                        self.ActionFlag.SplitHClick
                    )
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self._set_action_flag_(
                        self.ActionFlag.SplitVClick
                    )
                self._set_action_split_move_start_(event)
                self._set_action_pressed_(True)
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self._set_action_flag_(
                        self.ActionFlag.SplitHMove
                    )
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self._set_action_flag_(
                        self.ActionFlag.SplitVMove
                    )
                self._set_action_split_move_execute_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._set_action_split_move_stop_(event)
                self._set_action_pressed_(False)
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_wgt_update_geometry_()
        #
        offset = self._get_action_offset_()
        #
        if self._action_is_enable is True:
            condition = self._action_is_hovered, self._action_is_pressed
            if condition == (False, False):
                border_color = QtBackgroundColor.Transparent
                background_color = QtBackgroundColor.Transparent
            elif condition == (False, True):
                border_color = self._actioned_frame_border_color
                background_color = self._actioned_frame_background_color
            elif condition == (True, True):
                border_color = self._actioned_frame_border_color
                background_color = self._actioned_frame_background_color
            elif condition == (True, False):
                border_color = self._hovered_frame_border_color
                background_color = self._hovered_frame_background_color
            else:
                raise SyntaxError()
        else:
            border_color = QtBackgroundColor.ButtonDisable
            background_color = QtBackgroundColor.ButtonDisable
        #
        painter._set_frame_draw_by_rect_(
            self._frame_draw_rect,
            border_color=border_color,
            background_color=background_color,
            border_radius=1,
            offset=offset
        )

    def _set_wgt_update_geometry_(self):
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
        self._contract_l_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(icon_name_l)
        )
        self._contract_l_button.update()
        icon_name_r = [self._contract_icon_name_r, self._contract_icon_name_l][self._is_contract_r]
        self._contract_r_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(icon_name_r)
        )
        self._contract_r_button.update()

    def _set_update_(self):
        pass

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def splitter(self):
        return self.parent()

    def _set_action_split_move_start_(self, event):
        pass

    def _set_action_split_move_execute_(self, event):
        self._contract_l_button._set_action_flag_(self.ActionFlag.PressMove)
        self._contract_r_button._set_action_flag_(self.ActionFlag.PressMove)
        self._swap_button._set_action_flag_(self.ActionFlag.PressMove)
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

    def _set_action_split_move_stop_(self, event):
        self._contract_l_button._set_action_flag_clear_()
        self._contract_r_button._set_action_flag_clear_()
        self._swap_button._set_action_flag_clear_()


class _QtHSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitterHandle, self).__init__(*args, **kwargs)


class _QtVSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitterHandle, self).__init__(*args, **kwargs)


class _QtWindowHead(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
):
    def _set_wgt_update_draw_(self):
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
        self._close_button = _QtIconPressItem(self)
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
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        self._set_widget_geometries_update_()
        #
        painter._set_frame_draw_by_rect_(
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
        self._set_frame_rect_(
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


class _QtItemGuideRect(
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtTypeDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtPathDef,
    utl_gui_qt_abstract.AbsQtFrameDef,
    #
    utl_gui_qt_abstract.AbsQtChooseDef,
):
    def _set_wgt_update_draw_(self):
        pass

    def __init__(self, *args, **kwargs):
        self._set_icon_def_init_()
        self._set_type_def_init_()
        self._set_name_def_init_()
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
