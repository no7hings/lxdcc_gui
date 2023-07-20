# coding:utf-8
import six

import fnmatch

import collections

import os

import functools

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxbasic.extra.methods as bsc_etr_methods

import lxresolver.commands as rsv_commands

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

import lxutil_gui.proxy.operators as utl_prx_operators

from lxsession import ssn_core

import lxsession.objects as ssn_objects

import lxsession.commands as ssn_commands


class _GuiBaseOpt(object):
    DCC_NAMESPACE = 'resolver'
    def __init__(self, window, session, resolver):
        self._window = window
        self._session = session
        self._resolver = resolver


class _GuiTaskOpt(_GuiBaseOpt):
    def __init__(self, window, session, resolver, tree_view):
        super(_GuiTaskOpt, self).__init__(window, session, resolver)
        self._tree_view = tree_view


class _GuiGuideOpt(_GuiBaseOpt):
    DCC_NAMESPACE = 'resolver'
    def __init__(self, window, session, resolver, guide_bar, tree_view, list_view):
        super(_GuiGuideOpt, self).__init__(window, session, resolver)

        self._guide_bar = guide_bar
        self._tree_view = tree_view
        self._list_view = list_view

        branch = self._window._rsv_filter_opt.get('branch')
        if branch == self._resolver.EntityTypes.Asset:
            self._types = [
                None,
                self._resolver.EntityTypes.Project,
                self._resolver.EntityTypes.Role,
                self._resolver.EntityTypes.Asset,
                self._resolver.EntityTypes.Step,
                self._resolver.EntityTypes.Task
            ]
        elif branch == self._resolver.EntityTypes.Shot:
            self._types = [
                None,
                self._resolver.EntityTypes.Project,
                self._resolver.EntityTypes.Sequence,
                self._resolver.EntityTypes.Shot,
                self._resolver.EntityTypes.Step,
                self._resolver.EntityTypes.Task
            ]
        else:
            raise RuntimeError()

        self._guide_bar.set_dict(self._tree_view._item_dict)
        self._guide_bar.set_types(self._types)

    def gui_refresh(self):
        path = None
        list_item_prxes = self._list_view.get_selected_items()
        # gain list first
        if list_item_prxes:
            list_item_prx = list_item_prxes[-1]
            path = list_item_prx.get_gui_attribute('path')
        else:
            tree_item_prxes = self._tree_view.get_selected_items()
            if tree_item_prxes:
                tree_item_prx = tree_item_prxes[-1]
                path = tree_item_prx.get_gui_attribute('path')
        #
        if path is not None:
            for i in self._window._rsv_project_paths:
                if i not in self._tree_view._item_dict:
                    self._tree_view._item_dict[i] = None
            #
            self._guide_bar.set_path(path)


class AbsPnlRsvUnitLoader(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = 'resolver'
    ITEM_ICON_FRAME_SIZE = 26, 26
    ITEM_ICON_SIZE = 24, 24

    THREAD_STEP = 8
    def set_all_setup(self):
        v_qt_widget = qt_widgets.QtWidget()
        self.add_widget(v_qt_widget)
        v_qt_layout = qt_widgets.QtVBoxLayout(v_qt_widget)
        v_qt_layout.setContentsMargins(0, 0, 0, 0)
        # top
        self._top_tool_bar = prx_widgets.PrxHToolBar()
        v_qt_layout.addWidget(self._top_tool_bar._qt_widget)
        self._top_tool_bar.set_expanded(True)
        #   guide
        self._guide_tool_box = prx_widgets.PrxHToolBox()
        self._top_tool_bar.add_widget(self._guide_tool_box)
        self._guide_tool_box.set_expanded(True)
        self._guide_tool_box.set_size_mode(1)
        #
        self._task_guide_bar = prx_widgets.PrxGuideBar()
        self._guide_tool_box.add_widget(self._task_guide_bar)
        #
        h_qt_widget = qt_widgets.QtWidget()
        v_qt_layout.addWidget(h_qt_widget)
        h_qt_layout = qt_widgets.QtHBoxLayout(h_qt_widget)
        h_qt_layout.setContentsMargins(0, 0, 0, 0)
        # left
        self._left_contract_group = prx_widgets.PrxLeftExpandedGroup()
        h_qt_layout.addWidget(self._left_contract_group._qt_widget)
        self._left_contract_group.set_width(320)
        self._left_contract_group.set_expanded(True)
        #
        main_scroll_area = prx_widgets.PrxVScrollArea()
        h_qt_layout.addWidget(main_scroll_area._qt_widget)
        #
        self.__setup_gui_viewers_(main_scroll_area)
        self.__setup_gui_options_()

        self._gui_guide_opt = _GuiGuideOpt(
            self, self._session, self._resolver,
            self._task_guide_bar, self._result_tree_view, self._rsv_uint_list_view_0
        )
        self._result_tree_view.connect_item_select_changed_to(
            self._gui_guide_opt.gui_refresh
        )
        self._rsv_uint_list_view_0.connect_item_select_changed_to(
            self._gui_guide_opt.gui_refresh
        )

        self.set_refresh_all()

    def restore_variants(self):
        self.__running_threads_stacks = []
        self.__thread_stack_index = 0
        self.__resource_count = 0

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlRsvUnitLoader, self).__init__(session, *args, **kwargs)
        self._hook_configure = self._session.configure
        self._hook_gui_configure = self._session.gui_configure

        self._resolver = rsv_commands.get_resolver()

        self._rsv_filter = self._hook_configure.get('resolver.filter')
        #
        self._item_frame_size = self._hook_gui_configure.get('item_frame_size')

        self._session_dict = {}

        self.__asset_keys = set()
        self.__task_keys = set()

    def set_refresh_all(self):
        if self._rsv_filters_dict:
            key = self._options_prx_node.get('filter')
            if key == 'auto':
                self._rsv_filter = self._get_resolver_application_filter_()
            else:
                self._rsv_filter = self._rsv_filters_dict[key]
            #
            self._rsv_filter_opt = bsc_core.ArgDictStringOpt(self._rsv_filter)
        #
        self.gui_refresh_fnc()

    def gui_tree_select_cbk_0(self, text):
        if text is not None:
            self._result_tree_view.select_item_by_key(
                text,
                exclusive=True
            )
            #
            if text in self._rsv_project_paths:
                self._rsv_project_name_cur = bsc_core.DccPathDagOpt(text).get_name()
                self.set_refresh_all()

    def gui_tree_select_cbk_1(self, text):
        if text is not None:
            self._result_tree_view.select_item_by_key(
                text,
                exclusive=True
            )

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

    def gui_refresh_fnc(self):
        project = self._rsv_project_name_cur
        rsv_project = self._resolver.get_rsv_project(project=project)
        if rsv_project is not None:
            utl_core.History.append(
                'gui.projects',
                project
            )
        #
        rsv_project.restore_all_gui_variants()
        #
        self._result_tree_view.restore_filter()
        self._gui_rsv_obj_opt.restore_all()
        self._prx_dcc_obj_tree_view_tag_filter_opt.restore_all()
        self._task_guide_bar.set_clear()
        #
        self.__asset_keys = set()
        self.__task_keys = set()
        #
        is_create, prx_item = self._gui_rsv_obj_opt.gui_add_root()
        if is_create is True:
            prx_item.set_selected(True)
            self.__gui_add_project_(rsv_project)
    #
    def __gui_add_project_(self, rsv_project):
        is_create, prx_item = self._gui_rsv_obj_opt.gui_add_as_tree(
            rsv_project
        )
        if is_create is True:
            prx_item.set_expanded(True)
            self.__gui_add_for_all_resources_(rsv_project)
    #
    def __asset_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = fnmatch.filter(
                self.__asset_keys, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:50]
        return []

    def __filter_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = fnmatch.filter(
                self.__task_keys, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)
        return []

    def __setup_gui_viewers_(self, scroll_area):
        v_s = prx_widgets.PrxVSplitter()
        self._left_contract_group.add_widget(v_s)
        self._result_tree_view = prx_widgets.PrxTreeView()
        v_s.add_widget(self._result_tree_view)
        # self._result_tree_view.get_top_tool_bar().set_expanded(True)
        self._result_tree_view.set_filter_history_key(
            'filter.{}-results'.format(self._session.name)
        )
        self._result_tree_view.set_filter_entry_tip('fiter by resource ...')
        #
        self._filter_tree_view = prx_widgets.PrxTreeView()
        self._filter_tree_view.set_filter_history_key(
            'filter.{}-filter'.format(self._session.name)
        )
        v_s.add_widget(self._filter_tree_view)
        #
        self._rsv_uint_list_view_0 = prx_widgets.PrxListView()
        scroll_area.add_widget(self._rsv_uint_list_view_0)
        # self._rsv_uint_list_view_0.get_top_tool_bar().set_expanded(True)
        #
        self._options_prx_node = prx_widgets.PrxNode_('options')
        self._left_contract_group.add_widget(self._options_prx_node)
        self._options_prx_node.set_expanded(False)
        #
        v_s.set_stretches([2, 1])
        #
        self._result_tree_view.set_header_view_create(
            [('name', 3)],
            320 - 48
        )
        self._result_tree_view.set_selection_use_single()
        #
        self._filter_tree_view.set_header_view_create(
            [('name', 3), ('count', 1)],
            320 - 48
        )
        self._filter_tree_view.view._set_selection_disable_()
        # self._filter_tree_view.set_selection_use_single()
        #
        self._gui_rsv_obj_opt = utl_prx_operators.GuiRsvObjOpt(
            self._resolver,
            prx_tree_view=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem,
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.GuiTagFilterOpt(
            prx_tree_view_src=self._filter_tree_view,
            prx_tree_view_tgt=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        #
        self._result_tree_view.connect_item_select_changed_to(
            self.__execute_gui_refresh_tasks_and_units_by_selection_
        )
        #
        self._rsv_uint_list_view_0.set_item_frame_size_basic(*self._item_frame_size)
        self._rsv_uint_list_view_0.get_check_tool_box().set_visible(True)
        self._rsv_uint_list_view_0.get_scale_switch_tool_box().set_visible(True)
        self._rsv_uint_list_view_0.get_sort_switch_tool_box().set_visible(True)
        #
        self._rsv_uint_list_view_0.set_item_icon_frame_size(*self.ITEM_ICON_FRAME_SIZE)
        self._rsv_uint_list_view_0.set_item_icon_size(*self.ITEM_ICON_SIZE)
        self._rsv_uint_list_view_0.set_item_icon_frame_draw_enable(True)
        self._rsv_uint_list_view_0.set_item_name_frame_draw_enable(True)
        self._rsv_uint_list_view_0.set_item_names_draw_range([None, 3])
        self._rsv_uint_list_view_0.set_item_image_frame_draw_enable(True)
        #
        self._rsv_uint_list_view_0.connect_refresh_action_to(self.__execute_gui_refresh_tasks_and_units_by_selection_)
        #
        self._task_guide_bar.connect_user_text_choose_accepted_to(self.gui_tree_select_cbk_0)
        self._task_guide_bar.connect_user_text_press_accepted_to(self.gui_tree_select_cbk_1)

        self._result_tree_view.set_completion_gain_fnc(
            self.__asset_completion_gain_fnc_
        )
        self._filter_tree_view.set_completion_gain_fnc(
            self.__filter_completion_gain_fnc_
        )

        self._result_tree_view.connect_refresh_action_to(
            self.set_refresh_all
        )

    def __setup_gui_options_(self):
        self._available_rsv_show_args = self._get_available_rsv_show_args_()
        self._rsv_filter_opt = bsc_core.ArgDictStringOpt(self._rsv_filter)
        self._project_name_from_filter = self._rsv_filter_opt.get('project')
        #
        self._rsv_projects = self._resolver.get_rsv_projects()
        self._rsv_project_paths = [i.get_path() for i in self._rsv_projects]
        self._rsv_project_names = [i.get_name() for i in self._rsv_projects]
        #
        _port = self._options_prx_node.add_port(
            prx_widgets.PrxPortAsEnumerate('filter')
        )
        self._rsv_filters_dict = self._hook_configure.get('resolver.filters')
        if self._rsv_filters_dict is not None:
            _port.set(
                self._rsv_filters_dict.keys()
            )
        #
        current_project = self._get_current_project_()
        if current_project:
            if current_project in self._rsv_project_names:
                self._rsv_project_names.remove(current_project)
            #
            self._rsv_project_names.append(current_project)
        #
        utl_core.History.extend(
            'gui.projects',
            self._rsv_project_names
        )
        self._rsv_project_name_cur = self._rsv_project_names[0]
        if self._project_name_from_filter is not None:
            if self._project_name_from_filter in self._rsv_project_names:
                self._rsv_project_name_cur = self._project_name_from_filter
        else:
            project_name_from_history = utl_core.History.get_latest(
                'gui.projects'
            )
            if project_name_from_history is not None:
                if project_name_from_history in self._rsv_project_names:
                    self._rsv_project_name_cur = project_name_from_history

    def __restore_thread_stack_(self):
        if self.__running_threads_stacks:
            [i.set_kill() for i in self.__running_threads_stacks]
        #
        self.__running_threads_stacks = []
    #
    def __gui_add_for_all_resources_(self, rsv_project):
        def post_fnc_():
            self._end_timestamp = bsc_core.TimeMtd.get_timestamp()
            #
            utl_core.Log.set_module_result_trace(
                'load asset/shot from "{}"'.format(
                    rsv_project.path
                ),
                'count={}, cost-time="{}"'.format(
                    self.__resource_count,
                    bsc_core.RawIntegerMtd.second_to_time_prettify(self._end_timestamp-self._start_timestamp)
                )
            )

        def quit_fnc_():
            ts.set_quit()
        #
        self.__resource_count = 0
        self._start_timestamp = bsc_core.TimeMtd.get_timestamp()
        #
        rsv_resource_groups = rsv_project.get_rsv_resource_groups(**self._rsv_filter_opt.value)
        #
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            ts.run_finished.connect(post_fnc_)
            for i_rsv_resource_group in rsv_resource_groups:
                ts.register(
                    cache_fnc=functools.partial(self.__gui_cache_fnc_for_resources_by_group_, i_rsv_resource_group),
                    build_fnc=self.__gui_build_fnc_for_resources_
                )
            #
            ts.set_start()
            #
            self.set_window_close_connect_to(quit_fnc_)
        else:
            with utl_core.GuiProgressesRunner.create(maximum=len(rsv_resource_groups), label='gui-add for resource') as g_p:
                for i_rsv_resource_group in rsv_resource_groups:
                    g_p.set_update()
                    self.__gui_build_fnc_for_resources_(
                        self.__gui_cache_fnc_for_resources_by_group_(i_rsv_resource_group)
                    )
    # refresh resources by group
    def __gui_cache_fnc_for_resources_by_group_(self, rsv_resource_group):
        rsv_objs = rsv_resource_group.get_rsv_resources(**self._rsv_filter_opt.value)
        return rsv_objs

    def __gui_build_fnc_for_resources_(self, rsv_resources):
        for i_rsv_resource in rsv_resources:
            self.__gui_add_resource_(i_rsv_resource)
            self.__asset_keys.add(i_rsv_resource.name)
        #
        self.__resource_count += len(rsv_resources)

    def __gui_add_resource_(self, rsv_resource):
        is_create, prx_item = self._gui_rsv_obj_opt.gui_add_as_tree(
            rsv_resource
        )
        if is_create is True:
            prx_item.start_loading()
            #
            branch = rsv_resource.properties.get('branch')
            if branch == 'asset':
                asset_menu_content = self.get_rsv_asset_menu_content(rsv_resource)
                if asset_menu_content:
                    rsv_resource.set_gui_menu_content(
                        asset_menu_content
                    )
            #
            self._result_tree_view.connect_item_expand_to(
                prx_item, lambda *args, **kwargs: self.__execute_gui_refresh_for_tasks_by_resource_expand_changed_(rsv_resource),
                time=100
            )
    # refresh tasks by resource
    def __execute_gui_refresh_for_tasks_by_resource_expand_changed_(self, rsv_resource):
        def post_fnc_():
            rsv_resource.get_obj_gui().set_loading_end()
            #
            self.set_filter_update()

        def quit_fnc_():
            t.set_quit()
        #
        t = utl_gui_qt_core.QtBuildThread(self.widget)
        t.set_cache_fnc(
            functools.partial(self.__gui_cache_fnc_for_tasks_by_resource_, rsv_resource)
        )
        t.built.connect(self.__gui_build_fnc_for_tasks_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()

        self.set_window_close_connect_to(quit_fnc_)
    
    def __gui_cache_fnc_for_tasks_by_resource_(self, rsv_resource):
        return rsv_resource.get_rsv_tasks(**self._rsv_filter_opt.value)

    def __gui_build_fnc_for_tasks_(self, rsv_tasks):
        for i_rsv_task in rsv_tasks:
            self.__gui_add_task_(i_rsv_task)
            #
            self.__task_keys.add(i_rsv_task.name)

    def __gui_add_task_(self, rsv_task):
        is_create, rsv_task_item_prx = self._gui_rsv_obj_opt.gui_add_as_tree(
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
            self._prx_dcc_obj_tree_view_tag_filter_opt.register(
                rsv_task_item_prx, keys
            )
            #
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                '{}.{}'.format(step, task), rsv_task_item_prx
            )

    def __execute_gui_refresh_tasks_and_units_by_selection_(self):
        tree_item_prxes = self._result_tree_view.get_selected_items()
        # kill running
        self.__restore_thread_stack_()
        #
        self.__thread_stack_index += 1
        #
        self._start_timestamp = bsc_core.TimeMtd.get_timestamp()
        #
        self._rsv_uint_list_view_0.restore_all()
        if tree_item_prxes:
            tree_item_prx = tree_item_prxes[-1]
            rsv_entity = tree_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
            if rsv_entity is not None:
                obj_type_name = rsv_entity.type_name
                if obj_type_name in [
                    'role', 'sequence',
                    'asset', 'shot',
                    'step',
                    'task'
                ]:
                    self.__batch_add_tasks_and_units_by_entities_([rsv_entity], self.__thread_stack_index)
    # refresh task unit by any entity
    # todo: thread bug in katana
    def __batch_add_tasks_and_units_by_entities_(self, rsv_entities, thread_stack_index):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.set_quit()

        rsv_entities_map = bsc_core.RawListMtd.set_grid_to(
            rsv_entities, self.THREAD_STEP
        )
        #
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_rsv_entities in rsv_entities_map:
                ts.register(
                    functools.partial(self.__batch_gui_cache_fnc_for_tasks_and_units_by_entities_, i_rsv_entities, thread_stack_index),
                    self.__batch_gui_build_fnc_for_tasks_and_units_
                )
            #
            ts.set_start()
            #
            self.set_window_close_connect_to(quit_fnc_)
        else:
            for i_rsv_entities in rsv_entities_map:
                self.__batch_gui_build_fnc_for_tasks_and_units_(
                    self.__batch_gui_cache_fnc_for_tasks_and_units_by_entities_(i_rsv_entities, thread_stack_index)
                )

    def __batch_gui_cache_fnc_for_tasks_and_units_by_entities_(self, rsv_entities, thread_stack_index):
        if rsv_entities:
            type_name = rsv_entities[0].type_name
            if type_name in [
                'role', 'sequence',
            ]:
                return [
                    [j for i in rsv_entities for j in i.get_rsv_resources(**self._rsv_filter_opt.value)],
                    thread_stack_index
                ]
            else:
                return [
                    rsv_entities,
                    thread_stack_index
                ]

    def __batch_gui_build_fnc_for_tasks_and_units_(self, *args):
        def post_fnc_():
            # update for filter
            self.set_filter_update()

        def quit_fnc_():
            ts.set_quit()

        rsv_entities, thread_stack_index = args[0]
        rsv_entities_map = bsc_core.RawListMtd.set_grid_to(
            rsv_entities, self.THREAD_STEP
        )

        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_rsv_entities in rsv_entities_map:
                ts.register(
                    functools.partial(self.__gui_cache_fnc_for_tasks_and_units_by_entities_, i_rsv_entities, thread_stack_index),
                    self.__gui_build_fnc_for_tasks_and_units_
                )
            #
            ts.set_start()
            #
            self.set_window_close_connect_to(quit_fnc_)
        else:
            with utl_core.GuiProgressesRunner.create(maximum=len(rsv_entities_map), label='gui-add for task unit') as g_p:
                for i_rsv_entities in rsv_entities_map:
                    g_p.set_update()
                    self.__gui_build_fnc_for_tasks_and_units_(
                        self.__gui_cache_fnc_for_tasks_and_units_by_entities_(i_rsv_entities, thread_stack_index)
                    )

    def __gui_cache_fnc_for_tasks_and_units_by_entities_(self, rsv_entities, thread_stack_index):
        if rsv_entities:
            if rsv_entities[0].type_name == 'task':
                return [
                    rsv_entities,
                    thread_stack_index
                ]
            else:
                # print self._rsv_filter_opt.value
                # print rsv_entities[0]
                # print rsv_entities[0].get_rsv_tasks(**self._rsv_filter_opt.value)
                return [
                    [j for i in rsv_entities for j in i.get_rsv_tasks(**self._rsv_filter_opt.value)],
                    thread_stack_index
                ]

    def __gui_build_fnc_for_tasks_and_units_(self, *args):
        rsv_tasks, thread_stack_index = args[0]
        # print rsv_tasks
        if thread_stack_index == self.__thread_stack_index:
            with self.gui_bustling():
                for i_rsv_task in rsv_tasks:
                    self.__gui_add_task_(i_rsv_task)
                    self.__gui_add_unit_(i_rsv_task)
                    #
                    self.__task_keys.add(i_rsv_task.name)
    #
    def __gui_add_unit_(self, rsv_task):
        def cache_fnc_():
            _list = []
            #
            _show_args = self._available_rsv_show_args
            for _i_keyword, _i_hidden in _show_args:
                if _i_hidden is False:
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
            self.__gui_show_deferred_fnc_for_task_unit_(
                rsv_task, rsv_task_unit_prx_item, data
            )
        #
        task_prx_item = rsv_task.get_obj_gui()
        if task_prx_item is not None:
            visible = self._get_rsv_task_unit_visible_(rsv_task)
            if visible is True:
                rsv_task_unit_prx_item = self._rsv_uint_list_view_0.create_item()
                rsv_task_unit_prx_item.set_gui_dcc_obj(
                    rsv_task, namespace=self.DCC_NAMESPACE
                )
                rsv_task_unit_prx_item.set_gui_attribute('path', rsv_task.get_path())
                rsv_task_unit_prx_item.set_index_draw_enable(True)
                rsv_task_unit_prx_item.set_check_enable(True)
                rsv_task_unit_prx_item.set_sort_name_key(rsv_task.get_name())

                keys = {rsv_task.properties.get(i) or 'unknown' for i in self._resolver.VariantTypes.Mains}
                rsv_task_unit_prx_item.set_keyword_filter_keys_tgt(keys)
                #
                key = rsv_task.path
                # todo: use new filter instance
                # task_prx_item.set_visible_connect_to(
                #     key, rsv_task_unit_prx_item
                # )
                #
                rsv_task_unit_prx_item.set_show_fnc(
                    cache_fnc_, build_fnc_
                )
                task_prx_item.set_status(task_prx_item.ValidatorStatus.Normal)
            else:
                task_prx_item.set_status(task_prx_item.ValidatorStatus.Disable)

    def _get_rsv_task_unit_visible_(self, rsv_task):
        for i_keyword, i_hidden in self._available_rsv_show_args:
            i_rsv_unit = rsv_task.get_rsv_unit(
                keyword=i_keyword
            )
            i_file_path = i_rsv_unit.get_result(version='latest')
            if i_file_path:
                return True
        return False

    def _get_available_rsv_show_args_(self):
        list_ = []
        keywords_args = self._hook_configure.get('resolver.task_unit.keywords') or []
        for i_arg in keywords_args:
            if isinstance(i_arg, six.string_types):
                i_keyword = i_arg
                list_.append((i_keyword, True))
            elif isinstance(i_arg, dict):
                for j_keyword, j_raw in i_arg.items():
                    j_hidden = j_raw.get('hidden') or False
                    j_system_keys = j_raw.get('systems') or []
                    if j_system_keys:
                        if bsc_core.SystemMtd.get_is_matched(j_system_keys):
                            list_.append((j_keyword, j_hidden))
                    else:
                        list_.append((j_keyword, j_hidden))
        return list_

    def __gui_show_deferred_fnc_for_task_unit_(self, rsv_task, prx_item, show_data):
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
                tag=i_rsv_properties.get('workspace_key'),
                frame_size=self.ITEM_ICON_SIZE
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
                bsc_core.ArgDictStringOpt(
                    dict(
                        option_hook_key='actions/movie-open',
                        file=movie_file_path,
                        gui_group_name='movie',
                        gui_name='open movie'
                    )
                ).to_string()
            )
            #
            movie_file_opt = bsc_core.StgFileOpt(movie_file_path)
            show_info_dict['update'] = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                movie_file_opt.get_modify_timestamp(),
                language=1
            )
            show_info_dict['user'] = movie_file_opt.get_user()
            #
            prx_item.connect_press_db_clicked_to(
                execute_fnc
            )
            image_file_path, image_sub_process_cmds = bsc_core.VdoFileOpt(movie_file_path).get_thumbnail_create_args()
            prx_item.set_image(image_file_path)
            prx_item.set_movie_enable(True)
            if image_sub_process_cmds is not None:
                prx_item.set_image_show_args(image_file_path, image_sub_process_cmds)
        else:
            show_info_dict['update'] = 'N/a'
            show_info_dict['user'] = 'N/a'
            prx_item.set_image(
                utl_gui_core.RscIconFile.get('image_loading_failed')
            )
        #
        unit_menu_content = self.get_rsv_task_unit_menu_content(rsv_task)
        if unit_menu_content:
            prx_item.set_menu_content(unit_menu_content)

        prx_item.set_name_dict(show_info_dict)
        r, g, b = bsc_core.RawTextOpt(task).to_rgb_(s_p=25, v_p=35)
        prx_item.set_name_frame_background_color((r, g, b, 127))
        prx_item.set_icon_by_text(step)
        prx_item.set_icons_by_pixmap(pixmaps)
        prx_item.set_tool_tip(
            rsv_task.description
        )
    @classmethod
    def _get_current_application_(cls):
        return bsc_core.ApplicationMtd.get_current()
    @classmethod
    def _get_current_project_(cls):
        return bsc_etr_methods.EtrBase.get_project()

    def _get_resolver_application_filter_(self):
        _ = self._hook_configure.get('resolver.application_filter') or {}
        for k, v in _.items():
            if bsc_core.SystemMtd.get_is_matched(['*-{}'.format(k)]):
                return v
        return self._hook_configure.get('resolver.filter')

    def get_rsv_assets_menu_content(self, rsv_resource):
        hook_keys = self._hook_configure.get(
            'actions.assets.hooks'
        ) or []
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_resource
        )

    def get_rsv_asset_menu_content(self, rsv_resource):
        hook_keys = self._hook_configure.get(
            'actions.asset.hooks'
        ) or []
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_resource
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
            self._session_dict, hook_keys, rsv_task, view_gui=self._rsv_uint_list_view_0
        )
    @classmethod
    def _get_menu_content_by_hook_keys_(cls, session_dict, hooks, *args, **kwargs):
        content = bsc_objects.Dict()
        for i_hook in hooks:
            if isinstance(i_hook, six.string_types):
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
                        if 'gui_sub_icon_name' in i_hook_option:
                            content.set(
                                '{}.properties.sub_icon_name'.format(i_gui_path), i_hook_option.get('gui_sub_icon_name')
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
            session.execute_python_file(python_file_path, session=session)
        #
        rsv_task = args[0]
        session_path = '{}/{}'.format(rsv_task.path, key)
        if session_path in session_dict:
            return session_dict[session_path]
        else:
            python_file_path = ssn_core.SsnHookFileMtd.get_python(key)
            yaml_file_path = ssn_core.SsnHookFileMtd.get_yaml(key)
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
                            if 'view_gui' in kwargs:
                                session.set_view_gui(
                                    kwargs['view_gui']
                                )
                        else:
                            raise TypeError()
                        #
                        session_dict[session_path] = session, execute_fnc
                        return session, execute_fnc
