# coding:utf-8
from lxbasic import bsc_core

import lxutil_gui.qt.widgets as qt_widgets

from lxutil import utl_configure, utl_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxresolver.commands as rsv_commands


class AbsAssetBuilderPanel(
    prx_widgets.PrxToolWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/asset-builder'
    def __init__(self, *args, **kwargs):
        super(AbsAssetBuilderPanel, self).__init__(*args, **kwargs)
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
        self._set_group_0_build_()

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_refresh_all_()

    def _set_group_0_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Build-tool(s)')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._node_prx_0 = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._node_prx_0.widget)
        #
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxEnumeratePort('project', 'Project-name')
        )
        projects = self._get_projects_()
        _port.set(
            projects
        )
        _port.set_tool_tip(
            [
                'choose or enter one "project-name"'
            ]
        )
        current_project = self._get_current_project_()
        if current_project in projects:
            _port.set_current(
                current_project
            )
        #
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxEnumeratePort('asset', 'Asset-name')
        )
        _port.set_tool_tip(
            [
                'choose or enter one "asset-name"'
            ]
        )
        #
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxButtonPort('refresh', 'Refresh')
        )
        _port.set(
            self._set_refresh_all_
        )
        _port.set_tool_tip(
            [
                'press to refresh assets'
            ]
        )
        #
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxBooleanPort('with_model_geometry', 'With Model-geometry', default_value=True, join_to_next=True)
        )
        _port.set_tool_tip(
            [
                'import "Model-geometry" from "USD" if it is checked'
            ]
        )
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxBooleanPort('with_surface_geometry_uv_map', 'With Surface-geometry UV-map', default_value=True, join_to_next=True)
        )
        _port.set_tool_tip(
            [
                'import "Surface-geometry" "UV-map" from "USD" if it is checked'
            ]
        )
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxBooleanPort('with_groom_geometry', 'With Groom-geometry', default_value=True, join_to_next=True)
        )
        _port.set_tool_tip(
            [
                'import "Groom-geometry" ( xgen, xgen-glow ) from "xgen", "Alembic" if it is checked'
            ]
        )
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxBooleanPort('with_surface_look', 'With Surface-look', default_value=True)
        )
        _port.set_tool_tip(
            [
                'import surface-look ( material, properties, visibility, assign ) from "ASS" if it is checked'
            ]
        )
        #
        _port = self._node_prx_0.set_port_add(
            prx_widgets.PrxButtonPort('build', 'Build')
        )
        _port.set_tool_tip(
            [
                'press for build checked unit'
            ]
        )
        _port.set(
            self._set_build_run_
        )
    @classmethod
    def _get_current_project_(cls):
        import os
        _ = os.environ.get('PG_SHOW')
        if _:
            return _.lower()
    @classmethod
    def _get_projects_(cls):
        return ['shl', 'lib', 'cjd']

    def _set_assets_(self):
        project = self._node_prx_0.get_port('project').get()
        resolver = rsv_commands.get_resolver()
        rsv_project = resolver.get_rsv_project(project=project)
        rsv_assets = rsv_project.get_rsv_entities(branch='asset')
        assets = [
            i.name for i in rsv_assets
        ]
        self._node_prx_0.get_port('asset').set(assets)

    def _set_refresh_all_(self):
        self._set_assets_()

    def _set_build_run_(self):
        pass
