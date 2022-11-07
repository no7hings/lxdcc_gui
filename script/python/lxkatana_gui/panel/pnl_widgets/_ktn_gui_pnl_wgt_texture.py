# coding:utf-8
import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts


class AssetWorkspaceTextureManager(utl_gui_pnl_abstracts.AbsPnlAssetWorkspaceTextureManager):
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_NAMESPACE = 'katana'
    def __init__(self, session, *args, **kwargs):
        super(AssetWorkspaceTextureManager, self).__init__(session, *args, **kwargs)

    def _set_dcc_scene_update_(self):
        self._file_path = ktn_dcc_objects.Scene.get_current_file_path()

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = ktn_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            root = self._options_prx_node.get('dcc.location')
            geometry_location = '/root/world/geo'
            location = '{}{}'.format(geometry_location, root)
            dcc_workspace = ktn_dcc_objects.AssetWorkspace()
            dcc_shaders = dcc_workspace.get_all_dcc_geometry_shaders_by_location(location)
            self._dcc_objs = self._dcc_texture_references.get_objs(
                include_paths=[i.path for i in dcc_shaders]
            )


class PnlAssetDccTextureManager(utl_gui_pnl_abstracts.AbsPnlAssetDccTextureManager):
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_NAMESPACE = 'maya'
    def __init__(self, *args, **kwargs):
        super(PnlAssetDccTextureManager, self).__init__(*args, **kwargs)

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = ktn_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            root = self._options_prx_node.get('dcc.location')
            geometry_location = '/root/world/geo'
            location = '{}{}'.format(geometry_location, root)
            dcc_workspace = ktn_dcc_objects.AssetWorkspace()
            dcc_shaders = dcc_workspace.get_all_dcc_geometry_shaders_by_location(location)
            self._dcc_objs = self._dcc_texture_references.get_objs(
                include_paths=[i.path for i in dcc_shaders]
            )
