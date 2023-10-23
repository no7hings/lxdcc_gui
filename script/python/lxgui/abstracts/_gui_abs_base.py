# coding:utf-8
import lxgui.core as gui_core


class AbsGuiDcc(object):
    @classmethod
    def get_is_maya(cls):
        return gui_core.GuiUtil.get_is_maya()

    @classmethod
    def get_is_houdini(cls):
        return gui_core.GuiUtil.get_is_houdini()

    @classmethod
    def get_is_katana(cls):
        return gui_core.GuiUtil.get_is_katana()

    @classmethod
    def get_is_clarisse(cls):
        return gui_core.GuiUtil.get_is_clarisse()
