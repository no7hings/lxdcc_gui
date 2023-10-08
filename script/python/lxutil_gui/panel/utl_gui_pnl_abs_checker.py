# coding:utf-8
import six

from lxutil_gui.qt import gui_qt_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

from lxutil_gui.panel import utl_gui_pnl_abstract

from lxutil_gui import gui_core


class AbsSceneCheckerToolPanel(
    prx_widgets.PrxBaseWindow,
    utl_gui_pnl_abstract.AbsGuiMethodDef
):
    PANEL_KEY = 'scene_checker'
    #
    DCC_SELECTION_CLS = None
    #
    STEP_LOADER_CLS = None
    METHOD_CREATOR_CLS = None
    #
    TEST_ENABLE = False
    TEST_KEYS = []
    def __init__(self, properties, *args, **kwargs):
        super(AbsSceneCheckerToolPanel, self).__init__(*args, **kwargs)
        #
        self._window_configure = gui_core.PanelsConfigure().get_window(
            self.PANEL_KEY
        )
        self.set_window_title(
            self._window_configure.get('name')
        )
        self.set_definition_window_size(
            self._window_configure.get('size')
        )
        #
        self.set_panel_build()
        #
        self._set_gui_method_def_init_()
        self._is_check_passed = False
        self._ignore_show_hide_enable = False
        self._obj_names = []
        self._obj_name_dict = {}
        if properties:
            step_key = self.STEP_LOADER_CLS.get_key(properties)
            self._step_loader = self.STEP_LOADER_CLS(step_key)
            self._method_creator = self.METHOD_CREATOR_CLS(self._get_checker_keys_())
            self._set_method_obj_guis_build_()

    def set_panel_build(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()
        #
        self._check_and_repair_button = prx_widgets.PrxPressItem()
        self._check_and_repair_button.set_icon_name('python')
        self._check_and_repair_button.set_name('Check and Repair')
        self.add_button(self._check_and_repair_button)
        self._check_and_repair_button.connect_press_clicked_to(self.set_repair_run)
        #
        self._check_button = prx_widgets.PrxPressItem()
        self._check_button.set_icon_name('python')
        self._check_button.set_name('Check')
        self.add_button(self._check_button)
        self._check_button.connect_press_clicked_to(self.set_check_run)
        #
        self._repair_button = prx_widgets.PrxPressItem()
        self._repair_button.set_icon_name('python')
        self._repair_button.set_name('Repair')
        self.add_button(self._repair_button)
        self._repair_button.connect_press_clicked_to(self.set_repair_run)

    def _set_viewer_groups_build_(self):
        # viewer
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        self._tree_viewer = prx_widgets.PrxTreeView()
        expand_box_0.add_widget(self._tree_viewer)
        self._tree_viewer.set_header_view_create(
            [('Name(s)', 6), ('Type(s)', 2), ('Ignore-enable(s)', 2), ('Description(s)', 4)],
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
                ('Check All', None, self.set_check_run),
                ('Repair All', None, self.set_repair_run),
                (),
                ('Expand All', None, self._tree_viewer.set_all_items_expand),
                ('Collapse All', None, self._tree_viewer.set_all_items_collapse),
                (),
                ('Select all', None, None),
                ('Select clear', None, None),
                (),
                ('Show Ignore Node(s)', None, (self.get_ignore_show_hide, self.set_ignore_show_hide_switch)),
            ]
        )

    def _set_configure_groups_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Configure(s)')
        # expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        #
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.add_widget(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._configure_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._configure_gui.widget)
        #
        _port = self._configure_gui.add_port(
            prx_widgets.PrxPortAsFileOpen('file_path', 'File-path')
        )

    def set_ignore_show_hide_switch(self):
        self._ignore_show_hide_enable = not self._ignore_show_hide_enable

    def get_ignore_show_hide(self):
        return self._ignore_show_hide_enable

    def _get_checker_keys_(self):
        if self.TEST_ENABLE is True:
            return self.TEST_KEYS
        return self._step_loader.get_checker_keys()

    def _set_method_obj_guis_build_(self):
        fnc_scn_isp_paths = self._method_creator.get_method_keys()
        for method_key in fnc_scn_isp_paths:
            inspection = self._method_creator._set_method_create_(method_key)
            if inspection:
                if method_key not in self._method_gui_dict:
                    inspection_gui = self._tree_viewer.create_item(
                        name=(inspection.loader.label,),
                        item_class=prx_widgets.PrxLabelTreeItem,
                        tool_tip=(inspection.loader.get_gui_descriptions(),),
                        icon=gui_qt_core.QtUtilMtd.get_qt_icon('inspection')
                    )
                    inspection_gui.set_gui_menu_raw(
                        [
                            ('Ignore Check Selected Method(s) On', None, self.set_selected_inspection_ignore_check_on),
                            ('Ignore Check Selected Method(s) Off', None, self.set_selected_inspection_ignore_check_off),
                            (),
                            ('Check Selected Method(s)', None, self.set_selected_inspections_check),
                            ('Repair Selected Method(s)', None, self.set_selected_inspections_repair),
                            (),
                            ('About Current Method', None, None)
                        ]
                    )
                    inspection_gui.set_gui_attribute('inspection', inspection)
                    self._method_gui_dict[method_key] = inspection_gui
    # inspection
    def get_selected_inspection_guis(self):
        qt_tree_items = self._tree_viewer._get_selected_items_()
        lis = []
        for qt_tree_item in qt_tree_items:
            gui_proxy = qt_tree_item.gui_proxy
            if isinstance(gui_proxy, prx_widgets.PrxLabelTreeItem):
                lis.append(gui_proxy)
        return lis

    def set_selected_inspections_check(self):
        inspection_guis = self.get_selected_inspection_guis()
        if inspection_guis:
            for inspection_gui in inspection_guis:
                # noinspection PyUnresolvedReferences
                inspection = inspection_gui.get_gui_attribute('inspection')
                test_inspection = self._set_isp_check_debug_(inspection)
                self._set_isp_gui_update_(test_inspection, inspection_gui)

    def set_selected_inspections_repair(self):
        inspection_guis = self.get_selected_inspection_guis()
        if inspection_guis:
            for inspection_gui in inspection_guis:
                # noinspection PyUnresolvedReferences
                inspection = inspection_gui.get_gui_attribute('inspection')
                inspection.set_repair_run()
                self._set_isp_gui_update_(inspection, inspection_gui)
        # recheck
        self.set_selected_inspections_check()

    def set_selected_inspection_ignore_check_on(self):
        inspection_guis = self.get_selected_inspection_guis()
        if inspection_guis:
            for inspection_gui in inspection_guis:
                children = inspection_gui.get_children()
                if children:
                    for obj_gui in children:
                        self._set_obj_ignore_by_gui_(obj_gui, True)
                    #
                    self._set_isp_gui_state_update_(inspection_gui)

    def set_selected_inspection_ignore_check_off(self):
        inspection_guis = self.get_selected_inspection_guis()
        if inspection_guis:
            for inspection_gui in inspection_guis:
                children = inspection_gui.get_children()
                if children:
                    for obj_gui in children:
                        self._set_obj_ignore_by_gui_(obj_gui, False)
                    #
                    self._set_isp_gui_state_update_(inspection_gui)
    # object
    def set_selected_objects_ignore_check_on(self):
        lis = []
        obj_guis = self.get_selected_obj_guis()
        for obj_gui in obj_guis:
            self._set_obj_ignore_by_gui_(obj_gui, True)
            #
            isp_gui = obj_gui.get_parent()
            if isp_gui not in lis:
                lis.append(isp_gui)
        #
        for isp_gui in lis:
            self._set_isp_gui_state_update_(isp_gui)

    def set_selected_objects_ignore_check_off(self):
        lis = []
        obj_guis = self.get_selected_obj_guis()
        for obj_gui in obj_guis:
            self._set_obj_ignore_by_gui_(obj_gui, False)
            #
            isp_gui = obj_gui.get_parent()
            if isp_gui not in lis:
                lis.append(isp_gui)
        #
        for isp_gui in lis:
            self._set_isp_gui_state_update_(isp_gui)
    @classmethod
    def _set_obj_ignore_by_gui_(cls, obj_gui, boolean):
        inspection, check_index = obj_gui.get_gui_attribute('inspection')
        dcc_obj = obj_gui.get_gui_attribute('dcc_obj')
        if dcc_obj is not None:
            is_ignored = inspection._set_object_ignore_at_(dcc_obj, check_index, boolean)
            #
            if is_ignored is True:
                obj_gui.set_temporary_state()
            else:
                obj_gui.set_normal_state()

    def set_selected_objects_check(self):
        pass

    def set_selected_objects_repair(self):
        pass

    def get_selected_obj_guis(self):
        lis = []
        qt_tree_items = self._tree_viewer._get_selected_items_()
        for qt_tree_item in qt_tree_items:
            # is child of inspection
            parent = qt_tree_item.parent()
            if parent is not None:
                if isinstance(parent.gui_proxy, prx_widgets.PrxLabelTreeItem):
                    obj_gui = qt_tree_item.gui_proxy
                    if isinstance(obj_gui, prx_widgets.PrxDccObjTreeItem):
                        lis.append(obj_gui)
        return lis

    def _set_dcc_obj_select_(self):
        if self.DCC_SELECTION_CLS is not None:
            paths = []
            qt_tree_items = self._tree_viewer._get_selected_items_()
            for qt_tree_item in qt_tree_items:
                gui_proxy = qt_tree_item.gui_proxy
                if isinstance(gui_proxy, prx_widgets.PrxDccObjTreeItem):
                    dcc_obj = gui_proxy.get_gui_attribute('dcc_obj')
                    if dcc_obj is not None:
                        paths.append(dcc_obj.path)
            if paths:
                self.DCC_SELECTION_CLS(paths).select_all()
            else:
                self.DCC_SELECTION_CLS.set_clear()

    # noinspection PyMethodMayBeStatic
    def _set_error_components_gui_build_(self, inspection, dcc_obj, include_indices=None):
        obj_path = dcc_obj.path
        tree_item = dcc_obj.get_obj_gui()
        sub_raws = inspection.get_error_obj_comp_raw_at(obj_path)
        for sub_raw in sub_raws:
            sub_obj, check_index = sub_raw
            if include_indices is not None:
                if check_index not in include_indices:
                    continue
            error_description = inspection.get_error_description_at(check_index)
            ignore_enable = inspection.loader.get_ignore_enable_at(check_index)
            gui_description = inspection.loader.get_gui_description_at(check_index)
            sub_obj_gui = tree_item.add_child(
                name=(sub_obj.name, sub_obj.type, ignore_enable, error_description),
                item_class=prx_widgets.PrxDccObjTreeItem,
                tool_tip=(u'type:"{}"\npath:"{}"'.format(sub_obj.type, sub_obj.path), None, None, gui_description),
                icon=sub_obj.icon
            )
            sub_obj_gui.set_gui_attribute('dcc_obj', sub_obj)

    # noinspection PyMethodMayBeStatic
    def _set_error_files_gui_build_(self, inspection, dcc_obj, include_indices=None):
        obj_path = dcc_obj.path
        tree_item = dcc_obj.get_obj_gui()
        sub_raws = inspection.get_error_object_file_raw(obj_path)
        for sub_raw in sub_raws:
            sub_obj, check_index = sub_raw
            if include_indices is not None:
                if check_index not in include_indices:
                    continue
            error_description = inspection.get_error_description_at(check_index)
            ignore_enable = inspection.loader.get_ignore_enable_at(check_index)
            gui_description = inspection.loader.get_gui_description_at(check_index)
            sub_obj_gui = tree_item.add_child(
                name=(sub_obj.name, sub_obj.type, ignore_enable, error_description),
                item_class=prx_widgets.PrxStgObjTreeItem,
                icon=sub_obj.icon,
                tool_tip=(u'type:"{}"\npath:"{}"'.format(sub_obj.type, sub_obj.path), None, None, gui_description),
                menu=sub_obj.get_gui_menu_raw()
            )
            sub_obj_gui.set_gui_attribute('os', sub_obj)

    # noinspection PyMethodMayBeStatic
    def _set_error_sources_gui_build_(self, inspection, dcc_obj, include_indices=None):
        obj_path = dcc_obj.path
        tree_item = dcc_obj.get_obj_gui()
        sub_raws = inspection.get_error_object_source_raw(obj_path)
        for source_raw in sub_raws:
            sub_obj, check_index = source_raw
            if include_indices is not None:
                if check_index not in include_indices:
                    continue
            error_description = inspection.get_error_description_at(check_index)
            ignore_enable = inspection.loader.get_ignore_enable_at(check_index)
            gui_description = inspection.loader.get_gui_description_at(check_index)
            sub_obj_gui = tree_item.add_child(
                name=(sub_obj.name, sub_obj.type, ignore_enable, error_description),
                item_class=prx_widgets.PrxDccObjTreeItem,
                tool_tip=(u'type:"{}"\npath:"{}"'.format(sub_obj.type, sub_obj.path), None, None, gui_description),
                icon=sub_obj.icon
            )
            sub_obj_gui.set_gui_attribute('dcc_obj', sub_obj)

    def _set_isp_check_debug_(self, inspection):
        text_browser = self.get_log_text_browser()
        # noinspection PyBroadException
        try:
            inspection.set_check_run()
            utl_core.Log.set_module_result_trace(
                'inspection-check',
                'inspection: "{}"'.format(inspection.loader.label)
            )
            return inspection
        except Exception:
            import sys
            import traceback
            ex_type, ex_val, ex_stack = sys.exc_info()
            #
            utl_core.Log.set_module_result_trace(
                'inspection-check',
                'inspection: "{}"'.format(inspection.loader.label)
            )
            utl_core.Log.set_result_trace(str(ex_type))
            utl_core.Log.set_result_trace(str(ex_val))
            ex_text = u'\n'.join(
                (u' '.join((unicode(i) for i in stack)) for seq, stack in enumerate(traceback.extract_tb(ex_stack))))
            utl_core.Log.set_result_trace(ex_text)

    def _set_isp_repair_debug_(self, inspection):
        # noinspection PyBroadException
        try:
            inspection.set_repair_run()
            utl_core.Log.set_module_result_trace(
                'inspection-repair',
                'inspection: "{}"'.format(inspection.loader.label)
            )
            return True
        except Exception:
            import sys
            import traceback
            ex_type, ex_val, ex_stack = sys.exc_info()
            #
            utl_core.Log.set_module_result_trace(
                'inspection-repair',
                'inspection: "{}"'.format(inspection.loader.label)
            )
            utl_core.Log.set_result_trace(str(ex_type))
            utl_core.Log.set_result_trace(str(ex_val))
            ex_text = u'\n'.join(
                (u' '.join((unicode(i) for i in stack)) for seq, stack in enumerate(traceback.extract_tb(ex_stack))))
            utl_core.Log.set_result_trace(ex_text)

    def _set_isp_gui_update_(self, inspection, inspection_gui):
        if inspection is not None:
            inspection_gui.set_gui_attribute('inspection', inspection)
            # clear obj gui
            inspection_gui.clear_children()
            #
            error_object_raw_dict = inspection.error_object_raw_dict
            if error_object_raw_dict:
                for k, v in error_object_raw_dict.items():
                    for check_index, (dcc_obj, obj_is_ignored) in v.items():
                        self._set_obj_gui_update_(inspection, inspection_gui, dcc_obj, check_index, obj_is_ignored)
            #
            self._set_isp_gui_state_update_(inspection_gui)

    def _set_obj_gui_update_(self, inspection, inspection_gui, dcc_obj, check_index, obj_is_ignored):
        error_description = inspection.get_error_description_at(check_index)
        ignore_enable = inspection.loader.get_ignore_enable_at(check_index)
        gui_description = inspection.loader.get_gui_description_at(check_index)
        obj_path = dcc_obj.path
        obj_type_name = dcc_obj.type
        if not isinstance(obj_type_name, six.string_types):
            obj_type_name = dcc_obj.type.name
        #
        obj_name = dcc_obj.name
        if obj_name not in self._obj_names:
            override = False
            self._obj_names.append(obj_name)
        else:
            override = True
            _obj_gui = self._obj_name_dict[obj_name]
            _dcc_obj = _obj_gui.get_gui_attribute('dcc_obj')
            _new_obj_name = _dcc_obj.PATHSEP.join(obj_path.split(_dcc_obj.PATHSEP)[-2:])
            _obj_gui.set_name(_new_obj_name)
            #
            obj_name = dcc_obj.PATHSEP.join(obj_path.split(dcc_obj.PATHSEP)[-2:])
        #
        obj_gui = inspection_gui.add_child(
            name=(obj_name, obj_type_name, ignore_enable, error_description),
            item_class=prx_widgets.PrxDccObjTreeItem,
            tool_tip=('type:"{}"\npath:"{}"'.format(obj_type_name, obj_path), None, None, gui_description),
            icon=dcc_obj.icon
        )
        if override is False:
            self._obj_name_dict[obj_name] = obj_gui
        #
        obj_gui.set_gui_attribute('dcc_obj', dcc_obj)
        obj_gui.set_gui_attribute('inspection', (inspection, check_index))
        obj_gui.set_gui_menu_raw(
            [
                ('Ignore Check Selected Object(s) On', None, self.set_selected_objects_ignore_check_on),
                ('Ignore Check Selected Object(s) Off', None, self.set_selected_objects_ignore_check_off),
                (),
                ('Check Selected Object(s)', None, None),
                ('Repair Selected Object(s)', None, None),

            ]
        )
        dcc_obj.set_obj_gui(obj_gui)
        # add node menu data
        error_node_menu_data = dcc_obj.get_gui_menu_raw()
        if error_node_menu_data:
            obj_gui.get_gui_menu_raw().append(())
            obj_gui.get_gui_menu_raw().extend(error_node_menu_data)
        #
        if obj_is_ignored is True:
            obj_gui.set_temporary_state()
        else:
            obj_gui.set_normal_state()
        #
        self._set_error_components_gui_build_(inspection, dcc_obj, [check_index])
        #
        self._set_error_files_gui_build_(inspection, dcc_obj, [check_index])
        #
        self._set_error_sources_gui_build_(inspection, dcc_obj, [check_index])

    def _set_isp_repair_(self, inspection, inspection_gui):
        pass

    @classmethod
    def _set_isp_gui_state_update_(cls, inspection_gui):
        inspection = inspection_gui.get_gui_attribute('inspection')
        if inspection is not None:
            inspection._set_check_result_update_()
            if inspection.get_is_check_passed():
                if inspection.get_is_check_ignored():
                    inspection_gui.set_temporary_state()
                else:
                    inspection_gui.set_adopt_state()
            else:
                inspection_gui.set_error_state()

    def set_check_run(self):
        fnc_scn_isp_paths = self._method_creator.get_method_keys()
        p = self.set_progress_create(len(fnc_scn_isp_paths))
        for fnc_isp_path in fnc_scn_isp_paths:
            inspection = self._method_creator._set_method_create_(fnc_isp_path)
            p.set_update()
            if inspection is not None:
                inspection_gui = self.get_method_gui(fnc_isp_path)
                inspection_ = self._set_isp_check_debug_(inspection)
                self._set_isp_gui_update_(inspection_, inspection_gui)
        p.set_stop()

    def set_repair_run(self):
        for inspection_gui in self._method_gui_dict.values():
            inspection = inspection_gui.get_gui_attribute('inspection')
            if inspection is not None:
                self._set_isp_repair_debug_(inspection)
        # recheck
        self.set_check_run()

    def set_check_and_repair(self):
        self.set_check_run()
        self.set_repair_run()

    def _set_check_result_update_(self):
        is_passed = True
        for inspection_gui in self._method_gui_dict.values():
            inspection = inspection_gui.get_gui_attribute('inspection')
            if inspection is not None:
                is_passed = inspection.get_is_check_passed()
                if is_passed is False:
                    is_passed = False
                    break
        self._is_check_passed = is_passed

    def get_is_check_passed(self):
        self._set_check_result_update_()
        return self._is_check_passed
