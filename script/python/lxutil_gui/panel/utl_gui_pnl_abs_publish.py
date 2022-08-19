# coding:utf-8
import collections

import time

import copy

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

from lxutil_gui import utl_gui_configure


class AbsDccValidatorOpt(object):
    DCC_NAMESPACE = None
    DCC_NODE_CLS = None
    DCC_SELECTION_CLS = None
    def __init__(self, prx_tree_view):
        self._prx_tree_view = prx_tree_view
        self._obj_add_dict = self._prx_tree_view._item_dict

        self._prx_tree_view.set_item_select_changed_connect_to(
            self.set_select
        )

    def set_select(self):
        utl_prx_operators.PrxDccObjTreeViewSelectionOpt._set_dcc_select_(
            prx_tree_view=self._prx_tree_view,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )

    def set_content_at(self, file_path, content):
        self._prx_tree_view.set_clear()

        self._set_results_build_at_(content.get('error') or [], bsc_configure.ValidatorStatus.Error)
        self._set_results_build_at_(content.get('warning') or [], bsc_configure.ValidatorStatus.Warning)

    def _set_results_build_at_(self, results, status):
        for i in results:
            i_type = i['type']
            i_dcc_path = i['node']
            i_group = i['group']

            i_dcc_obj = self.DCC_NODE_CLS(i_dcc_path)
            i_group_path = '/{}'.format(
                i_group
            )
            i_description = i['description']
            i_group_prx_item = self._set_group_add_(i_group_path)
            i_node_prx_item = self._set_node_add_(i_group_prx_item, i_dcc_obj, i_description, status)
            if i_type == 'file':
                i_file_paths = i['elements']
                for j_file_path in i_file_paths:
                    j_file = utl_dcc_objects.OsFile(j_file_path)
                    self._set_file_add_(i_node_prx_item, j_file, i_description, status)
            elif i_type == 'component':
                i_components = i['elements']

    def _set_group_add_(self, group_path):
        if group_path in self._obj_add_dict:
            return self._obj_add_dict[group_path]
        else:
            group_path_opt = bsc_core.DccPathDagOpt(group_path)
            prx_item = self._prx_tree_view.set_item_add(
                name=group_path_opt.name,
                icon_name_text=group_path_opt.name,
            )
            prx_item.set_expanded(True)
            self._obj_add_dict[group_path] = prx_item
            return prx_item

    def _set_node_add_(self, group_prx_item, dcc_obj, description, status):
        prx_item = group_prx_item.set_child_add(
            name=[dcc_obj.name, description],
            icon=dcc_obj.icon,
        )
        prx_item.set_status(status)
        prx_item.set_gui_dcc_obj(
            dcc_obj, self.DCC_NAMESPACE
        )
        return prx_item

    def _set_file_add_(self, obj_prx_item, stg_file, description, status):
        prx_item = obj_prx_item.set_child_add(
            name=[stg_file.name, description],
            icon=stg_file.icon,
        )
        print stg_file.icon
        prx_item.set_status(status)
        return prx_item

    def set_scene_add(self):
        pass


class AbsAssetPublish(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = None
    DCC_VALIDATOR_OPT_CLS = None
    def __init__(self, session, *args, **kwargs):
        super(AbsAssetPublish, self).__init__(session, *args, **kwargs)

    def set_variants_restore(self):
        pass

    def set_all_setup(self):
        self._tab_view = prx_widgets.PrxTabView()
        self.set_widget_add(self._tab_view)

        s_0 = prx_widgets.PrxScrollArea()

        self._tab_view.set_item_add(
            s_0,
            name='validation',
            icon_name_text='validation',
        )

        s_1 = prx_widgets.PrxScrollArea()
        self._tab_view.set_item_add(
            s_1,
            name='information',
            icon_name_text='information',
        )

        self._tree_view = prx_widgets.PrxTreeView()
        s_0.set_widget_add(self._tree_view)
        self._tree_view.set_header_view_create(
            [('name', 4), ('description', 2)],
            self.get_definition_window_size()[0] - 32
        )

        self._tree_view_validator_opt = self.DCC_VALIDATOR_OPT_CLS(
            self._tree_view
        )

        self._publish_options_prx_node = prx_widgets.PrxNode_('options')
        s_1.set_widget_add(self._publish_options_prx_node)
        self._publish_options_prx_node.set_ports_create_by_configure(
            self._session.configure.get('build.node.publish_options'),
        )

        option_hook_opt = self._session.option_opt
        file_path = option_hook_opt.get('file')

        if file_path:
            self._publish_options_prx_node.set(
                'resolver.scene_file', file_path
            )

        self._stg_connector = self._session.get_shotgun_connector()

        self._publish_options_prx_node.get_port(
            'shotgun.version.type'
        ).set_changed_connect_to(
            self._set_shotgun_version_status_update_
        )

        self._publish_options_prx_node.set(
            'resolver.load', self.set_refresh_all
        )

        # version_types = self._stg_connector.get_stg_all_version_types()
        #
        # self._publish_options_prx_node.set(
        #     'shotgun.version.type', version_types
        # )

        # version_statuses = self._stg_connector.get_stg_all_version_status()
        #
        # self._publish_options_prx_node.set(
        #     'shotgun.version.status', version_statuses
        # )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._publish_options_prx_node,
            }
        )

        self._validation_button = prx_widgets.PrxPressItem()
        self._validation_button.set_name('validation')
        self.set_button_add(
            self._validation_button
        )
        self._validation_button.set_press_clicked_connect_to(self._set_validation_execute_)

        self._publish_button = prx_widgets.PrxPressItem()
        self._publish_button.set_name('publish')
        self.set_button_add(
            self._publish_button
        )
        self._publish_button.set_press_clicked_connect_to(self._set_publish_execute_)

        self.set_refresh_all()

    def set_refresh_all(self):
        application = bsc_core.SystemMtd.get_application()
        if application == 'katana':
            self._scene_file_path = self._get_dcc_scene_file_path_()
        else:
            self._scene_file_path = self._publish_options_prx_node.get('resolver.scene_file')
        #
        r = rsv_commands.get_resolver()
        if self._scene_file_path:
            rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(self._scene_file_path)
            self._rsv_task = r.get_rsv_task(**rsv_scene_properties.value)

            self._publish_options_prx_node.set(
                'resolver.task', self._rsv_task.path
            )

            self._stg_task_query = self._stg_connector.get_stg_task_query(
                **rsv_scene_properties.value
            )

            self._set_shotgun_task_update_()

    def _get_dcc_scene_file_path_(self):
        pass

    def _set_shotgun_version_status_update_(self):
        version_type = self._publish_options_prx_node.get('shotgun.version.type')
        version_status_mapper = dict(
            daily='rev',
            check='pub',
            downstream='pub'
        )
        version_status = version_status_mapper[version_type]
        self._publish_options_prx_node.set(
            'shotgun.version.status', version_status
        )

    def _set_shotgun_task_update_(self):
        task_status = self._stg_task_query.get('sg_status_list')

        self._publish_options_prx_node.set(
            'shotgun.task.status', task_status
        )

        task_assignees = self._stg_task_query.get('task_assignees')
        if task_assignees:
            self._publish_options_prx_node.set(
                'shotgun.task.assignees',
                ', '.join([self._stg_connector.get_stg_user_query(**i).get('name') for i in task_assignees])
            )

    def _set_validation_execute_(self):
        if bsc_core.ApplicationMtd.get_is_katana():
            s = ssn_commands.set_option_hook_execute(
                bsc_core.KeywordArgumentsOpt(
                    option=dict(
                        option_hook_key='rsv-task-methods/asset/katana/gen-surface-validation',
                        file=self._scene_file_path,
                        # with_scene_validation=True,
                        with_geometry_topology_validation=True,
                        with_geometry_uv_map_validation=True,
                        with_texture_validation=True,
                        with_shotgun_validation=True,
                    )
                ).to_string()
            )
            self._tree_view_validator_opt.set_content_at(
                self._scene_file_path,
                s.get_validator().get_content()
            )

    def _set_publish_execute_(self):
        pass
