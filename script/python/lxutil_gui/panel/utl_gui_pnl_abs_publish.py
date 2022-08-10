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
                'scene_file', file_path
            )

        self._stg_connector = self._session.get_shotgun_connector()

        version_types = self._stg_connector.get_stg_all_version_types()

        self._publish_options_prx_node.set(
            'shotgun.version_type', version_types
        )

    def set_refresh_all(self):
        scene_file_path = self._publish_options_prx_node.get('scene_file')
