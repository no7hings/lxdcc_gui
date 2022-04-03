# coding:utf-8
import lxbasic.objects as bsc_objects
#
from lxutil import utl_configure, utl_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

import lxresolver.commands as rsv_commands

import lxresolver.operators as rsv_operators

import lxutil_gui.proxy.operators as utl_prx_operators


class AbsAssetComparerPanel(
    prx_widgets.PrxToolWindow
):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file('utility/panel/asset-comparer')
    HELP_FILE_PATH = utl_configure.MainData.get_help_file('utility/panel/asset-comparer')
    #
    PANEL_KEY = 'asset_comparer'
    #
    DCC_OBJ_CLASS = None
    #
    FNC_GEOMETRY_COMPARER = None
    #
    DESCRIPTION_INDEX = 2
    #
    DCC_SELECTION_CLS = None
    #
    USD_NAMESPACE = 'usd'
    #
    DCC_NAMESPACE = None
    DCC_OBJ_PATHSEP = None
    def __init__(self, *args, **kwargs):
        super(AbsAssetComparerPanel, self).__init__(*args, **kwargs)
        self._toolkit_configure = bsc_objects.Configure(value=self.CONFIGURE_FILE_PATH)
        #
        self.set_window_title(self._toolkit_configure.get('window.name'))
        self.set_definition_window_size(self._toolkit_configure.get('window.size'))
        #
        self._set_panel_build_()
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()
        #
        self._update_geometry_from_model_item = prx_widgets.PrxPressItem()
        self._update_geometry_from_model_item.set_name('Update Geometry(s) from model')
        self._update_geometry_from_model_item.set_icon_by_text('Update Geometry(s) from model')
        self._update_geometry_from_model_item.set_tool_tip(
            [
                'press to update geometry(s) form model task'
            ]
        )
        self.set_button_add(self._update_geometry_from_model_item)
        self._update_geometry_from_model_item.set_press_clicked_connect_to(self._set_checked_geometry_import_from_model_)
        #
        self._update_geometry_from_surface_item = prx_widgets.PrxPressItem()
        self._update_geometry_from_surface_item.set_name('Update Geometry(s) from surface')
        self._update_geometry_from_surface_item.set_icon_by_text('Update Geometry(s) from surface')
        self.set_button_add(self._update_geometry_from_surface_item)
        self._update_geometry_from_surface_item.set_enable(False)
        # self._update_geometry_from_surface_item.set_press_clicked_connect_to(self._set_checked_geometry_import_)
        #
        self._update_look_from_surface_item = prx_widgets.PrxPressItem()
        self._update_look_from_surface_item.set_name('Update Look(s) from surface')
        self._update_look_from_surface_item.set_icon_by_text('Update Look(s) from surface')
        self.set_button_add(self._update_look_from_surface_item)
        self._update_look_from_surface_item.set_enable(False)
        self._update_look_from_surface_item.set_press_clicked_connect_to(self._set_checked_look_import_from_surface_)

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        h_splitter_0 = prx_widgets.PrxHSplitter()
        v_splitter_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.set_widget_add(v_splitter_0)
        expand_box_0.set_widget_add(h_splitter_0)
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        v_splitter_0.set_widget_add(self._filter_tree_viewer_0)
        self._sector_chart = prx_widgets.PrxSectorChart()
        v_splitter_0.set_widget_add(self._sector_chart)
        self._radar_chart = prx_widgets.PrxRadarChart()
        v_splitter_0.set_widget_add(self._radar_chart)
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.set_widget_add(self._obj_tree_viewer_0)
        h_splitter_0.set_stretches([1, 2])
        #
        self._set_tree_viewer_build_()

    def _set_tree_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 24
        )
        #
        self._obj_tree_viewer_0.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 2), ('Check-status(s)', 2)],
            self.get_definition_window_size()[0]*(2.0/3.0) - 24
        )
        #
        self._prx_usd_mesh_tree_view_add_opt = utl_prx_operators.PrxUsdMeshTreeviewAddOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxDccObjTreeItem,
            tgt_obj_namespace=self.DCC_NAMESPACE,
            tgt_obj_pathsep=self.DCC_OBJ_PATHSEP,
            tgt_obj_class=self.DCC_OBJ_CLASS
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
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def _set_configure_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Configure(s)')
        # expand_box_0.set_expanded(True)
        expand_box_0.set_size_mode(1)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._configure_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._configure_gui.widget)
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxTextPort('scene_file_path', 'Scene-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('model_usd_file_path', 'Model-usd-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('model_ass_file_path', 'Model-ass-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('surface_usd_file_path', 'Surface-usd-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('surface_ass_file_path', 'Surface-ass-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('cache_directory_path', 'Cache-directory')
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxTextPort('scene_root', 'Scene-root')
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxButtonPort('refresh', 'Refresh')
        )
        _port.set(self._set_obj_gui_refresh_)

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_refresh_all_()

    def _set_dcc_obj_guis_build_(self):
        self._prx_usd_mesh_tree_view_add_opt.set_restore()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_restore()
        #
        scene_file_path = self._configure_gui.get_port('scene_file_path').get()
        root = self._configure_gui.get_port('scene_root').get()
        self._fnc_dcc_geometry_comparer = self.FNC_GEOMETRY_COMPARER(
            scene_file_path, root
        )
        #
        self._fnc_dcc_geometry_comparer._set_model_geometry_usd_hi_file_path_(
            self._configure_gui.get_port('model_usd_file_path').get()
        )
        #
        sector_chart_data_dict = {}
        comparer_results = self._fnc_dcc_geometry_comparer.get_results()
        count = len(comparer_results)
        if comparer_results:
            g_p = utl_core.GuiProgressesRunner(maximum=count)
            for i_src_geometry_path, i_tgt_geometry_path, i_check_statuses in comparer_results:
                i_check_statuses_list = i_check_statuses.split('+')
                for j_check_status in i_check_statuses_list:
                    sector_chart_data_dict.setdefault(
                        j_check_status, []
                    ).append(
                        i_src_geometry_path
                    )
                g_p.set_update()
                i_src_dcc_geometry = self._fnc_dcc_geometry_comparer.get_scene_dcc_geometry(i_src_geometry_path)
                if i_src_dcc_geometry is None:
                    i_src_dcc_geometry = self._fnc_dcc_geometry_comparer.get_model_dcc_geometry(i_src_geometry_path)
                #
                if i_src_dcc_geometry.type_name in ['Mesh', 'mesh']:
                    i_src_mesh_item_prx = self._prx_usd_mesh_tree_view_add_opt.set_item_prx_add_as(
                        i_src_dcc_geometry, mode='list'
                    )
                    self._prx_usd_mesh_tree_view_add_opt.set_item_prx_update(i_src_dcc_geometry)
                    #
                    key = 'from-model'
                    if i_check_statuses == utl_configure.DccMeshCheckStatus.NON_CHANGED:
                        i_src_mesh_item_prx.set_adopt_state()
                    else:
                        if i_tgt_geometry_path is not None:
                            i_src_mesh_item_prx.set_warning_state()
                        else:
                            i_src_mesh_item_prx.set_error_state()
                    #
                    tag_filter_key = '{}.{}'.format(key, i_check_statuses)
                    #
                    self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                        tag_filter_key, i_src_mesh_item_prx
                    )
                    #
                    i_src_mesh_item_prx.set_gui_attribute(
                        'src_mesh_dcc_path', i_src_geometry_path
                    )
                    i_src_mesh_item_prx.set_gui_attribute(
                        'tgt_mesh_dcc_path', i_tgt_geometry_path
                    )
                    i_src_mesh_item_prx.set_gui_attribute(
                        'check_statuses', i_check_statuses
                    )
                    #
                    i_src_mesh_item_prx.set_name(i_check_statuses, self.DESCRIPTION_INDEX)
                    if i_tgt_geometry_path is not None:
                        i_src_mesh_item_prx.set_tool_tip(i_tgt_geometry_path, self.DESCRIPTION_INDEX)
            #
            g_p.set_stop()
        #
        sector_chart_data = []
        for i_check_status in utl_configure.DccMeshCheckStatus.ALL:
            if i_check_status != utl_configure.DccMeshCheckStatus.NON_CHANGED:
                if i_check_status in sector_chart_data_dict:
                    sector_chart_data.append(
                        (i_check_status, count, len(sector_chart_data_dict[i_check_status]))
                    )
                else:
                    sector_chart_data.append(
                        (i_check_status, count, 0)
                    )
        #
        self._sector_chart.set_chart_data(
            sector_chart_data,
            utl_configure.GuiSectorChartMode.Error
        )

    def _set_radar_chart_refresh_(self):
        pass

    def _set_refresh_all_(self):
        resolver = rsv_commands.get_resolver()
        scene_file_path = self._configure_gui.get_port('scene_file_path').get()
        self._task_properties = resolver.get_task_properties_by_any_scene_file_path(
            file_path=scene_file_path
        )
        if self._task_properties is not None:
            step = self._task_properties.get('step')
            if step in ['mod', 'srf', 'rig']:
                model_geometry_usd_hi_file_paths = rsv_operators.RsvAssetGeometryQuery(
                    self._task_properties
                ).get_usd_hi_file(
                    step='mod', task='modeling', version='all'
                )
                if model_geometry_usd_hi_file_paths:
                    _port = self._configure_gui.get_port('model_usd_file_path')
                    _port.set(model_geometry_usd_hi_file_paths)
                    _port.set_current(model_geometry_usd_hi_file_paths[-1])
                #
                model_look_ass_file_paths = rsv_operators.RsvAssetLookQuery(
                    self._task_properties
                ).get_ass_file(
                    step='mod', task='modeling', version='all'
                )
                if model_look_ass_file_paths:
                    _port = self._configure_gui.get_port('model_ass_file_path')
                    _port.set(model_look_ass_file_paths)
                    _port.set_current(model_look_ass_file_paths[-1])
                #
                surface_geometry_usd_hi_file_paths = rsv_operators.RsvAssetGeometryQuery(
                    self._task_properties
                ).get_usd_hi_file(
                    step='srf', task='surfacing', version='all'
                )
                if surface_geometry_usd_hi_file_paths:
                    _port = self._configure_gui.get_port('surface_usd_file_path')
                    _port.set(surface_geometry_usd_hi_file_paths)
                    _port.set_current(surface_geometry_usd_hi_file_paths[-1])
                #
                surface_look_ass_file_paths = rsv_operators.RsvAssetLookQuery(
                    self._task_properties
                ).get_ass_file(
                    step='srf', task='surfacing', version='all'
                )
                if surface_look_ass_file_paths:
                    _port = self._configure_gui.get_port('surface_ass_file_path')
                    _port.set(surface_look_ass_file_paths)
                    _port.set_current(surface_look_ass_file_paths[-1])
                #
                self._configure_gui.get_port('scene_root').set(
                    '/master/hi'
                )
                _port = self._configure_gui.get_port('cache_directory_path')
                if step == 'mod':
                    _port.set(
                        rsv_operators.RsvAssetSceneQuery(self._task_properties).get_work_cache_directory(
                            task='modeling'
                        )
                    )
                elif step == 'srf':
                    _port.set(
                        rsv_operators.RsvAssetSceneQuery(self._task_properties).get_work_cache_directory(
                            task='surfacing'
                        )
                    )
                elif step == 'rig':
                    _port.set(
                        rsv_operators.RsvAssetSceneQuery(self._task_properties).get_work_cache_directory(
                            task='rigging'
                        )
                    )
            #
            self._set_obj_gui_refresh_()
    #
    def _set_obj_gui_refresh_(self):
        self._set_dcc_obj_guis_build_()
        self._set_radar_chart_refresh_()
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def _get_checked_geometry_objs_(self):
        lis = []
        for i_item_prx in self._obj_tree_viewer_0.get_all_items():
            if i_item_prx.get_is_checked() is True:
                i_dcc_obj = i_item_prx.get_gui_dcc_obj(namespace=self.USD_NAMESPACE)
                if i_dcc_obj is not None:
                    lis.append((i_item_prx, i_dcc_obj))
        return lis

    def _set_checked_geometry_import_from_model_(self):
        checked_src_geometries = self._get_checked_geometry_objs_()
        if checked_src_geometries:
            g_p = utl_core.GuiProgressesRunner(maximum=len(checked_src_geometries))
            for i_src_geometry_item_prx, i_src_dcc_geometry in checked_src_geometries:
                g_p.set_update()
                if i_src_dcc_geometry.type_name in ['Mesh', 'mesh']:
                    i_tgt_dcc_mesh_path = i_src_geometry_item_prx.get_gui_attribute('tgt_mesh_dcc_path')
                    if i_tgt_dcc_mesh_path is not None:
                        i_check_statuses = i_src_geometry_item_prx.get_gui_attribute('check_statuses')
                        i_src_mesh_dcc_path = i_src_dcc_geometry.path
                        self._fnc_dcc_geometry_comparer.set_mesh_repair(
                            i_src_mesh_dcc_path, i_tgt_dcc_mesh_path, i_check_statuses
                        )
            #
            g_p.set_stop()
        #
        self._set_obj_gui_refresh_()

    def _set_path_exchanged_repair_(self, i_tgt_mesh, i_tgt_data):
        pass

    def _set_checked_look_import_from_surface_(self):
        pass
