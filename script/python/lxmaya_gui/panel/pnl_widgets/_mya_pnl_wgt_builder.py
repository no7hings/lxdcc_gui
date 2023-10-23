# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import lxgui.proxy.core as gui_prx_core

from lxutil_gui.panel import utl_gui_pnl_abs_builder


class AssetBuilderPanel(utl_gui_pnl_abs_builder.AbsAssetBuilderPanel):
    def __init__(self, *args, **kwargs):
        super(AssetBuilderPanel, self).__init__(*args, **kwargs)

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def _set_build_run_(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=self._options_prx_node.get('project'),
                asset=self._options_prx_node.get('asset').name,
                #
                with_model_geometry=self._options_prx_node.get('build_options.with_model_geometry'),
                #
                with_groom_geometry=self._options_prx_node.get('build_options.with_groom_geometry'), with_groom_grow_geometry=self._options_prx_node.get('build_options.with_groom_grow_geometry'),
                #
                with_surface_geometry_uv_map=self._options_prx_node.get('build_options.with_surface_geometry_uv_map'), with_surface_look=self._options_prx_node.get('build_options.with_surface_look'),
                #
                with_camera=self._options_prx_node.get('build_options.with_camera'), with_light=self._options_prx_node.get('build_options.with_light'),
                #
                render_resolution=self._options_prx_node.get('render.resolution'),
                #
                save_scene=self._options_prx_node.get('build_options.save_scene'),
            )
        ).set_run()
