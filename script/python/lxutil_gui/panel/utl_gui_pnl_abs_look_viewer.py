# coding:utf-8
import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui import utl_gui_core

import lxutil_gui.proxy.operators as utl_prx_operators


class AbsAssetLookViewerPanel(
    prx_widgets.PrxToolWindow
):
    PANEL_KEY = 'asset_look_viewer'
    #
    DCC_OBJ_CLASS = None
    DCC_SHAPE_OBJ_CLASS = None
    #
    DCC_SCENE_CLASS = None
    DCC_SCENE_OPT_CLASS = None
    DCC_NAMESPACE = None
    #
    DCC_SELECTION_CLS = None
    DCC_STAGE_SELECTION_CLS = None
    #
    DCC_GEOMETRY_TYPES = []
    DCC_GEOMETRY_ROOT = None
    #
    DCC_MATERIAL_TYPES = []
    DCC_MATERIAL_ROOT = None
    #
    DCC_MATERIALS_CLS = None
    #
    DESCRIPTION_INDEX = 2
    def __init__(self, *args, **kwargs):
        super(AbsAssetLookViewerPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_gui_core.PanelsConfigure().get_window(
            self.PANEL_KEY
        )
        self.set_window_title(
            self._window_configure.get('name')
        )
        self.set_definition_window_size(
            self._window_configure.get('size')
        )
        #
        self._set_panel_build_()
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_refresh_all_()

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        h_splitter_0 = prx_widgets.PrxHSplitter()
        expand_box_0.set_widget_add(h_splitter_0)
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.set_widget_add(self._filter_tree_viewer_0)
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.set_widget_add(self._obj_tree_viewer_0)
        h_splitter_0.set_stretches([1, 2])
        #
        self._set_tree_viewer_build_()

    def _set_tree_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 24
        )
        #
        self._obj_tree_viewer_0.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 2), ('Description(s)', 2)],
            self.get_definition_window_size()[0]*(2.0/3.0) - 24
        )
        #
        self._prx_dcc_obj_tree_view_add_opt = utl_prx_operators.PrxDccObjTreeViewAddOpt1(
            prx_tree_view=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_selection_opt = utl_prx_operators.PrxDccObjTreeViewSelectionOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            dcc_selection_cls=self.DCC_STAGE_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )
        self._obj_tree_viewer_0.set_item_select_changed_connect_to(
            self._prx_dcc_obj_tree_view_selection_opt.set_select
        )
        #
        self._prx_dcc_obj_tree_view_gain_opt = utl_prx_operators.PrxDccObjTreeViewGainOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_dcc_selection_args(
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )
        self._filter_tree_viewer_0.set_item_select_changed_connect_to(
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_select
        )

    def _set_configure_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Configure(s)')
        expand_box_0.set_expanded(True)
        expand_box_0.set_size_mode(1)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._configure_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._configure_gui.widget)
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxTextPort('geometry_root', 'Geometry-root')
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxTextPort('material_root', 'Material-root')
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('look_pass', 'Look-pass')
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxButtonPort('refresh', 'Refresh')
        )
        _port.set(self._set_obj_gui_refresh_)

    def _set_obj_gui_refresh_(self):
        self._set_dcc_obj_guis_build_()
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def _set_dcc_obj_guis_build_(self):
        pass

    def _set_refresh_all_(self):
        self._set_obj_gui_refresh_()

    def _set_dcc_objs_update_from_scene_(self):
        look_pass = self._configure_gui.get_port('look_pass').get()
        self._scene_obj_scene = self.DCC_SCENE_CLASS()
        ktn_obj_path = '{}__property_assigns_merge'.format(look_pass)
        self._scene_obj_scene.set_load_by_root(
            ktn_obj='look_pass_switch',
            root=self.DCC_GEOMETRY_ROOT
        )
        self._scene_obj_scene.set_load_by_root(
            ktn_obj='look_pass_switch',
            root=self.DCC_MATERIAL_ROOT
        )
        self._scene_obj_universe = self._scene_obj_scene.universe
        #
        self._scene_geometry_objs = []
        #
        self._scene_geometry_root = self._scene_obj_universe.get_obj(self.DCC_GEOMETRY_ROOT)
        geometry_types = [self._scene_obj_universe.get_obj_type(i) for i in self.DCC_GEOMETRY_TYPES]
        for geometry_type in geometry_types:
            if geometry_type is not None:
                self._scene_geometry_objs.extend(
                    geometry_type.get_objs()
                )
        #
        self._scene_material_objs = []
        #
        self._scene_material_root = self._scene_obj_universe.get_obj(self.DCC_MATERIAL_ROOT)
        material_types = [self._scene_obj_universe.get_obj_type(i) for i in self.DCC_MATERIAL_TYPES]
        for material_type in material_types:
            if material_type is not None:
                self._scene_material_objs.extend(
                    material_type.get_objs()
                )
