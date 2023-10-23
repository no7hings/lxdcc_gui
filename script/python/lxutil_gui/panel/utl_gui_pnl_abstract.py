# coding:utf-8
import collections

import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets

from lxutil import utl_core


class AbsGuiExtraDef(object):
    UTL_OBJ_CLS = None
    @classmethod
    def _set_prd_obj_gui_add_(cls, obj, tree_view_gui):
        item_dict = tree_view_gui._item_dict
        parent_obj_path = obj.get_parent_path()
        obj_path = obj.path
        port = obj.get_variant_port('icon')
        if port:
            icon_name = port.get()
            obj_icon = gui_core.GuiIcon.get(icon_name)
        else:
            obj_icon = gui_core.GuiIcon.get('tag')
        #
        if obj_path in item_dict:
            return item_dict[obj_path]
        #
        tool_tip = 'path: {}'.format(obj_path)
        #
        _kwargs = dict(
            name=(obj.name, obj.type.name),
            icon=obj_icon,
            tool_tip=tool_tip,
            item_class=prx_widgets.PrxObjTreeItem,
        )
        if parent_obj_path is None:
            obj_gui = tree_view_gui.create_item(
                **_kwargs
            )
            item_dict[obj_path] = obj_gui
            return obj_gui
        else:
            if parent_obj_path in item_dict:
                parent_gui = item_dict[parent_obj_path]
                obj_gui = parent_gui.add_child(
                    **_kwargs
                )
                item_dict[obj_path] = obj_gui
                return obj_gui
    @classmethod
    def gui_add(cls, dcc_obj, parent_obj_gui):
        dcc_obj_gui = parent_obj_gui.add_child(
            dcc_obj.name, dcc_obj.type,
            item_class=prx_widgets.PrxDccObjTreeItem,
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path
        )
        dcc_obj_gui.set_gui_attribute('dcc_obj', dcc_obj)
        return dcc_obj_gui

    def get_obj_gui(self, obj_path):
        pass
    @classmethod
    def _set_utl_obj_gui_add_(cls, obj_path, tree_view_gui, icon_name=None):
        item_dict = tree_view_gui._item_dict
        #
        utl_obj = cls.UTL_OBJ_CLS(obj_path)
        if utl_obj.path in item_dict:
            return item_dict[utl_obj.path]
        #
        if icon_name is not None:
            icon = gui_core.GuiIcon.get(icon_name)
        else:
            icon = utl_obj.icon

        _kwargs = dict(
            name=(utl_obj.name, utl_obj.type),
            icon=icon,
            tool_tip='path: {}'.format(utl_obj.path),
            item_class=prx_widgets.PrxObjTreeItem,
        )
        parent_path = utl_obj.get_parent_path()
        if parent_path in item_dict:
            parent_gui = item_dict[parent_path]
            obj_gui = parent_gui.add_child(
                **_kwargs
            )
            item_dict[utl_obj.path] = obj_gui
            return obj_gui
        else:
            obj_gui = tree_view_gui.create_item(
                **_kwargs
            )
            item_dict[utl_obj.path] = obj_gui
            return obj_gui


class AbsGuiMethodDef(object):
    def _set_gui_method_def_init_(self):
        self._method_dict = collections.OrderedDict()
        self._method_gui_dict = collections.OrderedDict()

    def set_method(self, method_key, method):
        self._method_dict[method_key] = method

    def get_method(self, method_key):
        return self._method_dict[method_key]

    def set_method_gui(self, method_key, method_gui):
        self._method_gui_dict[method_key] = method_gui

    def get_method_gui(self, method_key):
        return self._method_gui_dict[method_key]


class AbsUtilToolPanel(prx_widgets.PrxBaseWindow):
    TOOL_PANEL_KEY = None
    TOOL_SCHEME = None
    DCC_SELECTION_CLS = None
    def __init__(self, *args, **kwargs):
        super(AbsUtilToolPanel, self).__init__(*args, **kwargs)
        self.set_window_title(
            self.TOOL_SCHEME.get('tool.{}.label'.format(self.TOOL_PANEL_KEY))
        )
        self.set_definition_window_size(
            self.TOOL_SCHEME.get('tool.{}.size'.format(self.TOOL_PANEL_KEY))
        )


class AbsDccObjGuiDef(object):
    @classmethod
    def gui_add(cls, obj, obj_gui_parent=None, tree_viewer=None):
        kwargs = dict(
            name=(obj.name, obj.type.name),
            item_class=prx_widgets.PrxObjTreeItem,
            icon=obj.icon,
            tool_tip=obj.path
        )
        if obj_gui_parent is not None:
            obj_gui = obj_gui_parent.add_child(
                **kwargs
            )
        elif tree_viewer is not None:
            obj_gui = tree_viewer.create_item(
                **kwargs
            )
        else:
            raise TypeError()
        #
        obj.set_obj_gui(obj_gui)
        return obj_gui
    @classmethod
    def _set_obj_connect_to_dcc_(cls, obj, obj_gui, is_shape):
        raise NotImplementedError()
