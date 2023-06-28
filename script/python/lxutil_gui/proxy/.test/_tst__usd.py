# coding:utf-8
from lxusd import usd_setup

# usd_setup.UsdSetup(
#     '/data/e/myworkspace/td/lynxi/workspace/resource/linux/usd'
# ).set_run()

import os

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.qt import utl_gui_qt_core


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.set_definition_window_size([720, 720])

        s = prx_widgets.PrxHSplitter()
        self.add_widget(s)

        v = prx_widgets.PrxUsdStageView()
        s.add_widget(v)

        # usd_core.UsdShaderOpt(
        #     s.GetPrimAtPath('/mtl_preview/txr_albedo')
        # ).set_file(
        #     '/production/library/resource/all/surface/cobblestone_vl4jehpn/v0001/texture/original/src/cobblestone_vl4jehpn.albedo.jpg'
        # )

        # usd_core.UsdMaterialAssignOpt(
        #     s.GetPrimAtPath('/geometry/geometry_shape')
        # ).assign('/mtl_preview')

        # v.refresh_usd_stage_for_asset_preview(
        #     '/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/geometry/usd/metal_pot_vfyqcj2ga.usd',
        #     dict(
        #         albedo='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.albedo.jpg',
        #         roughness='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.roughness.jpg',
        #         normal='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.normal.jpg',
        #         displacement='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/original/src/metal_pot_vfyqcj2ga.displacement.jpg'
        #     )
        # )
        # v.refresh_usd_view_draw()

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

        # v.refresh_usd_stage_for_texture_preview(
        #     # use_acescg=True
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

        # v.refresh_usd_stage_for_texture_render(
        #     # dict(
        #     #     albedo='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.albedo.tx',
        #     #     roughness='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.roughness.tx',
        #     #     normal='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.normal.jpg',
        #     #     displacement='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.displacement.tx'
        #     # ),
        #     use_acescg=True
        # )
        # v.refresh_usd_view_draw()

        # v.refresh_usd_stage_for_asset_render(
        #     '/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/geometry/usd/metal_pot_vfyqcj2ga.usd',
        #     dict(
        #         albedo='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.albedo.tx',
        #         roughness='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.roughness.tx',
        #         normal='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.normal.tx',
        #         displacement='/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/texture/acescg/tx/metal_pot_vfyqcj2ga.displacement.tx'
        #     ),
        #     use_acescg=True
        # )
        # v.refresh_usd_view_draw()

        # v.refresh_usd_stage_for_asset_render(
        #     '/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/geometry/usd/rhazya_xdjmfeqqx.usd',
        #     dict(
        #         albedo='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/acescg/tx/rhazya_xdjmfeqqx.albedo.tx',
        #         roughness='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/acescg/tx/rhazya_xdjmfeqqx.roughness.tx',
        #         opacity='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/acescg/tx/rhazya_xdjmfeqqx.opacity.tx',
        #         normal='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/acescg/tx/rhazya_xdjmfeqqx.normal.tx',
        #         displacement='/production/library/resource/all/3d_plant/rhazya_xdjmfeqqx/v0001/texture/acescg/tx/rhazya_xdjmfeqqx.displacement.tx'
        #     ),
        #     use_acescg=True
        # )
        # v.refresh_usd_view_draw()

        v.refresh_usd_stage_for_asset_render(
            '/production/library/resource/all/3d_asset/thai_beach_rocks_ueopcguga/v0001/geometry/usd/thai_beach_rocks_ueopcguga.usd',
            dict(
                albedo='/production/library/resource/all/3d_asset/thai_beach_rocks_ueopcguga/v0001/texture/acescg/tx/thai_beach_rocks_ueopcguga.albedo.tx',
                roughness='/production/library/resource/all/3d_asset/thai_beach_rocks_ueopcguga/v0001/texture/acescg/tx/thai_beach_rocks_ueopcguga.roughness.tx',
                normal='/production/library/resource/all/3d_asset/thai_beach_rocks_ueopcguga/v0001/texture/acescg/tx/thai_beach_rocks_ueopcguga.normal.tx',
                displacement='/production/library/resource/all/3d_asset/thai_beach_rocks_ueopcguga/v0001/texture/acescg/tx/thai_beach_rocks_ueopcguga.displacement.tx'
            ),
            use_acescg=True
        )
        v.refresh_usd_view_draw()


if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_setup

    utl_setup.OcioSetup(
        bsc_core.StgPathMapMtd.map_to_current(
            '/job/PLE/bundle/thirdparty/aces/1.2'
        )
    ).set_run()

    utl_gui_qt_core.set_window_show_standalone(W)

