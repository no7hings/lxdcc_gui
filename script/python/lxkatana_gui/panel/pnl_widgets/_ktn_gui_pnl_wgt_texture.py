# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_texture

from lxkatana import ktn_core

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

from lxutil_gui.qt import utl_gui_qt_core


class TextureWorkspace(utl_gui_pnl_abs_texture.AbsTextureWorkspace):
    def __init__(self, *args, **kwargs):
        super(TextureWorkspace, self).__init__(*args, **kwargs)

    def _set_dcc_version_(self, version):
        ktn_core.WorkspaceSettings().set(
            'lynxi.workspace.texture.version', version
        )

    def _get_dcc_version_(self):
        return ktn_core.WorkspaceSettings().get(
            'lynxi.workspace.texture.version'
        )

    def _set_dcc_variant_(self, variant):
        ktn_core.WorkspaceSettings().set(
            'lynxi.workspace.texture.variant', variant
        )

    def _get_dcc_variant_(self):
        return ktn_core.WorkspaceSettings().get(
            'lynxi.workspace.texture.variant'
        )


class WorkTextureManager(utl_gui_pnl_abs_texture.AbsWorkTextureManager):
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    TEXTURE_WORKSPACE_CLS = TextureWorkspace

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

