# coding:utf-8
from lxgui.qt.warp import *

import lxlog.core as log_core

import lxbasic.core as bsc_core

import lxgui.abstracts as gui_abstracts

from lxgui.qt.core import _gui_qt_cor_base


class GuiQtMaya(object):
    @classmethod
    def get_qt_object(cls, ptr, base=QtWidgets.QWidget):
        from shiboken2 import wrapInstance

        return wrapInstance(long(ptr), base)

    @classmethod
    def get_qt_menu_bar(cls):
        qt_main_window = cls.get_qt_main_window()
        if qt_main_window:
            children = qt_main_window.children()
            for i_child in children:
                if i_child:
                    if isinstance(i_child, QtWidgets.QMenuBar):
                        return i_child

    @classmethod
    def get_qt_menu(cls, text):
        qt_menu_bar = cls.get_qt_menu_bar()
        if qt_menu_bar:
            children = qt_menu_bar.children()
            for i_child in children:
                if isinstance(i_child, QtWidgets.QMenu):
                    i_name = i_child.title()
                    if i_name == text:
                        return i_child

    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        from maya import OpenMayaUI

        #
        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window:
            return cls.get_qt_object(
                main_window,
                QtWidgets.QMainWindow
            )

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        # noinspection PyUnresolvedReferences
        from maya import OpenMayaUI

        ptr = OpenMayaUI.MQtUtil.createIcon(icon_name)
        if ptr is None:
            ptr = OpenMayaUI.MQtUtil.createIcon('default')
        return cls.get_qt_object(ptr, QtGui.QIcon)

    @classmethod
    def find_all_qt_widgets_by_class(cls, *args, **kwargs):
        return _gui_qt_cor_base.GuiQtUtil.find_all_qt_widgets_by_class(*args, **kwargs)

    @classmethod
    def _test(cls):
        # # noinspection PyUnresolvedReferences
        # from maya import cmds, mel, OpenMayaUI
        # from shiboken2 import wrapInstance, getCppPointer
        # width, height = 400, 400
        # control_name = 'lynxi_tool'
        # control_label = 'Lynxi Tool'
        # if cmds.workspaceControl(control_name, query=1, exists=1):
        #     cmds.workspaceControl(
        #         control_name, edit=1, visible=1, restore=1,
        #         initialWidth=width,
        #         minimumWidth=height
        #     )
        # else:
        #     LEcomponent = mel.eval(r'getUIComponentDockControl("Channel Box / Layer Editor", false);')
        #     cmds.workspaceControl(
        #         control_name,
        #         label=control_label, tabToControl=(LEcomponent, -1),
        #         initialWidth=width, initialHeight=height,
        #         widthProperty='free', heightProperty='free'
        #     )
        #     parentPtr = OpenMayaUI.MQtUtil.getCurrentParent()
        #     parentWidget = wrapInstance(parentPtr, QtWidgets.QWidget)
        #     from lxmaya.panel import widgets
        #     p = widgets.AnimationValidationPanel()
        #     p.widget.setParent(parentWidget)
        #     OpenMayaUI.MQtUtil.addWidgetToMayaLayout(
        #         long(getCppPointer(p.widget)[0]), long(parentPtr)
        #     )
        pass


class GuiQtHoudini(object):
    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        import hou

        return hou.qt.mainWindow()

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        # noinspection PyUnresolvedReferences
        import hou

        if icon_name is not None:
            return hou.qt.Icon(icon_name)
        return hou.qt.Icon('MISC_python')


class GuiQtKatana(object):
    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        import UI4

        return UI4.App.MainWindow.GetMainWindow()

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        # noinspection PyUnresolvedReferences
        import UI4

        return UI4.Util.ScenegraphIconManager.GetIcon(icon_name, 32)

    @classmethod
    def get_menu_bar(cls):
        main_window = cls.get_qt_main_window()
        if main_window is None:
            log_core.Log.trace_method_warning(
                'qt-katana',
                'main-window is non-exists'
            )
            return
        #
        return main_window.getMenuBar()

    @classmethod
    def get_menu(cls, name):
        menu_bar = cls.get_menu_bar()
        if menu_bar is None:
            log_core.Log.trace_method_warning(
                'qt-katana',
                'menu-bar is non-exists'
            )
            return
        #
        for i_child in menu_bar.children():
            if isinstance(i_child, QtWidgets.QMenu):
                i_name = i_child.title()
                if i_name == name:
                    return i_child


class GuiQtClarisse(object):
    QT_MAIN_WINDOW = None

    @classmethod
    def get_qt_main_window(cls):
        return None

    @classmethod
    def get_qt_main_window_geometry_args(cls):
        # noinspection PyUnresolvedReferences
        import ix

        x, y = ix.application.get_event_window().get_position()
        w, h = ix.application.get_event_window().get_size()
        return x, y, w, h


class GuiQtDcc(gui_abstracts.AbsGuiDcc):
    QT_MAIN_WINDOW = None

    @classmethod
    def get_qt_main_window(cls):
        if cls.get_is_maya():
            return GuiQtMaya.get_qt_main_window()
        elif cls.get_is_houdini():
            return GuiQtHoudini.get_qt_main_window()
        elif cls.get_is_katana():
            return GuiQtKatana.get_qt_main_window()
        elif cls.get_is_clarisse():
            return GuiQtClarisse.get_qt_main_window()
        #
        if cls.QT_MAIN_WINDOW is not None:
            return cls.QT_MAIN_WINDOW
        #
        _ = QtWidgets.QApplication.topLevelWidgets()
        if _:
            cls.QT_MAIN_WINDOW = _[0]
        return _gui_qt_cor_base.GuiQtUtil.get_qt_active_window()

    @classmethod
    def get_qt_active_window(cls):
        return _gui_qt_cor_base.GuiQtUtil.get_qt_active_window()

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        if cls.get_is_maya():
            return GuiQtMaya.generate_qt_icon_by_name(icon_name)
        elif cls.get_is_houdini():
            return GuiQtHoudini.generate_qt_icon_by_name(icon_name)
        return _gui_qt_cor_base.GuiQtIcon.generate_by_name(icon_name)

    @classmethod
    def get_qt_folder_icon(cls, use_system=False):
        if use_system is True:
            f_i_p = QtWidgets.QFileIconProvider()
            return f_i_p.icon(f_i_p.Folder)
        return _gui_qt_cor_base.GuiQtIcon.create_by_icon_name('file/folder')

    @classmethod
    def get_qt_file_icon(cls, file_path):
        f_i_p = QtWidgets.QFileIconProvider()
        if bsc_core.StgPathMtd.get_is_file(file_path) is True:
            info = QtCore.QFileInfo(file_path)
            return f_i_p.icon(info)
        return f_i_p.icon(f_i_p.File)

    @classmethod
    def generate_qt_palette(cls):
        if cls.get_is_maya():
            return _gui_qt_cor_base.GuiQtUtil.generate_qt_palette()
        elif cls.get_is_houdini():
            return _gui_qt_cor_base.GuiQtUtil.generate_qt_palette()
        elif cls.get_is_katana():
            return _gui_qt_cor_base.GuiQtUtil.generate_qt_palette()
        elif cls.get_is_clarisse():
            return _gui_qt_cor_base.GuiQtUtil.generate_qt_palette(tool_tip=True)
        return _gui_qt_cor_base.GuiQtUtil.generate_qt_palette(tool_tip=True)

    @classmethod
    def exit_app(cls, app):
        if cls.get_is_clarisse():
            # noinspection PyUnresolvedReferences
            import pyqt_clarisse

            pyqt_clarisse.exec_(app)
        else:
            sys.exit(app.exec_())

    @classmethod
    def get_qt_main_window_geometry_args(cls):
        if cls.get_is_clarisse():
            return GuiQtClarisse.get_qt_main_window_geometry_args()
