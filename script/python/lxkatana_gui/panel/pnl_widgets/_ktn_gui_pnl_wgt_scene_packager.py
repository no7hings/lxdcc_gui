# coding:utf-8
from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui.panel import utl_gui_pnl_abs_packager

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class ScenePackagerPanel(utl_gui_pnl_abs_packager.AbsScenePackagerPanel):
    TOOL_PANEL_KEY = 'scene_packager'
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    #
    UTL_OBJ_CLASS = utl_dcc_objects.Obj
    def __init__(self, *args, **kwargs):
        super(ScenePackagerPanel, self).__init__(*args, **kwargs)

    def _set_file_references_update_(self):
        self._texture_references = ktn_dcc_objects.TextureReferences()
        self._file_references = ktn_dcc_objects.TextureReferences()
        return self._file_references.get_objs()
