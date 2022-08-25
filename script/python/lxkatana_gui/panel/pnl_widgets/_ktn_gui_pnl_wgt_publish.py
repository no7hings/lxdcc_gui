# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_publish

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class KtnValidatorOpt(utl_gui_pnl_abs_publish.AbsValidatorOpt):
    DCC_NAMESPACE = 'katana'
    DCC_NODE_CLS = ktn_dcc_objects.Node
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(KtnValidatorOpt, self).__init__(*args, **kwargs)


class AssetPublish(utl_gui_pnl_abs_publish.AbsAssetPublish):
    DCC_VALIDATOR_OPT_CLS = KtnValidatorOpt
    def __init__(self, session, *args, **kwargs):
        super(AssetPublish, self).__init__(session, *args, **kwargs)

    def _get_dcc_scene_file_path_(self):
        return ktn_dcc_objects.Scene.get_current_file_path()
