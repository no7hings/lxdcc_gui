# coding:utf-8
import collections

import os

import functools

import lxutil_gui.proxy.widgets as prx_widgets

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

import lxutil_gui.proxy.operators as utl_prx_operators

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxresolver.commands as rsv_commands

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

from lxsession import ssn_core

import lxsession.objects as ssn_objects

import lxsession.commands as ssn_commands


class AbsEntitiesLoaderPanel_(prx_widgets.PrxToolWindow):
    DCC_NAMESPACE = 'resolver'
    ITEM_ICON_FRAME_SIZE = 26, 26
    ITEM_ICON_SIZE = 24, 24
    def __init__(self, session, *args, **kwargs):
        super(AbsEntitiesLoaderPanel_, self).__init__(*args, **kwargs)
        self._qt_thread_enable = bsc_core.EnvironMtd.get_qt_thread_enable()
        #
        self._rez_beta = bsc_core.EnvironMtd.get('REZ_BETA')
        #
        self._session = session
        self._hook_configure = self._session.configure
        self._hook_gui_configure = self._session.gui_configure

        self._rsv_filter = self._hook_configure.get('resolver.filter')
        #
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
        #
        self._item_frame_size = self._hook_gui_configure.get('item_frame_size')
        #
        self.get_log_bar().set_expanded(True)
        #
        self._set_panel_build_()
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

        self._rsv_task_unit_runner = None

        self._session_dict = {}
    #
    def _set_rsv_option_update_(self, raw):
        pass

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self.set_refresh_all()

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_options_build_()

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('viewers')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        #
        self._prx_obj_guide_bar = prx_widgets.PrxGuideBar()
        expand_box_0.set_widget_add(self._prx_obj_guide_bar)
        #
        h_s = prx_widgets.PrxHSplitter()
        expand_box_0.set_widget_add(h_s)
        v_s = prx_widgets.PrxVSplitter()
        h_s.set_widget_add(v_s)
        self._rsv_obj_tree_view_0 = prx_widgets.PrxTreeView()
        v_s.set_widget_add(self._rsv_obj_tree_view_0)
        self._rsv_obj_tree_view_0.set_filter_history_key(
            'filter.{}-task'.format(self._session.name)
        )
        #
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        v_s.set_widget_add(self._filter_tree_viewer_0)
        #
        self._rsv_uint_list_view_0 = prx_widgets.PrxListView()
        h_s.set_widget_add(self._rsv_uint_list_view_0)
        #
        v_s.set_stretches([1, 1])
        h_s.set_stretches([1, 3])
        #
        self._set_obj_viewer_build_()

    def _set_options_build_(self):
        self._rsv_keywords = self._get_available_rsv_keywords_()
        self._rsv_filter_opt = bsc_core.KeywordArgumentsOpt(self._rsv_filter)
        self._filter_project = self._rsv_filter_opt.get('project')
        #
        self._options_prx_node = prx_widgets.PrxNode_('options')
        self.set_widget_add(self._options_prx_node)
        #
        _port = self._options_prx_node.set_port_add(
            prx_widgets.PrxEnumeratePort_('filter')
        )
        self._rsv_filters_dict = self._hook_configure.get('resolver.filters')
        if self._rsv_filters_dict is not None:
            _port.set(
                self._rsv_filters_dict.keys()
            )
        #
        projects = [
            'shl',
            'cg7',
            'cjd',
            'lib',
        ]
        #
        current_project = self._get_current_project_()
        if current_project:
            if current_project in projects:
                projects.remove(current_project)
            #
            projects.append(current_project)
        #
        utl_core.History.set_extend(
            'gui.projects',
            projects
        )
        histories = utl_core.History.get(
            'gui.projects'
        )
        #
        _port = self._options_prx_node.set_port_add(
            prx_widgets.PrxRsvProjectChoosePort('project')
        )
        if self._filter_project is not None:
            _port.set(self._filter_project)
        else:
            _port.set(histories[-1])
        #
        _port = self._options_prx_node.set_port_add(
            prx_widgets.PrxButtonPort('refresh')
        )
        _port.set(self.set_refresh_all)

    def _set_obj_viewer_build_(self):
        self._rsv_obj_tree_view_0.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0]*(1.0/4.0) - 24
        )
        self._rsv_obj_tree_view_0.set_single_selection()
        #
        self._filter_tree_viewer_0.set_header_view_create(
            [('name', 3), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/4.0) - 24
        )
        self._filter_tree_viewer_0.set_single_selection()
        #
        self._prx_dcc_obj_tree_view_add_opt = utl_prx_operators.PrxRsvObjTreeViewAddOpt(
            prx_tree_view=self._rsv_obj_tree_view_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._rsv_obj_tree_view_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        #
        self._rsv_obj_tree_view_0.set_item_select_changed_connect_to(
            self._set_guide_bar_update_
        )
        self._rsv_obj_tree_view_0.set_item_select_changed_connect_to(
            self._set_gui_rsv_task_units_refresh_by_selection_
        )
        #
        self._rsv_uint_list_view_0.set_item_frame_size(*self._item_frame_size)
        self._rsv_uint_list_view_0.set_item_icon_frame_size(*self.ITEM_ICON_FRAME_SIZE)
        self._rsv_uint_list_view_0.set_item_icon_size(*self.ITEM_ICON_SIZE)
        self._rsv_uint_list_view_0.set_item_icon_frame_draw_enable(True)
        self._rsv_uint_list_view_0.set_item_name_frame_draw_enable(True)
        self._rsv_uint_list_view_0.set_item_image_frame_draw_enable(True)
        #
        self._rsv_uint_list_view_0.set_item_select_changed_connect_to(
            self._set_guide_bar_update_
        )
        self._rsv_uint_list_view_0.set_refresh_connect_to(self._set_gui_rsv_task_units_refresh_by_selection_)
        #
        self._prx_obj_guide_bar.set_item_clicked_connect_to(self._set_rsv_obj_select_)
        # self._prx_obj_guide_bar.set_item_changed_connect_to(self._set_rsv_obj_select_)

    def _set_gui_rsv_task_units_refresh_by_selection_(self):
        tree_item_prxes = self._rsv_obj_tree_view_0.get_selected_items()
        if self._rsv_task_unit_runner is not None:
            self._rsv_task_unit_runner.set_kill()
        #
        self._rsv_uint_list_view_0.set_clear()
        if tree_item_prxes:
            tree_item_prx = tree_item_prxes[-1]
            rsv_obj = tree_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
            if rsv_obj is not None:
                obj_type_name = rsv_obj.type_name
                if obj_type_name in [
                    'role', 'sequence',
                    'asset', 'shot',
                    'step',
                    'task'
                ]:
                    self._set_add_rsv_task_units_(rsv_obj)

    def _set_gui_rsv_objs_refresh_(self):
        self._resolver = rsv_commands.get_resolver()
        #
        project = self._options_prx_node.get_port(
            'project'
        ).get()
        #
        rsv_project = self._resolver.get_rsv_project(project=project)
        #
        rsv_project.set_gui_attribute_restore()
        self._prx_dcc_obj_tree_view_add_opt.set_restore()
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_restore()
        self._prx_obj_guide_bar.set_clear()
        #
        self._set_gui_add_rsv_project_(rsv_project)
        #
        self._set_add_rsv_entities_(rsv_project)
    #
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
                    functools.partial(self._set_cache_add_rsv_entities_, i_rsv_tag),
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
            prx_item.set_loading_start()
            #
            branch = rsv_entity.properties.get('branch')
            if branch == 'asset':
                asset_menu_content = self.get_rsv_asset_menu_content(rsv_entity)
                if asset_menu_content:
                    rsv_entity.set_gui_menu_content(
                        asset_menu_content
                    )
            #
            self._rsv_obj_tree_view_0.set_item_expand_connect_to(
                prx_item, lambda *args, **kwargs: self._set_add_rsv_tasks_by_entity_(rsv_entity),
                time=100
            )
    # tasks from entity
    def _set_add_rsv_tasks_by_entity_(self, rsv_entity):
        def post_fnc_():
            rsv_entity.get_obj_gui().set_loading_end()
            #
            self.set_filter_update()

        def quit_fnc_():
            t.quit()
            t.wait()
            t.deleteLater()
        #
        t = utl_gui_qt_core.QtBuildThread(self.widget)
        t.set_cache_fnc(
            functools.partial(rsv_entity.get_rsv_tasks, **self._rsv_filter_opt.value)
        )
        t.built.connect(self._set_gui_add_rsv_tasks_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()

        self.set_window_close_connect_to(quit_fnc_)

    def _set_gui_add_rsv_tasks_(self, rsv_tasks):
        for i_rsv_task in rsv_tasks:
            self._set_gui_add_rsv_task_(i_rsv_task)

    def _set_gui_add_rsv_task_(self, rsv_task):
        is_create, rsv_task_item_prx, show_threads = self._prx_dcc_obj_tree_view_add_opt.set_prx_item_add_as_tree_mode(
            rsv_task
        )
        if is_create is True:
            step = rsv_task.properties.get('step')
            task = rsv_task.properties.get('task')
            #
            task_menu_content = self.get_rsv_task_menu_content(rsv_task)
            if task_menu_content:
                rsv_task.set_gui_menu_content(
                    task_menu_content
                )
            #
            keys = ['{}.{}'.format(step, task)]
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_register(
                rsv_task_item_prx, keys
            )
            #
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                '{}.{}'.format(step, task), rsv_task_item_prx
            )
        return show_threads
    # tasks and units
    def _set_add_rsv_task_units_(self, rsv_obj):
        def post_fnc_():
            rsv_obj.get_obj_gui().set_loading_end()
            #
            self.set_filter_update()
            #
            self._rsv_uint_list_view_0.set_visible_tgt_raw_update()
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()
            #
            self._end_timestamp = bsc_core.SystemMtd.get_timestamp()
            utl_core.Log.set_module_result_trace(
                'load task from "{}"'.format(
                    rsv_obj.path
                ),
                'count={}, cost-time="{}"'.format(
                    self._count,
                    bsc_core.IntegerMtd.second_to_time_prettify(int(self._end_timestamp - self._start_timestamp))
                )
            )

        self._count = 0
        self._start_timestamp = bsc_core.SystemMtd.get_timestamp()
        #
        type_name = rsv_obj.type_name
        if type_name in [
            'role', 'sequence',
        ]:
            rsv_objs = rsv_obj.get_rsv_entities(
                **self._rsv_filter_opt.value
            )
            c = len(rsv_objs)
            if c > 50:
                w = utl_core.DialogWindow.set_create(
                    'List Tasks',
                    content='list all tasks from "{}", press "Yes" to continue'.format(
                        rsv_obj.name
                    ),
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    #
                    # use_exec=False,
                    #
                    parent=self.widget
                )
                result = w.get_result()
                if result is not True:
                    return
        else:
            rsv_objs = [rsv_obj]
        #
        if self._qt_thread_enable is True:
            self._rsv_task_unit_runner = utl_gui_qt_core.QtBuildThreadsRunner(self.widget)
            self._rsv_task_unit_runner.run_finished.connect(post_fnc_)
            for i_rsv_obj in rsv_objs:
                self._rsv_task_unit_runner.set_register(
                    functools.partial(self._set_cache_rsv_task_units_, i_rsv_obj),
                    self._set_gui_add_rsv_task_units_
                )
            self._rsv_task_unit_runner.set_start()
        else:
            with utl_core.gui_progress(maximum=len(rsv_objs)) as g_p:
                for i_rsv_obj in rsv_objs:
                    g_p.set_update()
                    self._set_gui_add_rsv_task_units_(
                        self._set_cache_rsv_task_units_(i_rsv_obj)
                    )

    def _set_cache_rsv_task_units_(self, rsv_obj):
        if rsv_obj.type_name == 'task':
            rsv_tasks = [rsv_obj]
        else:
            rsv_tasks = rsv_obj.get_rsv_tasks(**self._rsv_filter_opt.value)
        return rsv_tasks

    def _set_gui_add_rsv_task_units_(self, rsv_tasks):
        for i_rsv_task in rsv_tasks:
            self._set_gui_add_rsv_task_(i_rsv_task)
            #
            self._set_gui_add_rsv_task_unit_(i_rsv_task)

        self._count += len(rsv_tasks)

    def _get_rsv_task_unit_args_(self, rsv_task):
        list_ = []
        #
        for i_keyword in self._rsv_keywords:
            i_rsv_unit = rsv_task.get_rsv_unit(
                keyword=i_keyword
            )
            i_file_path = i_rsv_unit.get_result(version='latest')
            if i_file_path:
                list_.append(
                    (i_rsv_unit, i_file_path)
                )
        return list_

    def _get_rsv_task_unit_enable_(self, rsv_task):
        for i_keyword in self._rsv_keywords:
            i_rsv_unit = rsv_task.get_rsv_unit(
                keyword=i_keyword
            )
            i_file_path = i_rsv_unit.get_result(version='latest')
            if i_file_path:
                return True
        return False

    def _get_available_rsv_keywords_(self):
        list_ = []
        keywords = self._hook_configure.get('resolver.task_unit.keywords') or []
        for i_raw in keywords:
            if isinstance(i_raw, (str, unicode)):
                i_keyword = i_raw
                list_.append(i_keyword)
            elif isinstance(i_raw, dict):
                for j_keyword, j_raw in i_raw.items():
                    j_system_keys = j_raw.get('systems') or []
                    j_extend_variants = j_raw.get('extend_variants') or {}
                    if j_system_keys:
                        if bsc_core.SystemMtd.get_is_matched(j_system_keys):
                            list_.append(j_keyword)
                    else:
                        list_.append(j_keyword)
        return list_

    def _set_guide_bar_update_(self):
        list_item_prxes = self._rsv_uint_list_view_0.get_selected_items()
        rsv_obj = None
        if list_item_prxes:
            list_item_prx = list_item_prxes[-1]
            rsv_obj = list_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
        else:
            tree_item_prxes = self._rsv_obj_tree_view_0.get_selected_items()
            if tree_item_prxes:
                tree_item_prx = tree_item_prxes[-1]
                rsv_obj = tree_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
        #
        if rsv_obj is not None:
            self._prx_obj_guide_bar.set_path_args(
                rsv_obj.get_path_args()
            )
            dag_components = rsv_obj.get_ancestors()
            if dag_components:
                dag_components.reverse()
                for index, i in enumerate(dag_components):
                    content = [i.name for i in i.get_children()]
                    self._prx_obj_guide_bar.set_item_contents_at(content, index)

    def _set_rsv_obj_select_(self):
        obj_path = self._prx_obj_guide_bar.get_current_path()
        if obj_path is not None:
            self._rsv_obj_tree_view_0.set_item_select_by_filter_key(
                obj_path,
                exclusive=True
            )
    #
    def _set_gui_add_rsv_task_unit_(self, rsv_task):
        def cache_fnc_():
            _list = []
            #
            _keywords = self._rsv_keywords
            #
            for _i_keyword in _keywords:
                _i_rsv_unit = rsv_task.get_rsv_unit(
                    keyword=_i_keyword
                )
                _i_file_path = _i_rsv_unit.get_result(version='latest')
                if _i_file_path:
                    _list.append(
                        (_i_rsv_unit, _i_file_path)
                    )
            return _list

        def build_fnc_(data):
            self._set_gui_rsv_task_unit_show_deferred_(
                rsv_task, rsv_task_unit_gui, data
            )
        #
        rsv_task_gui = rsv_task.get_obj_gui()
        if rsv_task_gui is not None:
            enable = self._get_rsv_task_unit_enable_(rsv_task)
            if enable is True:
                rsv_task_unit_gui = self._rsv_uint_list_view_0.set_item_add()
                rsv_task_unit_gui.set_gui_dcc_obj(
                    rsv_task, namespace=self.DCC_NAMESPACE
                )
                #
                key = rsv_task.path
                rsv_task_gui.set_visible_connect_to(
                    key, rsv_task_unit_gui
                )
                #
                rsv_task_unit_gui.set_show_fnc(
                    cache_fnc_, build_fnc_
                )
                rsv_task_gui.set_state(utl_gui_core.State.ENABLE)
            else:
                rsv_task_gui.set_state(utl_gui_core.State.DISABLE)

    def _set_gui_rsv_task_unit_show_deferred_(self, rsv_task, rsv_task_unit_gui, show_data):
        project = rsv_task.get('project')
        branch = rsv_task.get('branch')
        name = rsv_task.get(branch)
        step = rsv_task.get('step')
        task = rsv_task.get('task')
        #
        show_info_dict = collections.OrderedDict(
            [
                (branch, name),
                ('step', step),
                ('task', task)
            ]
        )
        pixmaps = []
        for i_rsv_unit, i_file_path in show_data:
            i_file_path = i_rsv_unit.get_result()
            i_rsv_properties = i_rsv_unit.get_properties_by_result(i_file_path)
            i_rsv_unit_file = utl_dcc_objects.OsFile(i_file_path)
            i_pixmap = utl_gui_qt_core.QtPixmapMtd.get_by_file_ext_with_tag(
                i_rsv_unit_file.ext,
                tag=i_rsv_properties.get('workspace'),
                size=self.ITEM_ICON_SIZE
            )
            pixmaps.append(i_pixmap)
        #
        review_rsv_unit = rsv_task.get_rsv_unit(
            keyword='{branch}-review-file'
        )
        movie_file_path = review_rsv_unit.get_exists_result(
            version='latest'
        )
        if movie_file_path:
            session, execute_fnc = ssn_commands.get_option_hook_args(
                bsc_core.KeywordArgumentsOpt(
                    dict(
                        option_hook_key='actions/movie-open',
                        file=movie_file_path,
                        gui_group_name='movie',
                        gui_name='open movie'
                    )
                ).to_string()
            )
            #
            movie_file_opt = bsc_core.StorageFileOpt(movie_file_path)
            show_info_dict['update'] = bsc_core.TimeMtd.to_prettify_by_timestamp(
                movie_file_opt.get_modify_timestamp(),
                language=1
            )
            show_info_dict['user'] = movie_file_opt.get_user()
            #
            rsv_task_unit_gui.set_press_db_clicked_connect_to(
                execute_fnc
            )
            image_file_path, image_sub_process_cmds = bsc_core.VedioOpt(movie_file_path).get_thumbnail_create_args()
            rsv_task_unit_gui.set_image(image_file_path)
            rsv_task_unit_gui.set_movie_enable(True)
            if image_sub_process_cmds is not None:
                rsv_task_unit_gui.set_image_show_args(image_file_path, image_sub_process_cmds)
        else:
            show_info_dict['update'] = 'N/a'
            show_info_dict['user'] = 'N/a'
            rsv_task_unit_gui.set_image(
                utl_gui_core.RscIconFile.get('image_loading_failed')
            )
        #
        unit_menu_content = self.get_rsv_task_unit_menu_content(rsv_task)
        if unit_menu_content:
            rsv_task_unit_gui.set_menu_content(unit_menu_content)

        rsv_task_unit_gui.set_name_dict(show_info_dict)
        r, g, b = bsc_core.TextOpt(task).to_rgb()
        rsv_task_unit_gui.set_name_frame_background_color((r, g, b, 127))
        print pixmaps
        rsv_task_unit_gui.set_icons_by_pixmap(pixmaps)
        rsv_task_unit_gui.set_tool_tip(
            rsv_task.description
        )

    def set_refresh_all(self):
        if self._rsv_filters_dict:
            key = self._options_prx_node.get('filter')
            if key == 'auto':
                self._rsv_filter = self._get_resolver_application_filter_()
            else:
                self._rsv_filter = self._rsv_filters_dict[key]
            #
            self._rsv_filter_opt = bsc_core.KeywordArgumentsOpt(self._rsv_filter)
        #
        self._set_gui_rsv_objs_refresh_()
        # self.set_filter_refresh()

    def set_filter_update(self):
        self._rsv_uint_list_view_0.set_visible_tgt_raw_update()
        #
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_update()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def set_filter_refresh(self):
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh(expand_depth=1)
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()
    @classmethod
    def _get_current_application_(cls):
        return utl_core.Application.get_current()
    @classmethod
    def _get_current_project_(cls):
        _ = os.environ.get('PG_SHOW')
        if _:
            return _.lower()

    def _get_resolver_application_filter_(self):
        _ = self._hook_configure.get('resolver.application_filter') or {}
        for k, v in _.items():
            if bsc_core.SystemMtd.get_is_matched(['*-{}'.format(k)]):
                return v
        return self._hook_configure.get('resolver.filter')

    def get_rsv_assets_menu_content(self, rsv_entity):
        hook_keys = self._hook_configure.get(
            'actions.assets.hooks'
        ) or []
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_entity
        )

    def get_rsv_asset_menu_content(self, rsv_entity):
        hook_keys = self._hook_configure.get(
            'actions.asset.hooks'
        ) or []
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_entity
        )

    def get_rsv_task_menu_content(self, rsv_task):
        hook_keys = self._hook_configure.get(
            'actions.task.hooks'
        ) or []
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_task
        )

    def get_rsv_task_unit_menu_content(self, rsv_task):
        hook_keys = self._hook_configure.get(
            'actions.task_unit.hooks'
        ) or []
        #
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_task
        )
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
