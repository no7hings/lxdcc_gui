# coding:utf-8
from lxbasic import bsc_core

import lxutil_gui.qt.widgets as qt_widgets

from lxutil import utl_configure, utl_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxresolver.commands as rsv_commands


class AbsRenderManager(
    prx_widgets.PrxToolWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/asset-render-manager'
    def __init__(self, *args, **kwargs):
        super(AbsRenderManager, self).__init__(*args, **kwargs)
        self._window_configure = utl_configure.MainData.get_as_configure(
            self.CONFIGURE_FILE_PATH
        )
        self.set_window_title(
            self._window_configure.get('window.name')
        )
        self.set_definition_window_size(
            self._window_configure.get('window.size')
        )
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
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

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        #
        h_splitter_0 = prx_widgets.PrxHSplitter()
        expand_box_0.set_widget_add(h_splitter_0)
        v_splitter_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.set_widget_add(v_splitter_0)
        self._rsv_obj_tree_view_0 = prx_widgets.PrxTreeView()
        v_splitter_0.set_widget_add(self._rsv_obj_tree_view_0)
        #
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        v_splitter_0.set_widget_add(self._filter_tree_viewer_0)
        #
        self._rsv_uint_list_view_0 = prx_widgets.PrxListView()
        h_splitter_0.set_widget_add(self._rsv_uint_list_view_0)
        #
        v_splitter_0.set_stretches([1, 1])
        h_splitter_0.set_stretches([1, 3])
        #
        self._set_obj_viewer_build_()

    def _set_obj_viewer_build_(self):
        self._rsv_obj_tree_view_0.set_header_view_create(
            [('Name(s)', 3)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 24
        )
        self._rsv_obj_tree_view_0.set_single_selection()
        #
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/4.0) - 24
        )
        self._filter_tree_viewer_0.set_single_selection()

    def _set_configure_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Configure(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)

        self._prx_node = prx_widgets.PrxNode_()
        expand_box_0.set_widget_add(self._prx_node)

        self._prx_node.set_ports_create_by_configure(
            self._window_configure.get('configure')
        )
