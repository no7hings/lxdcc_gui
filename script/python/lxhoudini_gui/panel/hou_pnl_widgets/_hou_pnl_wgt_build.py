# coding:utf-8
# noinspection PyUnresolvedReferences
import hou

from lxutil import utl_core

from lxutil.dcc.dcc_objects import _utl_dcc_obj_utility

from lxutil_prd import utl_prd_objects

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.panel import utl_gui_pnl_abstract

from lxhoudini_prd import hou_prd_objects

import lxhoudini.dcc.dcc_objects as hou_dcc_objects


class SceneBuildToolPanel(utl_gui_pnl_abstract.AbsShotBuildToolPanel):
    TOOL_PANEL_KEY = 'shot_builder'
    TOOL_CONFIGURE = utl_core.Scheme.HOUDINI_TOOL_TD
    #
    DCC_SELECTION_CLS = hou_dcc_objects.Selection
    #
    OBJ_OPT_CLASS = utl_prd_objects.ObjOpt
    SHOT_OPT_CLASS = utl_prd_objects.ShotOpt
    #
    SCENE_OPT_CLASS = utl_prd_objects.SceneOpt
    #
    CONTAINER_OPT_CLASS = utl_prd_objects.ContainerOpt
    ELEMENT_CREATOR_CLASS = hou_prd_objects.ElementCreator
    #
    UTL_OBJ_CLASS = _utl_dcc_obj_utility.Obj
    DCC_OBJ_CLASS = hou_dcc_objects.Node
    #
    FILTER_SCHEME_OVERRIDE = '/houdini/custom'
    def __init__(self, file_path=None, *args, **kwargs):
        if file_path is None:
            file_path = hou_dcc_objects.Scene().path
        super(SceneBuildToolPanel, self).__init__(file_path, *args, **kwargs)

    def _set_dcc_port_elements_build_(self, element_opt, **build_kwargs):
        element_creator = self.ELEMENT_CREATOR_CLASS(element_opt, **build_kwargs)
        return element_creator.set_create()

    def _set_obj_gui_dcc_update_(self, obj_opt, obj_gui):
        dcc_path = obj_opt.dcc_path
        if dcc_path is not None:
            if self.DCC_OBJ_CLASS is not None:
                dcc_obj = self.DCC_OBJ_CLASS(dcc_path)
                if dcc_obj.get_is_exists() is True:
                    obj_gui.set_gui_attribute('dcc_obj', dcc_obj)
                    obj_gui.set_icon_by_file(dcc_obj.icon)
                    #
                    display_enable = dcc_obj.get_is_display_enable()
                    obj_gui.set_name(str(display_enable), self.GUI_DISPLAY_INDEX)
                    obj_gui.set_icon_by_file(utl_gui_qt_core.QtUtilMtd.get_qt_icon(['hide', 'show'][display_enable]), self.GUI_DISPLAY_INDEX)
                    render_enable = dcc_obj.get_is_render_enable()
                    obj_gui.set_name(str(render_enable), self.GUI_RENDER_INDEX)
                    obj_gui.set_icon_by_file(utl_gui_qt_core.QtUtilMtd.get_qt_icon(['hide', 'show'][render_enable]), self.GUI_RENDER_INDEX)

    def _set_dcc_objs_build_(self):
        self._set_dcc_pre_build_()
        #
        element_opts = self._get_checked_element_opts_()
        p = self.set_progress_create(len(element_opts))
        hou_obj_paths = []
        for element_opt in element_opts:
            p.set_update()
            sub_hou_obj_paths = self._set_dcc_port_elements_build_(element_opt)
            [hou_obj_paths.append(i) for i in sub_hou_obj_paths if i not in hou_obj_paths]
        p.set_stop()
        #
        dic = {}
        for i in hou_obj_paths:
            p = '/'.join(i.split('/')[:2])
            dic.setdefault(p, []).append(i)
        for k, v in dic.items():
            hou_obj = hou.node(k)
            hou_obj.layoutChildren(
                [hou.node(i) for i in v]
            )
        #
        self._set_obj_guis_dcc_update_()
        #
        self._set_dcc_pst_build_()

    def _set_dcc_pre_build_(self):
        dcc_obj = hou_dcc_objects.Node('/obj/assets')
        #
        hou_obj_paths = dcc_obj.get_all_input_obj_paths('output1')
        for i in hou_obj_paths:
            input_hou_obj = hou.node(i)
            if input_hou_obj.type().name() in ['null', 'geo']:
                input_hou_obj.destroy()
        #
        hou_renders = hou.nodeType('Driver/arnold').instances() or []
        for i in hou_renders:
            name = i.name()
            if name in ['chr', 'scn', 'volume']:
                i.setName('render_{}'.format(name))
        #
        hou_out = hou.node('/out')
        _ = hou_out.glob('*_mtl_mtx') or []
        for i in _:
            i.destroy()

    def _set_dcc_pst_build_(self):
        self._set_default_shader_create_()
        self._set_dcc_frame_range_()
    @utl_core.Modifier.debug_trace
    def _set_dcc_frame_range_(self):
        from lxshotgun import commands
        shot_opt = None
        if self._current_shot is not None:
            shot_opt = self._current_shot
        else:
            shot_opts = self._get_checked_shot_opts_()
            if shot_opts:
                shot_opt = shot_opts[-1]
        #
        if shot_opt is not None:
            dcc_scn = hou_dcc_objects.Scene()
            shotgun_frame_range = commands.get_shot_frame_range(shot_opt.name)
            if shotgun_frame_range:
                dcc_scn.set_frame_range(*shotgun_frame_range)
    @staticmethod
    def _set_default_shader_create_():
        hou_shop = hou.node('/shop')
        hou_default_material_path = '/shop/default_arnold_material'
        hou_default_material = hou.node(hou_default_material_path)
        if hou_default_material is None:
            hou_default_material = hou_shop.createNode('arnold_vopnet', 'default_arnold_material')
        #
        default_shader_path = '/shop/default_arnold_material/default_shader'
        hou_lambert = hou.node(default_shader_path)
        if hou_lambert is None:
            hou_lambert = hou_default_material.createNode('arnold::lambert', 'default_shader')
        hou.node('/shop/default_arnold_material/OUT_material').setInput(0, hou_lambert)

