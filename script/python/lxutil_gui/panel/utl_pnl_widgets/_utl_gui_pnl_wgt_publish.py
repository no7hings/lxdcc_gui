# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_publish

import lxutil.dcc.dcc_objects as utl_dcc_objects


class ValidatorOpt(utl_gui_pnl_abs_publish.AbsValidatorOpt):
    DCC_NAMESPACE = 'katana'
    DCC_NODE_CLS = utl_dcc_objects.Obj
    DCC_COMPONENT_CLS = utl_dcc_objects.Component
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = '/'
    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class AssetPublish(utl_gui_pnl_abs_publish.AbsAssetPublisher):
    DCC_NAMESPACE = 'python'
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt
    def __init__(self, session, *args, **kwargs):
        super(AssetPublish, self).__init__(session, *args, **kwargs)
