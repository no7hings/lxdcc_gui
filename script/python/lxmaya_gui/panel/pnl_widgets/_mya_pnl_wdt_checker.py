# coding:utf-8
from lxutil import utl_configure

from lxutil_gui.panel import utl_gui_pnl_abs_checker

import lxmaya.dcc.dcc_objects as mya_objects

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_utility

from lxmaya_fnc import ma_fnc_core


class SceneCheckerToolPanel(utl_gui_pnl_abs_checker.AbsSceneCheckerToolPanel):
    HELP_FILE_PATH = '{}/maya/validation_tool.md'.format(utl_configure.Root.DATA)
    DCC_SELECTION_CLS = _mya_dcc_obj_utility.Selection
    #
    STEP_LOADER_CLASS = ma_fnc_core.StpLoader
    METHOD_CREATOR_CLASS = ma_fnc_core.CheckerCreator
    def __init__(self, *args, **kwargs):
        import lxresolver.commands as rsv_commands
        work_source_file_path = mya_objects.Scene.get_current_file_path()
        #
        resolver = rsv_commands.get_resolver()
        task_properties = resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)
        super(SceneCheckerToolPanel, self).__init__(task_properties, *args, **kwargs)
