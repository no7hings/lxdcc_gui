# coding:utf-8
from lxgui.qt.warp import *

import types

import six

import lxbasic.core as bsc_core

import lxgui.configure as gui_configure

import lxgui.core as gui_core

from lxgui.qt.core import _gui_qt_cor_base

import lxcontent.abstracts as ctt_abstracts


class QtTimer(QtCore.QTimer):
    def __init__(self, *args, **kwargs):
        super(QtTimer, self).__init__(*args, **kwargs)


class QtHBoxLayout(QtWidgets.QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtHBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*gui_configure.Size.LayoutDefaultContentsMargins)
        self.setSpacing(gui_configure.Size.LayoutDefaultSpacing)

    def _set_align_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignTop
        )

    def _set_align_left_(self):
        self.setAlignment(
            QtCore.Qt.AlignLeft
        )

    def _get_all_widgets_(self):
        list_ = []
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                item = layout.itemAt(i)
                if item:
                    widget = item.widget()
                    list_.append(widget)
        return list_

    def _delete_latest_(self):
        layout = self
        c = layout.count()
        if c:
            item = layout.itemAt(c-1)
            if item:
                widget = item.widget()
                widget.close()
                widget.deleteLater()

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.close()
                    i_widget.deleteLater()


class QtVBoxLayout(QtWidgets.QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtVBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*gui_configure.Size.LayoutDefaultContentsMargins)
        self.setSpacing(gui_configure.Size.LayoutDefaultSpacing)

    def _set_align_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop
        )

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.close()
                    i_widget.deleteLater()


class QtGridLayout(QtWidgets.QGridLayout):
    def __init__(self, *args, **kwargs):
        super(QtGridLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*gui_configure.Size.LayoutDefaultContentsMargins)
        self.setSpacing(gui_configure.Size.LayoutDefaultSpacing)

    def _get_widget_count_(self):
        return self.count()

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.deleteLater()

    def _add_widget_(self, widget, d=2):
        c = self.count()

        index = c
        #
        column = index%d
        row = int(index/d)
        self.addWidget(widget, row, column, 1, 1)


class QtFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QtFileDialog, self).__init__(*args, **kwargs)
        self.setPalette(_gui_qt_cor_base.GuiQtUtil.generate_qt_palette())


class QtSystemTrayIcon(QtWidgets.QSystemTrayIcon):
    press_clicked = qt_signal()
    press_db_clicked = qt_signal()
    press_toggled = qt_signal(bool)

    def __init__(self, *args, **kwargs):
        super(QtSystemTrayIcon, self).__init__(*args, **kwargs)
        menu = QtWidgets.QMenu()
        self.setContextMenu(
            menu
        )
        #
        self._window = self.parent()
        self._set_quit_action_add_(menu)
        self.activated.connect(self._set_window_show_normal_)

    def _set_window_show_normal_(self, *args):
        r = args[0]
        # if r == self.Trigger:
        #     # print 'AAA'
        #     # if self._window.isVisible():
        #     #     self._window.hide()
        #     # else:
        #     #     self._window.show()
        #     if self._window.isMinimized():
        #         self._window.showNormal()
        #     else:
        #         self._window.showMinimized()
        if r == self.DoubleClick:
            if self._window.isVisible():
                self._window.hide()
            else:
                self._window.show()

    def _set_quit_action_add_(self, menu):
        widget_action = QtWidgetAction(menu)
        widget_action.setFont(_gui_qt_cor_base.QtFonts.NameNormal)
        widget_action.setText('quit')
        widget_action.setIcon(_gui_qt_cor_base.GuiQtIcon.create_by_icon_name('window/close'))
        menu.addAction(widget_action)
        widget_action.triggered.connect(
            self._window.close
        )


class QtWidgetAction(QtWidgets.QWidgetAction):
    def __init__(self, *args, **kwargs):
        super(QtWidgetAction, self).__init__(*args, **kwargs)
        self.setFont(_gui_qt_cor_base.QtFonts.NameNormal)


class GuiQtMenuOpt(object):
    def __init__(self, menu):
        if isinstance(menu, QtWidgets.QMenu):
            self._root_menu = menu
            self._item_dic = {
                '/': self._root_menu
            }
        else:
            raise RuntimeError()

    @gui_core.GuiModifier.debug_run
    def _set_cmd_debug_run_(self, cmd_str):
        exec cmd_str

    @gui_core.GuiModifier.debug_run
    def _set_fnc_debug_run_(self, fnc):
        fnc()

    def create_by_content(self, content):
        self._root_menu.clear()
        self._item_dic = {
            '/': self._root_menu
        }
        if isinstance(content, ctt_abstracts.AbsContent):
            keys = content.get_keys(regex='*.properties')
            for i_key in keys:
                i_atr_path_opt = bsc_core.DccAttrPathOpt(i_key)
                i_obj_path = i_atr_path_opt.obj_path
                i_obj_path_opt = bsc_core.DccPathDagOpt(i_obj_path)
                i_content = content.get_content(i_key)
                i_type = i_content.get('type')
                if i_obj_path_opt.get_is_root():
                    pass
                else:
                    menu = self.__get_menu_(i_obj_path_opt.get_parent())
                    if i_type == 'separator':
                        self.add_separator_fnc(menu, i_content)
                    elif i_type == 'action':
                        self.add_action_fnc(menu, i_content)

    def __get_menu_(self, path_opt):
        cur_menu = self._root_menu
        components = path_opt.get_components()
        components.reverse()
        for i_component in components:
            cur_menu = self.__get_menu_force_(cur_menu, i_component)
        return cur_menu

    def __get_menu_force_(self, menu, path_opt):
        path = path_opt.path
        if path in self._item_dic:
            return self._item_dic[path]
        #
        name = path_opt.name
        widget_action = QtWidgetAction(menu)
        menu.addAction(widget_action)
        widget_action.setFont(_gui_qt_cor_base.QtFonts.NameNormal)
        widget_action.setText(name)
        widget_action.setIcon(
            _gui_qt_cor_base.GuiQtIcon.create_by_icon_name('file/folder')
        )
        sub_menu = menu.__class__(menu)
        sub_menu.setTearOffEnabled(True)
        widget_action.setMenu(sub_menu)
        self._item_dic[path] = sub_menu
        return sub_menu

    @classmethod
    def add_separator_fnc(cls, menu, content):
        name = content.get('name')
        s = menu.addSeparator()
        s.setFont(_gui_qt_cor_base.QtFonts.MenuSeparator)
        s.setText(name)
        return s

    def add_action_fnc(self, menu, content):
        def set_disable_fnc_(widget_action_):
            widget_action_.setFont(_gui_qt_cor_base.QtFonts.NameDisable)
            widget_action_.setDisabled(True)

        #
        name = content.get('name')
        icon_name = content.get('icon_name')
        executable_fnc = content.get('executable_fnc')
        execute_fnc = content.get('execute_fnc')
        widget_action = QtWidgetAction(menu)
        widget_action.setFont(_gui_qt_cor_base.QtFonts.NameNormal)
        widget_action.setText(name)
        menu.addAction(widget_action)
        if icon_name:
            widget_action.setIcon(
                _gui_qt_cor_base.GuiQtIcon.create_by_icon_name(icon_name)
            )
        else:
            widget_action.setIcon(
                _gui_qt_cor_base.GuiQtIcon.generate_by_text(name, background_color=(64, 64, 64))
            )
        #
        if isinstance(executable_fnc, (bool, int)):
            executable = executable_fnc
            if executable is False:
                set_disable_fnc_(widget_action)
        elif isinstance(executable_fnc, (types.FunctionType, types.MethodType)):
            executable = executable_fnc()
            if executable is False:
                set_disable_fnc_(widget_action)
        #
        if isinstance(execute_fnc, (types.FunctionType, types.MethodType)):
            fnc = execute_fnc
            widget_action.triggered.connect(
                fnc
            )
        elif isinstance(execute_fnc, six.string_types):
            cmd = execute_fnc
            widget_action.triggered.connect(
                lambda *args, **kwargs: self._set_cmd_debug_run_(cmd)
            )
        return widget_action


class GuiQtApplicationOpt(object):
    def __init__(self, app=None):
        if app is None:
            self._instance = QtWidgets.QApplication.instance()
        else:
            self._instance = None

    def set_process_run_0(self):
        if self._instance:
            self._instance.processEvents(
                QtCore.QEventLoop.ExcludeUserInputEvents
            )

    def set_process_run_1(self):
        if self._instance:
            self._instance.processEvents()
