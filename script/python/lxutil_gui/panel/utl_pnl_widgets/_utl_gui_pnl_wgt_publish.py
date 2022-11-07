# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxutil.dcc.dcc_objects as utl_dcc_objects


class ValidatorOpt(utl_gui_pnl_abstracts.AbsValidatorOpt):
    DCC_NAMESPACE = 'lynxi'
    DCC_NODE_CLS = utl_dcc_objects.Obj
    DCC_COMPONENT_CLS = utl_dcc_objects.Component
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = '/'
    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class PnlAssetPublish(utl_gui_pnl_abstracts.AbsPnlAssetPublisher):
    DCC_NAMESPACE = 'python'
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt
    def __init__(self, session, *args, **kwargs):
        super(PnlAssetPublish, self).__init__(session, *args, **kwargs)
