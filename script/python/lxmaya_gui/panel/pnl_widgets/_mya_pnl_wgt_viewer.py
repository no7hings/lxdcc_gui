# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_utility

import lxmaya.dcc.dcc_objects as mya_dcc_objects

from lxutil_gui.qt import utl_gui_qt_core


class SceneTextureManagerPanel(utl_gui_pnl_abs_utility.AbsSceneTextureManagerPanel):
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(SceneTextureManagerPanel, self).__init__(*args, **kwargs)
    @utl_gui_qt_core.set_prx_window_waiting
    def _set_texture_references_update_(self):
        self._texture_references = mya_dcc_objects.TextureReferences()
