# coding:utf-8
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
                item_prx = gui_item.gui_proxy
                dcc_obj = item_prx.get_gui_dcc_obj(namespace=dcc_namespace)
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
        for item_prx in self._prx_tree_view.get_all_items():
            if item_prx.get_is_checked() is True:
                obj = item_prx.get_gui_dcc_obj(namespace=self._dcc_namespace)
                if obj is not None:
                    lis.append((item_prx, obj))
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
            value=bsc_objects.Content.DEFAULT_VALUE
        )
        #
        self._dcc_obj_dict = {}
        self._dcc_selection_cls = None
        self._dcc_namespace = None
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
            value=bsc_objects.Content.DEFAULT_VALUE
        )
        self._dcc_obj_dict = {}

    def _to_filter_key_path_(self, key):
        return self._filter_content._to_key_path_(key)

    def set_tgt_item_tag_update(self, key, tgt_item_prx, dcc_obj=None):
        tag_filter_key = self._to_filter_key_path_(key)
        #
        tgt_item_prx.set_tag_filter_tgt_mode('A+B')
        tgt_item_prx.set_tag_filter_tgt_key_add(
            tag_filter_key, ancestors=True
        )
        tgt_item_prx.set_tag_filter_statistic_enable(True)
        self._filter_content.set_element_add(key, tgt_item_prx)
        #
        if dcc_obj is not None:
            self._dcc_obj_dict[tag_filter_key] = dcc_obj

    def set_src_item_add(self, filter_path):
        item_dict = self._prx_tree_view_src._item_dict
        #
        dag_path = bsc_core.DccPathDagOpt(filter_path)
        name = dag_path.name
        #
        key = dag_path.path
        if key in item_dict:
            return item_dict[key]
        #
        icon_color = bsc_core.TextOpt(dag_path.path).to_rgb()
        _kwargs = dict(
            name=(name, ),
            item_class=self._prx_tree_item_cls,
            tool_tip=dag_path.path,
            filter_key=key
        )
        #
        parent_path = bsc_core.DccPathDagOpt(filter_path).get_parent_path()
        if parent_path in item_dict:
            item_prx_parent = item_dict[parent_path]
            item_prx = item_prx_parent.set_child_add(
                **_kwargs
            )
        else:
            item_prx = self._prx_tree_view_src.set_item_add(
                **_kwargs
            )
        #
        if key == '/':
            item_prx.set_expanded(True)
        #
        item_prx.set_checked(True)
        item_prx.set_name_icon(key, 0)
        item_prx.set_emit_send_enable(True)
        return item_prx

    def set_src_items_refresh(self, expand_depth=None):
        self._prx_tree_view_src.set_clear()
        #
        leaf_paths = self._filter_content.get_leaf_key_as_paths()
        all_paths = self._filter_content.get_key_as_paths()
        all_paths.sort()
        all_paths = bsc_core.TextsOpt(all_paths).set_sort_to()
        for path in all_paths:
            src_item_prx = self.set_src_item_add(path)
            if path in leaf_paths:
                tag_filter_key = path
                src_item_prx.set_tag_filter_src_key_add(tag_filter_key)
            #
            if path in self._dcc_obj_dict:
                dcc_obj = self._dcc_obj_dict[path]
                if self._dcc_namespace is not None:
                    src_item_prx.set_gui_dcc_obj(dcc_obj, namespace=self._dcc_namespace)
        #
        if isinstance(expand_depth, int):
            self._prx_tree_view_src.set_items_expand_by_depth(expand_depth)
        else:
            self._prx_tree_view_src.set_all_items_expand()

    def set_src_items_update(self):
        leaf_paths = self._filter_content.get_leaf_key_as_paths()
        all_paths = self._filter_content.get_key_as_paths()
        all_paths.sort()
        all_paths = bsc_core.TextsOpt(all_paths).set_sort_to()
        for path in all_paths:
            src_item_prx = self.set_src_item_add(path)
            if path in leaf_paths:
                tag_filter_key = path
                src_item_prx.set_tag_filter_src_key_add(tag_filter_key)

    def set_filter_statistic(self):
        target_filter_tag_item_prx_dict = self._prx_tree_view_tgt.get_tag_filter_tgt_statistic_raw()
        for src_item_prx in self._prx_tree_view_src._item_dict.values():
            tag_filter_src_keys = src_item_prx.get_tag_filter_src_keys()
            if tag_filter_src_keys:
                for tag_filter_src_key in tag_filter_src_keys:
                    if tag_filter_src_key in target_filter_tag_item_prx_dict:
                        tgt_item_prxes = target_filter_tag_item_prx_dict[tag_filter_src_key]
                        if tgt_item_prxes:
                            states = self._prx_tree_view_tgt.get_item_states(tgt_item_prxes)
                            if src_item_prx.get_check_enable() is True:
                                if utl_gui_prx_core.State.ERROR in states:
                                    src_item_prx.set_error_state()
                                elif utl_gui_prx_core.State.WARNING in states:
                                    src_item_prx.set_warning_state()
                                # else:
                                #     src_item_prx.set_adopt_state()
                                #
                                src_item_prx.set_name(str(len(tgt_item_prxes)), self.COUNT_COLUMN)
                                #
                                brushes = self._prx_tree_view_tgt.get_item_foregrounds(tgt_item_prxes)
                                src_item_prx.set_foregrounds_raw(brushes)
                                #
                                src_item_prx.set_states_raw(states)
                            else:
                                src_item_prx.set_name('N/a', self.COUNT_COLUMN)
                                #
                                src_item_prx.set_foregrounds_raw([])
                                #
                                src_item_prx.set_states_raw([])
                            #
                            src_item_prx.set_hidden(boolean=False, ancestors=True)
                        else:
                            src_item_prx.set_hidden(boolean=True, ancestors=True)
                    else:
                        src_item_prx.set_hidden(boolean=True, ancestors=True)

    def set_filter(self):
        tag_filter_src_all_keys = []
        for src_item_prx in self._prx_tree_view_src._item_dict.values():
            tag_filter_src_keys = src_item_prx.get_tag_filter_src_keys()
            for tag_filter_src_key in tag_filter_src_keys:
                if src_item_prx.get_is_checked() is True:
                    if tag_filter_src_key not in tag_filter_src_all_keys:
                        tag_filter_src_all_keys.append(tag_filter_src_key)
        #
        self._prx_tree_view_tgt.set_source_filter_tags(tag_filter_src_all_keys)


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
                item_prx_parent = self._obj_add_dict[parent.path]
                item_prx = item_prx_parent.set_child_add(
                    **kwargs
                )
            else:
                item_prx = self._prx_tree_view.set_item_add(
                    **kwargs
                )
            #
            item_prx.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            item_prx.set_expanded(True)
            item_prx.set_checked(True)
            item_prx.set_name_icon(obj.type_name, 1)
            self._obj_add_dict[obj_path] = item_prx
            return item_prx

    def _set_item_prx_add_(self, obj, item_prx_parent, name_use_path_prettify):
        if name_use_path_prettify is True:
            kwargs = dict(
                name=(obj.get_path_prettify_(), obj.type),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
        else:
            kwargs = dict(
                name=(obj.name, obj.type),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
        if item_prx_parent is not None:
            item_prx = item_prx_parent.set_child_add(
                **kwargs
            )
        else:
            item_prx = self._prx_tree_view.set_item_add(
                **kwargs
            )
        item_prx.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
        item_prx.set_expanded(True)
        item_prx.set_checked(True)
        item_prx.set_name_icon(obj.type_name, 1)
        self._obj_add_dict[obj.path] = item_prx
        return item_prx

    def _set_item_prx_add_2_(self, obj, item_prx_parent):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            return self._set_item_prx_add_(obj, item_prx_parent, name_use_path_prettify=False)

    def _set_item_prx_add_0_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                item_prx_parent = self._obj_add_dict[parent_key]
            else:
                item_prx_parent = None
            return self._set_item_prx_add_(obj, item_prx_parent, name_use_path_prettify=False)

    def _set_item_prx_add_1_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                item_prx_parent = self._obj_add_dict[parent_key]
            else:
                item_prx_parent = None
            return self._set_item_prx_add_(obj, item_prx_parent, name_use_path_prettify=True)

    def set_item_prx_add_as(self, obj, mode='tree'):
        if mode == 'tree':
            return self.set_item_prx_add_as_tree_mode(obj)
        elif mode == 'list':
            return self.set_item_prx_add_as_list_mode(obj)

    def set_item_prx_add_as_list_mode(self, obj):
        root = obj.get_root()
        self._set_item_prx_add_0_(root)
        parent = obj.get_parent()
        self._set_item_prx_add_1_(parent, root)
        #
        return self._set_item_prx_add_0_(obj, parent)

    def set_item_prx_add_as_tree_mode(self, obj):
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


class PrxStgObjTreeViewAddOpt(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        self._obj_add_dict = self._prx_tree_view._item_dict

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
                item_prx_parent = self._obj_add_dict[parent.path]
                item_prx = item_prx_parent.set_child_add(
                    **kwargs
                )
            else:
                item_prx = self._prx_tree_view.set_item_add(
                    **kwargs
                )
            #
            item_prx.set_checked(True)
            item_prx.set_color_icon(bsc_core.TextOpt(obj.type).to_rgb(), 1)
            self._obj_add_dict[obj_key] = item_prx
            return True, item_prx

    def _get_add_kwargs_(self, obj, name_use_path_prettify):
        tool_tip = [
            u'path="{}"'.format(obj.path)
        ]
        type_name = 'directory'
        if obj.get_is_file():
            type_name = 'file[{}]'.format(obj.ext)
            file_tiles = obj.get_exists_files()
            if file_tiles:
                tool_tip_ = []
                if len(file_tiles) > 50:
                    _ = file_tiles[:48] + file_tiles[-1:]
                else:
                    _ = file_tiles
                #
                for file_tile in _:
                    st_mode = file_tile.get_permission()
                    tool_tip_.append(
                        u'path="{}"; st-mode="{}"'.format(
                            file_tile.path, st_mode
                        )
                    )
                tool_tip = [tool_tip_]
        #
        if name_use_path_prettify is True:
            kwargs = dict(
                name=(obj.get_path_prettify_(), type_name),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=tool_tip,
                menu=obj.get_gui_menu_raw()
            )
        else:
            kwargs = dict(
                name=(obj.name, type_name),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=tool_tip,
                menu=obj.get_gui_menu_raw()
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

    def _set_item_prx_add_(self, obj, parent=None, name_use_path_prettify=False):
        obj_key = obj.normcase_path
        if obj_key in self._obj_add_dict:
            return False, self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.normcase_path
                item_prx_parent = self._obj_add_dict[parent_key]
            else:
                item_prx_parent = None
            #
            kwargs = self._get_add_kwargs_(obj, name_use_path_prettify)
            if item_prx_parent is not None:
                item_prx = item_prx_parent.set_child_add(
                    **kwargs
                )
            else:
                item_prx = self._prx_tree_view.set_item_add(
                    **kwargs
                )
            #
            item_prx.set_checked(True)
            item_prx.set_name_icon(obj.type_name, 1)
            self._obj_add_dict[obj_key] = item_prx
            #
            if obj.get_is_exists() is False:
                item_prx.set_state(item_prx.DISABLE_STATE)
            else:
                item_prx.set_state(item_prx.NORMAL_STATE)
                if obj.get_is_directory() is True:
                    item_prx.set_expanded(True)
            #
            item_prx.set_gui_dcc_obj(obj, namespace='storage')
            if obj.get_is_file() is True:
                item_prx.set_gui_dcc_obj(obj, namespace='storage-file')
            else:
                item_prx.set_gui_dcc_obj(obj, namespace='storage-directory')
            return True, item_prx

    def set_item_prx_add_as(self, obj, mode='tree'):
        if mode == 'tree':
            return self.set_item_prx_add_as_tree_mode(obj)
        elif mode == 'list':
            return self.set_item_prx_add_as_list_mode(obj)

    def set_item_prx_add_as_list_mode(self, obj):
        root = obj.get_root()
        self._set_item_prx_add_(obj=root)
        parent = obj.get_parent()
        self._set_item_prx_add_(obj=parent, parent=root, name_use_path_prettify=True)
        #
        return self._set_item_prx_add_(obj=obj, parent=parent)

    def set_item_prx_add_as_tree_mode(self, obj):
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


class PrxStgTextureTreeViewAddOpt(PrxStgObjTreeViewAddOpt):
    def __init__(self, *args, **kwargs):
        super(PrxStgTextureTreeViewAddOpt, self).__init__(*args, **kwargs)


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
                item_prx_parent = self._obj_add_dict[parent.path]
                item_prx = item_prx_parent.set_child_add(
                    **kwargs
                )
            else:
                item_prx = self._prx_tree_view.set_item_add(
                    **kwargs
                )
            #
            obj.set_obj_gui(item_prx)
            item_prx.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            item_prx.set_expanded(True)
            item_prx.set_checked(True)
            item_prx.set_color_icon(bsc_core.TextOpt(obj.type.name).to_rgb(), 1)
            self._obj_add_dict[obj_path] = item_prx
            return item_prx

    def _set_item_prx_add_(self, obj, item_prx_parent, name_use_path_prettify):
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
        if item_prx_parent is not None:
            item_prx = item_prx_parent.set_child_add(
                **kwargs
            )
        else:
            item_prx = self._prx_tree_view.set_item_add(
                **kwargs
            )
        obj.set_obj_gui(item_prx)
        item_prx.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
        item_prx.set_expanded(True)
        item_prx.set_checked(True)
        item_prx.set_name_icon(obj.type_name, 1)
        self._obj_add_dict[obj.path] = item_prx
        return item_prx

    def _set_item_prx_add_0_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                item_prx_parent = self._obj_add_dict[parent_key]
            else:
                item_prx_parent = None
            return self._set_item_prx_add_(obj, item_prx_parent, name_use_path_prettify=False)

    def _set_item_prx_add_1_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._obj_add_dict:
            return self._obj_add_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                item_prx_parent = self._obj_add_dict[parent_key]
            else:
                item_prx_parent = None
            return self._set_item_prx_add_(obj, item_prx_parent, name_use_path_prettify=True)

    def set_item_prx_add_as(self, obj, mode='tree'):
        if mode == 'tree':
            return self.set_item_prx_add_as_tree_mode(obj)
        elif mode == 'list':
            return self.set_item_prx_add_as_list_mode(obj)

    def set_item_prx_add_as_list_mode(self, obj):
        root = obj.get_root()
        self._set_item_prx_add_0_(root)
        parent = obj.get_parent()
        self._set_item_prx_add_1_(parent, root)
        #
        return self._set_item_prx_add_0_(obj, parent)

    def set_item_prx_add_as_tree_mode(self, obj):
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

    def set_item_prx_add_as_list_mode(self, obj):
        root = obj.get_root()
        self._set_item_prx_add_0_(root)
        transform = obj.get_parent()
        group = transform.get_parent()
        self._set_item_prx_add_1_(group, root)
        self._set_item_prx_add_0_(transform, group)
        #
        return self._set_item_prx_add_0_(obj, transform)

    def set_item_prx_update(self, src_mesh):
        src_transform = src_mesh.get_parent()
        src_group = src_transform.get_parent()
        self._set_tgt_update_(src_group)
        self._set_tgt_update_(src_transform)
        self._set_tgt_update_(src_mesh)

    def _set_tgt_update_(self, src_obj):
        src_path = src_obj.path
        item_prx = src_obj.get_obj_gui()
        if item_prx is not None:
            src_mesh_path_dag_opt = bsc_core.DccPathDagOpt(src_path)
            tgt_mesh_path_dag_opt = src_mesh_path_dag_opt.set_translate_to(self._tgt_obj_pathsep)
            tgt_mesh = self._tgt_obj_class(tgt_mesh_path_dag_opt.get_value())
            if tgt_mesh.get_is_exists() is True:
                item_prx.set_file_icon(tgt_mesh.icon)
                item_prx.set_gui_dcc_obj(tgt_mesh, namespace=self._tgt_obj_namespace)
            else:
                item_prx.set_temporary_state()


class PrxRsvObjTreeViewAddOpt(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._dcc_namespace = dcc_namespace
        self._obj_add_dict = self._prx_tree_view._item_dict

    def set_restore(self):
        self._prx_tree_view.set_clear()

    def _set_item_prx_add_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._obj_add_dict:
            item_prx = self._obj_add_dict[obj_path]
            return False, item_prx, None
        else:
            create_kwargs = dict(
                name='loading ...',
                name_icon=obj_type,
                item_class=self._prx_tree_item_cls,
                filter_key=obj.path
            )
            parent = obj.get_parent()
            if parent is not None:
                item_prx_parent = self._obj_add_dict[parent.path]
                item_prx = item_prx_parent.set_child_add(
                    **create_kwargs
                )
            else:
                item_prx = self._prx_tree_view.set_item_add(
                    **create_kwargs
                )
            #
            item_prx.set_keyword_filter_contexts([obj_path, obj_type])
            obj.set_obj_gui(item_prx)
            item_prx.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            self._obj_add_dict[obj_path] = item_prx
            #
            if use_show_thread is True:
                item_prx.set_show_method(
                    lambda *args, **kwargs: self._set_item_prx_show_(item_prx)
                )
                return True, item_prx, None
            else:
                self._set_item_prx_show_(item_prx)
                return True, item_prx, None

    def _set_item_prx_show_(self, item_prx):
        def expand_by_condition_fnc_(*args):
            _prx_item = args[0]
            type_name = _prx_item.get_name(1)
            return type_name
        #
        obj = item_prx.get_gui_dcc_obj(namespace=self._dcc_namespace)
        obj_name = obj.name
        obj_path = obj.path
        obj_type = obj.type
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        item_prx.set_name(obj_name)
        item_prx.set_tool_tips((obj_path,))
        #
        item_prx.set_checked(True)
        #
        menu_raw.extend(
            [
                ('expanded', ),
                ('Expand branch', None, item_prx.set_expand_branch),
                ('Collapse branch', None, item_prx.set_collapse_branch),
                # (),
                # [
                #     'Expand branch to', None,
                #     [
                #         ('Role / Sequence', None, lambda: item_prx.set_expand_branch_by_condition(expand_by_condition_fnc_, ['role', 'sequence'])),
                #         ('Asset / Shot', None, lambda: item_prx.set_expand_branch_by_condition(expand_by_condition_fnc_, ['asset', 'shot'])),
                #         ('Step', None, lambda: item_prx.set_expand_branch_by_condition(expand_by_condition_fnc_, ['step'])),
                #         ('Task', None, lambda: item_prx.set_expand_branch_by_condition(expand_by_condition_fnc_, ['task']))
                #     ]
                # ]
            ]
        )
        item_prx.set_gui_menu_raw(menu_raw)
        item_prx.set_menu_content(obj.get_gui_menu_content())
        #
        self._prx_tree_view.set_loading_update()

    def set_item_prx_add_as_tree_mode(self, obj):
        show_threads = []
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i in ancestors:
                ancestor_path = i.path
                if ancestor_path not in self._obj_add_dict:
                    i_is_create, i_item_prx, i_show_thread = self._set_item_prx_add_(i, use_show_thread=True)
                    if i_show_thread is not None:
                        show_threads.append(i_show_thread)
        #
        is_create, item_prx, thread = self._set_item_prx_add_(obj, use_show_thread=True)
        if thread is not None:
            show_threads.append(thread)
        return is_create, item_prx, show_threads
