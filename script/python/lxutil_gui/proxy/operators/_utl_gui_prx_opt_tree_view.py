# coding:utf-8
import collections
import functools

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil_gui.proxy import utl_gui_prx_core


class PrxDccObjTreeViewSelectionOpt(object):
    def __init__(self, prx_tree_view, dcc_selection_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._dcc_selection_cls = dcc_selection_cls
        #
        self._dcc_namespace = dcc_namespace
    @classmethod
    def _set_dcc_select_(cls, prx_tree_view, dcc_selection_cls, dcc_namespace):
        if dcc_selection_cls is not None:
            obj_paths = []
            gui_items = prx_tree_view._get_selected_items_()
            for gui_item in gui_items:
                prx_item = gui_item.gui_proxy
                dcc_obj = prx_item.get_gui_dcc_obj(namespace=dcc_namespace)
                if dcc_obj is not None:
                    obj_paths.append(dcc_obj.path)
            #
            if obj_paths:
                dcc_selection_cls(obj_paths).set_all_select()
            else:
                dcc_selection_cls.set_clear()

    def set_select(self):
        self._set_dcc_select_(
            prx_tree_view=self._prx_tree_view,
            dcc_selection_cls=self._dcc_selection_cls,
            dcc_namespace=self._dcc_namespace
        )


class PrxDccObjTreeViewGainOpt(object):
    def __init__(self, prx_tree_view, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._dcc_namespace = dcc_namespace

    def get_checked_args(self):
        lis = []
        for prx_item in self._prx_tree_view.get_all_items():
            if prx_item.get_is_checked() is True:
                obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)
                if obj is not None:
                    lis.append((prx_item, obj))
        return lis


class PrxDccObjTreeViewTagFilterOpt(object):
    COUNT_COLUMN = 1
    def __init__(self, prx_tree_view_src, prx_tree_view_tgt, prx_tree_item_cls):
        self._prx_tree_view_src = prx_tree_view_src
        self._prx_tree_view_tgt = prx_tree_view_tgt
        #
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._filter_content = bsc_objects.Content(
            value=collections.OrderedDict()
        )
        #
        self._dcc_obj_dict = {}
        self._dcc_selection_cls = None
        self._dcc_namespace = None

        self._namespace_src = 'filter'

        self._obj_add_dict = self._prx_tree_view_src._item_dict
        #
        self._prx_tree_view_src.set_item_check_changed_connect_to(
            self.set_filter
        )

    def set_dcc_selection_args(self, dcc_selection_cls, dcc_namespace):
        self._dcc_selection_cls = dcc_selection_cls
        self._dcc_namespace = dcc_namespace

    def set_select(self):
        PrxDccObjTreeViewSelectionOpt._set_dcc_select_(
            prx_tree_view=self._prx_tree_view_src,
            dcc_selection_cls=self._dcc_selection_cls,
            dcc_namespace=self._dcc_namespace
        )

    def set_restore(self):
        self._filter_content = bsc_objects.Content(
            value=collections.OrderedDict()
        )
        self._dcc_obj_dict = {}

    def _to_filter_key_path_(self, key):
        return self._filter_content._to_key_path_(key)

    def set_tgt_item_tag_update(self, key, prx_item_tgt, dcc_obj=None):
        self.set_register(
            prx_item_tgt,
            [key],
            dcc_obj=dcc_obj
        )

    def _set_item_src_show_deferred_(self, prx_item):
        path_dag_opt = prx_item.get_gui_dcc_obj(namespace=self._namespace_src)
        name = path_dag_opt.name
        path = path_dag_opt.path
        prx_item.set_name(name)
        prx_item.set_icon_by_name_text(path, 0)
        prx_item.set_tool_tip(path)

    def _set_prx_item_src_add_(self, path):
        path_dag_opt = bsc_core.DccPathDagOpt(path)
        key = path_dag_opt.path
        if key in self._obj_add_dict:
            return False, self._obj_add_dict[key]
        #
        _kwargs = dict(
            name='...',
            item_class=self._prx_tree_item_cls,
            filter_key=key
        )
        #
        parent_path = bsc_core.DccPathDagOpt(path).get_parent_path()
        if parent_path in self._obj_add_dict:
            prx_item_parent = self._obj_add_dict[parent_path]
            prx_item = prx_item_parent.set_child_add(
                **_kwargs
            )
        else:
            prx_item = self._prx_tree_view_src.set_item_add(
                **_kwargs
            )
        #
        prx_item.set_checked(True)
        prx_item.set_emit_send_enable(True)
        prx_item.set_gui_dcc_obj(path_dag_opt, self._namespace_src)
        #
        prx_item.set_show_method(
            self._set_item_src_show_deferred_(
                prx_item
            )
        )
        return True, prx_item

    def set_src_items_refresh(self, expand_depth=None):
        self._prx_tree_view_src.set_clear()
        #
        leaf_paths = self._filter_content.get_leaf_key_as_paths()
        all_paths = self._filter_content.get_key_as_paths()
        all_paths.sort()
        all_paths = bsc_core.TextsOpt(all_paths).set_sort_to()
        for path in all_paths:
            i_is_create, i_prx_item_src = self._set_prx_item_src_add_(path)
            if path in leaf_paths:
                tag_filter_key = path
                i_prx_item_src.set_tag_filter_src_key_add(tag_filter_key)
            #
            if path in self._dcc_obj_dict:
                dcc_obj = self._dcc_obj_dict[path]
                if self._dcc_namespace is not None:
                    i_prx_item_src.set_gui_dcc_obj(dcc_obj, namespace=self._dcc_namespace)
        #
        if isinstance(expand_depth, int):
            self._prx_tree_view_src.set_items_expand_by_depth(expand_depth)
        else:
            self._prx_tree_view_src.set_all_items_expand()

    def set_filter_statistic(self):
        target_filter_tag_item_prx_dict = self._prx_tree_view_tgt.get_tag_filter_tgt_statistic_raw()
        for i_prx_item_src in self._prx_tree_view_src._item_dict.values():
            tag_filter_src_keys = i_prx_item_src.get_tag_filter_src_keys()
            if tag_filter_src_keys:
                for tag_filter_src_key in tag_filter_src_keys:
                    if tag_filter_src_key in target_filter_tag_item_prx_dict:
                        tgt_item_prxes = target_filter_tag_item_prx_dict[tag_filter_src_key]
                        if tgt_item_prxes:
                            states = self._prx_tree_view_tgt.get_item_states(tgt_item_prxes)
                            if i_prx_item_src.get_check_enable() is True:
                                if utl_gui_prx_core.State.ERROR in states:
                                    i_prx_item_src.set_error_state()
                                elif utl_gui_prx_core.State.WARNING in states:
                                    i_prx_item_src.set_warning_state()
                                # else:
                                #     i_prx_item_src.set_adopt_state()
                                #
                                i_prx_item_src.set_name(str(len(tgt_item_prxes)), self.COUNT_COLUMN)
                                #
                                brushes = self._prx_tree_view_tgt.get_item_state_colors(tgt_item_prxes)
                                i_prx_item_src.set_foregrounds_raw(brushes)
                                #
                                i_prx_item_src.set_states_raw(states)
                            else:
                                i_prx_item_src.set_name('N/a', self.COUNT_COLUMN)
                                #
                                i_prx_item_src.set_foregrounds_raw([])
                                #
                                i_prx_item_src.set_states_raw([])
                            #
                            i_prx_item_src.set_hidden(boolean=False, ancestors=True)
                        else:
                            i_prx_item_src.set_hidden(boolean=True, ancestors=True)
                    else:
                        i_prx_item_src.set_hidden(boolean=True, ancestors=True)

    def set_filter(self):
        tag_filter_src_all_keys = []
        for i_prx_item_src in self._prx_tree_view_src._item_dict.values():
            tag_filter_src_keys = i_prx_item_src.get_tag_filter_src_keys()
            for tag_filter_src_key in tag_filter_src_keys:
                if i_prx_item_src.get_is_checked() is True:
                    if tag_filter_src_key not in tag_filter_src_all_keys:
                        tag_filter_src_all_keys.append(tag_filter_src_key)
        #
        self._prx_tree_view_tgt.set_tag_filter_tgt_keys(tag_filter_src_all_keys)

    def get_filter_dict(self):
        dic = collections.OrderedDict()
        for i_prx_item_src in self._prx_tree_view_src._item_dict.values():
            i_key = i_prx_item_src.get_path()
            i_value = i_prx_item_src.get_is_checked()
            dic[i_key] = i_value
        return dic

    def set_filter_by_dict(self, dic):
        prx_items = self._prx_tree_view_src.get_all_leaf_items()
        for i_prx_item in prx_items:
            i_path = i_prx_item.get_path()
            if i_path in dic:
                i_prx_item.set_checked(dic[i_path])
            else:
                i_prx_item.set_checked(False)

        self.set_filter()

    def set_register(self, prx_item_tgt, keys, dcc_obj=None, expand_depth=1):
        for i_key in keys:
            i_path = self._to_filter_key_path_(i_key)
            #
            prx_item_tgt.set_tag_filter_tgt_mode('A+B')
            prx_item_tgt.set_tag_filter_tgt_key_add(
                i_path, ancestors=True
            )
            prx_item_tgt.set_tag_filter_tgt_statistic_enable(True)
            self._filter_content.set_element_add(
                i_key,
                prx_item_tgt
            )
            #
            self._set_registry_src_(i_path, dcc_obj, expand_depth)

    def _set_registry_src_(self, path, dcc_obj=None, expand_depth=1):
        path_dag_opt = bsc_core.DccPathDagOpt(path)
        ancestor_paths = path_dag_opt.get_ancestor_paths()
        if ancestor_paths:
            ancestor_paths.reverse()
            #
            for seq, i_ancestor_path in enumerate(ancestor_paths):
                if i_ancestor_path not in self._obj_add_dict:
                    i_is_create, i_ancestor_prx_item_src = self._set_prx_item_src_add_(i_ancestor_path)
                    if i_is_create is True:
                        if seq+1 <= expand_depth:
                            i_ancestor_prx_item_src.set_expanded(True)
        #
        is_create, prx_item_src = self._set_prx_item_src_add_(path)
        prx_item_src.set_tag_filter_src_key_add(path)
        if is_create is True:
            if self._dcc_namespace is not None:
                if dcc_obj is not None:
                    prx_item_src.set_gui_dcc_obj(
                        dcc_obj,
                        namespace=self._dcc_namespace
                    )
        return prx_item_src


class PrxDccObjKeywordFilterOpt(object):
    def __init__(self, prx_tree_view):
        pass


class PrxDccObjTreeViewAddOpt(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._dcc_namespace = dcc_namespace
        self._obj_add_dict = self._prx_tree_view._item_dict

    def set_restore(self):
        self._prx_tree_view.set_clear()

    def _set_dag_dcc_obj_gui_add_(self, obj):
        obj_path = obj.path
        if obj_path in self._obj_add_dict:
            return self._obj_add_dict[obj_path]
        else:
            kwargs = dict(
                name=(obj.name, obj.type),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._obj_add_dict[parent.path]
                prx_item = prx_item_parent.set_child_add(
                    **kwargs
                )
            else:
                prx_item = self._prx_tree_view.set_item_add(
                    **kwargs
                )
            #
            prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            prx_item.set_expanded(True)
            prx_item.set_checked(True)
            prx_item.set_icon_by_name_text(obj.type_name, 1)
            self._obj_add_dict[obj_path] = prx_item
            return prx_item

    def _set_prx_item_add_(self, obj, prx_item_parent, name_use_path_prettify):
        tool_tips = [
            'type: {}'.format(obj.type_name),
            'path: {}'.format(obj.path)
        ]
        tool_tip = '\n'.join(tool_tips)
        if name_use_path_prettify is True:
            kwargs = dict(
                name=obj.get_path_prettify_(),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=tool_tip,
                menu=obj.get_gui_menu_raw()
            )
        else:
            kwargs = dict(
                name=obj.name,
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=tool_tip,
                menu=obj.get_gui_menu_raw()
            )
        if prx_item_parent is not None:
            prx_item = prx_item_parent.set_child_add(
                **kwargs
            )
        else:
            prx_item = self._prx_tree_view.set_item_add(
                **kwargs
            )
        prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
        prx_item.set_expanded(True)
        prx_item.set_checked(True)
        self._obj_add_dict[obj.path] = prx_item
        return prx_item

    def _set_prx_item_add_2_(self, obj, prx_item_parent):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            return self._set_prx_item_add_(
                obj,
                prx_item_parent,
                name_use_path_prettify=False
            )

    def _set_prx_item_add_0_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._obj_add_dict[parent_key]
            else:
                prx_item_parent = None
            return self._set_prx_item_add_(obj, prx_item_parent, name_use_path_prettify=False)

    def _set_prx_item_add_1_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._obj_add_dict[parent_key]
            else:
                prx_item_parent = None
            return self._set_prx_item_add_(obj, prx_item_parent, name_use_path_prettify=True)

    def set_prx_item_add_as(self, obj, mode='tree'):
        if mode == 'tree':
            return self.set_prx_item_add_as_tree_mode(obj)
        elif mode == 'list':
            return self.set_prx_item_add_as_list_mode(obj)

    def set_prx_item_add_as_list_mode(self, obj):
        root = obj.get_root()
        self._set_prx_item_add_0_(root)
        parent = obj.get_parent()
        self._set_prx_item_add_1_(parent, root)
        #
        return self._set_prx_item_add_0_(obj, parent)

    def set_prx_item_add_as_tree_mode(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            #
            for ancestor in ancestors:
                ancestor_path = ancestor.path
                if ancestor_path not in self._obj_add_dict:
                    self._set_dag_dcc_obj_gui_add_(ancestor)
        #
        return self._set_dag_dcc_obj_gui_add_(obj)

    def get_checked_dcc_objs(self):
        list_ = []
        for k, v in self._prx_tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace=self._dcc_namespace)
            if i_texture is not None:
                if v.get_is_checked() is True:
                    list_.append(i_texture)
        return list_


class PrxStgObjTreeViewAddOpt(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        self._obj_add_dict = self._prx_tree_view._item_dict

        self._dcc_namespace = 'storage'

    def set_restore(self):
        self._prx_tree_view.set_clear()

    def _set_dag_dcc_obj_gui_add_(self, obj):
        obj_path = obj.path
        obj_key = obj.normcase_path
        if obj_path in self._obj_add_dict:
            return False, self._obj_add_dict[obj_path]
        else:
            kwargs = self._get_add_kwargs_(obj, False)
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._obj_add_dict[parent.path]
                prx_item = prx_item_parent.set_child_add(
                    **kwargs
                )
            else:
                prx_item = self._prx_tree_view.set_item_add(
                    **kwargs
                )
            #
            prx_item.set_checked(True)
            prx_item.set_icon_by_color(bsc_core.TextOpt(obj.type).to_rgb(), 1)
            self._obj_add_dict[obj_key] = prx_item
            return True, prx_item

    def _get_add_kwargs_(self, obj, name_use_path_prettify):
        obj_name = obj.name
        type_name = 'directory'
        if obj.get_is_file():
            type_name = 'file({})'.format(obj.ext)
        #
        if name_use_path_prettify is True:
            kwargs = dict(
                name='...',
                item_class=self._prx_tree_item_cls,
                # icon=obj.icon,
                icon_name_text=type_name,
            )
        else:
            kwargs = dict(
                name='...',
                item_class=self._prx_tree_item_cls,
                # icon=obj.icon,
                icon_name_text=type_name,
            )
        return kwargs

    def _get_item_prx_parent_(self, obj, parent):
        obj_key = obj.normcase_path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.normcase_path
                return self._obj_add_dict[parent_key]

    def _set_prx_item_add_(self, obj, parent=None, use_show_thread=False, name_use_path_prettify=False):
        obj_key = obj.normcase_path
        if obj_key in self._obj_add_dict:
            return False, self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.normcase_path
                prx_item_parent = self._obj_add_dict[parent_key]
            else:
                prx_item_parent = None
            #
            create_kwargs = dict(
                name='loading ...',
                item_class=self._prx_tree_item_cls,
                filter_key=obj.path
            )
            #
            if prx_item_parent is not None:
                prx_item = prx_item_parent.set_child_add(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.set_item_add(
                    **create_kwargs
                )
            #
            self._obj_add_dict[obj_key] = prx_item
            prx_item.set_checked(True)
            prx_item.set_keyword_filter_tgt_contexts([obj.path, obj.type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            if obj.get_is_file() is True:
                prx_item.set_gui_dcc_obj(obj, namespace='storage-file')
            else:
                prx_item.set_gui_dcc_obj(obj, namespace='storage-directory')
            #
            if use_show_thread is True:
                prx_item.set_show_method(
                    lambda *args, **kwargs: self._set_prx_item_show_deferred_(prx_item, name_use_path_prettify)
                )
                return True, prx_item
            else:
                self._set_prx_item_show_deferred_(prx_item, name_use_path_prettify)
                return True, prx_item

    def set_prx_item_add_as(self, obj, mode='tree', use_show_thread=False):
        if mode == 'tree':
            return self.set_prx_item_add_as_tree_mode(obj)
        elif mode == 'list':
            return self.set_prx_item_add_as_list_mode(obj, use_show_thread=use_show_thread)

    def set_prx_item_add_as_list_mode(self, obj, use_show_thread=False):
        obj_key = obj.normcase_path
        if obj_key in self._obj_add_dict:
            return False, self._obj_add_dict[obj_key]

        if obj.PATHSEP in obj.path:
            root = obj.get_root()
            self._set_prx_item_add_(
                obj=root,
                use_show_thread=use_show_thread
            )
            directory = obj.get_parent()
            self._set_prx_item_add_(
                obj=directory,
                parent=root,
                use_show_thread=use_show_thread,
                name_use_path_prettify=True
            )
            #
            return self._set_prx_item_add_(
                obj=obj,
                parent=directory,
                use_show_thread=use_show_thread
            )
        #
        return False, None

    def set_prx_item_add_as_tree_mode(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            #
            for i_ancestor in ancestors:
                ancestor_path = i_ancestor.path
                if ancestor_path not in self._obj_add_dict:
                    self._set_dag_dcc_obj_gui_add_(i_ancestor)
        #
        return self._set_dag_dcc_obj_gui_add_(obj)

    def _set_prx_item_show_deferred_(self, prx_item, name_use_path_prettify):
        obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)
        obj_name = obj.name
        obj_path = obj.path
        obj_type = obj.type
        #
        if name_use_path_prettify is True:
            name = obj.get_path_prettify_()
        else:
            name = obj_name
        #
        descriptions = [
            u'path="{}"'.format(obj_path)
        ]
        if obj.get_is_file():
            file_tiles = obj.get_exists_files_()
            if file_tiles:
                tool_tip_ = []
                if len(file_tiles) > 10:
                    _ = file_tiles[:8] + ['...'] + file_tiles[-1:]
                else:
                    _ = file_tiles
                #
                for i_file_tile in _:
                    if isinstance(i_file_tile, (str, unicode)):
                        tool_tip_.append(i_file_tile)
                    else:
                        readable = i_file_tile.get_is_readable()
                        writeable = i_file_tile.get_is_writeable()
                        tool_tip_.append(
                            u'path="{}"; readable={}; writeable={}'.format(
                                i_file_tile.path, readable, writeable
                            )
                        )
                #
                name = '{} ({})'.format(name, len(file_tiles))
                descriptions = [tool_tip_]
        #
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        prx_item.set_name(name)
        prx_item.set_icon_by_file(obj.icon_file)
        #
        menu_raw.extend(
            [
                ('expanded',),
                ('expand branch', None, prx_item.set_expand_branch),
                ('collapse branch', None, prx_item.set_collapse_branch),
                ('permission', ),
                ('unlock', None, None),
            ]
        )
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        if obj.get_is_root() is False:
            if obj.get_is_exists() is False:
                prx_item.set_state(prx_item.State.LOST)
            elif obj.get_is_writeable() is False:
                prx_item.set_state(prx_item.State.LOCKED)
            else:
                prx_item.set_state(prx_item.NORMAL_STATE)
                if obj.get_is_directory() is True:
                    prx_item.set_expanded(True)
        else:
            prx_item.set_expanded(True)

            # if obj.get_is_writeable() is False:
            #     prx_item.set_state(prx_item.State.LOCKED)

        prx_item.set_tool_tips(descriptions)
        #
        # self._prx_tree_view.set_loading_update()

    def get_files(self):
        list_ = []
        for k, v in self._prx_tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                list_.append(i_texture)
        return list_

    def get_checked_files(self):
        list_ = []
        for k, v in self._prx_tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                if v.get_is_checked() is True:
                    list_.append(i_texture)
        return list_
    @staticmethod
    def get_file(item):
        return item.gui_proxy.get_gui_dcc_obj(namespace='storage-file')


class PrxStgTextureTreeViewAddOpt(PrxStgObjTreeViewAddOpt):
    def __init__(self, *args, **kwargs):
        super(PrxStgTextureTreeViewAddOpt, self).__init__(*args, **kwargs)

        self._output_directory_path = None

    def set_output_directory(self, directory_path):
        self._output_directory_path = directory_path

    def _set_prx_item_show_deferred_(self, prx_item, name_use_path_prettify):
        obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)
        obj_name = obj.name
        obj_path = obj.path
        obj_type = obj.type
        #
        if name_use_path_prettify is True:
            name = obj.get_path_prettify_()
        else:
            name = obj_name
        #
        descriptions = [
            u'path="{}"'.format(obj_path)
        ]
        if obj.get_is_file():
            file_tiles = obj.get_exists_files_()
            if file_tiles:
                tool_tip_ = []
                if len(file_tiles) > 10:
                    _ = file_tiles[:8] + ['...'] + file_tiles[-1:]
                else:
                    _ = file_tiles
                #
                for i_file_tile in _:
                    if isinstance(i_file_tile, (str, unicode)):
                        tool_tip_.append(i_file_tile)
                    else:
                        st_mode = i_file_tile.get_permission()
                        tool_tip_.append(
                            u'path="{}"; st-mode="{}"'.format(
                                i_file_tile.path, st_mode
                            )
                        )
                #
                name = '{} ({})'.format(name, len(file_tiles))
                descriptions = [tool_tip_]
        #
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        prx_item.set_name(name)
        prx_item.set_icon_by_file(obj.icon_file)
        prx_item.set_tool_tips(descriptions)
        #
        menu_raw.extend(
            [
                ('expanded', ),
                ('Expand branch', None, prx_item.set_expand_branch),
                ('Collapse branch', None, prx_item.set_collapse_branch),
            ]
        )
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        if obj.get_is_exists() is False:
            prx_item.set_state(prx_item.DISABLE_STATE)
        else:
            prx_item.set_state(prx_item.NORMAL_STATE)
            if obj.get_is_directory() is True:
                prx_item.set_expanded(True)
            else:
                i_tx_exists = obj._get_is_exists_as_tgt_ext_(
                    obj.path, obj.TX_EXT, self._output_directory_path
                )
                if i_tx_exists is True:
                    prx_item.set_state(prx_item.State.NORMAL)
                else:
                    prx_item.set_state(prx_item.State.WARNING)
        #
        # self._prx_tree_view.set_loading_update()


class PrxDccObjTreeViewAddOpt1(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._dcc_namespace = dcc_namespace
        self._obj_add_dict = self._prx_tree_view._item_dict

    def set_restore(self):
        self._prx_tree_view.set_clear()

    def _set_dag_dcc_obj_gui_add_(self, obj):
        obj_path = obj.path
        if obj_path in self._obj_add_dict:
            return self._obj_add_dict[obj_path]
        else:
            kwargs = dict(
                name=(obj.name, obj.type.name),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._obj_add_dict[parent.path]
                prx_item = prx_item_parent.set_child_add(
                    **kwargs
                )
            else:
                prx_item = self._prx_tree_view.set_item_add(
                    **kwargs
                )
            #
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            prx_item.set_expanded(True)
            prx_item.set_checked(True)
            prx_item.set_icon_by_color(bsc_core.TextOpt(obj.type.name).to_rgb(), 1)
            self._obj_add_dict[obj_path] = prx_item
            return prx_item

    def _set_prx_item_show_deferred_(self, prx_item, name_use_path_prettify):
        obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)

        icon = obj.icon
        obj_type_name = obj.type_name
        obj_name = obj.name
        obj_path = obj.path

        menu_raw = obj.get_gui_menu_raw()

        prx_item.set_icon_by_file(icon)
        prx_item.set_icon_by_name_text(obj_type_name, 1)
        prx_item.set_name(obj_name)
        prx_item.set_tool_tip(obj_path)

        prx_item.set_gui_menu_raw(menu_raw)

    def _set_prx_item_add_(self, obj, prx_item_parent, name_use_path_prettify):
        if name_use_path_prettify is True:
            kwargs = dict(
                name=(obj.get_path_prettify_(), obj.type_path),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
        else:
            kwargs = dict(
                name=(obj.name, obj.type_path),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
        if prx_item_parent is not None:
            prx_item = prx_item_parent.set_child_add(
                **kwargs
            )
        else:
            prx_item = self._prx_tree_view.set_item_add(
                **kwargs
            )
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
        prx_item.set_expanded(True)
        prx_item.set_checked(True)

        self._obj_add_dict[obj.path] = prx_item
        # prx_item.set_show_method(
        #     functools.partial(
        #         self._set_prx_item_show_deferred_, prx_item, name_use_path_prettify
        #     )
        # )
        return prx_item

    def _set_prx_item_add_0_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._obj_add_dict[parent_key]
            else:
                prx_item_parent = None
            return self._set_prx_item_add_(
                obj,
                prx_item_parent,
                name_use_path_prettify=False
            )

    def _set_prx_item_add_1_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._obj_add_dict[parent_key]
            else:
                prx_item_parent = None
            return self._set_prx_item_add_(
                obj,
                prx_item_parent,
                name_use_path_prettify=True
            )

    def set_prx_item_add_as(self, obj, mode='tree'):
        if mode == 'tree':
            return self.set_prx_item_add_as_tree_mode(obj)
        elif mode == 'list':
            return self.set_prx_item_add_as_list_mode(obj)

    def set_prx_item_add_as_list_mode(self, obj):
        root = obj.get_root()
        self._set_prx_item_add_0_(root)
        parent = obj.get_parent()
        self._set_prx_item_add_1_(parent, root)
        #
        return self._set_prx_item_add_0_(obj, parent)

    def set_prx_item_add_as_tree_mode(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            #
            for ancestor in ancestors:
                ancestor_path = ancestor.path
                if ancestor_path not in self._obj_add_dict:
                    self._set_dag_dcc_obj_gui_add_(ancestor)
        #
        return self._set_dag_dcc_obj_gui_add_(obj)


class PrxUsdMeshTreeviewAddOpt(PrxDccObjTreeViewAddOpt1):
    def __init__(self, prx_tree_view, prx_tree_item_cls, tgt_obj_namespace, tgt_obj_pathsep, tgt_obj_class):
        super(PrxUsdMeshTreeviewAddOpt, self).__init__(prx_tree_view, prx_tree_item_cls, dcc_namespace='usd')
        self._tgt_obj_namespace = tgt_obj_namespace
        self._tgt_obj_pathsep = tgt_obj_pathsep
        self._tgt_obj_class = tgt_obj_class

    def set_prx_item_add_as_list_mode(self, obj):
        root = obj.get_root()
        self._set_prx_item_add_0_(root)
        transform = obj.get_parent()
        group = transform.get_parent()
        self._set_prx_item_add_1_(group, root)
        # self._set_prx_item_add_0_(transform, group)
        #
        return self._set_prx_item_add_0_(obj, group)

    def set_item_prx_update(self, src_mesh):
        src_transform = src_mesh.get_parent()
        src_group = src_transform.get_parent()
        self._set_tgt_update_(src_group)
        self._set_tgt_update_(src_transform)
        self._set_tgt_update_(src_mesh)

    def _set_tgt_update_(self, src_obj):
        src_path = src_obj.path
        prx_item = src_obj.get_obj_gui()
        if prx_item is not None:
            src_mesh_path_dag_opt = bsc_core.DccPathDagOpt(src_path)
            tgt_mesh_path_dag_opt = src_mesh_path_dag_opt.set_translate_to(self._tgt_obj_pathsep)
            tgt_mesh = self._tgt_obj_class(tgt_mesh_path_dag_opt.get_value())
            if tgt_mesh.get_is_exists() is True:
                prx_item.set_icon_by_file(tgt_mesh.icon)
                prx_item.set_gui_dcc_obj(tgt_mesh, namespace=self._tgt_obj_namespace)
            else:
                prx_item.set_temporary_state()


class PrxRsvObjTreeViewAddOpt(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._dcc_namespace = dcc_namespace
        self._obj_add_dict = self._prx_tree_view._item_dict

    def set_restore(self):
        self._prx_tree_view.set_clear()

    def _set_prx_item_add_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._obj_add_dict:
            prx_item = self._obj_add_dict[obj_path]
            return False, prx_item, None
        else:
            create_kwargs = dict(
                name='...',
                item_class=self._prx_tree_item_cls,
                filter_key=obj.path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._obj_add_dict[parent.path]
                prx_item = prx_item_parent.set_child_add(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.set_item_add(
                    **create_kwargs
                )
            #
            prx_item.set_checked(True)
            prx_item.set_keyword_filter_tgt_contexts([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            self._obj_add_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_method(
                    functools.partial(
                        self._set_prx_item_show_deferred_as_tree_mode_, prx_item
                    )
                )
                return True, prx_item, None
            else:
                self._set_prx_item_show_deferred_as_tree_mode_(prx_item)
                return True, prx_item, None

    def _set_prx_item_show_deferred_as_tree_mode_(self, prx_item):
        def expand_by_condition_fnc_(*args):
            _prx_item = args[0]
            type_name = _prx_item.get_name(1)
            return type_name
        #
        obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)
        obj_type_name = obj.type_name
        obj_name = obj.name
        obj_path = obj.path
        #
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        prx_item.set_icon_by_name_text(obj_type_name)
        prx_item.set_name(obj_name)
        prx_item.set_tool_tip(obj.description)
        #
        menu_raw.extend(
            [
                ('expanded', ),
                ('Expand branch', None, prx_item.set_expand_branch),
                ('Collapse branch', None, prx_item.set_collapse_branch),
                # (),
                # [
                #     'Expand branch to', None,
                #     [
                #         ('Role / Sequence', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['role', 'sequence'])),
                #         ('Asset / Shot', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['asset', 'shot'])),
                #         ('Step', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['step'])),
                #         ('Task', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['task']))
                #     ]
                # ]
            ]
        )
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def set_prx_item_add_as_tree_mode(self, obj):
        show_threads = []
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i in ancestors:
                i_path = i.path
                if i_path not in self._obj_add_dict:
                    i_is_create, i_item_prx, i_show_thread = self._set_prx_item_add_(i, use_show_thread=True)
                    if i_show_thread is not None:
                        show_threads.append(i_show_thread)
        #
        is_create, prx_item, thread = self._set_prx_item_add_(obj, use_show_thread=True)
        if thread is not None:
            show_threads.append(thread)
        return is_create, prx_item, show_threads

    def set_prx_item_add_as_list_mode(self, obj):
        pass


class PrxObjTreeViewAddOpt(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._dcc_namespace = dcc_namespace
        #
        self._obj_add_dict = self._prx_tree_view._item_dict

    def _set_item_add_(self, path_dag_opt, parent_path_dag_opt=None):
        if parent_path_dag_opt is not None:
            parent_item = self._obj_add_dict[parent_path_dag_opt.path]
            tree_item = parent_item.set_child_add(
                name=path_dag_opt.name,
                item_class=self._prx_tree_item_cls,
            )
        else:
            tree_item = self._prx_tree_view.set_item_add(
                name=path_dag_opt.name,
                item_class=self._prx_tree_item_cls,
            )
        #
        tree_item.set_checked(True)
        tree_item.set_gui_dcc_obj(path_dag_opt, namespace=self._dcc_namespace)
        #
        self._obj_add_dict[path_dag_opt.path] = tree_item

    def set_item_add(self, path):
        path_dag_opt = bsc_core.DccPathDagOpt(path)

        components = path_dag_opt.get_components()
        components.reverse()
        if components:
            parent_path_dag_opt = None
            for i_path_dag_opt in components:
                if i_path_dag_opt.path not in self._obj_add_dict:
                    self._set_item_add_(i_path_dag_opt, parent_path_dag_opt)
                #
                parent_path_dag_opt = i_path_dag_opt

    def get_checked_names(self):
        lis = []
        for k, v in self._obj_add_dict.items():
            if v.get_is_checked() is True:
                lis.append(
                    v.get_gui_dcc_obj(namespace=self._dcc_namespace).name
                )
        return lis
