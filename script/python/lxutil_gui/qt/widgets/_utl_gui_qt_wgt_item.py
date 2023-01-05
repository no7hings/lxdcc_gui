# coding=utf-8
import functools

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_chart

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui.qt import utl_gui_qt_core


class _QtListEntry(
    utl_gui_qt_abstract.AbsQtListWidget,
    utl_gui_qt_abstract.AbsQtHelpDef,
    #
    utl_gui_qt_abstract.AbsQtValueDef,
    utl_gui_qt_abstract.AbsQtValuesDef,
    #
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
    utl_gui_qt_abstract.AbsQtEntryDropDef,
):
    entry_changed = qt_signal()
    entry_added = qt_signal()
    def _get_value_(self):
        pass

    def __init__(self, *args, **kwargs):
        super(_QtListEntry, self).__init__(*args, **kwargs)
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
        self._set_entry_base_def_init_(self)
        self._set_entry_drop_def_init_(self)

        self.setAcceptDrops(self._entry_drop_is_enable)

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
                ('open folder', 'file/folder', (True, self._set_open_in_system_, False), QtGui.QKeySequence.Open)
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
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = False
                elif event.key() == QtCore.Qt.Key_Delete:
                    self._set_action_delete_execute_(event)
            elif event.type() == QtCore.QEvent.Wheel:
                pass
                # self._execute_action_wheel_(event)
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_view_all_items_viewport_showable_()
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

    def _set_entry_drop_enable_(self, boolean):
        super(_QtListEntry, self)._set_entry_drop_enable_(boolean)
        self.setAcceptDrops(boolean)
        # self.setDragDropMode(self.DropOnly)
        # self.setDropIndicatorShown(True)

    def _execute_action_drop_(self, event):
        data = event.mimeData()
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
                cs = bsc_core.MultiplyFileMtd.set_merge_to(
                    values,
                    ['*.####.*']
                )
                [self._set_value_append_(i) for i in cs]

    def _set_action_delete_execute_(self, event):
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
        super(_QtListEntry, self)._set_validator_use_as_storage_(boolean)
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
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(QtTextBrowser_, self).__init__(*args, **kwargs)
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
        self._set_entry_base_def_init_(self)

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
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility.QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_utility.QtEntryFrame):
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


class QtTextItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    #
    utl_gui_qt_abstract.AbsQtStatusDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtTextItem, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_name_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()

        self._set_status_def_init_()

        self._set_name_draw_font_(QtFonts.Label)
        self._name_text_option = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        if self._name_align == self.AlignRegion.Top:
            icn_frm_w, icn_frm_h = self._name_frame_size
            t_w, t_h = self._name_draw_size
            self._name_draw_rect.setRect(
                x, y+(icn_frm_h-t_h)/2, w, t_h
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
        painter = QtPainter(self)
        self._refresh_widget_draw_geometry_()
        # name
        if self._name_text is not None:
            color, hover_color = self._get_text_color_by_validator_status_(self._status)
            text_color = [color, hover_color][self._action_is_hovered]
            #
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=self._name_text,
                font_color=text_color,
                font=self._name_draw_font,
                text_option=self._name_text_option,
            )


class _QtInfoItem(QtWidgets.QWidget):
    pass


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
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtActionCheckDef,
    utl_gui_qt_abstract.AbsQtActionOptionPressDef,
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
        self._set_check_update_draw_()
        #
        self._set_name_draw_font_(QtFonts.Button)
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
                    elif self._action_flag == self.ActionFlag.PressClick:
                        self.clicked.emit()
                    elif self._action_flag == self.ActionFlag.OptionClick:
                        self.option_clicked.emit()
                    #
                    self._action_flag = None
                    self.update()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        self._refresh_widget_draw_geometry_()
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
            painter._draw_frame_by_rect_(
                rect=self._progress_rect,
                border_color=QtBackgroundColors.Transparent,
                background_color=Color.PROGRESS,
                border_radius=2,
                offset=offset
            )
        # check
        if self._get_check_action_is_enable_() is True:
            painter._set_icon_file_draw_by_rect_(
                self._check_icon_draw_rect,
                self._check_icon_file_path_current,
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
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtCheckItem, self).__init__(*args, **kwargs)
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
        self._set_icon_def_init_()
        self._set_name_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_check_def_init_()
        self._set_check_enable_(True)
        #
        self._set_value_default_def_init_()
        #
        self._set_check_update_draw_()
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
        self._set_frame_draw_geometry_(
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
        self._set_name_draw_geometry_(
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
                        self._set_item_check_action_run_()
                    #
                    self._set_action_flag_clear_()
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
        background_color = painter._get_item_background_color_1_by_rect_(
            self._check_action_rect,
            is_hovered=self._action_is_hovered,
            is_actioned=self._get_is_actioned_()
        )
        painter._draw_frame_by_rect_(
            self._check_action_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            border_radius=4,
            offset=offset
        )
        if self._check_is_enable is True:
            if self._check_icon_file_path_current is not None:
                painter._set_icon_file_draw_by_rect_(
                    rect=self._check_icon_draw_rect,
                    file_path=self._check_icon_file_path_current,
                    offset=offset
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
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionCheckDef,
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
        self._set_frame_def_init_()
        self._set_icon_def_init_()
        self._set_name_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_check_def_init_()
        self._set_check_enable_(True)
        #
        self._set_value_default_def_init_()
        #
        self._set_check_update_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_w, icn_h = self._icon_file_draw_size
        #
        self._set_frame_draw_geometry_(
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
        x += icn_frm_w+spacing
        self._set_name_draw_geometry_(
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
                        self._set_item_check_action_run_()
                    #
                    self._set_action_flag_clear_()
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
            border_radius=4,
            offset=offset
        )
        #
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                painter._set_icon_file_draw_by_rect_(
                    rect=self._icon_file_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset
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
        self._set_check_update_draw_()

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
                        self._set_item_check_action_run_()
                #
                self._set_action_flag_clear_()
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


class _QtItemRgbaChooseDropFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    def _refresh_widget_draw_(self):
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
        self._frame_border_color = QtBackgroundColors.Light
        self._hovered_frame_border_color = QtBackgroundColors.Hovered
        self._selected_frame_border_color = QtBackgroundColors.Selected
        self._frame_background_color = QtBackgroundColors.Dark

        self._chart = _utl_gui_qt_wgt_chart.QtColorChooseChart(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self.parent():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._close_popup_()
        elif widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._end_action_popup_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            elif event.type() == QtCore.QEvent.Show:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        painter = QtPainter(self)
        #
        painter._draw_popup_frame_(
            bck_rect,
            margin=self._popup_margin,
            side=self._popup_side,
            shadow_radius=self._popup_shadow_radius,
            region=self._popup_region,
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
        )

    def _refresh_widget_draw_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius-2
        #
        self._chart.setGeometry(
            v_x, v_y, v_w, v_h
        )
        self._chart.update()

    def _start_action_popup_(self):
        parent = self.parent()
        press_rect = parent._get_color_rect_()
        press_point = self._get_popup_press_point_(parent, press_rect)
        desktop_rect = get_qt_desktop_rect()
        self._show_popup_0_(
            press_point,
            press_rect,
            desktop_rect,
            320, 320
        )
        self._chart._set_color_rgba_(*parent._get_color_rgba_())
        parent._set_focused_(True)

    def _end_action_popup_(self, *args, **kwargs):
        r, g, b, a = self._chart._get_color_rgba_()
        self.parent()._set_color_rgba_(r, g, b, a)


class QtValueEntryForConstant(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit_
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryForConstant, self).__init__(*args, **kwargs)
        #
        self._set_value_entry_def_init_(self)
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
        super(QtValueEntryForConstant, self)._set_value_entry_enable_(boolean)

        self._value_entry.setReadOnly(not boolean)

        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dark
        ][boolean]
        self._refresh_widget_draw_()


class QtValueEntryForScript(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = QtTextBrowser_
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryForScript, self).__init__(*args, **kwargs)
        #
        self._set_value_entry_def_init_(self)
        self._set_value_default_def_init_()
        #
        self._build_entry_(self._value_type)

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
        #
        self._resize_gui = _utl_gui_qt_wgt_utility.QtVResizeFrame(self)
        self._resize_gui.hide()

    def _set_item_value_entry_enable_(self, boolean):
        self._value_entry.setReadOnly(not boolean)

    def _get_resize_gui_(self):
        return self._resize_gui

    def _set_resize_enable_(self, boolean):
        self._resize_gui.setVisible(boolean)

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryForScript, self)._set_value_entry_enable_(boolean)

        self._value_entry.setReadOnly(not boolean)
        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dark
        ][boolean]
        self._refresh_widget_draw_()


class QtaValueEntryForRgba(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtRgbaDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit_
    #
    POPUP_CHOOSE_WIDGET_CLASS = _QtItemRgbaChooseDropFrame
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtaValueEntryForRgba, self).__init__(*args, **kwargs)
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
        self._set_value_entry_def_init_(self)
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
        super(QtaValueEntryForRgba, self)._refresh_widget_draw_geometry_()
        #
        x, y = 0, 0
        w, h = 20, self.height()
        c_w, c_h = 16, 16
        self._color_rect.setRect(
            x+2, y+(h-c_h)/2, c_w, c_h
        )

    def eventFilter(self, *args):
        super(QtaValueEntryForRgba, self).eventFilter(*args)
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
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtaValueEntryForRgba, self).paintEvent(self)
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
        widget = self.POPUP_CHOOSE_WIDGET_CLASS(self)
        # widget._set_popup_offset_(0, 22)
        widget._start_action_popup_()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self.update()

    def _set_value_entry_enable_(self, boolean):
        pass


class QtValueEntryForEnumerate(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtValueEntryEnumerate,
    utl_gui_qt_abstract.AbsQtValueDefaultDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionEntryDef,
    #
    utl_gui_qt_abstract.AbsQtChooseDef,
    utl_gui_qt_abstract.AbsQtEntryCompletionDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit_
    #
    POPUP_CHOOSE_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtPopupChooseFrame
    COMPLETION_FRAME_CLASS = _utl_gui_qt_wgt_utility.QtPopupCompletionFrame
    def _execute_popup_choose_(self):
        self._popup_choose_frame._start_action_popup_()

    def _refresh_widget_(self):
        self._refresh_enumerate_()
        self._refresh_widget_draw_()

    def _refresh_enumerate_(self):
        if self._value_enumerate_index_is_enable is True:
            values = self._get_value_enumerate_strings_()
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
                self._value_index_label.hide()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryForEnumerate, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._set_value_entry_enumerate_init_(self)
        self._set_value_default_def_init_()
        #
        self._set_action_def_init_(self)
        self._set_action_entry_def_init_(self)
        #
        self._set_choose_def_init_()
        self._set_entry_completion_def_init_(self)
        #
        self._build_entry_(self._value_type)

    def eventFilter(self, *args):
        super(QtValueEntryForEnumerate, self).eventFilter(*args)
        #
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                if event.type() == QtCore.QEvent.Wheel:
                    self._execute_action_wheel_(event)
        return False

    def _execute_action_wheel_(self, event):
        delta = event.angleDelta().y()
        values = self._get_value_enumerate_strings_()
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
                self._send_user_choose_changed_emit_()

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
        self._value_entry._set_enter_enable_(False)
        #
        self._value_index_label = QtTextItem()
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
        self._popup_choose_frame = self.POPUP_CHOOSE_WIDGET_CLASS(self)
        self._popup_choose_frame._set_popup_auto_resize_enable_(True)
        self._popup_choose_frame._set_popup_entry_(self._value_entry)
        self._popup_choose_frame._set_popup_entry_frame_(self)
        self._popup_choose_frame.hide()
        self._value_entry.up_key_pressed.connect(
            self._popup_choose_frame._execute_popup_scroll_to_pre_
        )
        self._value_entry.down_key_pressed.connect(
            self._popup_choose_frame._execute_popup_scroll_to_next_
        )
        self._value_entry.user_entry_finished.connect(
            self._popup_choose_frame._end_action_popup_
        )
        #
        self._build_entry_completion_(self._value_entry, self)

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryForEnumerate, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_enter_enable_(boolean)
        self._value_choose_button.setHidden(not boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_()

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_entry_drop_enable_(boolean)

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
    #
    def _get_choose_values_(self):
        return self._get_value_enumerate_strings_()

    def _get_choose_current_values_(self):
        return [self._get_value_()]

    def _extend_choose_current_values_(self, values):
        self._set_value_(values[-1])
        #
        self._refresh_widget_()

    def _set_value_default_by_enumerate_index_(self, index):
        self._set_value_default_(
            self._get_value_enumerate_string_at_(index)
        )


class QtValueEntryForTuple(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    utl_gui_qt_abstract.AbsQtValueEntryForTupleDef,
):
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit_
    #
    entry_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtValueEntryForTuple, self).__init__(*args, **kwargs)
        #
        self._set_value_entry_for_tuple_def_init_()
        #
        # s = _utl_gui_qt_wgt_utility.QtHSplitter()
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
                i_widget = _utl_gui_qt_wgt_utility.QtLineEdit_()
                i_widget._set_value_type_(self._value_type)
                self._value_entry_layout.addWidget(i_widget)
                self._value_entries.append(i_widget)

    def _set_value_entry_enable_(self, boolean):
        pass


class QtValueEntryForArray(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    utl_gui_qt_abstract.AbsQtChooseDef,
):
    QT_VALUE_ENTRY_CLASS = _QtListEntry
    #
    POPUP_CHOOSE_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtPopupChooseFrame
    #
    add_press_clicked = qt_signal()
    def _execute_popup_choose_(self):
        self._popup_choose_frame._start_action_popup_()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryForArray, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._set_name_def_init_()
        self._set_value_entry_def_init_(self)
        self._set_choose_def_init_()
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
        self._popup_choose_frame = self.POPUP_CHOOSE_WIDGET_CLASS(self)
        # self._popup_choose_frame._set_popup_offset_(0, 22)
        self._popup_choose_frame._set_popup_entry_(self._value_entry)
        self._popup_choose_frame._set_popup_entry_frame_(self)
        self._popup_choose_frame.hide()

        self._resize_gui = _utl_gui_qt_wgt_utility.QtVResizeFrame(self)

    def _get_value_entry_gui_(self):
        return self._value_entry

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryForArray, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_entry_drop_enable_(boolean)

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
    # resize
    def _get_resize_gui_(self):
        return self._resize_gui

    def _get_popup_choose_gui_(self):
        return self._popup_choose_frame
    # choose
    def _extend_choose_current_values_(self, values):
        self._set_value_extend_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()

    def _set_choose_tag_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_tag_filter_enable_(boolean)

    def _set_choose_item_size_(self, w, h):
        self._popup_choose_frame._set_popup_item_size_(w, h)

    def _set_choose_multiply_enable_(self, boolean):
        super(QtValueEntryForArray, self)._set_choose_multiply_enable_(boolean)
        self._popup_choose_frame._set_popup_multiply_enable_(boolean)


class QtValueEntryForArrayAsChoose(
    _utl_gui_qt_wgt_utility.QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    utl_gui_qt_abstract.AbsQtChooseDef,
):
    QT_VALUE_ENTRY_CLASS = _QtListEntry
    #
    POPUP_CHOOSE_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtPopupChooseFrame
    #
    add_press_clicked = qt_signal()
    def _execute_popup_choose_(self):
        self._popup_choose_frame._start_action_popup_()

    def __init__(self, *args, **kwargs):
        super(QtValueEntryForArrayAsChoose, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._set_name_def_init_()
        self._set_value_entry_def_init_(self)
        self._set_choose_def_init_()
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
        self._popup_choose_frame = self.POPUP_CHOOSE_WIDGET_CLASS(self)
        # self._popup_choose_frame._set_popup_offset_(0, 22)
        self._popup_choose_frame._set_popup_entry_(self._value_entry)
        self._popup_choose_frame._set_popup_entry_frame_(self)
        self._popup_choose_frame.hide()

        self._resize_gui = _utl_gui_qt_wgt_utility.QtVResizeFrame(self)

    def _get_value_entry_gui_(self):
        return self._value_entry

    def _set_value_entry_enable_(self, boolean):
        super(QtValueEntryForArrayAsChoose, self)._set_value_entry_enable_(boolean)

        self._value_entry._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_entry_drop_enable_(boolean)

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
    # resize
    def _get_resize_gui_(self):
        return self._resize_gui

    def _get_popup_choose_gui_(self):
        return self._popup_choose_frame
    # choose
    def _extend_choose_current_values_(self, values):
        self._set_value_extend_(values)

    def _get_choose_current_values_(self):
        return self._get_values_()

    def _set_choose_tag_filter_enable_(self, boolean):
        self._popup_choose_frame._set_popup_tag_filter_enable_(boolean)

    def _set_choose_item_size_(self, w, h):
        self._popup_choose_frame._set_popup_item_size_(w, h)

    def _set_choose_multiply_enable_(self, boolean):
        super(QtValueEntryForArrayAsChoose, self)._set_choose_multiply_enable_(boolean)
        self._popup_choose_frame._set_popup_multiply_enable_(boolean)


class QtFilterBar(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionEntryDef,
    #
    utl_gui_qt_abstract.AbsQtEntryHistoryDef,
    #
    utl_gui_qt_abstract.AbsQtChooseDef,
    utl_gui_qt_abstract.AbsQtEntryCompletionDef,
):
    occurrence_previous_press_clicked = qt_signal()
    occurrence_next_press_clicked = qt_signal()
    #
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit_
    #
    POPUP_CHOOSE_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtPopupChooseFrame
    COMPLETION_FRAME_CLASS = _utl_gui_qt_wgt_utility.QtPopupCompletionFrame
    def _execute_popup_choose_(self):
        self._entry_history_choose_drop_frame._start_action_popup_()

    def _refresh_widget_(self):
        self.update()

    def _refresh_widget_draw_(self):
        pass

    def __init__(self, *args, **kwargs):
        super(QtFilterBar, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        qt_layout_0 = QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        self._set_value_entry_def_init_(self)
        #
        self._set_action_def_init_(self)
        self._set_action_entry_def_init_(self)
        #
        self._set_choose_def_init_()
        #
        self._set_entry_completion_def_init_(self)
        #
        self._result_label = _utl_gui_qt_wgt_utility.QtLabel()
        qt_layout_0.addWidget(self._result_label)
        self._result_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        self._value_entry_frame = _utl_gui_qt_wgt_utility.QtEntryFrame()
        self._value_entry_frame.setMaximumWidth(240)
        qt_layout_0.addWidget(self._value_entry_frame)
        #
        self._build_entry_(str)
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
        self._set_entry_history_def_init_(self)
        #
        self._result_count = None
        self._result_index = None
        #
        self._refresh_filter_()

    def _build_entry_(self, value_type):
        self._value_type = value_type
        self._value_entry_layout = QtHBoxLayout(self._value_entry_frame)
        self._value_entry_layout.setContentsMargins(*[0]*4)
        self._value_entry_layout.setSpacing(2)
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
        self._header_button._set_menu_raw_(
            [
                ('option', None, None),
                (),
                ('history', None, None)
            ]
        )
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
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
        self._entry_clear_button.clicked.connect(self._execute_user_entry_clear_)
        #
        self._value_history_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._value_entry_layout.addWidget(self._value_history_button)
        self._value_history_button._set_icon_frame_draw_size_(18, 18)
        #
        self._value_history_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('history'))
        self._value_history_button._set_sub_icon_file_path_(utl_gui_core.RscIconFile.get('down'))
        self._value_history_button.press_clicked.connect(
            self._execute_popup_choose_
        )
        self._value_history_button.hide()
        #
        self._entry_history_choose_drop_frame = self.POPUP_CHOOSE_WIDGET_CLASS(self)
        # self._entry_history_choose_drop_frame._set_popup_offset_(0, 22)
        self._entry_history_choose_drop_frame._set_popup_entry_(self._value_entry)
        self._entry_history_choose_drop_frame._set_popup_entry_frame_(self._value_entry_frame)
        self._value_entry.up_key_pressed.connect(
            self._entry_history_choose_drop_frame._execute_popup_scroll_to_pre_
        )
        self._value_entry.down_key_pressed.connect(
            self._entry_history_choose_drop_frame._execute_popup_scroll_to_next_
        )
        self._entry_history_choose_drop_frame.hide()

        self._build_entry_completion_(self._value_entry, self._value_entry_frame)

        self._entry_completion_frame.completion_finished.connect(self._add_entry_history_value_)
    #
    def _set_entry_tip_(self, text):
        self._value_entry._set_entry_tip_(text)

    def _refresh_filter_(self):
        self._match_case_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(self._match_case_icon_names[self._is_match_case])
        )
        #
        self._match_word_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(self._match_word_icon_names[self._is_match_word])
        )
        #
        self._value_entry.setPlaceholderText(
            ' and '.join([i for i in [[None, 'Match-case'][self._is_match_case], [None, 'Match-word'][self._is_match_word]] if i])
        )

    def _execute_filter_match_case_swap_(self):
        self._is_match_case = not self._is_match_case
        self._refresh_filter_()
        #
        self._send_enter_changed_emit_()

    def _execute_filter_match_word_swap_(self):
        self._is_match_word = not self._is_match_word
        self._refresh_filter_()
        self._send_enter_changed_emit_()

    def _get_qt_entry_(self):
        return self._value_entry

    def _execute_entry_clear_(self):
        self._value_entry._set_clear_()
        self._value_entry.entry_cleared.emit()
        self._send_enter_changed_emit_()

    def _execute_user_entry_clear_(self):
        self._value_entry._set_clear_()
        self._value_entry.user_entry_cleared.emit()
        self._send_user_enter_changed_emit_()

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

    def _set_result_count_(self, value):
        self._result_count = value
        self._result_index = None
        self._refresh_filter_result_()

    def _set_result_index_(self, value):
        self._result_index = value
        self._refresh_filter_result_()

    def _refresh_filter_result_(self):
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
        self._refresh_filter_result_()

    def _set_entry_focus_(self, boolean):
        self._value_entry._set_focused_(boolean)

    def _set_entry_history_key_(self, key):
        super(QtFilterBar, self)._set_entry_history_key_(key)
        #
        self._value_history_button.show()

    def _add_entry_history_value_(self, value):
        if self._entry_history_key is not None:
            if value:
                if self._get_entry_history_value_is_valid_(value) is True:
                    utl_core.History.set_append(
                        self._entry_history_key,
                        value
                    )
            #
            self._refresh_entry_history_()

    def _setup_entry_history_(self):
        if self._entry_history_key is not None:
            value = self._get_value_()
            if value:
                if self._get_entry_history_value_is_valid_(value) is True:
                    utl_core.History.set_append(
                        self._entry_history_key,
                        value
                    )
            #
            self._refresh_entry_history_()

    def _refresh_entry_history_(self):
        if self._entry_history_key is not None:
            values = utl_core.History.get(
                self._entry_history_key
            )
            if values:
                # latest show on top
                values.reverse()
                # value validation
                values = [i for i in values if self._get_entry_history_value_is_valid_(i) is True]
                #
                self._set_choose_values_(values)
                #
                self._value_history_button._set_action_enable_(
                    True
                )
            else:
                self._set_choose_values_clear_()
                self._value_history_button._set_action_enable_(
                    False
                )

    def _extend_choose_current_values_(self, values):
        self._set_value_(values[-1])


class _QtHExpandItem0(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtActionExpandDef,
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
        self._set_name_def_init_()
        self._name_draw_font = Font.GROUP
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
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('expandopen')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('expandclose')

        self._expand_sub_icon_file_path_0 = None
        self._expand_sub_icon_file_path_1 = None

        self._action_is_hovered = False
        #
        self._refresh_expand_()
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

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        #
        self._set_frame_draw_geometry_(
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
        if self._icon_name_is_enable is True:
            if self._icon_name_text is not None:
                icn_w, icn_h = self._icon_name_draw_size
                self._set_icon_name_draw_rect_(
                    c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
                )
                c_x += icn_frm_w+spacing
        #
        self._set_name_draw_geometry_(
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
                        self._set_item_expand_action_run_()
                    #
                    self.press_toggled.emit(False)
                #
                self._set_action_flag_clear_()
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
        background_color = [self._frame_background_color, self._hovered_frame_background_color][self._action_is_hovered]
        # painter.setBrush(background_color)
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            # border_radius=1,
            offset=offset
        )
        # file-icon
        painter._set_icon_file_draw_by_rect_(
            self._icon_file_draw_rect,
            self._icon_file_path,
            offset=offset
        )
        if self._sub_icon_file_path is not None:
            painter._set_icon_file_draw_by_rect_(
                rect=self._sub_icon_file_draw_rect,
                file_path=self._sub_icon_file_path,
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
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=self._name_draw_font,
                font_color=color,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )

    def set_expanded(self, boolean):
        self._item_is_expanded = boolean

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._item_is_expanded]
        )
        self._set_sub_icon_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._item_is_expanded]
        )
        #
        self._refresh_widget_draw_()


class _QtHExpandItem1(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtActionExpandDef,
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
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
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
        background_color = [self._frame_background_color, self._hovered_frame_background_color][self._action_is_hovered]
        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            # border_radius=self._frame_border_radius,
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

    def _refresh_expand_(self):
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
                [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._item_is_expanded]
            )
        elif self._item_expand_direction == self.EXPAND_BOTTOM_TO_TOP:
            self._set_icon_file_path_(
                [self._expand_icon_file_path_1, self._item_expand_icon_file_path_2][self._item_is_expanded]
            )
        #
        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._set_frame_draw_geometry_(
            x+1, y+1, w-2, h-2
        )
        #
        icn_frm_w, icn_frm_h = 12, 12
        i_w, i_h = 8, 8
        #
        if self._item_expand_direction == self.EXPAND_TOP_TO_BOTTOM:
            self._set_icon_file_draw_rect_(
                x+(icn_frm_w-i_w)/2, y+(icn_frm_h-i_h)/2,
                i_w, i_h
            )
        elif self._item_expand_direction == self.EXPAND_BOTTOM_TO_TOP:
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
        self._item_expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-left')


class _AbsQtSplitterHandle(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    #
    utl_gui_qt_abstract.AbsQtStateDef,
):
    QT_ORIENTATION = None
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitterHandle, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._swap_enable = True
        #
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        #
        self._contract_icon_name_l = ['contract_h_l', 'contract_v_l'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._contract_icon_name_r = ['contract_h_r', 'contract_v_r'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._swap_icon_name = ['swap_h', 'swap_v'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        #
        self._contract_frame_size = [(16, 8), (8, 16)][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
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
        layout.setContentsMargins(*[0]*4)
        layout.setSpacing(2)
        self._contract_l_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._contract_l_button._set_icon_frame_draw_size_(*self._contract_frame_size)
        self._contract_l_button._set_icon_file_draw_percent_(1.0)
        self._contract_l_button.setMaximumSize(*self._contract_frame_size)
        self._contract_l_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._contract_l_button)
        self._contract_l_button.clicked.connect(self._set_contract_l_switch_)
        self._contract_l_button.setToolTip(
            '"LMB-click" to contact left/top.'
        )
        #
        self._swap_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._swap_button._set_icon_file_path_(utl_gui_core.RscIconFile.get(self._swap_icon_name))
        self._swap_button._set_icon_frame_draw_size_(*self._contract_frame_size)
        self._swap_button._set_icon_file_draw_percent_(1.0)
        self._swap_button.setMaximumSize(*self._contract_frame_size)
        self._swap_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._swap_button)
        self._swap_button.clicked.connect(self._set_swap_)
        self._swap_button.setToolTip(
            '"LMB-click" to swap.'
        )
        #
        self._contract_r_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._contract_r_button._set_icon_frame_draw_size_(*self._contract_frame_size)
        self._contract_r_button._set_icon_file_draw_percent_(1.0)
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
        self._set_state_def_init_()
        #
        self._hovered_frame_border_color = QtBorderColors.Button
        self._hovered_frame_background_color = QtBackgroundColors.Button

        self._actioned_frame_border_color = QtBorderColors.Actioned
        self._actioned_frame_background_color = QtBackgroundColors.Actioned

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
                self._set_pressed_(True)
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
                self._set_pressed_(False)
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        if self._action_is_enable is True:
            condition = self._action_is_hovered, self._is_pressed
            if condition == (False, False):
                border_color = QtBackgroundColors.Transparent
                background_color = QtBackgroundColors.Transparent
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
            border_color = QtBackgroundColors.ButtonDisable
            background_color = QtBackgroundColors.ButtonDisable
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=border_color,
            background_color=background_color,
            border_radius=1,
            offset=offset
        )

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            self._set_frame_draw_geometry_(x+1, y, w-3, h)
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            self._set_frame_draw_geometry_(x, y+1, w, h-3)

    def _set_contract_l_switch_(self):
        if self._is_contract_r is True:
            self._set_contract_r_switch_()
        else:
            splitter = self._get_splitter_()
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
                splitter._set_adjacent_sizes_(indices, sizes)
            else:
                splitter._set_adjacent_sizes_(indices, self._sizes)
            #
            self._set_contract_buttons_update_()

    def _set_contract_r_switch_(self):
        if self._is_contract_l is True:
            self._set_contract_l_switch_()
        else:
            splitter = self._get_splitter_()
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
        index_l = splitter.indexOf(self)-1
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

    def _get_splitter_(self):
        return self.parent()

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
        index_l = splitter.indexOf(self)-1
        index_r = splitter.indexOf(self)
        indices = index_l, index_r
        s_l_o, s_r_o = splitter._get_size_(index_l), splitter._get_size_(index_r)
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            s_l, s_r = s_l_o+x, s_r_o-x
            splitter._set_adjacent_sizes_(indices, [s_l, s_r])
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            s_l, s_r = s_l_o+y, s_r_o-y
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
        self._set_frame_draw_geometry_(
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


class _QtGuideRect(
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
