# coding:utf-8
import lxtool.publisher.gui.abstracts as pbs_gui_abstracts

import lxutil.dcc.dcc_objects as utl_dcc_objects


class ValidatorOpt(pbs_gui_abstracts.AbsValidatorOpt):
    DCC_NAMESPACE = 'lynxi'
    DCC_NODE_CLS = utl_dcc_objects.Obj
    DCC_COMPONENT_CLS = utl_dcc_objects.Component
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = '/'

    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class PnlPublisherForSurface(pbs_gui_abstracts.AbsPnlPublisherForSurface):
    DCC_NAMESPACE = 'python'
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt

    def __init__(self, session, *args, **kwargs):
        super(PnlPublisherForSurface, self).__init__(session, *args, **kwargs)
