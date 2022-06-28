# coding:utf-8
import collections

import functools

import time

import copy

from lxbasic import bsc_configure, bsc_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxobj import core_objects

import lxbasic.objects as bsc_objects

import lxutil_gui.proxy.operators as utl_prx_operators

import lxsession.commands as ssn_commands

import lxresolver.commands as rsv_commands

from lxsession import ssn_core

import lxsession.objects as ssn_objects

import lxutil_gui.proxy.operators as prx_operators

from lxutil_gui import utl_gui_core

import lxresolver.methods as rsv_methods


class TextureConfigure(object):
    def __init__(self, file_path):
        self._file_path_opt = bsc_core.StorageFileOpt(file_path)
        if self._file_path_opt.get_is_exists() is True:
            self._dict = self._file_path_opt.set_read()
        else:
            self._dict = collections.OrderedDict()
            self.set_update()

    def set_version(self, scene_file_path, version):
        key = bsc_core.StoragePathMtd.set_map_to_linux(scene_file_path)
        self._dict[key] = version
        self.set_update()

    def get_current_version(self, scene_file_path):
        key = bsc_core.StoragePathMtd.set_map_to_linux(scene_file_path)
        if key in self._dict:
            return self._dict[key]

    def set_update(self):
        self._file_path_opt.set_write(
            self._dict
        )


class AbsTextureWorkspace(object):
    def __init__(self, rsv_task):
        self._resolver = rsv_commands.get_resolver()

        self._rsv_task = rsv_task

        self._work_texture_base_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-base-dir'
        )

        self._work_texture_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-dir'
        )
        self._work_texture_src_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-src-dir'
        )
        self._work_texture_tx_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-tx-dir'
        )
        self._work_texture_configure_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-workspace-file'
        )

        self._configure_file_path = self.get_configure_file_path()
        self._configure_file_opt = bsc_core.StorageFileOpt(self._configure_file_path)

    def set_create_at(self, layer, version):
        if version == 'new':
            version = self._work_texture_directory_rsv_unit.get_new_version()
        #
        self.set_layer(layer)
        self.set_version(version)
        #
        bsc_core.StoragePathMtd.set_directory_create(
            self.get_directory_path_at(layer, version)
        )
        bsc_core.StoragePathMtd.set_directory_create(
            self.get_src_directory_path_at(layer, version)
        )
        bsc_core.StoragePathMtd.set_directory_create(
            self.get_tgt_directory_path_at(layer, version)
        )

    def set_lock_at(self, layer, version):
        directory_path = self.get_directory_path_at(layer, version)
        rsv_methods.PathGroupPermission(
            directory_path
        ).set_read_only(
            'srf_grp'
        )
        rsv_methods.PathGroupPermission(
            directory_path
        ).set_read_only(
            'td_grp'
        )

    def get_new_version(self):
        return self._work_texture_directory_rsv_unit.get_new_version()

    def set_load(self, layer, version):
        self.set_layer(layer)
        self.set_version(version)

    def get_configure_file_path(self):
        result = self._work_texture_configure_file_rsv_unit.get_result()
        if result is None:
            result = self._work_texture_configure_file_rsv_unit.get_result(version='new')
        return result

    def get_directory_path_at(self, layer, version):
        return self._work_texture_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(layer=layer)
        )

    def get_src_directory_path_at(self, layer, version):
        return self._work_texture_src_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(layer=layer)
        )

    def get_tgt_directory_path_at(self, layer, version):
        return self._work_texture_tx_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(layer=layer)
        )

    def get_current_directory_path(self):
        layer = self.get_current_layer()
        version = self.get_current_version()
        return self.get_directory_path_at(layer, version)

    def get_current_src_directory_path(self):
        layer = self.get_current_layer()
        version = self.get_current_version()
        return self.get_src_directory_path_at(layer, version)

    def get_current_tx_directory_path(self):
        layer = self.get_current_layer()
        version = self.get_current_version()
        return self.get_tgt_directory_path_at(layer, version)

    def get_data(self):
        dict_ = collections.OrderedDict()
        results = self._work_texture_directory_rsv_unit.get_result(version='all')
        if results:
            for i_result in results:
                i_properties = self._work_texture_directory_rsv_unit.get_properties_by_result(
                    i_result
                )
                i_layer = i_properties.get('layer')
                i_version = i_properties.get('version')
                dict_.setdefault(i_layer, []).append(i_version)
            for k, v in dict_.items():
                dict_.setdefault(
                    k, []
                ).append('new')
        else:
            dict_.setdefault(
                'main', []
            ).append('new')
        return dict_

    def get_used_data(self):
        dict_ = collections.OrderedDict()
        results = self._work_texture_directory_rsv_unit.get_result(version='all')
        if results:
            for i_result in results:
                is_locked = self.get_is_read_only(i_result)
                i_properties = self._work_texture_directory_rsv_unit.get_properties_by_result(
                    i_result
                )
                i_layer = i_properties.get('layer')
                i_version = i_properties.get('version')
                if i_layer not in dict_:
                    dict_[i_layer] = []
                if is_locked is False:
                    dict_.setdefault(i_layer, []).append(i_version)
            #
            for k, v in dict_.items():
                if len(v) == 0:
                    dict_.setdefault(
                        k, []
                    ).append('new')
        else:
            dict_.setdefault(
                'main', []
            ).append('new')
        return dict_

    def get_current_layer(self):
        return self._get_dcc_layer_()

    def set_layer(self, layer):
        self._set_dcc_layer_(layer)

    def set_version(self, version):
        self._set_dcc_version_(version)

    def get_current_version(self):
        return self._get_dcc_version_()

    def _set_dcc_version_(self, version):
        raise NotImplementedError()

    def _get_dcc_version_(self):
        raise NotImplementedError()

    def _set_dcc_layer_(self, layer):
        raise NotImplementedError()

    def _get_dcc_layer_(self):
        raise NotImplementedError()

    def _set_dcc_directory_(self, directory):
        pass

    def get_base_directory_path(self):
        result = self._work_texture_base_directory_rsv_unit.get_result()
        if result is None:
            result = self._work_texture_base_directory_rsv_unit.get_result(version='new')
        return result

    def get_kwargs_by_directory_path(self, directory_path):
        for i_rsv_unit in [
            self._work_texture_src_directory_rsv_unit,
            self._work_texture_tx_directory_rsv_unit
        ]:
            i_properties = i_rsv_unit.get_properties_by_result(directory_path)
            if i_properties:
                return i_properties.get_value()

    def get_search_directory_args(self, directory_path):
        kwargs = self.get_kwargs_by_directory_path(directory_path)
        if kwargs:
            kwargs_0, kwargs_1 = copy.copy(kwargs), copy.copy(kwargs)
            kwargs_0['keyword'], kwargs_1['keyword'] = 'asset-work-texture-src-dir', 'asset-work-texture-tx-dir'
            return self._resolver.get_result(**kwargs_0), self._resolver.get_result(**kwargs_1)
    @classmethod
    def get_is_read_only(cls, directory_path):
        return rsv_methods.PathGroupPermission(
            directory_path
        ).get_is_read_only(
            'srf_grp'
        )

    def get_current_is_read_only(self):
        return self.get_is_read_only(
            self.get_current_directory_path()
        )

    def get_is_read_only_at(self, layer, version):
        directory_path = self.get_directory_path_at(layer, version)
        return self.get_is_read_only(directory_path)


class AbsWorkTextureManager(prx_widgets.PrxToolWindow):
    OPTION_HOOK_KEY = None
    DCC_NAMESPACE = None

    DCC_SELECTION_CLS = None

    TEXTURE_WORKSPACE_CLS = None
    def __init__(self, session, *args, **kwargs):
        super(AbsWorkTextureManager, self).__init__(*args, **kwargs)
        self._qt_thread_enable = bsc_core.EnvironMtd.get_qt_thread_enable()
        #
        self._session = session
        self._session.set_configure_reload()
        # noinspection PyUnresolvedReferences
        self._gui_configure = self._session.gui_configure
        self._build_configure = self._session.configure.get_content('build')
        if self._session.get_rez_beta() is True:
            self.set_window_title('[BETA] {}'.format(self._gui_configure.get('name')))
        else:
            self.set_window_title(self._gui_configure.get('name'))
        self.set_definition_window_size(self._gui_configure.get('size'))

        self._dcc_texture_references = None
        self._dcc_objs = []

        self._create_data = []

        self._is_disable = False

        self._file_path = None
        self._texture_configure = None

        self._dcc_workspace_version = None

        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_tool_panel_setup_(self):
        self._viewer_group = prx_widgets.PrxExpandedGroup()
        self.set_widget_add(self._viewer_group)
        self._viewer_group.set_name('textures')
        self._viewer_group.set_expanded(True)
        #
        self._tree_view = prx_widgets.PrxTreeView()
        self._viewer_group.set_widget_add(self._tree_view)
        self._tree_view.set_header_view_create(
            [('name', 4), ('description', 2)],
            self.get_definition_window_size()[0] - 32
        )
        self._tree_view.set_single_selection()
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

        self._options_prx_node = prx_widgets.PrxNode_('options')
        self.set_widget_add(self._options_prx_node)
        self._options_prx_node.set_ports_create_by_configure(
            self._session.configure.get('build.node.options'),
        )

        # self._options_prx_node.get_port(
        #     'workspace.version'
        # ).set_changed_connect_to(
        #     self._set_workspace_directory_update_
        # )

        self._options_prx_node.set(
            'workspace.new_version', self._set_workspace_version_new_
        )

        self._options_prx_node.set(
            'texture.collection_to_current_version', self._set_textures_collection_and_repath_
        )

        self._options_prx_node.set(
            'texture.repath_to_src', self._set_textures_repath_to_src_
        )

        self._options_prx_node.set(
            'texture.repath_to_tx', self._set_textures_repath_to_tgt_
        )

        self._options_prx_node.set(
            'texture.create_tx', self._set_tx_create_
        )

        self._options_prx_node.set(
            'refresh', self._set_gui_refresh_
        )

        self._set_collapse_update_()

        self.set_window_loading_end()

        self.set_refresh_all()

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = None

    def _set_dcc_objs_update_(self):
        self._dcc_objs = []

    def _set_dcc_scene_update_(self):
        self._file_path = None

    def _set_texture_workspace_update_(self):
        self._texture_workspace = self.TEXTURE_WORKSPACE_CLS(self._rsv_task)

        current_layer = self._texture_workspace.get_current_layer()
        current_version = self._texture_workspace.get_current_version()

        if current_layer is None:
            current_layer, current_version = self._get_workspace_install_args_()
        else:
            self._set_workspace_version_unlocked_(current_layer, current_version)
            current_version = self._texture_workspace.get_current_version()

        self._options_prx_node.set(
            'workspace.layer', current_layer
        )
        self._options_prx_node.set(
            'workspace.version', current_version
        )

        self._options_prx_node.set(
            'resolver.task', self._rsv_task.path
        )
        #
        self._set_workspace_directory_update_()

    def _get_workspace_install_args_(self):
        def update_version_fnc_():
            _layer = n.get('layer')
            _versions = c.get(_layer)
            n.set('version', _versions)

        def yes_fnc_():
            _layer = n.get('layer')
            _version = n.get('version')
            if _version == 'new':
                self._texture_workspace.set_create_at(
                    _layer, _version
                )
            else:
                self._texture_workspace.set_load(
                    _layer, _version
                )

        data = self._texture_workspace.get_used_data()

        c = bsc_objects.Configure(value=data)

        w = utl_core.DialogWindow.set_create(
            self._session.gui_name,
            content='workspace is not install, choose "layer" and "version", press "confirm" to continue',
            status=utl_core.DialogWindow.ValidatorStatus.Warning,
            #
            options_configure=self._build_configure.get('node.dialog_0'),
            #
            yes_label='confirm',
            #
            yes_method=yes_fnc_,
            #
            no_visible=False,
            show=False
        )

        n = w.get_options_node()

        layers = c.get_top_keys()

        n.set('layer', layers)
        n.set('layer', layers[0])
        main_versions = c.get('main')
        n.set('version', main_versions)
        n.set('version', main_versions[0])

        n.get_port('layer').set_changed_connect_to(update_version_fnc_)

        w.set_window_show()

        result = w.get_result()
        kwargs = w.get_kwargs()
        if result is True:
            return kwargs['layer'], kwargs['version']
        else:
            self._is_disable = True
            self.set_window_close()
            return None, None

    def _set_workspace_version_unlocked_(self, layer, version):
        def yes_fnc_():
            _layer = n.get('layer')
            _version = n.get('version')
            if _version == 'new':
                self._texture_workspace.set_create_at(
                    _layer, _version
                )
            else:
                self._texture_workspace.set_load(
                    _layer, _version
                )

        is_locked = self._texture_workspace.get_is_read_only_at(layer, version)
        if is_locked is True:
            data = self._texture_workspace.get_used_data()

            c = bsc_objects.Configure(value=data)

            w = utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content='current version "{}" is locked, choose "layer" and "version", press "confirm" to continue'.format(
                    version
                ),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                options_configure=self._build_configure.get('node.dialog_0'),
                #
                yes_label='confirm',
                #
                yes_method=yes_fnc_,
                #
                no_visible=False,
                show=False
            )

            n = w.get_options_node()

            n.set('layer', [layer])
            n.set('layer', layer)
            main_versions = c.get(layer)
            n.set('version', main_versions)
            n.set('version', main_versions[0])

            w.set_window_show()

            result = w.get_result()
            kwargs = w.get_kwargs()
            if result is True:
                pass
            else:
                self._is_disable = True
                self.set_window_close()

    def _get_workspace_version_new_(self, layer, version):
        def yes_fnc_():
            self._texture_workspace.set_lock_at(
                layer, version
            )
            _layer = n.get('layer')
            _version = n.get('version')
            self._texture_workspace.set_create_at(
                _layer, _version
            )
            _collection_enable = n.get('collection_enable')

            if _collection_enable is True:
                self._set_textures_collection_and_repath_()

        w = utl_core.DialogWindow.set_create(
            self._session.gui_name,
            content='create a new version, press "confirm" to continue',
            status=utl_core.DialogWindow.ValidatorStatus.Warning,
            #
            options_configure=self._build_configure.get('node.dialog_2'),
            #
            yes_label='confirm',
            #
            yes_method=yes_fnc_,
            #
            no_visible=False,
            show=False
        )

        n = w.get_options_node()

        n.set('layer', [layer])
        n.set('layer', layer)
        n.set('version', ['new'])
        n.set('version', 'new')

        w.set_window_show()

        result = w.get_result()

    def _set_workspace_directory_update_(self):
        layer = self._options_prx_node.get(
            'workspace.layer'
        )
        version = self._options_prx_node.get(
            'workspace.version'
        )
        self._options_prx_node.set(
            'workspace.directory.base', self._texture_workspace.get_base_directory_path()
        )
        self._options_prx_node.set(
            'workspace.directory.src', self._texture_workspace.get_src_directory_path_at(
                layer,
                version
            )
        )
        self._options_prx_node.set(
            'workspace.directory.tx', self._texture_workspace.get_tgt_directory_path_at(
                layer,
                version
            )
        )

    def _set_workspace_version_new_(self):
        layer = self._texture_workspace.get_current_layer()
        pre_version = self._texture_workspace.get_current_version()
        self._get_workspace_version_new_(layer, pre_version)
        current_version = self._texture_workspace.get_current_version()
        if pre_version != current_version:
            # sleep wait for locked
            time.sleep(2)
            self.set_refresh_all()

    def set_refresh_all(self):
        self._set_dcc_scene_update_()
        if self._file_path is not None:
            self._resolver = rsv_commands.get_resolver()
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
                self._file_path
            )
            if self._rsv_scene_properties:
                self._rsv_task = self._resolver.get_rsv_task_by_any_file_path(
                    self._file_path
                )
                self._rsv_entity = self._rsv_task.get_rsv_entity()

                self._set_texture_workspace_update_()

                self._set_gui_refresh_()

    def _set_gui_refresh_(self):
        if self._is_disable is False:
            self._set_dcc_texture_references_update_()
            self._set_dcc_objs_update_()
            #
            self._set_gui_texture_refresh_()

    def _set_version_new_(self):
        pass

    def _set_collapse_update_(self):
        collapse_dict = {
            'options': self._options_prx_node,
        }
        for i_k, i_v in collapse_dict.items():
            i_c = self._build_configure.get(
                'node_collapse.{}'.format(i_k)
            ) or []
            if i_c:
                for i in i_c:
                    i_v.get_port(
                        i.replace('/', '.')
                    ).set_expanded(False)

    def _set_gui_texture_refresh_(self):
        self._texture_add_opt.set_restore()

        if self._dcc_objs:
            with utl_core.gui_progress(maximum=len(self._dcc_objs)) as g_p:
                for i_dcc_obj in self._dcc_objs:
                    g_p.set_update()

                    i_files = i_dcc_obj.get_file_objs()
                    if i_files:
                        for j_file in i_files:
                            j_is_create, j_file_prx_item = self._texture_add_opt.set_prx_item_add_as(
                                j_file,
                                mode='list',
                                use_show_thread=True
                            )
                            if j_file_prx_item is not None:
                                i_dcc_prx_item = self._dcc_obj_add_opt._set_prx_item_add_2_(
                                    i_dcc_obj,
                                    j_file_prx_item
                                )
                                i_dcc_obj.set_obj_gui(i_dcc_prx_item)

        self._set_gui_texture_validator_()

    def _set_gui_texture_validator_(self):
        textures = self._texture_add_opt.get_files()
        c = len(textures)
        src_texture_directory_path = self._texture_workspace.get_current_src_directory_path()
        tgt_texture_directory_path = self._texture_workspace.get_current_tx_directory_path()

        collection_port = self._options_prx_node.get_port('texture.collection_to_current_version')
        collection_statuses = [bsc_configure.ValidatorStatus.Normal]*c

        repath_src_port = self._options_prx_node.get_port('texture.repath_to_src')
        repath_src_statuses = [bsc_configure.ValidatorStatus.Normal]*c

        repath_tgt_port = self._options_prx_node.get_port('texture.repath_to_tx')
        repath_tgt_statuses = [bsc_configure.ValidatorStatus.Normal]*c
        for i_index, i_texture_any in enumerate(textures):
            i_prx_item = i_texture_any.get_obj_gui()
            #
            i_descriptions = []
            #
            i_texture_any_directory_path = i_texture_any.directory.path
            i_directory_args = self._texture_workspace.get_search_directory_args(
                i_texture_any_directory_path
            )
            if i_directory_args:
                i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx_by_directory_args(i_directory_args)
            else:
                i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx()
            #
            if i_texture_src is None:
                i_descriptions.append(
                    u'src is non-exists'
                )
                repath_src_statuses[i_index] = i_prx_item.ValidatorStatus.Error
            else:
                if i_texture_any == i_texture_src:
                    repath_src_statuses[i_index] = i_prx_item.ValidatorStatus.Correct
                    #
                    if i_texture_any_directory_path == src_texture_directory_path:
                        collection_statuses[i_index] = bsc_configure.ValidatorStatus.Correct
                    else:
                        if i_directory_args:
                            collection_statuses[i_index] = bsc_configure.ValidatorStatus.Locked
                            i_descriptions.append(
                                u'version is locked'
                            )
                        else:
                            collection_statuses[i_index] = bsc_configure.ValidatorStatus.Warning
                            i_descriptions.append(
                                u'src is non-collection'
                            )
                else:
                    repath_src_statuses[i_index] = i_prx_item.ValidatorStatus.Warning

            if i_texture_tgt.get_is_exists() is False:
                i_descriptions.append(
                    u'tx is non-exists'
                )
                repath_tgt_statuses[i_index] = i_prx_item.ValidatorStatus.Error
            else:
                if i_texture_any == i_texture_tgt:
                    repath_tgt_statuses[i_index] = i_prx_item.ValidatorStatus.Correct
                    #
                    if i_texture_any_directory_path == tgt_texture_directory_path:
                        collection_statuses[i_index] = bsc_configure.ValidatorStatus.Correct
                    else:
                        if i_directory_args:
                            collection_statuses[i_index] = bsc_configure.ValidatorStatus.Locked
                            i_descriptions.append(
                                u'version is locked'
                            )
                        else:
                            collection_statuses[i_index] = bsc_configure.ValidatorStatus.Warning
                            i_descriptions.append(
                                u'tx is non-collection'
                            )
                else:
                    repath_tgt_statuses[i_index] = i_prx_item.ValidatorStatus.Warning

            if i_texture_src is not None and i_texture_tgt is not None:
                if i_texture_src.get_is_exists_as_tx(i_texture_tgt.directory.path) is False:
                    i_descriptions.append(
                        u'tx need update'
                    )
                    repath_tgt_statuses[i_index] = i_prx_item.ValidatorStatus.Error

            i_prx_item.set_name(
                u', '.join(i_descriptions), 1
            )

            if i_descriptions:
                i_prx_item.set_state(
                    utl_gui_core.State.WARNING, 1
                )
            else:
                i_prx_item.set_state(
                    utl_gui_core.State.NORMAL, 1
                )

        collection_port.set_statuses(
            collection_statuses
        )
        repath_src_port.set_statuses(
            repath_src_statuses
        )
        repath_tgt_port.set_statuses(
            repath_tgt_statuses
        )

    def _set_textures_collection_and_repath_(self):
        collection_replace_enable = self._options_prx_node.get('texture.collection_replace_enable')
        collection_locked_enable = self._options_prx_node.get('texture.collection_locked_enable')
        # base
        base_texture_directory_path = self._texture_workspace.get_base_directory_path()
        # src + tx
        src_texture_directory_path = self._texture_workspace.get_current_src_directory_path()
        tgt_texture_directory_path = self._texture_workspace.get_current_tx_directory_path()
        textures = self._texture_add_opt.get_checked_files()
        with utl_core.gui_progress(maximum=len(textures)) as g_p:
            for i_texture_any in self._texture_add_opt.get_checked_files():
                g_p.set_update()
                #
                i_texture_prx_item = i_texture_any.get_obj_gui()
                i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                #
                i_texture_any_directory_path = i_texture_any.directory.path
                i_directory_args = self._texture_workspace.get_search_directory_args(
                    i_texture_any_directory_path
                )
                # check is in used version
                if i_directory_args:
                    i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx_by_directory_args(i_directory_args)
                    if collection_locked_enable is False:
                        continue
                else:
                    i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx()
                #
                if i_texture_src is not None:
                    i_texture_src.set_copy_as_src(
                        directory_path_src=base_texture_directory_path,
                        directory_path_tgt=src_texture_directory_path,
                        replace=collection_replace_enable
                    )
                #
                if i_texture_tgt is not None:
                    i_texture_tgt.set_copy_as_src(
                        directory_path_src=base_texture_directory_path,
                        directory_path_tgt=tgt_texture_directory_path,
                        replace=collection_replace_enable
                    )
                #
                i_port_path = i_texture_any.get_relevant_dcc_port_path()
                i_texture_path_any_new = None
                # get new path
                if i_texture_any.get_ext_is_tx():
                    if i_texture_tgt is not None:
                        i_texture_path_any_new = bsc_core.StorageFileOpt(
                            i_texture_tgt.path
                        ).set_directory_repath_to(tgt_texture_directory_path).get_path()
                else:
                    if i_texture_src is not None:
                        i_texture_path_any_new = bsc_core.StorageFileOpt(
                            i_texture_src.path
                        ).set_directory_repath_to(src_texture_directory_path).get_path()
                # repath node path
                for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                    j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                    #
                    self._dcc_texture_references.set_obj_repath_to(
                        j_dcc_obj, i_port_path, i_texture_path_any_new
                    )

        self._set_gui_refresh_()

    def _set_textures_repath_to_src_(self):
        textures = self._texture_add_opt.get_checked_files()
        with utl_core.gui_progress(maximum=len(textures)) as g_p:
            for i_texture_any in self._texture_add_opt.get_checked_files():
                g_p.set_update()
                #
                i_texture_prx_item = i_texture_any.get_obj_gui()
                i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                #
                i_texture_any_directory_path = i_texture_any.directory.path
                i_directory_args = self._texture_workspace.get_search_directory_args(
                    i_texture_any_directory_path
                )
                if i_directory_args:
                    i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx_by_directory_args(i_directory_args)
                else:
                    i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx()

                i_port_path = i_texture_any.get_relevant_dcc_port_path()

                if i_texture_src is not None:
                    for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                        j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                        self._dcc_texture_references.set_obj_repath_to(
                            j_dcc_obj, i_port_path, i_texture_src.path
                        )

        self._set_gui_refresh_()

    def _set_textures_repath_to_tgt_(self):
        textures = self._texture_add_opt.get_checked_files()
        with utl_core.gui_progress(maximum=len(textures)) as g_p:
            for i_texture_any in self._texture_add_opt.get_checked_files():
                g_p.set_update()
                #
                i_texture_prx_item = i_texture_any.get_obj_gui()
                i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                #
                i_texture_any_directory_path = i_texture_any.directory.path
                i_directory_args = self._texture_workspace.get_search_directory_args(
                    i_texture_any_directory_path
                )
                if i_directory_args:
                    i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx_by_directory_args(i_directory_args)
                else:
                    i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx()

                i_port_path = i_texture_any.get_relevant_dcc_port_path()

                if i_texture_tgt is not None:
                    for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                        j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                        self._dcc_texture_references.set_obj_repath_to(
                            j_dcc_obj, i_port_path, i_texture_tgt.path
                        )

        self._set_gui_refresh_()
    #
    def _set_tx_create_data_update_(self, force_enable):
        self._create_data = []

        contents = []
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            with utl_core.gui_progress(maximum=len(textures)) as g_p:
                for i_texture_any in textures:
                    g_p.set_update()
                    #
                    i_texture_any_directory_path = i_texture_any.directory.path
                    i_directory_args = self._texture_workspace.get_search_directory_args(
                        i_texture_any_directory_path
                    )
                    if i_directory_args:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx_by_directory_args(i_directory_args)
                    else:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_tx()
                    #
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
                                    ext_tgt=j_texture_src_unit.TX_EXT,
                                    search_directory_path=i_output_directory_path,
                                ) is False:
                                    self._create_data.append(
                                        (j_texture_src_unit.path, i_output_directory_path)
                                    )
        else:
            contents = [
                'non-texture(s) to converted, you can click refresh and try again'
            ]
        #
        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            return False
        else:
            return True

    def _set_tx_create_by_data_(self, button):
        def finished_fnc_(index, status):
            button.set_finished_at(index, status)
            # self._set_gui_refresh_()

        def status_update_at_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            for i_index, (i_file_path, i_output_directory_path) in enumerate(self._create_data):
                bsc_core.StoragePathMtd.set_directory_create(
                    i_output_directory_path
                )

                i_cmd = utl_dcc_objects.OsTexture._get_unit_tx_create_cmd_by_src__(
                    i_file_path,
                    search_directory_path=i_output_directory_path,
                )
                if button.get_is_stopped():
                    break
                #
                if i_cmd:
                    bsc_core.CmdSubProcessThread.set_wait()
                    i_t = bsc_core.CmdSubProcessThread.set_start(i_cmd, i_index)
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

            button.set_status(bsc_configure.Status.Waiting)
            button.set_initialization(c, bsc_configure.Status.Waiting)

            t = utl_gui_qt_core.QtMethodThread(self.widget)
            t.set_method_add(
                run_fnc_
            )
            t.start()

            t.run_finished.connect(
                self._set_gui_refresh_
            )

            self.set_window_close_connect_to(quit_fnc_)
        else:
            button.set_restore()

            contents = [
                'non-texture(s) to converted, you can click refresh and try again'
            ]

        if contents:
            utl_core.DialogWindow.set_create_at(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            return False
        else:
            return True

    def _set_tx_create_(self):
        force_enable = self._options_prx_node.get('texture.create_tx_force_enable')
        button = self._options_prx_node.get_port('texture.create_tx')

        method_args = [
            (self._set_tx_create_data_update_, (force_enable, )),
            (self._set_tx_create_by_data_, (button,))
        ]
        with utl_core.gui_progress(maximum=len(method_args)) as g_p:
            for i_fnc, i_args in method_args:
                g_p.set_update()
                i_result = i_fnc(*i_args)
                if i_result is False:
                    break
