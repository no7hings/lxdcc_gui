# coding:utf-8
import lxlog.core as log_core

import lxlog.bridge as log_bridge

import lxgui.configure as gui_configure

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core


class GuiProxyUtil(object):

    @staticmethod
    def show_window_proxy_auto(window_proxy_cls, show_kwargs=None, process_fnc=None, **kwargs):
        exists_app = gui_qt_core.GuiQtUtil.get_exists_app()
        if exists_app is None:
            app = gui_qt_core.GuiQtUtil.create_app()

            gui_qt_core.GuiQtUtil.add_qt_fonts(
                gui_core.GuiQtFont.get_all()
            )

            prx_window = window_proxy_cls(**kwargs)
            prx_window.set_main_window_geometry(gui_qt_core.GuiQtDcc.get_qt_main_window_geometry_args())

            window = prx_window.widget
            system_tray_icon = gui_qt_core.QtSystemTrayIcon(window)
            system_tray_icon.setIcon(window.windowIcon())
            system_tray_icon.show()
            window._set_window_system_tray_icon_(system_tray_icon)

            if isinstance(show_kwargs, dict):
                prx_window.set_window_show(**show_kwargs)
            else:
                prx_window.set_window_show()

            if process_fnc is not None:
                process_fnc(prx_window)

            gui_qt_core.GuiQtDcc.exit_app(app)
        else:
            prx_window = window_proxy_cls(**kwargs)
            prx_window.set_main_window_geometry(gui_qt_core.GuiQtDcc.get_qt_main_window_geometry_args())

            if isinstance(show_kwargs, dict):
                prx_window.set_window_show(**show_kwargs)
            else:
                prx_window.set_window_show()

            if process_fnc is not None:
                process_fnc(prx_window)

            if gui_qt_core.GuiQtDcc.get_is_clarisse():
                gui_qt_core.GuiQtDcc.exit_app(exists_app)

    @staticmethod
    def find_widget_proxy_by_class(widget_proxy_cls):
        list_ = []
        # noinspection PyArgumentList
        qt_widgets = gui_qt_core.QtWidgets.QApplication.topLevelWidgets()
        if qt_widgets:
            for i_qt_widget in qt_widgets:
                if hasattr(i_qt_widget, 'gui_proxy'):
                    i_widget_proxy = i_qt_widget.gui_proxy
                    if i_widget_proxy.__class__.__name__ == widget_proxy_cls.__name__:
                        list_.append(i_widget_proxy)
        return list_

    @staticmethod
    def find_widget_proxy_by_category(category_includes):
        list_ = []
        # noinspection PyArgumentList
        qt_widgets = gui_qt_core.QtWidgets.QApplication.topLevelWidgets()
        if qt_widgets:
            for i_qt_widget in qt_widgets:
                if hasattr(i_qt_widget, 'gui_proxy'):
                    i_widget_proxy = i_qt_widget.gui_proxy
                    if i_widget_proxy.PRX_CATEGORY in category_includes:
                        list_.append(i_widget_proxy)
        return list_

    @staticmethod
    def find_all_tool_window_proxies():
        qt_widgets = gui_qt_core.GuiQtUtil.find_all_valid_qt_windows()
        list_ = []
        for i_qt_widget in qt_widgets:
            if hasattr(i_qt_widget, 'gui_proxy'):
                i_widget_proxy = i_qt_widget.gui_proxy
                if hasattr(i_widget_proxy, 'PRX_CATEGORY'):
                    if i_widget_proxy.PRX_CATEGORY == 'tool_window':
                        list_.append(i_widget_proxy)
        return list_

    @staticmethod
    def window_proxy_trace_log(window_proxy, text):
        if hasattr(window_proxy, 'trace_log_use_thread'):
            window_proxy.trace_log_use_thread(text)

    @staticmethod
    def window_proxy_write_log(window_proxy, text):
        if hasattr(window_proxy, 'qt_log_write_fnc'):
            window_proxy.qt_log_write_fnc(text)

    @staticmethod
    def find_window_proxy_by_unique_id(unique_id):
        qt_windows = gui_qt_core.GuiQtUtil.find_all_valid_qt_windows()
        for i_window in qt_windows:
            if hasattr(i_window, 'gui_proxy'):
                window_proxy = i_window.gui_proxy
                if hasattr(window_proxy, 'PRX_CATEGORY'):
                    if window_proxy.get_window_unique_id() == unique_id:
                        return window_proxy

    @staticmethod
    def find_window_proxy_by_session_name(name):
        qt_windows = gui_qt_core.GuiQtUtil.find_all_valid_qt_windows()
        for i_window in qt_windows:
            if hasattr(i_window, 'gui_proxy'):
                window_proxy = i_window.gui_proxy
                if hasattr(window_proxy, 'PRX_TYPE'):
                    if window_proxy.PRX_TYPE == 'session_window':
                        if window_proxy.session.get_name() == name:
                            return window_proxy


class GuiProxyLog(object):
    @staticmethod
    def trace_result(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_trace_log(window_proxy, text)

    @staticmethod
    def trace_warning(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_trace_log(window_proxy, text)

    @staticmethod
    def trace_error(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_trace_log(window_proxy, text)

    @staticmethod
    def write(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_write_log(window_proxy, text)


class GuiProxyModifier(object):
    @staticmethod
    def window_proxy_waiting(method):
        def sub_fnc_(*args, **kwargs):
            _window_proxy = args[0]
            _window_proxy.start_waiting()
            _fnc = method(*args, **kwargs)
            _window_proxy.stop_waiting()
            return _fnc
        return sub_fnc_


class GuiProxyProcess(object):
    @staticmethod
    def create(maximum, label=None):
        list_ = []
        qt_windows = gui_qt_core.GuiQtUtil.find_all_valid_qt_windows()
        for i_window in qt_windows:
            if hasattr(i_window, 'gui_proxy'):
                window_proxy = i_window.gui_proxy
                if hasattr(window_proxy, 'PRX_CATEGORY'):
                    if window_proxy.PRX_CATEGORY in {'tool_window', 'dialog_window'}:
                        p = window_proxy.set_progress_create(maximum, label=label)
                        list_.append(p)
        return list_


class GuiProxyException(object):
    ValidationStatus = gui_configure.ValidationStatus

    @classmethod
    def _generate_window_(cls):
        import lxgui.proxy.core as gui_prx_core

        import lxgui.proxy.widgets as prx_widgets

        _0 = gui_prx_core.GuiProxyUtil.find_widget_proxy_by_category(['exception_window'])
        if _0:
            return _0[0]

        _1 = prx_widgets.PrxExceptionWindow()

        _1.set_window_title('Exception')
        _1.set_definition_window_size((640, 320))
        _1.set_window_show()
        return _1

    @classmethod
    def trace(cls):
        import sys
        #
        import traceback

        #
        exc_texts = []
        exc_type, exc_value, exc_stack = sys.exc_info()
        if exc_type:
            value = repr(exc_value)
            for i_stk in traceback.extract_tb(exc_stack):
                i_file_path, i_line, i_fnc, i_fnc_line = i_stk
                exc_texts.append(
                    '    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
                )

            w = cls._generate_window_()

            w.set_status(cls.ValidationStatus.Error)
            w.add_content('*'*80)
            w.add_content('traceback:')
            [w.add_content(i) for i in exc_texts]
            w.add_content(value)
            w.add_content('*'*80)

            # sys.stderr.write('traceback:\n')
            # sys.stderr.write('\n'.join(exc_texts)+'\n')
            # sys.stderr.write(value+'\n')
            return w


class GuiProxyLogBridge(object):
    KEY = 'gui bridge'

    @classmethod
    def generate_for_log(cls):
        if log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_ENABLE'] is False:
            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_ENABLE'] = True

            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_RESULT'] = GuiProxyLog.trace_result
            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_WARNING'] = GuiProxyLog.trace_warning
            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_ERROR'] = GuiProxyLog.trace_error

            log_core.Log.trace_method_result(
                cls.KEY, 'generate log trace bridge'
            )

    @classmethod
    def generate_for_process(cls):
        if log_bridge.__dict__['BRG_FNC_LOG_GUI_PROCESS_ENABLE'] is False:
            log_bridge.__dict__['BRG_FNC_LOG_GUI_PROCESS_ENABLE'] = True

            log_bridge.__dict__['BRG_FNC_LOG_GUI_PROCESS_CREATE'] = GuiProxyProcess.create

            log_core.Log.trace_method_result(
                cls.KEY, 'generate log progress bridge'
            )

    @classmethod
    def generate_for_exception(cls):
        if log_bridge.__dict__['BRG_FNC_LOG_GUI_EXCEPTION_ENABLE'] is False:
            log_bridge.__dict__['BRG_FNC_LOG_GUI_EXCEPTION_ENABLE'] = True

            log_bridge.__dict__['BRG_FNC_LOG_GUI_EXCEPTION_TRACE'] = GuiProxyException.trace

            log_core.Log.trace_method_result(
                cls.KEY, 'generate log exception bridge'
            )

    @classmethod
    def generate_all(cls):
        cls.generate_for_log()
        cls.generate_for_process()
        cls.generate_for_exception()
