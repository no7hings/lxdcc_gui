# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil_gui.panel import utl_gui_pnl_abs_utility

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class PnlHashGeometry(utl_gui_pnl_abs_utility.AbsPnlHashGeometry):
    def __init__(self, session, *args, **kwargs):
        super(PnlHashGeometry, self).__init__(session, *args, **kwargs)

    def _set_usd_file_export_(self):
        import lxmaya.dcc.dcc_objects as maya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        file_path = self._utility_node_prx.get_port('save_usd_file').get()
        if file_path:
            root = maya_dcc_objects.Selection.get_current()
            if root:
                mya_fnc_exporters.FncGeometryUsdExporter(
                    option=dict(
                        file=file_path,
                        location=root,
                        #
                        default_prim_path=root,
                        with_mesh_uv=True,
                        with_mesh=True,
                        use_override=False,
                        port_match_patterns=['pg_*']
                    )
                ).execute()

    def _set_usd_file_import_(self):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        file_path = self._utility_node_prx.get_port('open_usd_file').get()
        if file_path:
            mya_fnc_importers.FncGeometryUsdImporter(
                option=dict(
                    file=file_path
                )
            ).execute()

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
                    bsc_core.RawIntegerMtd.second_to_time_prettify(running_time_cost)
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
            mya_fnc_exporters.FncGeometryUsdExporter(
                option=dict(
                    file=self._geometry_unify_file_path,
                    location=root,
                    #
                    default_prim_path=root,
                    with_mesh_uv=True,
                    with_mesh=True,
                    use_override=False
                )
            ).execute()
            #
            method_query = ddl_objects.DdlMethodQuery(key='geometry-unify')

            method = ddl_methods.HookExecutor(
                method_option=method_query.get_method_option(),
                script_option=method_query.get_script_option(
                    file=self._geometry_unify_file_path
                )
            )
            #
            method.execute_with_deadline()
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
        if bsc_core.StgPathOpt(self._geometry_unify_output_file_path).get_is_exists() is True:
            mya_fnc_importers.FncGeometryUsdImporter(
                option=dict(
                    file=self._geometry_unify_output_file_path,
                    root_override='/geometry_unify/v_{}'.format(
                        self._geometry_unify_time_tag
                    )
                )
            ).execute()
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
                    bsc_core.RawIntegerMtd.second_to_time_prettify(running_time_cost)
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
            mya_fnc_exporters.FncGeometryUsdExporter(
                option=dict(
                    file=self._geometry_uv_map_assign_file_path,
                    location=root,
                    #
                    default_prim_path=root,
                    with_mesh_uv=True,
                    with_mesh=True,
                    use_override=False
                )
            ).execute()
            #

            method_query = ddl_objects.DdlMethodQuery(key='geometry-uv-assign')
            method = ddl_methods.HookExecutor(
                method_option=method_query.get_method_option(),
                script_option=method_query.get_script_option(
                    file=self._geometry_uv_map_assign_file_path
                )
            )
            #
            method.execute_with_deadline()
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
        if bsc_core.StgPathOpt(self._geometry_uv_map_assign_output_file_path).get_is_exists() is True:
            mya_fnc_importers.FncGeometryUsdImporter(
                option=dict(
                    file=self._geometry_uv_map_assign_output_file_path,
                    root_override='/geometry_uv_map_assign/v_{}'.format(
                        self._geometry_uv_map_assign_time_tag
                    )
                )
            ).execute()
        else:
            utl_core.Log.set_module_warning_trace(
                'geometry uv-map assign',
                'file="{}" is non-exists'.format(self._geometry_uv_map_assign_output_file_path)
            )
        #
        self._geometry_uv_assign_ddl_job_process.set_stop()
