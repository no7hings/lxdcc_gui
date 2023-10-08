# coding:utf-8
from lxutil import utl_configure

from lxutil_gui.panel import utl_gui_pnl_abs_checker

import lxhoudini.dcc.dcc_objects as hou_dcc_objects

from lxhoudini_fnc import hou_fnc_core


class SceneCheckerToolPanel(utl_gui_pnl_abs_checker.AbsSceneCheckerToolPanel):
    HELP_FILE_PATH = '{}/maya/validation_tool.md'.format(utl_configure.Root.DATA)
    DCC_SELECTION_CLS = hou_dcc_objects.Selection
    #
    STEP_LOADER_CLS = hou_fnc_core.StpLoader
    METHOD_CREATOR_CLS = hou_fnc_core.CheckerCreator

    def __init__(self, *args, **kwargs):
        import lxresolver.commands as rsv_commands

        resolver = rsv_commands.get_resolver()
        work_source_file_path = hou_dcc_objects.Scene().path
        task_properties = resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)
        super(SceneCheckerToolPanel, self).__init__(task_properties, *args, **kwargs)
