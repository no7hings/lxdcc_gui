# coding:utf-8
import lxutil_fnc.objects as utl_fnc_objects

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui import utl_gui_core

from lxutil_gui.panel import utl_gui_pnl_abstract

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxresolver.commands as rsv_commands

import lxresolver.operators as rsv_operators

from lxutil import utl_core


class AbsTaskMethodObjGuiDef(object):
    DCC_OBJ_PATHSEP = None
    @classmethod
    def _set_method_group_obj_gui_add_(cls, obj, obj_gui_parent=None, tree_viewer=None):
        obj_gui = obj.get_obj_gui()
        if obj_gui is not None:
            return obj_gui
        #
        kwargs = dict(
            name=(obj.label, obj.type.name),
            item_class=prx_widgets.PrxObjTreeItem,
            tool_tip=obj.properties.get_str_as_yaml_style()
        )
        if obj_gui_parent is not None:
            obj_gui = obj_gui_parent.set_child_add(
                **kwargs
            )
        elif tree_viewer is not None:
            obj_gui = tree_viewer.set_item_add(
                **kwargs
            )
        else:
            raise TypeError()
        #
        obj.set_obj_gui(obj_gui)
        obj_gui.set_icon_by_text(obj.name)
        obj_gui.set_icon_by_text(obj.type_name, 1)
        return obj_gui
    @classmethod
    def _set_method_unit_obj_gui_add_(cls, method_obj, root_dcc_obj_gui):
        key = method_obj.path
        tree_view = root_dcc_obj_gui.get_view()
        if key in tree_view._item_dict:
            return tree_view._item_dict[key]
        else:
            group_dcc_obj = method_obj.get_parent()
            group_dcc_obj_gui = cls._set_method_group_obj_gui_add_(group_dcc_obj, obj_gui_parent=root_dcc_obj_gui)
            group_dcc_obj_gui.set_expanded(True)
            group_dcc_obj_gui.set_checked(True)
            #
            method_obj_gui = cls._set_method_obj_gui_add_(method_obj, obj_gui_parent=group_dcc_obj_gui)
            method_obj_gui.set_checked(True)
            tree_view._item_dict[key] = method_obj_gui
            return method_obj_gui
    @classmethod
    def _set_method_obj_gui_add_(cls, obj, obj_gui_parent=None, tree_viewer=None):
        kwargs = dict(
            name=(obj.label, obj.type.name),
            item_class=prx_widgets.PrxObjTreeItem,
            # tool_tip=obj.properties.get_str_as_yaml_style()
        )
        if obj_gui_parent is not None:
            obj_gui = obj_gui_parent.set_child_add(
                **kwargs
            )
        elif tree_viewer is not None:
            obj_gui = tree_viewer.set_item_add(
                **kwargs
            )
        else:
            raise TypeError()
        #
        obj_gui.set_checked(True)
        obj.set_obj_gui(obj_gui)
        obj_gui.set_icon_by_text(obj.name)
        obj_gui.set_icon_by_text(obj.type_name, 1)
        obj_gui.set_gui_dcc_obj(obj, namespace='method')
        return obj_gui
    @classmethod
    def _set_item_prx_add_(cls, dcc_obj, obj_gui_parent=None, tree_viewer=None):
        kwargs = dict(
            name=(dcc_obj.name, dcc_obj.type),
            item_class=prx_widgets.PrxDccObjTreeItem,
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path
        )
        if obj_gui_parent is not None:
            obj_gui = obj_gui_parent.set_child_add(
                **kwargs
            )
        elif tree_viewer is not None:
            obj_gui = tree_viewer.set_item_add(
                **kwargs
            )
        else:
            raise TypeError()
        #
        obj_gui.set_checked(True)
        dcc_obj.set_obj_gui(obj_gui)
        obj_gui.set_gui_dcc_obj(dcc_obj, namespace='dcc')
        return obj_gui
    @classmethod
    def _set_file_obj_gui_add_(cls, file_obj, obj_gui_parent=None, tree_viewer=None):
        kwargs = dict(
            name=(file_obj.name, file_obj.type),
            item_class=prx_widgets.PrxStgObjTreeItem,
            icon=file_obj.icon,
            tool_tip=file_obj.path,
            menu=file_obj.get_gui_menu_raw()
        )
        if obj_gui_parent is not None:
            obj_gui = obj_gui_parent.set_child_add(
                **kwargs
            )
        elif tree_viewer is not None:
            obj_gui = tree_viewer.set_item_add(
                **kwargs
            )
        else:
            raise TypeError()
        #
        obj_gui.set_checked(True)
        file_obj.set_obj_gui(obj_gui)
        obj_gui.set_gui_dcc_obj(file_obj, namespace='plf')
        return obj_gui
    @classmethod
    def _set_comp_obj_gui_add_(cls, dcc_comp_obj, obj_gui_parent=None, tree_viewer=None):
        kwargs = dict(
            name=(dcc_comp_obj.name, dcc_comp_obj.type),
            item_class=prx_widgets.PrxDccObjTreeItem,
            icon=dcc_comp_obj.icon,
            tool_tip=dcc_comp_obj.path
        )
        if obj_gui_parent is not None:
            obj_gui = obj_gui_parent.set_child_add(
                **kwargs
            )
        elif tree_viewer is not None:
            obj_gui = tree_viewer.set_item_add(
                **kwargs
            )
        else:
            raise TypeError()
        #
        obj_gui.set_checked(True)
        dcc_comp_obj.set_obj_gui(obj_gui)
        obj_gui.set_gui_dcc_obj(dcc_comp_obj, namespace='dcc')
        return obj_gui


class AbsSceneMethodRunnerPanel(
    prx_widgets.PrxToolWindow,
    utl_gui_pnl_abstract.AbsGuiMethodDef,
    AbsTaskMethodObjGuiDef
):
    PANEL_KEY = 'scene_method_runner'
    DCC_OBJ_CLASS = None
    OBJ_COMP_CLASS = None
    #
    DCC_SELECTION_CLS = None
    #
    DESCRIPTION_INDEX = 2
    def __init__(self, *args, **kwargs):
        super(AbsSceneMethodRunnerPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_gui_core.PanelsConfigure().get_window(
            self.PANEL_KEY
        )
        self.set_window_title(
            self._window_configure.get('name')
        )
        self.set_definition_window_size(
            self._window_configure.get('size')
        )
        self.get_log_bar().set_expanded(True)
        #
        self._set_gui_method_def_init_()
        #
        self._set_panel_build_()

        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_refresh_all_()

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()
        #
        self._check_button = prx_widgets.PrxPressItem()
        self._check_button.set_icon_by_text('Check')
        self._check_button.set_name('Check')
        self.set_button_add(self._check_button)
        self._check_button.set_press_clicked_connect_to(self._set_checked_methods_check_run_)
        #
        self._repair_button = prx_widgets.PrxPressItem()
        self._repair_button.set_icon_by_text('Repair')
        self._repair_button.set_name('Repair')
        self.set_button_add(self._repair_button)
        self._repair_button.set_press_clicked_connect_to(self._set_checked_methods_repair_run_)
        #
        self._export_button = prx_widgets.PrxPressItem()
        self._export_button.set_icon_by_text('Export')
        self._export_button.set_name('Export')
        self.set_button_add(self._export_button)
        self._export_button.set_press_clicked_connect_to(self._set_checked_methods_export_run_)

    def _set_viewer_groups_build_(self):
        # viewer
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        self._tree_viewer = prx_widgets.PrxTreeView()
        expand_box_0.set_widget_add(self._tree_viewer)
        self._tree_viewer.set_header_view_create(
            [('Name(s)', 2), ('Type(s)', 2), ('Description(s)', 2)],
            self.get_definition_window_size()[0] - 16
        )
        self._tree_viewer.set_item_select_changed_connect_to(self._set_dcc_obj_select_)

    def _set_configure_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Configure(s)')
        expand_box_0.set_expanded(True)
        expand_box_0.set_size_mode(1)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._configure_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._configure_gui.widget)
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxStringPort('work_scene_src_file_path', 'Work-Scene-src-file')
        )
        _port.set_use_as_storage()
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('scene_src_file_path', 'Scene-src-file')
        )
        _port.set_use_as_storage()
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('scheme', 'Scheme')
        )
        _port.set(
            [
                # 'work',
                'publish'
            ]
        )
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('version', 'Version')
        )
        _port.set(['latest', 'new'])
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxButtonPort('refresh', 'Refresh')
        )
        _port.set(self._set_refresh_all_)

    def _set_dcc_obj_select_(self):
        if self.DCC_SELECTION_CLS is not None:
            tree_viewer = self._tree_viewer
            dcc_paths = []
            qt_tree_items = tree_viewer._get_selected_items_()
            for qt_tree_item in qt_tree_items:
                gui_proxy = qt_tree_item.gui_proxy
                dcc_obj = gui_proxy.get_gui_dcc_obj(namespace='dcc')
                if dcc_obj is not None:
                    dcc_paths.append(dcc_obj.path)
            if dcc_paths:
                self.DCC_SELECTION_CLS(dcc_paths).set_all_select()
            else:
                self.DCC_SELECTION_CLS.set_clear()

    def _set_obj_check_result_build_(self, method, method_obj_gui):
        method_obj_gui.set_children_clear()
        for obj_path, v in method.check_results.value.items():
            check_tags = method.get_obj_check_tags(obj_path)
            #
            dcc_obj = self.DCC_OBJ_CLASS(obj_path)
            dcc_obj_gui = self._set_item_prx_add_(
                dcc_obj, obj_gui_parent=method_obj_gui
            )
            dcc_obj_gui.check_state.set(check_tags)
            dcc_obj_gui.set_name(
                method.get_obj_check_description(obj_path), column=self.DESCRIPTION_INDEX
            )
            for index, result in v.items():
                i_check_tag = result['check_tag']
                file_paths = method.get_obj_files_check_result_at(obj_path, index)
                self._set_obj_files_check_result_build_(method, index, dcc_obj_gui, file_paths, i_check_tag)
                #
                comp_names = method.get_obj_comps_check_result_at(obj_path, index)
                self._set_obj_comps_check_result_build_(method, index, dcc_obj_gui, comp_names, i_check_tag)
        #
        method_obj_gui.set_tool_tip(
            method.check_results.__str__(), self.DESCRIPTION_INDEX
        )

    def _set_obj_files_check_result_build_(self, method, index, dcc_obj_gui, file_paths, check_tag):
        for file_path in file_paths:
            if file_path is not None:
                file_obj = utl_dcc_objects.OsFile(file_path)
                file_obj_gui = self._set_file_obj_gui_add_(file_obj, obj_gui_parent=dcc_obj_gui)
                file_obj_gui.check_state.set(check_tag)
                file_obj_gui.set_name(
                    method.get_check_description_at(index), column=self.DESCRIPTION_INDEX
                )

    def _set_obj_comps_check_result_build_(self, method, index, dcc_obj_gui, comp_names, check_tag):
        for comp_name in comp_names:
            if comp_name is not None:
                dcc_obj = dcc_obj_gui.get_gui_dcc_obj(namespace='dcc')
                dcc_comp_obj = self.OBJ_COMP_CLASS(dcc_obj, comp_name)
                dcc_comp_obj_gui = self._set_comp_obj_gui_add_(dcc_comp_obj, obj_gui_parent=dcc_obj_gui)
                dcc_comp_obj_gui.check_state.set(check_tag)
                dcc_comp_obj_gui.set_name(
                    method.get_check_description_at(index), column=self.DESCRIPTION_INDEX
                )

    def _get_checked_method_args_(self):
        lis = []
        for item_prx in self._tree_viewer.get_all_items():
            if item_prx.get_is_checked() is True:
                obj = item_prx.get_gui_dcc_obj(namespace='method')
                if obj is not None:
                    lis.append((item_prx, obj))
        return lis

    def _set_checked_methods_check_run_(self):
        if self._methods_loader is not None:
            checked_method_paths = [obj.path for obj_gui, obj in self._get_checked_method_args_()]
            if checked_method_paths:
                method_obj_paths = self._methods_loader.get_sorted_objs(checked_method_paths)
                p = self.set_progress_create(len(method_obj_paths))
                for method_path in method_obj_paths:
                    p.set_update()
                    #
                    method_obj = self._methods_loader.get_obj(method_path)
                    if method_obj is not None:
                        method_obj_gui = method_obj.get_obj_gui()
                        method = self._methods_loader.get_method(method_path)
                        if method is not None:
                            method.set_check_rest()
                            method._set_check_debug_run_()
                            method.set_check_result_update(self._task_properties)
                            check_tags = method.get_check_tags()
                            method_obj_gui.check_state.set(check_tags)
                            self._set_obj_check_result_build_(method, method_obj_gui)
                #
                p.set_stop()
            #
            self._root_obj_gui.set_tool_tip(
                self._task_properties.get_str_as_yaml_style()
            )

    def _set_checked_methods_repair_run_(self):
        if self._methods_loader is not None:
            checked_method_paths = [obj.path for obj_gui, obj in self._get_checked_method_args_()]
            if checked_method_paths:
                method_obj_paths = self._methods_loader.get_sorted_objs(checked_method_paths)
                p = self.set_progress_create(len(method_obj_paths))
                for method_path in method_obj_paths:
                    p.set_update()
                    #
                    method_obj = self._methods_loader.get_obj(method_path)
                    if method_obj is not None:
                        method = self._methods_loader.get_method(method_path)
                        if method is not None:
                            method._set_repair_debug_run_()
                #
                p.set_stop()

    def _set_checked_methods_export_run_(self):
        if self._methods_loader is not None:
            checked_method_paths = [obj.path for obj_gui, obj in self._get_checked_method_args_()]
            if checked_method_paths:
                method_obj_paths = self._methods_loader.get_sorted_objs(checked_method_paths)
                #
                p = self.set_progress_create(len(method_obj_paths))
                for method_path in method_obj_paths:
                    p.set_update()
                    self._set_method_export_run_at_(method_path)
                #
                p.set_stop()

    def _set_method_export_run_at_(self, method_path):
        method_obj = self._methods_loader.get_obj(method_path)
        if method_obj is not None:
            method = self._methods_loader.get_method(method_path)
            if method is not None:
                method._set_export_debug_run_()

    def _get_task_properties_(self):
        self._resolver = rsv_commands.get_resolver()
        work_scene_src_file_path = self._configure_gui.get_port('work_scene_src_file_path').get()
        scheme = self._configure_gui.get_port('scheme').get()
        if work_scene_src_file_path:
            rsv_task = self._resolver.get_rsv_task_by_work_scene_src_file_path(file_path=work_scene_src_file_path)
            new_version = rsv_task.get_new_version(workspace='publish')
            work_task_properties = self._resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_scene_src_file_path)
            if work_task_properties:
                _port = self._configure_gui.get_port('scene_src_file_path')
                scene_src_file_paths = rsv_operators.RsvAssetSceneQuery(work_task_properties).get_src_file(
                    workspace='publish',
                    version='all'
                )
                _port.set(scene_src_file_paths)
                new_scene_src_file_path = rsv_operators.RsvAssetSceneQuery(work_task_properties).get_src_file(
                    workspace='publish',
                    version=new_version
                )
                if new_scene_src_file_path:
                    _port.set_append(new_scene_src_file_path)
                    _port.set_current(new_scene_src_file_path)
                    self._task_properties = self._resolver.get_task_properties_by_any_scene_file_path(new_scene_src_file_path)
                    if self._task_properties is not None:
                        self._task_properties.set('option.scheme', scheme)
                    else:
                        self._task_properties = None
                else:
                    self._task_properties = None
            else:
                self._task_properties = None
        else:
            self._task_properties = None

    def _set_properties_update_(self):
        scheme = self._configure_gui.get_port('scheme').get()
        #
        if scheme == 'work':
            version = self._task_properties.get('version')
            self._task_properties.set('option.workspace', 'work')
            self._task_properties.set('option.version', version)
        elif scheme == 'publish':
            self._task_properties.set('option.workspace', 'publish')
            version_scheme = self._configure_gui.get_port('version').get()
            version = self._resolver.get_task_publish_version(self._task_properties, version_scheme)
            self._task_properties.set('option.version', version)

    def _set_method_obj_guis_build_(self):
        tree_viewer = self._tree_viewer
        method_obj_paths = self._method_obj_paths
        #
        tree_viewer.set_clear()
        if method_obj_paths:
            root_obj = self._methods_loader.get_root_obj()
            root_obj.properties = self._task_properties
            self._root_obj_gui = self._set_method_group_obj_gui_add_(root_obj, tree_viewer=tree_viewer)
            self._root_obj_gui.set_checked(True)
            self._root_obj_gui.set_expanded(True)
            p_0 = self.set_progress_create(len(method_obj_paths))
            for i_method_path in method_obj_paths:
                p_0.set_update()
                i_method = self._methods_loader.get_obj(i_method_path)
                if i_method is not None:
                    method_obj_gui = self._set_method_unit_obj_gui_add_(i_method, self._root_obj_gui)
                    method_obj_gui.set_checked(True)
                    method_obj_gui.set_expanded(True)
                else:
                    utl_core.Log.set_module_warning_trace(
                        'method-gui-build',
                        'method-obj="{}" is Non-exists'.format(i_method_path)
                    )
            #
            p_0.set_stop()

    def _set_refresh_all_(self):
        self._method_obj_paths = []
        self._get_task_properties_()
        if self._task_properties is not None:
            # self._set_properties_update_()
            #
            if utl_core.System.get_user_name() == 'dongchangbao':
                utl_core.Environ.set_td_enable(True)
            #
            self._methods_loader = utl_fnc_objects.TaskMethodsLoader(self._task_properties)
            entity_path = self._methods_loader.get_entity_obj_path()
            #
            self._method_obj_paths = self._methods_loader.get_entity_method_obj_paths(entity_path)
            self._set_method_obj_guis_build_()
        else:
            self._methods_loader = None
