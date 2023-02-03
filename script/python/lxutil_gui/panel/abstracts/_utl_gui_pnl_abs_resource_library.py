# coding:utf-8
import fnmatch

import collections

import functools

from lxbasic import bsc_core

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxdatabase import dtb_configure

import lxdatabase.objects as dtb_objects

from lxutil_gui import utl_gui_configure, utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

import lxsession.commands as ssn_commands


class _GuiBaseOpt(object):
    def __init__(self, window, session, database_opt):
        self._window = window
        self._session = session
        self._dtb_opt = database_opt

    def get_dtb_entity_menu_content(self, dtb_entity):
        options = []
        c = self._session.configure.get(
            'entity-actions.{}.option-hooks'.format(dtb_entity.entity_type)
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
                    database=self._dtb_opt.get_database(),
                    database_configure=self._dtb_opt.get_database_configure(),
                    #
                    entity_type=dtb_entity.entity_type,
                    entity=dtb_entity.path,
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.ArgDictStringOpt(i_kwargs).to_string(),
                )
            return ssn_commands.get_menu_content_by_hook_options(options)

    def get_dtb_extra_menu_content(self, dtb_entity, sub_path):
        options = []
        c = self._session.configure.get(
            'entity-extra-actions.{}-{}.{}.option-hooks'.format(dtb_entity.entity_type, dtb_entity.kind, sub_path)
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
                    database=self._dtb_opt.get_database(),
                    database_configure=self._dtb_opt.get_database_configure(),
                    #
                    entity_type=dtb_entity.entity_type,
                    entity=dtb_entity.path,
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.ArgDictStringOpt(i_kwargs).to_string(),
                )
            return ssn_commands.get_menu_content_by_hook_options(options)

    def get_dtb_entity_location(self, dtb_entity):
        dtb_port = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            filters=[
                ('node', 'is', dtb_entity.path),
                ('port', 'is', 'location'),
            ]
        )
        return dtb_port.value


class _GuiTypeOpt(_GuiBaseOpt):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, prx_view):
        super(_GuiTypeOpt, self).__init__(window, session, database_opt)
        #
        self._tree_prx_view = prx_view
        self._item_dict = self._tree_prx_view._item_dict
        self._keys = set()

    def restore(self):
        self._tree_prx_view.set_clear()
        #
        self._keys.clear()

    def get_gui_is_exists(self, path):
        return path in self._item_dict

    def get_gui(self, path):
        return self._item_dict[path]

    def gui_add_root(self):
        path = '/'
        if self.get_gui_is_exists(path) is False:
            prx_item = self._tree_prx_view.set_item_add(
                self.ROOT_NAME,
                icon=utl_gui_core.RscIconFile.get('database/all'),
            )
            self._item_dict[path] = prx_item
            prx_item.set_expanded(True)
            # prx_item.set_checked(False)
            return prx_item
        return self.get_gui(path)

    def gui_add_all_category_groups(self):
        dtb_category_groups = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.CategoryGroup,
            filters=[
                ('kind', 'is', self._dtb_opt.Kinds.ResourceCategoryGroup)
            ]
        )
        [self.gui_add_category_group(i) for i in dtb_category_groups]

    def gui_add_category_group(self, dtb_entity):
        path = dtb_entity.path
        if self.get_gui_is_exists(path) is False:
            parent_gui = self.get_gui(dtb_entity.group)
            prx_item = parent_gui.set_child_add(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            self._tree_prx_view._item_dict[path] = prx_item
            #
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            prx_item.set_tool_tip(dtb_entity.to_string())
            prx_item.set_expanded(True)
            # prx_item.set_checked(False)
            #
            menu_content = self.get_dtb_entity_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            return prx_item
        return self.get_gui(path)

    def gui_add_all_categories(self):
        pass

    def gui_add_category(self, dtb_entity):
        path = dtb_entity.path
        if self.get_gui_is_exists(path) is False:
            parent_gui = self.get_gui(dtb_entity.group)
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
            #
            menu_content = self.get_dtb_entity_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            #
            # prx_item.set_checked(False)
            return prx_item
        return self.get_gui(path)

    def __execute_gui_refresh_for_type_by_category_expand_changed_(self, prx_item):
        child_prx_items = prx_item.get_children()
        for i_prx_item in child_prx_items:
            i_dtb_entity = i_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
            if i_dtb_entity is not None:
                if i_dtb_entity.entity_type == self._dtb_opt.EntityTypes.Type:
                    i_dtb_assigns = self._dtb_opt.get_entities(
                        entity_type=self._dtb_opt.EntityTypes.Types,
                        filters=[
                            ('kind', 'is', self._dtb_opt.Kinds.ResourceType),
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
        if self.get_gui_is_exists(path) is False:
            parent_gui = self.get_gui(dtb_entity.group)
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
            menu_content = self.get_dtb_entity_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            #
            # prx_item.set_checked(False)
            return prx_item
        return self.get_gui(path)
    # for type
    def gui_cache_fnc_for_types_by_categories(self, dtb_categories):
        dtb_types = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.Type,
            filters=[
                ('group', 'in', [i.path for i in dtb_categories]),
            ]
        )
        self._keys.update(set([i.name for i in dtb_types]))
        return dtb_types

    def gui_build_fnc_for_types(self, dtb_types):
        [self.gui_add_type(i) for i in dtb_types]


class _GuiTagOpt(_GuiBaseOpt):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, tree_prx_view):
        super(_GuiTagOpt, self).__init__(window, session, database_opt)
        #
        self._tree_prx_view = tree_prx_view
        self._key_item_dict = {}
        self._value_item_dict = {}
        self._count_dict = {}
        #
        self._tag_group_kinds = [
            self._dtb_opt.Kinds.ResourceSemanticTagGroup,
            self._dtb_opt.Kinds.ResourcePropertyTagGroup,
            self._dtb_opt.Kinds.ResourceStorageTagGroup
        ]
        self._tag_kinds = [
            self._dtb_opt.Kinds.ResourcePrimarySemanticTag,
            self._dtb_opt.Kinds.ResourcePropertyTag,
            self._dtb_opt.Kinds.ResourceFileTag
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
            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)
            return prx_item
        else:
            return self.gui_get_group(path)

    def gui_add_all_groups(self):
        dtb_tags = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.TagGroup,
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

    def get_gui_is_exists(self, path):
        return path in self._value_item_dict

    def get_gui(self, path):
        return self._value_item_dict[path]

    def add_gui(self, dtb_entity):
        path = dtb_entity.path
        if self.get_gui_is_exists(path) is False:
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
        return self.get_gui(path)

    def gui_add_by_path(self, path):
        if self.get_gui_is_exists(path) is False:
            path_opt = bsc_core.DccPathDagOpt(path)
            parent_path = path_opt.get_parent_path()
            parent_gui = self.gui_get_group(parent_path)
            gui_name = bsc_core.RawStringUnderlineOpt(path_opt.name).to_prettify()
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
        return self.get_gui(path)

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
        if isinstance(dtb_tag, six.string_types):
            tag_path = dtb_tag
            prx_item = self.gui_add_by_path(dtb_tag)
        elif isinstance(dtb_tag, dict):
            tag_path = dtb_tag.path
            prx_item = self.add_gui(dtb_tag)
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


class _GuiResourceOpt(_GuiBaseOpt):
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, list_prx_view):
        super(_GuiResourceOpt, self).__init__(window, session, database_opt)
        #
        self._list_prx_view = list_prx_view
        self._item_dict = self._list_prx_view._item_dict
        self._keys = set()

    def restore(self):
        self._list_prx_view.set_clear()
        self._keys.clear()

    def get_gui_is_exists(self, path):
        return path in self._item_dict

    def get_gui(self, path):
        return self._item_dict[path]

    def add_gui(self, dtb_resource, semantic_tag_filter_data):
        def cache_fnc_():
            _list = []
            return _list

        def build_fnc_(data):
            self.__gui_show_deferred_fnc_(
                dtb_resource, prx_item, semantic_tag_filter_data, data
            )

        path = dtb_resource.path
        if self.get_gui_is_exists(path) is False:
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
        return self.get_gui(path)

    def get_checked_dtb_resources(self):
        list_ = []
        _ = self._list_prx_view.get_checked_items()
        for i in _:
            i_dtb_resource = i.get_gui_dcc_obj(self.DCC_NAMESPACE)
            list_.append(i_dtb_resource)
        return list_

    def __gui_show_deferred_fnc_(self, dtb_resource, prx_item, semantic_tag_filter_data, data):
        # type_ = dtb_resource.type
        prx_item.set_check_enable(True)
        # r, g, b = bsc_core.RawTextOpt(type_).to_rgb_()
        # prx_item.set_name_frame_background_color((r, g, b, 127))
        name_dict = collections.OrderedDict()
        name_dict['resource'] = dtb_resource.gui_name
        for i_k, i_v in semantic_tag_filter_data.items():
            name_dict[bsc_core.DccPathDagOpt(i_k).name] = ', '.join([bsc_core.DccPathDagOpt(j).name for j in i_v])

        prx_item.set_image(
            utl_gui_core.RscIconFile.get('image_loading_failed_error')
        )

        dtb_version_port = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            filters=[
                ('node', 'is', dtb_resource.path),
                ('port', 'is', 'version')
            ],
        )

        dtb_version = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Version,
            filters=[
                ('path', 'is', dtb_version_port.value),
            ],
        )
        # drag action
        prx_item.set_drag_enable(True)
        if self._session.get_application() == 'katana':
            prx_item.set_drag_data(
                {
                    'nodegraph/noderefs': 'rootNode',
                    'pre-import/hook-option': self._get_callback_hook_option_(
                        option_hook_key='dtb-callbacks/katana/resource-pre-import-by-drag',
                        dtb_entity=dtb_resource
                    ),
                    'import/hook-option': self._get_callback_hook_option_(
                        option_hook_key='dtb-callbacks/katana/resource-import-by-drag',
                        dtb_entity=dtb_resource
                    )
                }
            )
            prx_item.set_drag_pressed_connect_to(
                self._drag_pressed_fnc_
            )
            prx_item.set_drag_released_connect_to(
                self._drag_release_fnc_
            )
        # menu
        dtb_resource_menu_content = self.get_dtb_entity_menu_content(dtb_resource)
        dtb_version_menu_content = self.get_dtb_entity_menu_content(dtb_version)
        dtb_resource_menu_content.set_update(dtb_version_menu_content.get_value())
        prx_item.set_menu_content(dtb_resource_menu_content)
        #
        prx_item.set_name_dict(
            name_dict
        )
        prx_item.set_tool_tip(dtb_resource.to_string())

        preview_image_dtb_port = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            filters=[
                ('node', 'is', dtb_version_port.value),
                ('port', 'is', 'image_preview_file'),
            ],
            new_connection=False
        )
        if preview_image_dtb_port:
            image = preview_image_dtb_port.value
            if bsc_core.StgFileOpt(image).get_is_exists() is True:
                prx_item.set_image(
                    image
                )
                image_file_path, image_sub_process_cmds = bsc_core.ImgFileOpt(image).get_thumbnail_create_args(
                    width=256, ext='.png'
                )
                prx_item.set_image(image_file_path)
                if image_sub_process_cmds is not None:
                    prx_item.set_image_show_args(image_file_path, image_sub_process_cmds)
        else:
            prx_item.set_image(
                utl_gui_core.RscIconFile.get('image_loading_failed_error')
            )

    def _get_callback_hook_option_(self, option_hook_key, dtb_entity):
        return bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key=option_hook_key,
                #
                window_unique_id=self._window.get_window_unique_id(),
                database=self._dtb_opt.get_database(),
                database_configure=self._dtb_opt.get_database_configure(),
                #
                entity_type=dtb_entity.entity_type,
                entity=dtb_entity.path,
            )
        ).to_string()

    def _drag_pressed_fnc_(self, *args, **kwargs):
        mime_data, = args[0]
        key = 'pre-import/hook-option'
        if mime_data.hasFormat(key):
            hook_option = mime_data.data(key).data()
            ssn_commands.set_option_hook_execute(
                hook_option
            )

    def _drag_release_fnc_(self, *args, **kwargs):
        flag, mime_data = args[0]
        if flag in [
            utl_gui_configure.DragFlag.Copy,
            utl_gui_configure.DragFlag.Move
        ]:
            key = 'import/hook-option'
            if mime_data.hasFormat(key):
                hook_option = mime_data.data(key).data()
                ssn_commands.set_option_hook_execute(
                    hook_option
                )


class _GuiDirectoryOpt(_GuiBaseOpt):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, tree_prx_view):
        super(_GuiDirectoryOpt, self).__init__(window, session, database_opt)
        #
        self._tree_prx_view = tree_prx_view
        self._item_dict = self._tree_prx_view._item_dict

    def restore(self):
        self._tree_prx_view.set_clear()

    def get_gui_is_exists(self, path):
        return path in self._item_dict

    def get_gui(self, path):
        return self._item_dict[path]

    def gui_add_all(self, dtb_version):
        version_path = dtb_version.path
        version_path_opt = bsc_core.DccPathDagOpt(version_path)
        #
        self.gui_add_root(version_path_opt.name)
        dtb_directories = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.Storage,
            filters=[
                ('kind', 'is', self._dtb_opt.Kinds.Directory),
                ('group', 'startswith', dtb_version.path),
            ]
        )
        for i_dtb_directory in dtb_directories:
            i_path = i_dtb_directory.path
            i_sub_path = i_path[len(version_path):]
            #
            self.gui_add_one(i_sub_path, i_dtb_directory)

    def gui_add_one(self, sub_path, dtb_directory):
        path_opt = bsc_core.DccPathDagOpt(sub_path)
        ancestors = path_opt.get_ancestors()
        if ancestors:
            ancestors.reverse()
            #
            for i_ancestor in ancestors:
                i_ancestor_path = i_ancestor.path
                self.gui_add_group(i_ancestor_path)
        #
        self.add_gui(sub_path, dtb_directory)

    def gui_add_root(self, name):
        path = '/'
        if self.get_gui_is_exists(path) is False:
            prx_item = self._tree_prx_view.set_item_add(
                name,
                icon=utl_gui_core.RscIconFile.get('database/group'),
            )
            self._item_dict[path] = prx_item
            prx_item.set_expanded(True)
            # prx_item.set_checked(False)
            return prx_item
        else:
            return self.get_gui(path)

    def gui_add_group(self, sub_path):
        if self.get_gui_is_exists(sub_path) is False:
            path_opt = bsc_core.DccPathDagOpt(sub_path)
            #
            parent_gui = self.get_gui(path_opt.get_parent_path())
            #
            prx_item = parent_gui.set_child_add(
                path_opt.name,
                icon=utl_gui_core.RscIconFile.get('database/group'),
            )
            self._item_dict[sub_path] = prx_item
            prx_item.set_tool_tip(sub_path)
            prx_item.set_expanded(True)
            # prx_item.set_checked(False)
            return prx_item
        return self.get_gui(sub_path)

    def add_gui(self, sub_path, dtb_directory):
        if self.get_gui_is_exists(sub_path) is False:
            path_opt = bsc_core.DccPathDagOpt(sub_path)
            #
            parent_gui = self.get_gui(path_opt.get_parent_path())
            #
            prx_item = parent_gui.set_child_add(
                path_opt.name,
                icon=utl_gui_core.RscIconFile.get('database/objects'),
            )
            self._item_dict[sub_path] = prx_item
            prx_item.set_tool_tip(sub_path)
            #
            dtb_entity_menu_content = self.get_dtb_entity_menu_content(dtb_directory)
            dtb_extra_menu_content = self.get_dtb_extra_menu_content(dtb_directory, sub_path)
            if dtb_extra_menu_content:
                dtb_entity_menu_content.set_update(dtb_extra_menu_content)
            #
            if dtb_entity_menu_content:
                prx_item.set_menu_content(dtb_entity_menu_content)
            #
            location = self.get_dtb_entity_location(dtb_directory)
            if bsc_core.StorageBaseMtd.get_is_exists(location) is True:
                prx_item.set_status(prx_item.ValidatorStatus.Normal)
            else:
                prx_item.set_status(prx_item.ValidatorStatus.Disable)
            #
            prx_item.set_expanded(True)
            # prx_item.set_checked(False)
            return prx_item
        return self.get_gui(sub_path)


class _GuiFileOpt(_GuiBaseOpt):
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, list_prx_view):
        super(_GuiFileOpt, self).__init__(window, session, database_opt)
        #
        self._list_prx_view = list_prx_view
        self._item_dict = self._list_prx_view._item_dict
        self._keys = set()

    def restore(self):
        self._list_prx_view.set_clear()
        self._keys.clear()

    def get_gui_is_exists(self, path):
        return path in self._item_dict

    def get_gui(self, path):
        return self._item_dict[path]


class AbsPnlAbsResourceLibrary(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = 'database'
    THREAD_STEP = 8
    FILTER_MAXIMUM = 50
    def set_all_setup(self):
        self._item_frame_size = self._session.gui_configure.get('item_frame_size')
        self._item_icon_frame_size = self._session.gui_configure.get('item_icon_frame_size')
        self._item_icon_size = self._session.gui_configure.get('item_icon_size')

        main_scroll_area = prx_widgets.PrxScrollArea()
        self.set_widget_add(main_scroll_area)
        #
        self._guide_bar = prx_widgets.PrxGuideBar()
        main_scroll_area.set_widget_add(self._guide_bar)
        #
        h_s_0 = prx_widgets.PrxHSplitter()
        main_scroll_area.set_widget_add(h_s_0)
        #
        v_s_0 = prx_widgets.PrxVSplitter()
        h_s_0.set_widget_add(v_s_0)
        # type
        self._type_expand_group = prx_widgets.PrxExpandedGroup()
        v_s_0.set_widget_add(self._type_expand_group)
        self._type_expand_group.set_expanded(True)
        self._type_expand_group.set_name('type')
        #
        self._type_prx_view = prx_widgets.PrxTreeView()
        self._type_expand_group.set_widget_add(self._type_prx_view)
        self._type_prx_view.set_filter_entry_tip('fiter by type ...')
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
        # tag
        self._tag_expand_group = prx_widgets.PrxExpandedGroup()
        v_s_0.set_widget_add(self._tag_expand_group)
        self._tag_expand_group.set_expanded(True)
        self._tag_expand_group.set_name('tag')
        #
        self._tag_prx_view = prx_widgets.PrxTreeView()
        self._tag_expand_group.set_widget_add(self._tag_prx_view)
        self._tag_prx_view.set_filter_entry_tip('filter by tag ...')
        self._tag_prx_view.set_selection_disable()
        self._tag_prx_view.set_header_view_create(
            [('tag', 3), ('count', 1)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 48
        )
        self._tag_prx_view.set_item_check_changed_connect_to(
            self.__execute_gui_refresh_for_resources_by_property_check_
        )
        #
        view_scroll_area_1_0 = prx_widgets.PrxScrollArea()
        h_s_0.set_widget_add(view_scroll_area_1_0)
        # resource
        self._resource_expand_group = prx_widgets.PrxExpandedGroup()
        view_scroll_area_1_0.set_widget_add(self._resource_expand_group)
        self._resource_expand_group.set_expanded(True)
        self._resource_expand_group.set_name('resource')
        #
        self._resource_prx_view = prx_widgets.PrxListView()
        self._resource_expand_group.set_widget_add(self._resource_prx_view)
        # self._resource_prx_view.set_draw_enable(True)
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
        self._resource_prx_view.set_item_select_changed_connect_to(
            self.__execute_gui_refresh_for_textures_
        )
        # texture
        self._storage_expand_group = prx_widgets.PrxExpandedGroup()
        view_scroll_area_1_0.set_widget_add(self._storage_expand_group)
        self._storage_expand_group.set_expanded(True)
        self._storage_expand_group.set_name('storage')
        self._storage_expand_group.set_expand_changed_connect_to(
            self.__execute_gui_refresh_for_textures_
        )
        #
        texture_v_splitter = prx_widgets.PrxHSplitter()
        self._storage_expand_group.set_widget_add(texture_v_splitter)
        #
        self._directory_prx_view = prx_widgets.PrxTreeView()
        texture_v_splitter.set_widget_add(self._directory_prx_view)
        self._directory_prx_view.set_header_view_create(
            [('directory', 1)]
        )
        #
        self._file_prx_view = prx_widgets.PrxListView()
        texture_v_splitter.set_widget_add(self._file_prx_view)
        self._file_prx_view.set_item_frame_size(*self._item_frame_size)
        self._file_prx_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._file_prx_view.set_item_icon_size(*self._item_icon_size)
        self._file_prx_view.set_item_icon_frame_draw_enable(True)
        self._file_prx_view.set_item_name_frame_draw_enable(True)
        self._file_prx_view.set_item_names_draw_range([None, 1])
        self._file_prx_view.set_item_image_frame_draw_enable(True)
        #
        h_s_0.set_stretches([1, 3])
        v_s_0.set_stretches([2, 1])
        #
        texture_v_splitter.set_stretches([1, 2])

        self.refresh_all()

        self.setup_menu()

    def setup_menu(self):
        menu = self.set_menu_add('tool')
        menu_content = self.get_tool_menu_content()
        menu.set_menu_content(menu_content)

    def get_tool_menu_content(self):
        options = []
        c = self._session.configure.get(
            'window-actions.tool.option-hooks'
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
                    window_unique_id=self.get_window_unique_id(),
                    database=self._dtb_opt.get_database(),
                    database_configure=self._dtb_opt.get_database_configure(),
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.ArgDictStringOpt(i_kwargs).to_string(),
                )
            return ssn_commands.get_menu_content_by_hook_options(options)

    def set_variants_restore(self):
        self.__running_threads_stacks = None

        self.__thread_stack_index = 0

        self.__attribute_options = {}
        self.__attribute_options_default = {}
        self.__attribute_filters = []

        self.__attribute_count_dict = {}

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAbsResourceLibrary, self).__init__(session, *args, **kwargs)

    def refresh_all(self):
        self._dtb_cfg = dtb_configure.DataFile.LIBRARY_BASIC
        self._dtb_opt = dtb_objects.DtbResourceLibraryOpt(self._dtb_cfg)

        self._gui_type_opt = _GuiTypeOpt(
            self, self._session, self._dtb_opt, self._type_prx_view
        )
        self._gui_tag_opt = _GuiTagOpt(
            self, self._session, self._dtb_opt, self._tag_prx_view
        )
        self._gui_resource_opt = _GuiResourceOpt(
            self, self._session, self._dtb_opt, self._resource_prx_view
        )
        #
        self._gui_directory_opt = _GuiDirectoryOpt(
            self, self._session, self._dtb_opt, self._directory_prx_view
        )
        self._gui_file_opt = _GuiFileOpt(
            self, self._session, self._dtb_opt, self._file_prx_view
        )

        self.__gui_refresh_for_all_()

    def get_gui_resource_opt(self):
        return self._gui_resource_opt

    def __refresh_guide_bar_(self):
        def get_path_args_fnc_(dtb_entity_):
            types = [
                self._dtb_opt.EntityTypes.CategoryGroup,
                self._dtb_opt.EntityTypes.Category,
                self._dtb_opt.EntityTypes.Type
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
            return bsc_core.RawTextsMtd.set_sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def __restore_thread_stack_(self):
        if self.__running_threads_stacks:
            [i.set_kill() for i in self.__running_threads_stacks]
        #
        self.__running_threads_stacks = []

    def __gui_refresh_for_all_(self):
        self._gui_type_opt.restore()
        self._gui_tag_opt.restore()
        self._gui_resource_opt.restore()
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
            self._end_timestamp = bsc_core.TimeBaseMtd.get_timestamp()
            #
            utl_core.Log.set_module_result_trace(
                'load all types',
                'count={}, cost-time="{}"'.format(
                    len(self._gui_type_opt._keys),
                    bsc_core.RawIntegerMtd.second_to_time_prettify(self._end_timestamp - self.__start_timestamp)
                )
            )

        def quit_fnc_():
            ts.set_quit()
        #
        self.__start_timestamp = bsc_core.TimeBaseMtd.get_timestamp()
        #
        dtb_categories = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.Category,
            filters=[
                ('kind', 'is', self._dtb_opt.Kinds.ResourceCategory)
            ]
        )
        dtb_categories_map = bsc_core.RawListMtd.set_grid_to(
            dtb_categories, self.THREAD_STEP
        )
        # use thread
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            ts.run_finished.connect(post_fnc_)
            with utl_core.gui_progress(maximum=len(dtb_categories_map), label='gui-add for type') as g_p:
                for i_dtb_categories in dtb_categories_map:
                    g_p.set_update()
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
                if dtb_entity.entity_category == self._dtb_opt.EntityCategories.Type:
                    if dtb_entity.entity_type in [self._dtb_opt.EntityTypes.CategoryGroup, self._dtb_opt.EntityTypes.Category]:
                        dtb_types = self._dtb_opt.get_entities(
                            entity_type=self._dtb_opt.EntityTypes.Type,
                            filters=[
                                ('group', 'startswith', dtb_entity.path),
                            ]
                        )
                    elif dtb_entity.kind == self._dtb_opt.Kinds.ResourceType:
                        dtb_types = [dtb_entity]
                #
                self.__batch_gui_add_for_resources_by_types_(dtb_types, self.__thread_stack_index)

    def __batch_gui_add_for_resources_by_types_(self, dtb_types, thread_stack_index):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.set_quit()
        #
        dtb_types_map = bsc_core.RawListMtd.set_grid_to(
            dtb_types, self.THREAD_STEP
        )
        if self._qt_thread_enable is True:
            ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            with utl_core.gui_progress(maximum=len(dtb_types_map), label='batch gui-add resource') as g_p:
                for i_dtb_types in dtb_types_map:
                    g_p.set_update()
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
                dtb_type_assigns = self._dtb_opt.get_entities(
                    entity_type=self._dtb_opt.EntityTypes.Types,
                    filters=[
                        ('kind', 'is', self._dtb_opt.Kinds.ResourceType),
                        #
                        ('value', 'in', [i.path for i in dtb_types])
                    ]
                )
                return [dtb_type_assigns, thread_stack_index]

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
                dtb_type_assigns_map = bsc_core.RawListMtd.set_grid_to(
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
        dtb_resources = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.Resource,
            filters=[
                ('path', 'in', [i.node for i in dtb_resource_assigns])
            ]
        )
        build_args = []
        for i_dtb_resource in dtb_resources:
            self.__test_set.add(i_dtb_resource.name)
            i_dtb_tag_assigns = self._dtb_opt.get_entities(
                entity_type=self._dtb_opt.EntityTypes.Tags,
                filters=[
                    ('kind', 'in', self._gui_tag_opt._tag_kinds),
                    #
                    ('node', 'is', i_dtb_resource.path)
                ]
            )
            i_semantic_tag_filter_data = {}
            i_tag_args = []
            for j_dtb_tag_assign in i_dtb_tag_assigns:
                j_dtb_tag = self._dtb_opt.get_entity(
                    entity_type=self._dtb_opt.EntityTypes.Tag,
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
        return [build_args, thread_stack_index]

    def __gui_build_fnc_for_resources_(self, *args):
        build_args, thread_stack_index = args[0]

        if args[0] is None:
            return

        if thread_stack_index == self.__thread_stack_index:
            for i_dtb_resource, i_dtb_tags, i_semantic_tag_filter_data in build_args:
                self._gui_resource_opt.add_gui(
                    i_dtb_resource, i_semantic_tag_filter_data
                )
                #
                for j_dtb_tag in i_dtb_tags:
                    self._gui_tag_opt.gui_register(
                        j_dtb_tag
                    )
    # build for textures
    def __execute_gui_refresh_for_textures_(self):
        self._gui_directory_opt.restore()
        self._gui_file_opt.restore()
        #
        if self._storage_expand_group.get_is_expanded():
            resource_selected_prx_items = self._resource_prx_view.get_selected_items()
            if resource_selected_prx_items:
                dtb_entity = resource_selected_prx_items[-1].get_gui_dcc_obj(self.DCC_NAMESPACE)
                if dtb_entity is not None:
                    self.__gui_add_directories_(dtb_entity)

    def __gui_add_directories_(self, dtb_resource):
        dtb_resource_version_port = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            filters=[
                ('node', 'is', dtb_resource.path),
                ('port', 'is', 'version'),
            ]
        )
        dtb_version = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Version,
            filters=[
                ('path', 'is', dtb_resource_version_port.value),
            ],
        )
        self._gui_directory_opt.gui_add_all(dtb_version)
