# coding:utf-8
from lxbasic import bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.core as gui_prx_core

from lxutil import utl_configure

import lxgui.proxy.widgets as prx_widgets

import lxresolver.commands as rsv_commands


class AbsAssetBuilderPanel(
    prx_widgets.PrxBaseWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/asset-builder'

    def __init__(self, *args, **kwargs):
        super(AbsAssetBuilderPanel, self).__init__(*args, **kwargs)
        self._option_hook_configure = utl_configure.MainData.get_as_configure(
            self.CONFIGURE_FILE_PATH
        )
        self._hook_gui_configure = self._option_hook_configure.get_content('option.gui')
        self._hook_build_configure = self._option_hook_configure.get_content('build')
        raw = bsc_core.EnvironMtd.get('REZ_BETA')
        if raw:
            self._rez_beta = True
        else:
            self._rez_beta = False
        #
        if self._rez_beta:
            self.set_window_title(
                '[BETA] {}'.format(self._hook_gui_configure.get('name'))
            )
        else:
            self.set_window_title(
                self._hook_gui_configure.get('name')
            )

        self.set_window_icon_name_text(
            self._hook_gui_configure.get('name')
        )
        self.set_definition_window_size(
            self._hook_gui_configure.get('size')
        )
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.start_loading(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        self._set_group_0_build_()

    def _set_tool_panel_setup_(self):
        self.refresh_all_fnc()

    def _set_group_0_build_(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.options')
        )
        #
        _port = self._options_prx_node.get_port('project')
        histories = _port.get_histories()
        if histories:
            _port.set(histories[-1])
        #
        current_project = self._get_current_project_()
        if current_project:
            if current_project in _port.get_histories():
                _port.set(
                    current_project
                )
        #
        self._options_prx_node.set('refresh', self.refresh_all_fnc)
        self._options_prx_node.set('check_all', self._set_check_all_)
        self._options_prx_node.set('check_clear', self._set_check_clear_)
        self._options_prx_node.set('build', self._set_build_run_)

    @classmethod
    def _get_current_project_(cls):
        import os

        _ = os.environ.get('PG_SHOW')
        if _:
            return _.lower()

    def _set_assets_(self):
        project = self._options_prx_node.get_port('project').get()
        resolver = rsv_commands.get_resolver()
        rsv_project = resolver.get_rsv_project(project=project)
        rsv_assets = rsv_project.get_rsv_resources(branch='asset')
        assets = [
            i.name for i in rsv_assets
        ]
        self._options_prx_node.set(
            'asset', rsv_assets
        )

    def _set_check_all_(self):
        for i in self._options_prx_node.get_port('build_options').get_children():
            i.set(True)

    def _set_check_clear_(self):
        for i in self._options_prx_node.get_port('build_options').get_children():
            i.set(False)

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def refresh_all_fnc(self):
        self._set_assets_()

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def _set_build_run_(self):
        pass
