# coding:utf-8
import collections

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

import lxutil.dcc.dcc_operators as utl_dcc_operators

from lxutil_gui.panel import utl_gui_pnl_abstract

from lxutil_gui import utl_gui_core

import lxutil_gui.proxy.operators as utl_prx_operators


class AbsScenePackagerPanel(
    prx_widgets.PrxToolWindow,
    utl_gui_pnl_abstract.AbsObjGuiDef,
):
    PANEL_KEY = 'scene_package'
    #
    DCC_SELECTION_CLS = None
    DCC_NAMESPACE = 'dcc'
    #
    DSC_IDX_PORT = 1
    def __init__(self, *args, **kwargs):
        super(AbsScenePackagerPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_gui_core.PanelsConfigure().get_window(
            self.PANEL_KEY
        )
        self.set_window_title(
            self._window_configure.get('name')
        )
        self.set_definition_window_size(
            self._window_configure.get('size')
        )
        #
        self._is_tree_mode = False
        #
        self.set_panel_build()
        # self._set_op_wdt_0_build_()
        self._set_op_wgt_1_build_()
        self._set_op_wgt_2_build_()
        self._set_op_wgt_3_build_()
        #
        self._os_obj_gui_dict = collections.OrderedDict()
        #
        self._texture_references = None
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_refresh_all_()

    def _get_is_tree_mode_(self):
        return self._is_tree_mode

    def _set_tree_mode_switch_(self):
        self._is_tree_mode = not self._is_tree_mode

    def set_panel_build(self):
        self._viewer_menu = self.set_menu_add('Configure(s)')
        self._viewer_menu.set_menu_raw(
            [
                ('Tree-mode', None, (self._get_is_tree_mode_, self._set_tree_mode_switch_))
            ]
        )
        # viewer
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        #
        h_splitter_0 = prx_widgets.PrxHSplitter()
        expand_box_0.set_widget_add(h_splitter_0)
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.set_widget_add(self._filter_tree_viewer_0)
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.set_widget_add(self._obj_tree_viewer_0)
        h_splitter_0.set_stretches([1, 3])
        #
        self._set_filter_tree_view_build_()
        self._set_obj_tree_view_build_()
        #
        self._refresh_button_0 = prx_widgets.PrxPressItem()
        self._refresh_button_0.set_name('Refresh')
        self.set_button_add(self._refresh_button_0)
        self._refresh_button_0.set_press_clicked_connect_to(self._set_refresh_all_)

    def _set_filter_tree_view_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 16
        )

    def _set_obj_tree_view_build_(self):
        self._obj_tree_viewer_0.set_header_view_create(
            [('Name(s)', 4), ('Port(s)', 1)],
            self.get_definition_window_size()[0] * (3.0 / 4.0) - 16
        )
        self._obj_tree_viewer_0.set_gui_menu_raw(
            [
                ('Expand All', None, self._obj_tree_viewer_0.set_all_items_expand),
                ('Collapse All', None, self._obj_tree_viewer_0.set_all_items_collapse),
                (),
                ('Checked Exists', None, None),
                ('Checked Non-exists', None, None),
            ]
        )
        #
        self._prx_stg_obj_tree_view_add_opt = utl_prx_operators.PrxStgObjTreeViewAddOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxStgObjTreeItem,
        )
        self._prx_dcc_obj_tree_view_add_opt = utl_prx_operators.PrxDccObjTreeViewAddOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxDccObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_selection_opt = utl_prx_operators.PrxDccObjTreeViewSelectionOpt(
            prx_tree_view=self._obj_tree_viewer_0,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )
        self._obj_tree_viewer_0.set_item_select_changed_connect_to(
            self._prx_dcc_obj_tree_view_selection_opt.set_select
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def _set_op_wdt_0_build_(self):
        # operator
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Operator')
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        attribute_box_0 = prx_widgets.PrxNode()
        qt_layout_0.addWidget(attribute_box_0.widget)
        #
        self._search_string_attribute = attribute_box_0.set_port_add(
            prx_widgets.PrxTextPort(
                'search_string', 'Search String'
            )
        )
        self._replace_string_attribute = attribute_box_0.set_port_add(
            prx_widgets.PrxTextPort(
                'replace_string', 'Replace String'
            )
        )
        self._replace_start_attribute = attribute_box_0.set_port_add(
            prx_widgets.PrxEnumeratePort(
                'replace_with', 'Replace With'
            )
        )
        self._replace_start_attribute.set(['replace with start', 'replace with all'])
        #
        qt_action_widget_0 = qt_widgets.QtWidget()
        qt_layout_0.addWidget(qt_action_widget_0)
        qt_action_layout_0 = qt_widgets.QtHBoxLayout(qt_action_widget_0)
        #
        self._preview_button_0 = qt_widgets.QtPressButton()
        qt_action_layout_0.addWidget(self._preview_button_0)
        self._preview_button_0.setText('Preview')
    # package
    def _set_op_wgt_1_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Package')
        expand_box_0.set_size_mode(1)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._package_node_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._package_node_gui.widget)
        #
        _port = self._package_node_gui.set_port_add(
            prx_widgets.PrxTextPort('target_directory', 'Target-directory')
        )
        _port.set('/data/package_temporary')
        #
        _port = self._package_node_gui.set_port_add(
            prx_widgets.PrxBooleanPort('ignore_structure', 'Ignore-structure')
        )
        _port.set(False)
        #
        _port = self._package_node_gui.set_port_add(
            prx_widgets.PrxBooleanPort('repath', 'Repath')
        )
        _port.set_enable(False)
        #
        _port = self._package_node_gui.set_port_add(
            prx_widgets.PrxButtonPort('package_file', 'Package-file(s)')
        )
        _port.set(self.set_package)
    # search
    def _set_op_wgt_2_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Search')
        expand_box_0.set_size_mode(1)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._search_node_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._search_node_gui.widget)
        #
        _port = self._search_node_gui.set_port_add(
            prx_widgets.PrxTextPort('target_directory', 'Target-directory')
        )
        _port = self._search_node_gui.set_port_add(
            prx_widgets.PrxBooleanPort('ignore_source_resolved', 'Ignore-source-resolved')
        )
        _port.set(True)
        _port = self._search_node_gui.set_port_add(
            prx_widgets.PrxButtonPort('search_file', 'Search-file(s)')
        )
        _port.set(self.set_search)
    # copy & repath
    def _set_op_wgt_3_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Copy & Repath')
        expand_box_0.set_size_mode(1)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._copy_and_repath_node_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._copy_and_repath_node_gui.widget)
        #
        _port = self._copy_and_repath_node_gui.set_port_add(
            prx_widgets.PrxTextPort('target_directory', 'Target-directory')
        )
        _port = self._copy_and_repath_node_gui.set_port_add(
            prx_widgets.PrxButtonPort('copy_and_repath_file', 'Copy & repath-file(s)')
        )
        _port.set(self.set_copy_and_repath)

    def _set_dcc_obj_select_(self):
        if self.DCC_SELECTION_CLS is not None:
            paths = []
            qt_tree_items = self._obj_tree_viewer_0._get_selected_items_()
            for qt_tree_item in qt_tree_items:
                gui_proxy = qt_tree_item.gui_proxy
                if isinstance(gui_proxy, prx_widgets.PrxDccObjTreeItem):
                    dcc_obj = gui_proxy.get_gui_attribute('dcc_obj')
                    if dcc_obj is not None:
                        paths.append(dcc_obj.path)
            if paths:
                self.DCC_SELECTION_CLS(paths).set_all_select()
            else:
                self.DCC_SELECTION_CLS.set_clear()

    def set_package(self):
        target_directory = self._package_node_gui.get_port('target_directory').get()
        ignore_structure = self._package_node_gui.get_port('ignore_structure').get()
        os_objs = self._get_checked_os_objs_()
        p = self.set_progress_create(len(os_objs))
        for file_plf_obj in os_objs:
            p.set_update()
            if file_plf_obj.get_is_file():
                for i in file_plf_obj.get_exists_files():
                    i.set_copy_to(target_directory, ignore_structure)
        p.set_stop()

    def set_search(self):
        target_directory = self._search_node_gui.get_port('target_directory').get()
        ignore_source_resolved = self._search_node_gui.get_port('ignore_source_resolved')
        target_directory_paths = [
            i.lstrip().rstrip() for i in target_directory.split(',')
        ]
        if self._texture_references is not None:
            if target_directory_paths:
                utl_dcc_operators.DccTexturesOpt(
                    self._texture_references
                ).set_search_from(
                    target_directory_paths=target_directory_paths,
                    ignore_source_resolved=ignore_source_resolved
                )
        #
        self._set_refresh_all_()

    def set_copy_and_repath(self):
        target_directory = self._copy_and_repath_node_gui.get_port('target_directory').get()
        if self._texture_references is not None:
            if target_directory:
                utl_dcc_operators.DccTexturesOpt(
                    self._texture_references
                ).set_copy_and_repath_to(target_directory)
        #
        self._set_refresh_all_()

    def _get_checked_os_objs_(self):
        lis = []
        item_prxes = self._prx_stg_obj_tree_view_add_opt._obj_add_dict.values()
        for v in item_prxes:
            if v.get_is_checked() is True:
                storage_obj = v.get_gui_dcc_obj(namespace='storage-file')
                if storage_obj is not None:
                    lis.append(storage_obj)
        return lis

    def _set_file_references_update_(self):
        self._texture_references = None
        self._file_references = None

    def _set_file_guis_refresh_(self):
        self._prx_stg_obj_tree_view_add_opt.set_restore()
        if self._file_references is not None:
            dcc_objs = self._file_references.get_objs()
            if dcc_objs:
                self._os_file_tree_item_dict = {}
                gp_0 = utl_core.GuiProgressesRunner(maximum=len(dcc_objs))
                for dcc_obj in dcc_objs:
                    gp_0.set_update()
                    stg_files = dcc_obj.get_file_objs()
                    if stg_files:
                        for stg_file in stg_files:
                            is_create, stg_file_item_prx = self._prx_stg_obj_tree_view_add_opt.set_prx_item_add_as(stg_file, mode='list')
                            stg_file_item_prx.set_gui_dcc_obj(stg_file, namespace='storage-file')
                            #
                            dcc_node_item_prx = self._prx_dcc_obj_tree_view_add_opt._set_prx_item_add_(
                                dcc_obj,
                                stg_file_item_prx,
                                name_use_path_prettify=False
                            )
                            dcc_node_item_prx.set_name(
                                stg_file.get_dcc_attribute_name(), self.DSC_IDX_PORT
                            )
                            # filter-ext
                            filter_ext = stg_file.type
                            #
                            ext_key = 'ext.{}'.format(filter_ext)
                            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                                ext_key, dcc_node_item_prx
                            )
                            # filter-state
                            if stg_file.get_is_exists() is True:
                                filter_state = 'resolved'
                            else:
                                filter_state = 'unresolved'
                            #
                            state_key = 'state.{}'.format(filter_state)
                            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                                state_key, dcc_node_item_prx
                            )
                #
                gp_0.set_stop()
                #
                self._obj_tree_viewer_0.set_items_expand_by_depth(depth=2)

    def _set_refresh_all_(self):
        self._set_file_references_update_()
        self._set_file_guis_refresh_()
        #
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()
