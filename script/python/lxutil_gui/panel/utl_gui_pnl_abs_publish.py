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


class AbsAssetPublish(prx_widgets.PrxSessionWindow):
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
            name='publish',
            icon_name_text='publish',
        )

        self._publish_options_prx_node = prx_widgets.PrxNode_('options')
        s_0.set_widget_add(self._publish_options_prx_node)
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

        self._publish_options_prx_node.set(
            'check_and_repair', self._set_check_and_repair_run_
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._publish_options_prx_node,
            }
        )

        self.set_refresh_all()

        self._publish_options_prx_node.get_port(
            'customize.to'
        ).set_append(
            'test'
        )

    def set_refresh_all(self):
        scene_file_path = self._publish_options_prx_node.get('resolver.scene_file')
        r = rsv_commands.get_resolver()
        if scene_file_path:
            rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(scene_file_path)
            self._rsv_task = r.get_rsv_task(**rsv_scene_properties.value)

            self._publish_options_prx_node.set(
                'resolver.task', self._rsv_task.path
            )

            self._stg_task_query = self._stg_connector.get_stg_task_query(
                **rsv_scene_properties.value
            )

            self._set_shotgun_task_update_()

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

    def _set_check_and_repair_run_(self):
        print self._publish_options_prx_node.get_as_kwargs()
