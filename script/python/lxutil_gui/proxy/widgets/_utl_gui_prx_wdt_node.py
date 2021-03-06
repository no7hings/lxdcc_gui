# coding:utf-8
import functools

import types

from lxbasic import bsc_core

from lxobj import obj_abstract
#
from lxutil import utl_core
#
import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil.modifiers as utl_modifiers

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_view

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui import utl_gui_core

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_view


class AttrConfig(object):
    height = 24
    label_width = 64
    PRX_PORT_HEIGHT = 22


class _PrxPortInfo(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtIconPressItem

    def __init__(self, *args, **kwargs):
        super(_PrxPortInfo, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMaximumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setToolTip(
            '"LMB-click" to use value "default" / "latest"'
        )

    def set(self, boolean):
        self.widget._set_item_checked_(boolean)


class _PrxPortStatus(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtStatusItem
    def __init__(self, *args, **kwargs):
        super(_PrxPortStatus, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMaximumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setToolTip(
            '"LMB-click" to use value "default" / "latest"'
        )

    def set(self, boolean):
        self.widget._set_item_checked_(boolean)


# label
class _PrxPortLabel(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtTextItem
    def __init__(self, *args, **kwargs):
        super(_PrxPortLabel, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)

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
        return self._qt_widget._get_name_text_draw_width_()


# entry
class AbsRsvTypeQtEntry(utl_gui_prx_abstract.AbsPrxWidget):
    QT_ENTRY_CLASS = None
    def __init__(self, *args, **kwargs):
        super(AbsRsvTypeQtEntry, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)

    def _set_build_(self):
        self._qt_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._qt_entry_widget = self.QT_ENTRY_CLASS()
        self._qt_layout.addWidget(self._qt_entry_widget)
        #
        self._use_as_storage = False

    def set_button_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, raw=None, **kwargs):
        raise NotImplementedError()

    def set_default(self, raw, **kwargs):
        pass

    def get_default(self):
        pass

    def get_is_default(self):
        return False

    def set_clear(self):
        pass

    def set_changed_connect_to(self, fnc):
        pass

    def set_use_as_storage(self, boolean=True):
        if hasattr(self._qt_entry_widget, '_set_use_as_storage_'):
            self._qt_entry_widget._set_use_as_storage_(boolean)

    def _set_file_show_(self):
        utl_dcc_objects.OsFile(self.get()).set_open()

    def get_use_as_storage(self):
        return self._use_as_storage


class PrxFileOpenEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.file-open'
    def __init__(self, *args, **kwargs):
        super(PrxFileOpenEntry, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_item_entry_enable_(True)
        #
        self._file_open_or_save_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._file_open_or_save_button)
        self._file_open_or_save_button.set_name('open file')
        self._file_open_or_save_button.set_icon_name('file/file')
        self._file_open_or_save_button.set_tool_tip(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )
        self._file_open_or_save_button.set_press_clicked_connect_to(self._set_file_open_or_save_)
        #
        self._ext_filter = 'All File(s) (*.*)'
        #
        self.set_history_update()
        #
        self._qt_entry_widget._set_item_choose_changed_connect_to_(self.set_history_update)

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def _set_file_open_or_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getOpenFileName(
            self.widget,
            'Open File',
            self.get(),
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
        return self._qt_entry_widget._get_item_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_item_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_entry_changed_connect_to_(fnc)
    #
    def set_history_update(self):
        path = self._qt_entry_widget._get_item_value_()
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
            self._qt_entry_widget._set_item_values_(
                histories
            )

    def set_show_history_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._qt_entry_widget._set_item_value_(_)


class PrxFileSaveEntry(PrxFileOpenEntry):
    HISTORY_KEY = 'gui.file-save'
    def __init__(self, *args, **kwargs):
        super(PrxFileSaveEntry, self).__init__(*args, **kwargs)
        self._file_open_or_save_button.set_name('save file')
        self._file_open_or_save_button.set_tool_tip(
            [
                '"LMB-click" to save file by "dialog"'
            ]
        )


class PrxDirectoryOpenEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.directory-open'
    def __init__(self, *args, **kwargs):
        super(PrxDirectoryOpenEntry, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_item_entry_enable_(True)
        #
        self._open_or_save_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._open_or_save_button)
        self._open_or_save_button.set_name('open directory')
        self._open_or_save_button.set_icon_name('file/folder')
        self._open_or_save_button.set_tool_tip(
            [
                '"LMB-click" to open directory by "dialog"'
            ]
        )
        self._open_or_save_button.set_press_clicked_connect_to(self._set_directory_open_or_save_)
        #
        self._ext_filter = 'All File(s) (*.*)'
        #
        self.set_history_update()
        #
        self._qt_entry_widget._set_item_choose_changed_connect_to_(self.set_history_update)

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def _set_directory_open_or_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Open Directory',
            self.get(),
        )
        if s:
            self.set(
                s
            )
            self.set_history_update()

    def get(self):
        return self._qt_entry_widget._get_item_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_item_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_entry_changed_connect_to_(fnc)
    #
    def set_history_update(self):
        path = self._qt_entry_widget._get_item_value_()
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
            self._qt_entry_widget._set_item_values_(
                histories
            )

    def set_show_history_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._qt_entry_widget._set_item_value_(_)


class PrxDirectorySaveEntry(PrxDirectoryOpenEntry):
    HISTORY_KEY = 'gui.directory-save'
    def __init__(self, *args, **kwargs):
        super(PrxDirectorySaveEntry, self).__init__(*args, **kwargs)
        self._open_or_save_button.set_name('save directory')
        self._open_or_save_button.set_tool_tip(
            [
                '"LMB-click" to save directory by "dialog"'
            ]
        )

    def _set_directory_open_or_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Save Directory',
            self.get(),
        )
        if s:
            self.set(
                s
            )
            self.set_history_update()


class PrxRsvProjectChooseEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.projects'
    def __init__(self, *args, **kwargs):
        super(PrxRsvProjectChooseEntry, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_item_entry_enable_(True)
        #
        self.set_history_update()
        #
        self._qt_entry_widget._set_item_entry_finished_connect_to_(self.set_history_update)
        self._qt_entry_widget._set_item_choose_changed_connect_to_(self.set_history_update)

    def get(self):
        return self._qt_entry_widget._get_item_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_item_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_entry_changed_connect_to_(fnc)
    #
    def set_history_update(self):
        project = self._qt_entry_widget._get_item_value_()
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
            self._qt_entry_widget._set_item_values_(
                histories
            )

    def set_show_history_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._qt_entry_widget._set_item_value_(_)

    def get_histories(self):
        return utl_core.History.get(
            self.HISTORY_KEY
        )


class PrxSchemeChooseEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    #
    HISTORY_KEY = 'gui.schemes'
    def __init__(self, *args, **kwargs):
        super(PrxSchemeChooseEntry, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_item_entry_enable_(True)
        #
        self._scheme_key = None
        #
        self.set_history_update()
        #
        self._qt_entry_widget._set_item_entry_finished_connect_to_(self.set_history_update)
        self._qt_entry_widget._set_item_choose_changed_connect_to_(self.set_history_update)

    def get(self):
        return self._qt_entry_widget._get_item_value_()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.set_history_add(raw[0])
            self.set_history_update()
            self.set_show_history_latest()

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()

    def set_scheme_key(self, key):
        self._scheme_key = key

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_entry_changed_connect_to_(fnc)
    #
    def get_histories(self):
        if self._scheme_key is not None:
            return utl_core.History.get(
                self._scheme_key
            )
        return []

    def set_history_add(self, scheme):
        if self._scheme_key is not None:
            utl_core.History.set_append(
                self._scheme_key,
                scheme
            )
    #
    def set_history_update(self):
        if self._scheme_key is not None:
            scheme = self._qt_entry_widget._get_item_value_()
            if scheme:
                utl_core.History.set_append(
                    self._scheme_key,
                    scheme
                )
            #
            histories = utl_core.History.get(
                self._scheme_key
            )
            if histories:
                histories = [i for i in histories if i]
                histories.reverse()
                #
                self._qt_entry_widget._set_item_values_(
                    histories
                )

    def set_show_history_latest(self):
        if self._scheme_key is not None:
            _ = utl_core.History.get_latest(self._scheme_key)
            if _:
                self._qt_entry_widget._set_item_value_(_)


class PrxConstantEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtConstantValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxConstantEntry, self).__init__(*args, **kwargs)
        # self._qt_entry_widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        #
        self.widget.setFocusProxy(self._qt_entry_widget)

    def set_value_type(self, value_type):
        self._qt_entry_widget._set_item_value_type_(value_type)

    def set_use_as_frames(self):
        self._qt_entry_widget._set_use_as_frames_()

    def set_use_as_rgba(self):
        self._qt_entry_widget._set_use_as_rgba_()

    def get(self):
        return self._qt_entry_widget._get_item_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_item_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_default(self):
        return self._qt_entry_widget._get_item_value_default_()

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_entry_changed_connect_to_(fnc)

    def set_maximum(self, value):
        self._qt_entry_widget._set_value_maximum_(value)

    def get_maximum(self):
        return self._qt_entry_widget._get_value_maximum_()

    def set_minimum(self, value):
        self._qt_entry_widget._set_value_minimum_(value)

    def get_minimum(self):
        return self._qt_entry_widget._get_value_minimum_()

    def set_range(self, maximum, minimum):
        self._qt_entry_widget._set_value_range_(maximum, minimum)

    def get_range(self):
        return self._qt_entry_widget._get_value_range_()


class PrxChooseEntry_(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxChooseEntry_, self).__init__(*args, **kwargs)
        #
        self.widget.setFocusProxy(self._qt_entry_widget)

    def get(self):
        return self._qt_entry_widget._get_item_value_()

    def get_enumerate_strings(self):
        return self._qt_entry_widget._get_item_values_()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self._qt_entry_widget._set_item_values_(raw)
            if raw:
                self._qt_entry_widget._set_item_value_(raw[-1])
        elif isinstance(raw, (str, unicode)):
            self._qt_entry_widget._set_item_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_default(self):
        return self._qt_entry_widget._get_item_value_default_()

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_choose_changed_connect_to_(fnc)


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


class PrxArrayEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtArrayValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxArrayEntry, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._qt_entry_widget._set_item_value_type_(value_type)

    def set_value_size(self, size):
        self._qt_entry_widget._set_value_size_(size)

    def get(self):
        return self._qt_entry_widget._get_item_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_item_value_(
            raw
        )

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()
    
    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_entry_changed_connect_to_(fnc)


class PrxIntegerArrayEntry(PrxArrayEntry):
    def __init__(self, *args, **kwargs):
        super(PrxIntegerArrayEntry, self).__init__(*args, **kwargs)
        self._qt_entry_widget._set_item_value_entry_build_(2, int)


class PrxFloatArrayEntry(PrxArrayEntry):
    def __init__(self, *args, **kwargs):
        super(PrxFloatArrayEntry, self).__init__(*args, **kwargs)
        self._qt_entry_widget._set_item_value_entry_build_(2, float)


class PrxRgbaEntry(PrxConstantEntry):
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtRgbaValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxRgbaEntry, self).__init__(*args, **kwargs)
        # self._qt_entry_widget._set_item_value_entry_build_(3, float)


class PrxBooleanEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtCheckItem
    def __init__(self, *args, **kwargs):
        super(PrxBooleanEntry, self).__init__(*args, **kwargs)

    def get(self):
        return self._qt_entry_widget._get_item_is_checked_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_item_checked_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_default(self):
        return self._qt_entry_widget._get_item_value_default_()

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget._set_item_check_changed_connect_to_(fnc)


class PrxScriptEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtScriptValueEntryItem
    def __init__(self, *args, **kwargs):
        super(PrxScriptEntry, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(80)
        self.widget.setMinimumHeight(80)
        self._qt_entry_widget._set_item_value_entry_enable_(True)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()

    def get(self):
        return self._qt_entry_widget._get_item_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_item_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_item_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_item_value_is_default_()


class PrxEnumerateEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtEnumerateConstantEntry
    def __init__(self, *args, **kwargs):
        super(PrxEnumerateEntry, self).__init__(*args, **kwargs)
        #
        self.widget.setFocusProxy(self._qt_entry_widget)

    def get(self):
        return self._qt_entry_widget.currentText()

    def get_enumerate_strings(self):
        return

    def get_current(self):
        return self._qt_entry_widget.currentText()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget.clear()
        if isinstance(raw, (tuple, list)):
            texts = list(raw)
        elif isinstance(raw, (str, unicode)):
            texts = [raw]
        elif isinstance(raw, (int, float)):
            texts = [str(raw)]
        else:
            texts = []
        #
        self._qt_entry_widget.addItems(texts)
        if texts:
            self._qt_entry_widget.setCurrentText(texts[-1])
        #
        self._set_tool_tip_update_()

    def set_current(self, raw):
        if isinstance(raw, (str, unicode)):
            self._qt_entry_widget.setCurrentText(raw)
        elif isinstance(raw, (int, float)):
            self._qt_entry_widget.setCurrentIndex(int(raw))

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
        self._qt_entry_widget.addItems(texts)
        #
        self._set_tool_tip_update_()

    def _set_tool_tip_update_(self):
        tool_tips = []
        texts = [self._qt_entry_widget.itemText(i) for i in range(self._qt_entry_widget.count())]
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
        self._qt_entry_widget.clear()

    def set_changed_connect_to(self, fnc):
        self._qt_entry_widget.currentIndexChanged.connect(fnc)


class PrxButtonEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxButtonEntry, self).__init__(*args, **kwargs)

    def get(self):
        return None
    @utl_modifiers.set_method_exception_catch
    def _set_fnc_debug_run_(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_entry_widget.clicked.connect(
                lambda *args, **kwargs: self._set_fnc_debug_run_(raw)
            )

    def set_menu_raw(self, raw):
        self._qt_entry_widget._set_menu_raw_(raw)


class PrxProcessEntry(AbsRsvTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item._QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxProcessEntry, self).__init__(*args, **kwargs)
        self._stop_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._stop_button)
        self._stop_button.set_name('Stop Process')
        self._stop_button.set_icon_by_name_text('Stop Process')
        self._stop_button.set_tool_tip('press to stop process')

    def get(self):
        return None
    @utl_modifiers.set_method_exception_catch
    def _set_fnc_debug_run_(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_entry_widget.clicked.connect(
                lambda *args, **_kwargs: self._set_fnc_debug_run_(raw)
            )

    def set_menu_raw(self, raw):
        self._qt_entry_widget._set_menu_raw_(raw)

    def set_stop(self, raw):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._stop_button.widget.press_clicked.connect(
                lambda *args, **kwargs: self._set_fnc_debug_run_(raw)
            )

    def set_stop_connect_to(self, fnc):
        self._stop_button.widget.press_clicked.connect(
            lambda *args, **kwargs: self._set_fnc_debug_run_(fnc)
        )


class AbsRsvTypeEntry(utl_gui_prx_abstract.AbsPrxWidget):
    PRX_ENTRY_CLASS = None
    def __init__(self, *args, **kwargs):
        super(AbsRsvTypeEntry, self).__init__(*args, **kwargs)

    def _set_build_(self):
        self._qt_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._prx_entry_widget = self.PRX_ENTRY_CLASS()
        self._qt_layout.addWidget(self._prx_entry_widget.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, raw=None, **kwargs):
        raise NotImplementedError()

    def set_default(self, raw=None, **kwargs):
        pass

    def get_is_default(self):
        return False

    def set_clear(self):
        pass

    def set_changed_connect_to(self, fnc):
        pass


class PrxRsvObjChooseEntry(AbsRsvTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLASS = _utl_gui_prx_wgt_view.PrxTreeView
    NAMESPACE = 'resolver'
    def __init__(self, *args, **kwargs):
        super(PrxRsvObjChooseEntry, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(160)
        self.widget.setMinimumHeight(160)
        self._prx_entry_widget.set_header_view_create(
            [('name', 2), ('update', 1)],
            180
        )
        self._prx_entry_widget.set_single_selection()
        self._prx_entry_widget.set_size_policy_height_fixed_mode()
        self._obj_add_dict = {}

    def __set_item_comp_add_as_tree_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._obj_add_dict:
            prx_item = self._obj_add_dict[obj_path]
            return False, prx_item, None
        else:
            create_kwargs = dict(
                name='loading ...',
                icon_name_text=obj_type,
                filter_key=obj_path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._obj_add_dict[parent.path]
                prx_item = prx_item_parent.set_child_add(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_entry_widget.set_item_add(
                    **create_kwargs
                )
            # prx_item.set_checked(True)
            prx_item.set_keyword_filter_tgt_contexts([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._obj_add_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_method(
                    lambda *args, **kwargs: self.__set_item_show_deferred_(prx_item)
                )
                return True, prx_item, None
            else:
                self.__set_item_show_deferred_(prx_item)
                return True, prx_item, None

    def __set_item_show_deferred_(self, prx_item, use_as_tree=True):
        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        obj_type_name = obj.type_name
        obj_name = obj.name
        obj_path = obj.path
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        if use_as_tree is True:
            menu_raw.extend(
                [
                    ('expanded',),
                    ('Expand branch', None, prx_item.set_expand_branch),
                    ('Collapse branch', None, prx_item.set_collapse_branch),
                ]
            )
        #
        result = obj.get('result')
        update = obj.get('update')
        prx_item.set_icon_by_name_text(obj_type_name)
        prx_item.set_names([obj_name, update])
        prx_item.set_tool_tip(obj.description)
        if result:
            if bsc_core.StoragePathOpt(result).get_is_file():
                prx_item.set_icon_by_file(utl_dcc_objects.OsFile(result).icon)
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def __set_item_add_as_tree_(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._obj_add_dict:
                    self.__set_item_comp_add_as_tree_(i_rsv_obj, use_show_thread=True)
        #
        self.__set_item_comp_add_as_tree_(obj, use_show_thread=True)

    def __set_item_add_as_list_(self, obj):
        obj_path = obj.path
        obj_type = obj.type
        #
        create_kwargs = dict(
            name='...',
            filter_key=obj_path
        )
        prx_item = self._prx_entry_widget.set_item_add(
            **create_kwargs
        )
        # prx_item.set_checked(True)
        prx_item.set_keyword_filter_tgt_contexts([obj_path, obj_type])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._obj_add_dict[obj_path] = prx_item
        #
        prx_item.set_show_method(
            functools.partial(
                self.__set_item_show_deferred_, prx_item, False
            )
        )

    def __set_item_selected_(self, obj):
        item = obj.get_obj_gui()
        self._prx_entry_widget.set_item_selected(
            item, exclusive=True
        )

    def __set_item_clear_(self):
        self._prx_entry_widget.set_clear()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__set_item_clear_()
            objs = raw
            if objs:
                for i in objs:
                    self.__set_item_add_as_list_(i)
                #
                self.__set_item_selected_(
                    objs[-1]
                )
        else:
            pass

    def get(self):
        _ = self._prx_entry_widget.get_current_item()
        if _:
            return _.get_gui_dcc_obj(namespace=self.NAMESPACE)

    def set_changed_connect_to(self, fnc):
        self._prx_entry_widget.set_item_select_changed_connect_to(
            fnc
        )


class PrxComponentsEntry(AbsRsvTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLASS = _utl_gui_prx_wgt_view.PrxTreeView
    NAMESPACE = 'resolver'
    def __init__(self, *args, **kwargs):
        super(PrxComponentsEntry, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(160)
        self.widget.setMinimumHeight(160)
        self._prx_entry_widget.set_header_view_create(
            [('name', 1)],
            320
        )
        self._prx_entry_widget.set_single_selection()
        self._prx_entry_widget.set_size_policy_height_fixed_mode()
        self._obj_add_dict = {}

    def __set_item_comp_add_as_tree_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._obj_add_dict:
            prx_item = self._obj_add_dict[obj_path]
            return False, prx_item, None
        else:
            create_kwargs = dict(
                name='loading ...',
                icon_name_text=obj_type,
                filter_key=obj_path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._obj_add_dict[parent.path]
                prx_item = prx_item_parent.set_child_add(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_entry_widget.set_item_add(
                    **create_kwargs
                )
            prx_item.set_checked(True)
            prx_item.set_keyword_filter_tgt_contexts([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._obj_add_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_method(
                    lambda *args, **kwargs: self.__set_item_show_deferred_(prx_item)
                )
                return True, prx_item, None
            else:
                self.__set_item_show_deferred_(prx_item)
                return True, prx_item, None

    def __set_item_show_deferred_(self, prx_item, use_as_tree=True):
        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        obj_name = obj.name
        obj_path = obj.path
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        if use_as_tree is True:
            menu_raw.extend(
                [
                    ('expanded',),
                    ('Expand branch', None, prx_item.set_expand_branch),
                    ('Collapse branch', None, prx_item.set_collapse_branch),
                ]
            )
        #
        prx_item.set_names([obj_name])
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        # self._prx_entry_widget.set_loading_update()
    #
    def __set_item_add_as_tree_(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._obj_add_dict:
                    self.__set_item_comp_add_as_tree_(i_rsv_obj, use_show_thread=True)
        #
        self.__set_item_comp_add_as_tree_(obj, use_show_thread=True)

    def __set_item_add_as_list_(self, obj):
        obj_path = obj.path
        obj_type = obj.type_name
        #
        create_kwargs = dict(
            name='...',
            icon_name_text=obj_type,
            filter_key=obj_path
        )
        prx_item = self._prx_entry_widget.set_item_add(
            **create_kwargs
        )
        #
        prx_item.set_checked(True)
        prx_item.set_keyword_filter_tgt_contexts([obj_path, obj_type])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._obj_add_dict[obj_path] = prx_item
        #
        self.__set_item_show_deferred_(prx_item, use_as_tree=False)

    def __set_item_selected_(self, obj):
        item = obj.get_obj_gui()
        self._prx_entry_widget.set_item_selected(
            item, exclusive=True
        )

    def __set_item_clear_(self):
        self._prx_entry_widget.set_clear()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__set_item_clear_()
            objs = raw
            if objs:
                for i in objs:
                    self.__set_item_add_as_list_(i)
                #
                self.__set_item_selected_(
                    objs[-1]
                )
        else:
            pass

    def get(self):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE) for i in _ if i.get_is_checked()]
        return []

    def set_changed_connect_to(self, fnc):
        self._prx_entry_widget.set_item_select_changed_connect_to(
            fnc
        )


# port =============================================================================================================== #
class AbsPrxPortDef(object):
    def _set_prx_port_def_init_(self, type_, path, label=None):
        self._prx_node = None
        #
        self._type = type_
        self._port_path = path
        self._name = self._port_path.split('.')[-1]
        #
        if label is not None:
            self._label = label
        else:
            self._label = bsc_core.StrUnderlineOpt(self._name).to_prettify(capitalize=False)

    def _set_node_(self, obj):
        self._prx_node = obj

    def get_node(self):
        return self._prx_node

    def get_node_path(self):
        return self.get_node().get_path()

    def get_type(self):
        return self._type
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
            _ = bsc_core.DccPathDagMtd.get_dag_children(
                port_path, port_paths, pathsep='.'
            )
        return node._get_ports_(_)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


# port
class AbsPrxTypePort(AbsPrxPortDef):
    ENABLE_CLASS = None
    LABEL_CLASS = None
    LABEL_HIDED = False
    ENTRY_CLASS = None
    def __init__(self, path, label=None, enable=None, default_value=None, join_to_next=False, scheme_key=None, node_widget=None):
        self._set_prx_port_def_init_('value', path, label)
        #
        self._key = None
        #
        if isinstance(enable, bool):
            self._enable = enable
        #
        self._prx_port_enable = self.ENABLE_CLASS(node_widget)
        self._prx_port_enable.set_hide()
        # gui
        self._prx_port_label = self.LABEL_CLASS(node_widget)
        self._prx_port_label.set_hide()
        self._prx_port_label.set_name(self._label)
        self._prx_port_label.set_name_tool_tip(
            'path: {}\nname: {}'.format(
                self._port_path,
                self._name
            )
        )
        #
        self._prx_port_entry = self.ENTRY_CLASS(node_widget)
        # self._prx_port_entry.set_hide()
        #
        if default_value is not None:
            self._prx_port_entry.set(default_value)
        #
        self._layout = None
        #
        self._is_join_to_next = join_to_next
        self._join_layout = None
        #
        self._custom_widget = None
        #
        self.set_name(self.label)

        self.set_changed_connect_to(
            self.set_changed_update
        )

    def set_node_widget(self, node_widget):
        self._prx_port_enable.set_parent_widget(
            node_widget
        )
        self._prx_port_entry.set_parent_widget(
            node_widget
        )
        self._prx_port_entry.set_parent_widget(
            node_widget
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

    def set_key(self, key):
        self._key = key

    def get_key(self):
        return self._key

    def set_name(self, name):
        self._prx_port_label.set_name(name)

    def set_label(self, text):
        if text:
            self.set_name(text)

    def set_sub_name_update(self):
        if hasattr(self._prx_port_entry._qt_entry_widget, '_set_name_text_'):
            self._prx_port_entry._qt_entry_widget._set_name_text_(self.label)

    def set_enable(self, boolean):
        if boolean is not None:
            if isinstance(boolean, bool):
                self._prx_port_enable.set_show()
                self._prx_port_enable.set(boolean)
        else:
            self._prx_port_enable.set_hide()

    def set_name_width(self, w):
        self.label_widget.set_width(w)

    def set(self, raw=None, **kwargs):
        self._prx_port_entry.set(raw, **kwargs)
        self.set_changed_update()

    def set_changed_update(self):
        if self._prx_port_entry.get_is_default() is False:
            self._prx_port_enable.set(True)
        else:
            self._prx_port_enable.set(False)

    def set_default(self, raw, **kwargs):
        self._prx_port_entry.set_default(raw, **kwargs)

    def get_default(self):
        return self._prx_port_entry.get_default()

    def set_value(self, *args, **kwargs):
        self.set(*args, **kwargs)

    def set_append(self, raw):
        if hasattr(self._prx_port_entry, 'set_append'):
            self._prx_port_entry.set_append(raw)

    def set_clear(self):
        self._prx_port_entry.set_clear()

    def set_reset(self):
        default = self.get_default()
        if default is not None:
            self.set(default)

    def set_tool_tip(self, text, as_markdown_style=False):
        if text is not None:
            if isinstance(text, (tuple, list)):
                if len(text) > 0:
                    text_ = u'\n'.join((u'{}'.format(i) for i in text))
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
            else:
                html = u'<html><body>'
                html += u'<h3>{}</h3>'.format(self._label)
                for i in text_.split('\n'):
                    html += u'<ul><li>{}</li></ul>'.format(i)
                html += u'</body></html>'
            #
            if hasattr(self._prx_port_entry, '_qt_entry_widget'):
                self._prx_port_entry._qt_entry_widget.setToolTip(html)

    def get(self):
        return self._prx_port_entry.get()

    def set_changed_connect_to(self, fnc):
        self._prx_port_entry.set_changed_connect_to(fnc)

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

    def set_menu_raw(self, raw):
        self._prx_port_entry.set_menu_raw(raw)

    def to_custom_widget(self, label_width=80):
        if self._custom_widget is not None:
            return self._custom_widget
        else:
            widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(widget)
            label = self.label_widget
            label.set_width(label_width)
            layout.addWidget(label.widget)
            entry = self._prx_port_entry
            layout.addWidget(entry.widget)
            self._custom_widget = widget
            return self._custom_widget


class PrxConstantPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
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


class PrxFramesPort(PrxConstantPort):
    ENTRY_CLASS = PrxStringEntry
    def __init__(self, *args, **kwargs):
        super(PrxFramesPort, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_use_as_frames()


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
        self._prx_port_entry.set_ext_filter(ext_filter)


class PrxDirectoryOpenPort(PrxConstantPort):
    ENTRY_CLASS = PrxDirectoryOpenEntry
    def __init__(self, *args, **kwargs):
        super(PrxDirectoryOpenPort, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self._prx_port_entry.set_ext_filter(ext_filter)

    def set_show_history_latest(self):
        self._prx_port_entry.set_show_history_latest()


class PrxDirectorySavePort(PrxDirectoryOpenPort):
    ENTRY_CLASS = PrxDirectorySaveEntry
    def __init__(self, *args, **kwargs):
        super(PrxDirectorySavePort, self).__init__(*args, **kwargs)


class PrxFileSavePort(PrxConstantPort):
    ENTRY_CLASS = PrxFileSaveEntry
    def __init__(self, *args, **kwargs):
        super(PrxFileSavePort, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self._prx_port_entry.set_ext_filter(ext_filter)

    def set_history_update(self):
        self._prx_port_entry.set_history_update()


class PrxRsvProjectChoosePort(PrxConstantPort):
    ENTRY_CLASS = PrxRsvProjectChooseEntry
    def __init__(self, *args, **kwargs):
        super(PrxRsvProjectChoosePort, self).__init__(*args, **kwargs)

    def get_histories(self):
        return self.entry_widget.get_histories()


class PrxSchemChoosePort(PrxConstantPort):
    ENTRY_CLASS = PrxSchemeChooseEntry
    def __init__(self, *args, **kwargs):
        super(PrxSchemChoosePort, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_scheme_key(kwargs['scheme_key'])


class PrxBooleanPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = True
    ENTRY_CLASS = PrxBooleanEntry
    def __init__(self, *args, **kwargs):
        super(PrxBooleanPort, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._prx_port_entry._qt_entry_widget._set_name_text_(text)


class PrxEnumeratePort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxEnumerateEntry
    def __init__(self, *args, **kwargs):
        super(PrxEnumeratePort, self).__init__(*args, **kwargs)

    def set_current(self, raw):
        self._prx_port_entry.set_current(raw)

    def get_current(self):
        return self._prx_port_entry.get_current()

    def get_enumerate_strings(self):
        return self._prx_port_entry.get()


class PrxEnumeratePort_(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxChooseEntry_
    def __init__(self, *args, **kwargs):
        super(PrxEnumeratePort_, self).__init__(*args, **kwargs)

    def get_enumerate_strings(self):
        return self._prx_port_entry.get_enumerate_strings()


class PrxScriptPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = PrxScriptEntry
    def __init__(self, *args, **kwargs):
        super(PrxScriptPort, self).__init__(*args, **kwargs)


class PrxArrayPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxArrayEntry
    def __init__(self, *args, **kwargs):
        super(PrxArrayPort, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._prx_port_entry.set_value_type(value_type)

    def set_value_size(self, size):
        self._prx_port_entry.set_value_size(size)


class PrxIntegerArrayPort(PrxArrayPort):
    ENTRY_CLASS = PrxIntegerArrayEntry
    def __init__(self, *args, **kwargs):
        super(PrxIntegerArrayPort, self).__init__(*args, **kwargs)


class PrxFloatArrayPort(PrxArrayPort):
    ENTRY_CLASS = PrxFloatArrayEntry
    def __init__(self, *args, **kwargs):
        super(PrxFloatArrayPort, self).__init__(*args, **kwargs)


class PrxRgbaPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = PrxRgbaEntry
    def __init__(self, *args, **kwargs):
        super(PrxRgbaPort, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_use_as_rgba()


class PrxButtonPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = True
    ENTRY_CLASS = PrxButtonEntry
    def __init__(self, *args, **kwargs):
        super(PrxButtonPort, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._prx_port_entry._qt_entry_widget._set_name_text_(text)

    def set_status(self, status):
        self._prx_port_entry._qt_entry_widget._set_status_(status)


class PrxStatusPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = True
    ENTRY_CLASS = PrxProcessEntry
    def __init__(self, *args, **kwargs):
        super(PrxStatusPort, self).__init__(*args, **kwargs)
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
        self._prx_port_entry._qt_entry_widget._set_rate_statuses_(statuses)

    def set_initialization(self, count, status):
        self._prx_port_entry._qt_entry_widget._set_rate_initialization_(count, status)

    def set_restore(self):
        self._prx_port_entry._qt_entry_widget._set_rate_restore_()

    def set_status_update_at(self, index, status):
        widget = self._prx_port_entry._qt_entry_widget
        widget.rate_status_update_at.emit(index, status)

    def set_finished_at(self, index, status):
        widget = self._prx_port_entry._qt_entry_widget
        widget.rate_finished_at.emit(index, status)

    def set_finished_connect_to(self, fnc):
        widget = self._prx_port_entry._qt_entry_widget
        widget._set_rate_finished_connect_to_(fnc)

    def set_stop_connect_to(self, fnc):
        self._prx_port_entry.set_stop_connect_to(fnc)

    def set_stopped(self, boolean=True):
        self._is_stopped = boolean
        # self.set_restore()

    def get_is_stopped(self):
        return self._is_stopped


class PrxRsvObjChoosePort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = PrxRsvObjChooseEntry
    def __init__(self, *args, **kwargs):
        super(PrxRsvObjChoosePort, self).__init__(*args, **kwargs)


class PrxComponentsPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = PrxComponentsEntry
    def __init__(self, *args, **kwargs):
        super(PrxComponentsPort, self).__init__(*args, **kwargs)


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
                enter_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
                self._qt_entry_layout.addWidget(
                    enter_widget
                )
                enter_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(enter_widget)
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


class PrxGroupPort_(
    AbsPrxPortDef
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLASS = PrxPortStack
    def __init__(self, path):
        self._set_prx_port_def_init_('group', path)
        #
        self._prx_widget = _utl_gui_prx_wdt_utility.PrxExpandedGroup()
        self._prx_widget.set_height_match_to_minimum()
        self._qt_widget = self._prx_widget.widget
        self._prx_widget.set_name(self._label)
        self._prx_widget.set_expanded(True)
        qt_line = _utl_gui_qt_wgt_utility._QtLine()
        self._prx_widget.set_widget_add(qt_line)
        self._port_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_line)
        self._port_layout.setContentsMargins(8, 0, 0, 0)
        #
        self._port_stack = self.PORT_STACK_CLASS()
        # default use -1
        self._label_width_maximum = -1

    def get_label(self):
        return self._label

    def set_use_as_root(self):
        self._prx_widget.set_head_visible(False)

    def set_label(self, text):
        self._prx_widget.set_name(text)

    def set_child_group_create(self, name):
        if self.get_is_root() is True:
            path = name
        else:
            path = '{}.{}'.format(self._port_path, name)
        #
        group_port = self.__class__(path)
        group_port._prx_widget.set_name_font_size(8)
        group_port._prx_widget.set_name_icon_enable(False)
        self._port_layout.addWidget(group_port._prx_widget.widget)
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
            layout._set_align_top_()
            cur_port._set_layout_(layout)
            layout.addWidget(
                cur_port._prx_port_enable.widget
            )
            layout.addWidget(
                cur_port._prx_port_label.widget
            )
            layout.addWidget(
                cur_port._prx_port_entry.widget
            )
            if cur_port.LABEL_HIDED is False:
                cur_port._prx_port_label.set_show()
        elif condition == (False, True):
            widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            self._port_layout.addWidget(widget)
            layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(widget)
            layout._set_align_top_()
            cur_port._set_layout_(layout)
            #
            enter_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            layout.addWidget(
                enter_widget
            )
            enter_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(enter_widget)
            enter_layout.setContentsMargins(0, 0, 0, 0)
            enter_layout.setSpacing(2)
            enter_layout.addWidget(
                cur_port._prx_port_enable.widget
            )
            cur_port._prx_port_enable.set_hide()
            enter_layout.addWidget(
                cur_port._prx_port_label.widget
            )
            cur_port._prx_port_label.set_hide()
            cur_port.set_sub_name_update()
            enter_layout.addWidget(
                cur_port._prx_port_entry.widget
            )
            cur_port._set_join_layout_(enter_layout)
        elif condition == (True, True):
            enter_layout = pre_port._get_join_layout_()
            enter_layout.addWidget(
                cur_port._prx_port_enable.widget
            )
            cur_port._prx_port_enable.set_hide()
            enter_layout.addWidget(
                cur_port._prx_port_label.widget
            )
            cur_port._prx_port_label.set_hide()
            cur_port.set_sub_name_update()
            enter_layout.addWidget(
                cur_port._prx_port_entry.widget
            )
            cur_port._set_join_layout_(enter_layout)
        elif condition == (True, False):
            enter_layout = pre_port._get_join_layout_()
            enter_layout.addWidget(
                cur_port._prx_port_enable.widget
            )
            cur_port._prx_port_enable.set_hide()
            enter_layout.addWidget(
                cur_port._prx_port_label.widget
            )
            cur_port._prx_port_label.set_hide()
            cur_port.set_sub_name_update()
            enter_layout.addWidget(
                cur_port._prx_port_entry.widget
            )
        #
        cur_port._prx_port_entry.set_show()
        #
        self._port_stack.set_object_add(cur_port)
        #
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

    def get_label_width_maximum(self):
        widths = []
        children = self.get_children()
        for i_child in children:
            if i_child.get_type() == 'group':
                pass
            else:
                if i_child.LABEL_HIDED is False:
                    i_width = i_child._prx_port_label.get_name_draw_width()
                    widths.append(i_width)
                else:
                    widths.append(0)
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

    def set_expanded(self, boolean):
        self._prx_widget.set_expanded(boolean)

    def set_reset(self):
        pass

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


class PrxNodePortStack_(obj_abstract.AbsObjStack):
    def __init__(self):
        super(PrxNodePortStack_, self).__init__()

    def get_key(self, obj):
        return obj.get_port_path()


class PrxNode_(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLASS = PrxNodePortStack_
    PORT_CLASS_DICT = dict(
        string=PrxStringPort,
        interge=PrxIntegerPort,
        float=PrxFloatPort,
        button=PrxButtonPort,
        enumerate=PrxEnumeratePort
    )
    def __init__(self, path, *args, **kwargs):
        super(PrxNode_, self).__init__(*args, **kwargs)
        self._path_dag_opt = bsc_core.DccPathDagOpt(path)
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)

        self._port_stack = self.PORT_STACK_CLASS()
        #
        self._prx_port_root = PrxGroupPort_(
            path=self.get_path()
        )
        qt_layout_0.addWidget(self._prx_port_root._prx_widget.widget)
        self._set_port_register_(self._prx_port_root)

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

    def set_port_add(self, port):
        root_port = self.get_port_root()

        port_path = port.get_port_path()
        _ = port_path.split('.')
        group_names = _[:-1]

        current_group_port = root_port
        for i_group_name in group_names:
            i_group_port = current_group_port.get_child(i_group_name)
            if i_group_port is None:
                i_group_port = current_group_port.set_child_group_create(i_group_name)
                self._set_port_register_(i_group_port)

            current_group_port = i_group_port

        group_port = current_group_port
        # print group_port, group_port.get_children_()
        #
        self._set_port_register_(port)
        return group_port.set_child_add(port)

    def _set_port_register_(self, port):
        port._set_node_(self)
        self._port_stack.set_object_add(port)

    def get_port(self, port_path):
        return self._port_stack.get_object(port_path)

    def get_ports(self, regex=None):
        return self._port_stack.get_objects(regex)

    def get_as_kwargs(self):
        dic = {}
        ports = self._port_stack.get_objects()
        for i_port in ports:
            key = i_port.get_port_path()
            if i_port.get_type() not in ['group']:
                value = i_port.get()
                dic[key] = value
        return dic

    def set_name_width(self, w):
        self._name_width = w
        # self._prx_port_root._qt_label_widget.setFixedWidth(self._name_width)

    def set_ports_create_by_configure(self, configure):
        for k, v in configure.items():
            self.set_port_create_by_option(k.replace('/', '.'), v)

    def set_port_create_by_option(self, port_path, option):
        widget_ = option['widget']
        key_ = option.get('key')
        label_ = option.get('label')
        value_ = option['value']
        enable_ = option.get('enable')
        tool_tip_ = option.get('tool_tip')
        #
        join_to_next_ = option.get('join_to_next') or False

        if widget_ in ['string']:
            port = PrxStringPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        elif widget_ in ['integer']:
            port = PrxIntegerPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        elif widget_ in ['float']:
            port = PrxFloatPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        elif widget_ in ['float2']:
            port = PrxFloatArrayPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in ['rgb']:
            port = PrxRgbaPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in ['boolean']:
            port = PrxBooleanPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

        elif widget_ in ['enumerate']:
            port = PrxEnumeratePort_(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            current_ = option.get('current')
            if current_ is not None:
                port.set(current_)
                port.set_default(current_)
            else:
                if value_:
                    port.set(value_[-1])
                    port.set_default(value_[-1])
        #
        elif widget_ in ['file']:
            open_or_save = option.get('open_or_save')
            if open_or_save == 'save':
                port = PrxFileSavePort(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxFileOpenPort(
                    port_path,
                    node_widget=self.widget
                )
            port.set(value_)
            port.set_default(value_)
            ext_filter = option.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)
        #
        elif widget_ in ['directory']:
            open_or_save = option.get('open_or_save')
            if open_or_save == 'save':
                port = PrxDirectorySavePort(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxDirectoryOpenPort(
                    port_path,
                    node_widget=self.widget
                )
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in ['button']:
            port = PrxButtonPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)

        elif widget_ in ['status_button']:
            port = PrxStatusPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
        #
        elif widget_ in ['project']:
            port = PrxRsvProjectChoosePort(
                port_path,
                node_widget=self.widget
            )
            if value_:
                port.set(value_)
        elif widget_ in ['rsv-obj']:
            port = PrxRsvObjChoosePort(
                port_path,
                node_widget=self.widget
            )
            # port.set(value_)
        elif widget_ in ['scheme']:
            port = PrxSchemChoosePort(
                port_path,
                scheme_key=option['scheme_key'],
                node_widget=self.widget
            )
            port.set(value_)
        elif widget_ in ['script']:
            port = PrxScriptPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in ['components']:
            port = PrxComponentsPort(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in ['frames']:
            port = PrxFramesPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        else:
            raise TypeError()
        #
        port.set_key(key_)
        port.set_label(label_)
        port.set_enable(enable_)
        port.set_tool_tip(tool_tip_)
        port.set_join_to_next(join_to_next_)

        self.set_port_add(port)

    def set_expanded(self, boolean):
        self._prx_port_root.set_expanded(boolean)

    def set(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.set(value)
        else:
            utl_core.Log.set_module_warning_trace(
                'port set',
                'port="{}" is non-exists'.format(key)
            )

    def set_changed_connect_to(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.set_changed_connect_to(value)

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
