# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxbasic import bsc_configure, bsc_core

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui.panel import utl_gui_pnl_abstract, utl_gui_pnl_abs_utility

import lxutil_gui.proxy.widgets as prx_widgets

import lxutil_gui.qt.widgets as qt_widgets

import lxmaya.dcc.dcc_objects as mya_dcc_objects

from lxmaya.commands import _mya_cmd_utility

from lxutil_gui import utl_gui_core


class SceneImporterToolPanel(utl_gui_pnl_abstract.AbsUtilToolPanel):
    TOOL_PANEL_KEY = 'scene_importer'
    TOOL_SCHEME = utl_core.Scheme.MAYA_TOOL_TD
    def __init__(self, *args, **kwargs):
        super(SceneImporterToolPanel, self).__init__(*args, **kwargs)
        self.set_panel_build()

    def set_panel_build(self):
        # tool
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Gpu-import(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        #
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        self._qt_layout_0 = qt_widgets.QtGridLayout(qt_widget_0)
        self._set_tool_0_build_()

    def _set_tool_0_build_(self):
        def import_fnc_():
            transform_dcc_paths = mya_dcc_objects.Selection.get_selected_paths(include='transform')
            if transform_dcc_paths:
                p = self.set_progress_create(len(transform_dcc_paths))
                for transform_dcc_path in transform_dcc_paths:
                    p.set_update()
                    transform_dcc_obj = mya_dcc_objects.Transform(transform_dcc_path)
                    gpu_dcc_objs = [i for i in transform_dcc_obj.get_children() if i.type == 'gpuCache']
                    if gpu_dcc_objs:
                        gpu_dcc_obj = mya_dcc_objects.Shape(gpu_dcc_objs[-1].path)
                        plf_file_path = gpu_dcc_obj.get_port('cacheFileName').get()
                        if plf_file_path:
                            plf_file_obj = utl_dcc_objects.OsFile(plf_file_path)
                            if plf_file_obj.get_is_exists() is True:
                                mya_dcc_objects.Scene.set_file_import(plf_file_obj.path)
                                import_dcc_obj = mya_dcc_objects.Transform('import_gpu')
                                import_dcc_obj.set_create('transform')
                                new_obj = mya_dcc_objects.Node('|hi')
                                new_obj.set_parent_path(import_dcc_obj.path)
                                #
                                matrix = gpu_dcc_obj.transform.get_matrix()
                                import_dcc_obj.set_matrix(matrix)
                                #
                                gpu_dcc_obj.transform.set_visible(False)
                                import_dcc_obj.set_rename('import_gpu_0')
                p.set_stop()

        def reference_fnc_():
            gpu_paths = mya_dcc_objects.Selection.get_selected_paths(include='gpuCache')
            for transform_path in gpu_paths:
                print transform_path

        qt_button_0 = qt_widgets.QtPressButton()
        self._qt_layout_0.addWidget(qt_button_0, 0, 0, 1, 1)
        qt_button_0.setText('Import')
        qt_button_0.clicked.connect(import_fnc_)
        #
        # qt_button_1 = qt_widgets.QtPressButton()
        # self._qt_layout_0.addWidget(qt_button_1, 0, 1, 1, 1)
        # qt_button_1.setText('Reference')
        # qt_button_1.clicked.connect(reference_fnc_)


class SceneCleanerToolPanel(prx_widgets.PrxToolWindow):
    PANEL_KEY = 'scene_cleaner'
    def __init__(self, *args, **kwargs):
        super(SceneCleanerToolPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_gui_core.PanelsConfigure().get_window(
            self.PANEL_KEY
        )
        self.set_window_title(
            self._window_configure.get('name')
        )
        self.set_definition_window_size(
            self._window_configure.get('size')
        )
        self.set_panel_build()

    def set_panel_build(self):
        # tool
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Scene-cleaner(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        #
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        self._qt_layout_0 = qt_widgets.QtGridLayout(qt_widget_0)
        self._set_tool_0_build_()

    def _set_tool_0_build_(self):
        def set_unused_scripts_clear_fnc_():
            for i in cmds.scriptJob(listJobs=1):
                for k in ['leukocyte.antivirus()']:
                    if k in i:
                        utl_core.Log.set_result_trace(
                            'unused-script-job-remove: "{}"'.format(k)
                        )
                        index = i.split(': ')[0]
                        cmds.scriptJob(kill=int(index), force=1)
            #
            for i in cmds.ls(type='script'):
                if i in ['breed_gene', 'vaccine_gene']:
                    utl_core.Log.set_result_trace(
                        'unused-script-remove: "{}"'.format(i)
                    )
                    cmds.delete(i)
        #
        button_cfg_raw = [
            (
                'Unused-script(s) / script-job(s)',
                'python',
                (
                    u'delete unused-script/script-job(s)'
                ),
                set_unused_scripts_clear_fnc_, (0, 0, 1, 1)
            ),
            (
                'Unused-namespace(s)',
                'python',
                (
                    u'remove unused-namespace(s)\n'
                    u'1.not from reference/assembly-reference'
                ),
                _mya_cmd_utility.set_unused_namespaces_clear, (0, 1, 1, 1)
            ),
            (
                'Unknown-plug-in(s)',
                'python',
                (
                    u'delete unknown-plug-in(s)'
                ),
                mya_dcc_objects.Scene.set_unknown_plug_ins_clear, (1, 0, 1, 1)
            ),
            (
                'Unknown-node(s)',
                'python',
                (
                    u'delete unknown-node(s)'
                ),
                _mya_cmd_utility.set_unknown_nodes_clear, (1, 1, 1, 1)
            ),
            (
                'Unused-window(s)',
                'python',
                (
                    u'delete unused-window(s)'
                ),
                mya_dcc_objects.Scene.set_unused_windows_clear, (2, 0, 1, 1)
            ),
            (
                'Unloaded-reference(s)',
                'python',
                (
                    u'delete unloaded-reference(s)'
                ),
                _mya_cmd_utility.set_unload_references_clear, (2, 1, 1, 1)
            ),
        ]
        #
        for j in button_cfg_raw:
            label, icon, tool_tip, fnc, pos_args = j
            qt_button = prx_widgets.PrxPressItem()
            qt_button.set_check_enable(True)
            qt_button.set_name(label)
            qt_button.set_icon_name(icon)
            qt_button.set_tool_tip(tool_tip)
            self._qt_layout_0.addWidget(qt_button.widget, *pos_args)
            qt_button.set_press_clicked_connect_to(fnc)


class DatabaseGeometryManagerPanel(utl_gui_pnl_abs_utility.AbsDatabaseGeometryManagerPanel):
    def __init__(self, *args, **kwargs):
        super(DatabaseGeometryManagerPanel, self).__init__(*args, **kwargs)

    def _set_usd_file_export_(self):
        import lxmaya.dcc.dcc_objects as maya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        file_path = self._utility_node_prx.get_port('save_usd_file').get()
        if file_path:
            root = maya_dcc_objects.Selection.get_current()
            if root:
                mya_fnc_exporters.GeometryUsdExporter_(
                    file_path,
                    root=root,
                    option=dict(
                        default_prim_path=root,
                        with_uv=True,
                        with_mesh=True,
                        use_override=False
                    )
                ).set_run()

    def _set_usd_file_import_(self):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        file_path = self._utility_node_prx.get_port('open_usd_file').get()
        if file_path:
            mya_fnc_importers.GeometryUsdImporter_(
                file_path
            ).set_run()

    def _set_database_uv_map_export_(self):
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        force = self._database_export_node_prx.get_port('export_uv_map_force').get()
        mya_fnc_exporters.DatabaseGeometryExport(
            option=dict(force=force)
        ).set_run()

    def _set_database_uv_map_import_(self):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        mya_fnc_importers.DatabaseGeometryImporter().set_run()
    # geometry unify
    def _set_geometry_unify_run_(self):
        if self._geometry_unify_ddl_job_process is not None:
            if self._geometry_unify_ddl_job_process.get_is_stopped():
                self._set_geometry_unify_start_()
            else:
                if self._geometry_unify_ddl_job_process.get_is_completed():
                    self._set_geometry_unify_next_()
        else:
            self._set_geometry_unify_start_()

    def _set_geometry_unify_ddl_job_processing_(self, running_time_cost):
        if self._geometry_unify_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_unify')
            port.set_name(
                'Unify Geometry by Select(s) [ Running {} ]'.format(
                    bsc_core.IntegerMtd.second_to_time_prettify(running_time_cost)
                )
            )

    def _set_geometry_unify_ddl_job_status_changed_(self, status):
        if self._geometry_unify_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_unify')
            port.set_status(status)
            status = str(status).split('.')[-1]
            port.set_name(
                'Unify Geometry by Select(s) [ {} ]'.format(status)
            )
            mya_dcc_objects.Scene.set_message_show(
                'Unify Geometry by Select(s)',
                status
            )

    def _set_geometry_unify_start_(self):
        from lxbasic import bsc_core
        #
        from lxutil import utl_core
        #
        from lxdeadline import ddl_core
        #
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        import lxmaya.dcc.dcc_objects as maya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        root = maya_dcc_objects.Selection.get_current()
        if root:
            uuid = bsc_core.UuidMtd.get_new()
            #
            self._geometry_unify_file_path = '/l/resource/temporary/.lynxi/.cache/geometry-unify/{}.usd'.format(uuid)
            self._geometry_unify_output_file_path = '/l/resource/temporary/.lynxi/.cache/geometry-unify/{}.output.usd'.format(uuid)
            self._geometry_unify_time_tag = utl_core.System.get_time_tag()
            #
            mya_fnc_exporters.GeometryUsdExporter_(
                self._geometry_unify_file_path,
                root=root,
                option=dict(
                    default_prim_path=root,
                    with_uv=True,
                    with_mesh=True,
                    use_override=False
                )
            ).set_run()
            #
            method_query = ddl_objects.DdlMethodQuery(key='geometry-unify')

            method = ddl_methods.HookExecutor(
                method_option=method_query.get_method_option(),
                script_option=method_query.get_script_option(
                    file=self._geometry_unify_file_path
                )
            )
            #
            method.set_run_with_deadline()
            job_id = method.get_ddl_job_id()
            self._geometry_unify_ddl_job_process = ddl_objects.DdlJobProcess(job_id)
            if self._geometry_unify_ddl_job_process is not None:
                self._geometry_unify_ddl_job_process.processing.set_connect_to(
                    self._set_geometry_unify_ddl_job_processing_
                )
                self._geometry_unify_ddl_job_process.status_changed.set_connect_to(
                    self._set_geometry_unify_ddl_job_status_changed_
                )
                self._geometry_unify_ddl_job_process.set_start()
        else:
            utl_core.Log.set_module_warning_trace(
                'geometry unify',
                'please select a root'
            )

    def _set_geometry_unify_next_(self):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if bsc_core.StoragePathOpt(self._geometry_unify_output_file_path).get_is_exists() is True:
            mya_fnc_importers.GeometryUsdImporter_(
                self._geometry_unify_output_file_path,
                option=dict(
                    root_override='/geometry_unify/v_{}'.format(
                        self._geometry_unify_time_tag
                    )
                )
            ).set_run()
        else:
            utl_core.Log.set_module_warning_trace(
                'geometry unify',
                'file="{}" is non-exists'.format(self._geometry_unify_output_file_path)
            )
        #
        self._geometry_unify_ddl_job_process.set_stop()
    # geometry uv-map assign
    def _set_geometry_uv_map_assign_run_(self):
        if self._geometry_uv_assign_ddl_job_process is not None:
            if self._geometry_uv_assign_ddl_job_process.get_is_stopped():
                self._set_geometry_uv_map_assign_start_()
            else:
                if self._geometry_uv_assign_ddl_job_process.get_is_completed():
                    self._set_geometry_uv_map_assign_next_()
        else:
            self._set_geometry_uv_map_assign_start_()
    
    def _set_geometry_uv_map_assign_ddl_job_processing_(self, running_time_cost):
        if self._geometry_uv_assign_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_uv_map_assign')
            port.set_name(
                'Assign Geometry UV-map By Select(s) [ Running {} ]'.format(
                    bsc_core.IntegerMtd.second_to_time_prettify(running_time_cost)
                )
            )

    def _set_geometry_uv_map_assign_ddl_job_status_changed_(self, status):
        if self._geometry_uv_assign_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_uv_map_assign')
            port.set_status(status)
            status = str(status).split('.')[-1]
            port.set_name(
                'Assign Geometry UV-map By Select(s) [ {} ]'.format(status)
            )
            mya_dcc_objects.Scene.set_message_show(
                'Assign Geometry UV-map By Select(s)',
                status
            )

    def _set_geometry_uv_map_assign_start_(self):
        from lxbasic import bsc_core
        #
        from lxutil import utl_core
        #
        from lxdeadline import ddl_core
        #
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        import lxmaya.dcc.dcc_objects as maya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        root = maya_dcc_objects.Selection.get_current()
        if root:
            uuid = bsc_core.UuidMtd.get_new()
            #
            self._geometry_uv_map_assign_file_path = '/l/resource/temporary/.lynxi/.cache/geometry-uv-assign/{}.usd'.format(uuid)
            self._geometry_uv_map_assign_output_file_path = '/l/resource/temporary/.lynxi/.cache/geometry-uv-assign/{}.output.usd'.format(uuid)
            self._geometry_uv_map_assign_time_tag = utl_core.System.get_time_tag()
            #
            mya_fnc_exporters.GeometryUsdExporter_(
                self._geometry_uv_map_assign_file_path,
                root=root,
                option=dict(
                    default_prim_path=root,
                    with_uv=True,
                    with_mesh=True,
                    use_override=False
                )
            ).set_run()
            #

            method_query = ddl_objects.DdlMethodQuery(key='geometry-uv-assign')
            method = ddl_methods.HookExecutor(
                method_option=method_query.get_method_option(),
                script_option=method_query.get_script_option(
                    file=self._geometry_uv_map_assign_file_path
                )
            )
            #
            method.set_run_with_deadline()
            job_id = method.get_ddl_job_id()
            self._geometry_uv_assign_ddl_job_process = ddl_objects.DdlJobProcess(job_id)
            if self._geometry_uv_assign_ddl_job_process is not None:
                self._geometry_uv_assign_ddl_job_process.processing.set_connect_to(
                    self._set_geometry_uv_map_assign_ddl_job_processing_
                )
                self._geometry_uv_assign_ddl_job_process.status_changed.set_connect_to(
                    self._set_geometry_uv_map_assign_ddl_job_status_changed_
                )
                self._geometry_uv_assign_ddl_job_process.set_start()
        else:
            utl_core.Log.set_module_warning_trace(
                'geometry uv-map assign',
                'please select a root'
            )

    def _set_geometry_uv_map_assign_next_(self):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if bsc_core.StoragePathOpt(self._geometry_uv_map_assign_output_file_path).get_is_exists() is True:
            mya_fnc_importers.GeometryUsdImporter_(
                self._geometry_uv_map_assign_output_file_path,
                option=dict(
                    root_override='/geometry_uv_map_assign/v_{}'.format(
                        self._geometry_uv_map_assign_time_tag
                    )
                )
            ).set_run()
        else:
            utl_core.Log.set_module_warning_trace(
                'geometry uv-map assign',
                'file="{}" is non-exists'.format(self._geometry_uv_map_assign_output_file_path)
            )
        #
        self._geometry_uv_assign_ddl_job_process.set_stop()


class GeometryChecker(utl_gui_pnl_abs_utility.AbsGeometryCheckerPanel):
    def __init__(self, *args, **kwargs):
        super(GeometryChecker, self).__init__(*args, **kwargs)
