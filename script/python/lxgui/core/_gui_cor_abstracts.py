# coding:utf-8
from ..core import _gui_cor_base


class AbsGuiDcc(object):
    @classmethod
    def get_is_maya(cls):
        return _gui_cor_base.GuiUtil.get_is_maya()

    @classmethod
    def get_is_houdini(cls):
        return _gui_cor_base.GuiUtil.get_is_houdini()

    @classmethod
    def get_is_katana(cls):
        return _gui_cor_base.GuiUtil.get_is_katana()

    @classmethod
    def get_is_clarisse(cls):
        return _gui_cor_base.GuiUtil.get_is_clarisse()
