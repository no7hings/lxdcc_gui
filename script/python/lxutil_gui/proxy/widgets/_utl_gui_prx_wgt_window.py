# coding:utf-8
from lxbasic import bsc_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.proxy import utl_gui_prx_abstract


class PrxDialogWindow(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMainWindow
    def __init__(self, *args, **kwargs):
        super(PrxDialogWindow, self).__init__(*args, **kwargs)
        self.widget.setWindowFlags(
            _utl_gui_qt_wgt_utility.QtCore.Qt.Window | _utl_gui_qt_wgt_utility.QtCore.Qt.WindowStaysOnTopHint
        )
        self.widget.setWindowModality(
            _utl_gui_qt_wgt_utility.QtCore.Qt.ApplicationModal
        )

    def _set_build_(self):
        qt_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(qt_widget_0)
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        #
        self._text_browser = _utl_gui_prx_wdt_utility.PrxTextBrowser()
        qt_layout_0.addWidget(self._text_browser.widget)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        #
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        #
        qt_spacer_0 = _utl_gui_qt_wgt_utility._QtSpacer()
        qt_layout_1.addWidget(qt_spacer_0)
        #
        self._yes_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._yes_button.widget)
        self._yes_button.set_name('Yes')
        self._yes_button.set_name_icon('Yes')
        self._yes_button.set_width(80)
        self._yes_button.set_press_clicked_connect_to(self.set_yes_run)
        #
        self._no_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._no_button.widget)
        self._no_button.set_name('No')
        self._no_button.set_name_icon('No')
        self._no_button.set_width(80)
        self._no_button.set_press_clicked_connect_to(self.set_no_run)
        #
        self._cancel_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._cancel_button.widget)
        self._cancel_button.set_name('Cancel')
        self._cancel_button.set_name_icon('Cancel')
        self._cancel_button.set_width(80)
        self._cancel_button.set_press_clicked_connect_to(self.set_cancel_run)
        #
        self._yes_methods = []
        self._no_methods = []
        self._cancel_methods = []
        #
        self._result = False

    def set_content(self, text):
        self._text_browser.set_content(text)

    def set_content_add(self, text):
        self._text_browser.set_add(text)

    def set_no_run(self):
        self._result = False
        for i in self._no_methods:
            i()
        self.set_window_close()

    def set_yes_run(self):
        self._result = True
        for i in self._yes_methods:
            i()
        self.set_window_close()

    def set_cancel_run(self):
        self._result = False
        for i in self._cancel_methods:
            i()
        self.set_window_close()

    def get_result(self):
        return self._result

    def set_yes_method_add(self, method, args=None):
        self._yes_methods.append(method)

    def set_cancel_method_add(self, method, args=None):
        self._cancel_methods.append(method)


class PrxDialogWindow1(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtDialog
    def __init__(self, *args, **kwargs):
        super(PrxDialogWindow1, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        #
        self._text_browser = _utl_gui_prx_wdt_utility.PrxTextBrowser()
        qt_layout_0.addWidget(self._text_browser.widget)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        #
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        #
        qt_spacer_0 = _utl_gui_qt_wgt_utility._QtSpacer()
        qt_layout_1.addWidget(qt_spacer_0)
        #
        self._yes_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._yes_button.widget)
        self._yes_button.set_name('Yes')
        self._yes_button.set_name_icon('Yes')
        self._yes_button.set_width(160)
        self._yes_button.set_press_clicked_connect_to(self.set_yes_run)
        #
        self._no_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._no_button.widget)
        self._no_button.set_name('No')
        self._no_button.set_name_icon('No')
        self._no_button.set_width(160)
        self._no_button.set_press_clicked_connect_to(self.set_no_run)
        #
        self._cancel_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._cancel_button.widget)
        self._cancel_button.set_name('Cancel')
        self._cancel_button.set_name_icon('Cancel')
        self._cancel_button.set_width(160)
        self._cancel_button.set_press_clicked_connect_to(self.set_cancel_run)
        #
        self._yes_methods = []
        self._no_methods = []
        self._cancel_methods = []
        #
        self._result = False

    def set_content(self, text):
        self._text_browser.set_content(text)

    def set_content_add(self, text):
        self._text_browser.set_add(text)

    def set_content_text_size(self, size):
        self._text_browser.set_text_size(size)

    def set_yes_run(self):
        self._result = True
        for i in self._yes_methods:
            i()
        #
        self.widget._set_yes_run_()
        # self.set_window_close()

    def set_no_run(self):
        self._result = False
        for i in self._no_methods:
            i()
        #
        self.widget._set_no_run_()
        # self.set_window_close()

    def set_cancel_run(self):
        self._result = None
        for i in self._cancel_methods:
            i()
        #
        self.widget._set_cancel_run_()
        # self.set_window_close()

    def get_result(self):
        return self._result

    def set_yes_method_add(self, method, args=None):
        self._yes_methods.append(method)

    def set_yes_label(self, text):
        self._yes_button.set_name(text)
        self._yes_button.set_name_icon(text)

    def set_no_method_add(self, method, args=None):
        self._no_methods.append(method)

    def set_no_label(self, text):
        self._no_button.set_name(text)
        self._no_button.set_name_icon(text)

    def set_cancel_method_add(self, method, args=None):
        self._cancel_methods.append(method)

    def set_cancel_label(self, text):
        self._cancel_button.set_name(text)
        self._cancel_button.set_name_icon(text)

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # show unique
        utl_gui_qt_core.set_qt_window_show(self.widget, pos, size, use_exec=True)

    def set_status(self, status):
        self._text_browser.set_status(status)


class PrxProcessWindow(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtMainWindow
    def __init__(self, *args, **kwargs):
        super(PrxProcessWindow, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(qt_widget_0)
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        #
        self._text_browser = _utl_gui_prx_wdt_utility.PrxTextBrowser()
        qt_layout_0.addWidget(self._text_browser.widget)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        #
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        #
        qt_spacer_0 = _utl_gui_qt_wgt_utility._QtSpacer()
        qt_layout_1.addWidget(qt_spacer_0)
        #
        self._stop_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._stop_button.widget)
        self._stop_button.set_name('Stop')
        self._stop_button.set_name_icon('Stop')
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
        self._text_browser.set_content(text)
        utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
            utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def set_content_add(self, text):
        self._text_browser.set_add(text)

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


class PrxWaitWindow(utl_gui_prx_abstract.AbsPrxWindow):
    STATUS_STARED = 'started'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    #
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtDialog
    def __init__(self, *args, **kwargs):
        super(PrxWaitWindow, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        #
        self._text_browser = _utl_gui_prx_wdt_utility.PrxTextBrowser()
        qt_layout_0.addWidget(self._text_browser.widget)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        #
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        #
        qt_spacer_0 = _utl_gui_qt_wgt_utility._QtSpacer()
        qt_layout_1.addWidget(qt_spacer_0)
        #
        self._wait_button = _utl_gui_prx_wdt_utility.PrxPressItem()
        qt_layout_1.addWidget(self._wait_button.widget)
        self._wait_button.set_name('Waiting ...')
        self._wait_button.set_name_icon('Waiting')
        self._wait_button.set_width(320)
        self._wait_button.set_press_clicked_connect_to(self._set_run_)
        #
        self._cost_second = 0
        self._cost_time = '00:00:00'
        self._wait_running_timer = utl_gui_qt_core.QtCore.QTimer(self.widget)
        self._status = None
        #
        self._wait_description = None
        self._next_description = None
        #
        self._completed_pre_method = None
        self._completed_post_method = None
        self._failed_pre_method = None
        self._failed_post_method = None

    def set_content(self, text):
        self._text_browser.set_content(text)
        utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
            utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def set_content_add(self, text):
        self._text_browser.set_add(text)

    def set_start(self):
        self._status = self.STATUS_STARED
        self.set_content_add(
            '"{wait}" is "{status}".'.format(
                **dict(
                    wait=self._wait_description,
                    status=self._status
                )
            )
        )
        self._wait_running_timer.timeout.connect(
            self._set_status_update_
        )
        self._wait_running_timer.start(1000)

        self.set_window_title('Wait for "{}"'.format(self._wait_description))

    def set_wait_description(self, text):
        self._wait_description = text

    def set_next_description(self, text):
        self._next_description = text

    def set_completed_update_method(self, method):
        self._completed_pre_method = method

    def set_completed_post_method(self, method):
        self._completed_post_method = method

    def _set_completed_post_run_(self):
        if self._completed_post_method is not None:
            self._completed_post_method()
        #
        self.set_window_close()

    def set_failed_update_method(self, method):
        self._failed_pre_method = method

    def set_failed_post_method(self, method):
        self._failed_post_method = method

    def _set_failed_post_run_(self):
        if self._failed_post_method is not None:
            self._failed_post_method()
        #
        self.set_window_close()

    def get_is_completed(self):
        if self._completed_pre_method is not None:
            return self._completed_pre_method()

    def get_is_failed(self):
        if self._failed_pre_method is not None:
            return self._failed_pre_method()

    def _set_run_(self):
        if self._status == self.STATUS_STARED:
            self.set_content_add(
                '"{}" is "{}", please wait.'.format(
                    self._wait_description,
                    self.STATUS_STARED
                )
            )
        if self._status == self.STATUS_COMPLETED:
            self._set_completed_post_run_()
        elif self._status == self.STATUS_FAILED:
            self._set_failed_post_run_()

    def _set_status_update_(self):
        is_completed = self.get_is_completed()
        is_failed = self.get_is_failed()
        if is_completed is not None:
            if is_completed is True:
                self._set_completed_status_()
            else:
                if is_failed is not None:
                    if is_failed is True:
                        self._set_failed_status_()
                    else:
                        self._cost_second += 1
                        self._cost_time = bsc_core.IntegerMtd.second_to_time_prettify(self._cost_second)
                        self._wait_button.set_name(
                            'Waiting [ {} ]'.format(bsc_core.IntegerMtd.second_to_time_prettify(self._cost_second))
                        )
        else:
            raise RuntimeError(
                'complete method is non-definition'
            )

    def _set_completed_status_(self):
        self._status = self.STATUS_COMPLETED
        self.set_content_add(
            '"{wait}" is "{status}", cost {time}, press "Next" to "{next}".'.format(
                **dict(
                    wait=self._wait_description,
                    next=self._next_description,
                    status=self._status,
                    time=self._cost_time
                )
            )
        )
        self._wait_button.set_name(
            'Next'
        )
        self._wait_button.set_name_icon('Next')
        self._wait_button.set_status(
            self._status
        )
        #
        self._wait_running_timer.stop()

    def _set_failed_status_(self):
        self._status = self.STATUS_FAILED
        self.set_content_add(
            '"{wait}" is "{status}", cost {time}, press "Close".'.format(
                **dict(
                    wait=self._wait_description,
                    status=self._status,
                    time=self._cost_time
                )
            )
        )
        self._wait_button.set_name(
            'Close'
        )
        self._wait_button.set_name_icon('Close')
        self._wait_button.set_status(
            self._status
        )
        #
        self._wait_running_timer.stop()
