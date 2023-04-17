# coding:utf-8
import collections

from lxbasic import bsc_configure, bsc_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

import lxutil.extra.methods as utl_etr_methods

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

        self._filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_view,
            prx_tree_view_tgt=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def set_select(self):
        utl_prx_operators.PrxDccObjTreeViewSelectionOpt._set_dcc_select_(
            prx_tree_view=self._result_tree_view,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )

    def set_results_at(self, rsv_scene_properties, results):
        file_path = rsv_scene_properties.get('extra.file')
        check_results = results['check_results']
        scene_prx_item = self._get_scene_(file_path)
        scene_prx_item.clear_children()
        self._filter_opt.set_restore()
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
        self._result_tree_view.set_items_expand_by_depth(1)

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

        prx_item = scene_prx_item.set_child_add(
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
                dcc_path = dcc_path_dag_opt.set_translate_to(self.DCC_PATHSEP).to_string()
        #
        dcc_obj = self.DCC_NODE_CLS(dcc_path)
        prx_item = group_prx_item.set_child_add(
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
            dcc_path = dcc_path_dag_opt.set_translate_to(self.DCC_PATHSEP).to_string()
        #
        dcc_obj = self.DCC_COMPONENT_CLS(dcc_path)
        prx_item = node_prx_item.set_child_add(
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
        prx_item = node_prx_item.set_child_add(
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
        prx_item = node_prx_item.set_child_add(
            name=[stg_directory.get_path_prettify_(maximum=32), description],
            icon=stg_directory.icon,
            menu=stg_directory.get_gui_menu_raw(),
            tool_tip=stg_directory.path
        )
        prx_item.set_status(status)
        prx_item.set_checked(False)
        return prx_item


class DccPublisherOpt(object):
    def __init__(self, session, scene_file_path, validation_info_file, rsv_scene_properties, **kwargs):
        self._session = session
        self._scene_file_path = scene_file_path
        self._validation_info_file = validation_info_file
        self._rsv_scene_properties = rsv_scene_properties
        self._kwargs = kwargs

    def set_run(self):
        k = self._kwargs
        media_files = self._kwargs['review']
        version_type = self._kwargs['version_type']
        scene_file_path = self._scene_file_path

        scene_file_opt = bsc_core.StgFileOpt(scene_file_path)
        movie_file_path = None
        if media_files:
            user_directory_path = bsc_core.StgTmpBaseMtd.get_user_directory('vedio-converter')

            movie_file_path = '{}/{}.mov'.format(
                user_directory_path,
                scene_file_opt.name_base,
                bsc_core.TimestampOpt(
                    bsc_core.StgFileOpt(scene_file_path).get_modify_timestamp()
                ).get_as_tag_36()
            )

            movie_file_opt = bsc_core.StgFileOpt(movie_file_path)
            movie_file_opt.create_directory()

            utl_etr_methods.EtrRv.convert_to_mov(
                input=media_files,
                output=movie_file_path
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
                td_enable=self._session.get_td_enable(),
                rez_beta=self._session.get_rez_beta(),
                #
                localhost_enable=self._kwargs['process.deadline.scheme'] == 'localhost'
            )
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=option_opt.to_string()
        )


class AbsPnlAssetPublisher(prx_widgets.PrxSessionWindow):
    DCC_VALIDATOR_OPT_CLS = None
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAssetPublisher, self).__init__(session, *args, **kwargs)

    def set_variants_restore(self):
        self._scene_file_path = None
        self._rsv_scene_properties = None

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
        self.set_widget_add(self._tab_view)

        sa_0 = prx_widgets.PrxScrollArea()
        self._tab_view.set_item_add(
            sa_0,
            name='Validation',
            icon_name_text='Validation',
        )

        sa_1 = prx_widgets.PrxScrollArea()
        self._tab_view.set_item_add(
            sa_1,
            name='Configure',
            icon_name_text='Configure',
        )

        ep_0 = prx_widgets.PrxExpandedGroup()
        sa_0.set_widget_add(ep_0)
        ep_0.set_expanded(True)
        ep_0.set_name('check results')

        # v_t = prx_widgets.PrxVToolBar()
        # ep_0.set_widget_add(v_t)

        h_s_0 = prx_widgets.PrxHSplitter()
        ep_0.set_widget_add(h_s_0)

        self._filter_tree_view = prx_widgets.PrxTreeView()
        h_s_0.set_widget_add(self._filter_tree_view)
        self._filter_tree_view.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 32
        )
        #
        self._result_tree_view = prx_widgets.PrxTreeView()
        h_s_0.set_widget_add(self._result_tree_view)
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
        sa_1.set_widget_add(self._cfg_options_prx_node)
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
        self._publish_button.connect_press_clicked_to(self._set_publish_execute_)
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
            self._set_publish_enable_refresh_
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

    def _set_publish_enable_refresh_(self):
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
        self._set_publish_enable_refresh_()

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

    @utl_gui_qt_core.set_prx_window_waiting
    def _set_katana_validation_in_execute_(self):
        self._set_dcc_validation_execute_(
            'rsv-task-methods/asset/katana/gen-surface-validation'
        )

    def _set_katana_validation_execute_by_shell_(self):
        self._set_dcc_validation_execute_by_shell_(
            'rsv-task-methods/asset/katana/gen-surface-validation'
        )

    @utl_gui_qt_core.set_prx_window_waiting
    def _set_maya_validation_in_dcc_(self):
        self._set_dcc_validation_execute_(
            'rsv-task-methods/asset/maya/gen-surface-validation'
        )

    def _set_maya_validation_execute_by_shell_(self):
        self._set_dcc_validation_execute_by_shell_(
            'rsv-task-methods/asset/maya/gen-surface-validation'
        )

    @utl_gui_qt_core.set_prx_window_waiting
    def _set_publish_execute_(self):
        def yes_fnc_():
            _kwargs = w.get_options_as_kwargs()
            #
            DccPublisherOpt(
                self._session,
                self._scene_file_path,
                self._validation_info_file,
                self._rsv_scene_properties,
                **_kwargs
            ).set_run()
            # import time
            # time.sleep(3)

        if self._rsv_scene_properties:
            w = utl_core.DialogWindow.set_create(
                label=self._session.gui_name,
                sub_label='Publish for {}'.format(self._rsv_task),
                content=(
                    u'1. choose a version type in "version type";\n'
                    u'    a). default is "downstream"\n'
                    u'2. entry description in "description";\n'
                    u'3. choose one or more image or movie file or make a snapshot in "review";\n'
                    u'    a). support formats: "jpg", "exr", "mov"\n'
                    u'4. choose one or more user in "notice";\n'
                    u'5. configure in "process";\n'
                    u'6. press "Confirm" to continue'
                ),
                #
                options_configure=self._session.configure.get('build.node.extra_publish'),
                #
                yes_label='Confirm',
                #
                yes_method=yes_fnc_,
                #
                no_visible=False,
                show=False,
                #
                window_size=(480, 720),
                #
                parent=self.widget,
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

            self.widget.hide()

            w.set_window_show()
