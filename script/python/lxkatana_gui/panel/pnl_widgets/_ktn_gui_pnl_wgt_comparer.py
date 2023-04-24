# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxkatana.fnc.comparers as ktn_fnc_comparers

from lxkatana import ktn_core


class PnlAssetDccGeometryComparer(utl_gui_pnl_abstracts.AbsPnlAssetDccGeometryComparer):
    DCC_NODE_CLASS = ktn_dcc_objects.Node
    #
    FNC_GEOMETRY_COMPARER = ktn_fnc_comparers.FncGeometryComparer
    #
    DCC_SELECTION_CLS = ktn_core.KtnSGSelectionOpt
    #
    DCC_NAMESPACE = 'usd'
    DCC_PATHSEP = None
    #
    DCC_LOCATION = '/master/hi'
    #
    DCC_GEOMETRY_LOCATION = '/root/world/geo'
    def __init__(self, session, *args, **kwargs):
        super(PnlAssetDccGeometryComparer, self).__init__(session, *args, **kwargs)

    def post_setup_fnc(self):
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
