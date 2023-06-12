# coding:utf-8
import fnmatch

import functools

import uuid

from contextlib import contextmanager

from lxbasic import bsc_configure, bsc_core

from lxutil import utl_core

from lxutil_gui import utl_gui_configure

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.proxy import utl_gui_prx_core


class AbsPrxStateDef(object):
    NORMAL_STATE = utl_gui_configure.State.NORMAL
    ENABLE_STATE = utl_gui_configure.State.ENABLE
    DISABLE_STATE = utl_gui_configure.State.DISABLE
    WARNING_STATE = utl_gui_configure.State.WARNING
    ERROR_STATE = utl_gui_configure.State.ERROR

    LOCKED_STATE = utl_gui_configure.State.LOCKED
    #
    State = utl_gui_configure.State


class AbsPrx(object):
    QT_WIDGET_CLS = None
    MODEL_CLS = None
    DCC_OBJ_KEY = 'dcc_obj'
    #
    PRX_CATEGORY = 'dialog_window'
    def __init__(self, *args, **kwargs):
        self._qt_widget = self.QT_WIDGET_CLS(*args, **kwargs)
        self._qt_widget.gui_proxy = self
        if self.MODEL_CLS is not None:
            self._model = self.MODEL_CLS()
        else:
            self._model = None
        #
        self._custom_raw = {}
    @property
    def widget(self):
        return self._qt_widget
    @property
    def model(self):
        return self._model

    def set_parent_widget(self, widget):
        self._qt_widget.setParent(widget)

    def set_gui_attribute(self, key, value):
        self._custom_raw[key] = value

    def get_gui_attribute(self, key, default=None):
        return self._custom_raw.get(key, default)

    def set_gui_dcc_obj(self, dcc_obj, namespace=None):
        key = self.DCC_OBJ_KEY
        if namespace is not None:
            key = '{}:{}'.format(namespace, self.DCC_OBJ_KEY)
        self.set_gui_attribute(key, dcc_obj)

    def get_gui_dcc_obj(self, namespace=None):
        key = self.DCC_OBJ_KEY
        if namespace is not None:
            key = '{}:{}'.format(namespace, self.DCC_OBJ_KEY)
        return self.get_gui_attribute(key)

    def get_obj_gui(self):
        pass

    def get_custom_raws(self, regex):
        lis = []
        keys = fnmatch.filter(self._custom_raw.keys(), regex) or []
        for key in keys:
            lis.append(self.get_gui_attribute(key))
        return lis

    def get_is_exists(self):
        pass

    def set_visible(self, boolean, **kwargs):
        self.widget.setHidden(not boolean)

    def set_actions_register(self, action_data):
        pass

    def __str__(self):
        return '{}(widget="{}")'.format(
            self.__class__.__name__,
            self.QT_WIDGET_CLS.__name__
        )


class AbsPrxWidget(AbsPrx):
    ProcessStatus = bsc_configure.Status
    ValidatorStatus = bsc_configure.ValidatorStatus
    def __init__(self, *args, **kwargs):
        super(AbsPrxWidget, self).__init__(*args, **kwargs)
        #
        self._qt_thread_enable = bsc_core.EnvironMtd.get_qt_thread_enable()
        #
        self._set_build_()

    def _set_build_(self):
        pass

    def set_hide(self, boolean=True):
        if boolean is True:
            self.widget.hide()
        else:
            self.widget.show()

    def set_show(self, boolean=True):
        if boolean is True:
            self.widget.show()
        else:
            self.widget.hide()


class AbsPrxViewDef(object):
    def _set_prx_view_def_init_(self, qt_view):
        self._qt_view = qt_view
    @property
    def view(self):
        return self._qt_view

    def set_item_add(self, *args, **kwargs):
        raise NotImplementedError()
    #
    def connect_item_select_changed_to(self, fnc):
        self._qt_view.itemSelectionChanged.connect(fnc)

    def connect_focus_changed_to(self, fnc):
        self._qt_view.focus_changed.connect(fnc)
    # select
    def _get_selected_items_(self):
        return self.view.selectedItems()

    def get_selected_items(self):
        return [i.gui_proxy for i in self._get_selected_items_()]


class _Loading(object):
    def __init__(self, proxy):
        self._proxy = proxy

    def start(self):
        self._proxy.start_waiting()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._proxy.stop_waiting()


class AbsPrxWaitingDef(object):
    QT_WAITING_CHART_CLS = None
    @property
    def widget(self):
        raise NotImplementedError()

    def waiting(self):
        return _Loading(self)

    def _set_waiting_def_init_(self):
        self._qt_waiting_char = self.QT_WAITING_CHART_CLS(self.widget)
        self._qt_waiting_char.hide()
        #
        self._auto_stop_timer = utl_gui_qt_core.QtCore.QTimer(self.widget)
        #
        self.widget._set_size_changed_connect_to_(self._refresh_waiting_draw_)

    def start_waiting(self, auto_stop_time=None):
        self.widget.setCursor(utl_gui_qt_core.QtCore.Qt.BusyCursor)
        self._qt_waiting_char.show()
        utl_gui_qt_core.ApplicationOpt().set_process_run_0()
        self._qt_waiting_char._start_waiting_()
        if isinstance(auto_stop_time, (int, float)):
            self._auto_stop_timer.singleShot(
                auto_stop_time, self.stop_waiting
            )

    def update_waiting(self):
        self._qt_waiting_char.update()
        utl_gui_qt_core.ApplicationOpt().set_process_run_0()

    def stop_waiting(self):
        self.widget.unsetCursor()
        self._qt_waiting_char.hide()
        utl_gui_qt_core.ApplicationOpt().set_process_run_0()
        self._qt_waiting_char._stop_waiting_()

    def _refresh_waiting_draw_(self):
        x, y = 0, 0
        w, h = self.widget.width(), self.widget.height()
        self._qt_waiting_char.setGeometry(
            x, y, w, h
        )

    def set_methods_run_use_thread(self, methods):
        def debug_run_fnc_(fnc_, *args, **kwargs):
            # noinspection PyBroadException
            try:
                _method = fnc_(*args, **kwargs)
            except:
                from lxutil import utl_core
                #
                utl_core.ExceptionCatcher.set_create()
                raise

        thread = self.widget._set_thread_create_()

        thread.run_started.connect(self.start_waiting)
        thread.run_finished.connect(self.stop_waiting)
        for i in methods:
            thread.set_method_add(
                functools.partial(debug_run_fnc_, i)
            )
        #
        thread.start()


class AbsPrxWindow(AbsPrx):
    def __init__(self, *args, **kwargs):
        super(AbsPrxWindow, self).__init__(*args, **kwargs)
        self._window_unicode_id = str(uuid.uuid1()).upper()
        #
        if kwargs.get('parent'):
            pass
            # print kwargs['parent']
        else:
            main_window = utl_gui_qt_core.QtDccMtd.get_qt_main_window()
            # print main_window.font()
            if main_window != self.widget:
                self.widget.setParent(
                    main_window, utl_gui_qt_core.QtCore.Qt.Window
                )
        #
        self._main_window_geometry = None
        #
        self._definition_window_size = 480, 320
        #
        self.widget.setBaseSize(
            utl_gui_qt_core.QtCore.QSize(*self._definition_window_size)
        )
        #
        self._window_title = None

        self._close_methods = []
        #
        self._status = bsc_configure.ValidatorStatus.Normal

        self._set_build_()

    def get_window_unique_id(self):
        return self._window_unicode_id

    def _set_build_(self):
        pass

    def set_main_window_geometry(self, geometry):
        self._main_window_geometry = geometry
        self._qt_widget._main_window_geometry = geometry

    def get_definition_window_size(self):
        return self._definition_window_size

    def set_definition_window_size(self, size):
        if size is not None:
            self._definition_window_size = size
            self.widget.setBaseSize(
                utl_gui_qt_core.QtCore.QSize(*self._definition_window_size)
            )

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # show unique
        if exclusive is True:
            gui_proxies = utl_gui_prx_core.get_gui_proxy_by_class(self.__class__)
            for i in gui_proxies:
                if hasattr(i, '_window_unicode_id'):
                    if i._window_unicode_id != self._window_unicode_id:
                        utl_core.Log.set_module_warning_trace(
                            'close exists window for "{}"'.format(
                                self.__class__.__name__
                            )
                        )
                        i.set_window_close()
        #
        utl_gui_qt_core.set_qt_window_show(self.widget, pos, size)

    def set_close_method(self, method):
        self._close_methods.append(method)

    def set_window_close_connect_to(self, method):
        self._close_methods.append(method)

    def set_window_close(self):
        for i in self._close_methods:
            i()
        #
        self._qt_widget.close()
        self._qt_widget.deleteLater()

    def set_window_close_later(self, time=1000):
        self._qt_widget.hide()
        self._qt_widget._set_close_later_(time)

    def set_window_title(self, *args):
        text = args[0]
        self._window_title = text
        self._qt_widget.setWindowTitle(text)
        self._qt_widget._set_icon_name_text_(text)

    def get_window_title(self):
        return self._window_title

    def set_window_icon_name_text(self, text):
        self.widget._set_icon_name_text_(text)

    def set_window_icon_name(self, icon_name):
        self.widget._set_icon_name_(icon_name)

    def set_window_system_tray_icon(self, widget):
        self.widget._set_window_system_tray_icon_(widget)

    def set_status(self, status):
        self._status = status

    def connect_refresh_action_to(self, fnc):
        self._qt_widget._create_window_shortcut_action_(
            fnc, 'F5'
        )

    def connect_window_activate_changed_to(self, fnc):
        self._qt_widget.window_activate_changed.connect(fnc)

    def get_is_active_window(self):
        return self._qt_widget.isActiveWindow()


class AbsWidgetContentDef(object):
    CONTENT_WIDGET_CLS = None
    def _set_widget_content_def_init_(self, layout):
        self._widget_content_qt_layout_0 = layout
        self._widget_content_widget_dict = {}
        self._widget_content_widget_current = None

    def create_content_widget(self, key):
        qt_widget_0 = self.CONTENT_WIDGET_CLS()
        qt_widget_0.hide()
        self._widget_content_qt_layout_0.addWidget(qt_widget_0)
        self._widget_content_widget_dict[key] = qt_widget_0
        return qt_widget_0

    def set_current_unit(self, key):
        pre_widget = self._widget_content_widget_current
        cur_widget = self._widget_content_widget_dict[key]
        if pre_widget is not None:
            pre_widget.hide()
        cur_widget.show()
        self._widget_content_widget_current = cur_widget

    def get_current_content_qt_widget(self):
        return self._widget_content_widget_current


class GuiProgress(object):
    FORMAT_0 = '{percent}% {costed_time}'
    FORMAT_1 = '{percent}% {costed_time} / {estimated_time}'
    def __init__(self, proxy, qt_progress, maximum, label=None):
        self._proxy = proxy
        self._qt_progress = qt_progress
        self._maximum = maximum
        self._value = 0
        self._label = label
        # time
        self._timestamp_started = bsc_core.TimeMtd.get_timestamp()
        self._timestamp_costed = 0
        #
        self._timestamp_estimated = 0
        # all value map to low
        self._map_maximum = min(maximum, 100)
        self._map_value = 0
        #
        self._parent = None
        #
        self._sub_start = None
        self._sub_end = None
        #
        self._children = []
        #
        self._is_stop = False
        #
        self._is_raise = False
        #
        self._depth = 0

        self._qt_progress.show()
    @property
    def label(self):
        return self._label
    @property
    def value(self):
        return self._value
    @property
    def maximum(self):
        return self._maximum
    @property
    def percent(self):
        return self._get_percent_()

    def get_qt_progress(self):
        return self._qt_progress

    def get_maximum(self):
        return self._maximum

    def set_maximum(self, v):
        self._maximum = v

    def get_value(self):
        return self._value

    def set_value(self, v):
        self._value = v
    #
    def get_depth(self):
        return self._depth
    #
    def set_start(self):
        pass

    def set_update(self):
        if self._is_stop is False:
            self._value += 1
            #
            if self._maximum > 1:
                map_value = int(
                    bsc_core.RawValueRangeMtd.set_map_to(
                        (1, self._maximum), (1, self._map_maximum), self._value
                    )
                )
                if map_value != self._map_value:
                    self._map_value = map_value
                    #
                    self._timestamp_costed = bsc_core.TimeMtd.get_timestamp()-self._timestamp_started
                    if self._value > 1:
                        self._timestamp_estimated = (self._timestamp_costed/(self._value-1))*self._maximum
                    else:
                        self._timestamp_estimated = 0
                    #
                    root = self.get_root()
                    root.update_qt_process()

    def set_stop(self):
        if self.get_is_root():
            self._qt_progress._stop_progress_()
            self._value = 0
            self._maximum = 0
            self._map_value = 0
            self._map_maximum = 0
            self._is_stop = True
            self._qt_progress.hide()

    def get_is_stop(self):
        return self._is_stop

    def set_raise(self):
        self._is_raise = True

    def get_parent(self):
        return self._parent

    def get_is_root(self):
        return self._parent is None

    def _get_percent_(self):
        if self._maximum > 0:
            return round(float(self._value)/float(self._maximum), 4)
        else:
            return 0

    def _get_span_(self):
        if self.maximum > 0:
            return round(float(1)/float(self.maximum), 4)
        return 0

    def add_child(self, progress_fnc):
        self._children.append(progress_fnc)
        progress_fnc._parent = self
        #
        progress_fnc._sub_end = self._get_percent_()
        progress_fnc._sub_start = max(min(round(progress_fnc._sub_end-self._get_span_(), 4), 1.0), 0.0)

    def get_show_percent(self):
        kwargs = dict(
            percent=('%3d' % (int(self._get_percent_()*100))),
            value=self._value,
            maximum=self._maximum,
            costed_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                self._timestamp_costed,
                mode=1
            ),
            estimated_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                self._timestamp_estimated,
                mode=1
            ),
        )
        if int(self._timestamp_estimated) > 0:
            return self.FORMAT_1.format(
                **kwargs
            )
        return self.FORMAT_0.format(
            **kwargs
        )

    def update_qt_process(self):
        if self._qt_progress is not None:
            if self.get_is_root() is True:
                descendants = self.get_descendants()
                #
                raw = [(self._get_percent_(), (0, 1), self._label, self.get_show_percent())]
                maximums, values = [self._maximum], [self._value]
                map_maximums, map_values = [self._map_maximum], [self._map_value]
                for i_index, i_descendant in enumerate(descendants):
                    maximums.append(i_descendant._maximum)
                    values.append(i_descendant._value)
                    #
                    map_maximums.append(i_descendant._map_maximum)
                    map_values.append(i_descendant._map_value)
                    #
                    i_percent_start = i_descendant._sub_start
                    i_percent_end = i_descendant._sub_end
                    i_percent = i_descendant._get_percent_()
                    #
                    i_label = i_descendant._label
                    i_show_percent = i_descendant.get_show_percent()
                    if i_percent < 1:
                        raw.append(
                            (i_percent, (i_percent_start, i_percent_end), i_label, i_show_percent)
                        )
                #
                maximum, value = sum(maximums), sum(values)
                map_maximum, map_value = sum(map_maximums), sum(map_values)
                #
                self._qt_progress._set_progress_raw_(raw)
                #
                self._qt_progress._set_progress_maximum_(maximum)
                self._qt_progress._set_progress_map_maximum_(map_maximum)
                self._qt_progress._set_progress_value_(value)

    def get_root(self):
        def rcs_fnc_(obj_):
            _parent = obj_.get_parent()
            if _parent is None:
                return obj_
            else:
                return rcs_fnc_(_parent)
        #
        return rcs_fnc_(self)

    def get_descendants(self):
        def rcs_fnc_(lis_, obj_):
            _children = obj_.get_children()
            if _children:
                for _child in _children:
                    lis_.append(_child)
                    rcs_fnc_(lis_, _child)
        #
        lis = []
        rcs_fnc_(lis, self)
        return lis

    def get_children(self):
        return self._children

    def get_descendant_args(self):
        def rcs_fnc_(lis_, obj_, depth_):
            _children = obj_.get_children()
            if _children:
                for _i_child in _children:
                    lis_.append((depth_, _i_child))
                    #
                    rcs_fnc_(lis_, _i_child, depth_+1)
        #
        lis = []
        rcs_fnc_(lis, self, 0)
        return lis

    def __str__(self):
        return '{}(label="{}", maximum={}, value={})'.format(
            self.__class__.__name__,
            self._label,
            self.maximum,
            self.value
        )

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_stop()


class AbsPrxProgressingDef(object):
    QT_PROGRESSING_CHART_CLS = None
    PROGRESS_FNC_CLS = GuiProgress
    PROGRESS_WIDGET_CLS = None
    @property
    def widget(self):
        raise NotImplementedError()

    def _set_progressing_def_init_(self):
        self._qt_progressing_char = self.QT_PROGRESSING_CHART_CLS(self.widget)
        self._qt_progressing_char.hide()

        self.widget._set_size_changed_connect_to_(self._refresh_progressing_draw_)

        self._current_progress = None

    def _refresh_progressing_draw_(self):
        x, y = 0, 0
        w, h = self.widget.width(), self.widget.height()
        self._qt_progressing_char.setGeometry(
            x, y, w, h
        )
        self._qt_progressing_char._refresh_widget_draw_()

    def set_progress_create(self, maximum, label=None):
        g_p = self.PROGRESS_FNC_CLS(
            proxy=self,
            qt_progress=self._qt_progressing_char,
            maximum=maximum,
            label=label
        )
        if self._current_progress is None:
            self._current_progress = g_p
        else:
            if self._current_progress.get_is_stop() is True:
                self._current_progress = g_p
            else:
                self._current_progress.add_child(g_p)
        return g_p
    @contextmanager
    def gui_progressing(self, maximum, label=None):
        g_p = self.set_progress_create(maximum, label)
        yield g_p
        g_p.set_stop()


class AbsPrxMenuDef(object):
    def _set_prx_menu_def_init_(self):
        pass

    @property
    def widget(self):
        raise NotImplementedError()

    def set_menu_title(self, text):
        self.widget._set_menu_title_text_(text)

    def set_menu_raw(self, raw):
        self.widget._set_menu_data_(raw)

    def set_menu_raw_add(self, raw):
        self.widget._add_menu_data_(raw)

    def set_menu_raw_extend(self, raw):
        self.widget._extend_menu_data_(raw)

    def get_menu_raw(self):
        return self.widget._get_menu_data_()

    def set_menu_content(self, content):
        self.widget._set_menu_content_(content)


class AbsPrxItemFilterTgtDef(object):
    @property
    def item(self):
        raise NotImplementedError()

    def set_tag_filter_tgt_mode(self, *args, **kwargs):
        self.item._set_item_tag_filter_mode_(*args, **kwargs)

    def get_tag_filter_tgt_mode(self):
        return self.item._get_item_tag_filter_mode_()

    def set_tag_filter_tgt_key_add(self, *args, **kwargs):
        self.item._set_item_tag_filter_keys_tgt_add_(*args, **kwargs)

    def get_tag_filter_tgt_keys(self):
        return self.item._get_item_tag_filter_keys_tgt_()

    def set_tag_filter_tgt_statistic_enable(self, *args, **kwargs):
        self.item._set_item_tag_filter_tgt_statistic_enable_(*args, **kwargs)

    def get_tag_filter_tgt_statistic_enable(self):
        return self.item._get_item_tag_filter_tgt_statistic_enable_()

    def get_states(self):
        return self.item._get_state_()

    def set_states(self, *args, **kwargs):
        self.item._set_state_(*args, **kwargs)

    def set_keyword_filter_keys_tgt(self, keys):
        self.item._set_item_keyword_filter_keys_tgt_(keys)

    def update_keyword_filter_keys_tgt(self, keys):
        self.item._update_item_keyword_filter_keys_tgt_(keys)

    def get_keyword_filter_keys_tgt(self):
        return self.item._get_keyword_filter_keys_tgt_()


class AbsPrxViewFilterTagDef(object):
    @property
    def view(self):
        raise NotImplementedError()
    @property
    def filter_bar(self):
        raise NotImplementedError()

    def get_tag_filter_tgt_statistic_raw(self):
        return self.view._get_view_tag_filter_tgt_statistic_raw_()

    def set_tag_filter_all_keys_src(self, *args, **kwargs):
        self.view._set_view_tag_filter_data_src_(*args, **kwargs)
        self.refresh_items_visible_by_any_filter()
        self.view._refresh_view_all_items_viewport_showable_()

    def get_item_states(self, items):
        return self.view._get_view_item_states_(items)

    def get_item_state_colors(self, items):
        return self.view._get_view_item_state_colors_(items)

    def refresh_items_visible_by_any_filter(self):
        self.view._set_view_keyword_filter_data_src_(self.filter_bar.get_keywords())
        self.view._refresh_view_items_visible_by_any_filter_()


class AbsPrxItemVisibleConnectionDef(object):
    @property
    def item(self):
        raise NotImplementedError()

    def set_visible_connect_to(self, key, prx_item_tgt):
        self.item._set_item_visible_connect_to_(key, prx_item_tgt.item)

    def set_visible_src_key(self, key):
        self.item._set_item_visible_src_key_(key)

    def get_visible_src_key(self):
        return self.item._get_item_visible_src_key_()

    def set_visible_tgt_key(self, key):
        self.item._set_item_visible_tgt_key_(key)

    def get_visible_tgt_key(self):
        return self.item._get_item_visible_tgt_key_()

    def set_visible_tgt_view(self, prx_view):
        self.item._set_item_visible_tgt_view_(prx_view.view)

    def get_visible_tgt_view(self):
        return self.item._get_item_visible_tgt_view_()

    def set_visible_connection_refresh(self):
        self.item._set_item_visible_connection_refresh_()


class AbsPrxViewVisibleConnectionDef(object):
    @property
    def view(self):
        raise NotImplementedError()

    def set_visible_tgt_raw(self, raw):
        self.view._set_view_visible_tgt_raw_(raw)

    def get_visible_tgt_raw(self):
        return self.view._get_view_visible_tgt_raw_()

    def set_visible_tgt_raw_clear(self):
        self.view._set_view_visible_tgt_raw_clear_()

    def set_visible_tgt_raw_update(self):
        self.view._set_view_visible_tgt_raw_update_()
