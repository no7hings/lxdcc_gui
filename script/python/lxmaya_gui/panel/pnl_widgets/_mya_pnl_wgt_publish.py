# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class ValidatorOpt(utl_gui_pnl_abstracts.AbsValidatorOpt):
    DCC_NAMESPACE = 'maya'
    DCC_NODE_CLS = mya_dcc_objects.Node
    DCC_COMPONENT_CLS = mya_dcc_objects.Component
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_PATHSEP = '|'
    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class PnlAssetPublish(utl_gui_pnl_abstracts.AbsPnlAssetPublisher):
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt
    def __init__(self, session, *args, **kwargs):
        super(PnlAssetPublish, self).__init__(session, *args, **kwargs)

    def _get_dcc_scene_file_path_(self):
        return mya_dcc_objects.Scene.get_current_file_path()
