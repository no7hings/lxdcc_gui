# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_texture

from lxutil_gui.qt import utl_gui_qt_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class AssetDccTextureManager(utl_gui_pnl_abs_texture.AbsAssetDccTextureManager):
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_NAMESPACE = 'maya'
    def __init__(self, *args, **kwargs):
        super(AssetDccTextureManager, self).__init__(*args, **kwargs)

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = mya_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            self._dcc_objs = self._dcc_texture_references.get_objs()
