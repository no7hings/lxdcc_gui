# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import hou

from lxutil import utl_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.panel import utl_gui_pnl_abstract

from lxhoudini import hou_core

import lxhoudini.dcc.dcc_objects as hou_dcc_objects


class SceneOverviewToolPanel(utl_gui_pnl_abstract.AbsUtilToolPanel):
    TOOL_PANEL_KEY = 'scene_overview'
    TOOL_SCHEME = utl_core.Scheme.HOUDINI_TOOL_TD
    DCC_SELECTION_CLS = hou_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(SceneOverviewToolPanel, self).__init__(*args, **kwargs)
        self.set_panel_build()

    def set_panel_build(self):
        self.set_show_menu_raw(
            [
                ('Log', None, self.set_log_unit_show),
                ('Help', None, self.set_help_unit_show)
            ]
        )
        # viewer
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        self._tree_viewer = prx_widgets.PrxTreeView()
        expand_box_0.set_widget_add(self._tree_viewer)
        self._tree_viewer.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 1)],
            self.get_definition_window_size()[0] - 16
        )
        self._tree_viewer.connect_item_select_changed_to(self.set_select)
        # log
        expand_box_1 = prx_widgets.PrxExpandedGroup()
        expand_box_1.set_name('Log')
        self.set_widget_add(expand_box_1)
        self._text_browser = qt_widgets.QtTextBrowser_()
        expand_box_1.set_widget_add(self._text_browser)

        self._refresh_button_0 = qt_widgets.QtPressButton()
        self._refresh_button_0.setText('Refresh')
        self.set_button_add(self._refresh_button_0)
        self._refresh_button_0.clicked.connect(self.set_run)

    def set_select(self):
        if self.DCC_SELECTION_CLS is not None:
            paths = []
            treeItems = self._tree_viewer._get_selected_items_()
            for treeItem in treeItems:
                gui_proxy = treeItem.gui_proxy
                if isinstance(gui_proxy, prx_widgets.PrxDccObjTreeItem):
                    dcc_obj = gui_proxy.get_gui_attribute('dcc_obj')
                    if dcc_obj is not None:
                        paths.append(dcc_obj.path)
            if paths:
                self.DCC_SELECTION_CLS(paths).select_all()
            else:
                self.DCC_SELECTION_CLS.set_clear()

    def set_node_tree_item_add(self, path, parent_tree_item=None, node_class=None, is_dcc_node=False):
        if node_class is not None:
            dcc_obj = node_class(path)
        else:
            dcc_obj = hou_dcc_objects.Node(path)
        if parent_tree_item is None:
            tree_item = self._tree_viewer.set_item_add(
                dcc_obj.name, dcc_obj.type,
                item_class=prx_widgets.PrxDccObjTreeItem,
                tool_tip=dcc_obj.path
            )
        else:
            tree_item = parent_tree_item.set_child_add(
                dcc_obj.name, dcc_obj.type,
                item_class=prx_widgets.PrxDccObjTreeItem,
                tool_tip=dcc_obj.path
            )
        tree_item.set_icon_by_file(dcc_obj.icon)
        if is_dcc_node is True:
            tree_item.set_gui_attribute('dcc_obj', dcc_obj)
        return dcc_obj, tree_item

    def set_type_tree_item_add(self, name, icon=None, parent_tree_item=None):
        if parent_tree_item is None:
            tree_item = self._tree_viewer.set_item_add(
                name,
                item_class=prx_widgets.PrxDccObjTreeItem,
            )
        else:
            tree_item = parent_tree_item.set_child_add(
                name,
                item_class=prx_widgets.PrxDccObjTreeItem,
            )
        if icon is not None:
            tree_item.set_icon_by_file(icon)
        return tree_item

    def set_run(self):
        self._gui_obj_dict = {}
        self._tree_viewer.set_clear()
        self.set_geometry_type_setup()
        self.set_instance_type_setup()

    def set_geometry_type_setup(self):
        geometry_type_tree_item = self.set_type_tree_item_add(
            'geometry(s)', utl_core.FileIcon.get_folder()
        )
        geo_hou_objs = hou_core.HouObj.get_displayed_geos()
        for geo_hou_obj in geo_hou_objs:
            hou_geos_fnc = hou_core.HouGeos(geo_hou_obj)
            geo_dcc_obj, geo_gui_obj = self.set_node_tree_item_add(
                geo_hou_obj.path(),
                parent_tree_item=geometry_type_tree_item,
                is_dcc_node=True
            )
            #
            render_type_gui_obj = self.set_type_tree_item_add(
                'render-node(s)', utl_core.FileIcon.get_folder(),
                parent_tree_item=geo_gui_obj
            )
            render_hou_objs = hou_geos_fnc.get_render_nodes()
            for render_hou_obj in render_hou_objs:
                render_dcc_obj, render_gui_obj = self.set_node_tree_item_add(
                    render_hou_obj.path(),
                    parent_tree_item=render_type_gui_obj,
                    is_dcc_node=True
                )
            #
            operator_type_gui_obj = self.set_type_tree_item_add(
                'operator(s)', utl_core.FileIcon.get_folder(),
                parent_tree_item=geo_gui_obj
            )
            operator_hou_objs = hou_geos_fnc.get_operators()
            for operator_hou_obj in operator_hou_objs:
                operator_dcc_obj, operator_gui_obj = self.set_node_tree_item_add(
                    operator_hou_obj.path(),
                    parent_tree_item=operator_type_gui_obj,
                    is_dcc_node=True
                )

    def set_instance_type_setup(self):
        geometry_type_tree_item = self.set_type_tree_item_add(
            'instance(s)', utl_core.FileIcon.get_folder()
        )
        instance_hou_objs = hou_core.HouObj.get_displayed_instances()
        for instance_hou_obj in instance_hou_objs:
            hou_instances_fnc = hou_core.HouInstances(instance_hou_obj)
            geo_hou_objs = hou_instances_fnc.get_geos()
            for geo_hou_obj in geo_hou_objs:
                geo_hou_obj_path = geo_hou_obj.path()
                if geo_hou_obj_path not in self._gui_obj_dict:
                    geo_dcc_obj, geo_gui_obj = self.set_node_tree_item_add(
                        geo_hou_obj.path(),
                        parent_tree_item=geometry_type_tree_item,
                        is_dcc_node=True
                    )
                    self._gui_obj_dict[geo_hou_obj_path] = geo_gui_obj
                else:
                    geo_gui_obj = self._gui_obj_dict[geo_hou_obj_path]

                instance_dcc_obj, instance_gui_obj = self.set_node_tree_item_add(
                    instance_hou_obj.path(),
                    parent_tree_item=geo_gui_obj,
                    is_dcc_node=True
                )


class AttributeConstantTool(utl_gui_pnl_abstract.AbsUtilToolPanel):
    TOOL_PANEL_KEY = 'attribute_constant'
    TOOL_SCHEME = utl_core.Scheme.HOUDINI_TOOL_TD
    DCC_SELECTION_CLS = hou_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(AttributeConstantTool, self).__init__(*args, **kwargs)
        self.set_panel_build()

        self._left_node = None
        self._right_node = None

    def set_panel_build(self):
        self.set_show_menu_raw(
            [
                ('Log', None, self.set_log_unit_show),
                ('Help', None, self.set_help_unit_show)
            ]
        )
        # viewer
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        self._obj_tree_viewer_0.set_header_view_create(
            [('Label(s)', 2), ('Name(s)', 1), ('Type(s)', 1), ('Value(s)', 1), ('Description(s)', 1)],
            self.get_definition_window_size()[0] - 24
        )
        expand_box_0.set_widget_add(self._obj_tree_viewer_0)
        self._obj_tree_viewer_0.connect_item_select_changed_to(self.set_attribute_selected)
        # log
        expand_box_1 = prx_widgets.PrxExpandedGroup()
        expand_box_1.set_name('Log')
        self.set_widget_add(expand_box_1)
        self._text_browser = qt_widgets.QtTextBrowser_()
        expand_box_1.set_widget_add(self._text_browser)

        self._load_left_button = qt_widgets.QtPressButton()
        self._load_left_button.setText('Load Left')
        self._load_left_button.clicked.connect(self.set_left_reload)
        self.set_button_add(self._load_left_button)

        self._apply_button = qt_widgets.QtPressButton()
        self._apply_button.setText('Apply')
        self.set_button_add(self._apply_button)
        self._apply_button.clicked.connect(self.set_constant)

        self._load_right_button = qt_widgets.QtPressButton()
        self._load_right_button.setText('Load Right')
        self._load_right_button.clicked.connect(self.set_right_reload)
        self.set_button_add(self._load_right_button)

    def get_selected_attribute_names(self):
        lis = []
        treeItems = self._obj_tree_viewer_0._get_selected_items_()
        for treeItem in treeItems:
            port_path = treeItem.text(1)
            lis.append(port_path)
        return lis

    def set_attribute_selected(self):
        selected_attribute_names = self.get_selected_attribute_names()
        if selected_attribute_names:
            port_path = selected_attribute_names[0]
            if self._right_node is not None:
                hou_node = self._right_node.hou_obj
                network_editor = None
                for i in hou.ui.currentPaneTabs():
                    if isinstance(i, hou.NetworkEditor):
                        network_editor = i
                #
                if network_editor:
                    network_editor.setCurrentNode(hou_node)

                parameter_editor = None
                for i in hou.ui.currentPaneTabs():
                    if isinstance(i, hou.ParameterEditor):
                        parameter_editor = i

                if parameter_editor:
                    parameter_editor.setFilterEnabled(True)
                    parameter_editor.setFilterMode(hou.parmFilterMode.AllParms)
                    parameter_editor.setFilterCriteria(hou.parmFilterCriteria.NameOrLabel)
                    parameter_editor.setFilterExactMatch(True)

                    pattern = port_path
                    parameter_editor.setFilterPattern(pattern)

    def set_left_reload(self):
        selected_nodes = hou.selectedNodes()
        if selected_nodes:
            hou_node = selected_nodes[0]
            self._left_node = hou_dcc_objects.Node(hou_node.path())
            self._load_left_button.setText(
                'Load Left ( {} )'.format(self._left_node.path)
            )
            
    def set_right_reload(self):
        selected_nodes = hou.selectedNodes()
        if selected_nodes:
            hou_node = selected_nodes[0]
            self._right_node = hou_dcc_objects.Node(hou_node.path())
            self._load_right_button.setText(
                'Load Right ( {} )'.format(self._right_node.path)
            )

    def set_attribute_tree_item_add(self, label, name, type_name, value, icon=None, parent_tree_item=None):
        if parent_tree_item is None:
            tree_item = self._obj_tree_viewer_0.set_item_add(
                label, name, type_name, value,
                item_class=prx_widgets.PrxDccObjTreeItem,
            )
        else:
            tree_item = parent_tree_item.set_child_add(
                label, name, type_name, value,
                item_class=prx_widgets.PrxDccObjTreeItem,
            )
        if icon is not None:
            tree_item.set_icon_by_file(icon)
        return tree_item
    @classmethod
    def set_node_data_update(cls, dic, hou_node):
        hou_parms = hou_node.parmTuples()
        for hou_parm in hou_parms:
            parm_template = hou_parm.parmTemplate()
            parm_type = parm_template.type()
            if parm_type in [
                hou.parmTemplateType.Int,
                hou.parmTemplateType.Float,
                hou.parmTemplateType.String,
                hou.parmTemplateType.Toggle,
                hou.parmTemplateType.Menu,
                hou.parmTemplateType.Ramp,
            ]:
                is_hidden = parm_template.isHidden()
                name = hou_parm.name()
                label = parm_template.label()
                type_name = parm_type.name()
                value = hou_parm.eval()
                if parm_type == hou.parmTemplateType.Toggle:
                    value_string = ['False', 'True'][value[0]]
                else:
                    if parm_template.numComponents() == 1:
                        if isinstance(value, tuple):
                            value_string = str(value[0])
                        else:
                            value_string = str(value)
                    else:
                        value_string = str(value)
                dic[name] = label, type_name, value_string, is_hidden
    @classmethod
    def set_type_data_update(cls, dic, hou_node):
        hou_node_type = hou_node.type()
        hou_parm_templates = hou_node_type.parmTemplates()
        for parm_template in hou_parm_templates:
            parm_type = parm_template.type()
            if parm_type in [
                hou.parmTemplateType.Int,
                hou.parmTemplateType.Float,
                hou.parmTemplateType.String,
                hou.parmTemplateType.Toggle,
                hou.parmTemplateType.Menu,
                hou.parmTemplateType.Ramp,
            ]:
                is_hidden = parm_template.isHidden()
                label = parm_template.label()
                name = parm_template.name()
                type_name = parm_type.name()
                value = parm_template.defaultValue()
                if parm_template.numComponents() == 1:
                    if isinstance(value, tuple):
                        value_string = str(value[0])
                    else:
                        value_string = str(value)
                else:
                    value_string = str(value)
                dic[name] = label, type_name, value_string, is_hidden

    def set_constant(self):
        self._obj_tree_viewer_0.set_clear()
        #
        self._left_dict = collections.OrderedDict()
        if self._left_node is not None:
            hou_node = self._left_node.hou_obj
            self.set_node_data_update(self._left_dict, hou_node)
        else:
            if self._right_node is not None:
                hou_node = self._right_node.hou_obj
                self.set_type_data_update(self._left_dict, hou_node)
        self._right_dict = collections.OrderedDict()
        if self._right_node is not None:
            hou_node = self._right_node.hou_obj
            self.set_node_data_update(self._right_dict, hou_node)

        for k, v in self._left_dict.items():
            descriptions = []
            name = k
            label, type_name, value, is_hidden = v
            tree_item = self.set_attribute_tree_item_add(label, name, type_name, value)
            if k in self._right_dict:
                tree_item.set_adopt_state(0)
                tree_item.set_icon_by_file(utl_core.Icon.get('intersection'))
                right_value = self._right_dict[name][2]
                descriptions.append('intersection')
                if not value == right_value:
                    tree_item.set_name('{} | {}'.format(value, right_value), 3)
                    tree_item.set_error_state(3)
                    descriptions.append('value is changed')
            else:
                tree_item.set_error_state(0)
                tree_item.set_icon_by_file(utl_core.Icon.get('deletion'))
                descriptions.append('deletion')

            tree_item.set_name('; '.join(descriptions), 4)

            if is_hidden is True:
                tree_item.set_temporary_state(0)
        #
        for k, v in self._right_dict.items():
            descriptions = []
            name = k
            label, type_name, value, is_hidden = v
            if k not in self._left_dict:
                tree_item = self.set_attribute_tree_item_add(label, name, type_name, value)
                tree_item.set_warning_state(0)
                tree_item.set_icon_by_file(utl_core.Icon.get('addition'))
                descriptions.append('addition')

                tree_item.set_name('; '.join(descriptions), 4)

                tree_item.widget.setHidden(is_hidden)
                if is_hidden is True:
                    tree_item.set_temporary_state(0)
