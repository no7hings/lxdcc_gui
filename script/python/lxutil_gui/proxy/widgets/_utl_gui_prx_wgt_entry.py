# coding:utf-8
import collections

import six

import glob

import os

import functools

import types

from lxbasic import bsc_core
#
from lxutil import utl_core
#
import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_entry

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_view_for_tree


class AttrConfig(object):
    height = 24
    label_width = 64
    PRX_PORT_HEIGHT = 22


class _PrxPortInfo(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtIconPressButton

    def __init__(self, *args, **kwargs):
        super(_PrxPortInfo, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMaximumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget._set_tool_tip_text_(
            '"LMB-click" to use value "default" / "latest"'
        )

    def set(self, boolean):
        self.widget._set_checked_(boolean)


class _PrxPortStatus(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_item._QtStatusItem

    def __init__(self, *args, **kwargs):
        super(_PrxPortStatus, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMaximumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget._set_tool_tip_text_(
            '"LMB-click" to use value "default" / "local" / "global"'
        )

    def set(self, boolean):
        self.widget._set_checked_(boolean)


# label
class _PrxPortLabel(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtTextItem

    def __init__(self, *args, **kwargs):
        super(_PrxPortLabel, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignRight | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        # self._qt_widget._set_name_align_(utl_gui_configure.AlignRegion.Top)

    def set_name(self, text):
        self._qt_widget._set_name_text_(text)

    def set_width(self, w):
        self.widget.setMaximumWidth(w)
        self.widget.setMinimumWidth(w)

    def set_info_tool_tip(self, text):
        pass

    def set_name_tool_tip(self, *args, **kwargs):
        if hasattr(self._qt_widget, '_set_tool_tip_'):
            self._qt_widget._set_tool_tip_(args[0], **kwargs)

    def get_name_draw_width(self):
        return self._qt_widget._get_name_text_draw_width_()


# entry
class AbsPrxTypeQtEntry(utl_gui_prx_abstract.AbsPrxWidget):
    QT_ENTRY_CLS = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxTypeQtEntry, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)

    def _set_build_(self):
        self._qt_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._qt_entry_widget = self.QT_ENTRY_CLS()
        self._qt_layout.addWidget(self._qt_entry_widget)
        #
        self._use_as_storage = False

    def add_button(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, *args, **kwargs):
        raise NotImplementedError()

    def set_option(self, *args, **kwargs):
        pass

    def set_default(self, *args, **kwargs):
        pass

    def get_default(self):
        pass

    def get_is_default(self):
        return False

    def set_clear(self):
        pass

    def connect_value_changed_to(self, fnc):
        pass

    def connect_tab_pressed_to(self, fnc):
        pass

    def set_focus_in(self):
        pass

    def set_use_as_storage(self, boolean=True):
        if hasattr(self._qt_entry_widget, '_set_use_as_storage_'):
            self._qt_entry_widget._set_use_as_storage_(boolean)

    def _set_file_show_(self):
        utl_dcc_objects.OsFile(self.get()).set_open()

    def get_use_as_storage(self):
        return self._use_as_storage

    def set_locked(self, boolean):
        pass

    def set_history_key(self, key):
        pass

    def set_tool_tip(self, *args, **kwargs):
        if hasattr(self._qt_entry_widget, '_set_tool_tip_'):
            self._qt_entry_widget._set_tool_tip_(args[0], **kwargs)

    def set_height(self, h):
        self._qt_widget.setFixedHeight(h)


class _PrxStgObjEntry(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTextEditByChoose

    def __init__(self, *args, **kwargs):
        super(_PrxStgObjEntry, self).__init__(*args, **kwargs)
        self._history_key = 'gui.storage'
        #
        self._ext_filter = 'All File (*.*)'
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._set_value_entry_drop_enable_(True)
        self._qt_entry_widget._set_value_entry_use_as_storage_(True)
        self._qt_entry_widget._set_value_validation_fnc_(self._value_validation_fnc_)
        self._qt_entry_widget._set_completion_extra_gain_fnc_(self._value_completion_gain_fnc_)
        self._qt_entry_widget._set_value_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('history')
        )
        self._qt_entry_widget._set_value_choose_button_name_text_('choose history')
        self._qt_entry_widget._set_choose_button_state_icon_file_path_(
            utl_gui_core.RscIconFile.get('state/popup')
        )
        #
        self._qt_open_or_save_button = self._qt_entry_widget._get_value_add_button_()
        self._qt_open_or_save_button.show()
        self._qt_open_or_save_button._set_name_text_('open file')
        self._qt_open_or_save_button._set_icon_name_('file/file')
        self._qt_open_or_save_button._set_tool_tip_(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )
        self._qt_open_or_save_button.press_clicked.connect(self._set_open_or_save_)
        #
        self._qt_entry_widget.user_choose_changed.connect(self.update_history)
        self._qt_entry_widget._set_value_entry_finished_connect_to_(self.update_history)

        self._qt_entry_widget._set_value_entry_drop_enable_(True)

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def get_ext_filter(self):
        return self._ext_filter

    def set_history_key(self, key):
        self._history_key = key
        #
        self.update_history()

    def get_history_key(self):
        return self._history_key

    def _set_open_or_save_(self):
        raise NotImplementedError()

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget._set_value_entry_changed_connect_to_(fnc)

    #
    def update_history(self):
        value = self._qt_entry_widget._get_value_()
        if value:
            if self._value_validation_fnc_(value) is True:
                utl_core.History.append(
                    self._history_key,
                    value
                )
        #
        histories = utl_core.History.get_all(
            self._history_key
        )
        if histories:
            histories.reverse()
        #
        histories = [i for i in histories if self._value_validation_fnc_(i) is True]
        #
        self._qt_entry_widget._set_choose_values_(
            histories
        )

    def show_history_latest(self):
        _ = utl_core.History.get_latest(self._history_key)
        if _:
            self._qt_entry_widget._set_value_(_)

    def set_locked(self, boolean):
        self._qt_entry_widget._set_value_entry_enable_(
            not boolean
        )
        self._qt_open_or_save_button._set_action_enable_(
            not boolean
        )

    def _value_validation_fnc_(self, history):
        return True

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        return []


class PrxFileOpenEntry(_PrxStgObjEntry):
    def __init__(self, *args, **kwargs):
        super(PrxFileOpenEntry, self).__init__(*args, **kwargs)
        self._qt_open_or_save_button._set_name_text_('open file')
        self._qt_open_or_save_button._set_icon_name_('file/file')
        self._qt_open_or_save_button._set_tool_tip_(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )
        self.set_history_key('gui.file-open')

        self._qt_entry_widget._set_choose_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/file')
        )

    def _set_open_or_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getOpenFileName(
            self.widget,
            'Open File',
            self.get() or '',
            filter=self._ext_filter
        )
        if s:
            _ = s[0]
            if _:
                self.set(
                    s[0]
                )
                self.update_history()

    def _value_validation_fnc_(self, path):
        return os.path.isfile(path)


class PrxFileSaveEntry(_PrxStgObjEntry):
    def __init__(self, *args, **kwargs):
        super(PrxFileSaveEntry, self).__init__(*args, **kwargs)
        self._qt_open_or_save_button._set_name_text_('save file')
        self._qt_open_or_save_button._set_icon_name_('file/file')
        self._qt_open_or_save_button._set_icon_sub_name_('action/save')
        self._qt_open_or_save_button._set_tool_tip_(
            [
                '"LMB-click" to save file by "dialog"'
            ]
        )
        self.set_history_key('gui.file-save')

        self._qt_entry_widget._set_choose_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/file')
        )

    def _set_open_or_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getSaveFileName(
            self.widget,
            'Save File',
            self.get() or '',
            filter=self._ext_filter,
            options=options,
        )
        if s:
            _ = s[0]
            if _:
                self.set(
                    _
                )
                self.update_history()

    def _value_validation_fnc_(self, path):
        return os.path.isfile(path)


class PrxDirectoryOpenEntry(_PrxStgObjEntry):
    def __init__(self, *args, **kwargs):
        super(PrxDirectoryOpenEntry, self).__init__(*args, **kwargs)
        self._qt_open_or_save_button._set_name_text_('open directory')
        self._qt_open_or_save_button._set_icon_name_('file/folder')
        self._qt_open_or_save_button._set_tool_tip_(
            [
                '"LMB-click" to open directory by "dialog"'
            ]
        )
        self.set_history_key('gui.directory-open')

        self._qt_entry_widget._set_choose_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/folder')
        )

    def _set_open_or_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Open Directory',
            self.get() or '',
        )
        if s:
            self.set(
                s
            )
            self.update_history()

    def _value_validation_fnc_(self, path):
        return os.path.isdir(path)

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        _ = glob.glob(
            u'{}*'.format(keyword)
        )
        return [i for i in _ if os.path.isdir(i)]


class PrxDirectorySaveEntry(_PrxStgObjEntry):
    def __init__(self, *args, **kwargs):
        super(PrxDirectorySaveEntry, self).__init__(*args, **kwargs)
        self._qt_open_or_save_button._set_name_text_('save directory')
        self._qt_open_or_save_button._set_icon_name_('file/folder')
        self._qt_open_or_save_button._set_icon_sub_name_('action/save')
        self._qt_open_or_save_button._set_tool_tip_(
            [
                '"LMB-click" to save directory by "dialog"'
            ]
        )
        self.set_history_key('gui.directory-save')

        self._qt_entry_widget._set_choose_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/folder')
        )

    def _set_open_or_save_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Save Directory',
            self.get() or '',
        )
        if s:
            self.set(
                s
            )
            self.update_history()

    def _value_validation_fnc_(self, path):
        return os.path.isdir(path)

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        _ = glob.glob(
            u'{}*'.format(keyword)
        ) or []
        return [i for i in _ if os.path.isdir(i)]


# storage array open
class _PrxStgObjsEntry(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsList
    def __init__(self, *args, **kwargs):
        super(_PrxStgObjsEntry, self).__init__(*args, **kwargs)
        self._history_key = None
        # drop
        self._qt_entry_widget._set_value_entry_drop_enable_(True)
        # entry
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self._qt_widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        self._qt_entry_widget._get_value_entry_gui_()._set_use_as_storage_(True)
        self._qt_entry_widget._get_value_entry_gui_()._set_value_validation_fnc_(self._value_validation_fnc_)
        self._qt_entry_widget._get_value_entry_gui_().entry_added.connect(self.update_history)
        self._qt_entry_widget._get_choose_extra_gui_()._set_popup_auto_resize_enable_(True)
        self._qt_entry_widget._set_value_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('history')
        )
        self._qt_entry_widget._set_choose_button_state_icon_file_path_(
            utl_gui_core.RscIconFile.get('state/popup')
        )
        self._qt_entry_widget._set_value_choose_button_name_text_('choose history')

        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)

        self._ext_filter = 'All File (*.*)'

        self._ext_includes = []

        self._open_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self._qt_entry_widget._set_value_entry_button_add_(self._open_button.widget)
        self._open_button.connect_press_clicked_to(self.open_with_dialog_fnc)
        self._open_button.set_name('open file')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_icon_frame_size(18, 18)
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )

    def open_with_dialog_fnc(self):
        raise NotImplementedError()

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter
    
    def set_ext_includes(self, texts):
        self._ext_includes = texts
        self._ext_filter = 'All File ({})'.format(' '.join(map(lambda x: '*{}'.format(x), texts)))
        self._qt_entry_widget._value_entry._set_empty_sub_text_(
            self._ext_filter
        )

    def append(self, value):
        self._qt_entry_widget._append_value_(
            value
        )

    def extend(self, values):
        self._qt_entry_widget._extend_values_(
            values
        )

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_values_(
            raw
        )

    def get(self):
        return self._qt_entry_widget._get_values_()

    def set_history_key(self, key):
        self._history_key = key
        self.update_history()

    def _value_validation_fnc_(self, value):
        return True

    def update_history(self):
        if self._history_key is not None:
            values = self._qt_entry_widget._get_values_()
            if values:
                value = values[-1]
                if value:
                    if self._value_validation_fnc_(value) is True:
                        utl_core.History.append(
                            self._history_key,
                            value
                        )
            #
            histories = utl_core.History.get_all(
                self._history_key
            )
            if histories:
                histories.reverse()
            #
            histories = [i for i in histories if self._value_validation_fnc_(i) is True]
            #
            self._qt_entry_widget._set_choose_values_(
                histories
            )

    def show_history_latest(self):
        if self._history_key is not None:
            _ = utl_core.History.get_latest(self._history_key)
            if _:
                self._qt_entry_widget._append_value_(_)

    def set_history_visible(self, boolean):
        pass


# directory array open
class PrxEntryAsDirectoriesOpen(_PrxStgObjsEntry):
    def __init__(self, *args, **kwargs):
        super(PrxEntryAsDirectoriesOpen, self).__init__(*args, **kwargs)
        self._open_button.set_name('open directory')
        self._open_button.set_icon_name('file/folder')
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open directory by "dialog"'
            ]
        )
        self._qt_entry_widget._set_choose_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/folder')
        )
        self._qt_entry_widget._set_entry_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/folder')
        )
        self.set_history_key('gui.directories-open')

    def set_locked(self, boolean):
        self._qt_entry_widget._set_value_entry_enable_(not boolean)
        self._qt_entry_widget._set_value_entry_drop_enable_(not boolean)
        self._qt_entry_widget._set_value_entry_choose_enable_(not boolean)
        self._open_button.widget._set_action_enable_(not boolean)

    def set_history_visible(self, boolean):
        self._qt_entry_widget._set_value_entry_choose_visible_(boolean)

    def open_with_dialog_fnc(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Open Directory',
            self.get()[-1] if self.get() else '',
        )
        if s:
            self.append(s)
            self.update_history()

    def _value_validation_fnc_(self, value):
        if value:
            return os.path.isdir(value)
        return False

    def set(self, *args, **kwargs):
        self._qt_entry_widget._clear_all_values_()
        self._qt_entry_widget._set_values_(args[0])


# file array open
class PrxEntryAsFilesOpen(_PrxStgObjsEntry):
    def __init__(self, *args, **kwargs):
        super(PrxEntryAsFilesOpen, self).__init__(*args, **kwargs)
        self._ext_filter = 'All File (*.*)'
        #
        self._open_button.set_name('open file')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )
        self._qt_entry_widget._set_choose_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/file')
        )
        self._qt_entry_widget._set_entry_item_icon_file_path_(
            utl_gui_core.RscIconFile.get('file/file')
        )
        self._qt_entry_widget._value_entry._set_use_as_file_(True)
        self._qt_entry_widget._value_entry._set_use_as_file_multiply_(True)

    def open_with_dialog_fnc(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        # options |= f.DontUseNativeDialog
        s = f.getOpenFileNames(
            self.widget,
            'Open Files',
            self.get()[-1] if self.get() else '',
            filter=self._ext_filter
        )
        if s:
            # s = files, filter
            values = s[0]
            if values:
                values = bsc_core.StgFileMultiplyMtd.merge_to(
                    values,
                    ['*.<udim>.####.*', '*.####.*']
                )
                self.extend(values)
                self.update_history()

    def _value_validation_fnc_(self, value):
        if value:
            if self._ext_includes:
                ext = os.path.splitext(value)[-1]
                if ext not in self._ext_includes:
                    return False
            return bsc_core.StgFileMultiplyMtd.get_is_exists(value)
        return False


class PrxMediasOpenEntry(PrxEntryAsFilesOpen):
    def __init__(self, *args, **kwargs):
        super(PrxMediasOpenEntry, self).__init__(*args, **kwargs)
        self._create_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self._qt_entry_widget._set_value_entry_button_add_(self._create_button.widget)
        self._create_button.connect_press_clicked_to(self._set_create_)
        self._create_button.set_name('create file')
        self._create_button.set_icon_name('camera')
        self._create_button.set_icon_sub_name('action/add')
        self._create_button.set_icon_frame_size(18, 18)
        self._create_button.set_tool_tip(
            [
                '"LMB-click" create file by "screenshot"'
            ]
        )
    @staticmethod
    def _get_tmp_screenshot_file_path_():
        d = bsc_core.SystemMtd.get_home_directory()
        return six.u('{}/screenshot/untitled-{}.jpg').format(d, bsc_core.TimeExtraMtd.get_time_tag_36())

    def _set_save_(self, g):
        f = self._get_tmp_screenshot_file_path_()
        _utl_gui_prx_wdt_utility.PrxScreenshotFrame.set_save_to(
            g, f
        )
        self.append(f)
        self.update_history()

    def _set_create_(self):
        active_window = utl_gui_qt_core.get_active_window()
        w = _utl_gui_prx_wdt_utility.PrxScreenshotFrame()
        w.set_started_connect_to(active_window.hide)
        w.set_start()
        w.set_accepted_connect_to(self._set_save_)
        w.set_finished_connect_to(active_window.show)


class _PrxEntryForValueArray(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsList

    def __init__(self, *args, **kwargs):
        super(_PrxEntryForValueArray, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values'
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        self._qt_entry_widget._set_value_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('attribute')
        )

        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)

        self._add_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self._qt_entry_widget._set_value_entry_button_add_(self._add_button.widget)
        self._add_button.connect_press_clicked_to(self._set_add_)
        self._add_button.set_name('add')
        self._add_button.set_icon_name('add')
        self._add_button.set_icon_frame_size(18, 18)
        self._add_button.set_tool_tip(
            [
                '"LMB-click" add a value'
            ]
        )

    def _set_add_(self):
        pass

    def get(self):
        return self._qt_entry_widget._get_values_()

    def set(self, raw=None, **kwargs):
        pass

    def append(self, value):
        self._qt_entry_widget._append_value_(
            value
        )


class _PrxEntryAsArrayWithChoose(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsListWithChoose

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsArrayWithChoose, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values_choose'
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        self._qt_entry_widget._set_value_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('attribute')
        )

        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)

    def _set_add_(self):
        pass

    def get(self):
        pass

    def set(self, *args, **kwargs):
        pass

    def set_choose_values(self, *args, **kwargs):
        self._qt_entry_widget._clear_choose_values_()
        self._qt_entry_widget._set_choose_values_(args[0])

    def append(self, value):
        pass


class _AbsShotgunDef(object):
    @classmethod
    def get_shotgun_filter_keys_fnc(cls, data, fields):
        tags = []
        for i_tag in fields:
            if isinstance(i_tag, six.string_types):
                i_data = data.get(i_tag)
            else:
                i_data = data.get(i_tag.keys()[0])
            if isinstance(i_data, six.string_types):
                tags.append(i_data.decode('utf-8'))
            elif isinstance(i_data, (tuple, list)):
                for j_data in i_data:
                    if isinstance(j_data, six.string_types):
                        tags.append(j_data)
                    # entity
                    elif isinstance(j_data, dict):
                        tags.append(
                            j_data.get('name').decode('utf-8')
                        )
            elif isinstance(i_data, dict):
                tags.append(
                    i_data.get('name').decode('utf-8')
                )
        return list(tags)

    @classmethod
    def get_shotgun_args_fnc(
            cls, stg_entity_dict, shotgun_entity_kwargs, name_field=None, image_field=None, keyword_filter_fields=None,
            tag_filter_fields=None
            ):
        """
        :param stg_entity_dict
        :param shotgun_entity_kwargs:
        etc.
            {
                'entity_type': 'HumanUser',
                'filters': [['sg_studio', 'is', 'CG'], ['sg_status_list', 'is', 'act']],
                'fields': ['sg_nickname', 'email', 'name'],
            },
        :param name_field:
        :param image_field:
        :param keyword_filter_fields:
        :param tag_filter_fields:
        :return:
        """
        if shotgun_entity_kwargs:
            import lxshotgun.objects as stg_objects

            #
            name_field = name_field or 'name'
            image_field = image_field or 'image'
            shotgun_entity_kwargs['fields'].append(name_field)
            shotgun_entity_kwargs['fields'].append(image_field)
            if isinstance(tag_filter_fields, (tuple, list)):
                for i_tag in tag_filter_fields:
                    if isinstance(i_tag, six.string_types):
                        shotgun_entity_kwargs['fields'].append(i_tag)
            #
            stg_entities = stg_objects.StgConnector().get_shotgun_entities_(
                **shotgun_entity_kwargs
            )
            names = []
            image_url_dict = {}
            keyword_filter_dict = collections.OrderedDict()
            tag_filter_dict = collections.OrderedDict()
            for i_stg_entity in stg_entities:
                i_key = i_stg_entity[name_field].decode('utf-8')
                stg_entity_dict[i_key] = i_stg_entity
                names.append(i_key)
                #
                i_image_url = i_stg_entity.get(image_field)
                image_url_dict[i_key] = i_image_url
                if keyword_filter_fields:
                    i_filter_keys = cls.get_shotgun_filter_keys_fnc(
                        i_stg_entity, keyword_filter_fields
                    )
                    keyword_filter_dict[i_key] = i_filter_keys
                #
                if tag_filter_fields:
                    i_filter_keys = cls.get_shotgun_filter_keys_fnc(
                        i_stg_entity, tag_filter_fields
                    )
                    i_filter_keys.insert(0, 'All')
                    tag_filter_dict[i_key] = i_filter_keys
            #
            names = bsc_core.RawTextsMtd.sort_by_initial(names)
            return names, image_url_dict, keyword_filter_dict, tag_filter_dict


# shotgun
class _PrxEntryAsShotgunEntityByChoose(
    AbsPrxTypeQtEntry,
    _AbsShotgunDef
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTextEditByChoose

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsShotgunEntityByChoose, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # entry
        self._qt_entry_widget._set_value_entry_enable_(True)
        # choose
        self._qt_entry_widget._set_choose_extra_auto_resize_enable_(False)
        self._qt_entry_widget._set_choose_index_showable_(True)
        self._qt_entry_widget._set_choose_extra_tag_filter_enable_(True)
        self._qt_entry_widget._set_choose_extra_keyword_filter_enable_(True)
        self._qt_entry_widget._set_choose_extra_item_size_(40, 40)
        self._qt_entry_widget._set_value_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('application/shotgrid')
        )
        self._qt_entry_widget._set_choose_button_state_icon_file_path_(
            utl_gui_core.RscIconFile.get('state/popup')
        )

        self._data = []

        self._stg_entity_dict = {}

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, *args, **kwargs):
        self._qt_entry_widget._set_value_(args[0])

    def get_stg_entity(self):
        _ = self.get()
        if _ in self._stg_entity_dict:
            return self._stg_entity_dict[self.get()]

    def set_clear(self):
        self._stg_entity_dict = {}
        self._qt_entry_widget._set_value_clear_()

    def set_shotgun_entity_kwargs(
            self,
            shotgun_entity_kwargs,
            name_field=None,
            image_field=None,
            keyword_filter_fields=None,
            tag_filter_fields=None
    ):
        def post_fnc_():
            pass

        def cache_fnc_():
            return list(
                self.get_shotgun_args_fnc(
                    self._stg_entity_dict,
                    shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
                )
            )

        def build_fnc_(args):
            names, image_url_dict, keyword_filter_dict, tag_filter_dict = args
            #
            self._qt_entry_widget._set_choose_values_(names)
            self._qt_entry_widget._set_choose_image_url_dict_(image_url_dict)
            self._qt_entry_widget._set_choose_keyword_filter_dict_(keyword_filter_dict)
            self._qt_entry_widget._set_choose_tag_filter_dict_(tag_filter_dict)

        self._qt_entry_widget._run_build_use_thread_(
            cache_fnc_, build_fnc_, post_fnc_
        )

    def connect_value_changed_to(self, fnc):
        # clear
        self._qt_entry_widget.user_value_entry_cleared.connect(
            fnc
        )
        # completion
        self._qt_entry_widget.user_completion_finished.connect(
            fnc
        )
        # choose
        self._qt_entry_widget.user_choose_changed.connect(
            fnc
        )

    def connect_tab_pressed_to(self, fnc):
        self._qt_entry_widget.user_key_tab_pressed.connect(fnc)
        return True

    def set_focus_in(self):
        self._qt_entry_widget._set_value_entry_focus_in_()

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_entry_widget._run_build_use_thread_(
            cache_fnc, build_fnc, post_fnc
        )


class _PrxEntryAsShotgunEntitiesWithChoose(
    AbsPrxTypeQtEntry,
    _AbsShotgunDef
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsList

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsShotgunEntitiesWithChoose, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # entry
        self._qt_entry_widget._value_entry._set_grid_size_(80, 20)
        self._qt_entry_widget._value_entry._set_grid_mode_()
        # popup
        self._qt_entry_widget._set_value_entry_enable_(True)
        # resize
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        #
        self._qt_entry_widget._set_choose_extra_auto_resize_enable_(False)
        self._qt_entry_widget._set_choose_extra_tag_filter_enable_(True)
        self._qt_entry_widget._set_choose_extra_keyword_filter_enable_(True)
        self._qt_entry_widget._set_choose_extra_item_size_(40, 40)
        self._qt_entry_widget._set_value_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('application/shotgrid')
        )
        self._qt_entry_widget._set_choose_button_state_icon_file_path_(
            utl_gui_core.RscIconFile.get('state/popup')
        )
        #
        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)
        #
        self._data = []

        self._stg_entity_dict = {}

    def get(self):
        return self._qt_entry_widget._get_values_()

    def set(self, *args, **kwargs):
        self._qt_entry_widget._set_values_(args[0])

    def append(self, value):
        self._qt_entry_widget._append_value_(
            value
        )

    def set_clear(self):
        self._qt_entry_widget._set_clear_()

    def set_shotgun_entity_kwargs(
            self,
            shotgun_entity_kwargs,
            name_field=None,
            image_field=None,
            keyword_filter_fields=None,
            tag_filter_fields=None
    ):
        def post_fnc_():
            pass

        def cache_fnc_():
            return list(
                self.get_shotgun_args_fnc(
                    self._stg_entity_dict,
                    shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
                )
            )

        def build_fnc_(args):
            names, image_url_dict, keyword_filter_dict, tag_filter_dict = args
            #
            self._qt_entry_widget._set_choose_values_(names)
            self._qt_entry_widget._set_choose_image_url_dict_(image_url_dict)
            self._qt_entry_widget._set_choose_keyword_filter_dict_(keyword_filter_dict)
            self._qt_entry_widget._set_choose_tag_filter_dict_(tag_filter_dict)

        self._qt_entry_widget._run_build_use_thread_(
            cache_fnc_, build_fnc_, post_fnc_
        )

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_entry_widget._run_build_use_thread_(
            cache_fnc, build_fnc, post_fnc
        )


class _PrxEntryAsRsvProject(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTextEditByChoose
    #
    HISTORY_KEY = 'gui.projects'

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsRsvProject, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        #
        self.update_history()
        #
        self._qt_entry_widget._set_value_entry_finished_connect_to_(self.update_history)
        self._qt_entry_widget.user_choose_changed.connect(self.update_history)

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget._set_value_entry_changed_connect_to_(fnc)

    #
    def update_history(self):
        project = self._qt_entry_widget._get_value_()
        if project:
            import lxresolver.commands as rsv_commands

            resolver = rsv_commands.get_resolver()
            #
            rsv_project = resolver.get_rsv_project(project=project)
            project_directory_path = rsv_project.get_directory_path()
            work_directory_path = '{}/work'.format(project_directory_path)
            if bsc_core.StgPathOpt(work_directory_path).get_is_exists() is True:
                utl_core.History.append(
                    self.HISTORY_KEY,
                    project
                )
        #
        histories = utl_core.History.get_all(
            self.HISTORY_KEY
        )
        if histories:
            histories = [i for i in histories if i]
            histories.reverse()
            #
            self._qt_entry_widget._set_choose_values_(
                histories
            )

    def show_history_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._qt_entry_widget._set_value_(_)

    def get_histories(self):
        return utl_core.History.get_all(
            self.HISTORY_KEY
        )


class PrxEntryForSchemeAsChoose(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTextEditByChoose
    #
    HISTORY_KEY = 'gui.schemes'

    def __init__(self, *args, **kwargs):
        super(PrxEntryForSchemeAsChoose, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        #
        self._scheme_key = None
        #
        self.update_history()
        #
        self._qt_entry_widget._set_value_entry_finished_connect_to_(self.update_history)
        self._qt_entry_widget.user_choose_changed.connect(self.update_history)

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.set_history_add(raw[0])
            self.update_history()
            self.show_history_latest()

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def set_scheme_key(self, key):
        self._scheme_key = key

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget._set_value_entry_changed_connect_to_(fnc)

    #
    def get_histories(self):
        if self._scheme_key is not None:
            return utl_core.History.get_all(
                self._scheme_key
            )
        return []

    def set_history_add(self, scheme):
        if self._scheme_key is not None:
            utl_core.History.append(
                self._scheme_key,
                scheme
            )

    #
    def update_history(self):
        if self._scheme_key is not None:
            scheme = self._qt_entry_widget._get_value_()
            if scheme:
                utl_core.History.append(
                    self._scheme_key,
                    scheme
                )
            #
            histories = utl_core.History.get_all(
                self._scheme_key
            )
            if histories:
                histories = [i for i in histories if i]
                histories.reverse()
                #
                self._qt_entry_widget._set_choose_values_(
                    histories
                )

    def show_history_latest(self):
        if self._scheme_key is not None:
            _ = utl_core.History.get_latest(self._scheme_key)
            if _:
                self._qt_entry_widget._set_value_(_)


class _PrxEntryAsConstant(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTextEdit

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsConstant, self).__init__(*args, **kwargs)
        # self._qt_entry_widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        #
        self.widget.setFocusProxy(self._qt_entry_widget)

    def set_value_type(self, value_type):
        self._qt_entry_widget._set_value_type_(value_type)

    def set_use_as_frames(self):
        self._qt_entry_widget._set_value_validator_use_as_frames_()

    def set_use_as_rgba(self):
        self._qt_entry_widget._set_value_validator_use_as_rgba_()

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_default(self):
        return self._qt_entry_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget._set_value_entry_changed_connect_to_(fnc)

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

    def set_locked(self, boolean):
        self._qt_entry_widget._set_value_entry_enable_(not boolean)


class _PrxEntryAsEnumerate(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTextEditByChoose

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsEnumerate, self).__init__(*args, **kwargs)
        #
        self.widget.setFocusProxy(self._qt_entry_widget)
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._set_choose_index_showable_(True)

    def get(self):
        return self._qt_entry_widget._get_value_()

    def get_enumerate_strings(self):
        return self._qt_entry_widget._get_choose_values_()

    def set(self, *args, **kwargs):
        raw = args[0]
        if isinstance(raw, (tuple, list)):
            self._qt_entry_widget._set_choose_values_(raw)
            if raw:
                self.set(raw[-1])
                self.set_default(raw[-1])
        elif isinstance(raw, six.string_types):
            self._qt_entry_widget._set_value_(raw)
        elif isinstance(raw, (int, float)):
            self._qt_entry_widget._set_choose_value_by_index_(int(raw))

    def set_option(self, *args, **kwargs):
        self._qt_entry_widget._set_choose_values_(args[0])

    def set_icon_file_as_value(self, value, file_path):
        self._qt_entry_widget._set_choose_item_icon_file_path_at_(
            value, file_path
        )

    def set_default(self, raw, **kwargs):
        if isinstance(raw, six.string_types):
            self._qt_entry_widget._set_value_default_(raw)
        elif isinstance(raw, (int, float)):
            self._qt_entry_widget._set_choose_value_default_by_index_(raw)

    def get_default(self):
        return self._qt_entry_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget.choose_changed.connect(fnc)

    def set_locked(self, boolean):
        self._qt_entry_widget._set_value_entry_enable_(not boolean)


# capsule
class _PrxEntryAsCapsule(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsCapsule

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsCapsule, self).__init__(*args, **kwargs)

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, *args, **kwargs):
        self._qt_entry_widget._set_value_(
            args[0]
        )

    def set_locked(self, boolean):
        self._qt_entry_widget._set_value_entry_enable_(not boolean)

    def set_default(self, *args, **kwargs):
        self._qt_entry_widget._set_value_default_(
            args[0]
        )

    def get_default(self):
        return self._qt_entry_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def set_option(self, *args, **kwargs):
        self._qt_entry_widget._set_capsule_strings_(
            args[0]
        )

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget.value_changed.connect(fnc)


class PrxTextEntry(_PrxEntryAsConstant):
    def __init__(self, *args, **kwargs):
        super(PrxTextEntry, self).__init__(*args, **kwargs)
        self.set_value_type(str)


class _PrxEntryAsString(_PrxEntryAsConstant):
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsString, self).__init__(*args, **kwargs)
        self.set_value_type(str)


class _PrxEntryAsInteger(_PrxEntryAsConstant):
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsInteger, self).__init__(*args, **kwargs)
        self.set_value_type(int)


class _PrxEntryAsFloat(_PrxEntryAsConstant):
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsFloat, self).__init__(*args, **kwargs)
        self.set_value_type(float)


class _PrxEntryAsTuple(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTextEdits

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsTuple, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._qt_entry_widget._set_value_type_(value_type)

    def set_value_size(self, size):
        self._qt_entry_widget._set_value_size_(size)

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_value_(
            raw
        )

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget._set_value_entry_changed_connect_to_(fnc)


class _PrxEntryAsIntegerTuple(_PrxEntryAsTuple):
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsIntegerTuple, self).__init__(*args, **kwargs)
        self._qt_entry_widget._build_value_entry_(2, int)


class _PrxEntryAsFloatTuple(_PrxEntryAsTuple):
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsFloatTuple, self).__init__(*args, **kwargs)
        self._qt_entry_widget._build_value_entry_(2, float)


class _PrxEntryAsRgba(_PrxEntryAsConstant):
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsTupleByChoose
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsRgba, self).__init__(*args, **kwargs)


class _PrxEntryAsBoolean(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_item.QtCheckItem

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsBoolean, self).__init__(*args, **kwargs)

    def get(self):
        return self._qt_entry_widget._get_is_checked_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_checked_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_default(self):
        return self._qt_entry_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def connect_value_changed_to(self, fnc):
        self._qt_entry_widget._set_item_check_changed_connect_to_(fnc)


class _PrxEntryAsScript(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_entry.QtValueEntryAsContentEdit

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsScript, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)
        #
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._set_value_entry_drop_enable_(True)
        self._qt_entry_widget._set_item_value_entry_enable_(True)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_value_(raw)

    def set_external_editor_ext(self, ext):
        self._qt_entry_widget._set_external_editor_ext_(ext)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def set_locked(self, boolean):
        self._qt_entry_widget._set_value_entry_enable_(not boolean)


class _PrxEntryAsButton(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_item.QtPressItem

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsButton, self).__init__(*args, **kwargs)

    def get(self):
        return None

    @utl_core.Modifier.exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    @staticmethod
    @utl_core.Modifier.exception_catch
    def __exec_scp(script):
        exec script

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_entry_widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )
        elif isinstance(raw, six.string_types):
            self._qt_entry_widget.press_clicked.connect(
                functools.partial(self.__exec_scp, raw)
            )

    def set_menu_data(self, raw):
        self._qt_entry_widget._set_menu_data_(raw)

    def set_option_enable(self, boolean):
        self._qt_entry_widget._set_option_click_enable_(boolean)


class PrxSubProcessEntry(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_item.QtPressItem

    def __init__(self, *args, **kwargs):
        super(PrxSubProcessEntry, self).__init__(*args, **kwargs)
        self._stop_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.add_button(self._stop_button)
        self._stop_button.set_name('Stop Process')
        self._stop_button.set_icon_by_text('Stop Process')
        self._stop_button.set_tool_tip('press to stop process')

    def get(self):
        return None

    @utl_core.Modifier.exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_entry_widget.clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_menu_data(self, raw):
        self._qt_entry_widget._set_menu_data_(raw)

    def set_stop(self, raw):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._stop_button.widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_stop_connect_to(self, fnc):
        self._stop_button.widget.press_clicked.connect(
            functools.partial(self.__exec_fnc, fnc)
        )


class PrxValidatorEntry(AbsPrxTypeQtEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLS = _utl_gui_qt_wgt_item.QtPressItem

    def __init__(self, *args, **kwargs):
        super(PrxValidatorEntry, self).__init__(*args, **kwargs)

    def get(self):
        return None

    @utl_core.Modifier.exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_entry_widget.clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_menu_data(self, raw):
        self._qt_entry_widget._set_menu_data_(raw)


class _AbsPrxTypeEntry(utl_gui_prx_abstract.AbsPrxWidget):
    PRX_ENTRY_CLS = None
    def __init__(self, *args, **kwargs):
        super(_AbsPrxTypeEntry, self).__init__(*args, **kwargs)

    def _set_build_(self):
        self._qt_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._prx_entry_widget = self.PRX_ENTRY_CLS()
        self._qt_layout.addWidget(self._prx_entry_widget.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, raw=None, **kwargs):
        raise NotImplementedError()

    def get_default(self):
        return None

    def set_default(self, raw=None, **kwargs):
        pass

    def get_is_default(self):
        return False

    def set_tool_tip(self, *args, **kwargs):
        if hasattr(self._prx_entry_widget._qt_widget, '_set_tool_tip_'):
            if args[0]:
                self._prx_entry_widget._qt_widget._set_tool_tip_(args[0], **kwargs)

    def set_clear(self):
        pass

    def connect_value_changed_to(self, fnc):
        pass

    def set_locked(self, boolean):
        pass

    def set_height(self, h):
        self._qt_widget.setFixedHeight(h)

    def connect_tab_pressed_to(self, fnc):
        pass


class _PrxEntryAsRsvObj(_AbsPrxTypeEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLS = _utl_gui_prx_wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'resolver'

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsRsvObj, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(160)
        self.widget.setMinimumHeight(160)
        self._prx_entry_widget.set_header_view_create(
            [('name', 2), ('update', 1)],
            320
        )
        self._prx_entry_widget.set_selection_use_single()
        self._prx_entry_widget.set_size_policy_height_fixed_mode()
        # resize
        self._prx_entry_widget.set_resize_target(self.widget)
        self._prx_entry_widget.set_resize_enable(True)
        self._prx_entry_widget.set_resize_minimum(82)
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
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_entry_widget.create_item(
                    **create_kwargs
                )
            # prx_item.set_checked(True)
            prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._obj_add_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item)
                )
                return True, prx_item, None
            else:
                self.__item_show_deferred_fnc(prx_item)
                return True, prx_item, None

    def __item_show_deferred_fnc(self, prx_item, use_as_tree=True):
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
                    ('expand branch', 'expand', prx_item.set_expand_branch),
                    ('collapse branch', 'collapse', prx_item.set_collapse_branch),
                ]
            )
        #
        result = obj.get('result')
        update = obj.get('update')
        prx_item.set_icon_by_text(obj_type_name)
        prx_item.set_names([obj_name, update])
        prx_item.set_tool_tip(obj.description)
        if result:
            if bsc_core.StgPathOpt(result).get_is_file():
                prx_item.set_icon_by_file(utl_dcc_objects.OsFile(result).icon)
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def __add_item_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._obj_add_dict:
                    self.__set_item_comp_add_as_tree_(i_rsv_obj, use_show_thread=True)
        #
        self.__set_item_comp_add_as_tree_(obj, use_show_thread=True)

    def __add_item_as_list(self, obj):
        obj_path = obj.path
        obj_type = obj.type
        #
        create_kwargs = dict(
            name='...',
            filter_key=obj_path
        )
        prx_item = self._prx_entry_widget.create_item(
            **create_kwargs
        )
        # prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._obj_add_dict[obj_path] = prx_item
        #
        prx_item.set_show_build_fnc(
            functools.partial(
                self.__item_show_deferred_fnc, prx_item, False
            )
        )

    def __set_item_selected(self, obj):
        item = obj.get_obj_gui()
        self._prx_entry_widget.set_item_selected(
            item, exclusive=True
        )

    def __clear_items_(self):
        self._prx_entry_widget.set_clear()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__clear_items_()
            objs = raw
            if objs:
                with utl_core.GuiProgressesRunner.create(maximum=len(objs), label='gui-add for resolver object') as g_p:
                    for i in objs:
                        g_p.set_update()
                        #
                        self.__add_item_as_list(i)
                    #
                    self.__set_item_selected(
                        objs[-1]
                    )
        else:
            pass

    def get(self):
        _ = self._prx_entry_widget.get_current_item()
        if _:
            return _.get_gui_dcc_obj(namespace=self.NAMESPACE)

    def connect_value_changed_to(self, fnc):
        self._prx_entry_widget.connect_item_select_changed_to(
            fnc
        )


class _PrxEntryAsNodes(_AbsPrxTypeEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLS = _utl_gui_prx_wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'dcc'

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsNodes, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(162)
        self.widget.setMinimumHeight(162)
        self._prx_entry_widget.set_header_view_create(
            [('name', 1)],
            320
        )
        self._prx_entry_widget.set_selection_use_single()
        self._prx_entry_widget.set_size_policy_height_fixed_mode()
        self._prx_entry_widget.set_resize_target(self.widget)
        self._prx_entry_widget.set_resize_enable(True)
        self._prx_entry_widget.set_resize_minimum(82)
        #
        self._obj_add_dict = self._prx_entry_widget._item_dict

        self._view_mode = 'list'

    def __add_item_comp_as_tree_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._obj_add_dict:
            prx_item = self._obj_add_dict[obj_path]
            return False, prx_item, None
        else:
            create_kwargs = dict(
                name='loading ...',
                icon=obj.icon,
                filter_key=obj_path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._obj_add_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_entry_widget.create_item(
                    **create_kwargs
                )
            #
            prx_item.set_checked(True)
            prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._obj_add_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item)
                )
                return True, prx_item, None
            else:
                self.__item_show_deferred_fnc(prx_item)
                return True, prx_item, None

    def __item_show_deferred_fnc(self, prx_item, use_as_tree=True):
        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        prx_item.set_name(
            obj.get_name()
        )
        prx_item.set_tool_tip(
            (
                'type: {}\n'
                'path: {}\n'
            ).format(obj.get_type_name(), obj.get_path())
        )
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
                    ('expand branch', 'expand', prx_item.set_expand_branch),
                    ('collapse branch', 'collapse', prx_item.set_collapse_branch),
                ]
            )
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        # self._prx_entry_widget.set_loading_update()

    #
    def __add_item_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._obj_add_dict:
                    i_is_create, i_prx_item, _ = self.__add_item_comp_as_tree_(i_rsv_obj, use_show_thread=True)
                    if i_is_create is True:
                        i_prx_item.set_expanded(True)
        #
        self.__add_item_comp_as_tree_(obj, use_show_thread=True)

    def __add_item_as_list(self, obj):
        path = obj.path
        type_name = obj.type_name
        #
        create_kwargs = dict(
            name='loading ...',
            icon_name_text=type_name,
            filter_key=path
        )
        prx_item = self._prx_entry_widget.create_item(
            **create_kwargs
        )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._obj_add_dict[path] = prx_item
        #
        self.__item_show_deferred_fnc(prx_item, use_as_tree=False)

    def __set_item_selected(self, obj):
        item = obj.get_obj_gui()
        self._prx_entry_widget.set_item_selected(
            item, exclusive=True
        )

    def __clear_items_(self):
        self._prx_entry_widget.set_clear()

    def set_view_mode(self, mode):
        self._view_mode = mode

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__clear_items_()
            objs = raw
            if objs:
                for i in objs:
                    if self._view_mode == 'list':
                        self.__add_item_as_list(i)
                    elif self._view_mode == 'tree':
                        self.__add_item_as_tree(i)
                #
                self.__set_item_selected(
                    objs[-1]
                )
        else:
            pass

    def set_checked_by_include_paths(self, paths):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path in paths:
                    i.set_checked(True, extra=True)

    def set_unchecked_by_include_paths(self, paths):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path not in paths:
                    i.set_checked(False, extra=True)

    def get(self):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE) for i in _ if i.get_is_checked()]
        return []

    def get_all(self):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE) for i in _]
        return []

    def connect_value_changed_to(self, fnc):
        self._prx_entry_widget.connect_item_select_changed_to(
            fnc
        )


# files
class _PrxEntryAsFiles(_AbsPrxTypeEntry):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLS = _utl_gui_prx_wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'storage'

    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsFiles, self).__init__(*args, **kwargs)
        self._qt_widget.setFixedHeight(162)
        self._prx_entry_widget.set_header_view_create(
            [('name', 3), ('update', 1)],
            480
        )
        self._prx_entry_widget.set_selection_use_single()
        self._prx_entry_widget.set_size_policy_height_fixed_mode()
        self._prx_entry_widget.set_resize_target(self.widget)
        self._prx_entry_widget.set_resize_enable(True)
        self._prx_entry_widget.set_resize_minimum(82)
        #
        self._prx_entry_widget.connect_refresh_action_to(self.refresh)
        #
        self._obj_add_dict = self._prx_entry_widget._item_dict

        self._root_location = None

        self._view_mode = 'list'

        self._paths = []

    def __add_item_comp_as_tree_(self, obj, scheme):
        path = obj.path
        type_name = obj.type
        if path in self._obj_add_dict:
            prx_item = self._obj_add_dict[path]
            return False, prx_item, None

        create_kwargs = dict(
            name='...',
            filter_key=path
        )
        parent = obj.get_parent()
        if parent is not None:
            prx_item_parent = self._obj_add_dict[parent.path]
            prx_item = prx_item_parent.add_child(
                **create_kwargs
            )
        else:
            prx_item = self._prx_entry_widget.create_item(
                **create_kwargs
            )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._obj_add_dict[path] = prx_item
        #
        prx_item.set_show_build_fnc(
            lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item, scheme)
        )
        return True, prx_item, None

    def __item_show_deferred_fnc(self, prx_item, scheme, use_as_tree=True):
        def rpc_lock_folder_fnc_():
            bsc_core.StgPathPermissionMtd.change_mode(path, mode='555')
            prx_item.set_status(
                prx_item.ValidatorStatus.Locked
            )

        def rpc_unlock_folder_fnc_():
            bsc_core.StgPathPermissionMtd.change_mode(path, mode='777')
            prx_item.set_status(
                prx_item.ValidatorStatus.Normal
            )

        def rpc_lock_files_fnc_():
            file_paths = bsc_core.StgDirectoryOpt(path).get_all_file_paths()
            for i_file_path in file_paths:
                bsc_core.StgPathPermissionMtd.change_mode(i_file_path, mode='555')
                prx_item.set_status(
                    prx_item.ValidatorStatus.Normal
                )

        def rpc_unlock_files_fnc_():
            file_paths = bsc_core.StgDirectoryOpt(path).get_all_file_paths()
            for i_file_path in file_paths:
                bsc_core.StgPathPermissionMtd.change_mode(i_file_path, mode='777')
                prx_item.set_status(
                    prx_item.ValidatorStatus.Normal
                )

        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        path = obj.get_path()
        if bsc_core.StgFileOpt(path).get_is_exists() is True:
            update = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                bsc_core.StgFileOpt(
                    path
                ).get_modify_timestamp(),
                language=1
            )
        else:
            update = 'non-exists'
        if use_as_tree is True:
            prx_item.set_names([obj.get_name(), update])
        else:
            prx_item.set_names([obj.get_path_prettify(), update])
        prx_item.set_icon_by_file(
            obj.get_icon()
        )
        prx_item.set_tool_tip(
            (
                'type: {}\n'
                'path: {}\n'
            ).format(obj.get_type_name(), obj.get_path())
        )
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
                    ('expand branch', 'expand', prx_item.set_expand_branch),
                    ('collapse branch', 'collapse', prx_item.set_collapse_branch),
                ]
            )
        #
        if scheme == 'file':
            prx_item.set_drag_enable(True)
            prx_item.set_drag_urls([obj.get_path()])
            # for katana
            prx_item.set_drag_data(
                {
                    'nodegraph/fileref': str(obj.get_path())
                }
            )
        elif scheme == 'folder':
            menu_raw.extend(
                [
                    ('rpc folder permission',),
                    ('rpc lock folder', 'lock', rpc_lock_folder_fnc_),
                    ('rpc unlock folder', 'lock', rpc_unlock_folder_fnc_),
                    ('rpc file permission',),
                    ('rpc lock files', 'lock', rpc_lock_files_fnc_),
                    ('rpc unlock files', 'lock', rpc_unlock_files_fnc_),
                ]
            )
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        is_writeable = obj.get_is_writeable()
        if is_writeable is False:
            prx_item.set_status(
                prx_item.ValidatorStatus.Locked
            )
    #
    def __add_item_as_tree(self, obj, scheme):
        if self._root_location is not None:
            i_is_create, i_prx_item, _ = self.__add_item_as_list(self._root_obj, scheme)
            if i_is_create is True:
                i_prx_item.set_expanded(True)
            ancestor_paths = obj.get_ancestor_paths()
            ancestor_paths.reverse()
            if self._root_location in ancestor_paths:
                index = ancestor_paths.index(self._root_location)
                for i_path in ancestor_paths[index:]:
                    if i_path not in self._obj_add_dict:
                        i_obj = self._root_obj.create_dag_fnc(i_path)
                        i_is_create, i_prx_item, _ = self.__add_item_comp_as_tree_(i_obj, scheme='folder')
                        if i_is_create is True:
                            i_prx_item.set_expanded(True)
            else:
                return
        else:
            ancestors = obj.get_ancestors()
            if ancestors:
                ancestors.reverse()
                for i_obj in ancestors:
                    i_path = i_obj.path
                    if i_path not in self._obj_add_dict:
                        i_is_create, i_prx_item, _ = self.__add_item_comp_as_tree_(i_obj, scheme='folder')
                        if i_is_create is True:
                            i_prx_item.set_expanded(True)
        #
        self.__add_item_comp_as_tree_(obj, scheme)

    def __add_item_as_list(self, obj, scheme):
        path = obj.get_path()
        type_name = obj.get_type_name()
        if path in self._obj_add_dict:
            prx_item = self._obj_add_dict[path]
            return False, prx_item, None
        #
        create_kwargs = dict(
            name='...',
            filter_key=path
        )
        prx_item = self._prx_entry_widget.create_item(
            **create_kwargs
        )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._obj_add_dict[path] = prx_item
        #
        prx_item.set_show_build_fnc(
            lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item, scheme, use_as_tree=False)
        )
        return True, prx_item, None

    def __set_item_selected(self, obj):
        item = obj.get_obj_gui()
        self._prx_entry_widget.set_item_selected(
            item, exclusive=True
        )

    def restore(self):
        self._prx_entry_widget.set_clear()

    def refresh(self):
        self.set(self._paths)

    def set_view_mode(self, mode):
        self._view_mode = mode

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.restore()
            self._paths = raw
            if self._paths:
                obj_cur = None
                for i_path in self._paths:
                    if bsc_core.StgPathOpt(i_path).get_is_file():
                        i_obj = utl_dcc_objects.OsFile(i_path)
                        i_scheme = 'file'
                    else:
                        i_obj = utl_dcc_objects.OsDirectory_(i_path)
                        i_scheme = 'folder'
                    #
                    obj_cur = i_obj
                    #
                    if self._view_mode == 'list':
                        self.__add_item_as_list(i_obj, i_scheme)
                    elif self._view_mode == 'tree':
                        self.__add_item_as_tree(i_obj, i_scheme)
                #
                self.__set_item_selected(obj_cur)
        else:
            pass

    def set_root(self, path):
        self._root_location = path
        self._root_obj = utl_dcc_objects.OsDirectory_(path)

    def set_checked_by_include_paths(self, paths):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path in paths:
                    i.set_checked(True, extra=True)

    def set_unchecked_by_include_paths(self, paths):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path not in paths:
                    i.set_checked(False, extra=True)

    def get(self):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _ if i.get_is_selected()]
        return []

    def get_all(self, check_only=False):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            if check_only is True:
                return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _ if i.get_is_checked() is True]
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _]
        return []

    def connect_value_changed_to(self, fnc):
        self._prx_entry_widget.connect_item_select_changed_to(
            fnc
        )

    def connect_refresh_action_to(self, fnc):
        self._prx_entry_widget.connect_refresh_action_to(fnc)
