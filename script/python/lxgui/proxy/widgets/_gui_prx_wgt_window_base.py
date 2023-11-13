# coding:utf-8
import six

import lxlog.core as log_core

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

from lxgui.qt.widgets import _gui_qt_wgt_utility, _gui_qt_wgt_chart, _gui_qt_wgt_layer_stack

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.core as gui_prx_core

from lxgui.proxy.widgets import _gui_prx_wdt_utility, _gui_prx_wgt_contianer


class PrxBaseWindow(
    gui_prx_abstracts.AbsPrxWindow,
    #
    gui_prx_abstracts.AbsPrxLayerBaseDef,
    #
    gui_prx_abstracts.AbsPrxProgressingDef,
    gui_prx_abstracts.AbsPrxWaitingDef,
):
    PRX_CATEGORY = 'tool_window'
    PRX_TYPE = 'tool_window'

    QT_WIDGET_CLS = _gui_qt_wgt_utility.QtMainWindow

    PRX_LAYER_CLS = _gui_prx_wdt_utility.PrxLayer
    QT_LAYER_STACK_CLS = _gui_qt_wgt_layer_stack.QtLayerStack
    PROGRESS_WIDGET_CLS = _gui_qt_wgt_utility.QtProgressBar

    QT_WAITING_CHART_CLS = _gui_qt_wgt_chart.QtChartAsWaiting
    QT_PROGRESSING_CHART_CLS = _gui_qt_wgt_chart.QtChartAsProgressing

    HELP_FILE_PATH = None

    def __init__(self, *args, **kwargs):
        super(PrxBaseWindow, self).__init__(*args, **kwargs)
        #
        self.set_log_file_path(bsc_core.StgUserMtd.get_user_log_directory())
        #
        self._log_file_path = None
        #
        gui_prx_core.GuiProxyLogBridge.generate_all()

        self._qt_widget._create_window_shortcut_action_for_(
            self.show_help, 'F1'
        )
        #
        self.set_show_menu_raw(
            [
                ('log', 'log', self.set_log_unit_show),
                ('help', 'help', self.show_help)
            ]
        )

    def _gui_build_(self):
        self._is_loading = False
        # menu bar
        self._qt_menu_bar_0 = _gui_qt_wgt_utility.QtMenuBar()
        self._qt_widget.setMenuBar(self._qt_menu_bar_0)
        self._menu_0 = _gui_prx_wdt_utility.PrxMenu(self._qt_menu_bar_0)
        self._menu_0.set_name('show')
        self._qt_menu_bar_0.addMenu(self._menu_0.widget)
        #
        self._qt_central_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        self._qt_widget.setCentralWidget(self._qt_central_widget)
        #
        self._set_progressing_def_init_()
        #
        self._qt_central_layout = _gui_qt_wgt_utility.QtVBoxLayout(self._qt_central_widget)
        self._qt_central_layout.setContentsMargins(0, 0, 0, 0)
        #
        self._init_layer_base_def_(self._qt_central_layout)
        #
        self.__build_main_layer()
        self.__build_option_layer()
        self.__build_log_layer()
        self.__build_help_layer()
        self.__build_loading_layer()
        self.__build_expression_layer()
        self.__build_message_layer()
        #
        self._set_waiting_def_init_()
        #
        self.set_current_layer('main_0')

    def switch_to_main_layer(self):
        self.switch_current_layer_to('main_0')

    def create_menu(self, name):
        menu = _gui_prx_wdt_utility.PrxMenu(self._qt_menu_bar_0)
        menu.set_name(name)
        self._qt_menu_bar_0.addMenu(menu.widget)
        return menu

    def set_main_style_mode(self, mode):
        if mode == 0:
            self._qt_main_line.show()
            self._qt_main_layout.setContentsMargins(2, 2, 2, 2)
        elif mode == 1:
            self._qt_main_line.hide()
            self._qt_main_layout.setContentsMargins(0, 0, 0, 0)

    def create_layer_widget(self, key, label=None):
        def fnc_():
            self.switch_current_layer_to('main_0')

        layer = self.create_layer(key)
        layer_widget = layer.create_widget(key, label=label)
        layer_widget.connect_close_to(fnc_)
        return layer_widget

    # main
    def __build_main_layer(self):
        # content_widget_0
        layer = self.create_layer('main_0')
        qt_layout_0 = _gui_qt_wgt_utility.QtVBoxLayout(layer._qt_widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(0)
        self._qt_main_line = _gui_qt_wgt_utility.QtHLine()
        qt_layout_0.addWidget(self._qt_main_line)
        # main widget
        self._qt_main_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        qt_layout_0.addWidget(self._qt_main_widget)
        self._qt_main_layout = _gui_qt_wgt_utility.QtVBoxLayout(self._qt_main_widget)
        self._qt_main_layout.setContentsMargins(2, 2, 2, 2)
        # bottom toolbar
        self._window_bottom_tool_bar = _gui_prx_wgt_contianer.PrxHToolBar()
        qt_layout_0.addWidget(self._window_bottom_tool_bar.widget)
        self._window_bottom_tool_bar.set_expanded(True)
        self._window_bottom_tool_bar.set_hide()
        self._window_bottom_tool_bar.set_bottom_direction()
        #
        self._log_tool_bar = _gui_prx_wgt_contianer.PrxHToolBar()
        qt_layout_0.addWidget(self._log_tool_bar.widget)
        self._log_tool_bar.set_hide()
        self._log_tool_bar.set_height(120)
        self._log_text_browser_0 = _gui_prx_wdt_utility.PrxTextBrowser()
        self._log_tool_bar.add_widget(self._log_text_browser_0)
        self._log_tool_bar.set_bottom_direction()
        #
        self._progress_maximum = 10
        self._progress_value = 0

    # option
    def __build_option_layer(self):
        self.create_layer_widget('window_option_0', 'Option')

    # log
    def __build_log_layer(self):
        layer_widget = self.create_layer_widget('window_log_0', 'Log')
        self._log_text_browser = _gui_prx_wdt_utility.PrxTextBrowser()
        layer_widget.add_widget(self._log_text_browser)

    # help
    def __build_help_layer(self):
        layer_widget = self.create_layer_widget('window_help_0', 'Help')
        self._help_text_browser = _gui_prx_wdt_utility.PrxTextBrowser()
        layer_widget.add_widget(self._help_text_browser)

    # loading
    def __build_loading_layer(self):
        self.create_layer_widget('window_loading_0', 'Loading ...')

    # exception
    def __build_expression_layer(self):
        layer_widget = self.create_layer_widget('window_exception_0', 'Exception')
        self._exception_text_browser = _gui_prx_wdt_utility.PrxTextBrowser()
        self._exception_text_browser.set_font_size(10)
        layer_widget.add_widget(self._exception_text_browser.widget)

    # message
    def __build_message_layer(self):
        layer_widget = self.create_layer_widget('window_message_0', 'Message')
        self._message_text_browser = _gui_prx_wdt_utility.PrxTextBrowser()
        self._message_text_browser.set_font_size(12)
        layer_widget.add_widget(self._message_text_browser.widget)

    def get_main_widget(self):
        return self._qt_main_widget

    def get_central_widget(self):
        return self._qt_central_widget

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_main_layout.addWidget(widget)
        else:
            self._qt_main_layout.addWidget(widget.widget)

    def set_qt_widget_add(self, qt_widget):
        self._qt_main_layout.addWidget(qt_widget)

    def add_button(self, widget):
        self._window_bottom_tool_bar.add_widget(widget)
        self._window_bottom_tool_bar.set_show()

    def set_show_menu_raw(self, menu_raw):
        if menu_raw:
            menu = self._menu_0
            menu.set_setup(menu_raw)

    def set_option_unit_name(self, text):
        self.get_layer_widget('window_option_0').set_name(text)

    def set_option_unit_status(self, status):
        self.get_layer_widget('window_option_0').set_status(status)

    def show_option_unit(self):
        self.switch_current_layer_to('window_option_0')

    def get_option_layer_widget(self):
        return self.get_layer_widget('window_option_0')

    def set_option_unit_clear(self):
        self.get_layer_widget('window_option_0').clear()

    # loading
    def set_window_loading_show(self):
        gui_qt_core.GuiQtUtil.show_qt_window(
            self.widget,
            size=self.get_definition_window_size()
        )

    def start_loading(self, delay_time, method):
        def method_fnc_():
            self.set_window_loading_end()
            method()

        #
        self._is_loading = True
        self._loading_index = 0
        self.set_current_layer('window_loading_0')
        #
        self.start_waiting(auto_stop_time=delay_time)
        #
        self._loading_timer_start = gui_qt_core.QtCore.QTimer(self.widget)
        self._loading_timer_start.singleShot(delay_time, method_fnc_)

        self._loading_show_timer = gui_qt_core.QtCore.QTimer(self.widget)
        self._loading_show_timer.singleShot(int(delay_time*.8), self.set_window_loading_show)

    def set_window_loading_end(self):
        gui_qt_core.GuiQtUtil.show_qt_window(
            self.widget, size=self.get_definition_window_size()
        )
        #
        self.set_current_layer('main_0')
        #
        self._is_loading = False

    # log
    def set_log_unit_show(self):
        self.switch_current_layer_to('window_log_0')
        #
        context = self._log_text_browser_0.get_content()
        self._log_text_browser.set_content(context)

    def get_log_bar(self):
        return self._log_tool_bar

    def get_log_text_browser(self):
        return self._log_text_browser_0

    def set_log_add(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.add_result(text)

    def set_log_file_path(self, file_path):
        if file_path is not None:
            bsc_core.StgFileOpt(file_path).create_directory()
            self._log_file_path = file_path

    def qt_log_write_fnc(self, text):
        if hasattr(self, '_log_file_path'):
            if self._log_file_path is not None:
                with open(self._log_file_path, mode='a+') as log:
                    log.write(
                        u'{}\n'.format(text).encode('utf-8')
                    )
                #
                log.close()

    # help
    def show_help(self):
        self.switch_current_layer_to('window_help_0')
        #
        if self.HELP_FILE_PATH is not None:
            self._help_text_browser.set_markdown_file_open(
                self.HELP_FILE_PATH
            )

    def set_help_content(self, text):
        if isinstance(text, six.string_types):
            self._help_text_browser.set_content(text)
        elif isinstance(text, (tuple, list)):
            self._help_text_browser.set_content(
                '\n'.join(text)
            )

    def set_help_file(self, file_path):
        self._help_text_browser.set_markdown_file_open(file_path)

    # exception
    def show_exception(self):
        self.switch_current_layer_to('window_exception_0')

    def set_exception_content(self, text):
        if isinstance(text, six.string_types):
            self._exception_text_browser.set_content(text)
        elif isinstance(text, (tuple, list)):
            self._exception_text_browser.set_content(
                '\n'.join(text)
            )

    def show_message(self, text=None, status=None):
        self.switch_current_layer_to('window_message_0')
        if text:
            # unit.set_status(status)
            self._message_text_browser.set_content(
                text
            )

    def set_exception_content_add(self, text):
        if isinstance(text, six.string_types):
            self._exception_text_browser.append(text)
        elif isinstance(text, (tuple, list)):
            self._exception_text_browser.append(
                '\n'.join(text)
            )

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # show unique
        if exclusive is True:
            gui_proxies = gui_prx_core.GuiProxyUtil.find_widget_proxy_by_class(self.__class__)
            for i in gui_proxies:
                if hasattr(i, '_window_unicode_id'):
                    if i._window_unicode_id != self._window_unicode_id:
                        log_core.Log.trace_method_warning(
                            'close exists window for "{}"'.format(
                                self.__class__.__name__
                            )
                        )
                        i.set_window_close()
        #
        if self._is_loading is True:
            gui_qt_core.GuiQtUtil.show_qt_window(
                self.widget, pos, size=(480, 240)
            )
        else:
            gui_qt_core.GuiQtUtil.show_qt_window(
                self.widget, pos, size=self.get_definition_window_size()
            )

    def trace_log(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.trace_log(text)

    def trace_log_use_thread(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.trace_log_use_thread(text)

    def gui_bustling(self):
        return self._qt_widget._gui_bustling_()

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_widget._run_build_use_thread_(
            cache_fnc, build_fnc, post_fnc
        )


class PrxSessionWindow(PrxBaseWindow):
    PRX_TYPE = 'session_window'
    LOADING_DELAY_TIME = 1000

    def __init__(self, session, *args, **kwargs):
        super(PrxSessionWindow, self).__init__(*args, **kwargs)
        self._debug_run_(self._main_fnc_, session)

    @property
    def session(self):
        return self._session

    def _debug_run_(self, fnc, *args, **kwargs):
        # noinspection PyBroadException
        try:
            fnc(*args, **kwargs)
        except Exception as e:
            import sys

            import traceback

            exc_texts = []
            exc_type, exc_value, exc_stack = sys.exc_info()
            if exc_type:
                value = '{}: "{}"'.format(exc_type.__name__, repr(exc_value))
                for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
                    i_file_path, i_line, i_fnc, i_fnc_line = stk
                    exc_texts.append(
                        '{indent}file "{file}" line {line} in {fnc}\n{indent}{indent}{fnc_line}'.format(
                            **dict(
                                indent='    ',
                                file=i_file_path,
                                line=i_line,
                                fnc=i_fnc,
                                fnc_line=i_fnc_line
                            )
                        )
                    )
                #
                self.show_exception()
                self.set_exception_content_add('traceback:')
                [self.set_exception_content_add(i) for i in exc_texts]
                self.set_exception_content_add(value)

    def _main_fnc_(self, *args, **kwargs):
        self._session = args[0]
        self._session.reload_configure()
        if self._session.get_is_td_enable() is True:
            self.set_window_title(
                '[ALPHA] {} - {}'.format(
                    self._session.gui_configure.get('name'), str(self._session.application).capitalize()
                )
            )
        elif self._session.get_is_beta_enable() is True:
            self.set_window_title(
                '[BETA] {} - {}'.format(
                    self._session.gui_configure.get('name'), str(self._session.application).capitalize()
                )
            )
        else:
            self.set_window_title(
                '{} - {}'.format(
                    self._session.gui_configure.get('name'), str(self._session.application).capitalize()
                )
            )

        if self._session.gui_configure.get('icon_name'):
            self.set_window_icon_by_name(self._session.gui_configure.get('icon_name'))
        #
        self.set_definition_window_size(self._session.gui_configure.get('size'))
        self._qt_thread_enable = bsc_core.EnvironMtd.get_qt_thread_enable()
        #
        self.start_loading(
            delay_time=self.LOADING_DELAY_TIME, method=self._setup_fnc_
        )

    def _setup_fnc_(self):
        self.restore_variants()
        self.set_all_setup()

    def _set_collapse_update_(self, collapse_dict):
        for i_k, i_v in collapse_dict.items():
            i_c = self._session.configure.get(
                'build.node_collapse.{}'.format(i_k)
            ) or []
            i_v.set_ports_collapse(i_c)

    def restore_variants(self):
        pass

    def set_all_setup(self):
        raise NotImplementedError()


class PrxSessionToolWindow(PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PrxSessionToolWindow, self).__init__(session, *args, **kwargs)

    def _setup_fnc_(self):
        self.restore_variants()
        #
        self._setup_ssn_tool_()
        self.set_all_setup()

    def apply_fnc(self):
        raise NotImplementedError()

    def apply_and_close_fnc(self):
        self.apply_fnc()
        self.close_window_later()

    def close_fnc(self):
        self.close_window_later()

    def _setup_ssn_tool_(self):
        self._ssn_tool_apply_and_close_button = _gui_prx_wdt_utility.PrxPressItem()
        self.add_button(self._ssn_tool_apply_and_close_button)
        self._ssn_tool_apply_and_close_button.set_name('Apply and Close')
        self._ssn_tool_apply_and_close_button.connect_press_clicked_to(
            self.apply_and_close_fnc
        )

        self._ssn_tool_apply_button = _gui_prx_wdt_utility.PrxPressItem()
        self.add_button(self._ssn_tool_apply_button)
        self._ssn_tool_apply_button.set_name('Apply')
        self._ssn_tool_apply_button.connect_press_clicked_to(
            self.apply_fnc
        )

        self._ssn_tool_close_button = _gui_prx_wdt_utility.PrxPressItem()
        self.add_button(self._ssn_tool_close_button)
        self._ssn_tool_close_button.set_name('Close')
        self._ssn_tool_close_button.connect_press_clicked_to(
            self.close_fnc
        )
        self._log_tool_bar.set_visible(False)

    def set_all_setup(self):
        raise NotImplementedError()
