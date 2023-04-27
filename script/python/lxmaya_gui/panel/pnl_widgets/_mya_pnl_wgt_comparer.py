# coding:utf-8
from lxbasic import bsc_core

from lxmaya import ma_core

import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.fnc.comparers as mya_fnc_comparers


class PnlAssetDccGeometryComparer(utl_gui_pnl_abstracts.AbsPnlAssetDccGeometryComparer):
    DCC_NODE_CLASS = mya_dcc_objects.Node
    #
    FNC_GEOMETRY_COMPARER = mya_fnc_comparers.FncGeometryComparer
    #
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_NAMESPACE = 'usd'
    DCC_PATHSEP = '|'
    #
    DCC_LOCATION = '/master/mod/hi'
    DCC_LOCATION_SOURCE = '/master/hi'
    #
    DCC_GEOMETRY_LOCATION = None
    def __init__(self, session, *args, **kwargs):
        super(PnlAssetDccGeometryComparer, self).__init__(session, *args, **kwargs)

    def post_setup_fnc(self):
        scene_src_file_path = mya_dcc_objects.Scene.get_current_file_path()
        self._options_prx_node.set(
            'scene.file', scene_src_file_path
        )
