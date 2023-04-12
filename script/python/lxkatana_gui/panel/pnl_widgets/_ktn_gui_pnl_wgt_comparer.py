# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxkatana.fnc.comparers as ktn_fnc_comparers

from lxkatana import ktn_core


class PnlAssetGeometryComparer(utl_gui_pnl_abstracts.AbsPnlAssetGeometryComparer):
    DCC_OBJ_CLASS = ktn_dcc_objects.Node
    #
    FNC_GEOMETRY_COMPARER = ktn_fnc_comparers.GeometryComparer
    #
    DCC_SELECTION_CLS = ktn_core.KtnSGSelectionOpt
    DCC_NAMESPACE = 'dcc'
    DCC_OBJ_PATHSEP = '|'
    def __init__(self, session, *args, **kwargs):
        super(PnlAssetGeometryComparer, self).__init__(session, *args, **kwargs)

    def _post_setup_(self):
        scene_src_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        self._options_prx_node.set(
            'scene.file', scene_src_file_path
        )

    def _set_radar_chart_refresh_(self):
        pass
        # o = ma_core.CmdMeshesOpt('|master|hi')
        # self._radar_chart.set_chart_data(
        #     o.get_radar_chart_data()
        # )
