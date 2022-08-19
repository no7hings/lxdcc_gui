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

    def set_scene_add(self, file_path):
        if file_path in self._obj_add_dict:
            return self._obj_add_dict[file_path]
        #
        stg_file = utl_dcc_objects.OsFile(file_path)

        name = stg_file.get_path_prettify_()

        prx_item = self._prx_tree_view.set_item_add(
            name=name,
            icon=stg_file.icon,
            tool_tip=file_path,
        )
        prx_item.set_expanded(True)
        prx_item.set_checked(True)

        prx_item._validation_name = name
        prx_item._validation_result = [0, 0]

        prx_item._child_dict = {}
        self._obj_add_dict[file_path] = prx_item
        return prx_item

    def set_results_at(self, file_path, results):
        scene_prx_item = self.set_scene_add(file_path)
        scene_prx_item.set_children_clear()
        scene_prx_item._child_dict = {}
        if not results:
            scene_prx_item.set_status(
                bsc_configure.ValidatorStatus.Correct
            )
            return True

        self._set_sub_results_build_at_(
            scene_prx_item, results
        )

    def _set_sub_results_build_at_(self, scene_prx_item, results):
        with utl_core.gui_progress(maximum=len(results)) as g_p:
            for i_result in results:
                g_p.set_update()

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
                self._set_status_update_(scene_prx_item, i_validation_status)
                #
                i_group_prx_item = self._get_group_(scene_prx_item, i_group_name)
                self._set_status_update_(i_group_prx_item, i_validation_status)
                i_node_prx_item = self._get_node_(scene_prx_item, i_group_prx_item, i_dcc_path, i_description, i_validation_status)
                if i_type == 'file':
                    i_file_paths = i_result['elements']
                    for j_file_path in i_file_paths:
                        self._get_file_(scene_prx_item, i_node_prx_item, j_file_path, i_description, i_validation_status)
                elif i_type == 'component':
                    i_components = i_result['elements']

    def _get_group_(self, scene_prx_item, group_name):
        if group_name in scene_prx_item._child_dict:
            prx_item = scene_prx_item._child_dict[group_name]
            return prx_item

        prx_item = scene_prx_item.set_child_add(
            name=group_name,
            icon=utl_gui_core.RscIconFile.get('container'),
        )
        prx_item.set_expanded(True)
        #
        prx_item._validation_name = group_name
        prx_item._validation_result = [0, 0]
        #
        scene_prx_item._child_dict[group_name] = prx_item
        return prx_item

    def _set_status_update_(self, prx_item, status):
        group_name = prx_item._validation_name
        error_count, warning_count = prx_item._validation_result
        pre_status = prx_item.get_status()
        if status > pre_status:
            prx_item.set_status(status)

        if status == bsc_configure.ValidatorStatus.Error:
            error_count += 1
        elif status == bsc_configure.ValidatorStatus.Warning:
            warning_count += 1
        #
        prx_item._validation_result = [error_count, warning_count]
        #
        d = ', '.join([['error x {}', 'warning x {}'][seq].format(i) for seq, i in enumerate([error_count, warning_count]) if i])
        #
        prx_item.set_name(
            '{} [ {} ]'.format(group_name, d)
        )

    def _get_node_(self, scene_prx_item, group_prx_item, dcc_path, description, status):
        dcc_obj = self.DCC_NODE_CLS(dcc_path)
        prx_item = group_prx_item.set_child_add(
            name=[dcc_obj.name, description],
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path,
        )
        prx_item.set_status(status)
        prx_item.set_gui_dcc_obj(
            dcc_obj, self.DCC_NAMESPACE
        )
        return prx_item

    def _get_file_(self, scene_prx_item, obj_prx_item, file_path, description, status):
        stg_file = utl_dcc_objects.OsFile(file_path)
        prx_item = obj_prx_item.set_child_add(
            name=[stg_file.name, description],
            icon=stg_file.icon,
        )
        prx_item.set_status(status)
        return prx_item


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
            name='publish',
            icon_name_text='publish',
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

        self._publish_options_prx_node.set(
            'load', self.set_refresh_all
        )

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
        self._publish_button.set_option_click_enable(True)

        # self._publish_button.set_enable(False)

        self.set_refresh_all()

    def set_refresh_all(self):
        application = bsc_core.SystemMtd.get_application()
        if application == 'katana':
            self._scene_file_path = self._get_dcc_scene_file_path_()
        else:
            self._scene_file_path = self._publish_options_prx_node.get('resolver.scene_file')
        #
        r = rsv_commands.get_resolver()
        #
        self._tree_view.set_clear()
        if self._scene_file_path:
            self._tree_view_validator_opt.set_scene_add(self._scene_file_path)
            #
            self._rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(self._scene_file_path)
            self._rsv_task = r.get_rsv_task(**self._rsv_scene_properties.value)

            self._publish_options_prx_node.set(
                'resolver.task', self._rsv_task.path
            )

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

    @utl_gui_qt_core.set_prx_window_waiting
    def _set_validation_execute_(self):
        if bsc_core.ApplicationMtd.get_is_katana():
            s = ssn_commands.set_option_hook_execute(
                bsc_core.KeywordArgumentsOpt(
                    option=dict(
                        option_hook_key='rsv-task-methods/asset/katana/gen-surface-validation',
                        file=self._scene_file_path,
                        with_scene_validation=True,
                        with_geometry_topology_validation=True,
                        with_geometry_uv_map_validation=True,
                        with_texture_validation=True,
                        with_shotgun_validation=True,
                    )
                ).to_string()
            )
            #
            v = s.get_validator()
            #
            self._tree_view_validator_opt.set_results_at(
                self._scene_file_path,
                v.get_results()
            )
            self._publish_button.set_enable(v.get_is_passed())
        else:
            application = self._rsv_scene_properties.get('application')
            if application == 'katana':
                s = ssn_commands.set_option_hook_execute_by_shell(
                    bsc_core.KeywordArgumentsOpt(
                        option=dict(
                            option_hook_key='rsv-task-methods/asset/katana/gen-surface-validation',
                            file=self._scene_file_path,
                            with_scene_validation=True,
                            with_geometry_topology_validation=True,
                            with_geometry_uv_map_validation=True,
                            with_texture_validation=True,
                            with_shotgun_validation=True,
                        )
                    ).to_string(),
                    block=True
                )
                #
                v = s.get_validator()
                #
                self._tree_view_validator_opt.set_results_at(
                    self._scene_file_path,
                    v.get_results()
                )
                self._publish_button.set_enable(v.get_is_passed())

    @utl_gui_qt_core.set_prx_window_waiting
    def _set_publish_execute_(self):
        def yes_fnc_():
            print w.get_options_as_kwargs()

        w = utl_core.DialogWindow.set_create(
            'Publish',
            content=u'choose a version type, press "Confirm" to continue',
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
            window_size=(480, 480),
            #
            parent=self.widget,
            #
            use_exec=False
        )

        w.set_window_show()
