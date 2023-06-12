# coding:utf-8
from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui.panel import utl_gui_pnl_abs_packager

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class ScenePackagerToolPanel(utl_gui_pnl_abs_packager.AbsScenePackagerPanel):
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    #
    UTL_OBJ_CLS = utl_dcc_objects.Obj
    def __init__(self, *args, **kwargs):
        super(ScenePackagerToolPanel, self).__init__(*args, **kwargs)

    def _set_file_references_update_(self):
        self._texture_references = mya_dcc_objects.TextureReferences()
        self._file_references = mya_dcc_objects.FileReferences()
        return self._file_references.get_objs()
