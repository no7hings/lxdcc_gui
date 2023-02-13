# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxutil import utl_core

from lxutil.dcc.dcc_objects import _utl_dcc_obj_utility

from lxutil_prd import utl_prd_configure, utl_prd_objects

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.panel import utl_gui_pnl_abstract, utl_gui_pnl_abs_builder

from lxmaya_prd import ma_prd_objects

import lxmaya.dcc.dcc_objects as ma_dcc_objects


class SceneBuildToolPanel(utl_gui_pnl_abstract.AbsShotBuildToolPanel):
    TOOL_PANEL_KEY = 'shot_builder'
    TOOL_CONFIGURE = utl_core.Scheme.MAYA_TOOL_TD
    #
    DCC_SELECTION_CLS = ma_dcc_objects.Selection
    OBJ_OPT_CLASS = utl_prd_objects.ObjOpt
    SHOT_OPT_CLASS = utl_prd_objects.ShotOpt
    #
    SCENE_OPT_CLASS = utl_prd_objects.SceneOpt
    #
    CONTAINER_OPT_CLASS = utl_prd_objects.ContainerOpt
    ELEMENT_CREATOR_CLASS = ma_prd_objects.ElementCreator
    #
    UTL_OBJ_CLASS = _utl_dcc_obj_utility.Obj
    DCC_OBJ_CLASS = ma_dcc_objects.Node
    #
    FILTER_SCHEME_OVERRIDE = '/maya/surface'
    def __init__(self, file_path=None, *args, **kwargs):
        if file_path is None:
            file_path = ma_dcc_objects.SceneFile.get_current_file_path()
        #
        super(SceneBuildToolPanel, self).__init__(file_path, *args, **kwargs)
    #
    def _set_dcc_port_elements_build_(self, element_opt, **kwargs):
        element_creator = self.ELEMENT_CREATOR_CLASS(element_opt, **kwargs)
        return element_creator.set_create()

    def _set_dcc_pst_build_(self):
        self._set_dcc_frame_range_()
        self._set_dcc_render_resolution_()

    def _set_dcc_pre_build_(self):
        cmds.loadPlugin('gpuCache', quiet=1)
        cmds.loadPlugin('mtoa', quiet=1)
        #
        self._set_ar_string_replace_create_()

    def _set_ar_string_replace_create_(self):
        obj = ma_dcc_objects.AndStringReplace(utl_prd_configure.Name.AR_PATH_CONVERT)
        obj.get_dcc_instance('aiStringReplace', obj.path)
        if obj.get_is_exists() is True:
            obj.get_port('os').set(2)
            obj.get_port('selection').set('''*.(@node == 'image')''')
            obj.get_port('match').set('''/l/prod/cg7''')
            obj.get_port('replace').set('''l:/prod/cg7''')
    @utl_core.Modifier.debug_trace
    def _set_dcc_frame_range_(self):
        from lxshotgun import commands
        #
        shot_opt = None
        if self._current_shot is not None:
            shot_opt = self._current_shot
        else:
            shot_opts = self._get_checked_shot_opts_()
            if shot_opts:
                shot_opt = shot_opts[-1]
        #
        if shot_opt is not None:
            dcc_scn = ma_dcc_objects.Scene()
            shotgun_frame_range = commands.get_shot_frame_range(shot_opt.name)
            if shotgun_frame_range:
                dcc_scn.set_frame_range(*shotgun_frame_range)
                dcc_scn.set_render_frame_range(*shotgun_frame_range)
    @utl_core.Modifier.debug_trace
    def _set_dcc_render_resolution_(self):
        from lxshotgun import commands
        self._scene_opt = self.SCENE_OPT_CLASS(project='cg7', stage='publish')
        s = self._scene_opt.scene
        project = s.get_current_project_obj()
        if project is not None:
            shotgun_resolution = commands.get_project_resolution(project.name)
            if shotgun_resolution:
                ma_dcc_objects.Scene.set_render_resolution(*shotgun_resolution)


class AssetBuilderPanel(utl_gui_pnl_abs_builder.AbsAssetBuilderPanel):
    def __init__(self, *args, **kwargs):
        super(AssetBuilderPanel, self).__init__(*args, **kwargs)

    @utl_gui_qt_core.set_prx_window_waiting
    def _set_build_run_(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=self._options_prx_node.get('project'),
                asset=self._options_prx_node.get('asset').name,
                #
                with_model_geometry=self._options_prx_node.get('build_options.with_model_geometry'),
                #
                with_groom_geometry=self._options_prx_node.get('build_options.with_groom_geometry'), with_groom_grow_geometry=self._options_prx_node.get('build_options.with_groom_grow_geometry'),
                #
                with_surface_geometry_uv_map=self._options_prx_node.get('build_options.with_surface_geometry_uv_map'), with_surface_look=self._options_prx_node.get('build_options.with_surface_look'),
                #
                with_camera=self._options_prx_node.get('build_options.with_camera'), with_light=self._options_prx_node.get('build_options.with_light'),
                #
                render_resolution=self._options_prx_node.get('render.resolution'),
                #
                save_scene=self._options_prx_node.get('build_options.save_scene'),
            )
        ).set_run()
