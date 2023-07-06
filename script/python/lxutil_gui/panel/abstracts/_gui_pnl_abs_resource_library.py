# coding:utf-8
import six

import fnmatch

import collections

import functools

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_configure, utl_core

import lxdatabase.objects as dtb_objects

from lxutil_gui import utl_gui_configure, utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

import lxsession.commands as ssn_commands

LOAD_INDEX = utl_gui_qt_core.LOAD_INDEX


class _GuiBaseOpt(object):
    DCC_NAMESPACE = 'database'
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
                    database_configure_extend=self._dtb_opt.get_database_configure_extend(),
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
                    database_configure_extend=self._dtb_opt.get_database_configure_extend(),
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
        self._tree_view = prx_view
        self._item_dict = self._tree_view._item_dict
        self._keys = set()

    def restore(self):
        self._tree_view.set_clear()
        self._keys.clear()

    def gui_get_is_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get(self, path):
        return self._item_dict[path]

    def gui_register(self, path, prx_item):
        self._item_dict[path] = prx_item
        prx_item.set_gui_attribute('path', path)

    def gui_add_root(self):
        path = '/'
        if self.gui_get_is_exists(path) is False:
            prx_item = self._tree_view.create_item(
                self.ROOT_NAME,
                icon=utl_gui_core.RscIconFile.get('database/all'),
            )
            self.gui_register(path, prx_item)
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            return True, prx_item
        return False, self.gui_get(path)

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
        if self.gui_get_is_exists(path) is False:
            parent_gui = self.gui_get(dtb_entity.group)
            prx_item = parent_gui.add_child(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            self.gui_register(path, prx_item)
            prx_item.set_type(
                dtb_entity.entity_type
            )
            #
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            menu_content = self.get_dtb_entity_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            #
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            return prx_item
        return self.gui_get(path)

    def gui_add_all_categories(self):
        pass

    def gui_add_category(self, dtb_entity):
        def cache_fnc_():
            _dtb_assigns = self._dtb_opt.get_entities(
                entity_type=self._dtb_opt.EntityTypes.Types,
                filters=[
                    ('kind', 'is', self._dtb_opt.Kinds.ResourceType),
                    #
                    ('value', 'startswith', dtb_entity.path),
                ]
            )
            return [
                len(set([_i.node for _i in _dtb_assigns]))
            ]

        def build_fnc_(data_):
            _count = data_[0]
            prx_item.set_name(str(_count), 1)
            if _count > 0:
                prx_item.set_enable(True)
                prx_item.set_status(
                    prx_item.ValidatorStatus.Normal
                )
            else:
                prx_item.set_checked(False)
                prx_item.set_enable(False)
                prx_item.set_status(
                    prx_item.ValidatorStatus.Disable
                )
        #
        path = dtb_entity.path
        if self.gui_get_is_exists(path) is False:
            parent_gui = self.gui_get(dtb_entity.group)
            prx_item = parent_gui.add_child(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            self.gui_register(path, prx_item)
            prx_item.set_type(
                dtb_entity.entity_type
            )
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            self._tree_view.connect_item_expand_to(
                prx_item,
                functools.partial(self.refresh_by_category_expanded, prx_item),
                time=100
            )
            #
            menu_content = self.get_dtb_entity_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            #
            prx_item.set_checked(False)
            prx_item.set_show_fnc(
                cache_fnc_, build_fnc_
            )
            return prx_item
        return self.gui_get(path)

    def refresh_by_category_expanded(self, prx_item):
        child_prx_items = prx_item.get_children()
        dtb_assigns = []
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
                    dtb_assigns.extend(i_dtb_assigns)
                    i_count = len(i_dtb_assigns)
                    i_prx_item.set_name(str(i_count), 1)
                    if i_count > 0:
                        i_prx_item.set_enable(True)
                        i_prx_item.set_status(
                            i_prx_item.ValidatorStatus.Normal
                        )
                    else:
                        i_prx_item.set_checked(False)
                        i_prx_item.set_enable(False)
                        i_prx_item.set_status(
                            i_prx_item.ValidatorStatus.Disable
                        )
        #
        count = len(set([x.node for x in dtb_assigns]))
        prx_item.set_name(str(count), 1)
        if count > 0:
            prx_item.set_enable(True)
            prx_item.set_status(
                prx_item.ValidatorStatus.Normal
            )
        else:
            prx_item.set_checked(False)
            prx_item.set_enable(False)
            prx_item.set_status(
                prx_item.ValidatorStatus.Disable
            )

    def gui_add_type(self, dtb_entity):
        path = dtb_entity.path
        if self.gui_get_is_exists(path) is False:
            parent_gui = self.gui_get(dtb_entity.group)
            #
            # name = dtb_entity.name
            gui_name = dtb_entity.gui_name
            prx_item = parent_gui.add_child(
                gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            self.gui_register(path, prx_item)
            prx_item.set_type(
                dtb_entity.entity_type
            )
            prx_item.set_status(prx_item.ValidatorStatus.Disable)
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            #
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            menu_content = self.get_dtb_entity_menu_content(dtb_entity)
            if menu_content:
                prx_item.set_menu_content(menu_content)
            #
            prx_item.set_checked(False)
            return prx_item
        return self.gui_get(path)
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

    def get_checked_dtb_types(self):
        list_ = []
        for i_prx_item in self._tree_view.get_all_leaf_items():
            if i_prx_item.get_is_checked() is True:
                i_dtb_entity = i_prx_item.get_gui_dcc_obj(self.DCC_NAMESPACE)
                list_.append(
                    i_dtb_entity
                )
        return list_


class _GuiTagOpt(_GuiBaseOpt):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, tree_view):
        super(_GuiTagOpt, self).__init__(window, session, database_opt)
        #
        self._tree_view = tree_view
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
            self._dtb_opt.Kinds.ResourceFileTag,
            self._dtb_opt.Kinds.ResourceFormatTag
        ]
        #
        self.__thread_stack_index = 0

    def restore(self):
        self._tree_view.set_clear()
        self._key_item_dict.clear()
        self._value_item_dict.clear()
        self._count_dict.clear()

    def reset(self):
        self._count_dict.clear()
        self._value_item_dict.clear()
        for i_k, i_v in self._key_item_dict.items():
            i_dtb_entity = i_v.get_gui_dcc_obj(
                namespace=self.DCC_NAMESPACE
            )
            if i_dtb_entity is not None:
                if i_dtb_entity.kind in self._tag_group_kinds:
                    i_v.clear_children()
                    i_v.set_checked(False)
                    i_v.set_enable(False)
                    i_v.set_status(
                        i_v.ValidatorStatus.Disable
                    )

    def gui_get_group_is_exists(self, path):
        return path in self._key_item_dict

    def gui_get_group(self, path):
        return self._key_item_dict[path]

    def gui_add_root(self):
        path = '/'
        if self.gui_get_group_is_exists(path) is False:
            prx_item = self._tree_view.create_item(
                self.ROOT_NAME,
                icon=utl_gui_core.RscIconFile.get('database/all'),
            )
            self._key_item_dict[path] = prx_item
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)
            return True, prx_item
        return False, self.gui_get_group(path)

    def gui_add_all_groups(self):
        self.gui_add_root()
        #
        dtb_tags = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.TagGroup,
            filters=[
                ('kind', 'in', self._tag_group_kinds)
            ]
        )
        [self.gui_add_group(i) for i in dtb_tags]

    def gui_add_all_groups_use_thread(self):
        def cache_fnc_():
            return self.__thread_stack_index, self._dtb_opt.get_entities(
                entity_type=self._dtb_opt.EntityTypes.TagGroup,
                filters=[
                    ('kind', 'in', self._tag_group_kinds)
                ]
            )

        def build_fnc_(*args):
            _thread_stack_index, _dtb_tags = args[0]
            for _i_dtb_tag in _dtb_tags:
                if _thread_stack_index == self.__thread_stack_index:
                    self.gui_add_group(_i_dtb_tag)

        def post_fnc_():
            pass

        self.gui_add_root()

        self.__thread_stack_index += 1

        t = utl_gui_qt_core.QtBuildThread(self._window.widget)
        t.set_cache_fnc(cache_fnc_)
        t.built.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()

    def gui_add_group(self, dtb_entity):
        path = dtb_entity.path
        if self.gui_get_group_is_exists(path) is False:
            parent_gui = self.gui_get_group(dtb_entity.group)
            prx_item = parent_gui.add_child(
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
            prx_item.set_enable(False)
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
            parent_gui.set_status(parent_gui.ValidatorStatus.Normal)
            parent_gui.set_enable(True)
            #
            prx_item = parent_gui.add_child(
                dtb_entity.gui_name,
                icon=utl_gui_core.RscIconFile.get(dtb_entity.gui_icon_name),
            )
            #
            self._value_item_dict[path] = prx_item
            prx_item.set_gui_dcc_obj(dtb_entity, namespace=self.DCC_NAMESPACE)
            #
            prx_item.set_tool_tip(dtb_entity.to_string())
            #
            prx_item.set_checked(False)
            prx_item.set_enable(True)
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
            parent_gui.set_status(parent_gui.ValidatorStatus.Normal)
            parent_gui.set_enable(True)
            #
            gui_name = bsc_core.RawStrUnderlineOpt(path_opt.name).to_prettify()
            prx_item = parent_gui.add_child(
                gui_name,
                icon=utl_gui_core.RscIconFile.get('database/tag'),
            )
            #
            self._value_item_dict[path] = prx_item
            #
            prx_item.set_checked(False)
            prx_item.set_enable(True)
            prx_item.set_emit_send_enable(True)
            #
            prx_item.set_name('0', 1)
            return prx_item
        return self.gui_get(path)

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


class _GuiResourceOpt(_GuiBaseOpt):
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, list_view):
        super(_GuiResourceOpt, self).__init__(window, session, database_opt)
        #
        self._list_view = list_view
        self._item_dict = self._list_view._item_dict
        self._keys = set()

    def restore(self):
        self._list_view.set_clear()
        self._keys.clear()

    def gui_get_is_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get(self, path):
        return self._item_dict[path]

    def gui_register(self, path, prx_item):
        self._item_dict[path] = prx_item

    def gui_add(self, dtb_type, dtb_resource, semantic_tag_filter_data):
        def cache_fnc_():
            name_dict = collections.OrderedDict()
            pixmaps = []
            name_dict['resource'] = dtb_resource.gui_name
            for i_k, i_v in semantic_tag_filter_data.items():
                if '/geometry/fbx' in i_v:
                    i_pixmap = utl_gui_qt_core.QtPixmapMtd.get_by_file_ext('.fbx')
                    pixmaps.append(i_pixmap)
                #
                name_dict[bsc_core.DccPathDagOpt(i_k).get_name()] = ', '.join(
                    [bsc_core.DccPathDagOpt(j).get_name() for j in i_v]
                )
            #
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
            #
            preview_image_dtb_port = self._dtb_opt.get_entity(
                entity_type=self._dtb_opt.EntityTypes.Attribute,
                filters=[
                    ('node', 'is', dtb_version_port.value),
                    ('port', 'is', 'image_preview_file'),
                ]
            )
            image_args = None
            if preview_image_dtb_port:
                image_path_src = preview_image_dtb_port.value
                if bsc_core.StgFileOpt(image_path_src).get_is_exists() is True:
                    image_file_path, image_sp_cmd = bsc_core.ImgFileOpt(image_path_src).get_thumbnail_create_args(
                        width=256, ext='.png'
                    )
                    image_args = image_file_path, image_sp_cmd
            #
            drag_data = None
            if self._session.get_application() == 'katana':
                drag_data = {
                    'nodegraph/noderefs': 'rootNode',
                    # 'nodegraph/fileref': '/l/resource/td/asset/scene/empty.katana',
                    'pre-import/hook-option': self.get_callback_hook_option_fnc(
                        option_hook_key='dtb-callbacks/katana/resource-pre-import-by-drag',
                        dtb_entity=dtb_resource
                    ),
                    'import/hook-option': self.get_callback_hook_option_fnc(
                        option_hook_key='dtb-callbacks/katana/resource-import-by-drag',
                        dtb_entity=dtb_resource
                    )
                }
            #
            menu_content = self.get_dtb_entity_menu_content(dtb_resource)
            menu_content_extra = self.get_dtb_entity_menu_content(dtb_version)
            if menu_content_extra:
                menu_content.set_update(menu_content_extra.get_value())
            return name_dict, pixmaps, image_args, drag_data, menu_content

        def build_fnc_(data_):
            self.gui_show_deferred_fnc(
                dtb_type, dtb_resource, prx_item, data_
            )

        path = dtb_resource.path
        if self.gui_get_is_exists(path) is False:
            self._keys.add(dtb_resource.gui_name)
            #
            prx_item = self._list_view.create_item()
            self.gui_register(path, prx_item)
            prx_item.get_item()._update_item_semantic_tag_filter_keys_tgt_(
                semantic_tag_filter_data
            )
            prx_item.get_item()._update_item_keyword_filter_keys_tgt_(
                [dtb_resource.name, dtb_resource.gui_name]
            )
            prx_item.set_gui_dcc_obj(
                dtb_resource, namespace=self.DCC_NAMESPACE
            )
            prx_item.set_name(
                dtb_resource.gui_name
            )
            prx_item.set_sort_name_key(
                dtb_resource.gui_name
            )
            prx_item.set_gui_attribute(
                'path', dtb_type.path
            )
            prx_item.set_show_fnc(
                cache_fnc_, build_fnc_
            )
            keys = {bsc_core.DccPathDagOpt(j).get_name() for i_k, i_v in semantic_tag_filter_data.items() for j in i_v}
            keys.add(str(dtb_resource.gui_name).lower())
            keys.add(str(dtb_resource.name).lower())
            prx_item.set_keyword_filter_keys_tgt(keys)

            return prx_item
        return self.gui_get(path)

    def get_checked_dtb_resources(self):
        list_ = []
        _ = self._list_view.get_checked_items()
        for i in _:
            i_dtb_resource = i.get_gui_dcc_obj(self.DCC_NAMESPACE)
            list_.append(i_dtb_resource)
        return list_

    def gui_show_deferred_fnc(self, dtb_type, dtb_resource, prx_item, data):
        prx_item.set_check_enable(True)
        name_dict, pixmaps, image_args, drag_data, menu_content = data

        prx_item.set_image(
            utl_gui_core.RscIconFile.get('image_loading_failed_error')
        )

        prx_item.set_icons_by_pixmap(pixmaps)
        # image
        if image_args:
            image_file_path, image_sp_cmd = image_args
            prx_item.set_image(image_file_path)
            if image_sp_cmd is not None:
                prx_item.set_image_show_args(image_file_path, image_sp_cmd)
        else:
            prx_item.set_image(
                utl_gui_core.RscIconFile.get('image_loading_failed_error')
            )
        # drag action
        if drag_data:
            prx_item.set_drag_enable(True)
            prx_item.set_drag_data(drag_data)
            prx_item.connect_drag_pressed_to(
                self.drag_pressed_fnc
            )
            prx_item.connect_drag_released_to(
                self.drag_release_fnc
            )
        # menu
        if menu_content:
            prx_item.set_menu_content(menu_content)
        #
        prx_item.set_index_draw_enable(True)
        prx_item.set_icon_by_text(dtb_type.name)
        prx_item.set_name_dict(
            name_dict
        )
        prx_item.set_tool_tip(
            dtb_resource.to_string()
        )

    def get_callback_hook_option_fnc(self, option_hook_key, dtb_entity):
        return bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key=option_hook_key,
                #
                window_unique_id=self._window.get_window_unique_id(),
                database=self._dtb_opt.get_database(),
                database_configure=self._dtb_opt.get_database_configure(),
                database_configure_extend=self._dtb_opt.get_database_configure_extend(),
                #
                entity_type=dtb_entity.entity_type,
                entity=dtb_entity.path,
            )
        ).to_string()
    @classmethod
    def drag_pressed_fnc(cls, *args, **kwargs):
        mime_data, = args[0]
        key = 'pre-import/hook-option'
        if mime_data.hasFormat(key):
            hook_option = mime_data.data(key).data()
            ssn_commands.set_option_hook_execute(
                hook_option
            )
    @classmethod
    def drag_release_fnc(cls, *args, **kwargs):
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

    def get_current_dtb_entity(self):
        resource_selected_prx_items = self._list_view.get_selected_items()
        if resource_selected_prx_items:
            return resource_selected_prx_items[-1].get_gui_dcc_obj(self.DCC_NAMESPACE)


class _GuiDirectoryOpt(_GuiBaseOpt):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, tree_view):
        super(_GuiDirectoryOpt, self).__init__(window, session, database_opt)
        #
        self._tree_view = tree_view
        self._item_dict = self._tree_view._item_dict

        self.__thread_stack_index = 1

    def restore(self):
        self._tree_view.set_clear()

    def gui_get_is_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get(self, path):
        return self._item_dict[path]

    def gui_add_all_use_thread(self, dtb_version, path_cur=None):
        def cache_fnc_():
            return self.__thread_stack_index, self._dtb_opt.get_entities(
                entity_type=self._dtb_opt.EntityTypes.Storage,
                filters=[
                    ('kind', 'is', self._dtb_opt.Kinds.Directory),
                    ('group', 'is', dtb_version.path),
                ]
            )

        def build_fnc_(*args):
            _thread_stack_index, _dtb_directories = args[0]
            _version_stg_location = self._dtb_opt.get_property(version_dtb_path, 'location')
            for _i_dtb_storage in _dtb_directories:
                _i_storage_dtb_path = _i_dtb_storage.path
                _i_storage_stg_location = self._dtb_opt.get_property(_i_storage_dtb_path, 'location')
                _i_sub_path = _i_storage_stg_location[len(_version_stg_location):]
                if _thread_stack_index == self.__thread_stack_index:
                    self.gui_add_one(_i_sub_path, _i_dtb_storage, is_current=_i_sub_path == path_cur)

        def post_fnc_():
            pass

        version_dtb_path = dtb_version.path
        version_path_opt = bsc_core.DccPathDagOpt(version_dtb_path)
        self.gui_add_root(version_path_opt.name)

        self.__thread_stack_index += 1

        t = utl_gui_qt_core.QtBuildThread(self._window.widget)
        t.set_cache_fnc(cache_fnc_)
        t.built.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()

    def gui_add_all(self, dtb_version, path_cur=None):
        version_dtb_path = dtb_version.path
        version_path_opt = bsc_core.DccPathDagOpt(version_dtb_path)
        #
        self.gui_add_root(version_path_opt.name)
        dtb_directories = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.Storage,
            filters=[
                ('kind', 'is', self._dtb_opt.Kinds.Directory),
                ('group', 'is', dtb_version.path),
            ]
        )
        version_stg_location = self._dtb_opt.get_property(version_dtb_path, 'location')
        for i_dtb_storage in dtb_directories:
            i_storage_dtb_path = i_dtb_storage.path
            i_storage_stg_location = self._dtb_opt.get_property(i_storage_dtb_path, 'location')
            i_sub_path = i_storage_stg_location[len(version_stg_location):]
            #
            self.gui_add_one(i_sub_path, i_dtb_storage)

    def gui_add_one(self, sub_path, dtb_directory, is_current=False):
        path_opt = bsc_core.DccPathDagOpt(sub_path)
        ancestors = path_opt.get_ancestors()
        if ancestors:
            ancestors.reverse()
            #
            for i_ancestor in ancestors:
                i_ancestor_path = i_ancestor.get_path()
                self.gui_add_group(i_ancestor_path)
        #
        self.gui_add(sub_path, dtb_directory, is_current)

    def gui_add_root(self, name):
        path = '/'
        if self.gui_get_is_exists(path) is False:
            prx_item = self._tree_view.create_item(
                name,
                icon=utl_gui_core.RscIconFile.get('database/group'),
            )
            self._item_dict[path] = prx_item
            prx_item.set_expanded(True)
            # prx_item.set_checked(False)
            return True, prx_item
        return False, self.gui_get(path)

    def gui_add_group(self, sub_path):
        if self.gui_get_is_exists(sub_path) is False:
            path_opt = bsc_core.DccPathDagOpt(sub_path)
            #
            parent_gui = self.gui_get(path_opt.get_parent_path())
            #
            prx_item = parent_gui.add_child(
                path_opt.name,
                icon=utl_gui_qt_core.QtDccMtd.get_qt_folder_icon(),
            )
            self._item_dict[sub_path] = prx_item
            prx_item.set_tool_tip(sub_path)
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            return prx_item
        return self.gui_get(sub_path)

    def gui_add(self, sub_path, dtb_directory, is_current=False):
        if self.gui_get_is_exists(sub_path) is False:
            path_opt = bsc_core.DccPathDagOpt(sub_path)
            #
            parent_gui = self.gui_get(path_opt.get_parent_path())
            #
            location = self.get_dtb_entity_location(dtb_directory)
            #
            prx_item = parent_gui.add_child(
                path_opt.name,
                icon=utl_gui_core.RscIconFile.get('database/group'),
            )
            self._item_dict[sub_path] = prx_item
            prx_item.set_gui_dcc_obj(
                dtb_directory, namespace=self.DCC_NAMESPACE
            )
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
            if bsc_core.StorageMtd.get_is_exists(location) is True:
                prx_item.set_status(prx_item.ValidatorStatus.Normal)
            else:
                prx_item.set_status(prx_item.ValidatorStatus.Disable)
            #
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            prx_item._path = sub_path
            if is_current is True:
                prx_item.set_selected(True)
            return prx_item
        return self.gui_get(sub_path)

    def gui_show_deferred_fnc(self, dtb_directory, prx_item):
        pass

    def get_current_dtb_entity(self):
        resource_selected_prx_items = self._tree_view.get_selected_items()
        if resource_selected_prx_items:
            return resource_selected_prx_items[-1].get_gui_dcc_obj(self.DCC_NAMESPACE)


class _GuiFileOpt(_GuiBaseOpt):
    DCC_NAMESPACE = 'database'
    def __init__(self, window, session, database_opt, list_view):
        super(_GuiFileOpt, self).__init__(window, session, database_opt)
        #
        self._list_view = list_view
        self._item_dict = self._list_view._item_dict
        self._keys = set()

    def restore(self):
        self._list_view.set_clear()
        self._keys.clear()

    def gui_get_is_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get(self, path):
        return self._item_dict[path]

    def gui_add(self, file_path):
        def cache_fnc_():
            return []

        def build_fnc_(*args):
            if file_opt.get_ext() in ['.jpg', '.png']:
                image_file_path, image_sp_cmd = bsc_core.ImgFileOpt(file_path).get_thumbnail_create_args(
                    width=128, ext='.png'
                )
                prx_item.set_image(image_file_path)
                if image_sp_cmd is not None:
                    prx_item.set_image_show_args(image_file_path, image_sp_cmd)
            else:
                file_icon = utl_gui_qt_core.QtDccMtd.get_qt_file_icon(file_path)
                if file_icon:
                    pixmap = file_icon.pixmap(80, 80)
                    prx_item.set_image(
                        pixmap
                    )

        def copy_fnc_():
            _xml_File = bsc_core.RscFileMtd.get('asset/library/katana/image.xml')
            if _xml_File:
                _xml_data = bsc_core.StgFileOpt(_xml_File).set_read()
                _xml_data = _xml_data.replace(
                    'TEXTURE_FILE', file_opt.get_path()
                )
                utl_gui_qt_core.QtUtilMtd.set_text_to_clipboard(
                    _xml_data
                )
        #
        if self.gui_get_is_exists(file_path) is False:
            file_opt = bsc_core.StgFileOpt(file_path)
            prx_item = self._list_view.create_item()
            self._item_dict[file_path] = prx_item
            prx_item.set_name(file_opt.get_name())
            prx_item.set_drag_enable(True)
            prx_item.set_drag_urls([file_opt.get_path()])
            prx_item.set_show_fnc(
                cache_fnc_, build_fnc_
            )
            prx_item.connect_press_clicked_to(copy_fnc_)
            return prx_item
        return self.gui_get(file_path)


class _GuiGuideOpt(_GuiBaseOpt):
    def __init__(self, window, session, database_opt, guide_bar, tree_view, list_view):
        super(_GuiGuideOpt, self).__init__(window, session, database_opt)
        #
        self._guide_bar = guide_bar
        self._tree_view = tree_view
        self._list_view = list_view

        self._types = [
            None,
            self._dtb_opt.EntityTypes.CategoryGroup,
            self._dtb_opt.EntityTypes.Category,
            self._dtb_opt.EntityTypes.Type
        ]
        self._guide_bar.set_types(self._types)
        self._guide_bar.set_dict(self._tree_view._item_dict)

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
            for i in self._window._dtb_superclass_paths:
                if i not in self._tree_view._item_dict:
                    self._tree_view._item_dict[i] = None
            #
            self._guide_bar.set_path(path)


class _GuiUsdStageViewOpt(_GuiBaseOpt):
    def __init__(self, window, session, database_opt, usd_stage_view):
        super(_GuiUsdStageViewOpt, self).__init__(window, session, database_opt)
        self._usd_stage_view = usd_stage_view
        self.__thread_stack_index = 1

    def get_texture_dict(self, dtb_version):
        dict_ = {}
        for i_key in utl_configure.TextureTypes.All:
            i_dtb_path = '{}/texture_{}_file'.format(dtb_version.path, i_key)
            i_file_path = self._dtb_opt.get_property(
                i_dtb_path, 'location'
            )
            if i_file_path is not None:
                i_file_opt = bsc_core.StgFileOpt(i_file_path)
                if i_file_opt.get_ext() == '.exr':
                    i_file_opt = i_file_opt.set_ext_repath_to('.jpg')
                #
                if i_file_opt.get_is_file() is True:
                    # map to usd key
                    if i_key in utl_configure.TextureTypes.UsdPreviewMapper:
                        i_key = utl_configure.TextureTypes.UsdPreviewMapper[i_key]
                    #
                    dict_[i_key] = i_file_opt.get_path()
        return dict_

    def get_usd_file(self, dtb_resource, dtb_version):
        version_stg_path = self._dtb_opt.get_property(
            dtb_version.path, 'location'
        )
        usd_file_path = '{}/geometry/usd/{}.usd'.format(version_stg_path, dtb_resource.name)
        if bsc_core.StgPathMtd.get_is_exists(usd_file_path):
            return usd_file_path
        return bsc_core.RscFileMtd.get('asset/library/geo/sphere.usda')

    def refresh_textures_use_thread(self, dtb_resource, dtb_version, use_as_imperfection=False):
        def cache_fnc_():
            self._usd_stage_view.refresh_usd_stage_for_asset_preview(
                self.get_usd_file(dtb_resource, dtb_version),
                self.get_texture_dict(dtb_version),
                use_as_imperfection=use_as_imperfection
            )
            return [self.__thread_stack_index, None]

        def build_fnc_(*args):
            _thread_stack_index, _ = args[0]
            if _thread_stack_index == self.__thread_stack_index:
                self._usd_stage_view.refresh_usd_view_draw()

        def post_fnc_():
            pass

        self.__thread_stack_index += 1

        t = utl_gui_qt_core.QtBuildThread(self._window.widget)
        t.set_cache_fnc(cache_fnc_)
        t.built.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()

    def refresh_textures(self, dtb_resource, dtb_version, use_as_imperfection=False):
        self._usd_stage_view.refresh_usd_stage_for_texture_preview(
            self.get_texture_dict(dtb_version)
        )
        self._usd_stage_view.refresh_usd_view_draw()


class AbsPnlAbsResourceLibrary(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = 'database'
    THREAD_STEP = 8
    FILTER_MAXIMUM = 50
    HISTORY_KEY = 'gui.resource-library'
    def set_all_setup(self):
        #
        self._item_frame_size = self._session.gui_configure.get('item_frame_size')
        self._item_icon_frame_size = self._session.gui_configure.get('item_icon_frame_size')
        self._item_icon_size = self._session.gui_configure.get('item_icon_size')

        v_qt_widget = qt_widgets.QtWidget()
        self.add_widget(v_qt_widget)
        v_qt_layout = qt_widgets.QtVBoxLayout(v_qt_widget)
        v_qt_layout.setContentsMargins(0, 0, 0, 0)
        # top
        self._top_tool_bar = prx_widgets.PrxHToolBar()
        v_qt_layout.addWidget(self._top_tool_bar._qt_widget)
        self._top_tool_bar.set_expanded(True)
        self._top_tool_bar.set_left_alignment_mode()
        #   guide
        self._guide_tool_box = prx_widgets.PrxHToolBox()
        self._top_tool_bar.add_widget(self._guide_tool_box)
        self._guide_tool_box.set_expanded(True)
        self._guide_tool_box.set_size_mode(1)
        #
        self._type_guide_bar = prx_widgets.PrxGuideBar()
        self._guide_tool_box.add_widget(self._type_guide_bar)
        self._type_guide_bar.set_name('guide for type')
        #   tag
        self._tag_tool_box = prx_widgets.PrxHToolBox()
        self._top_tool_bar.add_widget(self._tag_tool_box)
        # self._tag_tool_box.set_expanded(True)
        self._tag_tool_box.set_size_mode(1)
        #
        self._tag_bar = prx_widgets.PrxTagBar()
        self._tag_tool_box.add_widget(self._tag_bar)
        #
        h_qt_widget = qt_widgets.QtWidget()
        v_qt_layout.addWidget(h_qt_widget)
        h_qt_layout = qt_widgets.QtHBoxLayout(h_qt_widget)
        h_qt_layout.setContentsMargins(0, 0, 0, 0)
        #
        main_scroll_area = prx_widgets.PrxHScrollArea()
        h_qt_layout.addWidget(main_scroll_area._qt_widget)
        #
        self._main_h_s = prx_widgets.PrxHSplitter()
        main_scroll_area.add_widget(self._main_h_s)
        #
        filter_v_s = prx_widgets.PrxVSplitter()
        self._main_h_s.add_widget(filter_v_s)
        #
        self._type_prx_view = prx_widgets.PrxTreeView()
        filter_v_s.add_widget(self._type_prx_view)
        self._type_prx_view.set_filter_entry_tip('fiter by type ...')
        # self._type_prx_view.get_top_tool_bar().set_expanded(True)
        self._type_prx_view.set_selection_use_single()
        self._type_prx_view.set_header_view_create(
            [('type', 3), ('count', 1)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 48
        )
        self._type_prx_view.connect_item_select_changed_to(
            self.__execute_gui_refresh_for_resources_by_type_selection_
        )
        #
        self._tag_prx_view = prx_widgets.PrxTreeView()
        filter_v_s.add_widget(self._tag_prx_view)
        self._tag_prx_view.set_filter_entry_tip('filter by tag ...')
        self._tag_prx_view.set_selection_disable()
        self._tag_prx_view.set_header_view_create(
            [('tag', 3), ('count', 1)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 48
        )
        self._tag_prx_view.connect_item_check_changed_to(
            self.__execute_gui_refresh_for_resources_by_property_check_
        )
        #
        filter_v_s.set_fixed_size_at(1, 320)
        #
        self._resource_prx_view = prx_widgets.PrxListView()
        self._main_h_s.add_widget(self._resource_prx_view._qt_widget)
        # self._resource_prx_view.set_draw_enable(True)
        self._resource_prx_view.get_check_tool_box().set_visible(True)
        self._resource_prx_view.get_scale_switch_tool_box().set_visible(True)
        self._resource_prx_view.get_sort_switch_tool_box().set_visible(True)
        self._resource_prx_view.set_filter_entry_tip('filter by keyword ...')
        #
        self._resource_prx_view.get_top_tool_bar().set_expanded(True)
        self._resource_prx_view.set_item_frame_size_basic(*self._item_frame_size)
        self._resource_prx_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._resource_prx_view.set_item_icon_size(*self._item_icon_size)
        self._resource_prx_view.set_item_icon_frame_draw_enable(True)
        self._resource_prx_view.set_item_name_frame_draw_enable(True)
        self._resource_prx_view.set_item_names_draw_range([None, 1])
        self._resource_prx_view.set_item_image_frame_draw_enable(True)
        self._resource_prx_view.connect_item_select_changed_to(
            self.__execute_gui_refresh_for_storage_directories_
        )
        self._resource_prx_view.connect_refresh_action_to(
            self.__execute_gui_refresh_for_resources_by_type_selection_
        )
        #
        extra_v_s = prx_widgets.PrxVSplitter()
        self._main_h_s.add_widget(extra_v_s)
        #
        if LOAD_INDEX == 0:
            self._usd_stage_prx_view = prx_widgets.PrxUsdStageViewProxy()
        else:
            self._usd_stage_prx_view = prx_widgets.PrxUsdStageView()
        #
        extra_v_s.add_widget(self._usd_stage_prx_view)
        #
        self._directory_prx_view = prx_widgets.PrxTreeView()
        extra_v_s.add_widget(self._directory_prx_view)
        self._directory_prx_view.set_header_view_create(
            [('directory', 1)]
        )
        #
        self._directory_prx_view.connect_item_select_changed_to(
            self.__execute_gui_refresh_for_storage_files_
        )
        #
        self._file_prx_view = prx_widgets.PrxListView()
        extra_v_s.add_widget(self._file_prx_view)
        self._file_frame_size = 80, 124
        self._item_name_frame_size = 80, 44
        self._file_prx_view.set_item_frame_size_basic(*self._file_frame_size)
        self._file_prx_view.set_item_name_frame_size(*self._item_name_frame_size)
        self._file_prx_view.set_item_icon_frame_draw_enable(False)
        self._file_prx_view.set_item_name_frame_draw_enable(False)
        self._file_prx_view.set_item_names_draw_range([None, 1])
        self._file_prx_view.set_item_image_frame_draw_enable(False)
        #
        extra_v_s.set_fixed_size_at(0, 320)
        self._main_h_s.set_fixed_size_at(0, 320)
        self._main_h_s.set_fixed_size_at(2, 320)
        if bsc_core.ApplicationMtd.get_is_dcc():
            self._main_h_s.set_contract_right_or_bottom_at(2)
        #
        self._type_guide_bar.connect_user_text_choose_accepted_to(self.gui_guide_choose_cbk)
        self._type_guide_bar.connect_user_text_press_accepted_to(self.gui_guide_press_cbk)

        self._dtb_cfg_file_path = bsc_core.CfgFileMtd.get_yaml('database/library/resource-basic')
        self._dtb_cfg = bsc_objects.Configure(value=self._dtb_cfg_file_path)

        self._dtb_superclass_paths = self._dtb_cfg.get('category_groups')

        self._dtb_superclass_name_history = utl_core.History.get_latest(self.HISTORY_KEY)
        if self._dtb_superclass_name_history is not None:
            self._dtb_superclass_path_cur = self._dtb_superclass_name_history
        else:
            self._dtb_superclass_path_cur = self._dtb_superclass_paths[0]
        self._dtb_superclass_name_cur = bsc_core.DccPathDagOpt(self._dtb_superclass_path_cur).get_name()

        self.refresh_all()

        self.setup_menu()

    def setup_menu(self):
        menu = self.create_menu('tool')
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
                    database_configure_extend=self._dtb_opt.get_database_configure_extend(),
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.ArgDictStringOpt(i_kwargs).to_string(),
                )
            return ssn_commands.get_menu_content_by_hook_options(options)

    def restore_variants(self):
        self.__running_threads_stacks = None

        self.__thread_stack_index = 0

        self.__attribute_options = {}
        self.__attribute_options_default = {}
        self.__attribute_filters = []

        self.__attribute_count_dict = {}

        self._directory_path_cur = None

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAbsResourceLibrary, self).__init__(session, *args, **kwargs)

    def refresh_all(self):
        if self._dtb_superclass_path_cur in self._dtb_superclass_paths:
            utl_core.History.append(
                self.HISTORY_KEY, self._dtb_superclass_path_cur
            )

        self._dtb_superclass_name_cur = bsc_core.DccPathDagOpt(self._dtb_superclass_path_cur).get_name()
        self._dtb_cfg_file_path_extend = bsc_core.CfgFileMtd.get_yaml(
            'database/library/resource-{}'.format(self._dtb_superclass_name_cur)
        )
        #
        self._dtb_opt = dtb_objects.DtbResourceLibraryOpt(
            self._dtb_cfg_file_path, self._dtb_cfg_file_path_extend
        )
        #
        self._gui_guide_opt = _GuiGuideOpt(
            self, self._session, self._dtb_opt, self._type_guide_bar,
            self._type_prx_view, self._resource_prx_view
        )
        #
        self._type_prx_view.connect_item_select_changed_to(
            self._gui_guide_opt.gui_refresh
        )
        self._resource_prx_view.connect_item_select_changed_to(
            self._gui_guide_opt.gui_refresh
        )
        #
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

        self._gui_usd_stage_view_opt = _GuiUsdStageViewOpt(
            self, self._session, self._dtb_opt, self._usd_stage_prx_view
        )

        self.gui_refresh_fnc()

    def get_gui_resource_opt(self):
        return self._gui_resource_opt

    def gui_guide_choose_cbk(self, text):
        if text is not None:
            self._type_prx_view.select_item_by_key(
                text,
                exclusive=True
            )
            #
            if text in self._dtb_superclass_paths:
                self._dtb_superclass_path_cur = text
                #
                self.refresh_all()

    def gui_guide_press_cbk(self, text):
        if text is not None:
            self._type_prx_view.select_item_by_key(
                text,
                exclusive=True
            )

    def __gui_resource_completion_gain_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = fnmatch.filter(
                self._gui_resource_opt._keys, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def __restore_thread_stack_(self):
        if self.__running_threads_stacks:
            [i.set_kill() for i in self.__running_threads_stacks]
        #
        self.__running_threads_stacks = []

    def gui_refresh_fnc(self):
        self._gui_type_opt.restore()
        self._gui_tag_opt.restore()
        self._gui_resource_opt.restore()
        self._type_guide_bar.set_clear()
        # type
        is_create, prx_item = self._gui_type_opt.gui_add_root()
        if is_create is True:
            prx_item.set_expanded(True, ancestors=True)
            prx_item.set_selected(True)
            self._gui_type_opt.gui_add_all_category_groups()
            self.__gui_add_for_all_types_()
            # properties
            if self._qt_thread_enable is True:
                self._gui_tag_opt.gui_add_all_groups_use_thread()
            else:
                self._gui_tag_opt.gui_add_all_groups()
    # build for types
    def __gui_add_for_all_types_(self):
        def post_fnc_():
            self._end_timestamp = bsc_core.TimeMtd.get_timestamp()
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
        self.__start_timestamp = bsc_core.TimeMtd.get_timestamp()
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
            with self.gui_bustling():
                for i_dtb_categories in dtb_categories_map:
                    [self._gui_type_opt.gui_add_category(i) for i in i_dtb_categories]
                    ts.register(
                        cache_fnc=functools.partial(self._gui_type_opt.gui_cache_fnc_for_types_by_categories, i_dtb_categories),
                        build_fnc=self._gui_type_opt.gui_build_fnc_for_types
                    )
            #
            ts.set_start()
            #
            self.set_window_close_connect_to(quit_fnc_)
        else:
            with self.gui_progressing(maximum=len(dtb_categories_map), label='gui-add for type') as g_p:
                for i_dtb_categories in dtb_categories_map:
                    g_p.set_update()
                    #
                    [self._gui_type_opt.gui_add_category(i) for i in i_dtb_categories]
                    self._gui_type_opt.gui_build_fnc_for_types(
                        self._gui_type_opt.gui_cache_fnc_for_types_by_categories(i_dtb_categories)
                    )
    # build for resources
    def __execute_gui_refresh_for_resources_by_property_check_(self):
        filter_data_src = self._gui_tag_opt.get_filter_data()
        qt_view = self._resource_prx_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._resource_prx_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

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
            with self.gui_bustling():
                for i_dtb_types in dtb_types_map:
                    ts.register(
                        cache_fnc=functools.partial(
                            self.__batch_gui_cache_fnc_for_resources_by_entities_, i_dtb_types, thread_stack_index
                        ),
                        build_fnc=self.__batch_gui_build_fnc_for_resources_
                    )
            #
            ts.set_start()
            #
            self.set_window_close_connect_to(quit_fnc_)
        else:
            with self.gui_progressing(maximum=len(dtb_types_map), label='batch gui-add resource') as g_p:
                for i_dtb_types in dtb_types_map:
                    g_p.set_update()
                    self.__batch_gui_build_fnc_for_resources_(
                        self.__batch_gui_cache_fnc_for_resources_by_entities_(i_dtb_types, thread_stack_index)
                    )

    def __batch_gui_cache_fnc_for_resources_by_entities_(self, dtb_types, thread_stack_index):
        if thread_stack_index == self.__thread_stack_index:
            if dtb_types:
                dtb_assigns = self._dtb_opt.get_entities(
                    entity_type=self._dtb_opt.EntityTypes.Types,
                    filters=[
                        ('kind', 'is', self._dtb_opt.Kinds.ResourceType),
                        #
                        ('value', 'in', [i.path for i in dtb_types])
                    ]
                )
                return [dtb_assigns, thread_stack_index]

    def __batch_gui_build_fnc_for_resources_(self, *args):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.set_quit()

        if args[0] is None:
            return

        dtb_assigns, thread_stack_index = args[0]
        if thread_stack_index == self.__thread_stack_index:
            dtb_type_assigns_map = bsc_core.RawListMtd.set_grid_to(
                dtb_assigns, self.THREAD_STEP
            )
            if self._qt_thread_enable is True:
                ts = utl_gui_qt_core.QtBuildThreadStack(self.widget)
                self.__running_threads_stacks.append(ts)
                ts.run_finished.connect(post_fnc_)
                for i_dtb_type_assigns in dtb_type_assigns_map:
                    ts.register(
                        cache_fnc=functools.partial(
                            self.__gui_cache_fnc_for_resources_, i_dtb_type_assigns, thread_stack_index
                        ),
                        build_fnc=self.__gui_build_fnc_for_resources_
                    )
                #
                ts.set_start()
                #
                self.set_window_close_connect_to(quit_fnc_)
            else:
                with self.gui_progressing(maximum=len(dtb_type_assigns_map), label='gui-add resources') as g_p:
                    for i_dtb_type_assigns in dtb_type_assigns_map:
                        g_p.set_update()
                        self.__gui_build_fnc_for_resources_(
                            self.__gui_cache_fnc_for_resources_(i_dtb_type_assigns, thread_stack_index)
                        )

    def __gui_cache_fnc_for_resources_(self, dtb_assigns, thread_stack_index):
        build_args = []

        for i_dtb_assign in dtb_assigns:
            i_dtg_type = self._dtb_opt.get_entity(
                entity_type=self._dtb_opt.EntityTypes.Type,
                filters=[
                    ('path', 'is', i_dtb_assign.value)
                ]
            )
            i_dtb_resource = self._dtb_opt.get_entity(
                entity_type=self._dtb_opt.EntityTypes.Resource,
                filters=[
                    ('path', 'is', i_dtb_assign.node)
                ]
            )
            #
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
                (i_dtg_type, i_dtb_resource, i_tag_args, i_semantic_tag_filter_data)
            )
        return [build_args, thread_stack_index]

    def __gui_build_fnc_for_resources_(self, *args):
        build_args, thread_stack_index = args[0]

        if args[0] is None:
            return

        if thread_stack_index == self.__thread_stack_index:
            with self.gui_bustling():
                for i_dtg_type, i_dtb_resource, i_dtb_tags, i_semantic_tag_filter_data in build_args:
                    self._gui_resource_opt.gui_add(
                        i_dtg_type, i_dtb_resource, i_semantic_tag_filter_data
                    )
                    #
                    for j_dtb_tag in i_dtb_tags:
                        self._gui_tag_opt.gui_register(
                            j_dtb_tag
                        )
                #
                self._resource_prx_view.refresh_viewport_showable_auto()
    # build for textures
    def __execute_gui_refresh_for_storage_directories_(self):
        self._gui_directory_opt.restore()
        self._gui_file_opt.restore()
        #
        if self._main_h_s.get_is_contracted_at(2) is False:
            dtb_entity = self._gui_resource_opt.get_current_dtb_entity()
            if dtb_entity is not None:
                self.__gui_refresh_usd_stage_(dtb_entity)
                self.__gui_add_directories_(dtb_entity)

    def __gui_refresh_usd_stage_(self, dtb_resource):
        dtb_version = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Version,
            filters=[
                ('path', 'is', self._dtb_opt.get_property(dtb_resource.path, 'version')),
            ],
        )
        use_as_imperfection = self._dtb_superclass_name_cur in {'imperfection', 'texture'}
        if self._qt_thread_enable is True:
            self._gui_usd_stage_view_opt.refresh_textures_use_thread(dtb_resource, dtb_version, use_as_imperfection)
        else:
            self._gui_usd_stage_view_opt.refresh_textures(dtb_resource, dtb_version, use_as_imperfection)

    def __gui_add_directories_(self, dtb_resource):
        dtb_version = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Version,
            filters=[
                ('path', 'is', self._dtb_opt.get_property(dtb_resource.path, 'version')),
            ],
        )
        if self._qt_thread_enable is True:
            self._gui_directory_opt.gui_add_all_use_thread(dtb_version, self._directory_path_cur)
        else:
            self._gui_directory_opt.gui_add_all(dtb_version, self._directory_path_cur)

    def __execute_gui_refresh_for_storage_files_(self):
        self._gui_file_opt.restore()
        current_item = self._directory_prx_view.get_current_item()
        if current_item:
            self._directory_path_cur = current_item._path
        #
        if self._main_h_s.get_is_contracted_at(2) is False:
            dtb_entity = self._gui_directory_opt.get_current_dtb_entity()
            if dtb_entity is not None:
                self.__gui_add_files_(dtb_entity)

    def __gui_add_files_(self, dtb_storage):
        location = self._dtb_opt.get_property(
            dtb_storage.path, 'location'
        )
        if location:
            location_opt = bsc_core.StgDirectoryOpt(location)
            all_file_paths = location_opt.get_all_file_paths()
            for i in all_file_paths:
                self._gui_file_opt.gui_add(i)
