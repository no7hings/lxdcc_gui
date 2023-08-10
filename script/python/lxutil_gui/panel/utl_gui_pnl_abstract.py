# coding:utf-8
import collections

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core


class AbsObjGuiDef(object):
    UTL_OBJ_CLS = None
    @classmethod
    def _set_prd_obj_gui_add_(cls, obj, tree_view_gui):
        item_dict = tree_view_gui._item_dict
        parent_obj_path = obj.get_parent_path()
        obj_path = obj.path
        port = obj.get_variant_port('icon')
        if port:
            icon_name = port.get()
            obj_icon = utl_core.Icon.get(icon_name)
        else:
            obj_icon = utl_core.Icon.get('tag')
        #
        if obj_path in item_dict:
            return item_dict[obj_path]
        #
        tool_tip = 'path: {}'.format(obj_path)
        #
        _kwargs = dict(
            name=(obj.name, obj.type.name),
            icon=obj_icon,
            tool_tip=tool_tip,
            item_class=prx_widgets.PrxObjTreeItem,
        )
        if parent_obj_path is None:
            obj_gui = tree_view_gui.create_item(
                **_kwargs
            )
            item_dict[obj_path] = obj_gui
            return obj_gui
        else:
            if parent_obj_path in item_dict:
                parent_gui = item_dict[parent_obj_path]
                obj_gui = parent_gui.add_child(
                    **_kwargs
                )
                item_dict[obj_path] = obj_gui
                return obj_gui
    @classmethod
    def gui_add(cls, dcc_obj, parent_obj_gui):
        dcc_obj_gui = parent_obj_gui.add_child(
            dcc_obj.name, dcc_obj.type,
            item_class=prx_widgets.PrxDccObjTreeItem,
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path
        )
        dcc_obj_gui.set_gui_attribute('dcc_obj', dcc_obj)
        return dcc_obj_gui

    def get_obj_gui(self, obj_path):
        pass
    @classmethod
    def _set_utl_obj_gui_add_(cls, obj_path, tree_view_gui, icon_name=None):
        item_dict = tree_view_gui._item_dict
        #
        utl_obj = cls.UTL_OBJ_CLS(obj_path)
        if utl_obj.path in item_dict:
            return item_dict[utl_obj.path]
        #
        if icon_name is not None:
            icon = utl_core.Icon.get(icon_name)
        else:
            icon = utl_obj.icon

        _kwargs = dict(
            name=(utl_obj.name, utl_obj.type),
            icon=icon,
            tool_tip='path: {}'.format(utl_obj.path),
            item_class=prx_widgets.PrxObjTreeItem,
        )
        parent_path = utl_obj.get_parent_path()
        if parent_path in item_dict:
            parent_gui = item_dict[parent_path]
            obj_gui = parent_gui.add_child(
                **_kwargs
            )
            item_dict[utl_obj.path] = obj_gui
            return obj_gui
        else:
            obj_gui = tree_view_gui.create_item(
                **_kwargs
            )
            item_dict[utl_obj.path] = obj_gui
            return obj_gui


class AbsGuiMethodDef(object):
    def _set_gui_method_def_init_(self):
        self._method_dict = collections.OrderedDict()
        self._method_gui_dict = collections.OrderedDict()

    def set_method(self, method_key, method):
        self._method_dict[method_key] = method

    def get_method(self, method_key):
        return self._method_dict[method_key]

    def set_method_gui(self, method_key, method_gui):
        self._method_gui_dict[method_key] = method_gui

    def get_method_gui(self, method_key):
        return self._method_gui_dict[method_key]


class AbsUtilToolPanel(prx_widgets.PrxBaseWindow):
    TOOL_PANEL_KEY = None
    TOOL_SCHEME = None
    DCC_SELECTION_CLS = None
    def __init__(self, *args, **kwargs):
        super(AbsUtilToolPanel, self).__init__(*args, **kwargs)
        self.set_window_title(
            self.TOOL_SCHEME.get('tool.{}.label'.format(self.TOOL_PANEL_KEY))
        )
        self.set_definition_window_size(
            self.TOOL_SCHEME.get('tool.{}.size'.format(self.TOOL_PANEL_KEY))
        )


class AbsSceneComposeToolPanel(
    prx_widgets.PrxBaseWindow,
):
    DCC_SELECTION_CLS = None
    DCC_NODE_CLS = None
    #
    OBJ_OP_CLS = None
    OP_REFERENCE_OBJ_CLS = None
    #
    GUI_DSC_INDEX = 5
    def __init__(self, scene, *args, **kwargs):
        super(AbsSceneComposeToolPanel, self).__init__(*args, **kwargs)
        self._scene = scene
        self.set_definition_window_size((960, 720))
        current_obj = self._scene.get_current_obj()
        if current_obj is not None:
            self.set_window_title(current_obj.__str__())
        else:
            self.set_window_title('Scene-compose')
        #
        self.set_panel_build()
        self.set_refresh()

    def set_panel_build(self):
        # viewer
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        self._tree_viewer = prx_widgets.PrxTreeView()
        expand_box_0.add_widget(self._tree_viewer)
        self._tree_viewer.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 2), ('Instance(s)', 2), ('Version(s)', 2), ('Data(s)', 2), ('Description(s)', 4)],
            self.get_definition_window_size()[0] - 16
        )
        self._tree_viewer.connect_item_select_changed_to(self._set_dcc_obj_select_)
        self._tree_viewer.set_gui_menu_raw(
            [
                [
                    'Main', None,
                    [
                        ('Log', None, self.set_log_unit_show),
                        ('Help', None, self.show_help)
                    ]
                ],
                (),
                ('Expand All', None, self._tree_viewer.set_all_items_expand),
                ('Collapse All', None, self._tree_viewer.set_all_items_collapse),
                (),
                ('Select all', None, None),
                ('Select clear', None, None)
            ]
        )

        self._refresh_button_0 = qt_widgets.QtPressButton()
        self._refresh_button_0.setText('Refresh')
        self.add_button(self._refresh_button_0)
        self._refresh_button_0.clicked.connect(self.set_refresh)

        self._repair_button = qt_widgets.QtPressButton()
        self._repair_button.setText('Repair')
        self.add_button(self._repair_button)
        self._repair_button.clicked.connect(self.set_repair_run)

    def _set_dcc_obj_select_(self):
        if self.DCC_SELECTION_CLS is not None:
            paths = []
            qt_tree_items = self._tree_viewer._get_selected_items_()
            for qt_tree_item in qt_tree_items:
                gui_proxy = qt_tree_item.gui_proxy
                if isinstance(gui_proxy, prx_widgets.PrxObjTreeItem):
                    dcc_obj = gui_proxy.get_gui_attribute('dcc_obj')
                    if dcc_obj is not None:
                        paths.append(dcc_obj.path)
            if paths:
                self.DCC_SELECTION_CLS(paths).select_all()
            else:
                self.DCC_SELECTION_CLS.set_clear()

    def _set_dcc_groups_add_(self, obj_opt, prod_obj_gui):
        dcc_group_paths = obj_opt.get_dcc_group_paths()
        dcc_objs = [self.DCC_NODE_CLS(i) for i in dcc_group_paths]
        for dcc_obj in dcc_objs:
            obj_gui = prod_obj_gui.add_child(
                name=(dcc_obj.name, dcc_obj.type),
                item_class=prx_widgets.PrxDccObjTreeItem,
                icon=dcc_obj.icon,
                tool_tip=dcc_obj.path
            )
            obj_gui.set_gui_attribute('dcc_obj', dcc_obj)
            if dcc_obj.get_is_exists() is False:
                obj_gui.set_error_state()
                obj_gui.set_name('"Dcc-path" is Non-exists', self.GUI_DSC_INDEX)

    def _set_dcc_path_check_(self, obj_opt, obj_gui):
        dcc_name = obj_opt.dcc_name
        if dcc_name:
            dcc_obj = self.DCC_NODE_CLS(dcc_name)
            if dcc_obj.get_is_exists() is True:
                obj_gui.set_gui_attribute('dcc_obj', dcc_obj)
                obj_gui.set_icon_by_file(dcc_obj.icon)
                exists_path = dcc_obj.path
                if not exists_path == obj_opt.dcc_path:
                    obj_gui.set_warning_state()
                    obj_gui.set_name('"Dcc-object" is Non-collection', self.GUI_DSC_INDEX)
            else:
                obj_gui.set_error_state()
                obj_gui.set_name('"Dcc-object" is Non-exists', self.GUI_DSC_INDEX)
        # if not obj_opt.reference_key:
        #     self._set_dcc_groups_add_(obj_opt, obj_gui)

    def set_refresh(self):
        def _set_gui_add(obj_, obj_op_):
            _parent = obj_.get_parent()
            _path = obj_.path
            if _path in self._gui_dict:
                return self._gui_dict[_path]

            _kwargs = dict(
                name=(obj_op_.name, obj_op_.type, obj_op_.reference_key, obj_op_.version, obj_op_.label),
                icon=obj_opt.icon,
                tool_tip='path: {}\nplt-path: {}\ndcc-path: {}'.format(obj_op_.path, obj_op_.plf_path, obj_op_.dcc_path),
                item_class=prx_widgets.PrxObjTreeItem,
            )
            if _parent is None:
                _obj_gui = self._tree_viewer.create_item(
                    **_kwargs
                )
                self._gui_dict[obj_op_.path] = _obj_gui
                return _obj_gui
            else:
                _parent_path = _parent.path
                if _parent_path in self._gui_dict:
                    parent_gui = self._gui_dict[_parent_path]
                    _obj_gui = parent_gui.add_child(
                        **_kwargs
                    )
                    self._gui_dict[obj_op_.path] = _obj_gui
                    return _obj_gui

        self._tree_viewer.set_clear()
        self._gui_dict = collections.OrderedDict()

        step_objs = self._scene.get_step_objs()
        for step_obj in step_objs:
            obj_paths = step_obj.get_dag_component_paths()
            obj_paths.reverse()
            for obj_path in obj_paths:
                obj = self._scene.universe.get_obj(obj_path)
                if obj is not None:
                    obj_opt = self.OBJ_OP_CLS(obj)
                    reference_key = obj_opt.reference_key
                    if reference_key:
                        obj_opt = self.OP_REFERENCE_OBJ_CLS(obj)
                    #
                    obj_gui = _set_gui_add(obj, obj_opt)
                    if obj_gui is not None:
                        self._set_dcc_path_check_(obj_opt, obj_gui)

        self._tree_viewer.set_all_items_expand()

    def set_repair_run(self):
        objs = self._scene.get_objs()
        for obj in objs:
            obj_opt = self.OBJ_OP_CLS(obj)
            if not obj_opt.reference_key:
                dcc_path = obj_opt.dcc_path
                dcc_obj = self.DCC_NODE_CLS(dcc_path)
                dcc_obj.set_ancestors_create()

        for obj in objs:
            obj_opt = self.OBJ_OP_CLS(obj)
            if obj_opt.reference_key == 'reference':
                dcc_name = obj_opt.dcc_name
                exists_dcc_obj = self.DCC_NODE_CLS(dcc_name)
                if exists_dcc_obj.get_is_exists() is True:
                    exists_path = exists_dcc_obj.path
                    dcc_path = obj_opt.dcc_path
                    if not exists_path == dcc_path:
                        parent_path = self.DCC_NODE_CLS(dcc_path).get_parent_path()
                        exists_dcc_obj.parent_to_path(parent_path)

        self.set_refresh()


class AbsDccObjGuiDef(object):
    @classmethod
    def gui_add(cls, obj, obj_gui_parent=None, tree_viewer=None):
        kwargs = dict(
            name=(obj.name, obj.type.name),
            item_class=prx_widgets.PrxObjTreeItem,
            icon=obj.icon,
            tool_tip=obj.path
        )
        if obj_gui_parent is not None:
            obj_gui = obj_gui_parent.add_child(
                **kwargs
            )
        elif tree_viewer is not None:
            obj_gui = tree_viewer.create_item(
                **kwargs
            )
        else:
            raise TypeError()
        #
        obj.set_obj_gui(obj_gui)
        return obj_gui
    @classmethod
    def _set_obj_connect_to_dcc_(cls, obj, obj_gui, is_shape):
        raise NotImplementedError()
