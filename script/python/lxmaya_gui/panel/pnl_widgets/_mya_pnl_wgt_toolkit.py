# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxutil_gui.panel import utl_gui_pnl_abs_toolkit

import lxresolver.commands as rsv_commands

import lxmaya.dcc.dcc_objects as mya_dcc_objects

from lxutil import utl_configure


def _set_texture_tx_load(window, item_prx):
    def set_processing_update(time_cost):
        c = 'Load Texture-tx(s) [ {} ] [ {} ]'.format(
            str(p_m.get_status()), bsc_core.RawIntegerMtd.second_to_time_prettify(time_cost)
        )
        item_prx.set_name(c)

    def set_status_changed_update(status):
        c = 'Load Texture-tx(s) [ {} ] [ {} ]'.format(
            str(status),
            bsc_core.RawIntegerMtd.second_to_time_prettify(p_m.get_running_time_cost())
        )
        item_prx.set_name(c)
        item_prx.set_status(status)

    def set_element_status_changed_update(element_statuses):
        item_prx.set_statuses(element_statuses)

    def set_logging_update(text):
        pass
    #
    import lxutil.dcc.dcc_operators as utl_dcc_operators
    # noinspection PyShadowingNames
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxbasic.objects as bsc_objects
    #
    result_dict = utl_dcc_operators.DccTexturesOpt(
        mya_dcc_objects.TextureReferences(
            option=dict(with_reference=True)
        )
    ).set_tx_create_and_repath_use_thread(use_deferred=True)
    p = result_dict['tx-create']
    p_m = bsc_objects.ProcessMonitor(p)
    p_m.logging.set_connect_to(set_logging_update)
    p_m.processing.set_connect_to(set_processing_update)
    p_m.status_changed.set_connect_to(set_status_changed_update)
    p_m.element_statuses_changed.set_connect_to(set_element_status_changed_update)
    p_m.set_start()
    p.set_start()
    window.set_window_close_connect_to(p_m.set_stop)


class UtilityToolkitPanel(utl_gui_pnl_abs_toolkit.AbsToolkitPanel):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file('maya/toolkit/utility')
    @utl_core.Modifier.exception_catch
    def __init__(self, *args, **kwargs):
        super(UtilityToolkitPanel, self).__init__(*args, **kwargs)
        self._toolkit_configure.set_flatten()
        self._set_build_by_configure_(self._toolkit_configure)
    @classmethod
    def set_texture_color_spaces_switch(cls):
        import lxutil.dcc.dcc_operators as utl_dcc_operators
        # noinspection PyShadowingNames
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        utl_dcc_operators.DccTexturesOpt(
            mya_dcc_objects.TextureReferences(
                option=dict(with_reference=True)
            )
        ).set_color_space_auto_switch()
    @classmethod
    def set_texture_tiles_preview_generate(cls):
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds
        # noinspection PyUnresolvedReferences
        import maya.mel as mel
        fs = cmds.ls(type='file')
        if fs:
            ps = utl_core.Progress.set_create(len(fs))
            for f in fs:
                utl_core.Progress.set_update(ps)
                mel.eval('generateUvTilePreview {}'.format(f))
            #
            utl_core.Progress.set_stop(ps)

    def set_texture_tx_load(self, item_prx):
        _set_texture_tx_load(self, item_prx)


class SceneCleanerPanel(utl_gui_pnl_abs_toolkit.AbsToolkitPanel):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file('maya/toolkit/scene-cleaner')
    HELP_FILE_PATH = utl_configure.MainData.get_help_file('maya/toolkit/scene-cleaner')
    @utl_core.Modifier.exception_catch
    def __init__(self, *args, **kwargs):
        super(SceneCleanerPanel, self).__init__(*args, **kwargs)
        self._toolkit_configure.set_flatten()
        self._set_build_by_configure_(self._toolkit_configure)
    #
    def set_all_run(self, *args, **kwargs):
        item_prx = args[0]
        sub_item_prxes = self.get_item_prxes()
        item_prx.widget._set_progress_maximum_(len(sub_item_prxes))
        for i in sub_item_prxes:
            item_prx.widget._set_progress_update_()
            #
            if i.get_is_checked() is True:
                i.set_click()
        #
        item_prx.widget._stop_progress_()
    @classmethod
    def set_unused_scripts_clear(cls):
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds
        #
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


class AssetToolkitPanel(utl_gui_pnl_abs_toolkit.AbsToolkitPanel):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file('maya/toolkit/asset')
    HELP_FILE_PATH = utl_configure.MainData.get_help_file('maya/toolkit/asset')
    @utl_core.Modifier.exception_catch
    def __init__(self, *args, **kwargs):
        super(AssetToolkitPanel, self).__init__(*args, **kwargs)
        #
        self._resolver = rsv_commands.get_resolver()
        work_source_file_path = mya_dcc_objects.Scene.get_current_file_path()
        self._task_properties = self._resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)
        if self._task_properties is not None:
            self._toolkit_configure.set_flatten()
            self._set_build_by_configure_(self._toolkit_configure)

    def set_model_scene_import(self):
        import lxmaya_fnc.scripts as mya_fn_scripts
        #
        mya_fn_scripts.set_asset_model_scene_import(self._task_properties)

    def set_model_geometry_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_model_geometry=True,
                with_surface_geometry_uv_map=True,
            )
        ).set_run()

    def set_surface_geometry_uv_map_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_surface_geometry_uv_map=True,
            )
        ).set_run()

    def set_work_surface_geometry_uv_map_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_surface_work_geometry_uv_map=True,
            )
        ).set_run()

    def set_groom_geometry_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_groom_geometry=True, with_groom_grow_geometry=True,
            )
        ).set_run()

    def set_asset_look_ass_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_surface_look=True,
            )
        ).set_run()

    def set_asset_work_look_preview_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_work_surface_look_preview=True,
            )
        ).set_run()

    def set_asset_look_preview_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_surface_look_preview=True,
            )
        ).set_run()

    def set_texture_tx_load(self, item_prx):
        _set_texture_tx_load(self, item_prx)
    # light
    @classmethod
    def set_light_rig_import(cls):
        mya_dcc_objects.Scene.set_file_reference(
            '/l/resource/srf/std_lgt_rig/maya_rig/srf_light_rig.ma'
        )


class SurfaceToolkitPanel(utl_gui_pnl_abs_toolkit.AbsToolkitPanel):
    CONFIGURE_FILE_PATH = utl_configure.MayaToolkitData.get('asset-surface')
    @utl_core.Modifier.exception_catch
    def __init__(self, *args, **kwargs):
        super(SurfaceToolkitPanel, self).__init__(*args, **kwargs)
        #
        self._resolver = rsv_commands.get_resolver()
        work_source_file_path = mya_dcc_objects.Scene.get_current_file_path()
        self._task_properties = self._resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)
        if self._task_properties is not None:
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

    def set_katana_scene_src_create(self):
        pass
    # geometry
    def set_work_surface_geometry_uv_map_export(self):
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        rsv_task = self._resolver.get_rsv_task(
            **self._task_properties.value
        )
        version = 'new'
        root = '/master'
        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_root.get_is_exists() is True:
            keyword = 'asset-source-geometry-usd-var-file'
            location_names = ['hi', 'shape']
            with utl_core.GuiProgressesRunner.create(maximum=len(location_names), label='export geometry uv-map in location') as g_p:
                for i_location_name in location_names:
                    g_p.set_update()
                    #
                    i_geometry_usd_var_file_rsv_unit = rsv_task.get_rsv_unit(
                        keyword=keyword
                    )
                    i_geometry_usd_var_file_path = i_geometry_usd_var_file_rsv_unit.get_result(
                        version=version,
                        extend_variants=dict(var=i_location_name)
                    )
                    #
                    i_location = '{}/{}'.format(root, i_location_name)
                    i_sub_root_dag_path = bsc_core.DccPathDagOpt(i_location)
                    i_mya_sub_root_dag_path = i_sub_root_dag_path.set_translate_to(
                        pathsep='|'
                    )
                    #
                    sub_root_mya_obj = mya_dcc_objects.Group(i_mya_sub_root_dag_path.path)
                    if sub_root_mya_obj.get_is_exists() is True:
                        mya_fnc_exporters.GeometryUsdExporter_(
                            file_path=i_geometry_usd_var_file_path,
                            root=i_location,
                            option=dict(
                                default_prim_path=root,
                                with_uv=True,
                                with_mesh=True,
                                use_override=False
                            )
                        ).set_run()

    def set_work_surface_geometry_uv_map_import(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        project = self._task_properties.get('project')
        asset = self._task_properties.get('asset')
        #
        mya_fnc_builders.AssetBuilder(
            option=dict(
                project=project,
                asset=asset,
                with_surface_work_geometry_uv_map=True,
            )
        ).set_run()

    def set_geometry_update(self, *args, **kwargs):
        def run_continue_fnc_(methods_):
            _gp = utl_core.GuiProgressesRunner(maximum=len(methods_))
            for _method in methods_:
                _gp.set_update()
                _method._set_export_debug_run_()
            _gp.set_stop()
        #
        def run_fnc_():
            work_task_properties.set('task', 'surfacing')
            work_task_properties.set('option.version', version)
            methods_loader = utl_fnc_objects.TaskMethodsLoader(work_task_properties)
            method_paths = ['/methods/asset_scene', '/methods/asset_surface_geometry']
            gp = utl_core.GuiProgressesRunner(maximum=len(method_paths))
            sorted_method_paths = methods_loader.get_sorted_objs(method_paths)
            methods = []
            check_results = []
            check_descriptions = []
            for method_path in sorted_method_paths:
                gp.set_update()
                method = methods_loader.get_method(method_path)
                methods.append(method)
                method.set_check_rest()
                method._set_check_debug_run_()
                method.set_check_result_update(work_task_properties)
                check_passed = method.get_is_check_passed()
                if check_passed is True:
                    pass
                else:
                    check_descriptions.append(method.get_obj_descriptions())
                #
                check_results.append(check_passed)
            #
            gp.set_stop()
            #
            if check_results == [True, True]:
                gp = utl_core.GuiProgressesRunner(maximum=len(method_paths))
                for method in methods:
                    gp.set_update()
                    method._set_export_debug_run_()
                gp.set_stop()
            else:
                utl_core.DialogWindow.set_create(
                    label='Geometry-update',
                    content='you scene has some error, press "Yes" to continue\n{}'.format(
                        u'\n'.join(check_descriptions)
                    ),
                    yes_method=lambda *_args, **_kwargs: run_continue_fnc_(methods)
                )
        #
        from lxutil import utl_core
        #
        import lxutil_fnc.objects as utl_fnc_objects
        #
        work_task_properties = self._task_properties
        rsv_task = self._resolver.get_rsv_task(
            **work_task_properties.value
        )
        rsv_unit = rsv_task.get_rsv_unit(keyword='asset-release-version-dir')
        scheme = kwargs['scheme']
        if scheme == 'latest':
            version = rsv_unit.get_latest_version()
        elif scheme == 'new':
            version = rsv_unit.get_new_version()
        else:
            raise TypeError()
        #
        if version:
            run_fnc_()
    #
    def get_geometry_update_schemes(self, *args, **kwargs):
        return ['latest', 'new']
    # texture
    def set_texture_tx_load(self, item_prx):
        _set_texture_tx_load(self, item_prx)
    # look
    def set_work_look_ass_export(self):
        import lxmaya_fnc.scripts as mya_fnc_scripts
        task_properties = self._task_properties
        mya_fnc_scripts.set_asset_look_ass_export(task_properties, force=True)

    def set_work_look_yml_export(self):
        import lxmaya_fnc.scripts as mya_fnc_scripts
        task_properties = self._task_properties
        mya_fnc_scripts.set_asset_look_preview_yml_export(task_properties)
    # light
    @classmethod
    def set_light_rig_import(cls):
        mya_dcc_objects.Scene.set_file_reference(
            '/l/resource/srf/std_lgt_rig/maya_rig/srf_light_rig.ma'
        )
    @classmethod
    def set_asset_comparer_panel_open(cls):
        from lxmaya_gui.panel import pnl_widgets
        w = pnl_widgets.PnlAssetGeometryComparer()
        w.set_window_show()
    @classmethod
    def set_method_runner_panel_open(cls):
        from lxmaya_gui.panel import pnl_widgets
        w = pnl_widgets.SceneMethodRunnerPanel()
        w.set_window_show()
    @classmethod
    def set_scene_packager_panel_open(cls):
        from lxmaya_gui.panel import pnl_widgets
        w = pnl_widgets.ScenePackagerToolPanel()
        w.set_window_show()

    def set_groom_geometry_xgen_import(self):
        pass

    def get_work_look_ass_files(self, **kwargs):
        import lxresolver.operators as rsv_operators
        #
        task_properties = self._task_properties
        return rsv_operators.RsvAssetLookQuery(task_properties).get_ass_work_file(version='all') or []

    def get_look_passes(self, **kwargs):
        return ['default']

    def set_work_look_ass_import(self, **kwargs):
        from lxutil import utl_core
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        look_pass = kwargs['look_pass']
        work_look_ass_file_path = kwargs['look_ass_file']
        #
        work_look_ass_file_obj = utl_dcc_objects.OsFile(work_look_ass_file_path)
        if work_look_ass_file_obj.get_is_exists() is True:
            mya_fnc_importers.LookAssImporter(
                option=dict(
                    file=work_look_ass_file_path,
                    location='/master',
                    look_pass=look_pass,
                    name_join_time_tag=True,
                )
            ).set_run()
        else:
            utl_core.Log.set_module_warning_trace(
                'work-look-ass-import',
                u'file="{}" is non-exists'.format(work_look_ass_file_path)
            )