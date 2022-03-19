# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core, utl_configure

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.panel import utl_gui_pnl_abs_toolkit


import lxresolver.commands as rsv_commands

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


def _set_texture_tx_load(window, item_prx):
    def set_processing_update(time_cost):
        c = 'Load Texture-tx(s) [ {} ] [ {} ]'.format(
            str(p_m.get_status()),
            bsc_core.IntegerMtd.second_to_time_prettify(time_cost)
        )
        item_prx.set_name(c)

    def set_status_changed_update(status):
        c = 'Load Texture-tx(s) [ {} ] [ {} ]'.format(
            str(status),
            bsc_core.IntegerMtd.second_to_time_prettify(p_m.get_running_time_cost())
        )
        item_prx.set_name(c)
        item_prx.set_status(status)

    def set_element_status_changed_update(element_statuses):
        item_prx.set_element_statuses(element_statuses)

    def set_logging_update(text):
        pass
    #
    import lxutil.dcc.dcc_operators as utl_dcc_operators
    #
    import lxbasic.objects as bsc_objects
    #
    result_dict = utl_dcc_operators.DccTexturesOpt(
        ktn_dcc_objects.TextureReferences(
            option=dict(
                with_reference=False
            )
        )
    ).set_tx_create_and_repath(use_deferred=True)
    p = result_dict['tx-create']
    p_m = bsc_objects.ProcessMonitor(p)
    p_m.logging.set_connect_to(set_logging_update)
    p_m.processing.set_connect_to(set_processing_update)
    p_m.status_changed.set_connect_to(set_status_changed_update)
    p_m.element_statuses_changed.set_connect_to(set_element_status_changed_update)
    p_m.set_start()
    p.set_start()
    window.set_window_close_connect_to(p_m.set_stop)


class SurfaceToolkitPanel(utl_gui_pnl_abs_toolkit.AbsToolkitPanel):
    CONFIGURE_FILE_PATH = utl_configure.KatanaToolkitData.get('asset-surface')
    def __init__(self, *args, **kwargs):
        super(SurfaceToolkitPanel, self).__init__(*args, **kwargs)
        #
        self._resolver = rsv_commands.get_resolver()
        work_source_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        self._task_properties = self._resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)
        if self._task_properties is not None:
            self._toolkit_configure.set('properties.task', self._task_properties.get('task'))
            self._toolkit_configure.set_flatten()
            self._set_build_by_configure_(self._toolkit_configure)
    # scene
    def set_system_workspace_create(self):
        import lxutil_fnc.commands as utl_fnc_commands
        task_properties = self._task_properties
        utl_fnc_commands.set_surface_system_workspace_create(task_properties)

    def set_system_workspace_open(self):
        import lxutil_fnc.commands as utl_fnc_commands
        task_properties = self._task_properties
        utl_fnc_commands.set_surface_system_workspace_open(task_properties)
    @classmethod
    def set_dcc_workspace_create(cls):
        import lxkatana.fnc.creators as ktn_fnc_creators
        ktn_fnc_creators.LookWorkspaceCreator().set_run()

    def set_work_set_usd_import(self):
        pass

    def set_set_usd_import(self):
        pass
    # look
    def set_material_create(self):
        pass
    @classmethod
    def set_look_pass_add(cls, **kwargs):
        import lxkatana.fnc.builders as ktn_fnc_builders
        #
        look_pass_name = kwargs['look_pass']
        ktn_fnc_builders.AssetWorkspaceBuilder().set_look_pass_add(look_pass_name)

    def set_work_look_ass_export(self):
        import lxkatana_fnc.scripts as ktn_fnc_scripts
        task_properties = self._task_properties
        ktn_fnc_scripts.set_asset_work_look_ass_export(task_properties, force=True)

    def set_work_look_ass_import(self, **kwargs):
        def pst_method_fnc_():
            ktn_fnc_importers.LookAssImporter._set_pst_run_()
            timer.stop()
        #
        from lxutil import utl_core
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxkatana.fnc.importers as ktn_fnc_importers
        #
        look_pass_name = kwargs['look_pass']
        work_look_ass_file_path = kwargs['look_ass_file']
        #
        work_look_ass_file_obj = utl_dcc_objects.OsFile(work_look_ass_file_path)
        if work_look_ass_file_obj.get_is_exists() is True:
            ktn_fnc_importers.LookAssImporter(
                file_path=work_look_ass_file_path,
                root='/root/materials',
                option=dict(
                    look_pass=look_pass_name
                )
            ).set_run()
            #
            timer = self._set_timer_method_start_(
                time=1000, method=pst_method_fnc_
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'work-look-ass-import',
                u'file="{}" is non-exists'.format(work_look_ass_file_path)
            )
    @classmethod
    def get_look_passes(cls, **kwargs):
        import lxkatana.fnc.builders as ktn_fnc_builders
        #
        return ktn_fnc_builders.AssetWorkspaceBuilder().get_look_pass_names()

    def get_work_look_ass_files(self, **kwargs):
        import lxresolver.operators as rsv_operators
        #
        task_properties = self._task_properties
        return rsv_operators.RsvAssetLookQuery(task_properties).get_ass_work_file(version='all') or []
    #
    def _set_timer_method_start_(self, time, method):
        timer = utl_gui_qt_core.QtCore.QTimer(self.widget)
        timer.start(time)
        timer.timeout.connect(method)
        return timer

    def set_standard_surface_user_data_create(self, **kwargs):
        # noinspection PyShadowingNames
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        ss = ktn_dcc_objects.AndShaders().get_standard_surfaces()
        #
        data_type_name = kwargs['data_type']
        port_name = kwargs['port']
        attribute_name = kwargs['attribute']
        default_value = kwargs['default_value']
        #
        if ss:
            gp = utl_core.GuiProgressesRunner(maximum=len(ss))
            for i in ss:
                gp.set_update()
                #
                s = ktn_dcc_objects.AndStandardSurface(i.path)
                s.set_port_user_data_create(data_type_name, port_name, attribute_name, default_value)
            #
            gp.set_stop()

    def set_look_update(self, **kwargs):
        def yes_fnc_():
            import lxkatana.fnc.exporters as ktn_fnc_exporters
            #
            from lxdeadline import ddl_core
            #
            import lxdeadline.objects as ddl_objects
            #
            import lxdeadline.methods as ddl_methods
            #
            katana_scene_src_file_path = kwargs['scene_src_file']
            #
            rsv_task_properties = self._task_properties
            #
            user = utl_core.System.get_user_name()
            time_tag = utl_core.System.get_time_tag()
            #
            ktn_fnc_exporters.SceneExporter(
                file_path=katana_scene_src_file_path
            ).set_run()
            #
            katana_look_export_query = ddl_objects.DdlRsvTaskQuery(
                'katana-look-export', rsv_task_properties
            )
            katana_look_export = ddl_methods.RsvTaskHookExecutor(
                method_option=katana_look_export_query.get_method_option(),
                script_option=katana_look_export_query.get_script_option(
                    file=katana_scene_src_file_path,
                    with_look_ass=True,
                    with_look_klf=True,
                    with_texture_tx=True,
                    force=True,
                    #
                    user=user, time_tag=time_tag
                )
            )
            katana_look_export.set_run_with_deadline()
        #
        utl_core.DialogWindow.set_create(
            label='Look-update',
            content='press "yes" to update look-data to latest version.',
            yes_method=yes_fnc_
        )

    def get_project(self, **kwargs):
        work_task_properties = self._task_properties
        return work_task_properties.get('project')

    def get_scene_src_files(self, **kwargs):
        import lxresolver.operators as rsv_operators
        work_task_properties = self._task_properties
        return rsv_operators.RsvAssetSceneQuery(work_task_properties).get_katana_src_file(version='all') or []
    # texture
    def set_texture_tx_load(self, item_prx):
        _set_texture_tx_load(self, item_prx)

    def set_light_rig_import(self):
        from lxkatana import commands
        task_properties = self._task_properties
        commands.set_surface_light_rig_update_(task_properties)
    @classmethod
    def set_method_runner_panel_open(cls):
        from lxkatana_gui.panel import pnl_widgets
        w = pnl_widgets.SceneMethodRunnerPanel()
        w.set_window_show()
    @classmethod
    def set_scene_packager_panel_open(cls):
        from lxkatana_gui.panel import pnl_widgets
        w = pnl_widgets.ScenePackagerPanel()
        w.set_window_show()
    @classmethod
    def set_scene_shader_viewer_panel_open(cls):
        import lxkatana_gui.panel.pnl_widgets as ktn_pnl_widgets
        w = ktn_pnl_widgets.SceneShaderViewerPanel()
        w.set_window_show()


class UtilityToolkitPanel(utl_gui_pnl_abs_toolkit.AbsToolkitPanel):
    CONFIGURE_FILE_PATH = utl_configure.KatanaToolkitData.get('utility')
    def __init__(self, *args, **kwargs):
        super(UtilityToolkitPanel, self).__init__(*args, **kwargs)
        self._toolkit_configure.set_flatten()
        self._set_build_by_configure_(self._toolkit_configure)
    @classmethod
    def set_dcc_workspace_create(cls):
        import lxkatana.fnc.creators as ktn_fnc_creators
        ktn_fnc_creators.LookWorkspaceCreator().set_run()

    def set_texture_tx_load(self, item_prx):
        _set_texture_tx_load(self, item_prx)
