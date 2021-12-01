# coding:utf-8
from lxutil.dcc.dcc_objects import _utl_dcc_obj_utility

from lxutil import utl_core

from lxutil_prd import utl_prd_objects

from lxutil_gui.panel import utl_gui_pnl_abstract, utl_gui_pnl_abs_utility


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
