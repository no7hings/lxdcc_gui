# coding:utf-8
import collections

from lxutil_gui import utl_gui_configure

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

from lxobj import obj_core, core_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui.proxy import utl_gui_prx_core

from lxutil_prd import utl_prd_configure, utl_prd_commands


class AbsObjGuiDef(object):
    UTL_OBJ_CLASS = None
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
            obj_gui = tree_view_gui.set_item_add(
                **_kwargs
            )
            item_dict[obj_path] = obj_gui
            return obj_gui
        else:
            if parent_obj_path in item_dict:
                parent_gui = item_dict[parent_obj_path]
                obj_gui = parent_gui.set_child_add(
                    **_kwargs
                )
                item_dict[obj_path] = obj_gui
                return obj_gui
    @classmethod
    def _set_prx_item_add_(cls, dcc_obj, parent_obj_gui):
        dcc_obj_gui = parent_obj_gui.set_child_add(
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
        utl_obj = cls.UTL_OBJ_CLASS(obj_path)
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
            obj_gui = parent_gui.set_child_add(
                **_kwargs
            )
            item_dict[utl_obj.path] = obj_gui
            return obj_gui
        else:
            obj_gui = tree_view_gui.set_item_add(
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


class AbsUtilToolPanel(prx_widgets.PrxToolWindow):
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
    prx_widgets.PrxToolWindow,
):
    DCC_SELECTION_CLS = None
    DCC_OBJ_CLASS = None
    #
    OBJ_OP_CLASS = None
    OP_REFERENCE_OBJ_CLASS = None
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
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        self._tree_viewer = prx_widgets.PrxTreeView()
        expand_box_0.set_widget_add(self._tree_viewer)
        self._tree_viewer.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 2), ('Instance(s)', 2), ('Version(s)', 2), ('Data(s)', 2), ('Description(s)', 4)],
            self.get_definition_window_size()[0] - 16
        )
        self._tree_viewer.set_item_select_changed_connect_to(self._set_dcc_obj_select_)
        self._tree_viewer.set_gui_menu_raw(
            [
                [
                    'Main', None,
                    [
                        ('Log', None, self.set_log_unit_show),
                        ('Help', None, self.set_help_unit_show)
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
        self.set_button_add(self._refresh_button_0)
        self._refresh_button_0.clicked.connect(self.set_refresh)

        self._repair_button = qt_widgets.QtPressButton()
        self._repair_button.setText('Repair')
        self.set_button_add(self._repair_button)
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
                self.DCC_SELECTION_CLS(paths).set_all_select()
            else:
                self.DCC_SELECTION_CLS.set_clear()

    def _set_dcc_groups_add_(self, obj_opt, prod_obj_gui):
        dcc_group_paths = obj_opt.get_dcc_group_paths()
        dcc_objs = [self.DCC_OBJ_CLASS(i) for i in dcc_group_paths]
        for dcc_obj in dcc_objs:
            obj_gui = prod_obj_gui.set_child_add(
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
            dcc_obj = self.DCC_OBJ_CLASS(dcc_name)
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
                _obj_gui = self._tree_viewer.set_item_add(
                    **_kwargs
                )
                self._gui_dict[obj_op_.path] = _obj_gui
                return _obj_gui
            else:
                _parent_path = _parent.path
                if _parent_path in self._gui_dict:
                    parent_gui = self._gui_dict[_parent_path]
                    _obj_gui = parent_gui.set_child_add(
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
                    obj_opt = self.OBJ_OP_CLASS(obj)
                    reference_key = obj_opt.reference_key
                    if reference_key:
                        obj_opt = self.OP_REFERENCE_OBJ_CLASS(obj)
                    #
                    obj_gui = _set_gui_add(obj, obj_opt)
                    if obj_gui is not None:
                        self._set_dcc_path_check_(obj_opt, obj_gui)

        self._tree_viewer.set_all_items_expand()

    def set_repair_run(self):
        objs = self._scene.get_objs()
        for obj in objs:
            obj_opt = self.OBJ_OP_CLASS(obj)
            if not obj_opt.reference_key:
                dcc_path = obj_opt.dcc_path
                dcc_obj = self.DCC_OBJ_CLASS(dcc_path)
                dcc_obj.set_ancestors_create()

        for obj in objs:
            obj_opt = self.OBJ_OP_CLASS(obj)
            if obj_opt.reference_key == 'reference':
                dcc_name = obj_opt.dcc_name
                exists_dcc_obj = self.DCC_OBJ_CLASS(dcc_name)
                if exists_dcc_obj.get_is_exists() is True:
                    exists_path = exists_dcc_obj.path
                    dcc_path = obj_opt.dcc_path
                    if not exists_path == dcc_path:
                        parent_path = self.DCC_OBJ_CLASS(dcc_path).get_parent_path()
                        exists_dcc_obj.set_parent_path(parent_path)

        self.set_refresh()


class AbsShotBuildToolPanel(
    prx_widgets.PrxToolWindow,
):
    TOOL_PANEL_KEY = None
    TOOL_CONFIGURE = None
    #
    HELP_FILE_PATH = '{}/UPDATE.md'.format(utl_gui_configure.Root.doc)
    DCC_SELECTION_CLS = None
    #
    OBJ_OPT_CLASS = None
    SHOT_OPT_CLASS = None
    #
    CONTAINER_OPT_CLASS = None
    ELEMENT_CREATOR_CLASS = None
    #
    SCENE_OPT_CLASS = None
    #
    UTL_OBJ_CLASS = None
    DCC_OBJ_CLASS = None
    #
    GUI_DISPLAY_INDEX = 2
    GUI_RENDER_INDEX = 3
    GUI_DSC_INDEX = 4
    #
    FILTER_SCHEME_OVERRIDE = None
    def __init__(self, file_path, *args, **kwargs):
        super(AbsShotBuildToolPanel, self).__init__(*args, **kwargs)
        self.set_window_title(
            self.TOOL_CONFIGURE.get('tool.{}.label'.format(self.TOOL_PANEL_KEY))
        )
        self.set_definition_window_size(
            self.TOOL_CONFIGURE.get('tool.{}.size'.format(self.TOOL_PANEL_KEY))
        )
        #
        self._file_path = file_path
        #
        self.set_definition_window_size((1280, 960))
        #
        self._filter_enable_dict = {
            'custom': {

            },
            '/houdini/custom': {

            },
            '/maya/custom': {
                '/sot_efx': False,
                '/sot_har': False,
                '/sot_crd': False,
            },
            '/houdini/light': {
                '/sot_anm/gmt_abc/shape': False,
                '/sot_asb/gmt_abc/shape': False
            },
            '/maya/surface': {
                '/sot_anm/gmt_abc/shape': False,
                '/sot_asb/gmt_abc/shape': False,
                '/sot_efx': False,
                '/sot_har': False,
                '/sot_crd': False,
            }
        }
        #
        self._filter_scheme = 'custom'
        if self.FILTER_SCHEME_OVERRIDE is not None:
            self._filter_scheme = self.FILTER_SCHEME_OVERRIDE
        #
        self._filter_gui_dict = collections.OrderedDict()
        self._shot_gui_dict = collections.OrderedDict()
        self._shot_opts = []
        self._container_gui_dict = collections.OrderedDict()
        self._manifest_opt_dict = collections.OrderedDict()
        self._element_opt_dict = collections.OrderedDict()
        #
        self.set_panel_build()
        self.set_option_build()
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def set_panel_build(self):
        self._tool_menu = self.set_menu_add('Tool(s)')
        self._tool_menu.set_menu_raw(
            [
                ('Guess', None, self._set_guess_)
            ]
        )
        # viewer
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        h_splitter_0 = prx_widgets.PrxHSplitter()
        expand_box_0.set_widget_add(h_splitter_0)
        # filter
        v_splitter_0_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.set_widget_add(v_splitter_0_0)
        self._shot_tree_view_gui = prx_widgets.PrxTreeView()
        v_splitter_0_0.set_widget_add(self._shot_tree_view_gui)
        #
        self._filter_tree_view_gui_0 = prx_widgets.PrxTreeView()
        v_splitter_0_0.set_widget_add(self._filter_tree_view_gui_0)
        v_splitter_0_0.set_stretches([1, 1])
        # main
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.set_widget_add(self._obj_tree_viewer_0)
        h_splitter_0.set_stretches([1, 2])
        # h_splitter_0.set_sizes([0, self.get_definition_window_size()[0]])
        #
        self._load_button_0 = qt_widgets.QtPressButton()
        self._load_button_0.setText('Load')
        self.set_button_add(self._load_button_0)
        self._load_button_0.clicked.connect(self._set_containers_gui_build_)
        #
        self._build_button_0 = qt_widgets.QtPressButton()
        self._build_button_0.setText('Build')
        self.set_button_add(self._build_button_0)
        self._build_button_0.clicked.connect(self._set_dcc_objs_build_)
        #
        self._set_filter_viewer_build_()
        self._set_shot_viewer_build_()
        self._set_container_viewer_build_()

    def _set_filter_viewer_build_(self):
        self._filter_tree_view_gui_0.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 1), ('Count(s)', 1)],
            self.get_definition_window_size()[0] * (1.0 / 3.0) - 16
        )

    def _set_shot_viewer_build_(self):
        self._shot_tree_view_gui.set_header_view_create(
            [('Name(s)', 4), ('Type(s)', 2)],
            self.get_definition_window_size()[0] * (1.0 / 3.0) - 16
        )

    def _set_container_viewer_build_(self):
        self._obj_tree_viewer_0.set_header_view_create(
            [('Name(s)', 6), ('Type(s)', 1), ('Display(s)', 1), ('Render(s)', 1), ('Description(s)', 2)],
            self.get_definition_window_size()[0] * (2.0 / 3.0) - 16
        )
        self._obj_tree_viewer_0.set_item_select_changed_connect_to(self._set_dcc_obj_select_)
        self._obj_tree_viewer_0.set_gui_menu_raw(
            [
                [
                    'Main', None,
                    [
                        ('Log', None, self.set_log_unit_show),
                        ('Help', None, self.set_help_unit_show)
                    ]
                ],
                (),
                ('Expand All', None, self._obj_tree_viewer_0.set_all_items_expand),
                ('Collapse All', None, self._obj_tree_viewer_0.set_all_items_collapse),
                (),
                ('Select all', None, None),
                ('Select clear', None, None)
            ]
        )

    def set_option_build(self):
        self._package_node_gui = prx_widgets.PrxNode()
        #
        option_layout = self.get_option_unit_layout()
        option_layout.addWidget(self._package_node_gui.widget)
        #
        _port = self._package_node_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('filter_scheme', 'Filter-scheme')
        )
        _port.set(self._filter_enable_dict.keys())

    def _set_dcc_obj_select_(self):
        if self.DCC_SELECTION_CLS is not None:
            paths = []
            qt_tree_items = self._obj_tree_viewer_0._get_selected_items_()
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

    def _set_guess_(self):
        if self._current_shot is not None:
            from lxutil import scripts
            shot_name = self._current_shot.name
            r = scripts.ShotReader(shot_name)
            fs = r.scene_file_paths
            if fs:
                f = fs[-1]
                r.set_manifest_create(f)

        self._set_tool_panel_setup_()

    def _set_scene_build_(self):
        self._scene_opt = self.SCENE_OPT_CLASS(project='cg7', stage='publish')
        self._scene = self._scene_opt.scene
        utl_prd_commands.set_current_scene(self._scene)
        self._scene_opt.set_shots_build()
        #
        project = self._scene.get_current_project_obj()
        self.set_window_title(project.__str__())

    def _set_tool_panel_setup_(self):
        self._current_shot = None
        #
        self._set_scene_build_()
        #
        self._scene.set_load_by_scene_file_path(self._file_path)
        #
        current_shot_obj = self._scene.get_current_entity_obj()
        if current_shot_obj:
            if current_shot_obj.type.name == utl_prd_configure.ObjType.SHOT:
                self._current_shot = self.SHOT_OPT_CLASS(current_shot_obj)
                self.set_window_title(self._current_shot.__str__())
        #
        self._set_shots_gui_build_()
        self.set_window_loading_end()
        #
        self._set_refresh_all_()
    #
    def _set_shots_gui_build_(self):
        self._shot_tree_view_gui.set_clear()
        self._shot_gui_dict = collections.OrderedDict()
        self._manifest_opt_dict = collections.OrderedDict()
        #
        self._shot_opts = self._scene_opt.get_shot_opts()
        if self._shot_opts:
            p = self.set_progress_create(len(self._shot_opts))
            for seq, shot_opt in enumerate(self._shot_opts):
                p.set_update()
                if self._current_shot is not None:
                    if shot_opt.path != self._current_shot.path:
                        continue
                #
                all_parent_paths = shot_opt.obj.get_ancestor_paths()
                all_parent_paths.reverse()
                for obj_path in all_parent_paths:
                    obj = self._scene.universe.get_obj(obj_path)
                    if obj is not None:
                        obj_opt = self.OBJ_OPT_CLASS(obj)
                        obj_gui = self._set_prd_obj_gui_add_(
                            obj_opt,
                            self._shot_tree_view_gui,
                            self._shot_gui_dict
                        )
                    else:
                        obj_gui = self._set_utl_obj_gui_add_(
                            obj_path,
                            self._shot_tree_view_gui,
                            self._shot_gui_dict
                        )
                    #
                    obj_gui.set_checked(False)
                    obj_gui.set_expanded(True)
                #
                shot_gui = self._set_prd_obj_gui_add_(
                    shot_opt,
                    self._shot_tree_view_gui,
                    self._shot_gui_dict
                )
                #
                shot_gui.set_gui_attribute('shot_opt', shot_opt)
            p.set_stop()

    def _set_manifests_gui_build_(self):
        if self._current_shot is not None:
            shot_opts = [self._current_shot]
        else:
            shot_opts = self._shot_opts
        s = self._scene
        universe = s.universe
        manifest_type = universe.get_obj_type(utl_prd_configure.ObjType.MANIFEST)
        manifest_schemes = manifest_type.get_variant('schemes')
        for shot_opt in shot_opts:
            shot_opt.set_manifests_build()
            for manifest_scheme in manifest_schemes:
                manifest_opts = shot_opt.get_manifest_opts(manifest_scheme)
                if manifest_opts:
                    manifest_opt = manifest_opts[-1]
                    all_parent_paths = manifest_opt.obj.get_ancestor_paths()
                    all_parent_paths.reverse()
                    for obj_path in all_parent_paths:
                        obj = self._scene.universe.get_obj(obj_path)
                        if obj is not None:
                            obj_opt = self.OBJ_OPT_CLASS(obj)
                            obj_gui = self._set_prd_obj_gui_add_(obj_opt, self._shot_tree_view_gui, self._shot_gui_dict)
                        else:
                            obj_gui = self._set_utl_obj_gui_add_(obj_path, self._shot_tree_view_gui, self._shot_gui_dict)

                        obj_gui.set_checked(False)
                    #
                    manifest_gui = self._set_prd_obj_gui_add_(
                        manifest_opt,
                        self._shot_tree_view_gui,
                        self._shot_gui_dict
                    )
                    manifest_gui.set_checked(False)
                    #
                    vsn_lst = manifest_opt.get_variant('self.manifest.vsn_lst')
                    vsn_key_lst, vsn_raw_lst = vsn_lst
                    manifest_gui.set_name(vsn_key_lst)
                    #
                    manifest_gui.set_gui_attribute('manifest_opt', manifest_opt)
                    #
                    menu_raw = self._get_prd_gui_menu_raw_(
                        manifest_opt, manifest_gui
                    )
                    manifest_gui.set_gui_menu_raw(menu_raw)
    #
    def _set_current_shot_gui_checked_(self):
        if self._current_shot is not None:
            shot_gui = self._shot_gui_dict[self._current_shot.path]
            shot_gui.set_checked(True, extra=True)
            shot_gui.set_expanded(True, ancestors=True)

    def _set_refresh_all_(self):
        self._set_manifests_gui_build_()
        self._set_current_shot_gui_checked_()
        #
        self._set_containers_gui_build_()
    #
    def _set_containers_gui_build_(self):
        self._obj_tree_viewer_0.set_clear()
        self._container_gui_dict = collections.OrderedDict()
        self._element_vsn_key_dict = collections.OrderedDict()
        #
        text_browser = self.get_log_text_browser()
        manifest_opts = self._get_checked_manifest_opts_()
        if manifest_opts:
            p = self.set_progress_create(len(manifest_opts))
            for manifest_opt in manifest_opts:
                p.set_update()
                vsn_key, vsn_raw = manifest_opt.vsn_key, manifest_opt.vsn_raw
                text_browser.set_result_add('build manifest-gui:\n- vsn_key={}\n- vsn_raw={}\n'.format(vsn_key, vsn_raw))
                manifest_opt.set_containers_build(progress_bar=self)
                self._set_per_manifest_containers_build_(manifest_opt)
            p.set_stop()
        #
        self._set_obj_guis_dcc_update_()

    def _set_per_manifest_containers_build_(self, manifest_opt):
        container_opts = manifest_opt.get_container_opts()
        if container_opts:
            p = self.set_progress_create(len(container_opts))
            for container_opt in container_opts:
                p.set_update()
                obj_paths = container_opt.obj.get_dag_component_paths()
                obj_paths.reverse()
                for obj_path in obj_paths:
                    if obj_path == container_opt.path:
                        container_gui = self._set_prd_obj_gui_add_(container_opt, self._obj_tree_viewer_0, self._container_gui_dict)
                        #
                        scheme = container_opt.get_variant('self.container.scheme')
                        data_scheme = container_opt.get_variant('self.container.data_scheme')
                        container_gui.set_gui_attribute(
                            'tag_filter_tgt_raw',
                            {
                                '{}.{}.variant'.format(scheme, data_scheme): container_opt.get_variant('self.container.variant')
                            }
                        )
                        container_gui.set_checked()
                        #
                        container_gui.set_gui_attribute('container_opt', container_opt)
                        #
                        self._set_element_gui_add_(container_opt, container_gui)
                    else:
                        obj = self._scene.universe.get_obj(obj_path)
                        if obj is not None:
                            obj_opt = self.OBJ_OPT_CLASS(obj)
                            obj_gui = self._set_prd_obj_gui_add_(obj_opt, self._obj_tree_viewer_0, self._container_gui_dict)
                        else:
                            obj_gui = self._set_utl_obj_gui_add_(obj_path, self._obj_tree_viewer_0, self._container_gui_dict)
                        obj_gui.set_checked()
                        obj_gui.set_expanded(True)
            p.set_stop()
    @classmethod
    def _get_prd_gui_menu_raw_(cls, prd_opt, prd_gui):
        def add_switch_fnc_(prd_opt_, vsn_):
            def fnc_():
                prd_gui.set_name(_vsn_key)
                prd_opt_.obj.set_variant('self.manifest.vsn', vsn_)
                #
                prd_opt_.obj.set_variant('self.manifest.vsn_key', _vsn_key)
                prd_opt_.obj.set_variant('self.manifest.vsn_raw', _vsn_raw)
            #
            def enable_fnc_():
                _vsn_key_cur = prd_opt_.get_variant('self.manifest.vsn_key')
                if _vsn_key == _vsn_key_cur:
                    return True
                return False
            #
            _vsn_key, _vsn_raw = vsn_
            #
            lis.append(
                (_vsn_key, None, (enable_fnc_, fnc_))
            )
        #
        def open_folder_fnc_():
            _vsn_raw_cur = prd_opt.get_variant('self.manifest.vsn_raw')
            if _vsn_raw_cur is not None:
                file_plf_obj = utl_dcc_objects.OsFile(_vsn_raw_cur)
                file_plf_obj.set_directory_open()

        lis = []
        vsn_all = prd_opt.get_variant('self.manifest.vsn_all')
        for vsn in vsn_all:
            add_switch_fnc_(prd_opt, vsn)
        #
        lis.extend(
            [
                (),
                ('Open Folder', 'file/folder', open_folder_fnc_)
            ]
        )

        return lis
    @classmethod
    def _set_prd_obj_gui_add_(cls, obj_opt, tree_view_gui, tree_item_gui_dict):
        paren_path = obj_opt.obj.get_parent_path()
        _path = obj_opt.path
        if _path in tree_item_gui_dict:
            return tree_item_gui_dict[_path]
        tool_tip = 'path: {}'.format(obj_opt.path)
        if hasattr(obj_opt, 'dcc_type'):
            tool_tip += '\ndcc-type: {}'.format(obj_opt.dcc_type)
        if hasattr(obj_opt, 'dcc_path'):
            tool_tip += '\ndcc-path: {}'.format(obj_opt.dcc_path)
        if hasattr(obj_opt, 'dcc_port'):
            tool_tip += '\nplf-file-dcc-port-name: {}'.format(obj_opt.dcc_port)
        #
        _kwargs = dict(
            name=(obj_opt.name, obj_opt.type),
            icon=obj_opt.icon,
            tool_tip=tool_tip,
            item_class=prx_widgets.PrxObjTreeItem,
        )
        if paren_path is None:
            obj_gui = tree_view_gui.set_item_add(
                **_kwargs
            )
            tree_item_gui_dict[obj_opt.path] = obj_gui
            return obj_gui
        else:
            if paren_path in tree_item_gui_dict:
                parent_gui = tree_item_gui_dict[paren_path]
                obj_gui = parent_gui.set_child_add(
                    **_kwargs
                )
                tree_item_gui_dict[obj_opt.path] = obj_gui
                return obj_gui
    @classmethod
    def _set_utl_obj_gui_add_(cls, obj_path, tree_view_gui, tree_item_gui_dict, icon_name=None):
        obj = cls.UTL_OBJ_CLASS(obj_path)
        if obj.path in tree_item_gui_dict:
            return tree_item_gui_dict[obj.path]

        if icon_name is not None:
            icon = utl_core.Icon.get(icon_name)
        else:
            icon = obj.icon

        _kwargs = dict(
            name=(obj.name, obj.type),
            icon=icon,
            tool_tip='path: {}'.format(obj.path),
            item_class=prx_widgets.PrxObjTreeItem,
        )
        parent_path = obj.get_parent_path()
        if parent_path in tree_item_gui_dict:
            parent_gui = tree_item_gui_dict[parent_path]
            obj_gui = parent_gui.set_child_add(
                **_kwargs
            )
            tree_item_gui_dict[obj.path] = obj_gui
            return obj_gui
        else:
            obj_gui = tree_view_gui.set_item_add(
                **_kwargs
            )
            tree_item_gui_dict[obj.path] = obj_gui
            return obj_gui
    #
    def _set_element_version_check_(self, prd_opt, element_gui):
        if self.ELEMENT_CREATOR_CLASS is not None:
            vsn_key_cur = prd_opt.get_variant('self.element.vsn_key')
            vsn_raw_cur = prd_opt.get_variant('self.element.vsn_raw')
            vsn_raw_lst = prd_opt.get_variant('self.element.vsn_raw_lst')
            #
            element_creator = self.ELEMENT_CREATOR_CLASS(prd_opt)
            vsn_raw_atv = element_creator.get_crt_plf_file_path()
            if vsn_raw_atv is not None:
                if vsn_raw_atv != vsn_raw_cur:
                    if vsn_raw_atv in self._element_vsn_key_dict:
                        vsn_key_atv = self._element_vsn_key_dict[vsn_raw_atv]
                        element_gui.set_name(
                            '{} > {}'.format(vsn_key_atv, vsn_key_cur)
                        )
                    else:
                        element_gui.set_name(
                            '{} > {}'.format('unknown-file-path', vsn_key_cur)
                        )
                else:
                    element_gui.set_name(vsn_key_cur)
            else:
                element_gui.set_name(vsn_key_cur)
            #
            error_descriptions = []
            #
            if vsn_raw_cur != vsn_raw_lst:
                error_descriptions.append('Current-version is Not Last-version')
            if vsn_raw_atv is not None:
                if vsn_raw_atv != vsn_raw_lst:
                    error_descriptions.append('Active-version is Not Last-version')
            #
            if error_descriptions:
                element_gui.set_warning_state()
            else:
                element_gui.set_adopt_state()
            element_gui.set_name(error_descriptions, self.GUI_DSC_INDEX)
    # menu
    def _get_element_menu_raw_(self, element_opts, prd_gui):
        def add_switch_fnc_(prd_opt_, vsn_):
            def fnc_():
                prd_gui.set_name(_vsn_key)
                prd_opt_.obj.set_variant('self.element.vsn', vsn_)
                #
                prd_opt_.obj.set_variant('self.element.vsn_key', _vsn_key)
                prd_opt_.obj.set_variant('self.element.vsn_raw', _vsn_raw)
                prd_opt_.obj.set_variant('self.element.vsn_cmp_raw', _vsn_cmp_raw)
                #
                self._set_element_version_check_(prd_opt_, prd_gui)
            #
            def enable_fnc_():
                _vsn_key_cur = prd_opt_.get_variant('self.element.vsn_key')
                if _vsn_key == _vsn_key_cur:
                    return True
                return False
            #
            _vsn_key, _vsn_raw, _vsn_cmp_raw = vsn_
            #
            lis.append(
                (_vsn_key, None, (enable_fnc_, fnc_))
            )
        #
        def open_folder_fnc_():
            _vsn_raw_cur = prd_opt.get_variant('self.element.vsn_raw')
            if _vsn_raw_cur is not None:
                file_plf_obj = utl_dcc_objects.OsFile(_vsn_raw_cur)
                file_plf_obj.set_directory_open()
        #
        def load_current_fnc_():
            self._set_dcc_port_elements_build_(prd_opt, **build_kwargs)
            self._set_obj_element_dcc_update_(prd_opt, prd_gui)
        #
        def load_last_fnc():
            vsn_lst = prd_opt.get_variant('self.element.vsn_lst')
            prd_opt.obj.set_variant('self.element.vsn', vsn_lst)
            self._set_dcc_port_elements_build_(prd_opt, **build_kwargs)
            self._set_obj_element_dcc_update_(prd_opt, prd_gui)
        #
        lis = []
        prd_opt = element_opts[-1]
        vsn_all = prd_opt.get_variant('self.element.vsn_all')
        for vsn in vsn_all:
            vsn_key, vsn_raw, vsn_cmp_raw = vsn
            self._element_vsn_key_dict[vsn_raw] = vsn_key
            add_switch_fnc_(prd_opt, vsn)
        #
        build_kwargs = dict(ignore_display=True)
        lis.extend(
            [
                (),
                ('Load Current', 'load', load_current_fnc_),
                (),
                ('Load Last', 'load', load_last_fnc),
                (),
                ('Open Folder', 'file/folder', open_folder_fnc_)
            ]
        )
        return lis

    def _set_element_gui_add_(self, container_opt, container_gui):
        container_scheme = container_opt.scheme
        container_data_scheme = container_opt.data_scheme
        ett_brhs = container_opt.get_element_entity_branches()
        container_variant = container_opt.variant
        enables = []
        for ett_brh in ett_brhs:
            element_opts = container_opt.get_element_opts(ett_brh)
            if element_opts:
                enable = 1
                element_opt = element_opts[-1]
                element_gui = self._set_prd_obj_gui_add_(element_opt, self._obj_tree_viewer_0, self._container_gui_dict)
                element_gui.set_checked()
                #
                vsn_lst = element_opt.get_variant('self.element.vsn_lst')
                vsn_key_lst, vsn_raw_lst, vsn_cmp_raw_lst = vsn_lst
                element_gui.set_name(vsn_key_lst)
                #
                element_gui.set_gui_attribute('element_opt', element_opt)
                element_gui.set_gui_menu_raw(
                    self._get_element_menu_raw_(element_opts, element_gui)
                )
                element_gui.set_adopt_state()
            else:
                enable = 0
            #
            enables.append(enable)
        # validation
        if container_data_scheme in ['cmr_abc']:
            if sum(enables) == 0:
                container_gui.set_error_state()
                container_gui.set_name('Camera-alembic is Non-exists', self.GUI_DSC_INDEX)
            elif sum(enables) == 1:
                container_gui.set_adopt_state()
        # material-materialx
        elif container_data_scheme in ['mtl_mtx']:
            if sum(enables) == 0:
                container_gui.set_error_state()
                container_gui.set_name('Material-materialx is Non-exists', self.GUI_DSC_INDEX)
            elif sum(enables) == 1:
                container_gui.set_adopt_state()
        elif container_data_scheme in ['gmt_abc']:
            if container_scheme in ['sot_anm']:
                if sum(enables) == 0:
                    container_gui.set_error_state()
                    container_gui.set_name('Geometry-alembic is Non-exists', self.GUI_DSC_INDEX)
                elif sum(enables) == 1:
                    container_gui.set_error_state()
                    container_gui.set_name('Asset/Shot-geometry-alembic is Non-exists', self.GUI_DSC_INDEX)
                elif sum(enables) == 2:
                    container_gui.set_adopt_state()
            elif container_scheme in ['sot_asb']:
                if sum(enables) == 0:
                    container_gui.set_error_state()
                    container_gui.set_name('Asset/Shot-geometry-alembic is Non-exists', self.GUI_DSC_INDEX)
                elif sum(enables) == 1:
                    container_gui.set_adopt_state()
        elif container_data_scheme in ['plt_dta']:
            if sum(enables) == 0:
                container_gui.set_force_hidden()
            elif sum(enables) == 1:
                container_gui.set_adopt_state()
        elif container_data_scheme in ['har_xgn']:
            if sum(enables) == 0:
                container_gui.set_error_state()
                container_gui.set_name('Hair-xgen is Non-exists', self.GUI_DSC_INDEX)
            elif sum(enables) == 1:
                container_gui.set_error_state()
                container_gui.set_name('Asset-hair-xgen is Non-exists', self.GUI_DSC_INDEX)
            elif sum(enables) == 2:
                container_gui.set_adopt_state()
        elif container_data_scheme in ['xgn_glo_abc']:
            if sum(enables) == 0:
                container_gui.set_error_state()
                container_gui.set_name('Hair-glow-alembic is Non-exists', self.GUI_DSC_INDEX)
            elif sum(enables) == 1:
                container_gui.set_adopt_state()
        elif container_data_scheme in ['crd_abc']:
            if sum(enables) == 0:
                container_gui.set_error_state()
                container_gui.set_name('Crowd-alembic is Non-exists', self.GUI_DSC_INDEX)
            elif sum(enables) == 1:
                container_gui.set_adopt_state()
        elif container_data_scheme in ['hou_dta']:
            if sum(enables) == 0:
                container_gui.set_error_state()
                container_gui.set_name('Houdini-data is Non-exists', self.GUI_DSC_INDEX)
            elif sum(enables) == 1:
                container_gui.set_adopt_state()
        #
        if container_variant not in ['main', 'hi']:
            if sum(enables) == 0:
                container_gui.set_force_hidden()

    def _get_checked_shot_opts_(self):
        lis = []
        for k, v in self._shot_gui_dict.items():
            if v.get_is_hidden(ancestors=True) is True:
                continue
            if v.get_is_checked():
                obj_opt = v.get_gui_attribute('shot_opt')
                if obj_opt:
                    lis.append(obj_opt)
        return lis

    def _get_checked_manifest_opts_(self):
        lis = []
        for k, v in self._shot_gui_dict.items():
            if v.get_is_hidden(ancestors=True) is True:
                continue
            if v.get_is_checked():
                obj_opt = v.get_gui_attribute('manifest_opt')
                if obj_opt:
                    lis.append(obj_opt)
        return lis

    def _get_checked_element_opts_(self):
        lis = []
        for k, v in self._container_gui_dict.items():
            if v.get_is_hidden(ancestors=True) is True:
                continue
            if v.get_is_checked():
                obj_opt = v.get_gui_attribute('element_opt')
                if obj_opt:
                    lis.append(obj_opt)
        return lis

    def _set_dcc_port_elements_build_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_obj_gui_dcc_update_(self, obj_opt, obj_gui):
        dcc_path = obj_opt.dcc_path
        if dcc_path is not None:
            if self.DCC_OBJ_CLASS is not None:
                dcc_obj = self.DCC_OBJ_CLASS(dcc_path)
                if dcc_obj.get_is_exists() is True:
                    obj_gui.set_gui_attribute('dcc_obj', dcc_obj)
                    obj_gui.set_icon_by_file(dcc_obj.icon)

    def _set_obj_element_dcc_update_(self, element_opt, element_gui):
        self._set_obj_gui_dcc_update_(element_opt, element_gui)
        self._set_element_version_check_(element_opt, element_gui)
        #
        container = element_opt.container
        container_opt = self.CONTAINER_OPT_CLASS(container)
        container_gui = element_gui.get_parent()
        #
        self._set_obj_gui_dcc_update_(container_opt, container_gui)

    def _set_obj_guis_dcc_update_(self):
        for k, v in self._container_gui_dict.items():
            obj_gui = v
            obj_opts = obj_gui.get_custom_raws('element_opt')
            for obj_opt in obj_opts:
                self._set_obj_element_dcc_update_(obj_opt, obj_gui)

    def _set_dcc_objs_build_(self):
        self._set_dcc_pre_build_()
        #
        element_opts = self._get_checked_element_opts_()
        if element_opts:
            p = self.set_progress_create(len(element_opts))
            for element_opt in element_opts:
                p.set_update()
                self._set_dcc_port_elements_build_(element_opt)
            p.set_stop()

        self._set_obj_guis_dcc_update_()
        #
        self._set_dcc_pst_build_()

    def _set_dcc_pre_build_(self):
        pass

    def _set_dcc_pst_build_(self):
        pass


class AbsDccObjGuiDef(object):
    @classmethod
    def _set_prx_item_add_(cls, obj, obj_gui_parent=None, tree_viewer=None):
        kwargs = dict(
            name=(obj.name, obj.type.name),
            item_class=prx_widgets.PrxObjTreeItem,
            icon=obj.icon,
            tool_tip=obj.path
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
        return obj_gui
    @classmethod
    def _set_obj_connect_to_dcc_(cls, obj, obj_gui, is_shape):
        raise NotImplementedError()
