# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class PnlAssetDccTextureManager(utl_gui_pnl_abstracts.AbsPnlAssetDccTextureManager):
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_NAMESPACE = 'maya'
    def __init__(self, *args, **kwargs):
        super(PnlAssetDccTextureManager, self).__init__(*args, **kwargs)

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = mya_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            self._dcc_objs = self._dcc_texture_references.get_objs()
