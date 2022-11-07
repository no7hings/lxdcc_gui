# coding:utf-8
import functools

from lxbasic import bsc_core

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxdatabase.objects as dtb_objects

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core


class AbsPnlAbsLib(prx_widgets.PrxSessionWindow):
    TYPE_ROOT_NAME = 'All Type'
    DTB_NAMESPACE = 'resource'
    THREAD_STEP = 8
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
        self._prx_obj_guide_bar = prx_widgets.PrxGuideBar()
        e_0.set_widget_add(self._prx_obj_guide_bar)
        #
        h_s_0 = prx_widgets.PrxHSplitter()
        e_0.set_widget_add(h_s_0)
        #
        self._type_prx_tree_view = prx_widgets.PrxTreeView()
        h_s_0.set_widget_add(self._type_prx_tree_view)
        self._type_prx_tree_view.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 24
        )
        self._type_prx_tree_view.set_item_select_changed_connect_to(
            self.__execute_gui_refresh_resources_by_selection_
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

        h_s_0.set_stretches([1, 3])

        self.refresh_all()

    def set_variants_restore(self):
        self.__running_threads_stacks = None

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAbsLib, self).__init__(session, *args, **kwargs)

    def refresh_all(self):
        self._dtb_rsc_lib = dtb_objects.DtbResourceLib(
            '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
        )

        self.__gui_refresh_for_all_()

    def __gui_get_type_(self, path):
        return self._type_prx_tree_view._item_dict[path]

    def __gui_get_type_is_exists_(self, path):
        return path in self._type_prx_tree_view._item_dict

    def __gui_refresh_for_all_(self):
        self._type_prx_tree_view.set_restore()
        self.__restore_thread_stack_()
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
            prx_item.set_checked(True)
            return prx_item
        else:
            return self._type_prx_tree_view._item_dict[path]

    def __restore_thread_stack_(self):
        if self.__running_threads_stacks:
            [i.set_kill() for i in self.__running_threads_stacks]
        #
        self.__running_threads_stacks = []

    def __gui_refresh_for_all_types_(self):
        def post_fnc_():
            self._end_timestamp = bsc_core.SystemMtd.get_timestamp()
            #
            utl_core.Log.set_module_result_trace(
                'load all types',
                'count={}, cost-time="{}"'.format(
                    self._count,
                    bsc_core.IntegerMtd.second_to_time_prettify(self._end_timestamp - self._start_timestamp)
                )
            )
        #
        self._count = 0
        self._start_timestamp = bsc_core.SystemMtd.get_timestamp()
        #
        dtb_categories = self._dtb_rsc_lib.get_categories()
        dtb_categories_map = bsc_core.ListMtd.set_grid_to(
            dtb_categories, self.THREAD_STEP
        )
        # use thread
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_dtb_categories in dtb_categories_map:
                [self.__gui_add_category_(i) for i in i_dtb_categories]
                ts.set_register(
                    cache_fnc=functools.partial(self.__gui_cache_fnc_for_types_by_categories_, i_dtb_categories),
                    build_fnc=self.__gui_build_fnc_for_types_
                )
                #
                ts.set_start()
        else:
            with utl_core.gui_progress(maximum=len(dtb_categories), label='gui-add for type') as g_p:
                for i_dtb_categories in dtb_categories_map:
                    g_p.set_update()
                    [self.__gui_add_category_(i) for i in i_dtb_categories]
                    self.__gui_build_fnc_for_types_(
                        self.__gui_cache_fnc_for_types_by_categories_(i_dtb_categories)
                    )

    def __gui_add_category_(self, dtb_category):
        path = dtb_category.path
        if self.__gui_get_type_is_exists_(path) is False:
            parent_gui = self.__gui_get_type_(bsc_core.DccPathDagOpt(path).get_parent_path())

            prx_item = parent_gui.set_child_add(
                dtb_category.gui_name,
                icon=utl_gui_core.RscIconFile.get('file/folder'),
            )
            prx_item.set_checked(True)
            prx_item.set_gui_dcc_obj(dtb_category, namespace=self.DTB_NAMESPACE)
            self._type_prx_tree_view._item_dict[path] = prx_item
            return prx_item
        else:
            return self._type_prx_tree_view._item_dict[path]

    def __gui_cache_fnc_for_types_by_categories_(self, dtb_categories):
        dtb_types = [j for i in dtb_categories for j in self._dtb_rsc_lib.get_types(filters=[('category', 'is', i.name)])]
        self._count += len(dtb_types)
        return dtb_types

    def __gui_build_fnc_for_types_(self, dtb_types):
        [self.__gui_add_type_(i) for i in dtb_types]

    def __gui_add_type_(self, dtb_type):
        path = dtb_type.path
        if self.__gui_get_type_is_exists_(path) is False:
            parent_gui = self.__gui_get_type_(bsc_core.DccPathDagOpt(path).get_parent_path())
            name = dtb_type.name
            gui_name = dtb_type.gui_name
            prx_item = parent_gui.set_child_add(
                gui_name,
                icon=utl_gui_core.RscIconFile.get('file/files'),
            )
            prx_item.set_checked(True)
            prx_item.set_gui_dcc_obj(dtb_type, namespace=self.DTB_NAMESPACE)
            self._type_prx_tree_view._item_dict[path] = prx_item
            prx_item.set_keyword_filter_keys_tgt_update([name, gui_name])
            return prx_item
        else:
            return self._type_prx_tree_view._item_dict[path]

    def __execute_gui_refresh_resources_by_selection_(self):
        entity_prx_items = self._type_prx_tree_view.get_selected_items()
        #
        self.__restore_thread_stack_()
        #
        self._resource_prx_list_view.set_clear()
        if entity_prx_items:
            lib_entities = [i.get_gui_dcc_obj(self.DTB_NAMESPACE) for i in entity_prx_items]
            lib_entities = [i for i in lib_entities if i is not None]
            self.__gui_refresh_for_resources_by_entities_(lib_entities)

    def __gui_refresh_for_resources_by_entities_(self, lib_entities):
        def post_fnc_():
            self._end_timestamp = bsc_core.SystemMtd.get_timestamp()
            #
            utl_core.Log.set_module_result_trace(
                'load all resources',
                'count={}, cost-time="{}"'.format(
                    self._count,
                    bsc_core.IntegerMtd.second_to_time_prettify(self._end_timestamp - self._start_timestamp)
                )
            )
        #
        self._count = 0
        self._start_timestamp = bsc_core.SystemMtd.get_timestamp()
        #
        dtb_entities_map = bsc_core.ListMtd.set_grid_to(
            lib_entities, self.THREAD_STEP
        )
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_dtb_entities in dtb_entities_map:
                ts.set_register(
                    functools.partial(self.__gui_cache_fnc_for_resources_by_entities_batch_, i_dtb_entities),
                    self.__gui_build_fnc_for_resources_batch_
                )
            ts.set_start()
        else:
            with utl_core.gui_progress(maximum=len(dtb_entities_map), label='batch gui-add resource') as g_p:
                for i_dtb_entities in dtb_entities_map:
                    g_p.set_update()
                    self.__gui_build_fnc_for_resources_batch_(
                        self.__gui_cache_fnc_for_resources_by_entities_batch_(i_dtb_entities)
                    )

    def __gui_cache_fnc_for_resources_by_entities_batch_(self, lib_entities):
        if lib_entities:
            if lib_entities[0].entity_type == self._dtb_rsc_lib.EntityTypes.Category:
                return [
                    j
                    for i in lib_entities
                    for j in self._dtb_rsc_lib.get_resources(
                        filters=[('category', 'is', i.name)]
                    )
                ]
            elif lib_entities[0].entity_type == self._dtb_rsc_lib.EntityTypes.Type:
                return [
                    j
                    for i in lib_entities
                    for j in self._dtb_rsc_lib.get_resources(
                        filters=[('category', 'is', i.category), ('type', 'is', i.name)]
                    )
                ]

    def __gui_build_fnc_for_resources_batch_(self, resources):
        def post_fnc_():
            pass

        # print len(resources)
        # for i_resource in resources:
        #     self.__gui_add_resource_(i_resource)
        resources_map = bsc_core.ListMtd.set_grid_to(
            resources, self.THREAD_STEP
        )
        # self._qt_thread_enable = False
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_resources in resources_map:
                ts.set_register(
                    functools.partial(self.__gui_cache_fnc_for_resources_, i_resources),
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

    def __gui_cache_fnc_for_resources_(self, resources):
        return resources

    def __gui_build_fnc_for_resources_(self, resources):
        for i_resource in resources:
            self.__gui_add_resource_(i_resource)

    def __gui_add_resource_(self, resource):
        def cache_fnc_():
            _list = []
            return _list

        def build_fnc_(data):
            self.__gui_show_deferred_fnc_for_resource_(
                resource, prx_item, data
            )

        path = resource.path
        prx_item = self._resource_prx_list_view.set_item_add()
        prx_item.set_gui_dcc_obj(
            resource, namespace=self.DTB_NAMESPACE
        )
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )

    def __gui_show_deferred_fnc_for_resource_(self, resource, prx_item, data):
        type_name = resource.type
        prx_item.set_check_enable(True)
        prx_item.set_name_dict(
            {'name': resource.name}
        )
        prx_item.set_file_icons(
            icon_names=['application/python']*1
        )

        prx_item.set_image(
            utl_gui_core.RscIconFile.get('image_loading_failed_error')
        )

        r, g, b = bsc_core.TextOpt(type_name).to_rgb()
        prx_item.set_name_frame_background_color((r, g, b, 127))
