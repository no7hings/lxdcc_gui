# coding:utf-8
import functools


class GuiRsvObjOpt(object):
    DCC_NAMESPACE = 'resolver'
    def __init__(self, prx_tree_view, prx_tree_item_cls):
        self._tree_view = prx_tree_view
        self._tree_item_cls = prx_tree_item_cls
        #
        self._item_dict = self._tree_view._item_dict
        self._keys = set()

    def gui_get_is_exists(self, path):
        return path in self._item_dict

    def gui_get(self, path):
        return self._item_dict[path]

    def set_restore(self):
        self._tree_view.set_clear()
        self._keys.clear()

    def gui_add(self, obj, use_show_thread=False):
        obj_name = obj.name
        obj_path = obj.path
        obj_type = obj.type
        if self.gui_get_is_exists(obj_path) is True:
            prx_item = self.gui_get(obj_path)
            return False, prx_item
        else:
            create_kwargs = dict(
                name=obj_name,
                item_class=self._tree_item_cls,
                filter_key=obj.path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.set_child_add(
                    **create_kwargs
                )
            else:
                prx_item = self._tree_view.set_item_add(
                    **create_kwargs
                )
            #
            prx_item.set_type(obj.get_type_name())
            prx_item.set_checked(False)
            prx_item.update_keyword_filter_keys_tgt(
                [obj_path, obj_type]
            )
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.DCC_NAMESPACE)
            self._item_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_method(
                    functools.partial(
                        self.gui_show_deferred_fnc, prx_item
                    )
                )
                return True, prx_item
            else:
                self.gui_show_deferred_fnc(prx_item)
                return True, prx_item

    def gui_show_deferred_fnc(self, prx_item):
        def expand_by_condition_fnc_(*args):
            _prx_item = args[0]
            type_name = _prx_item.get_name(1)
            return type_name
        #
        obj = prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
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
        prx_item.set_icon_by_file(obj.icon)
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

    def gui_add_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i in ancestors:
                i_path = i.path
                if self.gui_get_is_exists(i_path) is False:
                    self.gui_add(i, use_show_thread=True)
        #
        is_create, prx_item = self.gui_add(obj, use_show_thread=True)
        return is_create, prx_item

    def gui_add_as_list(self, obj):
        pass
