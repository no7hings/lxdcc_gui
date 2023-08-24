# coding:utf-8
from lxusd import usd_setup

# usd_setup.UsdSetup(
#     '/data/e/myworkspace/td/lynxi/workspace/resource/linux/usd'
# ).set_run()

import os

from lxbasic import bsc_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.qt import gui_qt_core

import lxdatabase.objects as dtb_objects

bsc_core.LogMtd.TEST = True


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        img_w, img_h = 515, 515
        self.set_definition_window_size([img_w+36, img_h+54])

        s = prx_widgets.PrxHSplitter()
        self.add_widget(s)

        self._usd_stage_view = prx_widgets.PrxUsdStageView()
        s.add_widget(self._usd_stage_view)

        self._main_dir = '/data/e/workspace/lynxi-py3/test/tensor-flow/resource/data'

        # self._data = [
        #     # '/3d_plant_proxy/tree_a001_rsc',
        #     # '/3d_plant_proxy/tree_a002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_b001_rsc',
        #     # '/3d_plant_proxy/tree_b002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_c001_rsc',
        #     # '/3d_plant_proxy/tree_c002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_d001_rsc',
        #     # '/3d_plant_proxy/tree_d002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_e001_rsc',
        #     # '/3d_plant_proxy/tree_e002_rsc',
        #
        #     # '/3d_plant_proxy/tree_f001_rsc',
        #     # '/3d_plant_proxy/tree_g001_rsc',
        #     # '/3d_plant_proxy/tree_h001_rsc',
        #     # '/3d_plant_proxy/tree_i001_rsc',
        #     # '/3d_plant_proxy/tree_j001_rsc',
        #     # '/3d_plant_proxy/tree_k001_rsc',
        #
        #     # '/3d_plant_proxy/tree_f002_rsc',
        #     # '/3d_plant_proxy/tree_g002_rsc',
        #     # '/3d_plant_proxy/tree_h002_rsc',
        #     # '/3d_plant_proxy/tree_i002_rsc',
        #     '/3d_plant_proxy/tree_j002_rsc',
        #
        #     '/3d_plant_proxy/tree_k002_rsc',
        # ]

        self._category_group = '3d_plant_proxy'

        self._dtb_opt = dtb_objects.DtbResourceLibraryOpt(
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-basic'),
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-{}'.format(self._category_group))
        )

        self._data = self._dtb_opt.find_resource_paths_by_category('/3d_plant_proxy/tree')

        self._used_data = []
        for i in self._data:
            if self.check_used(i) is True:
                self._used_data.append(i)

        self._index = 0

        self._index_max = len(self._used_data)

        if self._index_max > 0:
            self._usd_stage_view.widget.pre_geometry_snapshot_finished.connect(self.next_fnc)
            self.next_fnc()

    def next_fnc(self):
        print self._index, self._index_max
        if self._index >= self._index_max:
            return False
        path = self._data[self._index]
        self.build_lib_resource(path)
        self._index += 1
        return True

    def check_used(self, resource_path):
        version_path = '{}/v0001'.format(resource_path)
        path_opt = bsc_core.DccPathDagOpt(version_path)
        cs = path_opt.get_components()
        category_group = cs[-2].get_name()
        dtb_opt = dtb_objects.DtbResourceLibraryOpt(
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-basic'),
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-{}'.format(category_group))
        )
        dtb_version = dtb_opt.get_dtb_version(version_path)

        dtb_version_opt = dtb_objects.DtbVersionOpt(
            dtb_opt, dtb_version
        )

        key = '-'.join(version_path.split('/')[1:])

        dtb_types = dtb_version_opt.get_types()
        dtb_type = dtb_types[0]
        category = bsc_core.DccPathDagOpt(dtb_type.group).get_name()

        main_file_path = '{}/{}/{}.png'.format(self._main_dir, category, key)
        sub_file_p = '{}/{}-component/{}-{{index}}.png'.format(self._main_dir, category, key)
        sub_file_path_0 = sub_file_p.format(index=0)
        if (
            bsc_core.StgFileOpt(main_file_path).get_is_exists() is True
            and bsc_core.StgFileOpt(sub_file_path_0).get_is_exists() is True
        ):
            return False
        return True

    def build_lib_resource(self, resource_path):
        def cache_fnc_():
            bsc_core.LogMtd.test_start('build stage')
            self._usd_stage_view.refresh_usd_stage_for_asset_preview(
                usd_file=dtb_version_opt.get_geometry_usd_file(),
                look_preview_usd_file=dtb_version_opt.get_look_preview_usd_file(),
            )
            bsc_core.LogMtd.test_end('build stage')
            return []

        def build_fnc_():
            bsc_core.LogMtd.test_start('refresh stage')
            self._usd_stage_view.refresh_usd_view_draw()
            bsc_core.LogMtd.test_end('refresh stage')
            self._usd_stage_view.widget._usd_switch_camera_to_('/cameras/cam_front/cam_front_shape')

        def post_fnc_():
            self._usd_stage_view.widget._usd_save_snapshot_to_(
                main_file_path
            )
            self._usd_stage_view.widget._usd_save_per_geometry_snapshot_to_(
                sub_file_p
            )

        version_path = '{}/v0001'.format(resource_path)
        path_opt = bsc_core.DccPathDagOpt(version_path)
        cs = path_opt.get_components()
        category_group = cs[-2].get_name()
        dtb_opt = dtb_objects.DtbResourceLibraryOpt(
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-basic'),
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-{}'.format(category_group))
        )
        dtb_version = dtb_opt.get_dtb_version(version_path)

        dtb_version_opt = dtb_objects.DtbVersionOpt(
            dtb_opt, dtb_version
        )

        key = '-'.join(version_path.split('/')[1:])

        dtb_types = dtb_version_opt.get_types()
        dtb_type = dtb_types[0]
        category = bsc_core.DccPathDagOpt(dtb_type.group).get_name()

        main_file_path = '{}/{}/{}.png'.format(self._main_dir, category, key)
        sub_file_p = '{}/{}-component/{}-{{index}}.png'.format(self._main_dir, category, key)

        self._usd_stage_view.run_as_thread(
            cache_fnc_, build_fnc_, post_fnc_
        )


if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_setup

    utl_setup.OcioSetup(
        bsc_core.StgPathMapMtd.map_to_current(
            '/job/PLE/bundle/thirdparty/aces/1.2'
        )
    ).set_run()

    w = gui_qt_core.show_prx_window_auto(W)


