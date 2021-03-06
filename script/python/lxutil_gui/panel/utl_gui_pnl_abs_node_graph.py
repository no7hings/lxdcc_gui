# coding:utf-8
import functools

from lxbasic import bsc_core

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


class AbsRezGraph(prx_widgets.PrxToolWindow):
    OPTION_HOOK_KEY = None
    def __init__(self, hook_option, *args, **kwargs):
        super(AbsRezGraph, self).__init__(*args, **kwargs)
        if hook_option is not None:
            self._hook_option_opt = bsc_core.KeywordArgumentsOpt(hook_option)
            self._hook_option_opt.set(
                'option_hook_key', self.OPTION_HOOK_KEY
            )
            #
            self._option_hook_configure = ssn_commands.get_option_hook_configure(
                self._hook_option_opt.to_string()
            )
            #
            self._hook_gui_configure = self._option_hook_configure.get_content('option.gui')
            # self._hook_build_configure = self._option_hook_configure.get_content('build')
            #
            raw = bsc_core.EnvironMtd.get('REZ_BETA')
            if raw:
                self._rez_beta = True
            else:
                self._rez_beta = False

            if self._rez_beta:
                self.set_window_title(
                    '[BETA] {}'.format(self._hook_gui_configure.get('name'))
                )
            else:
                self.set_window_title(
                    self._hook_gui_configure.get('name')
                )
            #
            self.set_window_icon_name_text(
                self._hook_gui_configure.get('name')
            )
            self.set_definition_window_size(
                self._hook_gui_configure.get('size')
            )

            self.set_loading_start(
                time=1000,
                method=self._set_tool_panel_setup_
            )

    def _set_tool_panel_setup_(self):
        h_s = prx_widgets.PrxHSplitter()
        self.set_widget_add(h_s)
        self._node_tree = prx_widgets.PrxNGTree()
        h_s.set_widget_add(self._node_tree)
        self._node_graph = prx_widgets.PrxNGGraph()
        h_s.set_widget_add(self._node_graph)

        h_s.set_stretches([1, 3])

        packages = self._hook_option_opt.get('packages', as_array=True)
        self.test(packages)

        self.set_window_loading_end()

    def test(self, packages):
        import rez.resolved_context as r_c

        u = core_objects.ObjUniverse()

        r_s_t = u._get_obj_type_force_('rez', 'system')
        r_p_t = u._get_obj_type_force_('rez', 'package')
        r_v_t = u._get_obj_type_force_('rez', 'v')

        t = u._get_type_force_(u.Category.CONSTANT, u.Type.NODE)

        # ps = utl_core.MayaLauncher(
        #     project='cgm'
        # ).get_rez_packages()

        # ps = ['lxdcc']
        r = r_c.ResolvedContext(
            packages,
            package_paths=[
                bsc_core.StoragePathMtd.set_map_to_platform(i) for i in [
                    "/l/packages/pg/prod",
                    "/l/packages/pg/dept",
                    "/l/packages/pg/third_party/app",
                    "/l/packages/pg/third_party/plugin",
                    "/l/packages/pg/third_party/ocio"
                ]
            ]
        )

        root = u.get_root()
        root.set_input_port_create(
            t, 'input'
        )
        root.set_output_port_create(
            t, 'output'
        )

        path_dict = {}
        for i_key in packages:
            if '-' in i_key:
                i_type = r_v_t
                i_package, i_version = i_key.split('-')
                i_path = '/{}-{}'.format(i_package, i_version)
                i_n = i_type.set_obj_create(
                    i_path
                )
                i_n.set_input_port_create(
                    t, 'input'
                )
                i_n.set_output_port_create(
                    t, 'output'
                )
                root.get_input_port(
                    'input'
                ).set_source(
                    i_n.get_output_port(
                        'output'
                    )
                )
            else:
                i_package = i_key
                i_type = r_p_t
                i_path = '/{}'.format(i_package)

                i_p_n = i_type.set_obj_create(
                    i_path
                )
                i_p_n.set_input_port_create(
                    t, 'input'
                )
                i_p_n.set_output_port_create(
                    t, 'output'
                )
                root.get_input_port(
                    'input'
                ).set_source(
                    i_p_n.get_output_port(
                        'output'
                    )
                )

        g = r.graph()

        for i in g.nodes():
            i_atr = g.node_attributes(i)
            i_key = i_atr[0][1]
            if i_key.startswith('~'):
                i_type = r_s_t
                i_path = '/{}'.format(i_key)
            else:
                if '-' in i_key:
                    i_type = r_v_t
                    i_name, i_version = i_key.split('-')
                    if '[' in i_version:
                        if '[]' in i_version:
                            i_version_ = i_version[:-2]
                            i_path = '/{}-{}'.format(i_name, i_version_)
                        else:
                            i_version_ = i_version.split('[')[0]
                            i_index = i_version.split('[')[-1][:-1]
                            i_path = '/{}-{}-({})'.format(i_name, i_version_, i_index)
                    else:
                        i_path = '/{}-{}'.format(i_name, i_version)
                else:
                    i_type = r_p_t
                    i_path = '/{}'.format(i_key)
            #
            i_n = i_type.set_obj_create(
                i_path
            )
            i_n.set_input_port_create(
                t, 'input'
            )
            i_n.set_output_port_create(
                t, 'output'
            )
            path_dict[i] = i_path

        for i in g.edges():
            i_tgt, i_src = i
            i_src_path, i_tgt_path = path_dict[i_src], path_dict[i_tgt]
            i_n_src = u.get_obj(i_src_path)
            i_n_tgt = u.get_obj(i_tgt_path)
            i_n_src.get_output_port('output').set_connect_to(
                i_n_tgt.get_input_port('input')
            )

        self._node_graph.set_universe(u)
        self._node_graph.set_node_show()

        self._node_tree.set_universe(u)

        menu = self.set_menu_add(
            'Tool(s)'
        )
        menu.set_menu_raw(
            [
                ('Save Graph', None, self._set_graph_save_),
            ]
        )

    def _set_graph_save_(self):
        size = self._node_graph.widget.size()
        p = utl_gui_qt_core.QtGui.QPixmap(size)
        p.fill(utl_gui_qt_core.QtCore.Qt.transparent)
        self._node_graph.widget.render(
            p
        )
        p.save('/data/f/rez_test/png/test_0.png', 'PNG')


class AbsAssetLineup(prx_widgets.PrxToolWindow):
    OPTION_HOOK_KEY = None
    DCC_NAMESPACE = 'resolver'
    def __init__(self, hook_option, *args, **kwargs):
        super(AbsAssetLineup, self).__init__(*args, **kwargs)
        self._qt_thread_enable = bsc_core.EnvironMtd.get_qt_thread_enable()
        #
        if hook_option is not None:
            self._hook_option_opt = bsc_core.KeywordArgumentsOpt(hook_option)
            self._hook_option_opt.set(
                'option_hook_key', self.OPTION_HOOK_KEY
            )
            #
            self._option_hook_configure = ssn_commands.get_option_hook_configure(
                self._hook_option_opt.to_string()
            )
            #
            self._hook_gui_configure = self._option_hook_configure.get_content('option.gui')
            # self._hook_build_configure = self._option_hook_configure.get_content('build')
            self._hook_resolver_configure = self._option_hook_configure.get_content('resolver')
            self._hook_build_configure = self._option_hook_configure.get_content('build')
            #
            raw = bsc_core.EnvironMtd.get('REZ_BETA')
            if raw:
                self._rez_beta = True
            else:
                self._rez_beta = False

            if self._rez_beta:
                self.set_window_title(
                    '[BETA] {}'.format(self._hook_gui_configure.get('name'))
                )
            else:
                self.set_window_title(
                    self._hook_gui_configure.get('name')
                )
            #
            self.set_window_icon_name_text(
                self._hook_gui_configure.get('name')
            )
            self.set_definition_window_size(
                self._hook_gui_configure.get('size')
            )

            self._session_dict = {}

            self._image_dict = {}

            self.set_loading_start(
                time=1000,
                method=self._set_tool_panel_setup_
            )

    def _set_tool_panel_setup_(self):
        h_s = prx_widgets.PrxHSplitter()
        self.set_widget_add(h_s)
        v_s = prx_widgets.PrxVSplitter()
        h_s.set_widget_add(v_s)
        self._rsv_obj_tree_view_0 = prx_widgets.PrxTreeView()
        v_s.set_widget_add(self._rsv_obj_tree_view_0)

        s = prx_widgets.PrxScrollArea()
        v_s.set_widget_add(s)
        self._options_prx_node = prx_widgets.PrxNode_('options')
        s.set_widget_add(self._options_prx_node)
        self._options_prx_node.set_ports_create_by_configure(
            self._hook_build_configure.get('node.options')
        )

        self._options_prx_node.set('refresh', self.set_refresh_all)
        self._options_prx_node.set('graph.reload', self._set_graph_reload_)
        self._options_prx_node.set('output.save', self._set_graph_save_)

        v_s.set_stretches([1, 1])

        self._rsv_obj_tree_view_0.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 24
        )
        # self._rsv_obj_tree_view_0.set_single_selection()
        self._prx_dcc_obj_tree_view_add_opt = utl_prx_operators.PrxRsvObjTreeViewAddOpt(
            prx_tree_view=self._rsv_obj_tree_view_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._node_graph = prx_widgets.PrxNGImageGraph()
        h_s.set_widget_add(self._node_graph)

        h_s.set_stretches([1, 3])

        menu = self.set_menu_add(
            'Tool(s)'
        )
        menu.set_menu_raw(
            [
                ('Save Graph', None, self._set_graph_save_),
            ]
        )

        self.set_refresh_all()

        self.set_window_loading_end()

    def set_refresh_all(self):
        self._resolver = rsv_commands.get_resolver()

        self._project = self._options_prx_node.get('project')
        self._rsv_project = self._resolver.get_rsv_project(project=self._project)
        self._rsv_filter = self._hook_resolver_configure.get('filter')

        self._rsv_filter_opt = bsc_core.KeywordArgumentsOpt(self._rsv_filter)

        self._rsv_project.set_gui_attribute_restore()
        self._prx_dcc_obj_tree_view_add_opt.set_restore()

        self._image_dict = {}

        self._set_gui_rsv_objs_refresh_()

    def _set_gui_rsv_objs_refresh_(self):
        self._set_gui_add_rsv_project_(self._rsv_project)

        self._set_add_rsv_entities_(self._rsv_project)

    def _set_gui_add_rsv_project_(self, rsv_project):
        is_create, prx_item, show_threads = self._prx_dcc_obj_tree_view_add_opt.set_prx_item_add_as_tree_mode(
            rsv_project
        )
        if is_create is True:
            prx_item.set_expanded(True, ancestors=True)
        return show_threads
    #
    def _set_add_rsv_entities_(self, rsv_project):
        def post_fnc_():
            self._end_timestamp = bsc_core.SystemMtd.get_timestamp()
            #
            utl_core.Log.set_module_result_trace(
                'load asset/shot from "{}"'.format(
                    rsv_project.path
                ),
                'count={}, cost-time="{}"'.format(
                    self._count,
                    bsc_core.IntegerMtd.second_to_time_prettify(int(self._end_timestamp - self._start_timestamp))
                )
            )

            self._set_graph_reload_()

        self._count = 0
        self._start_timestamp = bsc_core.SystemMtd.get_timestamp()
        #
        rsv_tags = rsv_project.get_rsv_tags(**self._rsv_filter_opt.value)
        #
        if self._qt_thread_enable is True:
            t_r = utl_gui_qt_core.QtBuildThreadsRunner(self.widget)
            t_r.run_finished.connect(post_fnc_)
            for i_rsv_tag in rsv_tags:
                t_r.set_register(
                    functools.partial(
                        self._set_cache_add_rsv_entities_,
                        i_rsv_tag
                    ),
                    self._set_gui_add_rsv_entities_
                )
            t_r.set_start()
        else:
            with utl_core.gui_progress(maximum=len(rsv_tags)) as g_p:
                for i_rsv_tag in rsv_tags:
                    g_p.set_update()
                    self._set_gui_add_rsv_entities_(
                        self._set_cache_add_rsv_entities_(i_rsv_tag)
                    )
    # entities for tag
    def _set_cache_add_rsv_entities_(self, rsv_tag):
        return rsv_tag.get_rsv_entities(**self._rsv_filter_opt.value)

    def _set_gui_add_rsv_entities_(self, rsv_entities):
        for i_rsv_entity in rsv_entities:
            self._set_gui_add_rsv_entity_(i_rsv_entity)
        #
        self._count += len(rsv_entities)

    def _set_gui_add_rsv_entity_(self, rsv_entity):
        is_create, prx_item, show_threads = self._prx_dcc_obj_tree_view_add_opt.set_prx_item_add_as_tree_mode(
            rsv_entity
        )
        if is_create is True:
            branch = rsv_entity.properties.get('branch')
            if branch == 'asset':
                asset_menu_content = self.get_rsv_asset_menu_content(rsv_entity)
                if asset_menu_content:
                    rsv_entity.set_gui_menu_content(
                        asset_menu_content
                    )
            #
            self._set_gui_add_rsv_unit_(rsv_entity)

    def get_rsv_asset_menu_content(self, rsv_entity):
        hook_keys = self._option_hook_configure.get(
            'actions.asset.hooks'
        ) or []
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_entity
        )

    def _set_gui_add_rsv_unit_(self, rsv_entity):
        rsv_entity_gui = rsv_entity.get_obj_gui()
        model_rsv_task = rsv_entity.get_rsv_task(
            step='mod', task='modeling'
        )
        if model_rsv_task is not None:
            component_registry_usd_rsv_unit = model_rsv_task.get_rsv_unit(
                keyword='asset-component-registry-usd-file'
            )
            component_registry_usd_file_path = component_registry_usd_rsv_unit.get_result(
                version='latest'
            )
            if component_registry_usd_file_path:
                preview_rsv_unit = model_rsv_task.get_rsv_unit(
                    keyword='asset-output-katana-render-video-png-file'
                )
                result = preview_rsv_unit.get_result(
                    version='latest',
                    extend_variants=dict(
                        camera='front',
                        layer='master',
                        light_pass='all',
                        look_pass='plastic',
                        quality='custom'
                    )
                )
                if result is not None:
                    self._image_dict[rsv_entity.path] = result
                    rsv_entity_gui.set_state(
                        rsv_entity_gui.State.ENABLE
                    )
                else:
                    rsv_entity_gui.set_state(
                        rsv_entity_gui.State.DISABLE
                    )
            else:
                rsv_entity_gui.set_state(
                    rsv_entity_gui.State.WARNING
                )
        else:
            rsv_entity_gui.set_state(
                rsv_entity_gui.State.ERROR
            )

    def _set_graph_reload_(self):
        self._universe = core_objects.ObjUniverse()

        self._u_asset_type = self._universe._get_obj_type_force_('lynxi', 'asset')

        self._u_image_type = self._universe._get_type_force_(
            self._universe.Category.CONSTANT, self._universe.Type.STRING
        )

        if self._image_dict:
            for k, v in self._image_dict.items():
                i_prx_item = self._rsv_obj_tree_view_0.get_item_by_filter_key(k)
                i_rsv_entity = i_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                if i_prx_item.get_is_checked() is True:
                    i_n = self._u_asset_type.set_obj_create(
                        '/{}'.format(
                            i_rsv_entity.name
                        )
                    )
                    p = i_n.set_variant_port_create(
                        self._u_image_type, 'image'
                    )
                    p.set(v)

        self._node_graph.set_clear()
        self._node_graph.set_universe(self._universe)
        self._node_graph.set_node_show()
    @classmethod
    def _get_menu_content_by_hook_keys_(cls, session_dict, hooks, *args, **kwargs):
        content = bsc_objects.Dict()
        for i_hook in hooks:
            if isinstance(i_hook, (str, unicode)):
                i_hook_key = i_hook
                i_hook_option = None
            elif isinstance(i_hook, dict):
                i_hook_key = i_hook.keys()[0]
                i_hook_option = i_hook.values()[0]
            else:
                raise RuntimeError()
            #
            i_args = cls._get_rsv_unit_action_hook_args_(
                session_dict, i_hook_key, *args, **kwargs
            )
            if i_args:
                i_session, i_execute_fnc = i_args
                if i_session.get_is_loadable() is True and i_session.get_is_visible() is True:
                    i_gui_configure = i_session.gui_configure
                    #
                    i_gui_parent_path = '/'
                    #
                    i_gui_name = i_gui_configure.get('name')
                    if i_hook_option:
                        if 'gui_name' in i_hook_option:
                            i_gui_name = i_hook_option.get('gui_name')
                        #
                        if 'gui_parent' in i_hook_option:
                            i_gui_parent_path = i_hook_option['gui_parent']
                    #
                    i_gui_parent_path_opt = bsc_core.DccPathDagOpt(i_gui_parent_path)
                    #
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_path = '/{}'.format(i_gui_name)
                    else:
                        i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                    #
                    i_gui_separator_name = i_gui_configure.get('group_name')
                    if i_gui_separator_name:
                        if i_gui_parent_path_opt.get_is_root():
                            i_gui_separator_path = '/{}'.format(i_gui_separator_name)
                        else:
                            i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_separator_name)
                        #
                        content.set(
                            '{}.properties.type'.format(i_gui_separator_path), 'separator'
                        )
                        content.set(
                            '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                        )
                    #
                    content.set(
                        '{}.properties.type'.format(i_gui_path), 'action'
                    )
                    content.set(
                        '{}.properties.group_name'.format(i_gui_path), i_gui_configure.get('group_name')
                    )
                    content.set(
                        '{}.properties.name'.format(i_gui_path), i_gui_name
                    )
                    content.set(
                        '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                    )
                    if i_hook_option:
                        if 'gui_icon_name' in i_hook_option:
                            content.set(
                                '{}.properties.icon_name'.format(i_gui_path), i_hook_option.get('gui_icon_name')
                            )
                    #
                    content.set(
                        '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                    )
                    content.set(
                        '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                    )
        return content
    @classmethod
    def _get_rsv_unit_action_hook_args_(cls, session_dict, key, *args, **kwargs):
        def execute_fnc():
            session._set_file_execute_(python_file_path, dict(session=session))
        #
        rsv_task = args[0]
        session_path = '{}/{}'.format(rsv_task.path, key)
        if session_path in session_dict:
            return session_dict[session_path]
        else:
            python_file_path = ssn_core.RscHookFile.get_python(key)
            yaml_file_path = ssn_core.RscHookFile.get_yaml(key)
            if python_file_path and yaml_file_path:
                python_file = utl_dcc_objects.OsPythonFile(python_file_path)
                yaml_file = utl_dcc_objects.OsFile(yaml_file_path)
                if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
                    configure = bsc_objects.Configure(value=yaml_file.path)
                    type_name = configure.get('option.type')
                    if type_name is not None:
                        kwargs['configure'] = configure
                        #
                        if type_name in ['asset', 'shot', 'step', 'task']:
                            session = ssn_objects.RsvObjActionSession(
                                *args,
                                **kwargs
                            )
                        elif type_name in ['unit']:
                            session = ssn_objects.RsvUnitActionSession(
                                *args,
                                **kwargs
                            )
                        else:
                            raise TypeError()
                        #
                        session_dict[session_path] = session, execute_fnc
                        return session, execute_fnc

    def _set_graph_save_(self):
        file_path = self._options_prx_node.get(
            'output.file'
        )
        if file_path:
            self._node_graph.set_graph_save_to(
                file_path
            )
            self._options_prx_node.get_port(
                'output.file'
            ).set_history_update()
            utl_core.DialogWindow.set_create(
                'Save Graph',
                content='"{}" save is completed'.format(file_path),
                status=utl_core.DialogWindow.GuiStatus.Correct,
                #
                yes_label='Open Folder', yes_method=bsc_core.StoragePathOpt(file_path).set_open_in_system,
                no_label='Close',
                #
                cancel_visible=False
            )
        else:
            utl_core.DialogWindow.set_create(
                'Save Graph',
                content='enter a file name',
                status=utl_core.DialogWindow.GuiStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
