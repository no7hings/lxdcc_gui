# coding:utf-8
import collections

from lxbasic import bsc_configure, bsc_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core, utl_process

import lxutil.extra.methods as utl_etr_methods

import lxutil.scripts as utl_scripts

from lxutil_gui.qt import utl_gui_qt_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil_gui.proxy.operators as utl_prx_operators

from lxsession import ssn_core

import lxsession.commands as ssn_commands

import lxresolver.commands as rsv_commands

from lxutil_gui import utl_gui_core


class AbsValidatorOpt(object):
    DCC_NAMESPACE = None
    DCC_NODE_CLS = None
    DCC_COMPONENT_CLS = None
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = None
    def __init__(self, filter_tree_view, result_tree_view):
        self._filter_tree_view = filter_tree_view
        self._result_tree_view = result_tree_view
        self._obj_add_dict = self._result_tree_view._item_dict

        self._result_tree_view.connect_item_select_changed_to(
            self.set_select
        )

        self._filter_opt = utl_prx_operators.GuiTagFilterOpt(
            prx_tree_view_src=self._filter_tree_view,
            prx_tree_view_tgt=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def set_select(self):
        utl_prx_operators.PrxDccObjTreeViewSelectionOpt.select_fnc(
            prx_tree_view=self._result_tree_view,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )

    def set_results_at(self, rsv_scene_properties, results):
        file_path = rsv_scene_properties.get('extra.file')
        check_results = results['check_results']
        scene_prx_item = self._get_scene_(file_path)
        scene_prx_item.clear_children()
        self._filter_opt.restore_all()
        scene_prx_item._child_dict = {}
        if not check_results:
            scene_prx_item.set_status(
                bsc_configure.ValidatorStatus.Correct
            )
            return True
        #
        self._set_sub_check_results_build_at_(
            scene_prx_item, rsv_scene_properties, check_results
        )
        #
        self._result_tree_view.expand_items_by_depth(1)

    def _set_sub_check_results_build_at_(self, scene_prx_item, rsv_scene_properties, results):
        with utl_core.GuiProgressesRunner.create(maximum=len(results), label='gui-add for check result') as g_p:
            for i_result in results:
                g_p.set_update()
                #
                i_type = i_result['type']
                i_dcc_path = i_result['node']
                i_group_name = i_result['group']
                i_status = i_result['status']
                if i_status == 'warning':
                    i_validation_status = bsc_configure.ValidatorStatus.Warning
                elif i_status == 'error':
                    i_validation_status = bsc_configure.ValidatorStatus.Error
                else:
                    raise RuntimeError()

                i_description = i_result['description']
                #
                self._set_status_update_(scene_prx_item, i_status, i_validation_status)
                #
                i_group_prx_item = self._get_group_(scene_prx_item, i_group_name)
                self._set_status_update_(i_group_prx_item, i_status, i_validation_status)
                i_node_prx_item = self._get_node_(
                    scene_prx_item,
                    rsv_scene_properties,
                    i_group_prx_item,
                    i_dcc_path,
                    i_description,
                    i_validation_status
                )

                i_filter_key = '.'.join(
                    [
                        bsc_core.SPathMtd.set_quote_to(i_group_name),
                        bsc_core.SPathMtd.set_quote_to(i_description)
                    ]
                )

                self._filter_opt.set_register(
                    i_node_prx_item, [i_filter_key]
                )
                if i_type == 'file':
                    j_elements = i_result['elements']
                    for j_file_path in j_elements:
                        j_file_prx_item = self._get_file_(
                            scene_prx_item, i_node_prx_item,
                            j_file_path, i_description, i_validation_status
                        )
                        self._filter_opt.set_register(
                            j_file_prx_item, [i_filter_key]
                        )
                elif i_type == 'directory':
                    j_elements = i_result['elements']
                    for j_directory_path in j_elements:
                        j_file_prx_item = self._get_directory_(
                            scene_prx_item, i_node_prx_item,
                            j_directory_path, i_description, i_validation_status
                        )
                        self._filter_opt.set_register(
                            j_file_prx_item, [i_filter_key]
                        )
                elif i_type == 'component':
                    j_elements = i_result['elements']
                    for j_dcc_path in j_elements:
                        j_comp_prx_item = self._get_component_(
                            scene_prx_item, i_node_prx_item,
                            j_dcc_path, i_description, i_validation_status
                        )
                        self._filter_opt.set_register(
                            j_comp_prx_item, [i_filter_key]
                        )

    def _set_status_update_(self, prx_item, status, validation_status):
        name = prx_item._validation_name
        result = prx_item._validation_result
        #
        pre_validation_status = prx_item.get_status()
        if validation_status > pre_validation_status:
            prx_item.set_status(validation_status)

        if status in result:
            count = result[status]
        else:
            count = 0
            result[status] = 0

        count += 1

        result[status] = count
        #
        d = ' '.join(['[ {} x {} ]'.format(k, v) for k, v in result.items() if v])
        #
        prx_item.set_name(
            '{} {}'.format(name, d)
        )

    def _get_scene_(self, file_path):
        if file_path in self._obj_add_dict:
            return self._obj_add_dict[file_path]
        #
        stg_file = utl_dcc_objects.OsFile(file_path)
        name = stg_file.get_path_prettify_()
        prx_item = self._result_tree_view.set_item_add(
            name=name,
            icon=stg_file.icon,
            tool_tip=file_path,
        )
        prx_item.set_expanded(True)
        prx_item.set_checked(False)

        prx_item._validation_name = name
        prx_item._validation_result = collections.OrderedDict(
            [
                ('error', 0),
                ('warning', 0)
            ]
        )

        prx_item._child_dict = {}
        self._obj_add_dict[file_path] = prx_item
        return prx_item

    def _get_group_(self, scene_prx_item, group_name):
        if group_name in scene_prx_item._child_dict:
            prx_item = scene_prx_item._child_dict[group_name]
            return prx_item

        prx_item = scene_prx_item.add_child(
            name=group_name,
            icon=utl_gui_core.RscIconFile.get('application/python'),
        )
        prx_item.set_checked(False)
        #
        prx_item._validation_name = group_name
        prx_item._validation_result = collections.OrderedDict(
            [
                ('error', 0),
                ('warning', 0)
            ]
        )
        #
        scene_prx_item._child_dict[group_name] = prx_item
        return prx_item

    def _get_node_(self, scene_prx_item, rsv_scene_properties, group_prx_item, dcc_path, description, status):
        dcc_path_dag_opt = bsc_core.DccPathDagOpt(dcc_path)
        pathsep = dcc_path_dag_opt.get_pathsep()
        pathsep_src = rsv_scene_properties.get('dcc.pathsep')
        if pathsep == pathsep_src:
            if pathsep != self.DCC_PATHSEP:
                dcc_path = dcc_path_dag_opt.translate_to(self.DCC_PATHSEP).to_string()
        #
        dcc_obj = self.DCC_NODE_CLS(dcc_path)
        prx_item = group_prx_item.add_child(
            name=[dcc_obj.name, description],
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path,
        )
        prx_item.set_checked(False)
        prx_item.set_status(status)
        prx_item.set_gui_dcc_obj(
            dcc_obj, self.DCC_NAMESPACE
        )
        return prx_item

    def _get_component_(self, scene_prx_item, node_prx_item, dcc_path, description, status):
        dcc_path_dag_opt = bsc_core.DccPathDagOpt(dcc_path)
        pathsep = dcc_path_dag_opt.get_pathsep()
        if pathsep != self.DCC_PATHSEP:
            dcc_path = dcc_path_dag_opt.translate_to(self.DCC_PATHSEP).to_string()
        #
        dcc_obj = self.DCC_COMPONENT_CLS(dcc_path)
        prx_item = node_prx_item.add_child(
            name=[dcc_obj.name, description],
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path,
        )
        prx_item.set_checked(False)
        prx_item.set_status(status)
        prx_item.set_gui_dcc_obj(
            dcc_obj, self.DCC_NAMESPACE
        )
        return prx_item

    def _get_file_(self, scene_prx_item, node_prx_item, file_path, description, status):
        stg_file = utl_dcc_objects.OsFile(file_path)
        prx_item = node_prx_item.add_child(
            name=[stg_file.get_path_prettify_(maximum=32), description],
            icon=stg_file.icon,
            menu=stg_file.get_gui_menu_raw(),
            tool_tip=stg_file.path
        )
        prx_item.set_status(status)
        prx_item.set_checked(False)
        return prx_item

    def _get_directory_(self, scene_prx_item, node_prx_item, directory_path, description, status):
        stg_directory = utl_dcc_objects.OsDirectory_(directory_path)
        prx_item = node_prx_item.add_child(
            name=[stg_directory.get_path_prettify_(maximum=32), description],
            icon=stg_directory.icon,
            menu=stg_directory.get_gui_menu_raw(),
            tool_tip=stg_directory.path
        )
        prx_item.set_status(status)
        prx_item.set_checked(False)
        return prx_item


class DccPublishOpt(object):
    def __init__(self, session, scene_file_path, validation_info_file, rsv_scene_properties, **kwargs):
        self._session = session
        self._scene_file_path = scene_file_path
        self._validation_info_file = validation_info_file
        self._rsv_scene_properties = rsv_scene_properties
        self._kwargs = kwargs

    def execute(self):
        media_files = self._kwargs['review']
        version_type = self._kwargs['version_type']
        scene_file_path = self._scene_file_path

        movie_file_path = None
        if media_files:
            movie_file_path = utl_scripts.ScpVideo.comp_movie(
                media_files
            )

        user = bsc_core.SystemMtd.get_user_name()

        extra_data = dict(
            user=user,
            #
            version_type=self._kwargs['version_type'],
            version_status='pub',
            #
            notice=self._kwargs['notice'],
            description=self._kwargs['description'],
        )

        extra_key = ssn_core.SsnHookFileMtd.set_extra_data_save(extra_data)

        application = self._rsv_scene_properties.get('application')
        if application == 'katana':
            choice_scheme = 'asset-katana-publish'
        elif application == 'maya':
            choice_scheme = 'asset-maya-publish'
        else:
            raise RuntimeError()

        option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key='rsv-task-batchers/asset/gen-surface-export',
                #
                file=scene_file_path,
                #
                extra_key=extra_key,
                #
                choice_scheme=choice_scheme,
                #
                version_type=version_type,
                movie_file=movie_file_path,
                #
                validation_info_file=self._validation_info_file,
                #
                with_workspace_texture_lock=self._kwargs['process.options.with_workspace_texture_lock'],
                #
                user=user,
                #
                td_enable=self._session.get_is_td_enable(),
                rez_beta=self._session.get_is_beta_enable(),
                #
                localhost_enable=self._kwargs['process.deadline.scheme'] == 'localhost'
            )
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=option_opt.to_string()
        )


class AbsPnlAssetPublish(prx_widgets.PrxSessionWindow):
    DCC_VALIDATOR_OPT_CLS = None
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAssetPublish, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self._scene_file_path = None
        self._rsv_scene_properties = None
        self._rsv_task = None
        self._notice_user_names = []

    def set_all_setup(self):
        self._check_key_map = {
            'validation.ignore_shotgun_check': 'with_shotgun_check',
            #
            'validation.ignore_scene_check': 'with_scene_check',
            #
            'validation.ignore_geometry_check': 'with_geometry_check',
            'validation.ignore_geometry_topology_check': 'with_geometry_topology_check',
            #
            'validation.ignore_look_check': 'with_look_check',
            #
            'validation.ignore_texture_check': 'with_texture_check',
            'validation.ignore_texture_workspace_check': 'with_texture_workspace_check',
        }

        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)

        sa_0 = prx_widgets.PrxVScrollArea()
        self._tab_view.set_item_add(
            sa_0,
            name='Validation',
            icon_name_text='Validation',
        )

        sa_1 = prx_widgets.PrxVScrollArea()
        self._tab_view.set_item_add(
            sa_1,
            name='Configure',
            icon_name_text='Configure',
        )

        ep_0 = prx_widgets.PrxExpandedGroup()
        sa_0.add_widget(ep_0)
        ep_0.set_expanded(True)
        ep_0.set_name('check results')

        # v_t = prx_widgets.PrxVToolBar()
        # ep_0.add_widget(v_t)

        h_s_0 = prx_widgets.PrxHSplitter()
        ep_0.add_widget(h_s_0)

        self._filter_tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._filter_tree_view)
        self._filter_tree_view.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 32
        )
        #
        self._result_tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._result_tree_view)
        self._result_tree_view.set_header_view_create(
            [('name', 4), ('description', 2)],
            self.get_definition_window_size()[0]*(2.0/3.0) - 32
        )
        h_s_0.set_stretches([1, 3])
        h_s_0.set_widget_hide_at(0)

        self._tree_view_opt = self.DCC_VALIDATOR_OPT_CLS(
            self._filter_tree_view, self._result_tree_view
        )

        self._cfg_options_prx_node = prx_widgets.PrxNode_('options')
        sa_1.add_widget(self._cfg_options_prx_node)
        self._cfg_options_prx_node.create_ports_by_configure(
            self._session.configure.get('build.node.publish_options'),
        )

        self._cfg_options_prx_node.set(
            'resolver.load', self.set_refresh_all
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._cfg_options_prx_node,
            }
        )

        self._validation_button = prx_widgets.PrxPressItem()
        self._validation_button.set_name('validation')
        self.set_button_add(
            self._validation_button
        )
        self._validation_button.connect_press_clicked_to(self._set_validation_execute_)

        self._publish_button = prx_widgets.PrxPressItem()
        self._publish_button.set_name('publish')
        self.set_button_add(
            self._publish_button
        )
        self._publish_button.connect_press_clicked_to(self._execute_publish_)
        self._publish_button.set_option_click_enable(True)

        self._validation_checker = None
        self._validation_check_options = {}
        self._validation_info_file = None

        self._publish_button.set_enable(
            False
        )

        self._cfg_options_prx_node.get_port(
            'publish.ignore_validation_error'
        ).connect_value_changed_to(
            self.refresh_publish_enable_fnc
        )

        self.set_help_content(
            self._session.configure.get('option.gui.content'),
        )

        self._cfg_options_prx_node.set(
            'validation.ignore_all', self._set_validation_ignore_all_
        )
        self._cfg_options_prx_node.set(
            'validation.ignore_clear', self._set_validation_ignore_clear_
        )

        self.set_refresh_all()

    def _get_publish_is_enable_(self):
        if self._cfg_options_prx_node.get('publish.ignore_validation_error') is True:
            return True
        if self._validation_checker is not None:
            return self._validation_checker.get_is_passed()
        return False

    def _get_validation_info_file_path_(self):
        if self._rsv_scene_properties:
            file_opt = bsc_core.StgFileOpt(
                self._scene_file_path
            )
            return '{directory}/validation/{date}-{user}/{name}-{tag}{ext}.info'.format(
                **dict(
                    directory=file_opt.directory_path,
                    name=file_opt.name_base,
                    date=bsc_core.TimeMtd.get_date_tag(),
                    tag=bsc_core.TimeExtraMtd.get_time_tag_36(),
                    user=bsc_core.SystemMtd.get_user_name(),
                    ext=file_opt.ext
                )
            )

    def _get_validation_info_texts_(self):
        list_ = []
        if self._cfg_options_prx_node.get('publish.ignore_validation_error') is True:
            list_.append(
                'validation check ignore: on'
            )
        if self._validation_checker is not None:
            list_.append(
                'validation check run: on'
            )
            list_.append(self._validation_checker.get_info())
            return list_
        return ['validation check run: off']

    def refresh_publish_enable_fnc(self):
        self._validation_info_file = self._get_validation_info_file_path_()
        if self._validation_info_file is not None:
            info = '\n'.join(self._get_validation_info_texts_())
            bsc_core.StgFileOpt(
                self._validation_info_file
            ).set_write(
                info
            )
            self._publish_button.set_enable(
                self._get_publish_is_enable_()
            )

    def set_refresh_all(self):
        contents = []
        application = bsc_core.SystemMtd.get_application()
        #
        if bsc_core.ApplicationMtd.get_is_dcc():
            self._scene_file_path = self._get_dcc_scene_file_path_()
            self._cfg_options_prx_node.set(
                'resolver.scene_file', self._scene_file_path
            )
            self._cfg_options_prx_node.get_port(
                'resolver.scene_file'
            ).set_locked(True)
        else:
            self._scene_file_path = self._cfg_options_prx_node.get(
                'resolver.scene_file'
            )
        #
        r = rsv_commands.get_resolver()
        #
        self._result_tree_view.set_clear()
        if self._scene_file_path:
            self._tree_view_opt._get_scene_(self._scene_file_path)
            #
            self._rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(self._scene_file_path)
            if self._rsv_scene_properties:
                self._rsv_task = r.get_rsv_task(**self._rsv_scene_properties.value)
                self._notice_user_names = self.get_default_notice_user_names_fnc(
                    **self._rsv_task.properties.get_value()
                )
            else:
                contents.append(
                    u'scene file "{}" is not available'.format(self._scene_file_path)
                )
        else:
            if application == 'katana':
                contents.append(
                    'open a scene file in dcc and retry'
                )

        if contents:
            utl_core.DialogWindow.set_create(
                label=self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Error,
                #
                yes_label='Close', yes_method=self.set_window_close,
                #
                no_visible=False, cancel_visible=False,
                #
                use_exec=False
            )

    def _get_dcc_scene_file_path_(self):
        pass

    def _set_shotgun_version_status_update_(self):
        version_type = self._cfg_options_prx_node.get('shotgun.version.type')
        version_status_mapper = dict(
            daily='rev',
            check='pub',
            downstream='pub'
        )
        version_status = version_status_mapper[version_type]
        self._cfg_options_prx_node.set(
            'shotgun.version.status', version_status
        )

    def _set_validation_ignore_all_(self):
        [self._cfg_options_prx_node.set(k, True) for k, v in self._check_key_map.items()]

    def _set_validation_ignore_clear_(self):
        [self._cfg_options_prx_node.set(k, False) for k, v in self._check_key_map.items()]

    def _set_validation_execute_(self):
        if self._rsv_scene_properties:
            self._validation_check_options = {v: not self._cfg_options_prx_node.get(k) for k, v in self._check_key_map.items()}
            if bsc_core.ApplicationMtd.get_is_dcc():
                if bsc_core.ApplicationMtd.get_is_katana():
                    self._set_katana_validation_in_execute_()
                elif bsc_core.ApplicationMtd.get_is_maya():
                    self._set_maya_validation_in_dcc_()
            else:
                application = self._rsv_scene_properties.get('application')
                if application == 'katana':
                    self._set_katana_validation_execute_by_shell_()
                elif application == 'maya':
                    self._set_maya_validation_execute_by_shell_()

    def _set_gui_validation_check_results_show_(self, session):
        self._validation_checker = session.get_validation_checker()
        self._validation_checker.set_options(
            self._validation_check_options
        )
        #
        self._result_tree_view.set_clear()
        self._tree_view_opt.set_results_at(
            self._rsv_scene_properties,
            self._validation_checker.get_data()
        )
        self.refresh_publish_enable_fnc()

    def _set_dcc_validation_execute_(self, option_hook_key):
        s = ssn_commands.set_option_hook_execute(
            bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key=option_hook_key,
                    file=self._scene_file_path,
                    #
                    **self._validation_check_options
                )
            ).to_string()
        )

        self._set_gui_validation_check_results_show_(s)

    def _set_dcc_validation_execute_by_shell_(self, option_hook_key):
        def completed_fnc_(*args):
            self._set_gui_validation_check_results_show_(s)

        def finished_fnc_(*args):
            pass
        #
        s = ssn_commands.get_option_hook_session(
            bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key=option_hook_key,
                    file=self._scene_file_path,
                    #
                    **self._validation_check_options
                )
            ).to_string()
        )
        cmd = s.get_execute_shell_command()
        #
        q_c_s = utl_core.CommandMonitor.set_create(
            'Validation for {}'.format(self._rsv_task),
            cmd,
            parent=self.widget
        )
        #
        q_c_s.completed.connect(completed_fnc_)
        q_c_s.finished.connect(finished_fnc_)

    def _set_katana_validation_in_execute_(self):
        self._set_dcc_validation_execute_(
            'rsv-task-methods/asset/katana/gen-surface-validation'
        )

    def _set_katana_validation_execute_by_shell_(self):
        self._set_dcc_validation_execute_by_shell_(
            'rsv-task-methods/asset/katana/gen-surface-validation'
        )

    def _set_maya_validation_in_dcc_(self):
        self._set_dcc_validation_execute_(
            'rsv-task-methods/asset/maya/gen-surface-validation'
        )
    @classmethod
    def get_default_notice_user_names_fnc(cls, **kwargs):
        import lxshotgun.objects as stg_objects
        
        import lxshotgun.operators as stg_operators

        c = stg_objects.StgConnector()
        r_o = stg_operators.StgResourceOpt(c.get_stg_resource_query(**kwargs))
        resource_cc_stg_users = r_o.get_cc_stg_users()
        t_o = stg_operators.StgTaskOpt(c.get_stg_task_query(**kwargs))
        task_cc_stg_users = t_o.get_cc_stg_users()
        task_assign_stg_users = t_o.get_assign_stg_users()
        return [c.to_query(i).get('name').decode('utf-8') for i in resource_cc_stg_users+task_cc_stg_users+task_assign_stg_users]

    def _set_maya_validation_execute_by_shell_(self):
        self._set_dcc_validation_execute_by_shell_(
            'rsv-task-methods/asset/maya/gen-surface-validation'
        )

    def _execute_publish_(self):
        def yes_fnc_():
            _kwargs = w.get_options_as_kwargs()
            #
            DccPublishOpt(
                self._session,
                self._scene_file_path,
                self._validation_info_file,
                self._rsv_scene_properties,
                **_kwargs
            ).execute()
            # import time
            # time.sleep(3)

        if self._rsv_scene_properties:
            w = utl_core.DialogWindow.set_create(
                label=self._session.gui_name,
                sub_label='Publish for {}'.format(self._rsv_task),
                content=(
                    '1. choose a version type in "version type";\n'
                    '    a). default is "downstream"\n'
                    '2. entry description in "description";\n'
                    '3. choose one or more image or movie file or make a snapshot in "review";\n'
                    '    a). support formats: "jpg", "exr", "mov"\n'
                    '4. choose one or more user in "notice";\n'
                    '5. configure in "process";\n'
                    '6. press "Apply" to continue'
                ),
                #
                options_configure=self._session.configure.get('build.node.extra_publish'),
                #
                yes_label='Apply',
                #
                yes_method=yes_fnc_,
                #
                no_visible=False,
                show=False,
                #
                window_size=(480, 720),
                #
                # parent=self.widget,
                #
                use_exec=False,
                #
                use_window_modality=False
            )

            w.set_yes_completed_notify_enable(True)
            w.set_completed_content(
                'deadline job submit is completed, press "Close" to continue'
            )
            w.set_window_close_connect_to(
                self.widget.show
            )

            o = w.get_options_node()

            self.widget.hide()

            w.set_window_show()
            # set when window show
            o.set('notice', self._notice_user_names)


class GenPublishOpt(object):
    VERSION_NAME_PATTERN = '{project}.{resource}.{task}.{version}'
    def __init__(self, window, session, rsv_task, version_properties, options):
        self._window = window
        self._session = session
        self._rsv_task = rsv_task
        self._version_properties = version_properties
        self._options = options

        self._version_name = self.VERSION_NAME_PATTERN.format(
            **self._version_properties.get_value()
        )
        self._review_file = None

    def create_or_unlock_version_directory_fnc(self):
        directory_path = self._options.get('version_directory')
        if bsc_core.StgDirectoryOpt(directory_path).get_is_exists() is False:
            bsc_core.StgPathPermissionMtd.create_directory(
                directory_path
            )

    def lock_version_directory_fnc(self):
        directory_path = self._options.get('version_directory')
        if bsc_core.StgDirectoryOpt(directory_path).get_is_exists() is True:
            bsc_core.StgPathPermissionMtd.lock_all_directories(
                directory_path
            )

    def pre_fnc(self):
        self.create_or_unlock_version_directory_fnc()

    def export_review_fnc(self):
        file_paths = self._options['review']

        movie_file_path = None
        if file_paths:
            movie_file_path = utl_scripts.ScpVideo.comp_movie(
                file_paths
            )
        #
        if movie_file_path:
            version = self._version_properties.get('version')
            review_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-review-file'
            )
            review_file_path = review_file_rsv_unit.get_result(
                version=version
            )
            #
            bsc_core.StgPathPermissionMtd.copy_to_file(
                movie_file_path, review_file_path
            )
            self._review_file = movie_file_path

    def export_scene_fnc(self):
        def collection_and_repath_texture_fnc_(file_path_src_, scene_directory_path_, texture_directory_path_, look_yml_directory_path_):
            _cmd = utl_process.MayaProcess.get_command(
                'method=collection-and-repath-texture&file={}&scene_directory={}&texture_directory={}&look_yml_directory={}'.format(
                    file_path_src_,
                    scene_directory_path_,
                    texture_directory_path_,
                    look_yml_directory_path_
                )
            )
            bsc_core.SubProcessMtd.execute_with_result_in_linux(
                _cmd, clear_environ='auto'
            )
        #
        count_dict = {}
        file_paths = self._options.get('extra.scene')
        if file_paths:
            version = self._version_properties.get('version')
            texture_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-texture-dir'
            )
            texture_directory_path = texture_directory_rsv_unit.get_result(
                version=version
            )
            look_yml_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-look-yml-dir'
            )
            look_yml_directory_path = look_yml_directory_rsv_unit.get_result(
                version=version
            )
            with self._window.gui_progressing(maximum=len(file_paths), label='export scene') as g_p:
                for i_index, i_file_path in enumerate(file_paths):
                    g_p.set_update()
                    i_file_opt = bsc_core.StgFileOpt(i_file_path)
                    if i_file_opt.get_is_file():
                        i_ext = i_file_opt.get_ext()
                        if i_ext in count_dict:
                            i_c = len(count_dict[i_ext])
                        else:
                            i_c = 0

                        if i_ext == '.ma':
                            i_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-maya-scene-src-file'
                            )
                            i_scene_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-maya-scene-dir'
                            )
                        elif i_ext == '.katana':
                            i_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-katana-scene-src-file'
                            )
                            i_scene_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-katana-scene-dir'
                            )
                        else:
                            raise RuntimeError()
                        #
                        i_scene_src_file_path_tgt = i_scene_src_file_rsv_unit.get_result(
                            version=version
                        )
                        i_scene_directory_path = i_scene_directory_rsv_unit.get_result(
                            version=version
                        )
                        if i_c > 0:
                            i_scene_src_file_path_opt_tgt = bsc_core.StgFileOpt(
                                i_scene_src_file_path_tgt
                            )
                            i_scene_src_file_path_tgt = '{}.{}{}'.format(
                                i_scene_src_file_path_opt_tgt.get_path_base(),
                                i_c,
                                i_scene_src_file_path_opt_tgt.get_ext()
                            )
                        #
                        count_dict.setdefault(
                            i_ext, []
                        ).append(i_file_path)
                        if i_file_opt.get_is_readable() is False:
                            bsc_core.StgPathPermissionMtd.unlock(i_file_path)
                        #
                        i_file_opt.set_copy_to_file(
                            i_scene_src_file_path_tgt
                        )
                        #
                        if i_ext == '.ma':
                            collection_and_repath_texture_fnc_(
                                i_scene_src_file_path_tgt,
                                i_scene_directory_path,
                                texture_directory_path,
                                look_yml_directory_path,
                            )

    def export_image_fnc(self):
        file_paths = self._options.get('extra.image')
        if file_paths:
            version = self._version_properties.get('version')
            image_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-image-dir'
            )
            image_directory_path = image_directory_rsv_unit.get_result(
                version=version
            )
            with self._window.gui_progressing(maximum=len(file_paths), label='export image') as g_p:
                for i_index, i_file_path in enumerate(file_paths):
                    g_p.set_update()
                    i_file_tile_paths = bsc_core.StgFileMultiplyMtd.get_exists_tiles(
                        i_file_path
                    )
                    for j_file_path in i_file_tile_paths:
                        j_file_opt = bsc_core.StgFileOpt(j_file_path)
                        j_file_path_tgt = '{}/{}'.format(
                            image_directory_path, j_file_opt.get_name()
                        )
                        if j_file_opt.get_is_readable() is False:
                            bsc_core.StgPathPermissionMtd.unlock(j_file_path)
                        #
                        j_file_opt.set_copy_to_file(
                            j_file_path_tgt
                        )

    def export_shotgun_fnc(self):
        import lxshotgun.rsv.scripts as stg_rsv_scripts
        
        version = self._version_properties.get('version')
        user = self._version_properties.get('user')
        review_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='{branch}-review-file'
        )
        review_file_path = review_file_rsv_unit.get_exists_result(
            version=version
        )
        
        stg_rsv_scripts.RsvStgTaskOpt(self._rsv_task).execute_stg_version_create(
            version=version,
            user=user,
            movie_file=review_file_path,
            description=self._options.get('description'),
            notice=self._options.get('notice'),
            #
            version_type=self._options.get('version_type'),
            # version_status=None,
            #
            create_shotgun_playlists=True
        )

    def post_fnc(self):
        self.lock_version_directory_fnc()
    @utl_core.Modifier.exception_catch
    def execute(self):
        fncs = [
            self.pre_fnc,
            self.export_review_fnc,
            self.export_scene_fnc,
            self.export_image_fnc,
            # export shotgun latest
            self.export_shotgun_fnc,
            self.post_fnc
        ]
        with self._window.gui_progressing(maximum=len(fncs), label='general publish process') as g_p:
            for i_fnc in fncs:
                g_p.set_update()
                i_fnc()
        #
        self._window.show_message(
            'publish process is complected'
        )


class AbsPnlGeneralPublish(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlGeneralPublish, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self._task_data = {}
        #
        self._stg_user = None
        self._stg_task = None
        #
        self._rsv_task = None
        self._version_properties = None

    def set_all_setup(self):
        sa_1 = prx_widgets.PrxVScrollArea()
        self.add_widget(sa_1)
        #
        self._options_prx_node = prx_widgets.PrxNode_('options')
        sa_1.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_configure(
            self._session.configure.get('build.node.options')
        )

        self._options_prx_node.get_port('resource_type').connect_value_changed_to(
            self.refresh_resource_fnc
        )
        #
        self._options_prx_node.get_port('shotgun.project').connect_value_changed_to(
            self.refresh_resource_fnc
        )
        #
        self._options_prx_node.get_port('shotgun.resource').connect_value_changed_to(
            self.refresh_task_fnc
        )
        #
        self._options_prx_node.get_port('shotgun.task').connect_value_changed_to(
            self.refresh_next_enable_fnc
        )
        #
        self._next_button = prx_widgets.PrxPressItem()
        self._next_button.set_name('next')
        self.set_button_add(
            self._next_button
        )
        self._next_button.connect_press_clicked_to(self.execute_show_next)
        self._next_button.set_option_click_enable(True)

        self._next_button.set_enable(
            False
        )
        #
        self.set_option_unit_name('publish')
        layout = self.get_option_unit_layout()
        sa_2 = prx_widgets.PrxVScrollArea()
        layout.addWidget(sa_2.widget)
        self._publish_options_prx_node = prx_widgets.PrxNode_('options')
        sa_2.add_widget(self._publish_options_prx_node)
        self._publish_options_prx_node.create_ports_by_configure(
            self._session.configure.get('build.node.publish_options')
        )

        self._publish_options_prx_node.get_port('version_scheme').connect_value_changed_to(
            self.refresh_publish_version_directory
        )

        tool_bar = prx_widgets.PrxHToolBar()
        layout.addWidget(tool_bar.widget)
        tool_bar.set_expanded(True)

        self._publish_button = prx_widgets.PrxPressItem()
        tool_bar.add_widget(self._publish_button)
        self._publish_button.set_name('publish')
        self._publish_button.connect_press_clicked_to(
            self.execute_publish
        )

        self.refresh_all_fnc()

    def get_stg_project(self):
        return self._options_prx_node.get_port('shotgun.project').get_stg_entity()

    def get_stg_resource(self):
        return self._options_prx_node.get_port('shotgun.resource').get_stg_entity()

    def get_stg_task(self):
        return self._options_prx_node.get_port('shotgun.task').get_stg_entity()

    def load_from_task_id(self, task_id):
        self._task_data = self._stg_connector.get_data_from_task_id(task_id)
        if self._task_data:
            resource_type = self._task_data['branch']
            self._options_prx_node.set(
                'resource_type', resource_type
            )
            #
            self.refresh_project_fnc(self._task_data)
            self.refresh_resource_fnc(self._task_data)
            self.refresh_task_fnc(self._task_data)
            self.refresh_next_enable_fnc(self._task_data)
            self.execute_show_next()

    def refresh_all_fnc(self):
        import lxshotgun.objects as stg_objects
        #
        self._stg_connector = stg_objects.StgConnector()
        self._user_name = bsc_core.SystemMtd.get_user_name()
        self._stg_user = self._stg_connector.get_stg_user(user=self._user_name)
        if not self._stg_user:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content='user "{}" is not available'.format(self._user_name),
                status=utl_core.DialogWindow.ValidatorStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            self.set_window_close_later()
            return

        task_id = bsc_core.EnvironMtd.get(
            'PAPER_TASK_ID'
        )
        if task_id:
            self.load_from_task_id(task_id)
        else:
            self.refresh_project_fnc()

    def refresh_project_fnc(self, data=None):
        p = self._options_prx_node.get_port('shotgun.project')
        p.set_clear()
        if data is not None:
            project = data['project']
            p.set(str(project).upper())
        #
        p.set_shotgun_entity_kwargs(
            dict(
                entity_type='Project',
                filters=[
                    ['users', 'in', [self._stg_user]],
                    ['sg_status', 'in', ['Active', 'Accomplish']]
                ],
                fields=['name', 'sg_description']
            ),
            name_field='name',
            keyword_filter_fields=['name', 'sg_description'],
            tag_filter_fields=['sg_status']
        )

    def refresh_resource_fnc(self, data=None):
        p = self._options_prx_node.get_port('shotgun.resource')
        p.set_clear()
        self._options_prx_node.get_port('shotgun.task').set_clear()
        #
        resource_type = self._options_prx_node.get('resource_type')
        if resource_type not in ['asset', 'sequence', 'shot']:
            return
        p.set_name(resource_type)
        #
        if data is not None:
            stg_project = self._stg_connector.get_stg_project(
                **data
            )
            resource = data['resource']
            p.set(resource)
        else:
            stg_project = self.get_stg_project()
        #
        if not stg_project:
            return
        stg_entity_type = self._stg_connector._get_stg_resource_type_(resource_type)
        if resource_type == 'asset':
            tag_filter_fields = ['sg_asset_type']
            keyword_filter_fields = ['code', 'sg_chinese_name']
        elif resource_type == 'sequence':
            tag_filter_fields = ['tags']
            keyword_filter_fields = ['code', 'description']
        elif resource_type == 'shot':
            tag_filter_fields = ['sg_sequence']
            keyword_filter_fields = ['code', 'description']
        else:
            raise RuntimeError()

        p.set_shotgun_entity_kwargs(
            dict(
                entity_type=stg_entity_type,
                filters=[
                    ['project', 'is', stg_project],
                ],
                fields=keyword_filter_fields
            ),
            name_field='code',
            keyword_filter_fields=keyword_filter_fields,
            tag_filter_fields=tag_filter_fields,
        )

    def refresh_task_fnc(self, data=None):
        p = self._options_prx_node.get_port('shotgun.task')
        p.set_clear()
        if data is not None:
            stg_resource = self._stg_connector.get_stg_resource(
                **data
            )
            task = data['task']
            p.set(task)
        else:
            stg_resource = self.get_stg_resource()
        #
        if not stg_resource:
            return
        #
        p.set_shotgun_entity_kwargs(
            {
                'entity_type': 'Task',
                'filters': [
                    ['entity', 'is', stg_resource]
                ],
                'fields': ['content', 'sg_status_list'],
            },
            name_field='content',
            keyword_filter_fields=['content', 'sg_status_list'],
            tag_filter_fields=['step'],
        )

    def refresh_stg_task_fnc(self):
        pass

    def refresh_next_enable_fnc(self, data=None):
        if data is not None:
            self._stg_task = self._stg_connector.get_stg_task(
                **data
            )
        else:
            self._stg_task = self.get_stg_task()
        #
        if self._stg_task is not None:
            self._next_button.set_enable(True)
        else:
            self._next_button.set_enable(False)

    def refresh_publish_notice(self):
        def post_fnc_():
            pass

        def cache_fnc_():
            import lxshotgun.operators as stg_operators

            r_o = stg_operators.StgResourceOpt(self._stg_connector.get_stg_resource_query(**stg_resource))
            resource_cc_stg_users = r_o.get_cc_stg_users()

            t_o = stg_operators.StgTaskOpt(self._stg_connector.get_stg_task_query(**stg_task))
            task_cc_stg_users = t_o.get_cc_stg_users()
            task_assign_stg_users = t_o.get_assign_stg_users()
            return [self._stg_connector.to_query(i).get('name').decode('utf-8') for i in resource_cc_stg_users+task_cc_stg_users+task_assign_stg_users]

        def built_fnc_(user_names):
            self._publish_options_prx_node.set(
                'notice', user_names
            )

        p = self._publish_options_prx_node.get_port('notice')
        p.set_clear()
        p.set_shotgun_entity_kwargs(
            dict(
                entity_type='HumanUser',
                filters=[
                    ['sg_studio', 'is', 'CG'],
                    ['sg_status_list', 'is', 'act']
                ],
                fields=['name', 'email', 'sg_nickname']
            ),
            name_field='name',
            keyword_filter_fields=['name', 'email', 'sg_nickname'],
            tag_filter_fields=['department']
        )

        stg_task = self._stg_task
        stg_resource = self._stg_connector.get_stg_resource(**self._task_data)

        p.run_as_thread(
            cache_fnc_, built_fnc_, post_fnc_
        )

    def refresh_publish_version_directory(self):
        if self._task_data:
            version_scheme = self._publish_options_prx_node.get('version_scheme')
            #
            resolver = rsv_commands.get_resolver()
            self._rsv_task = resolver.get_rsv_task(
                **self._task_data
            )
            version_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-release-version-dir'
            )
            version_directory_path = version_directory_rsv_unit.get_result(
                version=version_scheme
            )
            self._publish_options_prx_node.set(
                'version_directory', version_directory_path
            )
            self._version_properties = version_directory_rsv_unit.get_properties_by_result(
                version_directory_path
            )
            self._version_properties.set_update(self._task_data)
            self._version_properties.set('user', self._user_name)

    def refresh_publish_options(self):
        self._publish_options_prx_node.set('version_type', 'daily')
        self._publish_options_prx_node.set('version_scheme', 'new')
        self._publish_options_prx_node.set('description', '')
        self._publish_options_prx_node.get_port('review').set_clear()
        self._publish_options_prx_node.get_port('extra.scene').set_clear()
        self._publish_options_prx_node.get_port('extra.image').set_clear()

    def refresh_publish_scene(self):
        if bsc_core.ApplicationMtd.get_is_dcc():
            if bsc_core.ApplicationMtd.get_is_maya():
                import lxmaya.dcc.dcc_objects as mya_dcc_objects
                self._publish_options_prx_node.set(
                    'extra.scene', [mya_dcc_objects.Scene.get_current_file_path()]

                )
            elif bsc_core.ApplicationMtd.get_is_katana():
                import lxkatana.dcc.dcc_objects as ktn_dcc_objects
                self._publish_options_prx_node.set(
                    'extra.scene', [ktn_dcc_objects.Scene.get_current_file_path()]

                )

    def execute_show_next(self):
        if self._next_button.get_is_enable() is True:
            self._task_data = self._stg_connector.get_data_from_task_id(
                str(self._stg_task['id'])
            )
            self.set_option_unit_show()
            self.set_option_unit_name(
                'publish for [{project}.{resource}.{task}]'.format(
                    **self._task_data
                )
            )
            self.refresh_publish_options()
            self.refresh_publish_version_directory()
            self.refresh_publish_notice()
            self.refresh_publish_scene()
    
    def execute_publish(self):
        p = GenPublishOpt(
            self,
            self._session,
            self._rsv_task,
            self._version_properties,
            self._publish_options_prx_node.get_as_kwargs()
        )
        p.execute()
