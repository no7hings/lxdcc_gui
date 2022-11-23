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

import lxsession.commands as ssn_commands


class GuiTypeOpt(object):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database, prx_view):
        self._window = window
        self._session = session
        self._dtb = database
        self._tree_prx_view = prx_view

        self._item_dict = self._tree_prx_view._item_dict

        self._keys = set()

    def restore(self):
        self._tree_prx_view.set_clear()
        #
        self._keys.clear()

    def gui_get_is_exists(self, path):
        return path in self._item_dict

    def gui_get(self, path):
        return self._item_dict[path]

    def gui_add_root(self):
        path = '/'
        if self.gui_get_is_exists(path) is False:
            prx_item = self._tree_prx_view.set_item_add(
                self.ROOT_NAME,
                icon=utl_gui_core.RscIconFile.get('database/all'),
            )
            self._item_dict[path] = prx_item
            prx_item.set_expanded(True)
            return prx_item
        return self.gui_get(path)

    def gui_add_all_category_groups(self):
        dtb_category_groups = self._dtb.get_entities(
            entity_type=self._dtb.EntityTypes.CategoryGroup,
            filters=[
                ('kind', 'is', self._dtb.Kinds.ResourceCategoryGroup)
            ]
        )
        [self.gui_add_category_group(i) for i in dtb_category_groups]

    def gui_add_category_group(self, dtb_entity):
        path = dtb_entity.path
        if self.gui_get_is_exists(path) is False:
            parent_gui = self.gui_get(dtb_entity.group)
            prx_item = parent_gui.set_child_add(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            self._tree_prx_view._item_dict[path] = prx_item
            #
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            prx_item.set_tool_tip(dtb_entity.to_string())
            prx_item.set_expanded(True)
            #
            menu_content = self.get_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            return prx_item
        return self.gui_get(path)

    def gui_add_all_categories(self):
        pass

    def gui_add_category(self, dtb_entity):
        path = dtb_entity.path
        if self.gui_get_is_exists(path) is False:
            parent_gui = self.gui_get(dtb_entity.group)
            prx_item = parent_gui.set_child_add(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            self._tree_prx_view._item_dict[path] = prx_item
            #
            prx_item.set_status(
                prx_item.ValidatorStatus.Disable
            )
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            self._tree_prx_view.set_item_expand_connect_to(
                prx_item,
                lambda *args, **kwargs: self.__execute_gui_refresh_for_type_by_category_expand_changed_(prx_item),
                time=100
            )
            menu_content = self.get_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            return prx_item
        return self.gui_get(path)

    def __execute_gui_refresh_for_type_by_category_expand_changed_(self, prx_item):
        child_prx_items = prx_item.get_children()
        for i_prx_item in child_prx_items:
            i_dtb_entity = i_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
            if i_dtb_entity is not None:
                if i_dtb_entity.entity_type == self._dtb.EntityTypes.Type:
                    i_dtb_assigns = self._dtb.get_entities(
                        entity_type=self._dtb.EntityTypes.Types,
                        filters=[
                            ('kind', 'is', self._dtb.Kinds.ResourceType),
                            #
                            ('value', 'is', i_dtb_entity.path),
                        ]
                    )
                    i_count = len(i_dtb_assigns)
                    i_prx_item.set_name(str(i_count), 1)
                    if i_count > 0:
                        i_prx_item.set_status(
                            prx_item.ValidatorStatus.Normal
                        )
                    else:
                        i_prx_item.set_status(
                            prx_item.ValidatorStatus.Disable
                        )

    def gui_add_type(self, dtb_entity):
        path = dtb_entity.path
        if self.gui_get_is_exists(path) is False:
            parent_gui = self.gui_get(dtb_entity.group)
            parent_gui.set_status(parent_gui.ValidatorStatus.Normal)

            name = dtb_entity.name
            gui_name = dtb_entity.gui_name
            prx_item = parent_gui.set_child_add(
                gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            self._tree_prx_view._item_dict[path] = prx_item
            prx_item.set_status(prx_item.ValidatorStatus.Disable)
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            # for keyword filter
            prx_item.update_keyword_filter_keys_tgt([name, gui_name])
            #
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            menu_content = self.get_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            return prx_item
        return self.gui_get(path)
    # for type
    def gui_cache_fnc_for_types_by_categories(self, dtb_categories):
        dtb_types = self._dtb.get_entities(
            entity_type=self._dtb.EntityTypes.Type,
            filters=[
                ('group', 'in', [i.path for i in dtb_categories]),
            ]
        )
        self._keys.update(set([i.name for i in dtb_types]))
        return dtb_types

    def gui_build_fnc_for_types(self, dtb_types):
        [self.gui_add_type(i) for i in dtb_types]

    def get_menu_content(self, dtb_entity):
        options = []
        c = self._session.configure.get(
            'actions.{}.option-hooks'.format(dtb_entity.entity_type)
        )
        if c:
            for i in c:
                if isinstance(i, dict):
                    i_key = i.keys()[0]
                    i_value = i.values()[0]
                else:
                    i_key = i
                    i_value = {}
                #
                i_kwargs = dict(
                    option_hook_key=i_key,
                    #
                    window_unique_id=self._window.get_window_unique_id(),
                    database=self._dtb.get_database(),
                    #
                    entity_type=dtb_entity.entity_type,
                    entity=dtb_entity.path,
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.KeywordArgumentsOpt(i_kwargs).to_string(),
                )
            return ssn_commands.get_menu_content_by_hook_options(options)


class GuiTagOpt(object):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database, tree_prx_view):
        self._window = window
        self._session = session
        self._dtb = database
        self._tree_prx_view = tree_prx_view
        #
        self._key_item_dict = {}
        self._value_item_dict = {}
        self._count_dict = {}

        self._tag_group_kinds = [
            self._dtb.Kinds.ResourceSemanticTagGroup,
            self._dtb.Kinds.ResourcePropertyTagGroup
        ]

    def restore(self):
        self._tree_prx_view.set_clear()
        self._key_item_dict.clear()
        self._value_item_dict.clear()
        self._count_dict.clear()

    def gui_get_group_is_exists(self, path):
        return path in self._key_item_dict

    def gui_get_group(self, path):
        return self._key_item_dict[path]

    def gui_add_root(self):
        path = '/'
        if self.gui_get_group_is_exists(path) is False:
            prx_item = self._tree_prx_view.set_item_add(
                self.ROOT_NAME,
                icon=utl_gui_core.RscIconFile.get('database/all'),
            )
            self._key_item_dict[path] = prx_item
            prx_item.set_expanded(True)
            #
            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)
            return prx_item
        else:
            return self.gui_get_group(path)

    def gui_add_all_groups(self):
        dtb_tags = self._dtb.get_entities(
            entity_type=self._dtb.EntityTypes.TagGroup,
            filters=[
                ('kind', 'in', self._tag_group_kinds)
            ]
        )
        [self.gui_add_group(i) for i in dtb_tags]

    def gui_add_group(self, dtb_entity):
        path = dtb_entity.path
        if self.gui_get_group_is_exists(path) is False:
            parent_gui = self.gui_get_group(dtb_entity.group)
            prx_item = parent_gui.set_child_add(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            self._key_item_dict[path] = prx_item
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            #
            prx_item.set_status(prx_item.ValidatorStatus.Disable)
            #
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)
            #
            return prx_item
        else:
            return self.gui_get_group(path)

    def gui_get_is_exists(self, path):
        return path in self._value_item_dict

    def gui_get(self, path):
        return self._value_item_dict[path]

    def gui_add(self, dtb_entity):
        path = dtb_entity.path
        if self.gui_get_is_exists(path) is False:
            parent_path = dtb_entity.group
            parent_gui = self.gui_get_group(parent_path)
            prx_item = parent_gui.set_child_add(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            parent_gui.set_status(parent_gui.ValidatorStatus.Normal)
            self._value_item_dict[path] = prx_item
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            #
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)
            #
            prx_item.set_name('0', 1)
            return prx_item
        return self.gui_get(path)

    def gui_add_by_path(self, path):
        if self.gui_get_is_exists(path) is False:
            path_opt = bsc_core.DccPathDagOpt(path)
            parent_path = path_opt.get_parent_path()
            parent_gui = self.gui_get_group(parent_path)
            gui_name = bsc_core.StrUnderlineOpt(path_opt.name).to_prettify()
            prx_item = parent_gui.set_child_add(
                gui_name,
                icon=utl_gui_core.RscIconFile.get('database/tag'),
            )
            parent_gui.set_status(parent_gui.ValidatorStatus.Normal)
            self._value_item_dict[path] = prx_item
            #
            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)
            #
            prx_item.set_name('0', 1)
            return prx_item
        return self.gui_get(path)

    def reset(self):
        self._count_dict.clear()
        self._value_item_dict.clear()
        for i_k, i_v in self._key_item_dict.items():
            i_dtb_entity = i_v.get_gui_dcc_obj(
                namespace=self.DCC_NAMESPACE
            )
            i_v.set_checked(False)
            if i_dtb_entity is not None:
                if i_dtb_entity.kind in self._tag_group_kinds:
                    i_v.clear_children()
                    i_v.set_status(
                        i_v.ValidatorStatus.Disable
                    )

    def register_count(self, resource_path, tag_path):
        self._count_dict.setdefault(
            tag_path, set()
        ).add(resource_path)

    def gui_register(self, dtb_tag):
        if isinstance(dtb_tag, (str, unicode)):
            tag_path = dtb_tag
            prx_item = self.gui_add_by_path(dtb_tag)
        elif isinstance(dtb_tag, dict):
            tag_path = dtb_tag.path
            prx_item = self.gui_add(dtb_tag)
        else:
            raise TypeError()

        if tag_path in self._count_dict:
            prx_item.set_name(str(len(self._count_dict[tag_path])), 1)

    def get_filter_data(self):
        dict_ = {}
        for i_k, i_v in self._value_item_dict.items():
            if i_v.get_is_checked() is True:
                i_key = bsc_core.DccPathDagOpt(i_k).get_parent_path()
                dict_.setdefault(i_key, []).append(i_k)
        return dict_


class GuiNodeOpt(object):
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database, list_prx_view):
        self._window = window
        self._session = session
        self._dtb = database
        self._list_prx_view = list_prx_view

        self._item_dict = self._list_prx_view._item_dict

        self._keys = set()

    def restore(self):
        self._list_prx_view.set_clear()
        self._keys.clear()

    def gui_get_is_exists(self, path):
        return path in self._item_dict

    def gui_get(self, path):
        return self._item_dict[path]

    def __gui_show_deferred_fnc_(self, dtb_resource, prx_item, semantic_tag_filter_data, data):
        # type_ = dtb_resource.type
        prx_item.set_check_enable(True)

        # r, g, b = bsc_core.TextOpt(type_).to_rgb_()
        # prx_item.set_name_frame_background_color((r, g, b, 127))
        name_dict = collections.OrderedDict()
        name_dict['name'] = dtb_resource.gui_name
        for i_k, i_v in semantic_tag_filter_data.items():
            name_dict[bsc_core.DccPathDagOpt(i_k).name] = ', '.join([bsc_core.DccPathDagOpt(j).name for j in i_v])

        prx_item.set_image(
            utl_gui_core.RscIconFile.get('image_loading_failed_error')
        )

        dtb_version_port = self._dtb.get_entity(
            entity_type=self._dtb.EntityTypes.Attribute,
            filters=[
                ('node', 'is', dtb_resource.path),
                ('port', 'is', 'version')
            ]
        )

        menu_content = self.get_menu_content(dtb_resource)
        prx_item.set_menu_content(menu_content)

        prx_item.set_name_dict(
            name_dict
        )

        prx_item.set_tool_tip(dtb_resource.to_string())

        preview_image_dtb_port = self._dtb.get_entity(
            entity_type=self._dtb.EntityTypes.Attribute,
            filters=[
                ('node', 'is', dtb_version_port.value),
                ('port', 'is', 'image-preview-png-file'),
            ],
            new_connection=False
        )
        if preview_image_dtb_port:
            image = preview_image_dtb_port.value
            if bsc_core.StorageFileOpt(image).get_is_exists() is True:
                prx_item.set_image(
                    image
                )
                image_file_path, image_sub_process_cmds = bsc_core.ImageOpt(image).get_thumbnail_create_args(
                    width=256, ext='.png'
                )
                prx_item.set_image(image_file_path)
                if image_sub_process_cmds is not None:
                    prx_item.set_image_show_args(image_file_path, image_sub_process_cmds)
        else:
            prx_item.set_image(
                utl_gui_core.RscIconFile.get('image_loading_failed_error')
            )

    def get_menu_content(self, dtb_resource):
        options = []
        c = self._session.configure.get(
            'actions.resource.option-hooks'
        )
        for i in c:
            if isinstance(i, dict):
                i_key = i.keys()[0]
                i_value = i.values()[0]
                i_kwargs = dict(
                    option_hook_key=i_key,
                    #
                    window_unique_id=self._window.get_window_unique_id(),
                    database=self._dtb.get_database(),
                    #
                    entity_type=dtb_resource.entity_type,
                    entity=dtb_resource.path,
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.KeywordArgumentsOpt(i_kwargs).to_string(),
                )
        return ssn_commands.get_menu_content_by_hook_options(options)

    def gui_add(self, dtb_resource, semantic_tag_filter_data):
        def cache_fnc_():
            _list = []
            return _list

        def build_fnc_(data):
            self.__gui_show_deferred_fnc_(
                dtb_resource, prx_item, semantic_tag_filter_data, data
            )

        path = dtb_resource.path
        if self.gui_get_is_exists(path) is False:
            self._keys.add(dtb_resource.name)
            #
            prx_item = self._list_prx_view.set_item_add()

            # print path, semantic_tag_filter_data
            prx_item.get_item()._set_item_semantic_tag_filter_key_update_(semantic_tag_filter_data)

            prx_item.set_gui_dcc_obj(
                dtb_resource, namespace=self.DCC_NAMESPACE
            )
            prx_item.set_show_fnc(
                cache_fnc_, build_fnc_
            )
            self._item_dict[path] = prx_item

            return prx_item
        return self.gui_get(path)


class AbsPnlAbsLib(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = 'database'
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
        self._type_prx_view = prx_widgets.PrxTreeView()
        v_s_0.set_widget_add(self._type_prx_view)
        self._type_prx_view.set_selection_use_single()
        self._type_prx_view.set_header_view_create(
            [('type', 3), ('count', 1)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 48
        )
        self._type_prx_view.set_item_select_changed_connect_to(
            self.__execute_gui_refresh_for_resources_by_type_selection_
        )
        self._type_prx_view.set_filter_completion_gain_fnc(
            self.__type_completion_gain_fnc_
        )
        self._type_prx_view.set_item_select_changed_connect_to(
            self.__refresh_guide_bar_
        )
        #
        self._tag_prx_view = prx_widgets.PrxTreeView()
        v_s_0.set_widget_add(self._tag_prx_view)
        self._tag_prx_view.set_selection_disable()
        self._tag_prx_view.set_header_view_create(
            [('tag', 3), ('count', 1)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 48
        )
        self._tag_prx_view.set_item_check_changed_connect_to(
            self.__execute_gui_refresh_for_resources_by_property_check_
        )
        # resource
        self._resource_prx_view = prx_widgets.PrxListView()
        h_s_0.set_widget_add(self._resource_prx_view)
        self._resource_prx_view.set_item_frame_size(*self._item_frame_size)
        self._resource_prx_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._resource_prx_view.set_item_icon_size(*self._item_icon_size)
        self._resource_prx_view.set_item_icon_frame_draw_enable(True)
        self._resource_prx_view.set_item_name_frame_draw_enable(True)
        self._resource_prx_view.set_item_names_draw_range([None, 1])
        self._resource_prx_view.set_item_image_frame_draw_enable(True)
        self._resource_prx_view.set_item_select_changed_connect_to(
            self.__refresh_guide_bar_
        )
        h_s_0.set_stretches([1, 3])
        v_s_0.set_stretches([1, 1])

        self.refresh_all()

    def set_variants_restore(self):
        self.__running_threads_stacks = None

        self.__thread_stack_index = 0

        self.__attribute_options = {}
        self.__attribute_options_default = {}
        self.__attribute_filters = []

        self.__attribute_count_dict = {}

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAbsLib, self).__init__(session, *args, **kwargs)

    def refresh_all(self):
        self._dtb = dtb_objects.DtbResourceLib(
            '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
        )

        self._gui_type_opt = GuiTypeOpt(
            self, self._session, self._dtb, self._type_prx_view
        )
        self._gui_tag_opt = GuiTagOpt(
            self, self._session, self._dtb, self._tag_prx_view
        )
        self._gui_node_opt = GuiNodeOpt(
            self, self._session, self._dtb, self._resource_prx_view
        )

        self.__gui_refresh_for_all_()

    def __refresh_guide_bar_(self):
        def get_path_args_fnc_(dtb_entity_):
            types = [
                self._dtb.EntityTypes.CategoryGroup,
                self._dtb.EntityTypes.Category,
                self._dtb.EntityTypes.Type
            ]
            _dict = collections.OrderedDict()
            path = dtb_entity_.path
            path_opt = bsc_core.DccPathDagOpt(path)
            comps = path_opt.get_components()
            comps.reverse()
            for seq, i in enumerate(comps[1:]):
                i_type = types[seq]
                i_name = i.name
                _dict[i_name] = i_type
            return _dict
        #
        dtb_entity = None
        type_selected_prx_items = self._type_prx_view.get_selected_items()
        if type_selected_prx_items:
            dtb_entity = type_selected_prx_items[-1].get_gui_dcc_obj(self.DCC_NAMESPACE)

        if dtb_entity is not None:
            self._guide_bar.set_path_args(get_path_args_fnc_(dtb_entity))

    def __type_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = fnmatch.filter(
                self._gui_type_opt._keys, '*{}*'.format(keyword)
            )
            return bsc_core.TextsMtd.set_sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def __restore_thread_stack_(self):
        if self.__running_threads_stacks:
            [i.set_kill() for i in self.__running_threads_stacks]
        #
        self.__running_threads_stacks = []

    def __gui_refresh_for_all_(self):
        self._gui_type_opt.restore()
        self._gui_tag_opt.restore()
        self._gui_node_opt.restore()
        #
        self._guide_bar.set_clear()
        # type
        self._gui_type_opt.gui_add_root()
        self._gui_type_opt.gui_add_all_category_groups()
        self.__gui_add_for_all_types_()
        # properties
        self._gui_tag_opt.gui_add_root()
        self._gui_tag_opt.gui_add_all_groups()
    # build for types
    def __gui_add_for_all_types_(self):
        def post_fnc_():
            self._end_timestamp = bsc_core.SystemMtd.get_timestamp()
            #
            utl_core.Log.set_module_result_trace(
                'load all types',
                'count={}, cost-time="{}"'.format(
                    len(self._gui_type_opt._keys),
                    bsc_core.IntegerMtd.second_to_time_prettify(self._end_timestamp - self.__start_timestamp)
                )
            )

        def quit_fnc_():
            ts.set_quit()
        #
        self.__start_timestamp = bsc_core.SystemMtd.get_timestamp()
        #
        dtb_categories = self._dtb.get_entities(
            entity_type=self._dtb.EntityTypes.Category,
            filters=[
                ('kind', 'is', self._dtb.Kinds.ResourceCategory)
            ]
        )
        dtb_categories_map = bsc_core.ListMtd.set_grid_to(
            dtb_categories, self.THREAD_STEP
        )
        # use thread
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            ts.run_finished.connect(post_fnc_)
            for i_dtb_categories in dtb_categories_map:
                [self._gui_type_opt.gui_add_category(i) for i in i_dtb_categories]
                ts.set_register(
                    cache_fnc=functools.partial(self._gui_type_opt.gui_cache_fnc_for_types_by_categories, i_dtb_categories),
                    build_fnc=self._gui_type_opt.gui_build_fnc_for_types
                )
                #
                ts.set_start()
                #
                self.set_window_close_connect_to(quit_fnc_)
        else:
            with utl_core.gui_progress(maximum=len(dtb_categories_map), label='gui-add for type') as g_p:
                for i_dtb_categories in dtb_categories_map:
                    g_p.set_update()
                    #
                    [self._gui_type_opt.gui_add_category(i) for i in i_dtb_categories]
                    self._gui_type_opt.gui_build_fnc_for_types(
                        self._gui_type_opt.gui_cache_fnc_for_types_by_categories(i_dtb_categories)
                    )
    # build for resources
    def __execute_gui_refresh_for_resources_by_property_check_(self):
        #
        filter_data_src = self._gui_tag_opt.get_filter_data()
        qt_view = self._resource_prx_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(
            filter_data_src
        )
        qt_view._set_view_items_visible_by_any_filter_(None)
        qt_view._refresh_view_all_items_viewport_showable_auto_()

    def __execute_gui_refresh_for_resources_by_type_selection_(self):
        entity_prx_items = self._type_prx_view.get_selected_items()
        #
        self.__restore_thread_stack_()
        #
        self.__thread_stack_index += 1
        #
        self._resource_prx_view.set_clear()
        self._gui_tag_opt.reset()
        self._resource_prx_view._qt_info_chart._clear_()
        #
        self.__attribute_count_dict = {}
        #
        self.__test_set = set()
        #
        if entity_prx_items:
            entity_prx_item = entity_prx_items[-1]
            dtb_entity = entity_prx_item.get_gui_dcc_obj(self.DCC_NAMESPACE)
            if dtb_entity is not None:
                dtb_types = []
                if dtb_entity.entity_category == self._dtb.EntityCategories.Type:
                    if dtb_entity.entity_type in [self._dtb.EntityTypes.CategoryGroup, self._dtb.EntityTypes.Category]:
                        dtb_types = self._dtb.get_entities(
                            entity_type=self._dtb.EntityTypes.Type,
                            filters=[
                                ('group', 'startswith', dtb_entity.path),
                            ]
                        )
                    elif dtb_entity.kind == self._dtb.Kinds.ResourceType:
                        dtb_types = [dtb_entity]
                #
                self.__batch_gui_add_for_resources_by_types_(dtb_types, self.__thread_stack_index)

    def __batch_gui_add_for_resources_by_types_(self, dtb_types, thread_stack_index):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.set_quit()
        #
        dtb_types_map = bsc_core.ListMtd.set_grid_to(
            dtb_types, self.THREAD_STEP
        )
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_dtb_types in dtb_types_map:
                ts.set_register(
                    functools.partial(self.__batch_gui_cache_fnc_for_resources_by_entities_, i_dtb_types, thread_stack_index),
                    self.__batch_gui_build_fnc_for_resources_
                )
            #
            ts.set_start()
            #
            self.set_window_close_connect_to(quit_fnc_)
        else:
            with utl_core.gui_progress(maximum=len(dtb_types_map), label='batch gui-add resource') as g_p:
                for i_dtb_types in dtb_types_map:
                    g_p.set_update()
                    self.__batch_gui_build_fnc_for_resources_(
                        self.__batch_gui_cache_fnc_for_resources_by_entities_(i_dtb_types, thread_stack_index)
                    )

    def __batch_gui_cache_fnc_for_resources_by_entities_(self, dtb_types, thread_stack_index):
        if thread_stack_index == self.__thread_stack_index:
            if dtb_types:
                dtb_type_assigns = self._dtb.get_entities(
                    entity_type=self._dtb.EntityTypes.Types,
                    filters=[
                        ('kind', 'is', self._dtb.Kinds.ResourceType),
                        #
                        ('value', 'in', [i.path for i in dtb_types])
                    ]
                )
                return dtb_type_assigns, thread_stack_index

    def __batch_gui_build_fnc_for_resources_(self, *args):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.set_quit()

        if args[0] is None:
            return

        dtb_type_assigns, thread_stack_index = args[0]
        if thread_stack_index == self.__thread_stack_index:
            if thread_stack_index == self.__thread_stack_index:
                dtb_type_assigns_map = bsc_core.ListMtd.set_grid_to(
                    dtb_type_assigns, self.THREAD_STEP
                )
                if self._qt_thread_enable is True:
                    ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
                    self.__running_threads_stacks.append(ts)
                    ts.run_finished.connect(post_fnc_)
                    for i_dtb_type_assigns in dtb_type_assigns_map:
                        ts.set_register(
                            functools.partial(self.__gui_cache_fnc_for_resources_, i_dtb_type_assigns, thread_stack_index),
                            self.__gui_build_fnc_for_resources_
                        )
                    #
                    ts.set_start()
                    #
                    self.set_window_close_connect_to(quit_fnc_)
                else:
                    with utl_core.gui_progress(maximum=len(dtb_type_assigns_map), label='gui-add resources') as g_p:
                        for i_dtb_type_assigns in dtb_type_assigns_map:
                            g_p.set_update()
                            self.__gui_build_fnc_for_resources_(
                                self.__gui_cache_fnc_for_resources_(i_dtb_type_assigns)
                            )

    def __gui_cache_fnc_for_resources_(self, dtb_resource_assigns, thread_stack_index):
        dtb_resources = self._dtb.get_entities(
            entity_type=self._dtb.EntityTypes.Resource,
            filters=[
                ('path', 'in', [i.node for i in dtb_resource_assigns])
            ]
        )
        build_args = []
        for i_dtb_resource in dtb_resources:
            self.__test_set.add(i_dtb_resource.name)
            i_dtb_tag_assigns = self._dtb.get_entities(
                entity_type=self._dtb.EntityTypes.Tags,
                filters=[
                    ('kind', 'in', [self._dtb.Kinds.ResourcePrimarySemanticTag, self._dtb.Kinds.ResourcePropertyTag]),
                    #
                    ('node', 'is', i_dtb_resource.path)
                ]
            )
            i_semantic_tag_filter_data = {}
            i_tag_args = []
            for j_dtb_tag_assign in i_dtb_tag_assigns:
                j_dtb_tag = self._dtb.get_entity(
                    entity_type=self._dtb.EntityTypes.Tag,
                    filters=[
                        ('path', 'is', j_dtb_tag_assign.value)
                    ]
                )
                if j_dtb_tag is not None:
                    j_tag = j_dtb_tag.path
                    j_tag_key = j_dtb_tag.group
                    i_tag_args.append(j_dtb_tag)
                else:
                    j_tag = j_dtb_tag_assign.value
                    j_tag_key = bsc_core.DccPathDagOpt(j_tag).get_parent_path()
                    i_tag_args.append(j_tag)

                i_semantic_tag_filter_data.setdefault(
                    j_tag_key, set()
                ).add(j_tag)

                self._gui_tag_opt.register_count(
                    j_dtb_tag_assign.node, j_dtb_tag_assign.value
                )
            #
            build_args.append(
                (i_dtb_resource, i_tag_args, i_semantic_tag_filter_data)
            )
        return build_args, thread_stack_index

    def __gui_build_fnc_for_resources_(self, *args):
        build_args, thread_stack_index = args[0]

        if args[0] is None:
            return

        if thread_stack_index == self.__thread_stack_index:
            for i_dtb_resource, i_dtb_tags, i_semantic_tag_filter_data in build_args:
                self._gui_node_opt.gui_add(
                    i_dtb_resource, i_semantic_tag_filter_data
                )
                #
                for j_dtb_tag in i_dtb_tags:
                    self._gui_tag_opt.gui_register(
                        j_dtb_tag
                    )
