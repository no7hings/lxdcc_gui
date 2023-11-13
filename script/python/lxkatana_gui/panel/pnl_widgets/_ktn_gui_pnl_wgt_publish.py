# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class ValidatorOpt(utl_gui_pnl_abstracts.AbsValidatorOpt):
    DCC_NAMESPACE = 'katana'
    DCC_NODE_CLS = ktn_dcc_objects.Node
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_PATHSEP = '/'

    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class PnlAssetPublish(utl_gui_pnl_abstracts.AbsPnlAssetPublish):
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt

    def __init__(self, session, *args, **kwargs):
        super(PnlAssetPublish, self).__init__(session, *args, **kwargs)

    def _get_dcc_scene_file_path_(self):
        return ktn_dcc_objects.Scene.get_current_file_path()
