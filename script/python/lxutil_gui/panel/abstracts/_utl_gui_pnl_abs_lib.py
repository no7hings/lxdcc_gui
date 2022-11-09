# coding:utf-8
import fnmatch

import collections

import functools

from lxbasic import bsc_core

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxdatabase.objects as dtb_objects

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core


class AbsPnlAbsLib(prx_widgets.PrxSessionWindow):
    TYPE_ROOT_TYPE = 'root'
    TYPE_ROOT_NAME = 'All'
    DTB_NAMESPACE = 'resource'
    THREAD_STEP = 8
    FILTER_MAXIMUM = 50
    def set_all_setup(self):
        self._item_frame_size = self._session.gui_configure.get('item_frame_size')
        self._item_icon_frame_size = self._session.gui_configure.get('item_icon_frame_size')
        self._item_icon_size = self._session.gui_configure.get('item_icon_size')

        s = prx_widgets.PrxScrollArea()
        self.set_widget_add(s)
        #
        e_0 = prx_widgets.PrxExpandedGroup()
        s.set_widget_add(e_0)
        e_0.set_name('viewers')
        e_0.set_expanded(True)
        #
        self._guide_bar = prx_widgets.PrxGuideBar()
        e_0.set_widget_add(self._guide_bar)
        #
        h_s_0 = prx_widgets.PrxHSplitter()
        e_0.set_widget_add(h_s_0)
        #
        v_s_0 = prx_widgets.PrxVSplitter()
        h_s_0.set_widget_add(v_s_0)
        #
        self._type_prx_tree_view = prx_widgets.PrxTreeView()
        v_s_0.set_widget_add(self._type_prx_tree_view)
        self._type_prx_tree_view.set_selection_use_single()
        self._type_prx_tree_view.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 24
        )
        self._type_prx_tree_view.set_item_select_changed_connect_to(
            self.__execute_gui_refresh_resources_by_selection_
        )
        self._type_prx_tree_view.set_filter_completion_gain_fnc(
            self.__type_completion_gain_fnc_
        )
        self._type_prx_tree_view.set_item_select_changed_connect_to(
            self.__refresh_guide_bar_
        )

        self._property_prx_tree_view = prx_widgets.PrxTreeView()
        v_s_0.set_widget_add(self._property_prx_tree_view)
        self._property_prx_tree_view.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 24
        )
        #
        self._resource_prx_list_view = prx_widgets.PrxListView()
        h_s_0.set_widget_add(self._resource_prx_list_view)
        self._resource_prx_list_view.set_item_frame_size(*self._item_frame_size)
        self._resource_prx_list_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._resource_prx_list_view.set_item_icon_size(*self._item_icon_size)
        self._resource_prx_list_view.set_item_icon_frame_draw_enable(True)
        self._resource_prx_list_view.set_item_name_frame_draw_enable(True)
        self._resource_prx_list_view.set_item_image_frame_draw_enable(True)
        self._resource_prx_list_view.set_item_select_changed_connect_to(
            self.__refresh_guide_bar_
        )
        h_s_0.set_stretches([1, 3])
        v_s_0.set_stretches([1, 1])

        self.refresh_all()

    def set_variants_restore(self):
        self.__running_threads_stacks = None

        self.__thread_stack_index = 0

        self.__filter_type_keys = []

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAbsLib, self).__init__(session, *args, **kwargs)

    def refresh_all(self):
        self._dtb_rsc_lib = dtb_objects.DtbResourceLib(
            '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
        )

        self.__gui_refresh_for_all_()
    
    def __refresh_guide_bar_(self):
        def get_path_args_fnc_(dtb_entity_):
            types = [
                self._dtb_rsc_lib.EntityTypes.TypeGroup,
                self._dtb_rsc_lib.EntityTypes.Type,
                self._dtb_rsc_lib.EntityTypes.Resource
            ]
            _dict = collections.OrderedDict()
            path = dtb_entity_.path
            path_opt = bsc_core.DccPathDagOpt(path)
            comps = path_opt.get_components()
            comps.reverse()
            c = len(comps)
            for seq, i in enumerate(comps[1:]):
                i_type = types[seq]
                i_name = i.name
                _dict[i_name] = i_type
            return _dict
        #
        dtb_entity = None
        resource_selected_prx_items = self._resource_prx_list_view.get_selected_items()
        if resource_selected_prx_items:
            dtb_entity = resource_selected_prx_items[-1].get_gui_dcc_obj(self.DTB_NAMESPACE)
        else:
            tree_selected_prx_items = self._type_prx_tree_view.get_selected_items()
            if tree_selected_prx_items:
                dtb_entity = tree_selected_prx_items[-1].get_gui_dcc_obj(self.DTB_NAMESPACE)

        if dtb_entity is not None:
            self._guide_bar.set_path_args(get_path_args_fnc_(dtb_entity))

    def __type_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = fnmatch.filter(
                self.__filter_type_keys, '*{}*'.format(keyword)
            )
            return bsc_core.TextsMtd.set_sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def __restore_thread_stack_(self):
        if self.__running_threads_stacks:
            [i.set_kill() for i in self.__running_threads_stacks]
        #
        self.__running_threads_stacks = []

    def __gui_get_type_(self, path):
        return self._type_prx_tree_view._item_dict[path]

    def __gui_get_type_is_exists_(self, path):
        return path in self._type_prx_tree_view._item_dict

    def __gui_refresh_for_all_(self):
        self._type_prx_tree_view.set_restore()
        self._guide_bar.set_clear()
        #
        self.__gui_add_type_root_()
        self.__gui_refresh_for_all_types_()

    def __gui_add_type_root_(self):
        path = '/'
        if self.__gui_get_type_is_exists_(path) is False:
            prx_item = self._type_prx_tree_view.set_item_add(
                self.TYPE_ROOT_NAME,
                icon=utl_gui_core.RscIconFile.get('file/folder'),
            )
            self._type_prx_tree_view._item_dict[path] = prx_item
            prx_item.set_expanded(True)
            # prx_item.set_checked(True)
            return prx_item
        else:
            return self._type_prx_tree_view._item_dict[path]

    def __gui_refresh_for_all_types_(self):
        def post_fnc_():
            self._end_timestamp = bsc_core.SystemMtd.get_timestamp()
            #
            utl_core.Log.set_module_result_trace(
                'load all types',
                'count={}, cost-time="{}"'.format(
                    self.__type_count,
                    bsc_core.IntegerMtd.second_to_time_prettify(self._end_timestamp - self.__start_timestamp)
                )
            )

        def quit_fnc_():
            ts.set_quit()
        #
        self.__type_count = 0
        self.__start_timestamp = bsc_core.SystemMtd.get_timestamp()
        #
        dtb_type_groups = self._dtb_rsc_lib.get_entities(
            entity_type=self._dtb_rsc_lib.EntityTypes.TypeGroup,
        )
        dtb_type_groups_map = bsc_core.ListMtd.set_grid_to(
            dtb_type_groups, self.THREAD_STEP
        )
        # use thread
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            ts.run_finished.connect(post_fnc_)
            for i_dtb_type_groups in dtb_type_groups_map:
                [self.__gui_add_type_group_(i) for i in i_dtb_type_groups]
                ts.set_register(
                    cache_fnc=functools.partial(self.__gui_cache_fnc_for_types_by_type_groups_, i_dtb_type_groups),
                    build_fnc=self.__gui_build_fnc_for_types_
                )
                #
                ts.set_start()
        else:
            with utl_core.gui_progress(maximum=len(dtb_type_groups), label='gui-add for type') as g_p:
                for i_dtb_type_groups in dtb_type_groups_map:
                    g_p.set_update()
                    [self.__gui_add_type_group_(i) for i in i_dtb_type_groups]
                    self.__gui_build_fnc_for_types_(
                        self.__gui_cache_fnc_for_types_by_type_groups_(i_dtb_type_groups)
                    )
    # for type group
    def __gui_add_type_group_(self, dtb_type_group):
        path = dtb_type_group.path
        if self.__gui_get_type_is_exists_(path) is False:
            parent_gui = self.__gui_get_type_(bsc_core.DccPathDagOpt(path).get_parent_path())

            prx_item = parent_gui.set_child_add(
                dtb_type_group.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_type_group.gui_icon_name),
            )
            # prx_item.set_checked(True)
            prx_item.set_gui_dcc_obj(dtb_type_group, namespace=self.DTB_NAMESPACE)
            self._type_prx_tree_view._item_dict[path] = prx_item
            return prx_item
        else:
            return self._type_prx_tree_view._item_dict[path]
    # for type
    def __gui_cache_fnc_for_types_by_type_groups_(self, dtb_type_groups):
        return [
            j
            for i in dtb_type_groups
            for j in self._dtb_rsc_lib.get_entities(
                entity_type=self._dtb_rsc_lib.EntityTypes.Type,
                filters=[
                    ('group', 'is', i.path),
                ]
            )
        ]

    def __gui_build_fnc_for_types_(self, dtb_types):
        [self.__gui_add_type_(i) for i in dtb_types]
        self.__filter_type_keys.extend([i.gui_name for i in dtb_types])
        self.__type_count += len(dtb_types)

    def __gui_add_type_(self, dtb_type):
        path = dtb_type.path
        if self.__gui_get_type_is_exists_(path) is False:
            parent_gui = self.__gui_get_type_(bsc_core.DccPathDagOpt(path).get_parent_path())
            name = dtb_type.name
            gui_name = dtb_type.gui_name
            prx_item = parent_gui.set_child_add(
                gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_type.gui_icon_name),
            )
            # prx_item.set_checked(True)
            prx_item.set_gui_dcc_obj(dtb_type, namespace=self.DTB_NAMESPACE)
            self._type_prx_tree_view._item_dict[path] = prx_item
            prx_item.update_keyword_filter_keys_tgt([name, gui_name])
            return prx_item
        else:
            return self._type_prx_tree_view._item_dict[path]

    def __execute_gui_refresh_resources_by_selection_(self):
        entity_prx_items = self._type_prx_tree_view.get_selected_items()
        #
        self.__restore_thread_stack_()
        #
        self.__thread_stack_index += 1
        #
        self._resource_prx_list_view.set_clear()
        if entity_prx_items:
            entity_prx_item = entity_prx_items[-1]
            dtb_entity = entity_prx_item.get_gui_dcc_obj(self.DTB_NAMESPACE)
            if dtb_entity is not None:
                self.__batch_gui_refresh_for_resources_by_entities_([dtb_entity], self.__thread_stack_index)

    def __batch_gui_refresh_for_resources_by_entities_(self, dtb_entities, thread_stack_index):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.set_quit()
        #
        dtb_entities_map = bsc_core.ListMtd.set_grid_to(
            dtb_entities, self.THREAD_STEP
        )
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_dtb_entities in dtb_entities_map:
                ts.set_register(
                    functools.partial(self.__batch_gui_cache_fnc_for_resources_by_entities_, i_dtb_entities, thread_stack_index),
                    self.__batch_gui_build_fnc_for_resources_
                )
            ts.set_start()
        else:
            with utl_core.gui_progress(maximum=len(dtb_entities_map), label='batch gui-add resource') as g_p:
                for i_dtb_entities in dtb_entities_map:
                    g_p.set_update()
                    self.__batch_gui_build_fnc_for_resources_(
                        self.__batch_gui_cache_fnc_for_resources_by_entities_(i_dtb_entities, thread_stack_index)
                    )

    def __batch_gui_cache_fnc_for_resources_by_entities_(self, dtb_entities, thread_stack_index):
        if dtb_entities:
            if dtb_entities[0].entity_type == self._dtb_rsc_lib.EntityTypes.TypeGroup:
                return [
                    j
                    for i in dtb_entities
                    for j in self._dtb_rsc_lib.get_entities(
                        entity_type=self._dtb_rsc_lib.EntityTypes.Resource,
                        filters=[
                            ('group', 'startswith', i.path)
                        ]
                    )
                ], thread_stack_index
            elif dtb_entities[0].entity_type == self._dtb_rsc_lib.EntityTypes.Type:
                return [
                    j
                    for i in dtb_entities
                    for j in self._dtb_rsc_lib.get_entities(
                        entity_type=self._dtb_rsc_lib.EntityTypes.Resource,
                        filters=[
                            ('group', 'is', i.path)
                        ]
                    )
                ], thread_stack_index

    def __batch_gui_build_fnc_for_resources_(self, *args):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.set_quit()

        if args[0] is None:
            return

        dtb_resources, thread_stack_index = args[0]
        if thread_stack_index == self.__thread_stack_index:
            resources_map = bsc_core.ListMtd.set_grid_to(
                dtb_resources, self.THREAD_STEP
            )
            if self._qt_thread_enable is True:
                ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
                self.__running_threads_stacks.append(ts)
                ts.run_finished.connect(post_fnc_)
                for i_resources in resources_map:
                    ts.set_register(
                        functools.partial(self.__gui_cache_fnc_for_resources_, i_resources, thread_stack_index),
                        self.__gui_build_fnc_for_resources_
                    )
                ts.set_start()
            else:
                with utl_core.gui_progress(maximum=len(resources_map), label='gui-add resources') as g_p:
                    for i_resources in resources_map:
                        g_p.set_update()
                        self.__gui_build_fnc_for_resources_(
                            self.__gui_cache_fnc_for_resources_(i_resources)
                        )

    def __gui_cache_fnc_for_resources_(self, dtb_resources, thread_stack_index):
        return dtb_resources, thread_stack_index

    def __gui_build_fnc_for_resources_(self, *args):
        dtb_resources, thread_stack_index = args[0]

        if args[0] is None:
            return

        if thread_stack_index == self.__thread_stack_index:
            for i_resource in dtb_resources:
                self.__gui_add_resource_(i_resource)

    def __gui_add_resource_(self, resource):
        def cache_fnc_():
            _list = []
            return _list

        def build_fnc_(data):
            self.__gui_show_deferred_fnc_for_resource_(
                resource, prx_item, data
            )

        prx_item = self._resource_prx_list_view.set_item_add()
        prx_item.set_gui_dcc_obj(
            resource, namespace=self.DTB_NAMESPACE
        )
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )

    def __gui_show_deferred_fnc_for_resource_(self, resource, prx_item, data):
        group = resource.group
        prx_item.set_check_enable(True)
        prx_item.set_name_dict(
            {'name': resource.name}
        )
        # prx_item.set_file_icons(
        #     icon_names=['application/python']*1
        # )

        prx_item.set_image(
            utl_gui_core.RscIconFile.get('image_loading_failed_error')
        )

        r, g, b = bsc_core.TextOpt(group).to_rgb()
        # prx_item.set_name_frame_background_color((r, g, b, 127))
