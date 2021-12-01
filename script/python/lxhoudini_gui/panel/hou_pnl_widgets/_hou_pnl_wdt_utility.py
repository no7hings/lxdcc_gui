# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import hou

from lxutil import utl_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.panel import utl_gui_pnl_abstract

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_prd import utl_prd_objects

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
        self._tree_viewer.set_item_select_changed_connect_to(self.set_select)
        # log
        expand_box_1 = prx_widgets.PrxExpandedGroup()
        expand_box_1.set_name('Log')
        self.set_widget_add(expand_box_1)
        self._text_browser = qt_widgets.QtTextBrowser()
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
                self.DCC_SELECTION_CLS(paths).set_all_select()
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
        tree_item.set_file_icon(dcc_obj.icon)
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
            tree_item.set_file_icon(icon)
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
        self._obj_tree_viewer_0.set_item_select_changed_connect_to(self.set_attribute_selected)
        # log
        expand_box_1 = prx_widgets.PrxExpandedGroup()
        expand_box_1.set_name('Log')
        self.set_widget_add(expand_box_1)
        self._text_browser = qt_widgets.QtTextBrowser()
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
            tree_item.set_file_icon(icon)
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
                tree_item.set_file_icon(utl_core.Icon.get('intersection'))
                right_value = self._right_dict[name][2]
                descriptions.append('intersection')
                if not value == right_value:
                    tree_item.set_name('{} | {}'.format(value, right_value), 3)
                    tree_item.set_error_state(3)
                    descriptions.append('value is changed')
            else:
                tree_item.set_error_state(0)
                tree_item.set_file_icon(utl_core.Icon.get('deletion'))
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
                tree_item.set_file_icon(utl_core.Icon.get('addition'))
                descriptions.append('addition')

                tree_item.set_name('; '.join(descriptions), 4)

                tree_item.widget.setHidden(is_hidden)
                if is_hidden is True:
                    tree_item.set_temporary_state(0)


class SceneSwitcherToolPanel(
    utl_gui_pnl_abstract.AbsUtilToolPanel,
    utl_gui_pnl_abstract.AbsObjGuiDef
):
    TOOL_PANEL_KEY = 'scene_switcher'
    TOOL_SCHEME = utl_core.Scheme.HOUDINI_TOOL_TD
    DCC_SELECTION_CLS = hou_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(SceneSwitcherToolPanel, self).__init__(*args, **kwargs)
        self.set_panel_build()

    def set_panel_build(self):
        # tool
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Alembic-switch(s)')
        expand_box_0.set_expanded(True)
        expand_box_0.set_size_mode(1)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        self._qt_layout_0 = qt_widgets.QtGridLayout(qt_widget_0)
        #
        self._set_alembic_switch_gui_build_()
        #
        # expand_box_1 = prx_widgets.PrxExpandedGroup()
        # expand_box_1.set_name('Asset-display-switch(s)')
        # expand_box_1.set_expanded(True)
        # self.set_widget_add(expand_box_1)

        expand_box_2 = prx_widgets.PrxExpandedGroup()
        expand_box_2.set_name('Asset-element-switch(s)')
        expand_box_2.set_expanded(True)
        self.set_widget_add(expand_box_2)
        qt_widget_2 = qt_widgets.QtWidget()
        expand_box_2.set_widget_add(qt_widget_2)
        self._qt_layout_2 = qt_widgets.QtGridLayout(qt_widget_2)
        self._set_asset_element_switch_build_()

    def _set_alembic_switch_gui_build_(self):
        def fnc_(qt_button_, switch_args_):
            def switch_fnc_():
                _port_name, _value = switch_args_
                alembic_hou_objs = hou_dcc_objects.Selection.get_selected_alembics()
                if alembic_hou_objs:
                    p = self.set_progress_create(len(alembic_hou_objs))
                    for _i in alembic_hou_objs:
                        p.set_update()
                        _i.parm(_port_name).set(_value)
                    p.set_stop()

            qt_button_.clicked.connect(switch_fnc_)

        button_cfg_raw = [
            ('Full-geometry', ('viewportlod', 0), (0, 0, 1, 1)),
            ('Point-cloud', ('viewportlod', 1), (0, 1, 1, 1)),
            ('Bounding-box', ('viewportlod', 2), (1, 0, 1, 1)),
            ('Centroid', ('viewportlod', 3), (1, 1, 1, 1)),
            ('Hidden', ('viewportlod', 4), (2, 0, 1, 2))
        ]
        for i in button_cfg_raw:
            label, switch_args, pos_args = i
            qt_button = qt_widgets.QtPressButton()
            qt_button.setText(label)
            self._qt_layout_0.addWidget(qt_button, *pos_args)
            fnc_(qt_button, switch_args)

    def _set_display_switch_gui_build_(self):
        pass

    def _set_asset_element_switch_build_(self):
        self._tree_view_2 = prx_widgets.PrxTreeView()
        self._qt_layout_2.addWidget(self._tree_view_2.widget)
        self._tree_view_2.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 2), ('Stage(s)', 2)],
            self.get_definition_window_size()[0] - 16
        )
        self._tree_view_2.set_item_select_changed_connect_to(self._set_dcc_obj_select_)

        self._load_button_2 = qt_widgets.QtPressButton()
        self._load_button_2.setText('Load')
        self._qt_layout_2.addWidget(self._load_button_2)

        self._load_button_2.clicked.connect(self._set_asset_gui_build_)
    @classmethod
    def _get_selected_asset_raw_(cls):
        lis = []
        selected_geos = hou_dcc_objects.Selection.get_selected_geos()
        for i in selected_geos:
            dcc_obj = hou_dcc_objects.Node(i.path())
            ctn_gmt_abc_dcc_path = dcc_obj.path
            ctn_prx_ass_dcc_path = dcc_obj.path.replace('gmt_abc', 'prx_ass')
            children = dcc_obj.get_children()
            for j in children:
                if j.type == 'Sop/alembic':
                    if j.get_is_naming_match('asset_gmt_abc'):
                        gmt_abc_dcc_obj = j
                        gmt_abc_plf_path = j.get_port('fileName').get()
                        mtl_mtx_dcc_path = dcc_obj.get_port('ar_operator_graph').get()
                        if mtl_mtx_dcc_path:
                            mtl_mtx_dcc_obj = hou_dcc_objects.Node(mtl_mtx_dcc_path)
                            mtl_mtx_plf_path = mtl_mtx_dcc_obj.get_port('filename').get()
                        else:
                            mtl_mtx_dcc_obj, mtl_mtx_plf_path = [None]*2
                        lis.append(
                            (
                                ctn_gmt_abc_dcc_path, ctn_prx_ass_dcc_path,
                                gmt_abc_dcc_obj.path, gmt_abc_plf_path,
                                mtl_mtx_dcc_obj.path, mtl_mtx_plf_path
                             )
                        )
        return lis

    def _set_entities_build_(self):
        self._assets_opt = utl_prd_objects.AssetsOpt(project='cg7')
        for i in self._get_selected_asset_raw_():
            (
                ctn_gmt_abc_dcc_path, ctn_prx_ass_dcc_path,
                gmt_abc_dcc_path, gmt_abc_plf_path,
                mtl_mtx_dcc_path, mtl_mtx_plf_path
            ) = i
            result = self._assets_opt.set_load_by_plf_path(gmt_abc_plf_path)
            if result:
                obj, is_create = result
                raw_dict = {
                    'self.asset.ctn.gmt_abc.dcc_path': ctn_gmt_abc_dcc_path,
                    'self.asset.ctn.prx_ass.dcc_path': ctn_prx_ass_dcc_path,
                    #
                    'self.asset.gmt_abc.dcc_path': gmt_abc_dcc_path,
                    'self.asset.gmt_abc.dcc_port': 'fileName',
                    'self.asset.mtl_mtx.dcc_path': mtl_mtx_dcc_path,
                    'self.asset.mtl_mtx.dcc_port': 'filename'
                }
                [obj._set_port_build_(k, v) for k, v in raw_dict.items()]
    @classmethod
    def _get_cnt_is_current_(cls, _ctn_dcc_path):
        _hou_obj = hou.node(_ctn_dcc_path)
        if _hou_obj is not None:
            return len([i for i in _hou_obj.dependents() if i.type().name() == 'instance']) > 0
        return False

    def _set_ast_ctn_switch_(self, entity_opt, dta_scm):
        pass

    def _get_ctn_gui_menu_raw_(self, entity_opt, entity_gui):
        def add_switch_fnc_(dta_scm_):
            def fnc_():
                if _ctn_dcc_path == _prx_ass_dcc_path:
                    _gmt_abc_hou_obj = hou.node(_gmt_abc_dcc_path)
                    #
                    _dcc_obj = hou_dcc_objects.Node(_ctn_dcc_path)
                    _hou_obj, _is_create = _dcc_obj.get_dcc_instance('arnold_procedural')
                    if _is_create is True:
                        _dcc_obj.get_port('ar_display').set(2)
                        _dcc_obj.set_display_enable(False)
                        _hou_obj.setInput(0, _gmt_abc_hou_obj)
                    #
                    vsn_all = entity_opt.get_vsn_all(dta_scm_)
                    vsn_lst = vsn_all[-1]
                    vsn_key_lst, vsn_raw_lst, vsn_cmp_raw_lst = vsn_lst
                    _hou_obj.parm('ar_filename').set(vsn_raw_lst)
                    #
                    if _gmt_abc_hou_obj is not None:
                        _ist_hou_objs = [i for i in _gmt_abc_hou_obj.dependents() if i.type().name() == 'instance']
                        [i.parm('instancepath').set(_prx_ass_dcc_path) for i in _ist_hou_objs]
                #
                elif _ctn_dcc_path == _gmt_abc_dcc_path:
                    _hou_obj = hou.node(_ctn_dcc_path)
                    _prx_ass_hou_obj = hou.node(_prx_ass_dcc_path)
                    if _prx_ass_hou_obj is not None:
                        _ist_hou_objs = [i for i in _prx_ass_hou_obj.dependents() if i.type().name() == 'instance']
                        [i.parm('instancepath').set(_gmt_abc_dcc_path) for i in _ist_hou_objs]

            def enable_fnc_():
                vsn_all = entity_opt.get_vsn_all(dta_scm_)
                if vsn_all:
                    return self._get_cnt_is_current_(_ctn_dcc_path)
            #
            _ctn_dcc_path = entity_opt.get_variant('self.asset.ctn.{}.dcc_path'.format(dta_scm_))
            #
            _gmt_abc_dcc_path = entity_opt.get_variant('self.asset.ctn.gmt_abc.dcc_path')
            _prx_ass_dcc_path = entity_opt.get_variant('self.asset.ctn.prx_ass.dcc_path')
            #
            lis.append(
                (dta_scm_, None, (enable_fnc_, fnc_))
            )
        #
        lis = []
        for dta_scm in ['gmt_abc', 'prx_ass']:
            add_switch_fnc_(dta_scm)

        return lis

    def _get_elm_gui_menu_raw_(self, entity_opt, entity_gui, dta_scm):
        def add_switch_fnc_(dta_scm_, stp_brh_, stg_brh_):
            def fnc_():
                vsn_all = entity_opt.get_vsn_all(dta_scm_, stp_brh_, stg_brh_)
                if vsn_all:
                    vsn_lst = vsn_all[-1]
                    vsn_key_lst, vsn_raw_lst, vsn_cmp_raw_lst = vsn_lst
                    _dcc_path = entity_opt.get_variant('self.asset.{}.dcc_path'.format(dta_scm_))
                    _dcc_obj = hou_dcc_objects.Node(_dcc_path)
                    if _dcc_obj.get_is_exists() is True:
                        dcc_port = entity_opt.get_variant('self.asset.{}.dcc_port'.format(dta_scm_))
                        _dcc_obj.get_port(dcc_port).set(vsn_raw_lst)
                        entity_gui.set_name(_key, 2)

            def enable_fnc_():
                vsn_all = entity_opt.get_vsn_all(dta_scm_, stp_brh_, stg_brh_)
                if vsn_all:
                    _dcc_path = entity_opt.get_variant('self.asset.{}.dcc_path'.format(dta_scm_))
                    _dcc_obj = hou_dcc_objects.Node(_dcc_path)
                    if _dcc_obj.get_is_exists() is True:
                        dcc_port = entity_opt.get_variant('self.asset.{}.dcc_port'.format(dta_scm_))
                        _plf_file_path = _dcc_obj.get_port(dcc_port).get()
                        if _plf_file_path:
                            if _plf_file_path.startswith(_cur_stp_plf_path):
                                return True
                    return False

            #
            _cur_stp_plf_path = entity_opt.get_stp_plf_path(stp_brh_, stg_brh_)
            _key = '{}-{}-{}'.format(stp_brh_, stg_brh_, dta_scm_)
            lis.append(
                (_key, None, (enable_fnc_, fnc_))
            )

        def open_prd_folder_fnc_():
            plf_path = entity_opt.prd_plf_path
            if plf_path is not None:
                os_file = utl_dcc_objects.OsDirectory_(plf_path)
                os_file.set_open()

        def open_tmp_folder_fnc_():
            plf_path = entity_opt.tmp_plf_path
            if plf_path is not None:
                os_file = utl_dcc_objects.OsDirectory_(plf_path)
                os_file.set_open()
        #
        stp_brhs_dict = {
            'mtl_mtx': [
                'surface'
            ],
            'gmt_abc': [
                'model', 'surface'
            ]
        }
        #
        lis = []
        stp_brhs = stp_brhs_dict[dta_scm]
        for stp_brh in stp_brhs:
            for stage in ['prd', 'tmp']:
                add_switch_fnc_(dta_scm, stp_brh, stage)
            lis.append(())

        lis.extend(
            [
                (),
                ('Open Prd-folder', 'file/folder', open_prd_folder_fnc_),
                ('Open Tmp-folder', 'file/folder', open_tmp_folder_fnc_)
            ]
        )
        return lis

    def _set_asset_gui_build_(self):
        self._set_entities_build_()
        entity_opts = self._assets_opt.get_entity_opts()
        self._tree_view_2.set_clear()
        for entity_opt in entity_opts:
            entity = entity_opt.obj
            all_parent_paths = entity.get_ancestor_paths()
            all_parent_paths.reverse()
            for obj_path in all_parent_paths:
                obj = self._assets_opt.universe.get_obj(obj_path)
                obj_gui = self._set_prd_obj_gui_add_(
                    obj,
                    self._tree_view_2
                )
                obj_gui.set_expanded(True)
            #
            entity_gui = self._set_prd_obj_gui_add_(
                entity,
                self._tree_view_2
            )
            entity_gui.set_expanded(True)
            ett_menu = self._get_ctn_gui_menu_raw_(entity_opt, entity_gui)
            entity_gui.set_gui_menu_raw(ett_menu)
            #
            entity_gui.set_gui_attribute('entity_opt', entity_opt)
            ctn_gmt_abc_dcc_path = entity_opt.get_variant('self.asset.ctn.gmt_abc.dcc_path')
            ctn_gmt_abc_dcc_obj = hou_dcc_objects.Node(ctn_gmt_abc_dcc_path)
            ctn_gmt_abc_dcc_obj_gui = self._set_item_prx_add_(ctn_gmt_abc_dcc_obj, entity_gui)
            #
            for dta_scm in ['mtl_mtx', 'gmt_abc']:
                elm_dcc_path = entity_opt.get_variant('self.asset.{}.dcc_path'.format(dta_scm))
                elm_dcc_obj = hou_dcc_objects.Node(elm_dcc_path)
                elm_dcc_obj_gui = self._set_item_prx_add_(elm_dcc_obj, ctn_gmt_abc_dcc_obj_gui)
                elm_menu_raw = self._get_elm_gui_menu_raw_(entity_opt, elm_dcc_obj_gui, dta_scm)
                elm_dcc_obj_gui.set_gui_menu_raw(elm_menu_raw)
            #
            ctn_prx_ass_dcc_path = entity_opt.get_variant('self.asset.ctn.prx_ass.dcc_path')
            ctn_prx_ass_dcc_obj = hou_dcc_objects.Node(ctn_prx_ass_dcc_path)
            ctn_prx_ass_dcc_obj_gui = self._set_item_prx_add_(ctn_prx_ass_dcc_obj, entity_gui)

    def _set_dcc_obj_select_(self):
        if self.DCC_SELECTION_CLS is not None:
            paths = []
            qt_tree_items = self._tree_view_2._get_selected_items_()
            for qt_tree_item in qt_tree_items:
                gui_proxy = qt_tree_item.gui_proxy
                if isinstance(gui_proxy, prx_widgets.PrxObjTreeItem):
                    dcc_obj = gui_proxy.get_gui_attribute('dcc_obj')
                    if dcc_obj is not None:
                        paths.append(dcc_obj.path)
            if paths:
                self.DCC_SELECTION_CLS(paths).set_all_select()
            else:
                self.DCC_SELECTION_CLS.set_clear()
