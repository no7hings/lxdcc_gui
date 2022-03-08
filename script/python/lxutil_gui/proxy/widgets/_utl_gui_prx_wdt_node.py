# coding:utf-8
import types

from lxbasic import bsc_core

from lxobj import obj_abstract
#
from lxutil import utl_core
#
import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil.modifiers as utl_modifiers

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_view


class AttrConfig(object):
    height = 24
    label_width = 64
    ENTRY_HEIGHT = 22


class _PrxPortEnable(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtCheckItem
    def __init__(self, *args, **kwargs):
        super(_PrxPortEnable, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.ENTRY_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.ENTRY_HEIGHT)
        self.widget.setMaximumWidth(AttrConfig.ENTRY_HEIGHT)
        self.widget.setMinimumWidth(AttrConfig.ENTRY_HEIGHT)

    def set(self, boolean):
        self.widget._set_item_checked_(boolean)


# label
class _PrxPortLabel(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtTextItem
    def __init__(self, *args, **kwargs):
        super(_PrxPortLabel, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.ENTRY_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.ENTRY_HEIGHT)

    def set_name(self, text):
        self._qt_widget._set_name_text_(text)

    def set_width(self, w):
        self.widget.setMaximumWidth(w)
        self.widget.setMinimumWidth(w)

    def set_info_tool_tip(self, text):
        pass

    def set_name_tool_tip(self, text):
        self._qt_widget.setToolTip(text)

    def get_name_draw_width(self):
        return self._qt_widget._get_name_draw_width_()


# entry
class AbsTypeEntry(utl_gui_prx_abstract.AbsPrxWidget):
    QT_ENTRY_CLASS = None
    def __init__(self, *args, **kwargs):
        super(AbsTypeEntry, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(AttrConfig.ENTRY_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.ENTRY_HEIGHT)

    def _set_build_(self):
        self._qt_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._entry_widget = self.QT_ENTRY_CLASS()
        self._qt_layout.addWidget(self._entry_widget)
        #
        self._use_as_storage = False

    def set_button_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget.widget)
    @property
    def entry(self):
        return self._entry_widget

    def get(self):
        raise NotImplementedError()

    def set(self, raw=None, **kwargs):
        raise NotImplementedError()

    def set_clear(self):
        pass

    def set_changed_connect_to(self, fnc):
        pass

    def set_use_as_storage(self, boolean=True):
        if hasattr(self.entry, '_set_use_as_storage_'):
            self.entry._set_use_as_storage_(boolean)

    def _set_file_show_(self):
        utl_dcc_objects.OsFile(self.get()).set_open()

    def get_use_as_storage(self):
        return self._use_as_storage


class PrxFileOpenEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.file-paths'
    def __init__(self, *args, **kwargs):
        super(PrxFileOpenEntry, self).__init__(*args, **kwargs)
        #
        self.entry._set_item_entry_enable_(True)
        #
        self._file_open_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._file_open_button)
        self._file_open_button.set_name('Open File')
        self._file_open_button.set_icon_by_name('File')
        self._file_open_button.set_tool_tip(
            [
                '"LMB-click" to open file by "file-dialog"'
            ]
        )
        self._file_open_button.set_press_clicked_connect_to(self._set_file_open_)
        #
        self._ext_filter = 'All File(s) (*.*)'
        #
        self.set_history_update()
        #
        self._entry_widget._set_choose_changed_connect_to_(self.set_history_update)

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def _set_file_open_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        s = f.getOpenFileName(
            self.widget,
            caption='Open File',
            dir=self.get(),
            filter=self._ext_filter
        )
        if s:
            _ = s[0]
            if _:
                self.set(
                    s[0]
                )
                self.set_history_update()

    def get(self):
        return self.entry._get_value_()

    def set(self, raw=None, **kwargs):
        self.entry._set_value_(raw)

    def set_changed_connect_to(self, fnc):
        self.entry._set_item_entry_changed_connect_to_(fnc)
    #
    def set_history_update(self):
        path = self._entry_widget._get_value_()
        if bsc_core.StoragePathOpt(path).get_is_exists() is True:
            utl_core.History.set_append(
                self.HISTORY_KEY,
                path
            )
        #
        histories = utl_core.History.get(
            self.HISTORY_KEY
        )
        if histories:
            histories.reverse()
            #
            self._entry_widget._set_values_(
                histories
            )

    def set_history_show_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._entry_widget._set_value_(_)


class PrxDirectoryOpenEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.directory-paths'
    def __init__(self, *args, **kwargs):
        super(PrxDirectoryOpenEntry, self).__init__(*args, **kwargs)
        #
        self.entry._set_item_entry_enable_(True)
        #
        self._directory_open_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._directory_open_button)
        self._directory_open_button.set_name('Open Directory')
        self._directory_open_button.set_icon_by_name('Directory')
        self._directory_open_button.set_tool_tip(
            [
                '"LMB-click" to open file by "file-dialog"'
            ]
        )
        self._directory_open_button.set_press_clicked_connect_to(self._set_directory_open_)
        #
        self._ext_filter = 'All File(s) (*.*)'
        #
        self.set_history_update()
        #
        self._entry_widget._set_choose_changed_connect_to_(self.set_history_update)

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def _set_directory_open_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        s = f.getExistingDirectory(
            self.widget,
            caption='Open Directory',
            dir=self.get(),
        )
        if s:
            self.set(
                s
            )
            self.set_history_update()

    def get(self):
        return self.entry._get_value_()

    def set(self, raw=None, **kwargs):
        self.entry._set_value_(raw)

    def set_changed_connect_to(self, fnc):
        self.entry._set_item_entry_changed_connect_to_(fnc)
    #
    def set_history_update(self):
        path = self._entry_widget._get_value_()
        if bsc_core.StoragePathOpt(path).get_is_exists() is True:
            utl_core.History.set_append(
                self.HISTORY_KEY,
                path
            )
        #
        histories = utl_core.History.get(
            self.HISTORY_KEY
        )
        if histories:
            histories.reverse()
            #
            self._entry_widget._set_values_(
                histories
            )

    def set_history_show_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._entry_widget._set_value_(_)


class PrxFileSaveEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.file-paths'
    def __init__(self, *args, **kwargs):
        super(PrxFileSaveEntry, self).__init__(*args, **kwargs)
        #
        self.entry._set_item_entry_enable_(True)
        #
        self._file_save_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._file_save_button)
        self._file_save_button.set_name('Save File')
        self._file_save_button.set_icon_by_name('File')
        self._file_save_button.set_tool_tip(
            [
                '"LMB-click" to open file by "file-dialog"'
            ]
        )
        self._file_save_button.set_press_clicked_connect_to(self._set_file_save_)
        #
        self._ext_filter = 'All File(s) (*.*)'
        #
        self.set_history_update()
        #
        self._entry_widget._set_choose_changed_connect_to_(self.set_history_update)

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def _set_file_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        s = f.getSaveFileName(
            self.widget,
            caption='Save File',
            dir=self.get(),
            filter=self._ext_filter
        )
        if s:
            _ = s[0]
            if _:
                self.set(
                    s[0]
                )
                self.set_history_update()

    def get(self):
        return self.entry._get_value_()

    def set(self, raw=None, **kwargs):
        self.entry._set_value_(raw)

    def set_changed_connect_to(self, fnc):
        self.entry._set_item_entry_changed_connect_to_(fnc)
    #
    def set_history_update(self):
        path = self._entry_widget._get_value_()
        if bsc_core.StoragePathOpt(path).get_is_exists() is True:
            utl_core.History.set_append(
                self.HISTORY_KEY,
                path
            )
        #
        histories = utl_core.History.get(
            self.HISTORY_KEY
        )
        if histories:
            histories.reverse()
            #
            self._entry_widget._set_values_(
                histories
            )

    def set_history_show_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._entry_widget._set_value_(_)


class PrxRsvProjectChooseEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.projects'
    def __init__(self, *args, **kwargs):
        super(PrxRsvProjectChooseEntry, self).__init__(*args, **kwargs)
        #
        self.entry._set_item_entry_enable_(True)
        #
        self.set_history_update()
        #
        self._entry_widget._set_item_entry_finished_connect_to_(self.set_history_update)
        self._entry_widget._set_choose_changed_connect_to_(self.set_history_update)

    def get(self):
        return self.entry._get_value_()

    def set(self, raw=None, **kwargs):
        self.entry._set_value_(raw)

    def set_changed_connect_to(self, fnc):
        self.entry._set_item_entry_changed_connect_to_(fnc)
    #
    def set_history_update(self):
        project = self._entry_widget._get_value_()
        if project:
            import lxresolver.commands as rsv_commands
            resolver = rsv_commands.get_resolver()
            #
            rsv_project = resolver.get_rsv_project(project=project)
            project_directory_path = rsv_project.get_directory_path()
            work_directory_path = '{}/work'.format(project_directory_path)
            if bsc_core.StoragePathOpt(work_directory_path).get_is_exists() is True:
                utl_core.History.set_append(
                    self.HISTORY_KEY,
                    project
                )
        #
        histories = utl_core.History.get(
            self.HISTORY_KEY
        )
        if histories:
            histories = [i for i in histories if i]
            histories.reverse()
            #
            self._entry_widget._set_values_(
                histories
            )

    def set_history_show_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._entry_widget._set_value_(_)


class PrxConstantEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtConstantValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxConstantEntry, self).__init__(*args, **kwargs)
        # self.entry.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        #
        self.widget.setFocusProxy(self.entry)

    def set_value_type(self, value_type):
        self.entry._set_value_type_(value_type)

    def get(self):
        return self.entry._get_value_()

    def set(self, raw=None, **kwargs):
        self.entry._set_value_(raw)

    def set_maximum(self, value):
        self.entry._set_value_maximum_(value)

    def get_maximum(self):
        return self.entry._get_value_maximum_()

    def set_minimum(self, value):
        self.entry._set_value_minimum_(value)

    def get_minimum(self):
        return self.entry._get_value_minimum_()

    def set_range(self, maximum, minimum):
        self.entry._set_value_range_(maximum, minimum)

    def get_range(self):
        return self.entry._get_value_range_()


class PrxChooseEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxChooseEntry, self).__init__(*args, **kwargs)
        #
        self.widget.setFocusProxy(self.entry)

    def get(self):
        return self._entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        values = None
        if 'values' in kwargs:
            values = kwargs['values']
            self._entry_widget._set_values_(values)
        #
        if raw is not None:
            self._entry_widget._set_value_(raw)
        else:
            if values:
                self._entry_widget._set_value_(values[-1])


class PrxTextEntry(PrxConstantEntry):
    def __init__(self, *args, **kwargs):
        super(PrxTextEntry, self).__init__(*args, **kwargs)
        self.set_value_type(str)


class PrxStringEntry(PrxConstantEntry):
    def __init__(self, *args, **kwargs):
        super(PrxStringEntry, self).__init__(*args, **kwargs)
        self.set_value_type(str)


class PrxIntegerEntry(PrxConstantEntry):
    def __init__(self, *args, **kwargs):
        super(PrxIntegerEntry, self).__init__(*args, **kwargs)
        self.set_value_type(int)


class PrxFloatEntry(PrxConstantEntry):
    def __init__(self, *args, **kwargs):
        super(PrxFloatEntry, self).__init__(*args, **kwargs)
        self.set_value_type(float)


class PrxArrayEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtArrayValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxArrayEntry, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self.entry._set_value_type_(value_type)

    def set_value_size(self, size):
        self.entry._set_value_size_(size)

    def get(self):
        return self.entry._get_value_()

    def set(self, raw=None, **kwargs):
        self.entry._set_value_(
            raw
        )


class PrxIntegerArrayEntry(PrxArrayEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtArrayValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxArrayEntry, self).__init__(*args, **kwargs)
        self.entry._set_value_entry_build_(2, int)


class PrxBooleanEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtCheckItem
    def __init__(self, *args, **kwargs):
        super(PrxBooleanEntry, self).__init__(*args, **kwargs)

    def get(self):
        return self.entry._get_item_is_checked_()

    def set(self, raw=None, **kwargs):
        self.entry._set_item_checked_(raw)

    def set_changed_connect_to(self, fnc):
        self.entry._set_item_check_changed_connect_to_(fnc)


class PrxEnumerateEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateConstantEntry
    def __init__(self, *args, **kwargs):
        super(PrxEnumerateEntry, self).__init__(*args, **kwargs)
        #
        self.widget.setFocusProxy(self.entry)

    def get(self):
        return self.entry.currentText()

    def get_current(self):
        return self.entry.currentText()

    def set(self, raw=None, **kwargs):
        self.entry.clear()
        if isinstance(raw, (tuple, list)):
            texts = list(raw)
        elif isinstance(raw, (str, unicode)):
            texts = [raw]
        elif isinstance(raw, (int, float)):
            texts = [str(raw)]
        else:
            texts = []
        #
        self.entry.addItems(texts)
        if texts:
            self.entry.setCurrentText(texts[-1])
        #
        self._set_tool_tip_update_()

    def set_current(self, raw):
        if isinstance(raw, (str, unicode)):
            self.entry.setCurrentText(raw)
        elif isinstance(raw, (int, float)):
            self.entry.setCurrentIndex(int(raw))

    def set_append(self, raw):
        if isinstance(raw, (tuple, list)):
            texts = list(raw)
        elif isinstance(raw, (str, unicode)):
            texts = [raw]
        elif isinstance(raw, (int, float)):
            texts = [str(raw)]
        else:
            texts = []
        #
        self.entry.addItems(texts)
        #
        self._set_tool_tip_update_()

    def _set_tool_tip_update_(self):
        tool_tips = []
        texts = [self.entry.itemText(i) for i in range(self.entry.count())]
        if self._use_as_storage is True:
            for i in texts:
                i_file_obj = utl_dcc_objects.OsFile(i)
                if i_file_obj.get_is_exists() is True:
                    i_time = i_file_obj.get_time()
                    i_user = i_file_obj.get_user()
                    tool_tips.append(
                        u'file="{}"; time="{}"; user="{}";'.format(i, i_time, i_user)
                    )
                else:
                    tool_tips.append(
                        u'file="{}"'.format(i)
                    )
        #
        self.widget.setToolTip(
            u'\n'.join(tool_tips)
        )

    def set_clear(self):
        self.entry.clear()

    def set_changed_connect_to(self, fnc):
        self.entry.currentIndexChanged.connect(fnc)


class PrxButtonEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxButtonEntry, self).__init__(*args, **kwargs)

    def get(self):
        return None
    @utl_modifiers.set_method_exception_catch
    def _set_fnc_run_(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self.entry.clicked.connect(
                lambda *args, **kwargs: self._set_fnc_run_(raw)
            )

    def set_menu_raw(self, raw):
        self.entry._set_menu_raw_(raw)


class PrxProcessEntry(AbsTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxProcessEntry, self).__init__(*args, **kwargs)
        self._stop_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._stop_button)
        self._stop_button.set_name('Stop Process')
        self._stop_button.set_icon_by_name('Stop Process')
        self._stop_button.set_tool_tip('press to stop process')

    def get(self):
        return None
    @utl_modifiers.set_method_exception_catch
    def _set_fnc_run_(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self.entry.clicked.connect(
                lambda *args, **kwargs: self._set_fnc_run_(raw)
            )

    def set_menu_raw(self, raw):
        self.entry._set_menu_raw_(raw)

    def set_stop(self, raw):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._stop_button.widget.press_clicked.connect(
                lambda *args, **kwargs: self._set_fnc_run_(raw)
            )


# port
class AbsTypePort(object):
    ENABLE_CLASS = None
    LABEL_CLASS = None
    LABEL_HIDED = False
    ENTRY_CLASS = None

    def __init__(self, name, label=None, enable=None, default_value=None, join_to_next=False):
        self._type = None
        #
        self._path = name
        self._name = self._path.split('.')[-1]
        if label is not None:
            self._label = label
        else:
            self._label = bsc_core.StrUnderlineOpt(self._name).to_prettify(capitalize=False)
        #
        if isinstance(enable, bool):
            self._enable = enable
        #
        self._prx_port_enable = self.ENABLE_CLASS()
        # gui
        self._prx_port_label = self.LABEL_CLASS()
        if self.LABEL_HIDED is False:
            self._prx_port_label.set_name(self._label)
        self._prx_port_label.set_name_tool_tip(
            'path: {}\nname: {}'.format(
                self._path,
                self._name
            )
        )
        #
        self._port_entry = self.ENTRY_CLASS()
        #
        if default_value is not None:
            self._port_entry.set(default_value)
        #
        self._layout = None
        #
        self._is_join_to_next = join_to_next
        self._join_layout = None
        #
        self._custom_widget = None
        #
        self.set_name(self.label)

    def get_type(self):
        return self._type
    type = property(get_type)
    @property
    def name(self):
        return self._name

    def get_path(self):
        return self._path
    path = property(get_path)
    @property
    def label(self):
        return self._label

    @property
    def port_label(self):
        return self._prx_port_label
    @property
    def port_entry(self):
        return self._port_entry

    def set_name(self, name):
        self._prx_port_label.set_name(name)

    def set_enable(self, boolean):
        if boolean is not None:
            if isinstance(boolean, bool):
                self._prx_port_enable.widget.show()
                self._prx_port_enable.set(boolean)
        else:
            self._prx_port_enable.widget.hide()

    def set_name_width(self, w):
        self.port_label.set_width(w)

    def set(self, raw=None, **kwargs):
        self.port_entry.set(raw, **kwargs)

    def set_value(self, *args, **kwargs):
        self.set(*args, **kwargs)

    def set_append(self, raw):
        if hasattr(self.port_entry, 'set_append'):
            self.port_entry.set_append(raw)

    def set_clear(self):
        self.port_entry.set_clear()

    def set_tool_tip(self, text, as_markdown_style=False):
        if text is not None:
            if isinstance(text, (tuple, list)):
                if len(text) > 0:
                    text_ = '\n'.join(('{}'.format(i) for i in text))
                elif len(text) == 1:
                    text_ = text[0]
                else:
                    text_ = ''
            else:
                text_ = unicode(text)
            #
            if as_markdown_style is True:
                import markdown
                html = markdown.markdown(text_)
                self.port_entry.entry.setToolTip(html)
            else:
                html = '<html><body>'
                html += '<h3>{}</h3>'.format(self._label)
                for i in text_.split('\n'):
                    html += '<ul><li>{}</li></ul>'.format(i)
                html += '</body></html>'
                self.port_entry.entry.setToolTip(html)

    def get(self):
        return self.port_entry.get()

    def set_changed_connect_to(self, fnc):
        pass

    def set_use_as_storage(self, boolean=True):
        self._port_entry.set_use_as_storage(boolean)
    #
    def _set_layout_(self, layout):
        self._layout = layout

    def _get_layout_(self):
        return self._layout
    # join to next
    def set_joint_to_next(self, boolean):
        self._is_join_to_next = boolean

    def _get_is_join_next_(self):
        return self._is_join_to_next

    def _set_join_layout_(self, layout):
        self._join_layout = layout

    def _get_join_layout_(self):
        return self._join_layout

    def set_menu_raw(self, raw):
        self.port_entry.set_menu_raw(raw)

    def to_custom_widget(self, label_width=80):
        if self._custom_widget is not None:
            return self._custom_widget
        else:
            widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(widget)
            label = self.port_label
            label.set_width(label_width)
            layout.addWidget(label.widget)
            entry = self.port_entry
            layout.addWidget(entry.widget)
            self._custom_widget = widget
            return self._custom_widget

    def __str__(self):
        return 'port(path="{}")'.format(self.get_path())


class PrxConstantPort(AbsTypePort):
    ENABLE_CLASS = _PrxPortEnable
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxConstantEntry
    def __init__(self, *args, **kwargs):
        super(PrxConstantPort, self).__init__(*args, **kwargs)


class PrxTextPort(PrxConstantPort):
    ENTRY_CLASS = PrxTextEntry
    def __init__(self, *args, **kwargs):
        super(PrxTextPort, self).__init__(*args, **kwargs)


class PrxStringPort(PrxConstantPort):
    ENTRY_CLASS = PrxStringEntry
    def __init__(self, *args, **kwargs):
        super(PrxStringPort, self).__init__(*args, **kwargs)


class PrxIntegerPort(PrxConstantPort):
    ENTRY_CLASS = PrxIntegerEntry
    def __init__(self, *args, **kwargs):
        super(PrxIntegerPort, self).__init__(*args, **kwargs)


class PrxFloatPort(PrxConstantPort):
    ENTRY_CLASS = PrxFloatEntry
    def __init__(self, *args, **kwargs):
        super(PrxFloatPort, self).__init__(*args, **kwargs)


class PrxFileOpenPort(PrxConstantPort):
    ENTRY_CLASS = PrxFileOpenEntry
    def __init__(self, *args, **kwargs):
        super(PrxFileOpenPort, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self.port_entry.set_ext_filter(ext_filter)


class PrxDirectoryOpenPort(PrxConstantPort):
    ENTRY_CLASS = PrxDirectoryOpenEntry
    def __init__(self, *args, **kwargs):
        super(PrxDirectoryOpenPort, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self.port_entry.set_ext_filter(ext_filter)

    def set_changed_connect_to(self, fnc):
        self.port_entry.set_changed_connect_to(fnc)


class PrxFileSavePort(PrxConstantPort):
    ENTRY_CLASS = PrxFileSaveEntry
    def __init__(self, *args, **kwargs):
        super(PrxFileSavePort, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self.port_entry.set_ext_filter(ext_filter)

    def set_changed_connect_to(self, fnc):
        self.port_entry.set_changed_connect_to(fnc)


class PrxRsvProjectChoosePort(PrxConstantPort):
    ENTRY_CLASS = PrxRsvProjectChooseEntry
    def __init__(self, *args, **kwargs):
        super(PrxRsvProjectChoosePort, self).__init__(*args, **kwargs)

    def set_changed_connect_to(self, fnc):
        self.port_entry.set_changed_connect_to(fnc)


class PrxBooleanPort(AbsTypePort):
    ENABLE_CLASS = _PrxPortEnable
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = True
    ENTRY_CLASS = PrxBooleanEntry
    def __init__(self, *args, **kwargs):
        super(PrxBooleanPort, self).__init__(*args, **kwargs)
        self._prx_port_label.set_hide()

    def set_name(self, text):
        self.port_entry.entry._set_name_text_(self.label)


class PrxEnumeratePort(AbsTypePort):
    ENABLE_CLASS = _PrxPortEnable
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxEnumerateEntry
    def __init__(self, *args, **kwargs):
        super(PrxEnumeratePort, self).__init__(*args, **kwargs)

    def set_current(self, raw):
        self.port_entry.set_current(raw)

    def get_current(self):
        return self.port_entry.get_current()

    def set_changed_connect_to(self, fnc):
        self.port_entry.set_changed_connect_to(fnc)


class PrxChoosePort(AbsTypePort):
    ENABLE_CLASS = _PrxPortEnable
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxChooseEntry
    def __init__(self, *args, **kwargs):
        super(PrxChoosePort, self).__init__(*args, **kwargs)


class PrxArrayPort(AbsTypePort):
    ENABLE_CLASS = _PrxPortEnable
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxArrayEntry
    def __init__(self, *args, **kwargs):
        super(PrxArrayPort, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self.port_entry.set_value_type(value_type)

    def set_value_size(self, size):
        self.port_entry.set_value_size(size)

    def set_changed_connect_to(self, fnc):
        self.port_entry.set_changed_connect_to(fnc)


class PrxIntegerArrayPort(PrxArrayPort):
    ENTRY_CLASS = PrxIntegerArrayEntry
    def __init__(self, *args, **kwargs):
        super(PrxIntegerArrayPort, self).__init__(*args, **kwargs)


class PrxButtonPort(AbsTypePort):
    ENABLE_CLASS = _PrxPortEnable
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = True
    ENTRY_CLASS = PrxButtonEntry
    def __init__(self, *args, **kwargs):
        super(PrxButtonPort, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self.port_entry.entry._set_name_text_(text)

    def set_status(self, status):
        self.port_entry.entry._set_status_(status)


class PrxStatusPort(AbsTypePort):
    ENABLE_CLASS = _PrxPortEnable
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxProcessEntry
    def __init__(self, *args, **kwargs):
        super(PrxStatusPort, self).__init__(*args, **kwargs)
        self.port_label.widget._set_name_text_('')
        self.port_entry.entry._set_name_text_(self.label)

    def set_name(self, text):
        self.port_entry.entry._set_name_text_(text)

    def set_status(self, status):
        self.port_entry.entry._set_status_(status)

    def set_element_statuses(self, element_statuses):
        self.port_entry.entry._set_statuses_(element_statuses)


class PrxPortStack(obj_abstract.AbsObjStack):
    def __init__(self):
        super(PrxPortStack, self).__init__()

    def get_key(self, obj):
        return obj.name


class PrxNode(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLASS = PrxPortStack
    LABEL_WIDTH = 160
    PORT_CLASS_DICT = dict(
        string=PrxStringPort,
        interge=PrxIntegerPort,
        float=PrxFloatPort,
        button=PrxButtonPort,
        enumerate=PrxEnumeratePort
    )
    @classmethod
    def get_port_cls(cls, type_name):
        return cls.PORT_CLASS_DICT[type_name]

    def __init__(self, *args, **kwargs):
        super(PrxNode, self).__init__(*args, **kwargs)
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        #
        qt_splitter_0 = _utl_gui_qt_wgt_utility.QtHSplitter()
        qt_layout_0.addWidget(qt_splitter_0)
        #
        self._qt_label_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        # self._qt_label_widget.setMaximumWidth(self.LABEL_WIDTH)
        self._name_width = 160
        self._qt_label_widget.setFixedWidth(self._name_width)
        qt_splitter_0.addWidget(self._qt_label_widget)
        self._qt_label_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_label_widget)
        self._qt_label_layout.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignTop)
        self._qt_label_layout.setContentsMargins(2, 0, 2, 0)
        #
        qt_entry_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        qt_splitter_0.addWidget(qt_entry_widget)
        self._qt_entry_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_entry_widget)
        self._qt_entry_layout.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignTop)
        self._qt_entry_layout.setContentsMargins(2, 0, 2, 0)

        self._port_stack = self.PORT_STACK_CLASS()

    def set_folder_add(self, label):
        pass

    def _get_pre_port_args_(self):
        ports = self._port_stack.get_objects()
        if ports:
            pre_port = ports[-1]
            return pre_port._get_is_join_next_(), pre_port
        return False, None

    def set_port_add(self, port):
        if isinstance(port, AbsTypePort):
            cur_port = port
            pre_port_is_join_next, pre_port = self._get_pre_port_args_()
            cur_port_is_join_next = cur_port._get_is_join_next_()
            #
            condition = pre_port_is_join_next, cur_port_is_join_next
            if condition == (False, False):
                self._qt_label_layout.addWidget(
                    cur_port.port_label.widget
                )
                self._qt_entry_layout.addWidget(
                    cur_port.port_entry.widget
                )
            elif condition == (False, True):
                self._qt_label_layout.addWidget(
                    cur_port.port_label.widget
                )
                #
                enter_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
                self._qt_entry_layout.addWidget(
                    enter_widget
                )
                enter_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(enter_widget)
                enter_layout.setContentsMargins(0, 0, 0, 0)
                enter_layout.setSpacing(2)
                enter_layout.addWidget(
                    cur_port.port_entry.widget
                )
                cur_port._set_join_layout_(enter_layout)
            elif condition == (True, True):
                enter_layout = pre_port._get_join_layout_()
                enter_layout.addWidget(
                    cur_port.port_entry.widget
                )
                cur_port._set_join_layout_(enter_layout)
            elif condition == (True, False):
                enter_layout = pre_port._get_join_layout_()
                enter_layout.addWidget(
                    cur_port.port_entry.widget
                )
            #
            self._port_stack.set_object_add(cur_port)
            return port
        elif isinstance(port, dict):
            pass

    def get_port(self, port_name):
        return self._port_stack.get_object(port_name)

    def get_as_kwargs(self):
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


class PrxGroupPort_(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLASS = PrxPortStack
    #
    def __init__(self, *args, **kwargs):
        super(PrxGroupPort_, self).__init__(*args, **kwargs)
        self._type = 'group'
        self._path = None
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)
        #
        self._prx_expanded_group = _utl_gui_prx_wdt_utility.PrxExpandedGroup()
        qt_layout_0.addWidget(self._prx_expanded_group.widget)
        self._prx_expanded_group.set_expanded(True)
        qt_line = _utl_gui_qt_wgt_utility._QtLine()
        self._prx_expanded_group.set_widget_add(qt_line)
        self._port_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_line)
        self._port_layout.setContentsMargins(4, 0, 0, 0)
        #
        self._port_stack = self.PORT_STACK_CLASS()
        # default use -1
        self._label_width_maximum = -1

    def _set_group_port_init_(self, name, label=None):
        self._path = name
        self._name = self._path.split('.')[-1]
        if label is not None:
            self._label = label
        else:
            self._label = bsc_core.StrUnderlineOpt(name).to_prettify(capitalize=False)
        #
        self._prx_expanded_group.set_name(self._label)

    def get_type(self):
        return self._type
    type = property(get_type)

    def get_path(self):
        return self._path
    path = property(get_path)

    def get_name(self):
        return self._name
    name = property(get_name)

    def get_label(self):
        return self._label

    def set_use_as_root(self):
        self._prx_expanded_group.set_head_visible(False)

    def set_label(self, text):
        self._prx_expanded_group.set_name(text)

    def set_child_group_create(self, name):
        label = bsc_core.StrUnderlineOpt(name).to_prettify(capitalize=False)
        group_port = self.__class__()
        group_port._set_group_port_init_('{}.{}'.format(self._path, name))
        group_port.set_label(label)
        self._port_layout.addWidget(group_port.widget)
        self._port_stack.set_object_add(group_port)
        return group_port

    def set_child_add(self, port):
        cur_port = port
        pre_port_is_join_next, pre_port = self._get_pre_child_args_()
        cur_port_is_join_next = cur_port._get_is_join_next_()
        #
        condition = pre_port_is_join_next, cur_port_is_join_next
        if condition == (False, False):
            widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            self._port_layout.addWidget(widget)
            layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(widget)
            port._set_layout_(layout)
            layout.addWidget(
                cur_port._prx_port_enable.widget
            )
            layout.addWidget(
                cur_port._prx_port_label.widget
            )
            layout.addWidget(
                cur_port.port_entry.widget
            )
        elif condition == (False, True):
            widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            self._port_layout.addWidget(widget)
            layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(widget)
            port._set_layout_(layout)
            layout.addWidget(
                cur_port._prx_port_enable.widget
            )
            layout.addWidget(
                cur_port._prx_port_label.widget
            )
            #
            enter_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            layout.addWidget(
                enter_widget
            )
            enter_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(enter_widget)
            enter_layout.setContentsMargins(0, 0, 0, 0)
            enter_layout.setSpacing(2)
            enter_layout.addWidget(
                cur_port.port_entry.widget
            )
            cur_port._set_join_layout_(enter_layout)
        elif condition == (True, True):
            enter_layout = pre_port._get_join_layout_()
            enter_layout.addWidget(
                cur_port.port_entry.widget
            )
            cur_port._set_join_layout_(enter_layout)
        elif condition == (True, False):
            enter_layout = pre_port._get_join_layout_()
            enter_layout.addWidget(
                cur_port.port_entry.widget
            )
        #
        self._port_stack.set_object_add(cur_port)
        self.set_label_width_update()
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

    def get_children(self):
        return self._port_stack.get_objects()

    def get_label_width_maximum(self):
        widths = []
        children = self.get_children()
        for i_child in children:
            if i_child.get_type() == 'group':
                pass
            else:
                i_width = i_child._prx_port_label.get_name_draw_width()
                widths.append(i_width)
        if widths:
            return max(widths)
        return 0

    def set_label_width_update(self):
        width = self.get_label_width_maximum()
        children = self.get_children()
        for i_child in children:
            if i_child.get_type() == 'group':
                pass
            else:
                if width > 0:
                    i_child._prx_port_label._qt_widget.setFixedWidth(width + 8)
                else:
                    i_child._prx_port_label.set_hide()

    def __str__(self):
        return '{}(path="{}")'.format(
            'group', self.get_path()
        )


class PrxNodePortStack_(obj_abstract.AbsObjStack):
    def __init__(self):
        super(PrxNodePortStack_, self).__init__()

    def get_key(self, obj):
        return obj.path


class PrxNode_(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLASS = PrxNodePortStack_
    LABEL_WIDTH = 160
    PORT_CLASS_DICT = dict(
        string=PrxStringPort,
        interge=PrxIntegerPort,
        float=PrxFloatPort,
        button=PrxButtonPort,
        enumerate=PrxEnumeratePort
    )
    def __init__(self, *args, **kwargs):
        super(PrxNode_, self).__init__(*args, **kwargs)
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)

        qt_scroll_area = _utl_gui_qt_wgt_utility.QtScrollArea()
        qt_layout_0.addWidget(qt_scroll_area)
        self._prx_port_root = PrxGroupPort_()
        self._prx_port_root._set_group_port_init_('root')
        self._prx_port_root.set_use_as_root()
        qt_scroll_area._layout.addWidget(self._prx_port_root.widget)
        self._port_stack = self.PORT_STACK_CLASS()

    def get_port_root(self):
        return self._prx_port_root

    def set_port_add(self, port):
        root_port = self.get_port_root()

        port_path = port.get_path()
        _ = port_path.split('.')
        group_names = _[:-1]

        current_group_port = root_port
        for i_group_name in group_names:
            i_group_port = current_group_port.get_child(i_group_name)
            if i_group_port is None:
                i_group_port = current_group_port.set_child_group_create(i_group_name)

            current_group_port = i_group_port

        group_port = current_group_port
        #
        self._port_stack.set_object_add(port)
        return group_port.set_child_add(port)

    def get_port(self, port_path):
        return self._port_stack.get_object(port_path)

    def get_as_kwargs(self):
        dic = {}
        ports = self._port_stack.get_objects()
        for port in ports:
            key = port.get_path()
            value = port.get()
            dic[key] = value
        return dic

    def set_name_width(self, w):
        self._name_width = w
        self._prx_port_root._qt_label_widget.setFixedWidth(self._name_width)

    def set_ports_create_by_configure(self, configure):
        for k, v in configure.items():
            self.set_port_create_by_option(k.replace('/', '.'), v)

    def set_port_create_by_option(self, port_path, option):
        widget_ = option['widget']
        value_ = option['value']
        enable_ = option.get('enable')
        tool_tip_ = option['tool_tip']
        #
        join_to_next_ = option.get('joint_to_next') or False

        if widget_ in ['string']:
            port = PrxStringPort(port_path)
            port.set(value_)
        elif widget_ in ['integer']:
            port = PrxIntegerPort(port_path)
            port.set(value_)
        elif widget_ in ['float']:
            port = PrxFloatPort(port_path)
            port.set(value_)
        elif widget_ in ['file']:
            port = PrxFileOpenPort(port_path)
            port.set(value_)
        elif widget_ in ['boolean']:
            port = PrxBooleanPort(port_path)
            port.set(value_)
        elif widget_ in ['button']:
            port = PrxButtonPort(port_path)
            port.set(value_)
        elif widget_ in ['enumerate']:
            port = PrxEnumeratePort(port_path)
            port.set(value_)
        elif widget_ in ['project']:
            port = PrxRsvProjectChoosePort(port_path)
            port.set(value_)
        else:
            raise TypeError()

        port.set_enable(enable_)
        port.set_tool_tip(tool_tip_)
        port.set_joint_to_next(join_to_next_)

        self.set_port_add(port)


