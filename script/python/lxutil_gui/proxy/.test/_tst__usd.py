# coding:utf-8
from lxusd import usd_setup

usd_setup.UsdSetup(
    '/data/e/myworkspace/td/lynxi/workspace/resource/linux/usd'
).set_run()

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_for_usd

from lxutil_gui.qt import utl_gui_qt_core


class W(_utl_gui_prx_wdt_utility.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.set_definition_window_size([720, 720])

        v = _utl_gui_prx_wgt_for_usd.PrxUsdStageView()
        self.add_widget(v)

        # usd_core.UsdShaderOpt(
        #     s.GetPrimAtPath('/mtl_preview/txr_albedo')
        # ).set_file(
        #     '/production/library/resource/all/surface/cobblestone_vl4jehpn/v0001/texture/original/src/cobblestone_vl4jehpn.albedo.jpg'
        # )

        # usd_core.UsdMaterialAssignOpt(
        #     s.GetPrimAtPath('/geometry/geometry_shape')
        # ).assign('/mtl_preview')

        v.refresh_usd_stage_for_asset_preview(
            '/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/geometry/usd/metal_pot_vfyqcj2ga.usd',
            dict(
                albedo='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.albedo.jpg',
                roughness='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.roughness.jpg',
                normal='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.normal.jpg',
                displacement='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.displacement.jpg'
            )
        )
        v.refresh_usd_view_draw()
        # v.refresh_usd_stage_for_asset_preview(
        #     '/production/library/resource/all/3d_asset/starfish_ue2jfgyjw/v0001/geometry/usd/starfish_ue2jfgyjw.usd',
        #     dict(
        #         albedo='/production/library/resource/all/3d_asset/starfish_ue2jfgyjw/v0001/texture/original/src/starfish_ue2jfgyjw.albedo.jpg',
        #         roughness='/production/library/resource/all/3d_asset/starfish_ue2jfgyjw/v0001/texture/original/src/starfish_ue2jfgyjw.roughness.jpg',
        #         normal='/production/library/resource/all/3d_asset/starfish_ue2jfgyjw/v0001/texture/original/src/starfish_ue2jfgyjw.normal.jpg',
        #         displacement='/production/library/resource/all/3d_asset/starfish_ue2jfgyjw/v0001/texture/original/src/starfish_ue2jfgyjw.displacement.jpg'
        #     )
        # )
        # v.refresh_usd_view_draw()
        # v.refresh_usd_stage_for_asset_preview(
        #     '/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/geometry/usd/rhazya_xdjmfeqqx.usd',
        #     dict(
        #         albedo='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/original/src/rhazya_xdjmfeqqx.albedo.jpg',
        #         roughness='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/original/src/rhazya_xdjmfeqqx.roughness.jpg',
        #         opacity='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/original/src/rhazya_xdjmfeqqx.opacity.jpg',
        #         normal='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/original/src/rhazya_xdjmfeqqx.normal.jpg',
        #         displacement='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/original/src/rhazya_xdjmfeqqx.displacement.jpg'
        #     )
        # )
        # v.refresh_usd_view_draw()


if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_setup
    utl_setup.OcioSetup(
        bsc_core.StgPathMapMtd.map_to_current(
            '/l/packages/pg/third_party/ocio/aces/1.2'
        )
    ).set_run()

    utl_gui_qt_core.set_window_show_standalone(W)

