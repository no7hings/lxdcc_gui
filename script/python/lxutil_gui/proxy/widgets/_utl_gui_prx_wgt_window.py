# coding:utf-8
import functools

from lxbasic import bsc_configure, bsc_core

from lxutil import utl_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_chart

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wdt_node

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.proxy import utl_gui_prx_abstract


class AbsPrxDialogWindow(
    utl_gui_prx_abstract.AbsPrxWindow,
    utl_gui_prx_abstract.AbsPrxWaitingDef,
    utl_gui_prx_abstract.AbsPrxProgressesDef,
):
    QT_WIDGET_CLASS = None
    BUTTON_WIDTH = 120
    WAITING_CHART_CLASS = _utl_gui_qt_wgt_chart._QtWaitingChart
    PROGRESS_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtProgressBar
    #
    ValidatorStatus = bsc_configure.ValidatorStatus
    def __init__(self, *args, **kwargs):
        super(AbsPrxDialogWindow, self).__init__(*args, **kwargs)
        if kwargs.get('parent'):
            self.widget.setWindowFlags(
                _utl_gui_qt_wgt_utility.QtCore.Qt.Tool | _utl_gui_qt_wgt_utility.QtCore.Qt.WindowStaysOnTopHint
            )
        else:
            self.widget.setWindowFlags(
                _utl_gui_qt_wgt_utility.QtCore.Qt.Window | _utl_gui_qt_wgt_utility.QtCore.Qt.WindowStaysOnTopHint
            )
        #
        self.widget.setWindowModality(
            _utl_gui_qt_wgt_utility.QtCore.Qt.WindowModal
        )
        self._use_thread = True
        self._notify_when_yes_completed = False

        self._completed_content = 'process is completed, press "Close" to continue'

    def set_yes_completed_notify_enable(self, boolean):
        self._notify_when_yes_completed = boolean

    def _set_central_layout_create_(self):
        self._central_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._central_widget)
        self._central_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._central_widget)

    def _set_build_(self):
        self._set_central_layout_create_()
        #
        self._set_waiting_def_init_()
        #
        self._sub_label_item = _utl_gui_qt_wgt_item._QtTextItem()
        self._central_layout.addWidget(self._sub_label_item)
        self._sub_label_item.setVisible(False)
        self._sub_label_item.setMaximumHeight(20)
        self._sub_label_item.setMinimumHeight(20)
        self._sub_label_item._set_name_text_option_(
            utl_gui_qt_core.QtCore.Qt.AlignHCenter | utl_gui_qt_core.QtCore.Qt.AlignVCenter
        )
        #
        qt_progress_bar = self.PROGRESS_WIDGET_CLASS()
        self._set_progresses_def_init_(qt_progress_bar)
        self._central_layout.addWidget(qt_progress_bar)
        #
        self._customize_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._central_layout.addWidget(self._customize_widget)
        self._customize_widget.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        self._customize_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._customize_widget)
        self._customize_layout.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignTop)
        # option
        self._options_prx_node = _utl_gui_prx_wdt_node.PrxNode_('options')
        self._customize_layout.addWidget(self._options_prx_node.widget)
        self._options_prx_node.set_hide()
        # tip
        self._tip_group = _utl_gui_prx_wdt_utility.PrxExpandedGroup()
        self._tip_group.set_visible(False)
        self._tip_group.set_name('tips')
        self._customize_layout.addWidget(self._tip_group.widget)
        self._tip_text_browser = _utl_gui_prx_wdt_utility.PrxTextBrowser()
        self._tip_group.set_widget_add(self._tip_text_browser)
        #
        self._button_tool_bar = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._button_tool_bar.set_expanded(True)
        self._central_layout.addWidget(self._button_tool_bar.widget)
        qt_widget_2 = _utl_gui_qt_wgt_utility.QtWidget()
        self._button_tool_bar.set_widget_add(qt_widget_2)
        self._button_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_2)
        #
        qt_spacer_0 = _utl_gui_qt_wgt_utility._QtSpacer()
        self._button_layout.addWidget(qt_spacer_0)
        #
        self._yes_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        # self._yes_button.set_visible(False)
        self._button_layout.addWidget(self._yes_button.widget)
        self._yes_button.set_name('Yes')
        self._yes_button.set_icon_by_name_text('Yes')
        self._yes_button.set_width(self.BUTTON_WIDTH)
        self._yes_button.set_press_clicked_connect_to(self.set_yes_run)
        #
        self._no_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        # self._no_button.set_visible(False)
        self._button_layout.addWidget(self._no_button.widget)
        self._no_button.set_name('No')
        self._no_button.set_icon_by_name_text('No')
        self._no_button.set_width(self.BUTTON_WIDTH)
        self._no_button.set_press_clicked_connect_to(self.set_no_run)
        #
        self._cancel_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        # self._cancel_button.set_visible(False)
        self._button_layout.addWidget(self._cancel_button.widget)
        self._cancel_button.set_name('Cancel')
        self._cancel_button.set_icon_by_name_text('Cancel')
        self._cancel_button.set_width(self.BUTTON_WIDTH)
        self._cancel_button.set_press_clicked_connect_to(self.set_cancel_run)
        #
        # self._close_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        # self._close_button.set_visible(False)
        # self._button_layout.addWidget(self._close_button.widget)
        # self._close_button.set_name('Close')
        # self._close_button.set_icon_by_name_text('close')
        # self._close_button.set_width(self.BUTTON_WIDTH)
        #
        self._yes_methods = []
        self._no_methods = []
        self._cancel_methods = []
        #
        self._result = False
        self._kwargs = {}

    def set_sub_label(self, text):
        self._sub_label_item.setVisible(True)
        self._sub_label_item._set_name_text_(text)

    def set_completed_content(self, text):
        self._completed_content = text

    def _set_completed_(self, scheme):
        if scheme == 'yes':
            if self._notify_when_yes_completed is True:
                self._options_prx_node.set_visible(False)
                self.set_yes_visible(False)
                self.set_cancel_visible(False)
                self.set_content(self._completed_content)
                self.set_status(self.ValidatorStatus.Correct)
                return
        self.set_window_close_later()

    def _set_failed_(self, log):
        self._options_prx_node.set_visible(False)
        self.set_yes_visible(False)
        self.set_cancel_visible(False)
        self.set_content(log)
        self.set_status(self.ValidatorStatus.Error)

    def _set_method_run_(self, methods, scheme):
        def completed_fnc_():
            self._set_completed_(scheme)

        def failed_fnc_(log):
            self._set_failed_(log)

        if self._use_thread is True:
            t = self.widget._set_thread_create_()
            t.run_started.connect(self.set_waiting_start)
            t.run_finished.connect(self.set_waiting_stop)
            t.completed.connect(completed_fnc_)
            t.failed.connect(failed_fnc_)
            for i in methods:
                t.set_method_add(i)
            #
            t.start()
        else:
            self.set_waiting_start()
            #
            for i in methods:
                i()
            #
            self.set_waiting_stop()
            self.set_window_close_later()

    def set_use_thread(self, boolean):
        self._use_thread = boolean

    def set_no_run(self):
        self._result = False
        self._kwargs = self.get_options_as_kwargs()
        self._set_method_run_(self._no_methods, scheme='no')

    def set_yes_run(self):
        self._result = True
        self._kwargs = self.get_options_as_kwargs()
        self._set_method_run_(self._yes_methods, scheme='yes')

    def set_cancel_run(self):
        self._result = False
        self._kwargs = self.get_options_as_kwargs()
        self._set_method_run_(self._cancel_methods, scheme='cancel')

    def get_result(self):
        return self._result

    def get_kwargs(self):
        return self._kwargs

    def set_yes_visible(self, boolean):
        self._yes_button.set_visible(boolean)

    def set_yes_label(self, text):
        self._yes_button.set_name(text)
        self._yes_button.set_icon_by_name_text(text)

    def set_yes_method_add(self, method, args=None):
        self._yes_methods.append(method)

    def set_no_visible(self, boolean):
        self._no_button.set_visible(boolean)

    def set_no_label(self, text):
        self._no_button.set_name(text)
        self._no_button.set_icon_by_name_text(text)

    def set_no_method_add(self, method, args=None):
        self._no_methods.append(method)

    def set_cancel_visible(self, boolean):
        self._cancel_button.set_visible(boolean)

    def set_cancel_label(self, text):
        self._cancel_button.set_name(text)
        self._cancel_button.set_icon_by_name_text(text)

    def set_cancel_method_add(self, method, args=None):
        self._cancel_methods.append(method)

    def set_status(self, status):
        self._central_widget._set_status_(status)

    def set_customize_widget_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self._customize_layout.addWidget(qt_widget)

    def set_content(self, text):
        self.set_print_over_use_thread(text)

    def set_content_add(self, text):
        self.set_print_add_use_thread(text)

    def set_content_font_size(self, size):
        self._tip_text_browser.set_font_size(size)

    def set_tip_group_enable(self):
        self._tip_group.set_visible(True)
        self._tip_group.set_expanded(True)

    def set_tip_visible(self, boolean):
        self._tip_group.set_visible(boolean)

    def set_options_group_enable(self):
        self._options_prx_node.set_visible(True)
        self._options_prx_node.set_expanded(True)

    def get_options_as_kwargs(self):
        return self._options_prx_node.get_as_kwargs()

    def get_options_node(self):
        return self._options_prx_node

    def set_options_create_by_configure(self, configure):
        self._options_prx_node.set_ports_create_by_configure(configure)

    def set_print_add_use_thread(self, text):
        self._tip_text_browser.set_print_add_use_thread(text)

    def set_print_over_use_thread(self, text):
        self._tip_text_browser.set_print_over_use_thread(text)

    def set_failed(self):
        pass

    def set_completed(self):
        pass


class PrxDialogWindow0(AbsPrxDialogWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMainWindow
    def __init__(self, *args, **kwargs):
        super(PrxDialogWindow0, self).__init__(*args, **kwargs)
        self._tip_group.set_visible(True)
        self._tip_group.set_expanded(True)
        self.set_content_font_size(10)

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # do not show unique
        utl_gui_qt_core.set_qt_window_show(
            self.widget,
            pos,
            size
        )


class PrxDialogWindow1(AbsPrxDialogWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtDialog
    def __init__(self, *args, **kwargs):
        super(PrxDialogWindow1, self).__init__(*args, **kwargs)
        self._tip_group.set_visible(True)
        self._tip_group.set_expanded(True)
        self.set_content_font_size(10)

    def _set_central_layout_create_(self):
        layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self._central_widget = _utl_gui_qt_wgt_utility.QtWidget()
        layout.addWidget(self._central_widget)
        self._central_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._central_widget)

    def set_yes_run(self):
        self._result = True
        self._kwargs = self.get_options_as_kwargs()
        for i in self._yes_methods:
            i()
        #
        self.widget._set_yes_run_()
        # self.set_window_close()

    def set_no_run(self):
        self._result = False
        self._kwargs = self.get_options_as_kwargs()
        for i in self._no_methods:
            i()
        #
        self.widget._set_no_run_()
        # self.set_window_close()

    def set_cancel_run(self):
        self._result = None
        self._kwargs = self.get_options_as_kwargs()
        for i in self._cancel_methods:
            i()
        #
        self.widget._set_cancel_run_()
        # self.set_window_close()

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # do not show unique
        utl_gui_qt_core.set_qt_window_show(
            self.widget,
            pos,
            size,
            use_exec=True
        )


class PrxTipWindow(PrxDialogWindow0):
    def __init__(self, *args, **kwargs):
        super(PrxTipWindow, self).__init__(*args, **kwargs)
        self._tip_group.set_visible(True)
        self._tip_group.set_expanded(True)
        self.set_content_font_size(10)

    def set_no_run(self):
        self._result = False
        for i in self._no_methods:
            i()
        self.set_window_close_later()

    def set_yes_run(self):
        self._result = True
        for i in self._yes_methods:
            i()
        self.set_window_close_later()

    def set_cancel_run(self):
        self._result = False
        for i in self._cancel_methods:
            i()
        self.set_window_close_later()


class PrxProcessWindow(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMainWindow
    def __init__(self, *args, **kwargs):
        super(PrxProcessWindow, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(qt_widget_0)
        self._central_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        #
        self._tip_text_browser = _utl_gui_prx_wdt_utility.PrxTextBrowser()
        self._central_layout.addWidget(self._tip_text_browser.widget)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        self._central_layout.addWidget(qt_widget_1)
        #
        self._button_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        #
        qt_spacer_0 = _utl_gui_qt_wgt_utility._QtSpacer()
        self._button_layout.addWidget(qt_spacer_0)
        #
        self._stop_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        self._button_layout.addWidget(self._stop_button.widget)
        self._stop_button.set_name('Stop')
        self._stop_button.set_icon_by_name_text('Stop')
        self._stop_button.set_width(80)
        self._stop_button.set_press_clicked_connect_to(self.set_process_stop)
        #
        self._process = utl_gui_qt_core.QtCore.QProcess(self.widget)
        self._process_name = None
        self._process_cmd = None
        #
        self._process_running_index = 0
        #
        self._process_running_timer = utl_gui_qt_core.QtCore.QTimer(self.widget)
        #
        self.widget.close_clicked.connect(self.set_process_stop)

    def set_content(self, text):
        self._tip_text_browser.set_content(text)
        utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
            utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def set_content_add(self, text):
        self._tip_text_browser.set_add(text)

    def set_process_start(self):
        if self._process_cmd is not None:
            self._process.start(self._process_cmd)
            #
            self._process.readyReadStandardOutput.connect(
                self._set_process_output_result_update_
            )
            self._process.stateChanged.connect(
                self._set_process_state_update_
            )
            self._process.finished.connect(
                self._set_process_exists_update_
            )
            self._process.errorOccurred.connect(
                self._set_process_error_update_
            )
            self._process_running_timer.timeout.connect(
                self._set_process_running_update_
            )
            self._process_running_timer.start(1000)

    def _set_process_running_update_(self):
        if self._process.state() == self._process.Running:
            self._process_running_index += 1
            self.set_window_title(
                '{} [ {} ]'.format(self._process_name, 'running {}'.format('.' * (self._process_running_index % 5)))
            )
            utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
                utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
            )

    def _set_process_output_result_update_(self):
        self.set_content_add(
            str(
                self._process.readAllStandardOutput().data().decode('utf-8')
            ).rstrip()
        )
        utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
            utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_process_state_update_(self, process_state):
        _ = {
            self._process.NotRunning: 'stopped',
            self._process.Starting: 'starting',
            self._process.Running: 'running'
        }
        self.set_window_title(
            '{} [ {} ]'.format(self._process_name, _[process_state])
        )
        #
        utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
            utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_process_exists_update_(self, process_exist_status):
        if process_exist_status == self._process.NormalExit:
            self.set_window_title(
                '{} [ {} ]'.format(self._process_name, 'completed')
            )
        elif process_exist_status == self._process.CrashExit:
            self.set_window_title(
                '{} [ {} ]'.format(self._process_name, 'failed')
            )
        #
        self._process_running_timer.stop()

    def _set_process_error_update_(self, process_error):
        self.set_window_title(
            '{} [ {} ]'.format(self._process_name, str(process_error))
        )
        utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
            utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def set_process_stop(self):
        self._process.kill()
        self._process_running_timer.stop()

    def set_process_name(self, name):
        self._process_name = name

    def set_process_cmd(self, cmd):
        self._process_cmd = cmd
        self.set_close_method(
            self.set_process_stop
        )


class PrxMonitorWindow(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMainWindow
    ValidatorStatus = bsc_configure.ValidatorStatus
    def __init__(self, *args, **kwargs):
        super(PrxMonitorWindow, self).__init__(*args, **kwargs)
        if kwargs.get('parent'):
            self.widget.setWindowFlags(
                _utl_gui_qt_wgt_utility.QtCore.Qt.Tool | _utl_gui_qt_wgt_utility.QtCore.Qt.WindowStaysOnTopHint
            )
        else:
            self.widget.setWindowFlags(
                _utl_gui_qt_wgt_utility.QtCore.Qt.Window | _utl_gui_qt_wgt_utility.QtCore.Qt.WindowStaysOnTopHint
            )
        self.widget.setWindowModality(
            _utl_gui_qt_wgt_utility.QtCore.Qt.WindowModal
        )

    def _set_build_(self):
        self._central_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._central_widget)
        self._central_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._central_widget)
        #
        self._tip_text_browser = _utl_gui_prx_wdt_utility.PrxTextBrowser()
        self._central_layout.addWidget(self._tip_text_browser.widget)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        self._central_layout.addWidget(qt_widget_1)
        #
        self._button_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        #
        self._status_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        self._button_layout.addWidget(self._status_button.widget)
        self._status_button.set_name('process')
        self._status_button.set_icon_by_name_text('process')

    def set_status(self, status):
        self._central_widget._set_status_(status)

    def get_status_button(self):
        return self._status_button

    def set_logging(self, *args):
        self._tip_text_browser.set_print_add_use_thread(*args)

    def set_status_at(self, *args):
        self._status_button.set_status_at(*args)

    def set_finished_at(self, *args):
        self._status_button.set_finished_at(*args)
