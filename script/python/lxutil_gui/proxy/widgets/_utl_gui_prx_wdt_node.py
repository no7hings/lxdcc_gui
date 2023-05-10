# coding:utf-8
import six

import glob

import os

import functools

import types

from lxbasic import bsc_core

import lxuniverse.abstracts as unr_abstracts
#
from lxutil import utl_core

from lxbasic import bsc_configure
#
import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_view_for_tree


class AttrConfig(object):
    height = 24
    label_width = 64
    PRX_PORT_HEIGHT = 22


class _PrxPortInfo(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtIconPressItem

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
        self.widget._set_checked_(boolean)


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
            '"LMB-click" to use value "default" / "local" / "global"'
        )

    def set(self, boolean):
        self.widget._set_checked_(boolean)


# label
class _PrxPortLabel(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item.QtTextItem
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
    QT_ENTRY_CLASS = None
    def __init__(self, *args, **kwargs):
        super(AbsPrxTypeQtEntry, self).__init__(*args, **kwargs)
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

    def set_use_as_storage(self, boolean=True):
        if hasattr(self._qt_entry_widget, '_set_validator_use_as_storage_'):
            self._qt_entry_widget._set_validator_use_as_storage_(boolean)

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


class _PrxStgObjEntry(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsEnumerate
    def __init__(self, *args, **kwargs):
        super(_PrxStgObjEntry, self).__init__(*args, **kwargs)
        self._history_key = 'gui.storage'
        # self._history_icon_file_path = utl_gui_core.RscIconFile.get('history')
        #
        self._ext_filter = 'All File (*.*)'
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._set_value_entry_popup_enable_(True)
        self._qt_entry_widget._set_value_entry_use_as_storage_(True)
        self._qt_entry_widget._set_value_validation_fnc_(self._value_validation_fnc_)
        self._qt_entry_widget._set_popup_completion_gain_fnc_(self._value_completion_gain_fnc_)
        self._qt_entry_widget._set_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('history')
        )
        self._qt_entry_widget._set_choose_button_sub_icon_file_path_(
            utl_gui_core.RscIconFile.get('down')
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
        self._qt_entry_widget.user_choose_changed.connect(self.set_history_update)
        self._qt_entry_widget._set_value_entry_finished_connect_to_(self.set_history_update)

        self._qt_entry_widget._set_value_entry_popup_enable_(True)

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def get_ext_filter(self):
        return self._ext_filter

    def set_history_key(self, key):
        self._history_key = key
        #
        self.set_history_update()

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
    def set_history_update(self):
        value = self._qt_entry_widget._get_value_()
        if value:
            if self._value_validation_fnc_(value) is True:
                utl_core.History.set_append(
                    self._history_key,
                    value
                )
        #
        histories = utl_core.History.get(
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

    def set_history_show_latest(self):
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
                self.set_history_update()

    def _value_validation_fnc_(self, path):
        return os.path.isfile(path)


class PrxFileSaveEntry(_PrxStgObjEntry):
    def __init__(self, *args, **kwargs):
        super(PrxFileSaveEntry, self).__init__(*args, **kwargs)
        self._qt_open_or_save_button._set_name_text_('save file')
        self._qt_open_or_save_button._set_icon_name_('file/file')
        self._qt_open_or_save_button._set_sub_icon_name_('create')
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
                self.set_history_update()

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
            self.set_history_update()

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
        self._qt_open_or_save_button._set_sub_icon_name_('create')
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
            self.set_history_update()

    def _value_validation_fnc_(self, path):
        return os.path.isdir(path)

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        _ = glob.glob(
            u'{}*'.format(keyword)
        ) or []
        return [i for i in _ if os.path.isdir(i)]


class _PrxStgObjsEntry(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsArray
    def __init__(self, *args, **kwargs):
        super(_PrxStgObjsEntry, self).__init__(*args, **kwargs)
        self._history_key = 'gui.storages'
        #
        self._qt_entry_widget._set_value_entry_popup_enable_(True)
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        self._qt_entry_widget._get_value_entry_gui_()._set_validator_use_as_storage_(True)
        self._qt_entry_widget._get_value_entry_gui_()._set_value_validation_fnc_(self._value_validation_fnc_)
        self._qt_entry_widget._get_value_entry_gui_().entry_added.connect(self.set_history_update)
        self._qt_entry_widget._get_popup_choose_gui_()._set_popup_auto_resize_enable_(True)
        self._qt_entry_widget._set_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('history')
        )

        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)

        self._ext_filter = 'All File (*.*)'

        self._open_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self._qt_entry_widget._set_value_entry_button_add_(self._open_button.widget)
        self._open_button.connect_press_clicked_to(self._set_open_)
        self._open_button.set_name('open file')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_icon_frame_size(18, 18)
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )

    def _set_open_(self):
        raise NotImplementedError()

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

    def set_append(self, raw):
        self._qt_entry_widget._set_value_append_(
            raw
        )

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_values_(
            raw
        )

    def get(self):
        return self._qt_entry_widget._get_values_()

    def set_history_key(self, key):
        self._history_key = key
        self.set_history_update()
        # self.set_history_show_latest()

    def _value_validation_fnc_(self, value):
        return True

    def set_history_update(self):
        values = self._qt_entry_widget._get_values_()
        if values:
            value = values[-1]
            if value:
                if self._value_validation_fnc_(value) is True:
                    utl_core.History.set_append(
                        self._history_key,
                        value
                    )
        #
        histories = utl_core.History.get(
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

    def set_history_show_latest(self):
        _ = utl_core.History.get_latest(self._history_key)
        if _:
            self._qt_entry_widget._set_value_append_(_)

    def set_history_visible(self, boolean):
        pass


# files
class PrxFilesOpenEntry(_PrxStgObjsEntry):
    def __init__(self, *args, **kwargs):
        super(PrxFilesOpenEntry, self).__init__(*args, **kwargs)
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
        self.set_history_key('gui.files-open')

    def _set_open_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getOpenFileNames(
            self.widget,
            'Open Files',
            self.get() or '',
            filter=self._ext_filter
        )
        if s:
            _ = s[0]
            if _:
                [self.set_append(i) for i in _]
                self.set_history_update()

    def _value_validation_fnc_(self, value):
        if value:
            return os.path.isfile(value)
        return False


class PrxEntryForDirectoriesOpen(_PrxStgObjsEntry):
    def __init__(self, *args, **kwargs):
        super(PrxEntryForDirectoriesOpen, self).__init__(*args, **kwargs)
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
        self._qt_entry_widget._set_value_entry_popup_enable_(not boolean)
        self._qt_entry_widget._set_value_entry_choose_enable_(not boolean)
        self._open_button.widget._set_action_enable_(not boolean)

    def set_history_visible(self, boolean):
        self._qt_entry_widget._set_value_entry_choose_visible_(boolean)

    def _set_open_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Open Directory',
            self.get()[-1] if self.get() else '',
        )
        if s:
            self.set_append(s)
            self.set_history_update()

    def _value_validation_fnc_(self, value):
        if value:
            return os.path.isdir(value)
        return False

    def set(self, *args, **kwargs):
        self._qt_entry_widget._set_values_clear_()
        self._qt_entry_widget._set_values_(args[0])


class PrxMediasOpenEntry(_PrxStgObjsEntry):
    def __init__(self, *args, **kwargs):
        super(PrxMediasOpenEntry, self).__init__(*args, **kwargs)
        self._open_button.set_name('open directory')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open directory by "dialog"'
            ]
        )

        self._create_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self._qt_entry_widget._set_value_entry_button_add_(self._create_button.widget)
        self._create_button.connect_press_clicked_to(self._set_create_)
        self._create_button.set_name('create file')
        self._create_button.set_icon_name('camera')
        self._create_button.set_sub_icon_name('create')
        self._create_button.set_icon_frame_size(18, 18)
        self._create_button.set_tool_tip(
            [
                '"LMB-click" create file by "screenshot"'
            ]
        )

        self._qt_entry_widget._set_choose_item_icon_file_path_(utl_gui_core.RscIconFile.get('file/file'))
        self._qt_entry_widget._set_entry_item_icon_file_path_(utl_gui_core.RscIconFile.get('file/file'))

        self.set_history_key('gui.medias-open')

    def _set_open_(self):
        f = utl_gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        _ = self.get()
        if _:
            d = _[0]
        else:
            d = ''

        s = f.getOpenFileNames(
            self.widget,
            'Open Files',
            d,
            filter=self._ext_filter
        )
        if s:
            _ = s[0]
            if _:
                cs = bsc_core.StgFileMultiplyMtd.set_merge_to(
                    _,
                    ['*.####.*']
                )
                [self.set_append(i) for i in cs]

                self.set_history_update()
    @staticmethod
    def _get_tmp_screenshot_file_path_():
        d = bsc_core.SystemMtd.get_home_directory()
        return u'{}/screenshot/scp_{}.jpg'.format(d, bsc_core.TimeExtraMtd.get_time_tag_36())

    def _set_save_(self, g):
        f = self._get_tmp_screenshot_file_path_()
        _utl_gui_prx_wdt_utility.PrxScreenshotFrame.set_save_to(
            g, f
        )
        self.set_append(f)
        self.set_history_update()

    def _set_create_(self):
        active_window = utl_gui_qt_core.get_active_window()
        w = _utl_gui_prx_wdt_utility.PrxScreenshotFrame()
        w.set_started_connect_to(active_window.hide)
        w.set_start()
        w.set_accepted_connect_to(self._set_save_)
        w.set_finished_connect_to(active_window.show)

    def _value_validation_fnc_(self, value):
        # if value:
        #     return os.path.isfile(value)
        # return False
        return True


class _PrxEntryForValueArray(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsArray
    def __init__(self, *args, **kwargs):
        super(_PrxEntryForValueArray, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values'
        #
        self._qt_entry_widget._set_value_entry_popup_enable_(True)
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        self._qt_entry_widget._set_choose_button_icon_file_path_(
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

    def set_append(self, value):
        self._qt_entry_widget._set_value_append_(
            value
        )


class _PrxEntryForValueArrayAsChoose(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsArrayChoose
    def __init__(self, *args, **kwargs):
        super(_PrxEntryForValueArrayAsChoose, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values_choose'
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        self._qt_entry_widget._set_choose_button_icon_file_path_(
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
        self._qt_entry_widget._set_choose_values_clear_()
        self._qt_entry_widget._set_choose_values_(args[0])

    def set_append(self, value):
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
    def get_shotgun_args_fnc(cls, shotgun_entity_kwargs, name_field=None, image_field=None, keyword_filter_fields=None, tag_filter_fields=None):
        """
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
            data = stg_objects.StgConnector().get_shotgun_entities_(
                **shotgun_entity_kwargs
            )
            names = []
            image_url_dict = {}
            keyword_filter_dict = {}
            tag_filter_dict = {}
            for i in data:
                i_key = i[name_field].decode('utf-8')
                names.append(i_key)
                #
                i_image_url = i.get(image_field)
                image_url_dict[i_key] = i_image_url
                if keyword_filter_fields:
                    i_filter_keys = cls.get_shotgun_filter_keys_fnc(
                        i, keyword_filter_fields
                    )
                    keyword_filter_dict[i_key] = i_filter_keys
                #
                if tag_filter_fields:
                    i_filter_keys = cls.get_shotgun_filter_keys_fnc(
                        i, tag_filter_fields
                    )
                    i_filter_keys.insert(0, 'ALL')
                    tag_filter_dict[i_key] = i_filter_keys
            #
            names = bsc_core.RawTextsMtd.set_sort_by_initial(names)
            return names, image_url_dict, keyword_filter_dict, tag_filter_dict


class _PrxEntryAsShotgunEntity(
    AbsPrxTypeQtEntry,
    _AbsShotgunDef
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsEnumerate
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsShotgunEntity, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # popup
        self._qt_entry_widget._set_value_entry_popup_enable_(True)
        # entry
        self._qt_entry_widget._set_value_entry_enable_(True)
        # choose
        self._qt_entry_widget._set_choose_popup_auto_resize_enable_(False)
        self._qt_entry_widget._set_choose_index_showable_(True)
        self._qt_entry_widget._set_choose_tag_filter_enable_(True)
        self._qt_entry_widget._set_choose_keyword_filter_enable_(True)
        self._qt_entry_widget._set_choose_item_size_(40, 40)
        self._qt_entry_widget._set_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('entity')
        )

        self._data = []

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, *args, **kwargs):
        pass

    def set_shotgun_entity_kwargs(self, shotgun_entity_kwargs, name_field=None, image_field=None, keyword_filter_fields=None, tag_filter_fields=None):
        args = self.get_shotgun_args_fnc(
            shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
        )
        if args:
            names, image_url_dict, keyword_filter_dict, tag_filter_dict = args
            #
            self._qt_entry_widget._set_choose_values_(names)
            self._qt_entry_widget._set_choose_image_url_dict_(image_url_dict)
            self._qt_entry_widget._set_choose_keyword_filter_dict_(keyword_filter_dict)
            self._qt_entry_widget._set_choose_tag_filter_dict_(tag_filter_dict)
            if names:
                self._qt_entry_widget._set_value_(names[0])


class _PrxEntryAsShotgunEntities(
    AbsPrxTypeQtEntry,
    _AbsShotgunDef
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsArray
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsShotgunEntities, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # popup
        self._qt_entry_widget._set_value_entry_popup_enable_(True)
        self._qt_entry_widget._set_value_entry_enable_(True)
        # resize
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()
        #
        self._qt_entry_widget._set_choose_tag_filter_enable_(True)
        self._qt_entry_widget._set_choose_keyword_filter_enable_(True)
        self._qt_entry_widget._set_choose_item_size_(40, 40)
        self._qt_entry_widget._set_choose_button_icon_file_path_(
            utl_gui_core.RscIconFile.get('entity')
        )

        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)

        self._data = []

    def get(self):
        return self._qt_entry_widget._get_values_()

    def set(self, raw=None, **kwargs):
        pass

    def set_append(self, value):
        self._qt_entry_widget._set_value_append_(
            value
        )

    def set_shotgun_entity_kwargs(self, shotgun_entity_kwargs, name_field=None, image_field=None, keyword_filter_fields=None, tag_filter_fields=None):
        args = self.get_shotgun_args_fnc(
            shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
        )
        if args:
            names, image_url_dict, keyword_filter_dict, tag_filter_dict = args
            #
            self._qt_entry_widget._set_choose_values_(names)
            self._qt_entry_widget._set_choose_image_url_dict_(image_url_dict)
            self._qt_entry_widget._set_choose_keyword_filter_dict_(keyword_filter_dict)
            self._qt_entry_widget._set_choose_tag_filter_dict_(tag_filter_dict)


class _PrxEntryAsRsvProject(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsEnumerate
    #
    HISTORY_KEY = 'gui.projects'
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsRsvProject, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        #
        self.set_history_update()
        #
        self._qt_entry_widget._set_value_entry_finished_connect_to_(self.set_history_update)
        self._qt_entry_widget.user_choose_changed.connect(self.set_history_update)

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
    def set_history_update(self):
        project = self._qt_entry_widget._get_value_()
        if project:
            import lxresolver.commands as rsv_commands
            resolver = rsv_commands.get_resolver()
            #
            rsv_project = resolver.get_rsv_project(project=project)
            project_directory_path = rsv_project.get_directory_path()
            work_directory_path = '{}/work'.format(project_directory_path)
            if bsc_core.StgPathOpt(work_directory_path).get_is_exists() is True:
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
            self._qt_entry_widget._set_choose_values_(
                histories
            )

    def set_history_show_latest(self):
        _ = utl_core.History.get_latest(self.HISTORY_KEY)
        if _:
            self._qt_entry_widget._set_value_(_)

    def get_histories(self):
        return utl_core.History.get(
            self.HISTORY_KEY
        )


class PrxEntryForSchemeAsChoose(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsEnumerate
    #
    HISTORY_KEY = 'gui.schemes'
    def __init__(self, *args, **kwargs):
        super(PrxEntryForSchemeAsChoose, self).__init__(*args, **kwargs)
        #
        self._qt_entry_widget._set_value_entry_enable_(True)
        #
        self._scheme_key = None
        #
        self.set_history_update()
        #
        self._qt_entry_widget._set_value_entry_finished_connect_to_(self.set_history_update)
        self._qt_entry_widget.user_choose_changed.connect(self.set_history_update)

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.set_history_add(raw[0])
            self.set_history_update()
            self.set_history_show_latest()

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
            scheme = self._qt_entry_widget._get_value_()
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
                self._qt_entry_widget._set_choose_values_(
                    histories
                )

    def set_history_show_latest(self):
        if self._scheme_key is not None:
            _ = utl_core.History.get_latest(self._scheme_key)
            if _:
                self._qt_entry_widget._set_value_(_)


class _PrxEntryAsConstant(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsConstant
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsConstant, self).__init__(*args, **kwargs)
        # self._qt_entry_widget.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft | utl_gui_qt_core.QtCore.Qt.AlignVCenter)
        #
        self.widget.setFocusProxy(self._qt_entry_widget)

    def set_value_type(self, value_type):
        self._qt_entry_widget._set_value_type_(value_type)

    def set_use_as_frames(self):
        self._qt_entry_widget._set_validator_use_as_frames_()

    def set_use_as_rgba(self):
        self._qt_entry_widget._set_validator_use_as_rgba_()

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
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsEnumerate
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


class _PrxEntryAsCapsule(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsCapsule
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsCapsule, self).__init__(*args, **kwargs)

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, *args, **kwargs):
        self._qt_entry_widget._set_value_(
            args[0]
        )

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
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsTuple
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
        self._qt_entry_widget._build_entry_(2, int)


class _PrxEntryAsFloatTuple(_PrxEntryAsTuple):
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsFloatTuple, self).__init__(*args, **kwargs)
        self._qt_entry_widget._build_entry_(2, float)


class _PrxEntryAsRgba(_PrxEntryAsConstant):
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtaValueEntryAsRgba
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsRgba, self).__init__(*args, **kwargs)
        # self._qt_entry_widget._build_entry_(3, float)


class _PrxEntryAsBoolean(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtCheckItem
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
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtValueEntryAsScript
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsScript, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(92)
        self.widget.setMinimumHeight(92)
        #
        self._qt_entry_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_entry_widget._set_resize_enable_(True)
        self._qt_entry_widget._set_item_value_entry_enable_(True)
        self._qt_entry_widget._set_size_policy_height_fixed_mode_()

    def get(self):
        return self._qt_entry_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_entry_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_entry_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_entry_widget._get_value_is_default_()

    def set_locked(self, boolean):
        self._qt_entry_widget._set_value_entry_enable_(not boolean)


class _PrxEntryAsButton(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtPressItem
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

    def set_menu_raw(self, raw):
        self._qt_entry_widget._set_menu_raw_(raw)

    def set_option_enable(self, boolean):
        self._qt_entry_widget._set_item_option_click_enable_(boolean)


class PrxSubProcessEntry(AbsPrxTypeQtEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxSubProcessEntry, self).__init__(*args, **kwargs)
        self._stop_button = _utl_gui_prx_wdt_utility.PrxIconPressItem()
        self.set_button_add(self._stop_button)
        self._stop_button.set_name('Stop Process')
        self._stop_button.set_icon_by_name('Stop Process')
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

    def set_menu_raw(self, raw):
        self._qt_entry_widget._set_menu_raw_(raw)

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
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    QT_ENTRY_CLASS = _utl_gui_qt_wgt_item.QtPressItem
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

    def set_menu_raw(self, raw):
        self._qt_entry_widget._set_menu_raw_(raw)


class _AbsPrxTypeEntry(utl_gui_prx_abstract.AbsPrxWidget):
    PRX_ENTRY_CLASS = None
    def __init__(self, *args, **kwargs):
        super(_AbsPrxTypeEntry, self).__init__(*args, **kwargs)

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

    def get_default(self):
        return None

    def set_default(self, raw=None, **kwargs):
        pass

    def get_is_default(self):
        return False

    def set_tool_tip(self, *args, **kwargs):
        if hasattr(self._prx_entry_widget._qt_widget, '_set_tool_tip_'):
            self._prx_entry_widget._qt_widget._set_tool_tip_(args[0], **kwargs)

    def set_clear(self):
        pass

    def connect_value_changed_to(self, fnc):
        pass

    def set_locked(self, boolean):
        pass


class _PrxEntryAsRsvObj(_AbsPrxTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLASS = _utl_gui_prx_wgt_view_for_tree.PrxTreeView
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
                prx_item = prx_item_parent.set_child_add(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_entry_widget.set_item_add(
                    **create_kwargs
                )
            # prx_item.set_checked(True)
            prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
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
        prx_item.set_icon_by_name(obj_type_name)
        prx_item.set_names([obj_name, update])
        prx_item.set_tool_tip(obj.description)
        if result:
            if bsc_core.StgPathOpt(result).get_is_file():
                prx_item.set_icon_by_file(utl_dcc_objects.OsFile(result).icon)
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def __add_item_as_tree_(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._obj_add_dict:
                    self.__set_item_comp_add_as_tree_(i_rsv_obj, use_show_thread=True)
        #
        self.__set_item_comp_add_as_tree_(obj, use_show_thread=True)

    def __add_item_as_list_(self, obj):
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
        prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
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
                        self.__add_item_as_list_(i)
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

    def connect_value_changed_to(self, fnc):
        self._prx_entry_widget.connect_item_select_changed_to(
            fnc
        )


class _PrxEntryAsNodes(_AbsPrxTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLASS = _utl_gui_prx_wgt_view_for_tree.PrxTreeView
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
                prx_item = prx_item_parent.set_child_add(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_entry_widget.set_item_add(
                    **create_kwargs
                )
            #
            prx_item.set_checked(False)
            prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
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
                    ('Expand branch', None, prx_item.set_expand_branch),
                    ('Collapse branch', None, prx_item.set_collapse_branch),
                ]
            )
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        # self._prx_entry_widget.set_loading_update()
    #
    def __add_item_as_tree_(self, obj):
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

    def __add_item_as_list_(self, obj):
        path = obj.path
        type_name = obj.type_name
        #
        create_kwargs = dict(
            name='loading ...',
            icon_name_text=type_name,
            filter_key=path
        )
        prx_item = self._prx_entry_widget.set_item_add(
            **create_kwargs
        )
        #
        prx_item.set_checked(False)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._obj_add_dict[path] = prx_item
        #
        self.__set_item_show_deferred_(prx_item, use_as_tree=False)

    def __set_item_selected_(self, obj):
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
                        self.__add_item_as_list_(i)
                    elif self._view_mode == 'tree':
                        self.__add_item_as_tree_(i)
                #
                self.__set_item_selected_(
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


class _PrxEntryAsFiles(_AbsPrxTypeEntry):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PRX_ENTRY_CLASS = _utl_gui_prx_wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'storage'
    def __init__(self, *args, **kwargs):
        super(_PrxEntryAsFiles, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(162)
        self.widget.setMinimumHeight(162)
        self._prx_entry_widget.set_header_view_create(
            [('name', 3), ('update', 1)],
            480+160
        )
        self._prx_entry_widget.set_selection_use_single()
        self._prx_entry_widget.set_size_policy_height_fixed_mode()
        self._prx_entry_widget.set_resize_target(self.widget)
        self._prx_entry_widget.set_resize_enable(True)
        self._prx_entry_widget.set_resize_minimum(82)
        #
        self._obj_add_dict = self._prx_entry_widget._item_dict

        self._root_location = None

        self._view_mode = 'list'

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
            prx_item = prx_item_parent.set_child_add(
                **create_kwargs
            )
        else:
            prx_item = self._prx_entry_widget.set_item_add(
                **create_kwargs
            )
        #
        prx_item.set_checked(False)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._obj_add_dict[path] = prx_item
        #
        prx_item.set_show_method(
            lambda *args, **kwargs: self.__set_item_show_deferred_(prx_item, scheme)
        )
        return True, prx_item, None

    def __set_item_show_deferred_(self, prx_item, scheme, use_as_tree=True):
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

        prx_item.set_names([obj.get_name(), update])
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
                    ('Expand branch', None, prx_item.set_expand_branch),
                    ('Collapse branch', None, prx_item.set_collapse_branch),
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
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
    #
    def __add_item_as_tree_(self, obj, scheme):
        if self._root_location is not None:
            i_is_create, i_prx_item, _ = self.__add_item_as_list_(self._root_obj, scheme)
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

    def __add_item_as_list_(self, obj, scheme):
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
        prx_item = self._prx_entry_widget.set_item_add(
            **create_kwargs
        )
        #
        prx_item.set_checked(False)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._obj_add_dict[path] = prx_item
        #
        prx_item.set_show_method(
            lambda *args, **kwargs: self.__set_item_show_deferred_(prx_item, scheme)
        )
        return True, prx_item, None

    def __set_item_selected_(self, obj):
        item = obj.get_obj_gui()
        self._prx_entry_widget.set_item_selected(
            item, exclusive=True
        )

    def restore(self):
        self._prx_entry_widget.set_clear()

    def set_view_mode(self, mode):
        self._view_mode = mode

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.restore()
            paths = raw
            if paths:
                obj_cur = None
                for i_path in paths:
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
                        self.__add_item_as_list_(i_obj, i_scheme)
                    elif self._view_mode == 'tree':
                        self.__add_item_as_tree_(i_obj, i_scheme)
                #
                self.__set_item_selected_(obj_cur)
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

    def get_all(self):
        _ = self._prx_entry_widget.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _]
        return []

    def connect_value_changed_to(self, fnc):
        self._prx_entry_widget.connect_item_select_changed_to(
            fnc
        )

    def connect_refresh_action_to(self, fnc):
        self._prx_entry_widget.connect_refresh_action_to(fnc)


# port =============================================================================================================== #
class AbsPrxPortDef(object):
    ENTRY_TYPE = 'custom'
    def _set_prx_port_def_init_(self, category, path, label=None):
        self._prx_node = None
        #
        self._category = category
        self._port_path = path
        self._name = self._port_path.split('.')[-1]
        #
        if label is not None:
            self._label = label
        else:
            self._label = bsc_core.RawStringUnderlineOpt(self._name).to_prettify(capitalize=False)

    def _set_node_(self, obj):
        self._prx_node = obj

    def get_node(self):
        return self._prx_node

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
    ENTRY_TYPE = 'custom'
    ENABLE_CLASS = None
    LABEL_CLASS = None
    LABEL_HIDED = False
    KEY_HIDE = False
    ENTRY_CLASS = None
    def __init__(self, path, label=None, enable=None, default_value=None, join_to_next=False, scheme_key=None, node_widget=None):
        self._set_prx_port_def_init_('value', path, label)
        #
        self._key = None
        #
        if isinstance(enable, bool):
            self._use_enable = enable
        else:
            self._use_enable = False
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
            ),
            name='label for "{}"'.format(self._label)
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
        self._key_widget = None
        #
        self._custom_widget = None
        #
        self.set_name(self.label)

        self.connect_value_changed_to(
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

    def set_append(self, raw):
        if hasattr(self._prx_port_entry, 'set_append'):
            self._prx_port_entry.set_append(raw)

    def set_clear(self):
        self._prx_port_entry.set_clear()

    def set_reset(self):
        default = self.get_default()
        if default is not None:
            self.set(default)

    def set_option(self, value):
        self._prx_port_entry.set_option(value)

    def set_tool_tip(self, *args, **kwargs):
        kwargs['name'] = '{} entry for "{}"'.format(
            self.ENTRY_TYPE,
            self._label,
        )
        self._prx_port_entry.set_tool_tip(*args, **kwargs)

    def get(self):
        return self._prx_port_entry.get()

    def connect_value_changed_to(self, fnc):
        self._prx_port_entry.connect_value_changed_to(fnc)

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
                utl_gui_core.RscIconFile.get('radio_unchecked'),
                utl_gui_core.RscIconFile.get('radio_checked')
            )
            i_qt_widget.user_check_clicked.connect(
                functools.partial(
                    exclusive_fnc_, i_p
                )
            )


class PrxConstantPort(AbsPrxTypePort):
    ENTRY_TYPE = 'constant'
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = _PrxEntryAsConstant
    def __init__(self, *args, **kwargs):
        super(PrxConstantPort, self).__init__(*args, **kwargs)

    def set_locked(self, boolean):
        self._prx_port_entry.set_locked(boolean)


class PrxTextPort(PrxConstantPort):
    ENTRY_TYPE = 'text'
    ENTRY_CLASS = PrxTextEntry
    def __init__(self, *args, **kwargs):
        super(PrxTextPort, self).__init__(*args, **kwargs)


class PrxPortForString(PrxConstantPort):
    ENTRY_TYPE = 'string'
    ENTRY_CLASS = _PrxEntryAsString
    def __init__(self, *args, **kwargs):
        super(PrxPortForString, self).__init__(*args, **kwargs)


class PrxPortForName(PrxConstantPort):
    ENTRY_TYPE = 'name'
    ENTRY_CLASS = _PrxEntryAsString
    def __init__(self, *args, **kwargs):
        super(PrxPortForName, self).__init__(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_value_entry_validator_use_as_name_()


class PrxFramesPort(PrxConstantPort):
    ENTRY_TYPE = 'frames'
    ENTRY_CLASS = _PrxEntryAsString
    def __init__(self, *args, **kwargs):
        super(PrxFramesPort, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_use_as_frames()


class PrxIntegerPort(PrxConstantPort):
    ENTRY_TYPE = 'integer'
    ENTRY_CLASS = _PrxEntryAsInteger
    def __init__(self, *args, **kwargs):
        super(PrxIntegerPort, self).__init__(*args, **kwargs)


class PrxFloatPort(PrxConstantPort):
    ENTRY_TYPE = 'float'
    ENTRY_CLASS = _PrxEntryAsFloat
    def __init__(self, *args, **kwargs):
        super(PrxFloatPort, self).__init__(*args, **kwargs)


class _PrxStgObjPort(PrxConstantPort):
    ENTRY_CLASS = _PrxStgObjEntry
    def __init__(self, *args, **kwargs):
        super(_PrxStgObjPort, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self._prx_port_entry.set_ext_filter(ext_filter)

    def set_history_show_latest(self):
        self._prx_port_entry.set_history_show_latest()

    def set_history_key(self, key):
        self._prx_port_entry.set_history_key(key)


class PrxFileOpenPort(_PrxStgObjPort):
    ENTRY_CLASS = PrxFileOpenEntry
    def __init__(self, *args, **kwargs):
        super(PrxFileOpenPort, self).__init__(*args, **kwargs)


class PrxFileSavePort(_PrxStgObjPort):
    ENTRY_CLASS = PrxFileSaveEntry
    def __init__(self, *args, **kwargs):
        super(PrxFileSavePort, self).__init__(*args, **kwargs)


class PrxDirectoryOpenPort(_PrxStgObjPort):
    ENTRY_CLASS = PrxDirectoryOpenEntry
    def __init__(self, *args, **kwargs):
        super(PrxDirectoryOpenPort, self).__init__(*args, **kwargs)


class PrxDirectorySavePort(_PrxStgObjPort):
    ENTRY_CLASS = PrxDirectorySaveEntry
    def __init__(self, *args, **kwargs):
        super(PrxDirectorySavePort, self).__init__(*args, **kwargs)


class PrxPortForRsvProject(PrxConstantPort):
    ENTRY_CLASS = _PrxEntryAsRsvProject
    def __init__(self, *args, **kwargs):
        super(PrxPortForRsvProject, self).__init__(*args, **kwargs)

    def get_histories(self):
        return self.entry_widget.get_histories()

    def set_history_show_latest(self):
        self._prx_port_entry.set_history_show_latest()


class PrxSchemChoosePort(PrxConstantPort):
    ENTRY_CLASS = PrxEntryForSchemeAsChoose
    def __init__(self, *args, **kwargs):
        super(PrxSchemChoosePort, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_scheme_key(kwargs['scheme_key'])


class PrxPortAsBoolean(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = True
    ENTRY_CLASS = _PrxEntryAsBoolean
    def __init__(self, *args, **kwargs):
        super(PrxPortAsBoolean, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._prx_port_entry._qt_entry_widget._set_name_text_(text)


class PrxPortAsEnumerate(AbsPrxTypePort):
    ENTRY_TYPE = 'enumerate'
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = _PrxEntryAsEnumerate
    def __init__(self, *args, **kwargs):
        super(PrxPortAsEnumerate, self).__init__(*args, **kwargs)

    def get_enumerate_strings(self):
        return self._prx_port_entry.get_enumerate_strings()

    def set_icon_file_as_value(self, value, file_path):
        self._prx_port_entry.set_icon_file_as_value(value, file_path)


class PrxPortAsCapsuleString(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsCapsule
    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleString, self).__init__(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_capsule_use_exclusive_(
            True
        )


class PrxPortAsCapsuleStrings(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsCapsule
    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleStrings, self).__init__(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_capsule_use_exclusive_(
            False
        )


class PrxPortAsScript(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsScript
    def __init__(self, *args, **kwargs):
        super(PrxPortAsScript, self).__init__(*args, **kwargs)


class PrxPortAsTuple(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = _PrxEntryAsTuple
    def __init__(self, *args, **kwargs):
        super(PrxPortAsTuple, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._prx_port_entry.set_value_type(value_type)

    def set_value_size(self, size):
        self._prx_port_entry.set_value_size(size)


class PrxPortForIntegerTuple(PrxPortAsTuple):
    ENTRY_CLASS = _PrxEntryAsIntegerTuple
    def __init__(self, *args, **kwargs):
        super(PrxPortForIntegerTuple, self).__init__(*args, **kwargs)


class PrxPortForFloatTuple(PrxPortAsTuple):
    ENTRY_CLASS = _PrxEntryAsFloatTuple
    def __init__(self, *args, **kwargs):
        super(PrxPortForFloatTuple, self).__init__(*args, **kwargs)


class PrxRgbaPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    ENTRY_CLASS = _PrxEntryAsRgba
    def __init__(self, *args, **kwargs):
        super(PrxRgbaPort, self).__init__(*args, **kwargs)
        self._prx_port_entry.set_use_as_rgba()


class PrxPortAsButton(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    ENTRY_CLASS = _PrxEntryAsButton
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
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    ENTRY_CLASS = PrxSubProcessEntry
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

    def set_initialization(self, count, status=bsc_configure.Status.Started):
        self._prx_port_entry._qt_entry_widget._set_sub_process_initialization_(count, status)

    def set_restore(self):
        self._prx_port_entry._qt_entry_widget._set_sub_process_restore_()

    def set_status_at(self, index, status):
        widget = self._prx_port_entry._qt_entry_widget
        widget.rate_status_update_at.emit(index, status)

    def set_finished_at(self, index, status):
        widget = self._prx_port_entry._qt_entry_widget
        widget.rate_finished_at.emit(index, status)

    def set_finished_connect_to(self, fnc):
        widget = self._prx_port_entry._qt_entry_widget
        widget._set_sub_process_finished_connect_to_(fnc)

    def set_stop_connect_to(self, fnc):
        self._prx_port_entry.set_stop_connect_to(fnc)

    def set_stopped(self, boolean=True):
        self._is_stopped = boolean
        # self.set_restore()

    def get_is_stopped(self):
        return self._is_stopped


class PrxValidatorPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    ENTRY_CLASS = PrxValidatorEntry
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

    def set_restore(self):
        self._prx_port_entry._qt_entry_widget._set_validator_restore_()

    def set_status_at(self, index, status):
        self._prx_port_entry._qt_entry_widget._set_validator_status_at_(index, status)


class PrxRsvObjChoosePort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsRsvObj
    def __init__(self, *args, **kwargs):
        super(PrxRsvObjChoosePort, self).__init__(*args, **kwargs)


class _PrxStgObjsPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxStgObjsEntry
    def __init__(self, *args, **kwargs):
        super(_PrxStgObjsPort, self).__init__(*args, **kwargs)


class PrxFilesOpenPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = PrxFilesOpenEntry
    def __init__(self, *args, **kwargs):
        super(PrxFilesOpenPort, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxFilesOpenPort, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def set_history_visible(self, boolean):
        self._prx_port_entry.set_history_visible(boolean)


class PrxDirectoriesOpenPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = PrxEntryForDirectoriesOpen
    def __init__(self, *args, **kwargs):
        super(PrxDirectoriesOpenPort, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxDirectoriesOpenPort, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def set_history_visible(self, boolean):
        self._prx_port_entry.set_history_visible(boolean)


class PrxMediasOpenPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = PrxMediasOpenEntry
    def __init__(self, *args, **kwargs):
        super(PrxMediasOpenPort, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxMediasOpenPort, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def set_ext_filter(self, ext_filter):
        self._prx_port_entry.set_ext_filter(ext_filter)


class PrxPortForValueArray(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryForValueArray
    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArray, self).__init__(*args, **kwargs)

    def set_append(self, value):
        self._prx_port_entry.set_append(value)


class PrxPortForValueArrayAsChoose(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryForValueArrayAsChoose
    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def set_append(self, value):
        self._prx_port_entry.set_append(value)


class PrxPortAsShotgunEntity(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsShotgunEntity
    def __init__(self, *args, **kwargs):
        super(PrxPortAsShotgunEntity, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsShotgunEntity, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def set_append(self, value):
        self._prx_port_entry.set_append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_entry.set_shotgun_entity_kwargs(*args, **kwargs)


class PrxPortAsShotgunEntities(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsShotgunEntities
    def __init__(self, *args, **kwargs):
        super(PrxPortAsShotgunEntities, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsShotgunEntities, self).set_name(*args, **kwargs)
        self._prx_port_entry._qt_entry_widget._set_name_text_(args[0])

    def set_append(self, value):
        self._prx_port_entry.set_append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_entry.set_shotgun_entity_kwargs(*args, **kwargs)


class PrxNodeListViewPort(AbsPrxTypePort):
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsNodes
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
    ENABLE_CLASS = _PrxPortStatus
    LABEL_CLASS = _PrxPortLabel
    LABEL_HIDED = False
    ENTRY_CLASS = _PrxEntryAsFiles
    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileList, self).__init__(*args, **kwargs)

    def restore(self):
        self._prx_port_entry.restore()

    def get_all(self):
        return self._prx_port_entry.get_all()

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


class PrxNode(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLASS = PrxPortStack
    LABEL_WIDTH = 160
    PORT_CLASS_DICT = dict(
        string=PrxPortForString,
        interge=PrxIntegerPort,
        float=PrxFloatPort,
        button=PrxPortAsButton,
        enumerate=PrxPortAsEnumerate
    )
    @classmethod
    def get_port_cls(cls, type_name):
        return cls.PORT_CLASS_DICT[type_name]

    def __init__(self, *args, **kwargs):
        super(PrxNode, self).__init__(*args, **kwargs)
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        #
        qt_splitter_0 = _utl_gui_qt_wgt_utility.QtHSplitter_()
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
    ENTRY_TYPE = 'group'
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
        self._port_layout = self._prx_widget._layout
        self._port_layout.setContentsMargins(8, 0, 0, 0)
        self._port_layout.setSpacing(2)
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

    def create_child_group(self, name):
        if self.get_is_root() is True:
            path = name
        else:
            path = '{}.{}'.format(self._port_path, name)
        #
        group_port = self.__class__(path)
        group_port._prx_widget.set_name_font_size(8)
        group_port._prx_widget.set_name_icon_enable(False)
        group_port._prx_widget.set_expand_icon_names(
            'qt-style/branch-open', 'qt-style/branch-close'
        )
        group_port._prx_widget.widget._set_line_draw_enable_(True)
        self._port_layout.addWidget(group_port._prx_widget._qt_widget)
        self._port_stack.set_object_add(group_port)
        return group_port

    def set_child_add(self, port):
        cur_port = port
        pre_port_is_join_next, pre_port = self._get_pre_child_args_()
        cur_port_is_join_next = cur_port._get_is_join_next_()
        #
        condition = pre_port_is_join_next, cur_port_is_join_next
        if condition == (False, False):
            port_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            self._port_layout.addWidget(port_widget)
            cur_port_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(port_widget)
            cur_port_layout.setContentsMargins(0, 0, 0, 0)
            cur_port_layout._set_align_top_()
            cur_port._set_layout_(cur_port_layout)
            #
            cur_key_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            cur_key_widget.hide()
            cur_port._set_key_widget_(cur_key_widget)
            cur_port_layout.addWidget(cur_key_widget)
            cur_key_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(cur_key_widget)
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
            port_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            self._port_layout.addWidget(port_widget)
            cur_port_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(port_widget)
            cur_port_layout.setContentsMargins(0, 0, 0, 0)
            cur_port_layout._set_align_top_()
            cur_port._set_layout_(cur_port_layout)
            cur_key_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            # cur_key_widget.hide()
            cur_port._set_key_widget_(cur_key_widget)
            cur_port_layout.addWidget(cur_key_widget)
            cur_key_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(cur_key_widget)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_top_()
            # + key
            cur_key_layout.addWidget(cur_port._prx_port_enable._qt_widget)
            cur_key_layout.addWidget(cur_port._prx_port_label._qt_widget)
            # + value
            cur_port_layout.addWidget(cur_port._prx_port_entry._qt_widget)
            # value
            next_port_widget = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
            cur_port_layout.addWidget(next_port_widget)
            next_port_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(next_port_widget)
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

    def set_label_width_update(self):
        width = self.get_label_width_maximum()
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

    def set_visible_condition(self, condition):
        def visible_fnc_():
            _operator = condition.get('operator')
            _value_0 = condition.get('value')
            _value = p.get()
            if _operator == 'in':
                self.set_visible(_value_0 in _value)
            elif _operator == 'is':
                self.set_visible(_value_0 == _value)

        if condition:
            p = self.get_node().get_port(condition.get('port'))
            if p is not None:
                p.connect_value_changed_to(visible_fnc_)
                visible_fnc_()
            else:
                bsc_core.LogMtd.trace_method_warning(
                    'visible condition connect',
                    'port="{}" is non-exists'.format(condition.get('port'))
                )

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


class PrxNodePortStack_(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PrxNodePortStack_, self).__init__()

    def get_key(self, obj):
        return obj.get_port_path()


class PrxNode_(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    PORT_STACK_CLASS = PrxNodePortStack_
    PORT_CLASS_DICT = dict(
        string=PrxPortForString,
        interge=PrxIntegerPort,
        float=PrxFloatPort,
        button=PrxPortAsButton,
        enumerate=PrxPortAsEnumerate
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
        group = self.create_group(port.get_group_path())
        self._set_port_register_(port)
        return group.set_child_add(port)

    def create_group(self, group_path):
        root_port = self.get_port_root()
        current_group = root_port
        if group_path:
            group_names = group_path.split('.')
            for i_group_name in group_names:
                i_group_port = current_group.get_child(i_group_name)
                if i_group_port is None:
                    i_group_port = current_group.create_child_group(i_group_name)
                    self._set_port_register_(i_group_port)
                #
                current_group = i_group_port
        return current_group

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
            if i_port.get_category() not in {'group'}:
                value = i_port.get()
                dic[key] = value
        return dic

    def set_name_width(self, w):
        self._name_width = w
        # self._prx_port_root._qt_label_widget.setFixedWidth(self._name_width)

    def create_ports_by_configure(self, configure):
        for k, v in configure.items():
            self.create_port_by_data(k.replace('/', '.'), v)

    def create_port_by_data(self, port_path, option):
        widget_ = option['widget']
        label_ = option.get('label')
        #
        if widget_ in {'group'}:
            group = self.create_group(port_path)
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
            port = PrxPortForString(
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
            port = PrxPortForName(
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
            port = PrxIntegerPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'float'}:
            port = PrxFloatPort(
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
        elif widget_ in {'rgb'}:
            port = PrxRgbaPort(
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
            port = PrxPortAsEnumerate(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            #
            current_ = option.get('current') or option.get('default')
            current_index_ = option.get('current_index')
            if current_ is not None:
                port.set(current_)
                port.set_default(current_)
            elif current_index_ is not None:
                port.set(current_index_)
                port.set_default(current_index_)
            else:
                if value_:
                    port.set(value_[-1])
                    port.set_default(value_[-1])
        #
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
                port = PrxFileSavePort(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxFileOpenPort(
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
                port.set_history_show_latest()
            #
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
        elif widget_ in {'files'}:
            port = PrxFilesOpenPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

            if 'history_visible' in option:
                port.set_history_visible(option['history_visible'])
        #
        elif widget_ in {'directory'}:
            open_or_save_ = option.get('open_or_save')
            if open_or_save_ == 'save':
                port = PrxDirectorySavePort(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxDirectoryOpenPort(
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
                port.set_history_show_latest()
        elif widget_ in {'directories'}:
            port = PrxDirectoriesOpenPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

            if 'history_visible' in option:
                port.set_history_visible(option['history_visible'])
        #
        elif widget_ in {'medias'}:
            port = PrxMediasOpenPort(
                port_path,
                node_widget=self.widget
            )
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            ext_filter = option.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)
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
            port = PrxPortForRsvProject(
                port_path,
                node_widget=self.widget
            )
            if value_:
                port.set(value_)

            show_history_latest = option.get('show_history_latest')
            if show_history_latest:
                port.set_history_show_latest()
        elif widget_ in {'rsv-obj'}:
            port = PrxRsvObjChoosePort(
                port_path,
                node_widget=self.widget
            )
            # port.set(value_)
        elif widget_ in {'scheme'}:
            port = PrxSchemChoosePort(
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
        port.ENTRY_TYPE = widget_
        port.set_key(key_)
        port.set_label(label_)
        port.set_use_enable(enable_)
        port.set_tool_tip(tool_tip_)
        port.set_join_to_next(join_to_next_)
        port.set_locked(lock_)

        self.set_port_add(port)

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
            utl_core.Log.set_module_warning_trace(
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
