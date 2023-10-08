# coding:utf-8
from lxutil_gui import gui_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxbasic import bsc_core

from lxutil import utl_core

import lxutil_gui.proxy.operators as utl_prx_operators


class AbsPnlShaderViewer(
    prx_widgets.PrxSessionWindow
):
    DCC_MATERIALS_CLS = None
    DCC_SHADER_CLS = None
    #
    DCC_SELECTION_CLS = None
    DCC_NAMESPACE = None
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlShaderViewer, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._set_panel_build_()
        self.refresh_all_fnc()

    def _set_tool_panel_setup_(self):
        self.refresh_all_fnc()

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        # self._set_configure_groups_build_()

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('viewers')
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        h_splitter_0 = prx_widgets.PrxHSplitter()
        expand_box_0.add_widget(h_splitter_0)
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.add_widget(self._filter_tree_viewer_0)
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.add_widget(self._obj_tree_viewer_0)
        h_splitter_0.set_stretches([1, 2])
        #
        self._set_obj_tree_viewer_build_()

    def _set_obj_tree_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('name', 3), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 24
        )
        self._obj_tree_viewer_0.set_header_view_create(
            [('name', 4), ('type', 2)],
            self.get_definition_window_size()[0]*(2.0/3.0) - 24
        )
        #
        self._prx_dcc_obj_tree_view_add_opt = utl_prx_operators.PrxDccObjTreeViewAddOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_selection_opt = utl_prx_operators.PrxDccObjTreeViewSelectionOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )
        self._obj_tree_viewer_0.connect_item_select_changed_to(
            self._prx_dcc_obj_tree_view_selection_opt.set_select
        )
        #
        self._prx_dcc_obj_tree_view_gain_opt = utl_prx_operators.PrxDccObjTreeViewGainOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.GuiTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def refresh_all_fnc(self):
        self._set_dcc_obj_viewer_refresh_()
        #
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def _set_dcc_obj_viewer_refresh_(self):
        self._prx_dcc_obj_tree_view_add_opt.restore_all()
        self._prx_dcc_obj_tree_view_tag_filter_opt.restore_all()
        #
        materials = self.DCC_MATERIALS_CLS().get_objs()
        if materials:
            with utl_core.GuiProgressesRunner.create(maximum=len(materials), label='gui-add for material') as g_p:
                for i_material in materials:
                    g_p.set_update()
                    #
                    material_type_name = 'material'
                    material_gui = self._prx_dcc_obj_tree_view_add_opt.set_prx_item_add_as(i_material, mode='list')
                    #
                    tag_filter_key = 'material.{}'.format(material_type_name)
                    self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                        tag_filter_key, material_gui
                    )
                    #
                    i_shaders = i_material.get_all_source_objs()
                    for i in i_shaders:
                        shader_path = i.path
                        shader = self.DCC_SHADER_CLS(shader_path)
                        shader_type_name = shader.get_shader_type_name()
                        if shader_type_name:
                            shader_gui = self._prx_dcc_obj_tree_view_add_opt.set_prx_item_add_as(shader, mode='list')
                            shader_gui.set_name(shader_type_name, 1)
                            shader_gui.set_icon_by_color(bsc_core.RawTextOpt(shader_type_name).to_rgb(), 1)
                            #
                            tag_filter_key = 'shader.{}'.format(shader_type_name)
                            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                                tag_filter_key, shader_gui
                            )


class AbsPnlMaterialViewer(
    prx_widgets.PrxSessionWindow
):
    DCC_NODE_CLS = None
    DCC_SHAPE_OBJ_CLS = None
    #
    DCC_SCENE_CLS = None
    DCC_SCENE_OPT_CLS = None
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
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlMaterialViewer, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._set_panel_build_()
        self.post_setup_fnc()
        self.refresh_all_fnc()

    def post_setup_fnc(self):
        pass

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()

    def _set_tool_panel_setup_(self):
        self.refresh_all_fnc()

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('viewers')
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        h_splitter_0 = prx_widgets.PrxHSplitter()
        expand_box_0.add_widget(h_splitter_0)
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.add_widget(self._filter_tree_viewer_0)
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.add_widget(self._obj_tree_viewer_0)
        h_splitter_0.set_stretches([1, 2])
        #
        self._set_tree_viewer_build_()

    def _set_tree_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('name', 3), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 24
        )
        #
        self._obj_tree_viewer_0.set_header_view_create(
            [('name', 4), ('type', 2), ('description', 2)],
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
        self._obj_tree_viewer_0.connect_item_select_changed_to(
            self._prx_dcc_obj_tree_view_selection_opt.set_select
        )
        #
        self._prx_dcc_obj_tree_view_gain_opt = utl_prx_operators.PrxDccObjTreeViewGainOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.GuiTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_dcc_selection_args(
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )
        self._filter_tree_viewer_0.connect_item_select_changed_to(
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_select
        )

    def _set_configure_groups_build_(self):
        self._options_prx_node = prx_widgets.PrxNode_('options')
        self.add_widget(self._options_prx_node)
        #
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.get_port(
            'refresh'
        ).set(
            self.refresh_all_fnc
        )

    def refresh_gui_fnc(self):
        self._set_dcc_obj_guis_build_()
        #
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def _set_dcc_obj_guis_build_(self):
        pass

    def refresh_all_fnc(self):
        self.refresh_gui_fnc()

    def _set_dcc_objs_update_from_scene_(self):
        pass
