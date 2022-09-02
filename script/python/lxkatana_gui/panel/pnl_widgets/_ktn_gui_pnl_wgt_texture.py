# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_texture

from lxkatana import ktn_core

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

from lxutil_gui.qt import utl_gui_qt_core


class WorkTextureManager(utl_gui_pnl_abs_texture.AbsWorkspaceTextureManager):
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_NAMESPACE = 'katana'
    def __init__(self, session, *args, **kwargs):
        super(WorkTextureManager, self).__init__(session, *args, **kwargs)

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = ktn_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            dcc_workspace = ktn_dcc_objects.AssetWorkspace()
            dcc_shaders = dcc_workspace.get_all_dcc_shaders()
            self._dcc_objs = self._dcc_texture_references.get_objs(
                include_paths=[i.path for i in dcc_shaders]
            )

    def _set_dcc_scene_update_(self):
        self._file_path = ktn_dcc_objects.Scene.get_current_file_path()


class TextureManager(utl_gui_pnl_abs_texture.AbsDccTextureManager):
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_NAMESPACE = 'maya'
    def __init__(self, *args, **kwargs):
        super(TextureManager, self).__init__(*args, **kwargs)

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = ktn_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            root = self._options_prx_node.get('dcc.location')
            geometry_location = '/root/world/geo'
            location = '{}{}'.format(geometry_location, root)
            dcc_workspace = ktn_dcc_objects.AssetWorkspace()
            dcc_shaders = dcc_workspace.get_all_dcc_geometry_shader_by_location(location)
            self._dcc_objs = self._dcc_texture_references.get_objs(
                include_paths=[i.path for i in dcc_shaders]
            )
