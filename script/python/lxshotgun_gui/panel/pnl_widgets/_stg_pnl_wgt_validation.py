# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_checker

from lxshotgun_fnc import stg_fnc_core


class SceneCheckerToolPanel(utl_gui_pnl_abs_checker.AbsSceneCheckerToolPanel):
    METHOD_CREATOR_CLS = stg_fnc_core.CheckerCreator
    STEP_LOADER_CLS = stg_fnc_core.StpLoader
    def __init__(self, work_source_file_path, *args, **kwargs):
        import lxresolver.commands as rsv_commands
        #
        resolver = rsv_commands.get_resolver()
        task_properties = resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)
        super(SceneCheckerToolPanel, self).__init__(task_properties, *args, **kwargs)
