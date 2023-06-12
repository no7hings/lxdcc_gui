# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import hou

from lxutil import utl_core

from lxutil_gui.panel import utl_gui_pnl_abs_packager

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxhoudini.dcc.dcc_objects as hou_dcc_objects


class ScenePackagerToolPanel(utl_gui_pnl_abs_packager.AbsScenePackagerPanel):
    DCC_SELECTION_CLS = hou_dcc_objects.Selection
    #
    UTL_OBJ_CLS = utl_dcc_objects.Obj

    def __init__(self, *args, **kwargs):
        super(ScenePackagerToolPanel, self).__init__(*args, **kwargs)

    def _set_file_references_update_(self):
        self._texture_references = hou_dcc_objects.TextureReferences()
        self._file_references = hou_dcc_objects.FileReferences()
        return self._file_references.get_objs()
