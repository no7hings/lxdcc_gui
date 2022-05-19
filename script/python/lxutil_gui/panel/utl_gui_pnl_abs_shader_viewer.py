# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil_gui import utl_gui_core

import lxutil_gui.proxy.operators as utl_prx_operators


class AbsSceneShaderViewerPanel(
    prx_widgets.PrxToolWindow
):
    PANEL_KEY = 'scene_shader_viewer'
    #
    DCC_MATERIALS_CLS = None
    DCC_SHADER_CLS = None
    #
    DCC_SELECTION_CLS = None
    DCC_NAMESPACE = None
    def __init__(self, *args, **kwargs):
        super(AbsSceneShaderViewerPanel, self).__init__(*args, **kwargs)

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

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_refresh_all_()

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        # self._set_configure_groups_build_()

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
        self._set_obj_tree_viewer_build_()

    def _set_obj_tree_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 24
        )
        self._obj_tree_viewer_0.set_header_view_create(
            [('Name(s)', 4), ('Katana-type(s)', 2), ('Arnold-type(s)', 2)],
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

    def _set_refresh_all_(self):
        self._set_dcc_obj_viewer_refresh_()
        #
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def _set_dcc_obj_viewer_refresh_(self):
        self._prx_dcc_obj_tree_view_add_opt.set_restore()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_restore()
        #
        materials = self.DCC_MATERIALS_CLS().get_objs()
        if materials:
            gp = utl_core.GuiProgressesRunner(maximum=len(materials))
            for material in materials:
                gp.set_update()
                #
                material_type_name = 'material'
                material_gui = self._prx_dcc_obj_tree_view_add_opt.set_prx_item_add_as(material, mode='list')
                #
                tag_filter_key = 'material.{}'.format(material_type_name)
                self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                    tag_filter_key, material_gui
                )
                #
                shaders = material.get_all_source_objs()
                for i in shaders:
                    shader_path = i.path
                    shader = self.DCC_SHADER_CLS(shader_path)
                    shader_type_name = shader.get_shader_type_name()
                    if shader_type_name:
                        shader_gui = self._prx_dcc_obj_tree_view_add_opt.set_prx_item_add_as(shader, mode='list')
                        shader_gui.set_name(shader_type_name, 2)
                        shader_gui.set_icon_by_color(bsc_core.TextOpt(shader_type_name).to_rgb(), 2)
                        #
                        tag_filter_key = 'shader.{}'.format(shader_type_name)
                        self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                            tag_filter_key, shader_gui
                        )
            #
            gp.set_stop()
