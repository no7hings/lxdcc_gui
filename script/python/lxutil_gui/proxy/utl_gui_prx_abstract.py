# coding:utf-8
import fnmatch

from lxbasic import bsc_configure

from lxutil_gui import utl_gui_configure

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.proxy import utl_gui_prx_core


class _PrxStateDef(object):
    NORMAL_STATE = utl_gui_configure.State.NORMAL
    ENABLE_STATE = utl_gui_configure.State.ENABLE
    DISABLE_STATE = utl_gui_configure.State.DISABLE
    WARNING_STATE = utl_gui_configure.State.WARNING
    ERROR_STATE = utl_gui_configure.State.ERROR


class AbsPrx(object):
    QT_WIDGET_CLASS = None
    MODEL_CLASS = None
    DCC_OBJ_KEY = 'dcc_obj'
    #
    PRX_TYPE = None
    def __init__(self, *args, **kwargs):
        self._qt_widget = self.QT_WIDGET_CLASS(*args, **kwargs)
        self._qt_widget.gui_proxy = self
        if self.MODEL_CLASS is not None:
            self._model = self.MODEL_CLASS()
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

    def __str__(self):
        return '{}(widget="{}")'.format(
            self.__class__.__name__,
            self.QT_WIDGET_CLASS.__name__
        )


class AbsPrxWidget(AbsPrx):
    def __init__(self, *args, **kwargs):
        super(AbsPrxWidget, self).__init__(*args, **kwargs)
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
    def set_item_select_changed_connect_to(self, fnc):
        self.view.itemSelectionChanged.connect(fnc)

    # select
    def _get_selected_items_(self):
        return self.view.selectedItems()

    def get_selected_items(self):
        return [i.gui_proxy for i in self._get_selected_items_()]


class AbsPrxWindow(AbsPrx):
    def __init__(self, *args, **kwargs):
        super(AbsPrxWindow, self).__init__(*args, **kwargs)
        main_window = utl_gui_qt_core.QtDccMtd.get_qt_main_window()
        # print main_window.font()
        if main_window != self.widget:
            self.widget.setParent(
                main_window, utl_gui_qt_core.QtCore.Qt.Window
            )
        self._definition_window_size = 480, 320
        #
        self.widget.setBaseSize(
            utl_gui_qt_core.QtCore.QSize(*self._definition_window_size)
        )
        #
        self._window_title = None

        self._close_methods = []
        #
        self._status = bsc_configure.GuiStatus.Normal

        self._set_build_()

    def _set_build_(self):
        pass

    def get_definition_window_size(self):
        return self._definition_window_size

    def set_definition_window_size(self, size):
        self._definition_window_size = size
        self.widget.setBaseSize(
            utl_gui_qt_core.QtCore.QSize(*self._definition_window_size)
        )

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # show unique
        if exclusive is True:
            gui_proxies = utl_gui_prx_core.get_gui_proxy_by_class(self.__class__)
            for i in gui_proxies:
                if not i == self:
                    if hasattr(i, 'set_window_close'):
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


class AbsWidgetContentDef(object):
    CONTENT_WIDGET_CLASS = None
    def _set_widget_content_def_init_(self, layout):
        self._widget_content_qt_layout_0 = layout
        self._widget_content_widget_dict = {}
        self._widget_content_widget_current = None

    def _set_cnt_wdt_create_(self, key):
        qt_widget_0 = self.CONTENT_WIDGET_CLASS()
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
    MAXIMUM_UPDATE_VALUE = 100
    def __init__(self, proxy, qt_progress, maximum, label=None):
        self._proxy = proxy
        self._qt_progress = qt_progress
        self._maximum = maximum
        self._value = 0
        self._label = label
        #
        self._range_maximum = 100
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

    def get_is_stop(self):
        return self._is_stop

    def set_update(self):
        if self._is_stop is False:
            self._value += 1
            #
            root = self.get_root()
            root._set_qt_progress_update_()

    def set_stop(self):
        if self.get_is_root():
            self._qt_progress._set_progress_stop_()
            self._value = 0
            self._maximum = 0
            self._is_stop = True

    def set_raise(self):
        self._is_raise = True

    def get_children(self):
        return self._children

    def get_parent(self):
        return self._parent

    def get_is_root(self):
        return self._parent is None

    def _get_percent_(self):
        if self.maximum > 0:
            return round(float(self.value)/float(self.maximum), 4)
        else:
            return 0

    def _get_span_(self):
        if self.maximum > 0:
            return round(float(1)/float(self.maximum), 4)
        return 0

    def set_child_add(self, progress):
        self._children.append(progress)
        progress._parent = self
        progress._sub_end = self._get_percent_()
        progress._sub_start = round(progress._sub_end - self._get_span_(), 4)

    def _set_qt_progress_update_(self):
        if self.get_qt_progress() is not None:
            if self.get_is_root() is True:
                raw = []
                descendants = self.get_descendants()
                #
                maximums, values = [self.maximum], [self.value]
                [maximums.append(i.maximum) for i in descendants], [values.append(i.value) for i in descendants]
                #
                maximum, value = sum(maximums), sum(values)
                #
                raw.append(
                    (0, 1, self._get_percent_(), self.label)
                )
                for descendant in descendants:
                    raw.append(
                        (descendant._sub_start, descendant._sub_end, descendant._get_percent_(), descendant.label)
                    )
                #
                self._qt_progress._set_progress_raw_(raw)
                #
                self._qt_progress._set_progress_maximum_value_(maximum)
                self._qt_progress._set_progress_value_(value)

    def get_root(self):
        def _rcs_fnc(obj_):
            _parent = obj_.get_parent()
            if _parent is None:
                return obj_
            else:
                return _rcs_fnc(_parent)
        return _rcs_fnc(self)

    def get_descendants(self):
        def _rcs_fnc(lis_, obj_):
            _children = obj_.get_children()
            if _children:
                for _child in _children:
                    lis_.append(_child)
                    _rcs_fnc(lis_, _child)

        lis = []
        _rcs_fnc(lis, self)
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


class AbsPrxProgressesDef(object):
    PROGRESS_CLASS = GuiProgress
    def _set_progresses_def_init_(self, qt_progress_bar):
        self._qt_progress_bar = qt_progress_bar
        #
        self._current_progress = None
        self._progress_maximum_value = 100
    #
    def set_progress_create(self, maximum, label=None):
        p = self.PROGRESS_CLASS(
            proxy=self,
            qt_progress=self._qt_progress_bar,
            maximum=maximum,
            label=label
        )
        if self._current_progress is None:
            self._current_progress = p
        else:
            if self._current_progress.get_is_stop() is True:
                self._current_progress = p
            else:
                self._current_progress.set_child_add(p)
        return p


class AbsPrxMenuDef(object):
    def _set_prx_menu_def_init_(self):
        pass

    @property
    def widget(self):
        raise NotImplementedError()

    def set_menu_title(self, text):
        self.widget._set_menu_title_text_(text)

    def set_menu_raw(self, raw):
        self.widget._set_menu_raw_(raw)

    def set_menu_raw_add(self, raw):
        self.widget._set_menu_raw_add_(raw)

    def set_menu_raw_extend(self, raw):
        self.widget._set_menu_raw_extend_(raw)

    def get_menu_raw(self):
        return self.widget._get_menu_raw_()

    def set_menu_content(self, content):
        self.widget._set_menu_content_(content)


class AbsPrxItemFilterTgtDef(object):
    @property
    def item(self):
        raise NotImplementedError()

    def set_tag_filter_tgt_mode(self, *args, **kwargs):
        self.item._set_item_tag_filter_tgt_mode_(*args, **kwargs)

    def get_tag_filter_tgt_mode(self):
        return self.item._get_item_tag_filter_tgt_mode_()

    def set_tag_filter_tgt_key_add(self, *args, **kwargs):
        self.item._set_item_tag_filter_tgt_key_add_(*args, **kwargs)

    def get_tag_filter_tgt_keys(self):
        return self.item._get_item_tag_filter_tgt_keys_()

    def set_tag_filter_tgt_statistic_enable(self, *args, **kwargs):
        self.item._set_item_tag_filter_tgt_statistic_enable_(*args, **kwargs)

    def get_tag_filter_tgt_statistic_enable(self):
        return self.item._get_item_tag_filter_tgt_statistic_enable_()

    def get_states(self):
        return self.item._get_item_state_()

    def set_states(self, *args, **kwargs):
        self.item._set_item_state_(*args, **kwargs)

    def set_keyword_filter_tgt_contexts(self, contexts):
        self.item._set_item_keyword_filter_tgt_contexts_(contexts)

    def get_keyword_filter_tgt_contexts(self):
        return self.item._get_item_keyword_filter_tgt_contexts_()


class AbsPrxViewFilterTagDef(object):
    @property
    def view(self):
        raise NotImplementedError()
    @property
    def filter_bar(self):
        raise NotImplementedError()

    def get_tag_filter_tgt_statistic_raw(self):
        return self.view._get_view_tag_filter_tgt_statistic_raw_()

    def set_tag_filter_tgt_keys(self, *args, **kwargs):
        self.view._set_view_tag_filter_tgt_keys_(*args, **kwargs)
        #
        self.set_items_visible_by_any_filter()
        #
        self.view._set_view_items_show_update_()

    def get_item_states(self, items):
        return self.view._get_view_item_states_(items)

    def get_item_state_colors(self, items):
        return self.view._get_view_item_state_colors_(items)

    def set_items_visible_by_any_filter(self):
        keyword = self.filter_bar.get_keyword()
        self.view._set_view_items_visible_by_any_filter_(
            keyword
        )


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
