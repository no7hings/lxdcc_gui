# coding:utf-8
from lxutil import utl_core

from lxutil_gui.panel import utl_gui_pnl_abs_method_runner

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class SceneMethodRunnerPanel(utl_gui_pnl_abs_method_runner.AbsSceneMethodRunnerPanel):
    DCC_PATHSEP = '/'
    DCC_NODE_CLASS = mya_dcc_objects.Node
    OBJ_COMP_CLASS = mya_dcc_objects.MeshComponent
    #
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(SceneMethodRunnerPanel, self).__init__(*args, **kwargs)
        work_source_file_path = mya_dcc_objects.Scene.get_current_file_path()
        self._configure_gui.get_port('work_scene_src_file_path').set(
            work_source_file_path
        )
