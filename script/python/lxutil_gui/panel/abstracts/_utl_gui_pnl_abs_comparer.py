# coding:utf-8
from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects
#
from lxutil import utl_configure, utl_core

from lxutil_gui import utl_gui_configure, utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

import lxutil_gui.proxy.operators as utl_prx_operators

import lxresolver.commands as rsv_commands

import lxresolver.operators as rsv_operators


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
        self._update_geometry_from_model_item.set_icon_by_name_text('Update Geometry(s) from model')
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
        self._update_geometry_from_surface_item.set_icon_by_name_text('Update Geometry(s) from surface')
        self.set_button_add(self._update_geometry_from_surface_item)
        self._update_geometry_from_surface_item.set_enable(False)
        # self._update_geometry_from_surface_item.set_press_clicked_connect_to(self._set_checked_geometry_import_)
        #
        self._update_look_from_surface_item = prx_widgets.PrxPressItem()
        self._update_look_from_surface_item.set_name('Update Look(s) from surface')
        self._update_look_from_surface_item.set_icon_by_name_text('Update Look(s) from surface')
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
            prx_widgets.PrxFileOpenPort('scene_file_path', 'Scene-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxPortForEnumerate('model_usd_file_path', 'Model-usd-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxPortForEnumerate('model_ass_file_path', 'Model-ass-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxPortForEnumerate('surface_usd_file_path', 'Surface-usd-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxPortForEnumerate('surface_ass_file_path', 'Surface-ass-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxPortForEnumerate('cache_directory_path', 'Cache-directory')
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxPortForString('scene_root', 'Scene-root')
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxButtonPort('refresh', 'Refresh')
        )
        _port.set(self._set_obj_gui_refresh_)

    def _set_tool_panel_setup_(self):
        self._set_refresh_all_()

    @utl_gui_qt_core.set_prx_window_waiting
    def _set_comparer_result_update_(self):
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
        return self._fnc_dcc_geometry_comparer.get_results()

    def _set_dcc_obj_guis_build_(self):
        self._prx_usd_mesh_tree_view_add_opt.set_restore()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_restore()
        #
        comparer_results = self._set_comparer_result_update_()
        #
        sector_chart_data_dict = {}
        count = len(comparer_results)
        if comparer_results:
            with utl_core.GuiProgressesRunner.create(maximum=count, label='gui-add for geometry-comparer result') as g_p:
                for i_src_geometry_path, i_tgt_geometry_path, i_check_statuses in comparer_results:
                    g_p.set_update()

                    i_check_statuses_list = i_check_statuses.split('+')
                    for j_check_status in i_check_statuses_list:
                        sector_chart_data_dict.setdefault(
                            j_check_status, []
                        ).append(
                            i_src_geometry_path
                        )
                    i_src_dcc_geometry = self._fnc_dcc_geometry_comparer.get_scene_dcc_geometry(i_src_geometry_path)
                    if i_src_dcc_geometry is None:
                        i_src_dcc_geometry = self._fnc_dcc_geometry_comparer.get_model_dcc_geometry(i_src_geometry_path)
                    #
                    if i_src_dcc_geometry.type_name in ['Mesh', 'mesh']:
                        i_src_mesh_item_prx = self._prx_usd_mesh_tree_view_add_opt.set_prx_item_add_as(
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
            utl_gui_configure.SectorChartMode.Error
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
            if step in ['mod', 'srf', 'rig', 'grm']:
                model_geometry_usd_hi_file_paths = rsv_operators.RsvAssetGeometryQuery(
                    self._task_properties
                ).get_usd_hi_file(
                    step='mod', task='modeling', version='all'
                )
                if model_geometry_usd_hi_file_paths:
                    _port = self._configure_gui.get_port('model_usd_file_path')
                    _port.set(model_geometry_usd_hi_file_paths)
                    _port.set(model_geometry_usd_hi_file_paths[-1])
                #
                model_look_ass_file_paths = rsv_operators.RsvAssetLookQuery(
                    self._task_properties
                ).get_ass_file(
                    step='mod', task='modeling', version='all'
                )
                if model_look_ass_file_paths:
                    _port = self._configure_gui.get_port('model_ass_file_path')
                    _port.set(model_look_ass_file_paths)
                    _port.set(model_look_ass_file_paths[-1])
                #
                surface_geometry_usd_hi_file_paths = rsv_operators.RsvAssetGeometryQuery(
                    self._task_properties
                ).get_usd_hi_file(
                    step='srf', task='surfacing', version='all'
                )
                if surface_geometry_usd_hi_file_paths:
                    _port = self._configure_gui.get_port('surface_usd_file_path')
                    _port.set(surface_geometry_usd_hi_file_paths)
                    _port.set(surface_geometry_usd_hi_file_paths[-1])
                #
                surface_look_ass_file_paths = rsv_operators.RsvAssetLookQuery(
                    self._task_properties
                ).get_ass_file(
                    step='srf', task='surfacing', version='all'
                )
                if surface_look_ass_file_paths:
                    _port = self._configure_gui.get_port('surface_ass_file_path')
                    _port.set(surface_look_ass_file_paths)
                    _port.set(surface_look_ass_file_paths[-1])
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
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
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
            with utl_core.GuiProgressesRunner.create(maximum=len(checked_src_geometries), label='import geometry') as g_p:
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
        self._set_obj_gui_refresh_()

    def _set_path_exchanged_repair_(self, i_tgt_mesh, i_tgt_data):
        pass

    def _set_checked_look_import_from_surface_(self):
        pass


class AbsDccComparerOpt(object):
    DCC_NAMESPACE = None
    DCC_NODE_CLS = None
    DCC_COMPONENT_CLS = None
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = None
    def __init__(self, filter_tree_view, result_tree_view):
        self._filter_tree_view = filter_tree_view
        self._result_tree_view = result_tree_view
        self._obj_add_dict = self._result_tree_view._item_dict

        self._result_tree_view.set_item_select_changed_connect_to(
            self.set_select
        )

        self._filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_view,
            prx_tree_view_tgt=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def set_restore(self):
        self._filter_tree_view.set_restore()
        self._result_tree_view.set_restore()
        self._filter_opt.set_restore()

    def get_node(self, path_src, path_tgt, status, description):
        if path_src in self._obj_add_dict:
            return self._obj_add_dict[path_src]
        #
        dcc_path_dag_opt_src = bsc_core.DccPathDagOpt(path_src)
        dcc_path_dag_opt_tgt = bsc_core.DccPathDagOpt(path_tgt)
        #
        dcc_obj_src = self.DCC_NODE_CLS(path_src)

        transform_path_opt_src = dcc_path_dag_opt_src.get_parent()
        transform_prx_item_src = self.get_transform(transform_path_opt_src)
        #
        prx_item_src = transform_prx_item_src.set_child_add(
            name=[dcc_obj_src.name, description, dcc_path_dag_opt_tgt.name],
            icon=utl_gui_core.RscIconFile.get('obj/mesh'),
            tool_tip=[path_src, description, path_tgt],
        )
        prx_item_src.set_status(
            status
        )
        self._obj_add_dict[path_src] = prx_item_src
        prx_item_src.set_gui_dcc_obj(
            dcc_obj_src, self.DCC_NAMESPACE
        )

        self._filter_opt.set_register(
            prx_item_src, [description]
        )
        return prx_item_src

    def get_root(self, path_dag_opt):
        path = path_dag_opt.path
        if path in self._obj_add_dict:
            return self._obj_add_dict[path]

        prx_item = self._result_tree_view.set_item_add(
            name=path_dag_opt.name,
            icon=utl_gui_core.RscIconFile.get('obj/transform'),
            tool_tip=path,
        )
        prx_item.set_expanded(True)
        self._obj_add_dict[path] = prx_item
        return prx_item

    def get_group(self, path_dag_opt):
        path = path_dag_opt.path
        if path in self._obj_add_dict:
            return self._obj_add_dict[path]

        parent_prx_item = self.get_root(path_dag_opt.get_root())

        prx_item = parent_prx_item.set_child_add(
            name=path_dag_opt.name,
            icon=utl_gui_core.RscIconFile.get('obj/transform'),
            tool_tip=path,
        )
        prx_item.set_expanded(True)
        self._obj_add_dict[path] = prx_item
        return prx_item

    def get_transform(self, path_dag_opt):
        path = path_dag_opt.path
        if path in self._obj_add_dict:
            return self._obj_add_dict[path]

        name = path_dag_opt.name

        parent_prx_item = self.get_group(path_dag_opt.get_parent())

        prx_item = parent_prx_item.set_child_add(
            name=name,
            icon=utl_gui_core.RscIconFile.get('obj/transform'),
            tool_tip=path,
        )
        prx_item.set_expanded(True)
        self._obj_add_dict[path] = prx_item
        return prx_item

    def set_select(self):
        pass

    def set_accept(self):
        pass


class AbsPnlGeometryComparer(prx_widgets.PrxSessionWindow):
    ERROR_STATUS = [
        utl_configure.DccMeshCheckStatus.DELETION,
        utl_configure.DccMeshCheckStatus.ADDITION,
        #
        utl_configure.DccMeshCheckStatus.NAME_CHANGED,
        utl_configure.DccMeshCheckStatus.PATH_CHANGED,
        utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
        #
        utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
    ]
    WARNING_STATUS = [
        utl_configure.DccMeshCheckStatus.POINTS_CHANGED,
    ]
    DCC_COMPARER_OPT_CLS = None

    def set_all_setup(self):
        s = prx_widgets.PrxScrollArea()
        self.set_widget_add(s)

        e_g = prx_widgets.PrxExpandedGroup()
        s.set_widget_add(e_g)
        e_g.set_name('viewers')
        e_g.set_expanded(True)

        h_s = prx_widgets.PrxHSplitter()
        e_g.set_widget_add(h_s)
        v_s = prx_widgets.PrxVSplitter()
        h_s.set_widget_add(v_s)
        self._filter_tree_view = prx_widgets.PrxTreeView()
        v_s.set_widget_add(self._filter_tree_view)
        self._filter_tree_view.set_header_view_create(
            [('name', 2), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 48
        )
        #
        self._sector_chart = prx_widgets.PrxSectorChart()
        v_s.set_widget_add(self._sector_chart)
        self._result_tree_view = prx_widgets.PrxTreeView()
        h_s.set_widget_add(self._result_tree_view)
        self._result_tree_view.set_header_view_create(
            [('name', 2), ('description', 1), ('target', 1)],
            self.get_definition_window_size()[0]*(2.0/3.0) - 48
        )
        #
        self._comparer_opt = self.DCC_COMPARER_OPT_CLS(
            self._filter_tree_view, self._result_tree_view
        )
        #
        self._options_prx_node = prx_widgets.PrxNode_('options')
        s.set_widget_add(self._options_prx_node)
        self._options_prx_node.set_ports_create_by_configure(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.set(
            'refresh', self.set_refresh_all
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )

        v_s.set_stretches([1, 2])
        h_s.set_stretches([1, 2])

        self._resolver = rsv_commands.get_resolver()
        self._rsv_project = self._resolver.get_rsv_project(
            project=self._session.option_opt.get('project')
        )
        self._rsv_asset = self._rsv_project.get_rsv_resource(
            asset=self._session.option_opt.get('asset')
        )

        self.__set_usd_source_file_refresh_()
        self.__set_usd_target_file_refresh_()

        self.set_refresh_all()

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlGeometryComparer, self).__init__(session, *args, **kwargs)

    def __set_usd_source_file_refresh_(self):
        step = self._session.option_opt.get('source_step')
        task = self._session.option_opt.get('source_task')

        keyword = 'asset-geometry-usd-var-file'
        rsv_task = self._rsv_asset.get_rsv_task(
            step=step, task=task
        )
        if rsv_task is not None:
            file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            file_paths = file_rsv_unit.get_result(
                version='all', extend_variants=dict(var='hi')
            )
            self._options_prx_node.set(
                'usd.source_file', file_paths
            )

    def __set_usd_target_file_refresh_(self):
        step = self._session.option_opt.get('step')
        task = self._session.option_opt.get('task')

        keyword = 'asset-geometry-usd-var-file'
        rsv_task = self._rsv_asset.get_rsv_task(
            step=step, task=task
        )
        if rsv_task is not None:
            file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            file_paths = file_rsv_unit.get_result(
                version='all', extend_variants=dict(var='hi')
            )
            self._options_prx_node.set(
                'usd.target_file', file_paths
            )

    def __gain_data_fnc_(self, file_path_src, file_path_tgt, location):
        import lxusd.fnc.comparers as usd_fnc_comparers

        self._comparer_results = usd_fnc_comparers.GeometryComparer(
            option=dict(
                file_src=file_path_src,
                file_tgt=file_path_tgt,
                #
                location=location
            )
        ).get_results()

    def __build_data_fnc_(self):
        sector_chart_data_dict = {}
        count = len(self._comparer_results)

        self._comparer_opt.set_restore()

        with utl_core.GuiProgressesRunner.create(maximum=count, label='gui-add for geometry-comparer result') as g_p:
            for i_path_src, i_path_tgt, i_description in self._comparer_results:
                i_keys = i_description.split('+')

                for j_key in i_keys:
                    sector_chart_data_dict.setdefault(
                        j_key, []
                    ).append(
                        i_path_src
                    )

                i_status = bsc_configure.ValidatorStatus.Correct
                for j_key in i_keys:
                    if j_key in self.ERROR_STATUS:
                        i_status = bsc_configure.ValidatorStatus.Error
                        break
                    elif j_key in self.WARNING_STATUS:
                        i_status = bsc_configure.ValidatorStatus.Warning
                        break

                self._comparer_opt.get_node(
                    i_path_src, i_path_tgt, i_status, i_description
                )
                #
                g_p.set_update()
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
            utl_gui_configure.SectorChartMode.Error
        )

        self._comparer_opt.set_accept()

    def set_refresh_all(self):
        file_path_src = self._options_prx_node.get('usd.source_file')
        if not file_path_src:
            return
        file_path_tgt = self._options_prx_node.get('usd.target_file')
        if not file_path_tgt:
            return

        location = '/master/hi'

        self._comparer_results = []

        ms = [
            # gain data
            (self.__gain_data_fnc_, (file_path_src, file_path_tgt, location)),
            # comparer
            (self.__build_data_fnc_, ())
        ]
        with utl_core.GuiProgressesRunner.create(maximum=len(ms), label='execute gui-build method') as g_p:
            for i_method, i_args in ms:
                g_p.set_update()
                i_method(*i_args)


