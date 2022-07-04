# coding:utf-8
from lxutil import utl_configure, utl_core

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_chart, _utl_gui_qt_wgt_window

from lxutil_gui.proxy import utl_gui_prx_configure, utl_gui_prx_core, utl_gui_prx_abstract

from lxutil_gui import utl_gui_core

import lxutil.modifiers as utl_modifiers

from lxbasic import bsc_configure

import lxutil.dcc.dcc_objects as utl_dcc_objects


class PrxExpandedGroup(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxExpandedGroup, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignTop)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(2)
        # header
        self._head = _utl_gui_qt_wgt_item._QtHExpandItem0()
        qt_layout_0.addWidget(self._head)
        self._head.setMaximumHeight(20)
        self._head.setMinimumHeight(20)
        self._head.expand_toggled.connect(self.set_expanded)
        self._head.setToolTip('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(0, 0, 0, 0)
        qt_layout_1.setSpacing(2)
        #
        self._layout = qt_layout_1
        #
        self._view = qt_widget_1
        #
        self._set_item_expand_update_()

    def _set_item_expand_update_(self):
        self._view.setVisible(self.get_is_expanded())

    def set_name(self, name):
        self._head._set_name_text_(name)
        self._head._set_icon_name_text_(name)

    def set_name_icon_enable(self, boolean):
        self._head._set_name_icon_enable_(boolean)

    def set_name_font_size(self, size):
        self._head._set_name_font_size_(size)

    def set_expanded(self, boolean):
        self._head._set_item_expanded_(boolean)
        self._set_item_expand_update_()

    def set_head_visible(self, boolean):
        self._head.setHidden(not boolean)

    def get_is_expanded(self):
        return self._head._get_item_is_expanded_()

    def set_widget_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
            self._layout.addWidget(widget)
        else:
            qt_widget = widget.widget
        #
        if qt_widget != self.widget:
            #
            self._layout.addWidget(qt_widget)

    def set_layout_alignment_to_top(self):
        self._layout.setAlignment(
            utl_gui_qt_core.QtCore.Qt.AlignTop
        )

    def set_size_mode(self, mode):
        if mode == 0:
            self._view.setSizePolicy(
                utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
            )
        elif mode == 1:
            self._view.setSizePolicy(
                utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
            )

    def set_height_match_to_minimum(self):
        self._view.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def set_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()
        #
        rcs_fnc_(self._layout)


class PrxScrollArea(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtScrollArea
    def __init__(self, *args, **kwargs):
        super(PrxScrollArea, self).__init__(*args, **kwargs)
        self._layout = self.widget._layout

    def set_widget_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._layout.addWidget(widget)
        else:
            self._layout.addWidget(widget.widget)

    def set_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()
        #
        rcs_fnc_(self._layout)


class PrxHToolBar(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxHToolBar, self).__init__(*args, **kwargs)
        #
        self.widget.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def _set_build_(self):
        self._bar_height = 24
        self._bar_height_min = 12
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        # header
        self._head = _utl_gui_qt_wgt_item._QtHExpandItem1()
        qt_layout_0.addWidget(self._head)
        self._head.expand_toggled.connect(self.set_expanded)
        self._head.setToolTip('LMB-click to expand "on" / "off"')
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(0, 0, 0, 0)
        qt_layout_1.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self._qt_layout_0 = qt_layout_1
        #
        self._view = qt_widget_1
        #
        self._set_item_expand_update_()
        #
        self._view.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def _set_item_expand_update_(self):
        if self.get_is_expanded() is True:
            self._head.setMaximumSize(self._bar_height_min, self._bar_height)
            self._head.setMinimumSize(self._bar_height_min, self._bar_height_min)
            #
            self.widget.setMaximumHeight(self._bar_height)
            self.widget.setMinimumHeight(self._bar_height)
        else:
            self._head.setMaximumSize(166667, self._bar_height_min)
            self._head.setMinimumSize(self._bar_height_min, self._bar_height_min)
            #
            self.widget.setMaximumHeight(self._bar_height_min)
            self.widget.setMinimumHeight(self._bar_height_min)
        #
        self._view.setVisible(self.get_is_expanded())
        self._head._set_item_expand_update_()

    def set_name(self, name):
        self._head.set_name(name)

    def set_expanded(self, boolean):
        self._head._set_item_expanded_(boolean)
        self._set_item_expand_update_()

    def set_expand_swap(self):
        self._head._set_item_expanded_swap_()
        self._set_item_expand_update_()

    def get_is_expanded(self):
        return self._head._get_item_is_expanded_()

    def set_widget_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def set_bar_height(self, h):
        self._bar_height = h
        self._set_item_expand_update_()

    def get_qt_layout(self):
        return self._qt_layout_0

    def set_top_direction(self):
        self._head._set_item_expand_direction_(self._head.EXPAND_TOP_TO_BOTTOM)

    def set_bottom_direction(self):
        self._head._set_item_expand_direction_(self._head.EXPAND_BOTTOM_TO_TOP)

    def set_border_radius(self, radius):
        self._head._set_frame_border_radius_(radius)


class Window(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMainWindow
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

    def _set_build_(self):
        self._main_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._main_widget)
        self._main_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._main_widget)

    def get_main_widget(self):
        return self._main_widget

    def set_widget_add(self, widget):
        self._main_layout.addWidget(widget)


class ContentWidget(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(ContentWidget, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._qt_label_0._set_name_text_(text)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(0)
        #
        qt_top_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_top_widget_0.setMaximumHeight(24)
        qt_top_widget_0.setMinimumHeight(24)
        qt_layout_0.addWidget(qt_top_widget_0)
        #
        qt_top_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_top_widget_0)
        self._qt_label_0 = _utl_gui_qt_wgt_item._QtTextItem()
        self._qt_label_0._set_name_text_option_(
            utl_gui_qt_core.QtCore.Qt.AlignHCenter | utl_gui_qt_core.QtCore.Qt.AlignVCenter
        )
        self._qt_label_0._set_name_font_size_(12)
        qt_top_layout_1.addWidget(self._qt_label_0)
        self._button_0 = PrxIconPressItem()
        self._button_0.set_icon_name('close')
        qt_top_layout_1.addWidget(self._button_0.widget)

        self._qt_central_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_central_widget_0.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding, utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_layout_0.addWidget(self._qt_central_widget_0)
        self._qt_central_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_central_widget_0)
        self._qt_central_layout.setContentsMargins(0, 0, 0, 0)

    def set_widget_add(self, widget):
        self._qt_central_layout.addWidget(widget)

    def set_close_connect_to(self, method):
        self._button_0.widget.clicked.connect(method)
    @property
    def central_widget(self):
        return self._qt_central_widget_0
    @property
    def central_layout(self):
        return self._qt_central_layout


class PrxTextBrowser(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxTextBrowser, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        widget = _utl_gui_qt_wgt_item._QtScriptValueEntryItem()
        qt_layout_0.addWidget(widget)
        self._qt_text_browser_0 = widget._item_value_entry_widget

    def set_markdown_file_open(self, file_path):
        if file_path:
            import markdown
            with open(file_path) as f:
                raw = f.read()
                raw = raw.decode('utf-8')
                html = markdown.markdown(raw)
                self._qt_text_browser_0.setHtml(html)

    def set_add(self, text):
        if isinstance(text, (str, unicode)):
            self._qt_text_browser_0.append(
                text
            )

    def set_result_add(self, text):
        self._qt_text_browser_0.append(
            utl_gui_core.HtmlText.get_text(text)
        )

    def set_error_add(self, text):
        self._qt_text_browser_0.append(
            utl_gui_core.HtmlText.get_text(text, font_color=utl_gui_prx_configure.Html.RED)
        )

    def set_warning_add(self, text):
        self._qt_text_browser_0.append(
            utl_gui_core.HtmlText.get_text(text, font_color=utl_gui_prx_configure.Html.YELLOW)
        )

    def set_print_add(self, text):
        self._qt_text_browser_0._set_content_add_(text)

    def set_print_add_use_thread(self, text):
        self._qt_text_browser_0._set_content_add_use_thread_(text)

    def set_print_over_use_thread(self, text):
        self._qt_text_browser_0._set_print_over_use_thread_(text)

    def set_content(self, text, as_html=False):
        if as_html is True:
            self._qt_text_browser_0.setHtml(
                text
            )
        else:
            self._qt_text_browser_0.setText(
                text
            )

    def set_font_size(self, size):
        font = self.widget.font()
        font.setPointSize(size)
        self._qt_text_browser_0.setFont(font)

    def get_content(self, as_html=False):
        if as_html is True:
            return self._qt_text_browser_0.toHtml()
        return self._qt_text_browser_0.toPlainText()

    def set_status(self, status):
        self.widget._set_status_(status)


class PrxMenu(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMenu
    def __init__(self, *args, **kwargs):
        super(PrxMenu, self).__init__(*args, **kwargs)

    def set_name(self, name):
        self.widget.setTitle(name)

    def set_setup(self, menu_raws):
        self.widget._set_menu_raw_(menu_raws)

    def set_menu_raw(self, menu_raws):
        self.widget._set_menu_raw_(menu_raws)

    def set_menu_content(self, content):
        self.widget._set_menu_content_(content)

    def set_show(self, boolean=True):
        self.widget.popup(
            utl_gui_qt_core.QtGui.QCursor().pos()
        )


class ProgressWindow(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtProgressDialog
    def __init__(self, title, max_value, *args, **kwargs):
        super(ProgressWindow, self).__init__(*args, **kwargs)
        self._title = title
        self._value = 0
        self._max_value = max_value
        self.widget.setWindowTitle(self._title)
        self.widget.setMaximum(self._max_value)
        self.widget.setValue(self._value)

    def set_label(self, text):
        if text is not None:
            self.widget.setLabelText(text)

    def set_show(self):
        self.set_window_show()

    def set_update(self, label=None):
        self._value += 1
        self.widget.setMaximum(self._max_value)
        self.widget.setValue(self._value)
        self.widget.update()
        self.set_label(label)
        if self._value == self._max_value:
            self.set_window_close()

    def set_close(self):
        self.set_window_close()


class PrxIconPressItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtIconPressItem
    def __init__(self, *args, **kwargs):
        super(PrxIconPressItem, self).__init__(*args, **kwargs)
        self.widget.setMaximumSize(20, 20)
        self.widget.setMinimumSize(20, 20)

    def set_name(self, *args, **kwargs):
        self.widget._set_name_text_(*args, **kwargs)

    def set_icon_name(self, icon_name):
        self.widget._set_icon_file_path_(utl_core.Icon.get(icon_name))

    def set_icon_by_name_text(self, text):
        self.widget._set_icon_name_text_(text)

    def set_icon_size(self, w, h):
        self.widget._set_file_icon_size_(w, h)

    def set_press_clicked_connect_to(self, fnc):
        self.widget.clicked.connect(fnc)

    def set_click(self):
        self.widget._set_action_press_click_emit_send_()

    def set_tool_tip(self, *args, **kwargs):
        self.widget._set_tool_tip_(*args, **kwargs)

    def set_action_enable(self, boolean):
        self._qt_widget._set_action_enable_(boolean)


class PrxPressItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxPressItem, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(20)
        self.widget.setMinimumHeight(20)

    def set_enable(self, boolean):
        self.widget._set_action_enable_(boolean)

    def set_check_enable(self, boolean):
        self.widget._set_action_check_enable_(boolean)
        self.widget.update()

    def get_is_checked(self):
        return self.widget._get_item_is_checked_()

    def set_checked(self, boolean):
        self.widget._set_item_checked_(boolean)

    def set_option_click_enable(self, boolean):
        self.widget._set_item_option_click_enable_(boolean)
        self.widget.update()

    def set_icon_name(self, icon_name):
        self.widget._icon_file_path = utl_core.Icon.get(icon_name)
        self.widget._icon_is_enable = True
        self.widget.update()

    def set_icon_by_color(self, color):
        self.widget._color_icon_rgb = color
        self.widget._icon_is_enable = True
        self.widget.update()

    def set_icon_by_name_text(self, text):
        self.widget._set_icon_name_text_(text)

    def set_icon_color_by_name(self):
        pass

    def set_width(self, w):
        self.widget.setMinimumWidth(w)

    def set_icon_size(self, w, h):
        self.widget._file_icon_size = w, h

    def set_name(self, text):
        self.widget._set_name_text_(text)

    def set_tool_tip(self, raw, as_markdown_style=False):
        self.widget._set_tool_tip_(raw, as_markdown_style)

    def set_check_clicked_connect_to(self, fnc):
        self.widget.check_clicked.connect(fnc)

    def set_press_clicked_connect_to(self, fnc):
        self.widget.clicked.connect(fnc)

    def set_press_clicked(self):
        self.widget.clicked.emit()

    def set_option_click_connect_to(self, fnc):
        self.widget.option_clicked.connect(fnc)

    def set_click(self):
        self.widget._set_action_press_click_emit_send_()

    def set_status(self, status):
        self.widget._set_status_(status)

    def set_statuses(self, element_statuses):
        self.widget._set_sub_process_statuses_(element_statuses)


class PrxFilterBar(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtFilterBar
    def __init__(self, *args, **kwargs):
        super(PrxFilterBar, self).__init__(*args, **kwargs)

    def get_enter_widget(self):
        return self.widget._get_qt_entry_()

    def set_filter_connect_to(self, proxy):
        proxy._set_filter_bar_(self)
        self.widget.entry_changed.connect(proxy._set_items_hidden_by_any_filter_)
        self.widget.preOccurrenceClicked.connect(proxy._set_scroll_to_pre_occurrence_match_item_)
        self.widget.nextOccurrenceClicked.connect(proxy._set_scroll_to_pst_occurrence_match_item_)

    def get_keyword(self):
        return self.get_enter_widget().text()

    def get_is_match_case(self):
        return self.widget._get_is_match_case_()

    def get_is_match_word(self):
        return self.widget._get_is_match_word_()

    def set_result_count(self, value):
        self.widget._set_result_count_(value)

    def set_result_index(self, value):
        self.widget._set_result_index_(value)

    def set_result_clear(self):
        self.widget._set_result_clear_()

    def set_entry_focus(self, boolean):
        self.widget._set_entry_focus_(boolean)


class PrxEntryItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit
    def __init__(self, *args, **kwargs):
        super(PrxEntryItem, self).__init__(*args, **kwargs)


class PrxToolWindow(
    utl_gui_prx_abstract.AbsPrxWindow,
    #
    utl_gui_prx_abstract.AbsWidgetContentDef,
    utl_gui_prx_abstract.AbsPrxProgressesDef,
    #
    utl_gui_prx_abstract.AbsPrxWaitingDef
):
    PRX_TYPE = 'tool_window'
    #
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMainWindow
    #
    CONTENT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtWidget
    PROGRESS_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtProgressBar
    WAITING_CHART_CLASS = _utl_gui_qt_wgt_chart._QtWaitingChart
    #
    HELP_FILE_PATH = None
    def __init__(self, *args, **kwargs):
        super(PrxToolWindow, self).__init__(*args, **kwargs)
        #
        if utl_core.System.get_is_windows():
            self.set_log_file_path(bsc_configure.LogDirectory.WINDOWS)
        elif utl_core.System.get_is_linux():
            self.set_log_file_path(bsc_configure.LogDirectory.LINUX)
        else:
            raise TypeError()
        #
        self._log_file_path = None
        #
        utl_gui_qt_core.set_qt_log_connect_create()
        #
        utl_gui_qt_core.set_qt_progress_connect_create()
        #
        utl_gui_qt_core.set_log_writer_connect()
        #
        self.set_show_menu_raw(
            [
                ('log', None, self.set_log_unit_show),
                ('help', None, self.set_help_unit_show)
            ]
        )

    def _set_build_(self):
        self._is_loading = False
        # menu bar
        self._qt_menu_bar_0 = _utl_gui_qt_wgt_utility.QtMenuBar()
        self._qt_widget.setMenuBar(self._qt_menu_bar_0)
        self._menu_0 = PrxMenu(self._qt_menu_bar_0)
        self._menu_0.set_name('show')
        self._qt_menu_bar_0.addMenu(self._menu_0.widget)
        #
        self._qt_central_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._qt_central_widget)
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_central_widget)
        # progress-bar
        qt_progress_bar = self.PROGRESS_WIDGET_CLASS()
        self._set_progresses_def_init_(qt_progress_bar)
        qt_layout_0.addWidget(qt_progress_bar)
        #
        self._set_widget_content_def_init_(qt_layout_0)
        #
        self._set_cnt_wdt_0_build_()
        self._set_cnt_wdt_1_build_()
        self._set_cnt_wdt_2_build_()
        self._set_cnt_wdt_3_build_()
        self._set_cnt_wdt_4_build_()
        #
        self._set_waiting_def_init_()
        #
        self.set_current_unit('main_0')

    def set_menu_add(self, name):
        menu = PrxMenu(self._qt_menu_bar_0)
        menu.set_name(name)
        self._qt_menu_bar_0.addMenu(menu.widget)
        return menu
    # main
    def _set_cnt_wdt_0_build_(self):
        # content_widget_0
        qt_widget_0 = self._set_cnt_wdt_create_('main_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        # central widget
        self._main_widget = _utl_gui_qt_wgt_utility.QtScrollArea()
        qt_layout_0.addWidget(self._main_widget)
        self._main_layout = self._main_widget._layout
        # bottom bar
        self._expanded_bar_1 = PrxHToolBar()
        qt_layout_0.addWidget(self._expanded_bar_1.widget)
        self._expanded_bar_1.set_expanded(True)
        self._expanded_bar_1.set_hide()
        self._expanded_bar_1.set_bottom_direction()
        #
        self._log_expand_bar = PrxHToolBar()
        qt_layout_0.addWidget(self._log_expand_bar.widget)
        self._log_expand_bar.set_bar_height(120)
        self._log_text_browser_0 = PrxTextBrowser()
        self._log_expand_bar.set_widget_add(self._log_text_browser_0)
        self._log_expand_bar.set_bottom_direction()
        #
        self._progress_maximum = 10
        self._progress_value = 0
    # option
    def _set_cnt_wdt_1_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self._set_cnt_wdt_create_('option_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        self._option_unit_0 = ContentWidget()
        self._option_unit_0.set_name('Option(s)')
        qt_layout_0.addWidget(self._option_unit_0.widget)
        self._option_unit_0.set_close_connect_to(fnc_)
        #
        self._option_unit_layout_0 = self._option_unit_0.central_layout
    # log
    def _set_cnt_wdt_2_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self._set_cnt_wdt_create_('log_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        content_widget_0 = ContentWidget()
        content_widget_0.set_name('log')
        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)
        #
        self._log_text_browser = PrxTextBrowser()
        content_widget_0.set_widget_add(self._log_text_browser.widget)
    # help
    def _set_cnt_wdt_3_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self._set_cnt_wdt_create_('help_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        content_widget_0 = ContentWidget()
        content_widget_0.set_name('help')
        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)
        #
        self._help_text_browser = PrxTextBrowser()
        content_widget_0.set_widget_add(self._help_text_browser.widget)
    # loading
    def _set_cnt_wdt_4_build_(self):
        def fnc_():
            self.set_current_unit('main_0')

        qt_widget_0 = self._set_cnt_wdt_create_('window_loading_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)

        content_widget_0 = ContentWidget()
        # content_widget_0.set_name('loading')

        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)

    def get_main_widget(self):
        return self._main_widget

    def get_central_widget(self):
        return self._qt_central_widget

    def set_widget_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._main_layout.addWidget(widget)
        else:
            self._main_layout.addWidget(widget.widget)

    def set_qt_widget_add(self, qt_widget):
        self._main_layout.addWidget(qt_widget)

    def set_button_add(self, widget):
        self._expanded_bar_1.set_widget_add(widget)
        self._expanded_bar_1.set_show()

    def set_show_menu_raw(self, menu_raw):
        if menu_raw:
            menu = self._menu_0
            menu.set_setup(menu_raw)

    def set_option_unit_name(self, text):
        self._option_unit_0.set_name(text)

    def set_option_unit_show(self):
        self.set_current_unit('option_0')

    def set_option_unit_hide(self):
        self.set_current_unit('main_0')

    def get_option_unit_layout(self):
        return self._option_unit_layout_0

    def set_option_unit_clear(self):
        layout = self._option_unit_layout_0
        c = layout.count()
        if c:
            for i in range(c):
                item = layout.itemAt(i)
                if item:
                    widget = item.widget()
                    widget.deleteLater()
    # loading
    def set_window_loading_show(self):
        utl_gui_qt_core.set_qt_window_show(
            self.widget, size=self.get_definition_window_size()
        )
        self._loading_show_timer.stop()

    def set_loading_start(self, time, method):
        self._is_loading = True
        self._loading_index = 0
        self.set_current_unit('window_loading_0')
        #
        self.set_waiting_start()
        #
        self._loading_timer_0 = utl_gui_qt_core.QtCore.QTimer(self.widget)
        self._loading_show_timer = utl_gui_qt_core.QtCore.QTimer(self.widget)
        #
        self._loading_timer_0.start(time)
        self._loading_timer_0.timeout.connect(method)
        #
        self._loading_show_timer.start(int(time*.8))
        self._loading_show_timer.timeout.connect(self.set_window_loading_show)

    def set_window_loading_end(self):
        self.set_waiting_stop()
        #
        self.set_current_unit('main_0')
        #
        self._loading_timer_0.stop()
        self._is_loading = False
    # log
    def set_log_unit_show(self):
        self.set_current_unit('log_0')
        #
        context = self._log_text_browser_0.get_content()
        self._log_text_browser.set_content(context)

    def get_log_bar(self):
        return self._log_expand_bar

    def get_log_text_browser(self):
        return self._log_text_browser_0

    def set_log_add(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.set_result_add(text)

    def set_log_file_path(self, file_path):
        if file_path is not None:
            f = utl_dcc_objects.OsFile(file_path)
            f.set_directory_create()
            self._log_file_path = file_path

    def set_log_write(self, text):
        if hasattr(self, '_log_file_path'):
            if self._log_file_path is not None:
                with open(self._log_file_path, mode='a+') as log:
                    log.write(
                        u'{}\n'.format(text).encode('utf-8')
                    )
                #
                log.close()
    # help
    def set_help_unit_show(self):
        self.set_current_unit('help_0')
        #
        if self.HELP_FILE_PATH is not None:
            self._help_text_browser.set_markdown_file_open(
                self.HELP_FILE_PATH
            )

    def set_help_content(self, content):
        if isinstance(content, (str, unicode)):
            self._help_text_browser.set_content(content)
        elif isinstance(content, (tuple, list)):
            self._help_text_browser.set_content(
                '\n'.join(content)
            )

    def set_help_file(self, file_path):
        self._help_text_browser.set_markdown_file_open(file_path)

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # show unique
        if exclusive is True:
            gui_proxies = utl_gui_prx_core.get_gui_proxy_by_class(self.__class__)
            for i in gui_proxies:
                if not i == self:
                    if hasattr(i, 'set_window_close'):
                        i.set_window_close()
        #
        if self._is_loading is True:
            utl_gui_qt_core.set_qt_window_show(
                self.widget, pos, size=(480, 160)
            )
        else:
            utl_gui_qt_core.set_qt_window_show(
                self.widget, pos, size=self.get_definition_window_size()
            )

    def set_print_add(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.set_print_add(text)

    def set_print_add_use_thread(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.set_print_add_use_thread(text)


class PrxSessionWindow(PrxToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PrxSessionWindow, self).__init__(*args, **kwargs)
        self._session = session
        self._session.set_configure_reload()
        self._session = session
        self._session.set_configure_reload()
        if self._session.get_rez_beta() is True:
            self.set_window_title('[BETA] {}'.format(self._session.gui_configure.get('name')))
        else:
            self.set_window_title(self._session.gui_configure.get('name'))
        #
        self.set_definition_window_size(self._session.gui_configure.get('size'))

        self.set_loading_start(
            time=1000,
            method=self._setup_fnc_
        )
    @property
    def session(self):
        return self._session

    def _setup_fnc_(self):
        self.set_all_setup()
        self.set_window_loading_end()

    def set_all_setup(self):
        raise NotImplementedError()


class PrxFramelessWindow(
    utl_gui_prx_abstract.AbsPrxWindow,
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_window._QtFramelessWindow
    def __init__(self, *args, **kwargs):
        super(PrxFramelessWindow, self).__init__(*args, **kwargs)
        self.widget.setWindowFlags(utl_gui_qt_core.QtCore.Qt.Window | utl_gui_qt_core.QtCore.Qt.FramelessWindowHint)


class PrxWindow(
    utl_gui_prx_abstract.AbsPrxWindow,
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_window._QtWindow
    def __init__(self, *args, **kwargs):
        super(PrxWindow, self).__init__(*args, **kwargs)

