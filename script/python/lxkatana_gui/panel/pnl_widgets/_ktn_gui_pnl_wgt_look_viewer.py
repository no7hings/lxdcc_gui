# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_look_viewer

from lxbasic import bsc_core

from lxutil import utl_core

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxkatana.dcc.dcc_operators as ktn_dcc_operators

import lxkatana.fnc.importers as ktn_fnc_importers

import lxkatana.fnc.builders as ktn_fnc_builders

from lxkatana import ktn_core


class AssetLookViewerPanel(utl_gui_pnl_abs_look_viewer.AbsAssetLookViewerPanel):
    DCC_SCENE_CLASS = ktn_dcc_objects.Scene
    DCC_FNC_LOOK_IMPORTER_CLASS = ktn_fnc_importers.LookAssImporter
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_STAGE_SELECTION_CLS = ktn_core.SceneGraphSelection
    #
    DCC_NAMESPACE = 'dcc'
    #
    DCC_GEOMETRY_TYPES = [
        'subdmesh',
        'renderer procedural'
    ]
    DCC_GEOMETRY_ROOT = '/root/world/geo/master'
    #
    DCC_MATERIAL_TYPES = [
        'material'
    ]
    DCC_MATERIAL_ROOT = '/root/materials'
    #
    DCC_MATERIALS_CLS = ktn_dcc_objects.Materials
    def __init__(self, *args, **kwargs):
        super(AssetLookViewerPanel, self).__init__(*args, **kwargs)

        self._configure_gui.get_port('geometry_root').set(
            self.DCC_GEOMETRY_ROOT
        )
        self._configure_gui.get_port('material_root').set(
            self.DCC_MATERIAL_ROOT
        )
        self._configure_gui.get_port('look_pass').set(
            ktn_dcc_objects.AssetWorkspace().get_look_pass_names()
        )

    def _set_dcc_obj_guis_build_(self):
        def add_geometry_gui_fnc_(geometry_obj_):
            def select_material_fnc_():
                if _material_obj is not None:
                    self.DCC_SELECTION_CLS([_material_obj.path]).set_all_select()
            #
            def select_nmc_material_fnc_():
                if _material_obj is not None:
                    _nmc_material_obj = nmc_material_dict[_material_scene_graph_path]
                    self.DCC_SELECTION_CLS([_nmc_material_obj.path]).set_all_select()
            #
            def select_nme_material_fnc_():
                if _material_obj is not None:
                    _nme_material_obj = nme_material_dict[_material_scene_graph_path]
                    self.DCC_SELECTION_CLS([_nme_material_obj.path]).set_all_select()
            #
            def get_nme_material_is_exists_fnc():
                return _material_scene_graph_path in nme_material_dict
            #
            def expanded_shaders_fnc_():
                if _material_obj is not None:
                    objs = _material_obj.get_all_source_objs()
                    [ktn_core.NGObjOpt(i.ktn_obj).set_gui_expanded() for i in objs]
            #
            def collapsed_shaders_fnc_():
                if _material_obj is not None:
                    objs = _material_obj.get_all_source_objs()
                    [ktn_core.NGObjOpt(i.ktn_obj).set_gui_collapsed() for i in objs]
            #
            def colour_shaders_fnc_():
                if _material_obj is not None:
                    _material_obj.set_source_objs_colour()
            #
            def layout_shaders_with_expanded_fnc_():
                if _material_obj is not None:
                    ktn_core.NGObjOpt(_material_obj.ktn_obj).set_gui_layout(size=(320, 960), expanded=True)
            #
            def layout_shaders_with_collapsed_fnc_():
                if _material_obj is not None:
                    ktn_core.NGObjOpt(_material_obj.ktn_obj).set_gui_layout(size=(320, 240), collapsed=True)
            #
            geometry_obj_.set_gui_attribute(
                'gui_menu',
                [
                    ('Select material', None, select_material_fnc_),
                    (),
                    ('Select material in "NetworkMaterialCreate"', None, select_nmc_material_fnc_),
                    ('Select material in "NetworkMaterialEdit"', None, (get_nme_material_is_exists_fnc, select_nme_material_fnc_, False)),
                    (),
                    ('Expanded shader(s)', None, expanded_shaders_fnc_),
                    ('Collapsed shader(s)', None, collapsed_shaders_fnc_),
                    (),
                    ('Colour shader(s)', None, colour_shaders_fnc_),
                    (),
                    ('Layout shader(s) with expanded', None, layout_shaders_with_expanded_fnc_),
                    ('Layout shader(s) with collapsed', None, layout_shaders_with_collapsed_fnc_),
                ]
            )
            #
            _geometry_obj_gui = self._prx_dcc_obj_tree_view_add_opt.set_item_prx_add_as(
                geometry_obj, mode='list'
            )
            #
            _key = 'material-assign'
            #
            _obj_opt = geometry_obj_.obj_opt
            _material_scene_graph_path = _obj_opt.get_port_raw('materialAssign')
            if _material_scene_graph_path is not None:
                _sub_material_key = bsc_core.DccPathDagOpt(_material_scene_graph_path).name
                _material_obj = material_dict[_material_scene_graph_path]
            else:
                _geometry_obj_gui.check_state.set('ignore')
                _sub_material_key = 'non-exists'
                _material_obj = None
            #
            _material_tag_filter_key = '{}.{}.{}'.format(_key, geometry_obj_.type.name, _sub_material_key)
            #
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                _material_tag_filter_key,
                _geometry_obj_gui,
                dcc_obj=_material_obj
            )
            _geometry_obj_gui.set_name(_sub_material_key, self.DESCRIPTION_INDEX)
            _material_color = bsc_core.TextOpt(_sub_material_key).to_rgb()
            _geometry_obj_gui.set_color_icon(_material_color, self.DESCRIPTION_INDEX)
        #
        self._prx_dcc_obj_tree_view_add_opt.set_restore()
        #
        methods = [
            self._set_dcc_objs_update_from_scene_,
        ]
        if methods:
            gp = utl_core.GuiProgressesRunner(maximum=len(methods))
            for method in methods:
                gp.set_update()
                method()
            gp.set_stop()
        #
        geometry_objs = self._scene_geometry_objs
        material_dict = ktn_dcc_objects.Materials.get_material_dict()
        nmc_material_dict = ktn_dcc_objects.Materials.get_nmc_material_dict()
        nme_material_dict = ktn_dcc_objects.Materials.get_nme_material_dict()
        if geometry_objs:
            for geometry_obj in geometry_objs:
                add_geometry_gui_fnc_(geometry_obj)


if __name__ == '__main__':
    import lxkatana
    lxkatana.set_reload()
    #
    import lxkatana_gui.panel.pnl_widgets as ktn_pnl_widgets
    w = ktn_pnl_widgets.AssetLookViewerPanel()
    w.set_window_show()
