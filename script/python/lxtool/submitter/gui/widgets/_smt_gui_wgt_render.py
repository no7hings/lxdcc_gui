# coding:utf-8
import lxtool.submitter.gui.abstracts as smt_gui_abstracts


class PnlRenderSubmitterForAsset(smt_gui_abstracts.AbsPnlRenderSubmitterForAsset):
    OPTION_HOOK_KEY = 'tool-panels/asset-render-submitter'

    def __init__(self, hook_option=None, *args, **kwargs):
        super(PnlRenderSubmitterForAsset, self).__init__(hook_option, *args, **kwargs)


class PnlRenderSubmitterForShot(smt_gui_abstracts.AbsPnlRenderSubmitterForShot):
    OPTION_HOOK_KEY = 'tool-panels/shot-render-submitter'

    def __init__(self, hook_option=None, *args, **kwargs):
        super(PnlRenderSubmitterForShot, self).__init__(hook_option, *args, **kwargs)
