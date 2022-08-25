# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_publish

import lxutil.dcc.dcc_objects as utl_dcc_objects


class DccValidatorOpt(utl_gui_pnl_abs_publish.AbsValidatorOpt):
    DCC_NAMESPACE = 'katana'
    DCC_NODE_CLS = utl_dcc_objects.Obj
    DCC_SELECTION_CLS = None
    def __init__(self, *args, **kwargs):
        super(DccValidatorOpt, self).__init__(*args, **kwargs)


class AssetPublish(utl_gui_pnl_abs_publish.AbsAssetPublish):
    DCC_NAMESPACE = 'python'
    DCC_VALIDATOR_OPT_CLS = DccValidatorOpt
    def __init__(self, session, *args, **kwargs):
        super(AssetPublish, self).__init__(session, *args, **kwargs)
