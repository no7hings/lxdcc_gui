# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_utility

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class SceneTextureManagerPanel(utl_gui_pnl_abs_utility.AbsSceneTextureManagerPanel):
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(SceneTextureManagerPanel, self).__init__(*args, **kwargs)

    def _set_texture_references_update_(self):
        self._texture_references = ktn_dcc_objects.TextureReferences()
