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

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self.set_all_refresh()

    def _set_viewer_groups_build_(self):
        h_splitter_0 = prx_widgets.PrxHSplitter()
        self.set_widget_add(h_splitter_0)
        v_splitter_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.set_widget_add(v_splitter_0)
        #
        self._prx_configure_node = prx_widgets.PrxNode_()
        v_splitter_0.set_widget_add(self._prx_configure_node)
        #
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        v_splitter_0.set_widget_add(self._filter_tree_viewer_0)
        #
        self._rsv_uint_list_view_0 = prx_widgets.PrxListView()
        h_splitter_0.set_widget_add(self._rsv_uint_list_view_0)
        #
        v_splitter_0.set_stretches([2, 1])
        h_splitter_0.set_stretches([1, 2])
        #
        self._set_obj_viewer_build_()

    def _set_obj_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/4.0) - 24
        )
        self._filter_tree_viewer_0.set_single_selection()

    def set_all_refresh(self):
        self.set_variables_create()
        self.set_usd_variants_create()

    def set_variables_create(self):
        pass

    def set_usd_variants_create(self):
        self._prx_configure_node.set_ports_create_by_configure(
            self._window_configure.get('node')
        )

        self._prx_configure_node.get_port('create').set(
            self._set_create_
        )

    def _set_create_(self):
        print self._prx_configure_node.get_as_kwargs()

