# coding:utf-8
import os

from lxutil_gui.panel import utl_gui_pnl_abs_method_runner

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class SceneMethodRunnerPanel(utl_gui_pnl_abs_method_runner.AbsSceneMethodRunnerPanel):
    DCC_PATHSEP = '/'
    DCC_NODE_CLS = ktn_dcc_objects.Node
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(SceneMethodRunnerPanel, self).__init__(*args, **kwargs)
        work_source_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        self._configure_gui.get_port('work_scene_src_file_path').set(
            work_source_file_path
        )
        self.refresh_all_fnc()
