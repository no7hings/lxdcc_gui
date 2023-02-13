# coding:utf-8
import time

from lxbasic import bsc_configure, bsc_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil_gui.proxy.operators as utl_prx_operators

import lxsession.commands as ssn_commands

import lxresolver.commands as rsv_commands

from lxutil_gui import utl_gui_core

import lxresolver.methods as rsv_methods

import lxutil.rsv.objects as utl_rsv_objects


class AbsPnlAssetWorkspaceTextureManager(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = None
    DCC_SELECTION_CLS = None
    TEXTURE_WORKSPACE_CLS = None
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAssetWorkspaceTextureManager, self).__init__(session, *args, **kwargs)

    def set_variants_restore(self):
        self._dcc_texture_references = None
        self._dcc_objs = []

        self._create_data = []

        self._is_disable = False

        self._file_path = None

    def set_all_setup(self):
        self._tab_view = prx_widgets.PrxTabView()
        self.set_widget_add(self._tab_view)

        s_0 = prx_widgets.PrxScrollArea()
        self._tab_view.set_item_add(
            s_0,
            name='workspace',
            icon_name_text='workspace',
        )

        self._options_prx_node = prx_widgets.PrxNode_('options')
        s_0.set_widget_add(self._options_prx_node)
        self._options_prx_node.set_ports_create_by_configure(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.set(
            'control.new_version', self._set_wsp_version_new_
        )
        self._options_prx_node.get_port(
            'control.variant'
        ).set_changed_connect_to(
            self._set_wsp_texture_directories_update_
        )

        self._options_prx_node.set(
            'control.lock_all_version', self._set_wsp_all_version_lock_
        )

        self._options_prx_node.set(
            'texture.create.execute', self._set_wsp_tx_create_execute_
        )

        self._options_prx_node.set(
            'texture.create.execute_us_deadline', self._set_wsp_tx_create_execute_by_deadline_
        )

        self._options_prx_node.set(
            'refresh', self._set_texture_workspace_update_
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )

        self.set_refresh_all()

    def _set_dcc_scene_update_(self):
        self._file_path = None

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = None

    def _set_dcc_objs_update_(self):
        self._dcc_objs = []

    def _set_texture_workspace_update_(self):
        self._rsv_workspace_texture_opt = utl_rsv_objects.RsvAssetWorkspaceTextureOpt(self._rsv_task)
        current_variant = 'main'
        self._rsv_workspace_texture_opt.set_current_variant(current_variant)
        if self._set_workspace_check_(current_variant) is True:
            self._options_prx_node.set(
                'resolver.task', self._rsv_task.path
            )

            self._options_prx_node.set(
                'control.variant', [current_variant]
            )

            self._options_prx_node.set(
                'control.variant', current_variant
            )
            #
            self._set_wsp_texture_directories_update_()

    def _set_wsp_texture_directories_update_(self):
        variant = self._options_prx_node.get(
            'control.variant'
        )
        unlocked_versions = self._rsv_workspace_texture_opt.get_all_unlocked_versions_at(
            variant
        )
        if unlocked_versions:
            self._options_prx_node.set(
                'texture.directories',
                [self._rsv_workspace_texture_opt.get_directory_path_at(variant, i) for i in unlocked_versions]
            )
        else:
            if unlocked_versions:
                self._options_prx_node.set(
                    'texture.directories',
                    []
                )

    def _set_workspace_check_(self, current_variant):
        def yes_fnc_():
            self._rsv_workspace_texture_opt.set_version_create_at(
                current_variant, 'new'
            )

        self._is_disable = True

        directory_path = self._rsv_workspace_texture_opt.get_directory_path_at(
            current_variant, 'latest'
        )
        if directory_path:
            return True
        else:
            w = utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content='workspace is not install in variant "{}", press "Confirm" to continue'.format(
                    current_variant
                ),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Confirm',
                #
                yes_method=yes_fnc_,
                #
                no_visible=False,
                # show=False,
                parent=self.widget,
                window_size=(480, 480),
            )
            result = w.get_result()
            if result is True:
                return True
            else:
                self._is_disable = True
                self.set_window_close()

    def _set_wsp_version_new_(self):
        def yes_fnc_():
            self._rsv_workspace_texture_opt.set_version_create_at(
                variant, next_version
            )

            _variant = variant
            _from_version = n.get('version')
            _to_version = next_version

            self._set_wsp_texture_pull_(
                _variant, _from_version, _to_version,
            )

            self._rsv_workspace_texture_opt.set_version_lock_at(
                _variant, _from_version
            )

            time.sleep(2)
            self._set_texture_workspace_update_()

        variant = self._options_prx_node.get('control.variant')
        next_version = self._rsv_workspace_texture_opt.get_new_version_at(variant)

        w = utl_core.DialogWindow.set_create(
            self._session.gui_name,
            content=u'create new version "{}" in variant "{}" and pull textures from choose version ( lock choose version ), press "Confirm" to continue'.format(
                next_version, variant
            ),
            status=utl_core.DialogWindow.ValidatorStatus.Warning,
            #
            options_configure=self._session.configure.get('build.node.new_version'),
            #
            yes_label='Confirm',
            #
            yes_method=yes_fnc_,
            #
            no_visible=False,
            show=False,
            #
            parent=self.widget,
            window_size=(480, 480),
        )

        n = w.get_options_node()
        v_p = n.get_port('version')
        all_versions = self._rsv_workspace_texture_opt.get_all_versions_at(variant)
        all_locked_versions = self._rsv_workspace_texture_opt.get_all_locked_versions_at(variant)

        v_p.set(
            all_versions
        )
        [v_p.set_icon_file_as_value(i, utl_gui_core.RscIconFile.get('lock')) for i in all_locked_versions]

        w.set_window_show()

    def _set_wsp_all_version_lock_(self):
        def yes_fnc_():
            if unlocked_directory_paths:
                with utl_core.GuiProgressesRunner.create(maximum=len(unlocked_directory_paths), label='lock version directory') as g_p:
                    for _i in unlocked_directory_paths:
                        self._rsv_workspace_texture_opt.set_directory_locked(_i)
                        g_p.set_update()
            #
            time.sleep(2)
            self._set_texture_workspace_update_()

        self._set_dcc_texture_references_update_()
        self._set_dcc_objs_update_()

        directory_paths = self._rsv_workspace_texture_opt.get_all_directories(
            self._dcc_objs
        )

        unlocked_directory_paths = [i for i in directory_paths if bsc_core.StorageMtd.get_is_writeable(i) is True]
        if unlocked_directory_paths:
            w = utl_core.DialogWindow.set_create(
                self._session.gui_name,
                sub_label='Lock All Version',
                content=u'lock all texture directories(used and matched "texture workspace" rule), press "Confirm" to continue',
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                options_configure=self._session.configure.get('build.node.lock_all_version'),
                #
                yes_label='Confirm',
                #
                yes_method=yes_fnc_,
                #
                no_visible=False,
                show=False,
                #
                parent=self.widget,
                window_size=(480, 480)
            )

            w.get_options_node().set(
                'directories', unlocked_directory_paths
            )

            w.set_window_show()
        else:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'all texture directories(used and matched "texture workspace" rule) is locked',
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )

    def _set_wsp_texture_pull_(self, from_variant, from_version, to_version):
        directory_path_src_0 = self._rsv_workspace_texture_opt.get_src_directory_path_at(
            from_variant, from_version
        )
        directory_path_tx_0 = self._rsv_workspace_texture_opt.get_tx_directory_path_at(
            from_variant, from_version
        )

        directory_path_src_1 = self._rsv_workspace_texture_opt.get_src_directory_path_at(
            from_variant, to_version
        )
        directory_path_tx_1 = self._rsv_workspace_texture_opt.get_tx_directory_path_at(
            from_variant, to_version
        )

        method_args = [
            (self._set_wsp_texture_pull_as_link_, (directory_path_src_0, directory_path_src_1)),
            (self._set_wsp_texture_pull_as_link_, (directory_path_tx_0, directory_path_tx_1))
        ]

        with utl_core.GuiProgressesRunner.create(maximum=len(method_args), label='execute texture pull method') as g_p:
            for i_method, i_args in method_args:
                g_p.set_update()
                i_method(*i_args)
    @classmethod
    def _set_wsp_texture_pull_as_link_(cls, directory_path_src, directory_path_tgt):
        file_paths_src = bsc_core.StgDirectoryMtd.get_file_paths__(
            directory_path_src
        )
        if file_paths_src:
            with utl_core.GuiProgressesRunner.create(maximum=len(file_paths_src), label='pull texture as link') as g_p:
                for i_file_path in file_paths_src:
                    g_p.set_update()
                    #
                    i_texture_src = utl_dcc_objects.OsTexture(
                        i_file_path
                    )
                    #
                    i_texture_src.set_link_to_directory(
                        directory_path_tgt
                    )

    def set_refresh_all(self):
        self._set_dcc_scene_update_()
        #
        if self._file_path is not None:
            self._resolver = rsv_commands.get_resolver()
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
                self._file_path
            )
            if self._rsv_scene_properties:
                self._rsv_task = self._resolver.get_rsv_task_by_any_file_path(
                    self._file_path
                )
                self._rsv_entity = self._rsv_task.get_rsv_resource()

                self._set_texture_workspace_update_()

    def _set_version_new_(self):
        pass

    def _set_tx_create_data_update_(self, directory_paths, force_enable=False, ext_tgt='.tx'):
        self._create_data = []
        with utl_core.GuiProgressesRunner.create(maximum=len(directory_paths), label='create texture-tx in directory') as g_p:
            for i_directory_path in directory_paths:
                i_directory_path_src = '{}/src'.format(i_directory_path)
                i_directory_path_tgt = '{}/{}'.format(i_directory_path, ext_tgt[1:])
                self._set_tx_create_data_update_at_(
                    i_directory_path_src, i_directory_path_tgt,
                    force_enable, ext_tgt,
                )
                g_p.set_update()

    def _set_tx_create_data_update_at_(self, directory_path_src, directory_path_tgt, force_enable=False, ext_tgt='.tx'):
        file_paths_src = bsc_core.StgDirectoryMtd.get_file_paths__(
            directory_path_src
        )
        if file_paths_src:
            with utl_core.GuiProgressesRunner.create(maximum=len(file_paths_src), label='texture-tx create running') as g_p:
                for i_file_path in file_paths_src:
                    i_texture_src = utl_dcc_objects.OsTexture(
                        i_file_path
                    )
                    if i_texture_src.ext != ext_tgt:
                        if force_enable is True:
                            self._create_data.append(
                                (i_texture_src.path, directory_path_tgt)
                            )
                        else:
                            if i_texture_src.get_is_exists_as_tgt_ext(
                                ext_tgt,
                                directory_path_tgt
                            ) is False:
                                self._create_data.append(
                                    (i_texture_src.path, directory_path_tgt)
                                )
                    #
                    g_p.set_update()

    def _set_tx_create_by_data_(self, button, post_fnc=None):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            # print '\n'.join(results)

        def status_update_at_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            for i_index, (i_file_path, i_output_directory_path) in enumerate(self._create_data):
                bsc_core.StorageMtd.set_directory_create(
                    i_output_directory_path
                )

                # print i_file_path, i_output_directory_path

                i_cmd = utl_dcc_objects.OsTexture._get_unit_tx_create_cmd_by_src_force_(
                    i_file_path,
                    search_directory_path=i_output_directory_path,
                )
                if button.get_is_stopped():
                    break
                #
                if i_cmd:
                    bsc_core.PrcCmdThread.set_wait()
                    i_t = bsc_core.PrcCmdThread.set_start(i_cmd, i_index)
                    i_t.status_changed.set_connect_to(status_update_at_fnc_)
                    i_t.finished.set_connect_to(finished_fnc_)
                else:
                    status_update_at_fnc_(
                        i_index, bsc_configure.Status.Completed
                    )
                    finished_fnc_(
                        i_index, bsc_configure.Status.Completed
                    )

        def quit_fnc_():
            button.set_stopped()
            #
            time.sleep(1)
            #
            t.quit()
            t.wait()
            t.deleteLater()

        contents = []
        if self._create_data:
            button.set_stopped(False)

            c = len(self._create_data)

            button.set_status(bsc_configure.Status.Started)
            button.set_initialization(c, bsc_configure.Status.Started)

            t = utl_gui_qt_core.QtMethodThread(self.widget)
            t.set_method_add(
                run_fnc_
            )
            t.start()
            if post_fnc is not None:
                t.run_finished.connect(
                    post_fnc
                )

            self.set_window_close_connect_to(quit_fnc_)
        else:
            button.set_restore()

            contents = [
                'non-texture(s) for create'
            ]

        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False
        else:
            return True

    def _set_wsp_tx_create_execute_(self):
        force_enable = self._options_prx_node.get('texture.create.force_enable')
        ext_tgt = '.tx'
        button = self._options_prx_node.get_port('texture.create.execute')
        directory_paths = self._options_prx_node.get('texture.directories')
        if directory_paths:
            method_args = [
                (self._set_tx_create_data_update_, (directory_paths, force_enable, ext_tgt)),
                (self._set_tx_create_by_data_, (button,))
            ]
            with utl_core.GuiProgressesRunner.create(maximum=len(method_args), label='texture-tx create processing') as g_p:
                for i_fnc, i_args in method_args:
                    g_p.set_update()
                    #
                    i_result = i_fnc(*i_args)
                    if i_result is False:
                        break
        else:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content='non-directory(s) for create',
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )

    def _set_wsp_tx_create_execute_by_deadline_(self):
        force_enable = self._options_prx_node.get('texture.create.force_enable')
        ext_tgt = '.tx'
        directory_paths = self._options_prx_node.get('texture.directories')
        if directory_paths:
            directory_paths_src = ['{}/src'.format(i) for i in directory_paths]
            directory_paths_tgt = ['{}/{}'.format(i, ext_tgt[1:]) for i in directory_paths]

            j_option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key='methods/texture/texture-convert',
                    #
                    directories=directory_paths_src,
                    output_directories=directory_paths_tgt,
                    #
                    force_enable=force_enable,
                    #
                    target_ext=ext_tgt,
                    width=None,
                    #
                    td_enable=self._session.get_td_enable(),
                    rez_beta=self._session.get_rez_beta(),
                )
            )
            #
            session = ssn_commands.set_option_hook_execute_by_deadline(
                option=j_option_opt.to_string()
            )
            ddl_job_id = session.get_ddl_job_id()

            utl_core.DDlMonitor.set_create(
                session.gui_name, ddl_job_id
            )
        else:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content='non-directory(s) for create',
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )


class AbsPnlAssetDccTextureManager(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = None
    DCC_SELECTION_CLS = None
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAssetDccTextureManager, self).__init__(session, *args, **kwargs)

    def set_variants_restore(self):
        self._create_data = []

    def set_all_setup(self):
        self._tab_view = prx_widgets.PrxTabView()
        self.set_widget_add(self._tab_view)

        s_a_0 = prx_widgets.PrxScrollArea()
        self._tab_view.set_item_add(
            s_a_0,
            name='dcc',
            icon_name_text='dcc',
        )

        e_p_0 = prx_widgets.PrxExpandedGroup()
        s_a_0.set_widget_add(e_p_0)
        h_s_0 = prx_widgets.PrxHSplitter()
        e_p_0.set_widget_add(h_s_0)
        e_p_0.set_name('textures')
        e_p_0.set_expanded(True)
        #
        self._filter_tree_view = prx_widgets.PrxTreeView()
        self._filter_tree_view.set_selection_use_single()
        self._filter_tree_view.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0]*(2.0/6.0)-32
        )
        h_s_0.set_widget_add(self._filter_tree_view)
        #
        self._tree_view = prx_widgets.PrxTreeView()
        h_s_0.set_widget_add(self._tree_view)
        self._tree_view.set_header_view_create(
            [('name', 4), ('color-space', 2), ('description', 2)],
            self.get_definition_window_size()[0]*(3.0/4.0)-32
        )
        h_s_0.set_stretches(
            [1, 3]
        )
        h_s_0.set_widget_hide_at(0)
        #
        self._texture_add_opt = utl_prx_operators.PrxStgObjTreeViewAddOpt(
            prx_tree_view=self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxStgObjTreeItem,
        )
        self._dcc_obj_add_opt = utl_prx_operators.PrxDccObjTreeViewAddOpt(
            prx_tree_view=self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxDccObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._tree_view_selection_opt = utl_prx_operators.PrxDccObjTreeViewSelectionOpt(
            prx_tree_view=self._tree_view,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )
        self._tree_view.set_item_select_changed_connect_to(
            self._tree_view_selection_opt.set_select
        )

        self._tree_view_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_view,
            prx_tree_view_tgt=self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        self.set_refresh_action_create(self._set_gui_refresh_)
        #
        self._options_prx_node = prx_widgets.PrxNode_('options')
        s_a_0.set_widget_add(self._options_prx_node)
        self._options_prx_node.set_ports_create_by_configure(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.set(
            'target.create_target', self._set_target_create_execute_
        )

        self._options_prx_node.set(
            'target.repath_to_source', self._set_repath_to_src_
        )
        self._options_prx_node.set(
            'target.repath_to_target', self._set_repath_to_tgt_
        )

        self._options_prx_node.set(
            'extra.search', self._set_search_execute_
        )

        self._options_prx_node.set(
            'extra.collection', self._set_collection_execute_
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )

        self._refresh_button = prx_widgets.PrxPressItem()
        self.set_button_add(self._refresh_button)
        self._refresh_button.set_name('refresh')
        self._refresh_button.set_press_clicked_connect_to(self._set_gui_refresh_)

        self.set_refresh_all()

    def set_refresh_all(self):
        self._set_gui_refresh_()

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = None

    def _set_dcc_objs_update_(self):
        self._dcc_objs = []

    def _set_gui_refresh_(self):
        self._set_dcc_texture_references_update_()
        self._set_dcc_objs_update_()
        method_args = [
            (self._set_gui_textures_refresh_, ()),
            (self._set_gui_textures_validator_, ())
        ]
        with utl_core.GuiProgressesRunner.create(maximum=len(method_args), label='gui processing') as g_p:
            for i_fnc, i_args in method_args:
                g_p.set_update()
                i_fnc(*i_args)

    def _set_gui_textures_refresh_(self):
        self._texture_add_opt.set_restore()
        self._tree_view_filter_opt.set_restore()

        if self._dcc_objs:
            with utl_core.GuiProgressesRunner.create(maximum=len(self._dcc_objs), label='gui texture showing') as g_p:
                for i_dcc_obj in self._dcc_objs:
                    g_p.set_update()
                    #
                    i_files = i_dcc_obj.get_file_objs()
                    if i_files:
                        j_keys = []
                        for j_file in i_files:
                            j_is_create, j_file_prx_item = self._texture_add_opt.set_prx_item_add_as(
                                j_file,
                                mode='list',
                                use_show_thread=True
                            )
                            if j_is_create is True:
                                j_file_prx_item.set_press_db_clicked_connect_to(
                                    self._set_detail_show_
                                )
                            #
                            if j_file_prx_item is not None:
                                i_dcc_obj_prx_item = self._dcc_obj_add_opt._set_prx_item_add_2_(
                                    i_dcc_obj,
                                    j_file_prx_item
                                )
                                i_dcc_obj.set_obj_gui(i_dcc_obj_prx_item)
                                j_keys.append('format.{}'.format(j_file.type_name))

    def _set_gui_textures_validator_(self):
        textures = self._texture_add_opt.get_files()
        c = len(textures)

        ext_tgt = self._options_prx_node.get('target.extension')

        repath_src_port = self._options_prx_node.get_port('target.repath_to_source')
        repath_src_statuses = [bsc_configure.ValidatorStatus.Normal]*c

        repath_tgt_port = self._options_prx_node.get_port('target.repath_to_target')
        repath_tgt_statuses = [bsc_configure.ValidatorStatus.Normal]*c
        with utl_core.GuiProgressesRunner.create(maximum=len(textures), label='gui texture validating') as g_p:
            for i_index, i_texture_any in enumerate(textures):
                g_p.set_update()

                i_texture_prx_item = i_texture_any.get_obj_gui()
                #
                i_descriptions = []

                i_directory_args = self._get_default_directory_args_(i_texture_any, ext_tgt)
                if i_directory_args:
                    i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(ext_tgt, i_directory_args)
                    if i_texture_src.ext == ext_tgt:
                        i_descriptions.append(
                            u'source is non-exists'
                        )
                        repath_src_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Error
                    else:
                        if i_texture_src.get_is_exists() is True:
                            if i_texture_src.get_is_writeable() is True:
                                if i_texture_any == i_texture_src:
                                    repath_src_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Correct
                            else:
                                repath_src_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Locked
                        else:
                            i_descriptions.append(
                                u'source is non-exists'
                            )
                            repath_src_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Error
                    #
                    if i_texture_tgt.get_is_exists() is True:
                        if i_texture_tgt.get_is_writeable() is True:
                            if i_texture_any == i_texture_tgt:
                                repath_tgt_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Correct
                        else:
                            repath_tgt_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Locked
                    else:
                        i_descriptions.append(
                            u'target is non-exists'
                        )
                        repath_tgt_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Error
                    #
                    if i_texture_src.get_is_exists() is True and i_texture_tgt.get_is_exists() is True:
                        if i_texture_src.get_timestamp_is_same_to(i_texture_tgt) is False:
                            i_descriptions.append(
                                u'target is changed'
                            )
                            repath_tgt_statuses[i_index] = i_texture_prx_item.ValidatorStatus.Warning

                i_texture_prx_item.set_name(
                    u', '.join(i_descriptions), 2
                )

                i_color_space = i_texture_src.get_best_color_space()
                i_texture_prx_item.set_name(i_color_space, 1)

                i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                    j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(
                        namespace=self.DCC_NAMESPACE
                    )
                    j_color_space = j_dcc_obj.get_color_space()
                    j_dcc_obj_prx_item.set_name(j_color_space, 1)
                    if i_descriptions:
                        self._tree_view_filter_opt.set_register(
                            j_dcc_obj_prx_item, [bsc_core.SPathMtd.set_quote_to(i) for i in i_descriptions]
                        )
                    else:
                        self._tree_view_filter_opt.set_register(
                            j_dcc_obj_prx_item, [bsc_core.SPathMtd.set_quote_to(i) for i in ['N/a']]
                        )

        repath_src_port.set_statuses(
            repath_src_statuses
        )
        repath_tgt_port.set_statuses(
            repath_tgt_statuses
        )
    @classmethod
    def _get_default_directory_args_(cls, texture_any, target_extension):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = texture_any.directory.path
            directory_path_tgt = texture_any.directory.get_as_new_name(target_format).path
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = (texture_any.directory.get_as_new_name('src')).path
            directory_path_tgt = texture_any.directory.path
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = texture_any.directory.path
        directory_path_tgt = texture_any.directory.path
        return directory_path_src, directory_path_tgt
    @classmethod
    def _get_default_directory_args_dst_(cls, texture_any, target_extension, target_directory):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = target_directory
        directory_path_tgt = target_directory
        return directory_path_src, directory_path_tgt
    @classmethod
    def _get_separate_directory_args_(cls, texture_any, target_extension):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = texture_any.directory.path
            directory_path_tgt = texture_any.directory.get_as_new_name(target_format).path
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = (texture_any.directory.get_as_new_name('src')).path
            directory_path_tgt = texture_any.directory.path
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = '{}/src'.format(texture_any.directory.path)
        directory_path_tgt = '{}/{}'.format(texture_any.directory.path, target_format)
        return directory_path_src, directory_path_tgt
    @classmethod
    def _get_separate_directory_args_dst_(cls, texture_any, target_extension, target_directory):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = '{}/src'.format(target_directory)
        directory_path_tgt = '{}/{}'.format(target_directory, target_format)
        return directory_path_src, directory_path_tgt

    def _set_target_create_data_update_(self, ext_tgt, force_enable):
        contents = []
        #
        self._create_data = []
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            with utl_core.GuiProgressesRunner.create(maximum=len(textures), label='gain texture create-data') as g_p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    g_p.set_update()
                    # ignore is locked
                    if i_texture_any.get_is_readable() is False:
                        continue
                    #
                    i_directory_args = self._get_default_directory_args_(i_texture_any, ext_tgt)
                    if i_directory_args:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(ext_tgt, i_directory_args)
                        if i_texture_src is not None:
                            i_texture_src_units = i_texture_src.get_exists_files_()
                            i_output_directory_path = i_texture_tgt.directory.path
                            for j_texture_src_unit in i_texture_src_units:
                                if force_enable is True:
                                    self._create_data.append(
                                        (j_texture_src_unit.path, i_output_directory_path)
                                    )
                                else:
                                    if j_texture_src_unit._get_unit_is_exists_as_tgt_ext_by_src_(
                                            j_texture_src_unit.path,
                                            ext_tgt=ext_tgt,
                                            search_directory_path=i_output_directory_path,
                                    ) is False:
                                        self._create_data.append(
                                            (j_texture_src_unit.path, i_output_directory_path)
                                        )
        else:
            contents.append(
                u'check one or more node and retry'
            )

        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def _set_target_create_by_data_(self, button, post_fnc=None):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            print '\n'.join(results)

        def status_update_at_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            for i_index, (i_file_path, i_output_directory_path) in enumerate(self._create_data):
                bsc_core.StorageMtd.set_directory_create(
                    i_output_directory_path
                )

                i_cmd = utl_dcc_objects.OsTexture._get_unit_tx_create_cmd_by_src_force_(
                    i_file_path,
                    search_directory_path=i_output_directory_path,
                )
                if button.get_is_stopped():
                    break
                #
                if i_cmd:
                    bsc_core.PrcCmdThread.set_wait()
                    i_t = bsc_core.PrcCmdThread.set_start(i_cmd, i_index)
                    i_t.status_changed.set_connect_to(status_update_at_fnc_)
                    i_t.finished.set_connect_to(finished_fnc_)
                else:
                    status_update_at_fnc_(
                        i_index, bsc_configure.Status.Completed
                    )
                    finished_fnc_(
                        i_index, bsc_configure.Status.Completed
                    )

        def quit_fnc_():
            button.set_stopped()
            #
            time.sleep(1)
            #
            t.quit()
            t.wait()
            t.deleteLater()

        contents = []
        if self._create_data:
            button.set_stopped(False)

            c = len(self._create_data)

            button.set_status(bsc_configure.Status.Started)
            button.set_initialization(c, bsc_configure.Status.Started)

            t = utl_gui_qt_core.QtMethodThread(self.widget)
            t.set_method_add(
                run_fnc_
            )
            t.start()
            if post_fnc is not None:
                t.run_finished.connect(
                    post_fnc
                )

            self.set_window_close_connect_to(quit_fnc_)
        else:
            button.set_restore()

            contents = [
                'non-texture(s) to create, you can click refresh and try again'
            ]

        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False
        else:
            return True

    def _set_target_create_execute_(self):
        force_enable = self._options_prx_node.get('target.create_force_enable')
        ext_tgt = self._options_prx_node.get('target.extension')
        button = self._options_prx_node.get_port('target.create_target')
        method_args = [
            (self._set_target_create_data_update_, (ext_tgt, force_enable)),
            (self._set_target_create_by_data_, (button, self._set_gui_refresh_))
        ]
        with utl_core.GuiProgressesRunner.create(maximum=len(method_args), label='create texture by data') as g_p:
            for i_fnc, i_args in method_args:
                g_p.set_update()
                #
                i_result = i_fnc(*i_args)
                if i_result is False:
                    break

    def _set_repath_to_src_(self):
        contents = []
        ext_tgt = self._options_prx_node.get('target.extension')
        #
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            with utl_core.GuiProgressesRunner.create(maximum=len(textures), label='repath texture to source') as g_p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    g_p.set_update()

                    i_texture_prx_item = i_texture_any.get_obj_gui()

                    i_directory_args = self._get_default_directory_args_(i_texture_any, ext_tgt)
                    if i_directory_args:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(ext_tgt, i_directory_args)
                        if i_texture_src is not None:
                            if i_texture_src.get_is_exists() is True:
                                i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                                i_port_path = i_texture_any.get_relevant_dcc_port_path()
                                for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                                    if j_dcc_obj_prx_item.get_is_checked() is True:
                                        j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(
                                            namespace=self.DCC_NAMESPACE
                                        )
                                        #
                                        self._dcc_texture_references.set_obj_repath_to(
                                            j_dcc_obj, i_port_path, i_texture_src.path
                                        )
                #
                self._set_gui_refresh_()
                return True
        else:
            contents.append(
                u'check one or more node and retry'
            )

        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def _set_repath_to_tgt_(self):
        contents = []
        #
        ext_tgt = self._options_prx_node.get('target.extension')
        #
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            with utl_core.GuiProgressesRunner.create(maximum=len(textures), label='repath texture to target') as g_p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    g_p.set_update()

                    i_texture_prx_item = i_texture_any.get_obj_gui()

                    i_directory_args = self._get_default_directory_args_(i_texture_any, ext_tgt)
                    if i_directory_args:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(ext_tgt, i_directory_args)
                        if i_texture_tgt.get_is_exists() is True:
                            i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                            i_port_path = i_texture_any.get_relevant_dcc_port_path()
                            for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                                if j_dcc_obj_prx_item.get_is_checked() is True:
                                    j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                                    #
                                    self._dcc_texture_references.set_obj_repath_to(
                                        j_dcc_obj, i_port_path, i_texture_tgt.path
                                    )
                #
                self._set_gui_refresh_()
                return True
        else:
            contents.append(
                u'check one or more node and retry'
            )

        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def _set_search_run_(self, window, directory, below_enable, ignore_exists, ignore_name_case, ignore_ext_case, ignore_ext):
        if directory:
            textures = self._texture_add_opt.get_checked_files()
            if textures:
                search_opt = bsc_core.StgFileSearchOpt(
                    ignore_name_case=ignore_ext_case,
                    ignore_ext_case=ignore_name_case,
                    ignore_ext=ignore_ext
                )
                search_opt.set_search_directory_append(directory, below_enable)
                with window.set_progress_create(maximum=len(textures)) as p:
                    for i_texture_any in self._texture_add_opt.get_checked_files():
                        p.set_update()
                        #
                        if ignore_exists is True:
                            if i_texture_any.get_is_exists() is True:
                                continue

                        if i_texture_any.directory.path == directory:
                            continue

                        i_texture_prx_item = i_texture_any.get_obj_gui()
                        i_result = search_opt.get_result(i_texture_any.path)
                        if i_result:
                            i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                            i_port_path = i_texture_any.get_relevant_dcc_port_path()
                            for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                                if j_dcc_obj_prx_item.get_is_checked() is True:
                                    j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                                    #
                                    self._dcc_texture_references.set_obj_repath_to(
                                        j_dcc_obj, i_port_path, i_result
                                    )

                self._set_gui_refresh_()

    def _set_search_execute_(self):
        def yes_fnc_():
            self._set_search_run_(w, **w.get_options_as_kwargs())

        w = utl_core.DialogWindow.set_create(
            self._session.gui_name,
            sub_label='Search',
            content=u'choose or entry a directory, press "Confirm" to continue',
            status=utl_core.DialogWindow.ValidatorStatus.Active,
            #
            options_configure=self._session.configure.get('build.node.extra_search'),
            #
            yes_label='Confirm',
            #
            yes_method=yes_fnc_,
            #
            no_visible=False,
            show=False,
            #
            window_size=(480, 480),
            #
            parent=self.widget,
        )

        w.set_window_show()

    def _set_collection_run_(self, window, directory, scheme, mode, copy_or_link_enable, replace_enable, repath_enable, target_extension):
        if directory:
            textures = self._texture_add_opt.get_checked_files()
            if textures:
                with window.set_progress_create(maximum=len(textures)) as p:
                    for i_texture_any in self._texture_add_opt.get_checked_files():
                        p.set_update()
                        #
                        if i_texture_any.directory.path == directory:
                            continue

                        if i_texture_any.get_is_readable() is False:
                            continue

                        i_texture_prx_item = i_texture_any.get_obj_gui()

                        if scheme == 'default':
                            i_directory_args = self._get_default_directory_args_(
                                i_texture_any, target_extension
                            )
                            i_directory_args_dst = self._get_default_directory_args_dst_(
                                i_texture_any, target_extension, directory
                            )
                        elif scheme == 'separate':
                            i_directory_args = self._get_separate_directory_args_(
                                i_texture_any, target_extension
                            )
                            i_directory_args_dst = self._get_separate_directory_args_dst_(
                                i_texture_any, target_extension, directory
                            )
                        else:
                            raise TypeError()

                        if i_directory_args and i_directory_args_dst:
                            i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(
                                target_extension, i_directory_args
                            )
                            i_directory_src_dst, i_directory_tgt_dst = i_directory_args_dst

                            if copy_or_link_enable is True:
                                if mode == 'copy':
                                    [j.set_copy_to_directory(i_directory_src_dst, replace=replace_enable) for j in i_texture_src.get_exists_files_()]
                                    [j.set_copy_to_directory(i_directory_tgt_dst, replace=replace_enable) for j in i_texture_tgt.get_exists_files_()]
                                #
                                elif mode == 'link':
                                    [j.set_link_to_directory(i_directory_src_dst, replace=replace_enable) for j in i_texture_src.get_exists_files_()]
                                    [j.set_link_to_directory(i_directory_tgt_dst, replace=replace_enable) for j in i_texture_tgt.get_exists_files_()]
                            #
                            if repath_enable is True:
                                i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                                i_port_path = i_texture_any.get_relevant_dcc_port_path()
                                for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                                    if j_dcc_obj_prx_item.get_is_checked() is True:
                                        j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                                        #
                                        if i_texture_any == i_texture_src:
                                            i_texture_any_dst = i_texture_src.get_target_file(
                                                i_directory_src_dst
                                            )
                                        else:
                                            i_texture_any_dst = i_texture_tgt.get_target_file(
                                                i_directory_tgt_dst
                                            )
                                        #
                                        if i_texture_any_dst.get_is_exists() is True:
                                            self._dcc_texture_references.set_obj_repath_to(
                                                j_dcc_obj, i_port_path, i_texture_any_dst.path
                                            )
                #
                self._set_gui_refresh_()
                return True

    def _set_collection_execute_(self):
        def yes_fnc_():
            self._set_collection_run_(w, **w.get_options_as_kwargs())

        w = utl_core.DialogWindow.set_create(
            self._session.gui_name,
            sub_label='Collection',
            content=u'choose or entry a directory, press "Confirm" to continue',
            status=utl_core.DialogWindow.ValidatorStatus.Active,
            #
            options_configure=self._session.configure.get('build.node.extra_collection'),
            #
            yes_label='Confirm',
            #
            yes_method=yes_fnc_,
            #
            no_visible=False,
            show=False,
            #
            window_size=(480, 480),
            #
            parent=self.widget,
        )

        w.set_window_show()

    def _set_detail_show_(self, item, column):
        texture = self._texture_add_opt.get_file(item)
        w = utl_core.DialogWindow.set_create(
            self._session.gui_name,
            window_size=(512, 512),
            #
            yes_visible=False, no_visible=False,
            tip_visible=False,
            show=False,
            #
            parent=self.widget
        )

        v = prx_widgets.PrxImageView()
        w.set_customize_widget_add(v)

        v.set_textures([texture])

        w.set_window_show()