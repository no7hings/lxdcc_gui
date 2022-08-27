# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_publish

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class ValidatorOpt(utl_gui_pnl_abs_publish.AbsValidatorOpt):
    DCC_NAMESPACE = 'katana'
    DCC_NODE_CLS = ktn_dcc_objects.Node
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_PATHSEP = '/'
    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class AssetPublish(utl_gui_pnl_abs_publish.AbsAssetPublisher):
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt
    def __init__(self, session, *args, **kwargs):
        super(AssetPublish, self).__init__(session, *args, **kwargs)

    def _get_dcc_scene_file_path_(self):
        return ktn_dcc_objects.Scene.get_current_file_path()
