# coding:utf-8
import functools

import lxlog.core as log_core

import lxbasic.core as bsc_core

import lxuniverse.abstracts as unr_abstracts

import lxgui.configure as gui_configure

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

from lxgui.qt.widgets import _gui_qt_wgt_utility, _gui_qt_wgt_split

import lxgui.proxy.abstracts as gui_prx_abstracts

from lxgui.proxy.widgets import _gui_prx_wgt_port_base, _gui_prx_wgt_port_entry, _gui_prx_wgt_contianer


# port =============================================================================================================== #
class AbsPrxPortBaseDef(object):
    ENTRY_TYPE = 'custom'

    Status = gui_configure.Status
    ProcessStatus = gui_configure.Status
    ShowStatus = gui_configure.ShowStatus
    ValidationStatus = gui_configure.ValidationStatus

    def _set_prx_port_def_init_(self, category, path, label=None):
        self._prx_node = None
        self._prx_group = None
        #
        self._category = category
        self._port_path = path
        self._name = self._port_path.split('.')[-1]
        #
        if label is not None:
            self._label = label
        else:
            self._label = bsc_core.RawStrUnderlineOpt(self._name).to_prettify(capitalize=False)

    def set_node(self, obj):
        self._prx_node = obj

    def get_node(self):
        return self._prx_node

    def set_group(self, obj):
        self._prx_group = obj

    def get_group(self):
        return self._prx_group

    def get_node_path(self):
        return self.get_node().get_path()

    def get_category(self):
        return self._category

    category = property(get_category)

    def get_type(self):
        return self.ENTRY_TYPE

    type = property(get_type)

    def get_name(self):
        return self._name

    name = property(get_name)

    def get_path(self):
        return '{}.{}'.format(
            self.get_node_path(),
            self.get_port_path()
        )

    path = property(get_path)

    def get_port_path(self):
        return self._port_path

    port_path = property(get_port_path)

    def get_group_path(self):
        return '.'.join(self.get_port_path().split('.')[:-1])

    group_path = property(get_group_path)

    def get_label(self):
        return self._label

    label = property(get_label)

    def get_is_root(self):
        return self._port_path == self.get_node().get_path()

    def get_children(self):
        node = self.get_node()
        port_path = self.get_port_path()
        port_paths = node.get_port_paths()
        if self.get_is_root():
            _ = [i for i in port_paths if not '.' in i]
        else:
            _ = bsc_core.DccPathDagMtd.get_dag_child_paths(
                port_path, port_paths, pathsep='.'
            )
        return node._get_ports_(_)

    def set_visible(self, *args, **kwargs):
        pass

    def set_visible_condition(self, condition):
        def visible_fnc_():
            _operator = condition.get('operator')
            _value_cdt = condition.get('value')
            _value = p.get()
            if _operator == 'in':
                self.set_visible(_value_cdt in _value)
            elif _operator == 'match_one':
                self.set_visible(_value in _value_cdt)
            elif _operator == 'is':
                self.set_visible(_value_cdt == _value)

        if condition:
            p = self.get_node().get_port(condition.get('port').replace('/', '.'))
            if p is not None:
                p.connect_value_changed_to(visible_fnc_)
                visible_fnc_()
            else:
                log_core.Log.trace_method_warning(
                    'visible condition connect',
                    'port="{}" is non-exists'.format(condition.get('port'))
                )

    def connect_value_changed_to(self, fnc):
        pass

    def connect_tab_pressed_to(self, fnc):
        pass

    def set_focus_in(self):
        pass

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


# port
class AbsPrxTypePort(AbsPrxPortBaseDef):
    ENTRY_TYPE = 'custom'
    ENABLE_CLS = None
    LABEL_CLS = None
    LABEL_HIDED = False
    KEY_HIDE = False
    ENTRY_CLS = None

    def __init__(
            self, path, label=None, enable=None, default_value=None, join_to_next=False, scheme_key=None,
            node_widget=None
    ):
        self._set_prx_port_def_init_('value', path, label)
        #
        self._key = None
        #
        if isinstance(enable, bool):
            self._use_enable = enable
        else:
            self._use_enable = False
        #
        self._prx_port_enable = self.ENABLE_CLS(node_widget)
        self._prx_port_enable.set_hide()
        # gui
        self._prx_port_label = self.LABEL_CLS(node_widget)
        self._prx_port_label.set_hide()
        self._prx_port_label.set_name(self._label)
        #
        self._prx_port_entry = self.ENTRY_CLS(node_widget)
        #
        if default_value is not None:
            self._prx_port_entry.set(default_value)
        #
        self._layout = None
        #
        self._is_join_to_next = join_to_next
        self._join_layout = None
        self._key_widget = None
        #
        self._custom_widget = None
        #
        self.set_name(self.label)

        self.connect_value_changed_to(
            self.set_changed_update
        )

        self._main_qt_widget = None

    def set_main_widget(self, widget):
        self._main_qt_widget = widget

    def set_node_widget(self, widget):
        self._prx_port_enable.set_parent_widget(
            widget
        )
        self._prx_port_entry.set_parent_widget(
            widget
        )
        self._prx_port_entry.set_parent_widget(
            widget
        )

    @property
    def label(self):
        return self._label

    @property
    def label_widget(self):
        return self._prx_port_label

    @property
    def entry_widget(self):
        return self._prx_port_entry

    def set_label_visible(self, boolean):
        self._prx_port_label.set_visible(boolean)

    def set_key(self, key):
        self._key = key

    def get_key(self):
        return self._key

    def set_name(self, name):
        self._prx_port_label.set_name(name)
        group = self.get_group()
        if group:
            group.update_children_name_width()

    def set_label(self, text):
        if text:
            self.set_name(text)
            self._label = text

    def set_sub_name_update(self):
        if hasattr(self._prx_port_entry._qt_entry_widget, '_set_name_text_'):
            self._prx_port_entry._qt_entry_widget._set_name_text_(self.label)

    def set_enable(self, boolean):
        if boolean is not None:
            if isinstance(boolean, bool):
                self._prx_port_enable.set_show()
                # self._prx_port_enable.set(boolean)
        else:
            self._prx_port_enable.set_hide()

    def set_use_enable(self, boolean):
        self._use_enable = boolean
        if boolean is not None:
            if isinstance(boolean, bool):
                if self._use_enable is True:
                    self._prx_port_enable.set_show()
                # self._prx_port_enable.set(boolean)
        else:
            self._prx_port_enable.set_hide()

    def get_use_enable(self):
        return self._use_enable

    def set_name_width(self, w):
        self.label_widget.set_width(w)

    def set(self, raw=None, **kwargs):
        self._prx_port_entry.set(raw, **kwargs)
        #
        self.set_changed_update()

    def set_default(self, raw, **kwargs):
        self._prx_port_entry.set_default(raw, **kwargs)
        #
        self.set_changed_update()

    def get_default(self):
        return self._prx_port_entry.get_default()

    def set_changed_update(self):
        if self.get_default() is not None:
            if self._prx_port_entry.get_is_default() is False:
                self._prx_port_enable.set(True)
            else:
                self._prx_port_enable.set(False)

    def set_value(self, *args, **kwargs):
        self.set(*args, **kwargs)

    def set_choose_values(self, *args, **kwargs):
        self._prx_port_entry.set_choose_values(*args, **kwargs)

    def append(self, raw):
        if hasattr(self._prx_port_entry, 'append'):
            self._prx_port_entry.append(raw)

    def set_clear(self):
        self._prx_port_entry.set_clear()

    def set_reset(self):
        default = self.get_default()
        if default is not None:
            self.set(default)

    def set_option(self, value):
        self._prx_port_entry.set_option(value)

    def set_tool_tip(self, *args, **kwargs):
        kwargs['name'] = 'entry as "{}"'.format(
            self.ENTRY_TYPE,
        )
        kwargs['name'] = self.get_port_path()
        self._prx_port_entry.set_tool_tip(*args, **kwargs)

    def get(self):
        return self._prx_port_entry.get()

    def connect_value_changed_to(self, fnc):
        return self._prx_port_entry.connect_value_changed_to(fnc)

    def connect_tab_pressed_to(self, fnc):
        return self._prx_port_entry.connect_tab_pressed_to(fnc)

    def set_focus_in(self):
        self._prx_port_entry.set_focus_in()

    def set_use_as_storage(self, boolean=True):
        self._prx_port_entry.set_use_as_storage(boolean)

    #
    def _set_layout_(self, layout):
        self._layout = layout

    def _get_layout_(self):
        return self._layout

    # join to next
    def set_join_to_next(self, boolean):
        self._is_join_to_next = boolean

    def _get_is_join_next_(self):
        return self._is_join_to_next

    def _set_join_layout_(self, layout):
        self._join_layout = layout

    def _get_join_layout_(self):
        return self._join_layout

    def _set_key_widget_(self, widget):
        self._key_widget = widget

    def set_menu_data(self, raw):
        self._prx_port_entry.set_menu_data(raw)

    def to_custom_widget(self, label_width=80):
        if self._custom_widget is not None:
            return self._custom_widget
        else:
            widget = _gui_qt_wgt_utility._QtTranslucentWidget()
            layout = _gui_qt_wgt_utility.QtHBoxLayout(widget)
            label = self.label_widget
            label.set_width(label_width)
            layout.addWidget(label.widget)
            entry = self._prx_port_entry
            layout.addWidget(entry.widget)
            self._custom_widget = widget
            return self._custom_widget

    def set_locked(self, *args, **kwargs):
        self._prx_port_entry.set_locked(*args, **kwargs)

    def set_history_key(self, key):
        self._prx_port_entry.set_history_key(key)

    def update_exclusive_set(self, ps):
        def exclusive_fnc_(p_cur_):
            for _i_p in ps:
                if _i_p == p_cur_:
                    self.get_node().set(_i_p, True)
                else:
                    self.get_node().set(_i_p, False)

        for i_p in ps:
            i_port = self.get_node().get_port(i_p)
            i_qt_widget = i_port._prx_port_entry._qt_entry_widget
            # use radio icon
            i_qt_widget._set_check_icon_file_paths_(
                gui_core.GuiIcon.get('radio_unchecked'),
                gui_core.GuiIcon.get('radio_checked')
            )
            i_qt_widget.user_check_clicked.connect(
                functools.partial(
                    exclusive_fnc_, i_p
                )
            )

    def set_height(self, h):
        self._prx_port_entry.set_height(h)

    def set_visible(self, boolean):
        if self._main_qt_widget is not None:
            self._main_qt_widget.setVisible(boolean)


# constant
class _PrxPortAsConstant(AbsPrxTypePort):
    ENTRY_TYPE = 'constant'
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    ENTRY_CLS = _gui_prx_wgt_port_entry._PrxEntryAsConstant

    def __init__(self, *args, **kwargs):
        super(_PrxPortAsConstant, self).__init__(*args, **kwargs)

    def set_locked(self, boolean):
        self._prx_port_entry.set_locked(boolean)


#   text
class PrxPortAsText(_PrxPortAsConstant):
    ENTRY_TYPE = 'text'
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsText

    def __init__(self, *args, **kwargs):
        super(PrxPortAsText, self).__init__(*args, **kwargs)


#   string
class PrxPortAsString(_PrxPortAsConstant):
    ENTRY_TYPE = 'string'
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsString, self).__init__(*args, **kwargs)


#   name
class PrxPortAsName(_PrxPortAsConstant):
    ENTRY_TYPE = 'name'
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsName, self).__init__(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_value_entry_validator_use_as_name_()


#   frames
class PrxPortAsFrames(_PrxPortAsConstant):
    ENTRY_TYPE = 'frames'
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFrames, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_use_as_frames()


#   integer
class PrxPortInteger(_PrxPortAsConstant):
    ENTRY_TYPE = 'integer'
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsInteger

    def __init__(self, *args, **kwargs):
        super(PrxPortInteger, self).__init__(*args, **kwargs)


#   boolean
class PrxPortAsBoolean(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = True
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsBoolean

    def __init__(self, *args, **kwargs):
        super(PrxPortAsBoolean, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._prx_port_entry._qt_entry_widget._set_name_text_(text)


#   float
class PrxPortAsFloat(_PrxPortAsConstant):
    ENTRY_TYPE = 'float'
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsFloat

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFloat, self).__init__(*args, **kwargs)


# storage
class _PrxPortAsStorage(_PrxPortAsConstant):
    ENTRY_CLS = _gui_prx_wgt_port_entry._PrxStgObjEntry

    def __init__(self, *args, **kwargs):
        super(_PrxPortAsStorage, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self._prx_port_entry.set_ext_filter(ext_filter)

    def show_history_latest(self):
        self._prx_port_entry.show_history_latest()

    def set_history_key(self, key):
        self._prx_port_entry.set_history_key(key)


#   file open
class PrxPortAsFileOpen(_PrxPortAsStorage):
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryFileOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileOpen, self).__init__(*args, **kwargs)


#   file save
class PrxPortAsFileSave(_PrxPortAsStorage):
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryFileSave

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileSave, self).__init__(*args, **kwargs)


#   directory open
class PrxPortAsDirectoryOpen(_PrxPortAsStorage):
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsDirectoryOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectoryOpen, self).__init__(*args, **kwargs)


#   directory save
class PrxPortAsDirectorySave(_PrxPortAsStorage):
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsDirectorySave

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectorySave, self).__init__(*args, **kwargs)


# resolver
#   project choose
class PrxPortAsRsvProjectChoose(_PrxPortAsConstant):
    ENTRY_CLS = _gui_prx_wgt_port_entry._PrxEntryAsRsvProject

    def __init__(self, *args, **kwargs):
        super(PrxPortAsRsvProjectChoose, self).__init__(*args, **kwargs)

    def get_histories(self):
        return self.entry_widget.get_histories()

    def show_history_latest(self):
        self._prx_port_entry.show_history_latest()


#  scheme choose
class PrxPortAsSchemChoose(_PrxPortAsConstant):
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryForSchemeAsChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsSchemChoose, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_scheme_key(kwargs['scheme_key'])


class PrxPortAsConstantChoose(AbsPrxTypePort):
    ENTRY_TYPE = 'enumerate'
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsConstantChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsConstantChoose, self).__init__(*args, **kwargs)

    def get_enumerate_strings(self):
        return self._prx_port_entry.get_enumerate_strings()

    def set_icon_file_as_value(self, value, file_path):
        self._prx_port_entry.set_icon_file_as_value(value, file_path)


# capsule
class PrxPortAsCapsuleString(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleString, self).__init__(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_capsule_use_exclusive_(
            True
        )


class PrxPortAsCapsuleStrings(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleStrings, self).__init__(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_capsule_use_exclusive_(
            False
        )


class PrxPortAsScript(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsScript

    def __init__(self, *args, **kwargs):
        super(PrxPortAsScript, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsScript, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._value_entry._set_empty_text_(args[0])

    def set_external_editor_ext(self, ext):
        self._prx_port_entry.set_external_editor_ext(ext)


class PrxPortAsTuple(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    ENTRY_CLS = _gui_prx_wgt_port_entry._PrxEntryAsAnyTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortAsTuple, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._prx_port_entry.set_value_type(value_type)

    def set_value_size(self, size):
        self._prx_port_entry.set_value_size(size)


class PrxPortForIntegerTuple(PrxPortAsTuple):
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsIntegerTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForIntegerTuple, self).__init__(*args, **kwargs)


class PrxPortForFloatTuple(PrxPortAsTuple):
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsFloatTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForFloatTuple, self).__init__(*args, **kwargs)


class PrxPortAsRgbaChoose(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsRgbaChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsRgbaChoose, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_use_as_rgba()


class PrxPortAsButton(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsPressButton

    def __init__(self, *args, **kwargs):
        super(PrxPortAsButton, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._prx_port_entry._qt_entry_widget._set_name_text_(text)

    def set_option_enable(self, boolean):
        self._prx_port_entry.set_option_enable(boolean)

    def set_status(self, status):
        self._prx_port_entry._qt_entry_widget._set_status_(status)

    def set_locked(self, boolean):
        self._prx_port_entry._qt_entry_widget._set_action_enable_(not boolean)


class PrxPortAsCheckButton(PrxPortAsButton):
    def __init__(self, *args, **kwargs):
        super(PrxPortAsButton, self).__init__(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_check_action_enable_(True)

    def set_checked(self, boolean):
        self._prx_port_entry._qt_entry_widget._set_checked_(boolean)

    def get_is_checked(self):
        return self._prx_port_entry._qt_entry_widget._get_is_checked_()

    def execute(self):
        self._prx_port_entry._qt_entry_widget._execute_()


class PrxSubProcessPort(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsSubProcessButton

    def __init__(self, *args, **kwargs):
        super(PrxSubProcessPort, self).__init__(*args, **kwargs)
        self.label_widget.widget._set_name_text_('')
        self._prx_port_entry._qt_entry_widget._set_name_text_(
            self.label
        )

        self._is_stopped = False

        self.set_stop_connect_to(
            self.set_stopped
        )

    def set_name(self, text):
        self._prx_port_entry._qt_entry_widget._set_name_text_(text)

    def set_status(self, status):
        widget = self._prx_port_entry._qt_entry_widget
        widget.status_changed.emit(status)

    def set_statuses(self, statuses):
        self._prx_port_entry._qt_entry_widget._set_sub_process_statuses_(statuses)

    def set_initialization(self, count, status=gui_configure.Status.Started):
        self._prx_port_entry._qt_entry_widget._initialization_sub_process_(count, status)

    def restore_all(self):
        self._prx_port_entry._qt_entry_widget._restore_sub_process_()

    def set_status_at(self, index, status):
        widget = self._prx_port_entry._qt_entry_widget
        widget.rate_status_update_at.emit(index, status)

    def set_finished_at(self, index, status):
        widget = self._prx_port_entry._qt_entry_widget
        widget.rate_finished_at.emit(index, status)

    def set_finished_connect_to(self, fnc):
        widget = self._prx_port_entry._qt_entry_widget
        widget._connect_sub_process_finished_to_(fnc)

    def set_stop_connect_to(self, fnc):
        self._prx_port_entry.set_stop_connect_to(fnc)

    def set_stopped(self, boolean=True):
        self._is_stopped = boolean
        # self.restore_all()

    def get_is_stopped(self):
        return self._is_stopped


class PrxValidatorPort(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryValidationButton

    def __init__(self, *args, **kwargs):
        super(PrxValidatorPort, self).__init__(*args, **kwargs)
        self.label_widget.widget._set_name_text_('')
        self._prx_port_entry._qt_entry_widget._set_name_text_(
            self.label
        )

    def set_name(self, text):
        self._prx_port_entry._qt_entry_widget._set_name_text_(text)

    def set_status(self, status):
        self._prx_port_entry._qt_entry_widget._set_status_(status)

    def set_statuses(self, statuses):
        self._prx_port_entry._qt_entry_widget._set_validator_statuses_(statuses)

    def restore_all(self):
        self._prx_port_entry._qt_entry_widget._restore_validator_()

    def set_status_at(self, index, status):
        self._prx_port_entry._qt_entry_widget._set_validator_status_at_(index, status)


class PrxRsvObjChoosePort(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsResolverEntity

    def __init__(self, *args, **kwargs):
        super(PrxRsvObjChoosePort, self).__init__(*args, **kwargs)


# storage array
#   many files open
class PrxPortAsFilesOpen(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsFilesOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFilesOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsFilesOpen, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])
        self._prx_port_entry._qt_entry_widget._value_entry._set_empty_text_(args[0])

    def set_history_visible(self, boolean):
        self._prx_port_entry.set_history_visible(boolean)

    def set_ext_includes(self, *args, **kwargs):
        self._prx_port_entry.set_ext_includes(*args, **kwargs)


#   many directories open
class PrxPortAsDirectoriesOpen(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsDirectoriesOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectoriesOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsDirectoriesOpen, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])
        self._prx_port_entry._qt_entry_widget._value_entry._set_empty_text_(args[0])

    def set_history_visible(self, boolean):
        self._prx_port_entry.set_history_visible(boolean)

    def set_ext_includes(self, *args, **kwargs):
        self._prx_port_entry.set_ext_includes(*args, **kwargs)


#   many medias open
class PrxPortAsMediasOpen(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxMediasOpenEntry

    def __init__(self, *args, **kwargs):
        super(PrxPortAsMediasOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsMediasOpen, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])
        self._prx_port_entry._qt_entry_widget._value_entry._set_empty_text_(args[0])

    def set_ext_filter(self, ext_filter):
        self._prx_port_entry.set_ext_filter(ext_filter)

    def set_ext_includes(self, *args, **kwargs):
        self._prx_port_entry.set_ext_includes(*args, **kwargs)


# icon choose
class PrxPortAsIconChoose(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsIconChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsIconChoose, self).__init__(*args, **kwargs)


# any array
class PrxPortForValueArray(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry._PrxEntryForValueArray

    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArray, self).__init__(*args, **kwargs)

    def append(self, value):
        self._prx_port_entry.append(value)


# any array choose
class PrxPortForValueArrayAsChoose(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry._PrxEntryAsArrayWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def append(self, value):
        self._prx_port_entry.append(value)


# shotgun
class PrxPortAsShotgunEntity(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsShotgunEntityByChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsShotgunEntity, self).__init__(*args, **kwargs)

    def get_stg_entity(self):
        return self._prx_port_entry.get_stg_entity()

    def set_name(self, *args, **kwargs):
        super(PrxPortAsShotgunEntity, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def append(self, value):
        self._prx_port_entry.append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_entry.set_shotgun_entity_kwargs(*args, **kwargs)

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._prx_port_entry.run_as_thread(
            cache_fnc, build_fnc, post_fnc
        )


class PrxPortAsShotgunEntities(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsShotgunEntitiesWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsShotgunEntities, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsShotgunEntities, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])
        self._prx_port_entry._qt_entry_widget._value_entry._set_empty_text_(args[0])

    def append(self, value):
        self._prx_port_entry.append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_entry.set_shotgun_entity_kwargs(*args, **kwargs)

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._prx_port_entry.run_as_thread(
            cache_fnc, build_fnc, post_fnc
        )


class PrxNodeListViewPort(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsNodes

    def __init__(self, *args, **kwargs):
        super(PrxNodeListViewPort, self).__init__(*args, **kwargs)

    def get_all(self):
        return self._prx_port_entry.get_all()

    def set_checked_by_include_paths(self, paths):
        self._prx_port_entry.set_checked_by_include_paths(paths)

    def set_unchecked_by_include_paths(self, paths):
        self._prx_port_entry.set_unchecked_by_include_paths(paths)

    def get_prx_tree(self):
        return self._prx_port_entry._prx_entry_widget


class PrxNodeTreeViewPort(PrxNodeListViewPort):
    def __init__(self, *args, **kwargs):
        super(PrxNodeTreeViewPort, self).__init__(*args, **kwargs)

        self._prx_port_entry.set_view_mode('tree')


class PrxPortAsFileList(AbsPrxTypePort):
    ENABLE_CLS = _gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = _gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLS = _gui_prx_wgt_port_entry.PrxEntryAsFiles

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileList, self).__init__(*args, **kwargs)

    def restore(self):
        self._prx_port_entry.restore()

    def get_all(self, *args, **kwargs):
        return self._prx_port_entry.get_all(*args, **kwargs)

    def set_root(self, path):
        self._prx_port_entry.set_root(path)

    def set_checked_by_include_paths(self, paths):
        self._prx_port_entry.set_checked_by_include_paths(paths)

    def set_unchecked_by_include_paths(self, paths):
        self._prx_port_entry.set_unchecked_by_include_paths(paths)

    def get_prx_tree(self):
        return self._prx_port_entry._prx_entry_widget

    def connect_refresh_action_to(self, fnc):
        self._prx_port_entry.connect_refresh_action_to(fnc)


# file tree
class PrxPortAsFileTree(PrxPortAsFileList):
    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileTree, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_view_mode('tree')


# node
class PrxPortStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PrxPortStack, self).__init__()

    def get_key(self, obj):
        return obj.name


class PrxNodeOld(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLS = PrxPortStack
    LABEL_WIDTH = 160
    PORT_CLS_DICT = dict(
        string=PrxPortAsString,
        interge=PrxPortInteger,
        float=PrxPortAsFloat,
        button=PrxPortAsButton,
        enumerate=PrxPortAsConstantChoose
    )

    @classmethod
    def get_port_cls(cls, type_name):
        return cls.PORT_CLS_DICT[type_name]

    def __init__(self, *args, **kwargs):
        super(PrxNodeOld, self).__init__(*args, **kwargs)
        qt_layout_0 = _gui_qt_wgt_utility.QtHBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        #
        qt_splitter_0 = _gui_qt_wgt_split.QtHSplitter_()
        qt_layout_0.addWidget(qt_splitter_0)
        #
        self._qt_label_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        # self._qt_label_widget.setMaximumWidth(self.LABEL_WIDTH)
        self._name_width = 160
        self._qt_label_widget.setFixedWidth(self._name_width)
        qt_splitter_0.addWidget(self._qt_label_widget)
        self._qt_label_layout = _gui_qt_wgt_utility.QtVBoxLayout(self._qt_label_widget)
        self._qt_label_layout.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        self._qt_label_layout.setContentsMargins(2, 0, 2, 0)
        #
        qt_entry_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
        qt_splitter_0.addWidget(qt_entry_widget)
        self._qt_entry_layout = _gui_qt_wgt_utility.QtVBoxLayout(qt_entry_widget)
        self._qt_entry_layout.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        self._qt_entry_layout.setContentsMargins(2, 0, 2, 0)

        self._port_stack = self.PORT_STACK_CLS()

    def set_folder_add(self, label):
        pass

    def _get_pre_port_args_(self):
        ports = self._port_stack.get_objects()
        if ports:
            pre_port = ports[-1]
            return pre_port._get_is_join_next_(), pre_port
        return False, None

    def add_port(self, port):
        if isinstance(port, AbsPrxTypePort):
            cur_port = port
            pre_port_is_join_next, pre_port = self._get_pre_port_args_()
            cur_port_is_join_next = cur_port._get_is_join_next_()
            #
            cur_port.set_node_widget(self.widget)
            #
            condition = pre_port_is_join_next, cur_port_is_join_next
            if condition == (False, False):
                self._qt_label_layout.addWidget(
                    cur_port.label_widget.widget
                )
                self._qt_entry_layout.addWidget(
                    cur_port._prx_port_entry.widget
                )
                if cur_port.LABEL_HIDED is False:
                    cur_port._prx_port_label.set_show()
            elif condition == (False, True):
                self._qt_label_layout.addWidget(
                    cur_port.label_widget.widget
                )
                #
                enter_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
                self._qt_entry_layout.addWidget(
                    enter_widget
                )
                enter_layout = _gui_qt_wgt_utility.QtHBoxLayout(enter_widget)
                enter_layout.setContentsMargins(0, 0, 0, 0)
                enter_layout.setSpacing(2)
                enter_layout.addWidget(
                    cur_port._prx_port_entry.widget
                )
                cur_port._set_join_layout_(enter_layout)
            elif condition == (True, True):
                enter_layout = pre_port._get_join_layout_()
                enter_layout.addWidget(
                    cur_port._prx_port_entry.widget
                )
                cur_port._set_join_layout_(enter_layout)
            elif condition == (True, False):
                enter_layout = pre_port._get_join_layout_()
                enter_layout.addWidget(
                    cur_port._prx_port_entry.widget
                )
            #
            self._port_stack.set_object_add(cur_port)
            return port
        elif isinstance(port, dict):
            pass

    def get_port(self, port_name):
        return self._port_stack.get_object(port_name)

    def to_dict(self):
        dic = {}
        ports = self._port_stack.get_objects()
        for port in ports:
            key = port.name
            value = port.get()
            dic[key] = value
        return dic

    def set_name_width(self, w):
        self._name_width = w
        self._qt_label_widget.setFixedWidth(self._name_width)


class PrxNodePortGroup(AbsPrxPortBaseDef):
    ENTRY_TYPE = 'group'
    QT_WIDGET_CLS = _gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLS = PrxPortStack

    def __init__(self, path):
        self._set_prx_port_def_init_('group', path)
        #
        self._prx_widget = _gui_prx_wgt_contianer.PrxHToolGroup()
        self._prx_widget.set_height_match_to_minimum()
        self._qt_widget = self._prx_widget.widget
        self._prx_widget.set_name(self._label)
        self._prx_widget.set_expanded(True)
        self._port_layout = self._prx_widget._layout
        self._port_layout.setContentsMargins(8, 0, 0, 0)
        self._port_layout.setSpacing(2)
        #
        self._port_stack = self.PORT_STACK_CLS()
        # default use -1
        self._label_width_maximum = -1

    def get_label(self):
        return self._label

    def set_label(self, text):
        self._prx_widget.set_name(text)

    def set_use_as_root(self):
        self._prx_widget.set_head_visible(False)

    def create_group(self, name):
        if self.get_is_root() is True:
            path = name
        else:
            path = '{}.{}'.format(self._port_path, name)
        #
        group = self.__class__(path)
        group._prx_widget.set_name_font_size(8)
        group._prx_widget.set_name_icon_enable(False)
        group._prx_widget.set_expand_icon_names(
            'qt-style/branch-open', 'qt-style/branch-close'
        )
        group._prx_widget.widget._set_line_draw_enable_(True)
        self._port_layout.addWidget(group._prx_widget._qt_widget)
        self._port_stack.set_object_add(group)
        return group

    def add_child(self, port):
        cur_port = port
        pre_port_is_join_next, pre_port = self._get_pre_child_args_()
        cur_port_is_join_next = cur_port._get_is_join_next_()
        #
        condition = pre_port_is_join_next, cur_port_is_join_next
        if condition == (False, False):
            port_main_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
            self._port_layout.addWidget(port_main_widget)
            cur_port.set_main_widget(port_main_widget)
            cur_port_layout = _gui_qt_wgt_utility.QtHBoxLayout(port_main_widget)
            cur_port_layout.setContentsMargins(0, 0, 0, 0)
            cur_port_layout._set_align_top_()
            cur_port._set_layout_(cur_port_layout)
            #
            cur_key_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
            cur_key_widget.hide()
            cur_port._set_key_widget_(cur_key_widget)
            cur_port_layout.addWidget(cur_key_widget)
            cur_key_layout = _gui_qt_wgt_utility.QtHBoxLayout(cur_key_widget)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_top_()
            # + key
            cur_key_layout.addWidget(cur_port._prx_port_enable._qt_widget)
            cur_key_layout.addWidget(cur_port._prx_port_label._qt_widget)
            # + value
            cur_port_layout.addWidget(cur_port._prx_port_entry._qt_widget)
            if cur_port.KEY_HIDE is False:
                cur_key_widget.show()
            if cur_port.LABEL_HIDED is False:
                cur_port._prx_port_label._qt_widget.show()
                cur_key_widget.show()
        # joint to next
        elif condition == (False, True):
            port_main_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
            self._port_layout.addWidget(port_main_widget)
            cur_port.set_main_widget(port_main_widget)
            cur_port_layout = _gui_qt_wgt_utility.QtHBoxLayout(port_main_widget)
            cur_port_layout.setContentsMargins(0, 0, 0, 0)
            cur_port_layout._set_align_top_()
            cur_port._set_layout_(cur_port_layout)
            cur_key_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
            # cur_key_widget.hide()
            cur_port._set_key_widget_(cur_key_widget)
            cur_port_layout.addWidget(cur_key_widget)
            cur_key_layout = _gui_qt_wgt_utility.QtHBoxLayout(cur_key_widget)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_top_()
            # + key
            cur_key_layout.addWidget(cur_port._prx_port_enable._qt_widget)
            cur_key_layout.addWidget(cur_port._prx_port_label._qt_widget)
            # + value
            cur_port_layout.addWidget(cur_port._prx_port_entry._qt_widget)
            # value
            next_port_widget = _gui_qt_wgt_utility._QtTranslucentWidget()
            cur_port_layout.addWidget(next_port_widget)
            next_port_layout = _gui_qt_wgt_utility.QtHBoxLayout(next_port_widget)
            next_port_layout.setContentsMargins(0, 0, 0, 0)
            next_port_layout.setSpacing(2)

            cur_port.set_sub_name_update()

            cur_port._set_join_layout_(next_port_layout)
            if cur_port.KEY_HIDE is False:
                cur_key_widget.show()
            if cur_port.LABEL_HIDED is False:
                cur_port._prx_port_label._qt_widget.show()
                cur_key_widget.show()
        elif condition == (True, True):
            # hide status and label
            pre_port_layout = pre_port._get_join_layout_()
            pre_port_layout.addWidget(cur_port._prx_port_enable._qt_widget)
            cur_port._prx_port_enable._qt_widget.hide()
            pre_port_layout.addWidget(cur_port._prx_port_label._qt_widget)
            cur_port._prx_port_label._qt_widget.hide()
            cur_port.set_sub_name_update()
            pre_port_layout.addWidget(cur_port._prx_port_entry._qt_widget)
            cur_port._set_join_layout_(pre_port_layout)
        elif condition == (True, False):
            # hide status and label
            pre_port_layout = pre_port._get_join_layout_()
            pre_port_layout.addWidget(cur_port._prx_port_enable._qt_widget)
            cur_port._prx_port_enable._qt_widget.hide()
            pre_port_layout.addWidget(cur_port._prx_port_label._qt_widget)
            cur_port._prx_port_label._qt_widget.hide()
            cur_port.set_sub_name_update()
            pre_port_layout.addWidget(cur_port._prx_port_entry._qt_widget)
        #
        cur_port._prx_port_entry.set_show()
        #
        self._port_stack.set_object_add(cur_port)
        cur_port.set_group(self)
        #
        self.update_children_name_width()
        return port

    def _get_pre_child_args_(self):
        ports = self._port_stack.get_objects()
        if ports:
            pre_port = ports[-1]
            if hasattr(pre_port, '_get_is_join_next_') is True:
                return pre_port._get_is_join_next_(), pre_port
            return False, pre_port
        return False, None

    def get_child(self, name):
        return self._port_stack.get_object(name)

    def generate_children_name_width(self):
        widths = []
        children = self.get_children()
        for i_child in children:
            if i_child.get_category() == 'group':
                continue
            #
            if i_child.KEY_HIDE is False:
                if i_child.LABEL_HIDED is False:
                    i_width = i_child._prx_port_label.get_name_draw_width()+8
                else:
                    i_width = 0
                #
                if i_child.get_use_enable() is True:
                    i_width += 22
                #
                widths.append(i_width)
        if widths:
            return max(widths)
        return 0

    def update_children_name_width(self):
        width = self.generate_children_name_width()
        children = self.get_children()
        for i_child in children:
            if i_child.get_category() == 'group':
                continue
            #
            i_key_widget = i_child._key_widget
            if i_key_widget is not None:
                i_width = width
                if i_child.KEY_HIDE is False:
                    if i_width > 0:
                        if i_child.LABEL_HIDED is False:
                            i_key_widget.setFixedWidth(i_width)
                        else:
                            if i_child.get_use_enable() is True:
                                i_key_widget.setFixedWidth(22)
                            else:
                                i_key_widget.setFixedWidth(0)
                                i_key_widget.hide()
                    else:
                        i_key_widget.setFixedWidth(0)
                        i_key_widget.hide()
                else:
                    i_key_widget.setFixedWidth(0)
                    i_key_widget.hide()

    def set_expanded(self, boolean):
        self._prx_widget.set_expanded(boolean)

    def set_reset(self):
        pass

    def set_visible(self, boolean):
        self._prx_widget.set_visible(boolean)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


class PrxNodePortStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PrxNodePortStack, self).__init__()

    def get_key(self, obj):
        return obj.get_port_path()


class PrxNode(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLS = PrxNodePortStack
    PORT_CLS_DICT = dict(
        string=PrxPortAsString,
        interge=PrxPortInteger,
        float=PrxPortAsFloat,
        button=PrxPortAsButton,
        enumerate=PrxPortAsConstantChoose
    )

    def __init__(self, path, *args, **kwargs):
        super(PrxNode, self).__init__(*args, **kwargs)
        self._path_dag_opt = bsc_core.DccPathDagOpt(path)
        # debug: do not set minimum height
        # self._qt_widget.setMinimumHeight(24)
        #
        qt_layout_0 = _gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)

        self._port_stack = self.PORT_STACK_CLS()
        self._port_switch_stack = self.PORT_STACK_CLS()
        #
        self._prx_port_root = self.create_root_port()
        qt_layout_0.addWidget(self._prx_port_root._prx_widget._qt_widget)

    def get_path(self):
        return self._path_dag_opt.get_path()

    def get_name(self):
        return self._path_dag_opt.get_name()

    name = property(get_name)

    def _get_ports_(self, port_paths):
        return [self._port_stack.get_object(i) for i in port_paths]

    def get_port_paths(self):
        return self._port_stack.get_keys()

    def get_port_root(self):
        return self._prx_port_root

    def add_port(self, port):
        group_port = self.create_group_port(port.get_group_path())
        self.register_port(port)
        return group_port.add_child(port)

    def create_root_port(self):
        group_port = PrxNodePortGroup(
            path=self.get_path()
        )
        group_port._prx_widget.widget._set_line_draw_enable_(True)
        self.register_port(group_port)
        return group_port

    def create_group_port(self, path):
        root = self.get_port_root()
        group_cur = root
        if path:
            names = path.split('.')
            for i_name in names:
                i_group = group_cur.get_child(i_name)
                if i_group is None:
                    i_group = group_cur.create_group(i_name)
                    self.register_port(i_group)
                #
                group_cur = i_group
        return group_cur

    def register_port(self, port):
        port.set_node(self)
        self._port_stack.set_object_add(port)
        #
        if hasattr(port, 'connect_tab_pressed_to'):
            connect_result = port.connect_tab_pressed_to(functools.partial(self.switch_port_fnc, port))
            if connect_result is True:
                self._port_switch_stack.set_object_add(port)

    def switch_port_fnc(self, port):
        maximum = self._port_switch_stack.get_maximum()
        if maximum > 0:
            index_cur = self._port_switch_stack.get_index(port.get_port_path())
            index_next = index_cur+1
            if index_next > maximum:
                index_next = 0
            #
            port = self._port_switch_stack.get_object_at(index_next)
            port.set_focus_in()

    def get_port(self, port_path):
        return self._port_stack.get_object(port_path)

    def get_ports(self, regex=None):
        return self._port_stack.get_objects(regex)

    def to_dict(self):
        dic = {}
        ports = self._port_stack.get_objects()
        for i_port in ports:
            key = i_port.get_port_path()
            if i_port.get_category() not in {'group'}:
                value = i_port.get()
                dic[key] = value
        return dic

    def set_name_width(self, w):
        self._name_width = w
        # self._prx_port_root._qt_label_widget.setFixedWidth(self._name_width)

    def create_ports_by_data(self, configure):
        for k, v in configure.items():
            self.create_port_by_data(k.replace('/', '.'), v)

    def create_port_by_data(self, port_path, option):
        widget_ = option['widget']
        label_ = option.get('label')
        #
        if widget_ in {'group'}:
            group = self.create_group_port(port_path)
            if label_:
                group.set_label(label_)
            #
            expand = option.get('expand') or False
            group.set_expanded(expand)

            collapse = option.get('collapse') or False
            group.set_expanded(not collapse)
            #
            group.set_visible_condition(
                option.get('visible_condition')
            )
            return
        #
        key_ = option.get('key')
        value_ = option.get('value')
        enable_ = option.get('enable')
        tool_tip_ = option.get('tool_tip')
        lock_ = option.get('lock') or False
        #
        join_to_next_ = option.get('join_to_next') or False

        if widget_ in {'string'}:
            port = PrxPortAsString(
                port_path,
                node_widget=self.widget
            )
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'name'}:
            port = PrxPortAsName(
                port_path,
                node_widget=self.widget
            )
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'integer'}:
            port = PrxPortInteger(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'float'}:
            port = PrxPortAsFloat(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'float2'}:
            port = PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(2)
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'float3'}:
            port = PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(3)
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in {'rgb', 'rgba'}:
            port = PrxPortAsRgbaChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in {'boolean'}:
            port = PrxPortAsBoolean(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

        elif widget_ in {'enumerate'}:
            port = PrxPortAsConstantChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            #
            default_ = option.get('current') or option.get('default')
            current_index_ = option.get('current_index') or option.get('default_index')
            if default_ is not None:
                port.set(default_)
                port.set_default(default_)
            elif current_index_ is not None:
                port.set(current_index_)
                port.set_default(current_index_)
            else:
                if value_:
                    port.set(value_[0])
                    port.set_default(value_[0])
                    # port.set(value_[-1])
                    # port.set_default(value_[-1])

        elif widget_ in {'icon'}:
            all_application_icon = option.get('all_application_icon')
            if all_application_icon is True:
                value_ = gui_core.GuiIcon.find_all_keys_at('application')
                value_.insert(0, '')
            all_tool_base_icon = option.get('all_tool_base_icon')
            if all_tool_base_icon is True:
                value_ = gui_core.GuiIcon.find_all_keys_at('tool_style')
                value_.insert(0, '')

            port = PrxPortAsIconChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)

            default_ = option.get('default')
            if default_ is not None:
                port.set(default_)
                port.set_default(default_)

        elif widget_ in {'capsule_string'}:
            port = PrxPortAsCapsuleString(
                port_path,
                node_widget=self.widget
            )
            #
            port.set_option(value_)
            #
            value_default = option.get('current') or option.get('default')
            if value_default is not None:
                port.set(value_default)
                port.set_default(value_default)
            else:
                port.set(value_[-1])
                port.set_default(value_[-1])
            #
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
        #
        elif widget_ in {'capsule_strings'}:
            port = PrxPortAsCapsuleStrings(
                port_path,
                node_widget=self.widget
            )
            #
            port.set_option(value_)
            #
            value_default = option.get('current') or option.get('default')
            if value_default is not None:
                port.set(value_default)
                port.set_default(value_default)
        #
        elif widget_ in {'file'}:
            open_or_save = option.get('open_or_save')
            if open_or_save == 'save':
                port = PrxPortAsFileSave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxPortAsFileOpen(
                    port_path,
                    node_widget=self.widget
                )
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            port.set(value_)
            port.set_default(value_)
            ext_filter = option.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)
            #
            show_history_latest = option.get('show_history_latest')
            if show_history_latest:
                port.show_history_latest()
            #
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
        elif widget_ in {'directory'}:
            open_or_save_ = option.get('open_or_save')
            if open_or_save_ == 'save':
                port = PrxPortAsDirectorySave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxPortAsDirectoryOpen(
                    port_path,
                    node_widget=self.widget
                )
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            port.set(value_)
            port.set_default(value_)
            #
            show_history_latest = option.get('show_history_latest')
            if show_history_latest:
                port.show_history_latest()
        # storage array
        elif widget_ in {'directories'}:
            port = PrxPortAsDirectoriesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            if 'history_visible' in option:
                port.set_history_visible(option['history_visible'])
        elif widget_ in {'files'}:
            port = PrxPortAsFilesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            #
            ext_includes = option.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            if 'history_visible' in option:
                port.set_history_visible(option['history_visible'])
        elif widget_ in {'medias'}:
            port = PrxPortAsMediasOpen(
                port_path,
                node_widget=self.widget
            )
            #
            ext_includes = option.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            ext_filter = option.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
        #
        elif widget_ in {'values'}:
            port = PrxPortForValueArray(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'values_choose'}:
            port = PrxPortForValueArrayAsChoose(
                port_path,
                node_widget=self.widget
            )
            port.set_choose_values(value_)

        elif widget_ in {'shotgun_entity_choose'}:
            port = PrxPortAsShotgunEntity(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = option.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=option.get('keyword_filter_fields'),
                    tag_filter_fields=option.get('tag_filter_fields')
                )
                port.set(value_)

        elif widget_ in {'shotgun_entities_choose'}:
            port = PrxPortAsShotgunEntities(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = option.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=option.get('keyword_filter_fields'),
                    tag_filter_fields=option.get('tag_filter_fields')
                )
                port.set(value_)
        #
        elif widget_ in {'button'}:
            port = PrxPortAsButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            if 'option_enable' in option:
                port.set_option_enable(option['option_enable'])

        elif widget_ in {'check_button'}:
            port = PrxPortAsCheckButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_checked(
                option.get('check', False)
            )

        elif widget_ in {'sub_process_button'}:
            port = PrxSubProcessPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
        elif widget_ in {'validator_button'}:
            port = PrxValidatorPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
        #
        elif widget_ in {'project'}:
            port = PrxPortAsRsvProjectChoose(
                port_path,
                node_widget=self.widget
            )
            if value_:
                port.set(value_)

            show_history_latest = option.get('show_history_latest')
            if show_history_latest:
                port.show_history_latest()
        elif widget_ in {'rsv-obj'}:
            port = PrxRsvObjChoosePort(
                port_path,
                node_widget=self.widget
            )
            # port.set(value_)
        elif widget_ in {'scheme'}:
            port = PrxPortAsSchemChoose(
                port_path,
                scheme_key=option['scheme_key'],
                node_widget=self.widget
            )
            port.set(value_)
        elif widget_ in {'script'}:
            port = PrxPortAsScript(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            if 'external_editor_ext' in option:
                port.set_external_editor_ext(
                    option['external_editor_ext']
                )
        #
        elif widget_ in {'components', 'node_list'}:
            port = PrxNodeListViewPort(
                port_path,
                node_widget=self.widget
            )
        elif widget_ in {'node_tree'}:
            port = PrxNodeTreeViewPort(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'file_list'}:
            port = PrxPortAsFileList(
                port_path,
                node_widget=self.widget
            )
        elif widget_ in {'file_tree'}:
            port = PrxPortAsFileTree(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'frames'}:
            port = PrxPortAsFrames(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        else:
            raise TypeError()
        #
        port.ENTRY_TYPE = widget_
        port.set_key(key_)
        port.set_label(label_)
        port.set_use_enable(enable_)
        port.set_tool_tip(tool_tip_ or '...')
        port.set_join_to_next(join_to_next_)
        port.set_locked(lock_)
        #
        height = option.get('height')
        if height:
            port.set_height(height)

        self.add_port(port)
        # run after add
        port.set_visible_condition(
            option.get('visible_condition')
        )

        if 'exclusive_set' in option:
            port.update_exclusive_set(option['exclusive_set'])

    def set_expanded(self, boolean):
        self._prx_port_root.set_expanded(boolean)

    def set_ports_collapse(self, port_paths):
        for i in port_paths:
            self.get_port(
                i.replace('/', '.')
            ).set_expanded(False)

    def set(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.set(value)
        else:
            log_core.Log.trace_method_warning(
                'port set',
                'port="{}" is non-exists'.format(key)
            )

    def connect_value_changed_to(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.connect_value_changed_to(value)

    def set_default(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.set_default(value)

    def get(self, key):
        port = self.get_port(key)
        if port is not None:
            return port.get()

    def set_reset(self):
        for i in self.get_ports():
            i.set_reset()

    def get_enumerate_strings(self, key):
        port = self.get_port(key)
        if port is not None:
            return port.get_enumerate_strings()
