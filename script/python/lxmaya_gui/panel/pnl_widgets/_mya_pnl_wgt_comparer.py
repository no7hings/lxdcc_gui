# coding:utf-8
from lxutil import utl_configure

from lxutil_gui.panel import utl_gui_pnl_abs_comparer

from lxmaya import ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.fnc.comparers as mya_fnc_comparers


class AssetComparerPanel(utl_gui_pnl_abs_comparer.AbsAssetComparerPanel):
    DCC_OBJ_CLASS = mya_dcc_objects.Node
    #
    FNC_GEOMETRY_COMPARER = mya_fnc_comparers.GeometryComparer
    #
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_NAMESPACE = 'dcc'
    DCC_OBJ_PATHSEP = '|'
    def __init__(self, *args, **kwargs):
        super(AssetComparerPanel, self).__init__(*args, **kwargs)
        work_source_file_path = mya_dcc_objects.Scene.get_current_file_path()
        self._configure_gui.get_port('scene_file_path').set(work_source_file_path)

    def _set_radar_chart_refresh_(self):
        o = ma_core.CmdMeshesOpt('|master|hi')
        self._radar_chart.set_chart_data(
            o.get_radar_chart_data()
        )
