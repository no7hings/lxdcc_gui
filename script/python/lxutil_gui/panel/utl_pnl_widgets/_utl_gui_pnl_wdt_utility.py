# coding:utf-8
from lxutil.dcc.dcc_objects import _utl_dcc_obj_utility

from lxutil import utl_core

from lxutil_prd import utl_prd_objects

from lxutil_gui.panel import utl_gui_pnl_abstract, utl_gui_pnl_abs_utility, utl_gui_pnl_abs_render_submitter, utl_gui_pnl_abs_loader, utl_gui_pnl_abs_node_graph, utl_gui_pnl_abs_publish


class SceneBuildToolPanel(utl_gui_pnl_abstract.AbsShotBuildToolPanel):
    TOOL_PANEL_KEY = 'shot_builder'
    TOOL_CONFIGURE = utl_core.Scheme.UTILITY_TOOL_TD
    #
    OBJ_OPT_CLASS = utl_prd_objects.ObjOpt
    SHOT_OPT_CLASS = utl_prd_objects.ShotOpt
    #
    SCENE_OPT_CLASS = utl_prd_objects.SceneOpt
    #
    CONTAINER_OPT_CLASS = utl_prd_objects.ContainerOpt
    #
    UTL_OBJ_CLASS = _utl_dcc_obj_utility.Obj
    FILTER_SCHEME_OVERRIDE = 'custom'
    def __init__(self, file_path=None, *args, **kwargs):
        # file_path = '/l/prod/cg7/work/shots/d10/d10250/lgt/lgt/houdini/d10250.lgt.lgt.v003.hip'
        super(SceneBuildToolPanel, self).__init__(file_path, *args, **kwargs)
    # noinspection PyMethodMayBeStatic
    def _set_dcc_port_elements_build_(self, element_opt):
        pass


class FncPanel(utl_gui_pnl_abs_utility.AbsFncPanel):
    def __init__(self, file_path=None, *args, **kwargs):
        super(FncPanel, self).__init__(file_path, *args, **kwargs)


class RsvEntitiesLoader(utl_gui_pnl_abs_loader.AbsEntitiesLoaderPanel_):
    def __init__(self, session, *args, **kwargs):
        super(RsvEntitiesLoader, self).__init__(session, *args, **kwargs)


class AssetRenderSubmitter(utl_gui_pnl_abs_render_submitter.AbsAssetRenderSubmitterPanel):
    OPTION_HOOK_KEY = 'tool-panels/asset-render-submitter'
    def __init__(self, hook_option=None, *args, **kwargs):
        super(AssetRenderSubmitter, self).__init__(hook_option, *args, **kwargs)


class ShotRenderSubmitter(utl_gui_pnl_abs_render_submitter.AbsShotRenderSubmitterPanel):
    OPTION_HOOK_KEY = 'tool-panels/shot-render-submitter'
    def __init__(self, hook_option=None, *args, **kwargs):
        super(ShotRenderSubmitter, self).__init__(hook_option, *args, **kwargs)


class RezGraph(utl_gui_pnl_abs_node_graph.AbsRezGraph):
    OPTION_HOOK_KEY = 'tool-panels/rez-graph'
    def __init__(self, hook_option=None, *args, **kwargs):
        super(RezGraph, self).__init__(hook_option, *args, **kwargs)


class AssetLineup(utl_gui_pnl_abs_node_graph.AbsAssetLineup):
    OPTION_HOOK_KEY = 'tool-panels/asset-lineup'
    def __init__(self, hook_option=None, *args, **kwargs):
        super(AssetLineup, self).__init__(hook_option, *args, **kwargs)
