# coding:utf-8
from lxbasic import bsc_core

import lxutil_gui.qt.widgets as qt_widgets

from lxutil import utl_configure, utl_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.proxy.operators as utl_prx_operators

import lxutil.dcc.dcc_operators as utl_dcc_operators


def _set_texture_tx_create(window, item_prx, texture_references, includes, force, completed_fnc):
    def set_processing_update(time_cost):
        c = 'Load Texture-tx(s) [ {} ] [ {} ]'.format(
            str(p_m.get_status()),
            bsc_core.RawIntegerMtd.second_to_time_prettify(time_cost)
        )
        item_prx.set_name(c)

    def set_status_changed_update(status):
        c = 'Load Texture-tx(s) [ {} ] [ {} ]'.format(
            str(status),
            bsc_core.RawIntegerMtd.second_to_time_prettify(p_m.get_running_time_cost())
        )
        item_prx.set_name(c)
        item_prx.set_status(status)

    def set_element_status_changed_update(element_statuses):
        item_prx.set_statuses(element_statuses)

    def set_logging_update(text):
        pass
    #
    import lxbasic.objects as bsc_objects
    #
    textures_opt = utl_dcc_operators.DccTexturesOpt(
        texture_references,
        includes=includes,
    )
    create_process = textures_opt.set_tx_create(use_deferred=True, force=force)
    #
    # result_dict = utl_dcc_operators.DccTexturesOpt(
    #     texture_references,
    #     includes=includes,
    # ).set_tx_create_and_repath_use_thread(use_deferred=True, force=force)
    #
    # create_process = result_dict['tx-create']
    p_m = bsc_objects.ProcessMonitor(create_process)
    p_m.logging.set_connect_to(set_logging_update)
    p_m.processing.set_connect_to(set_processing_update)
    p_m.status_changed.set_connect_to(set_status_changed_update)
    p_m.element_statuses_changed.set_connect_to(set_element_status_changed_update)
    #
    window.set_window_close_connect_to(p_m.set_stop)
    if completed_fnc is not None:
        p_m.completed.set_connect_to(completed_fnc)
    #
    p_m.set_start()
    create_process.set_start()


def _set_texture_tx_repath(texture_references, includes):
    textures_opt = utl_dcc_operators.DccTexturesOpt(
        texture_references,
        includes=includes,
    )
    textures_opt.set_tx_repath()


def _set_texture_jpg_create(window, item_prx, texture_references, includes, force, completed_fnc):
    def set_processing_update(time_cost):
        c = '{} [ {} ] [ {} ]'.format(
            label,
            str(p_m.get_status()),
            bsc_core.RawIntegerMtd.second_to_time_prettify(time_cost)
        )
        item_prx.set_name(c)

    def set_status_changed_update(status):
        c = '{} [ {} ] [ {} ]'.format(
            label,
            str(status),
            bsc_core.RawIntegerMtd.second_to_time_prettify(p_m.get_running_time_cost())
        )
        item_prx.set_name(c)
        item_prx.set_status(status)

    def set_element_status_changed_update(element_statuses):
        item_prx.set_statuses(element_statuses)

    def set_logging_update(text):
        pass
        #

    import lxbasic.objects as bsc_objects
    #
    label = 'Load Texture-jpg(s)'
    #
    textures_opt = utl_dcc_operators.DccTexturesOpt(
        texture_references,
        includes=includes,
    )
    create_process = textures_opt.set_jpg_create(use_deferred=True, force=force)
    #
    p_m = bsc_objects.ProcessMonitor(create_process)
    p_m.logging.set_connect_to(set_logging_update)
    p_m.processing.set_connect_to(set_processing_update)
    p_m.status_changed.set_connect_to(set_status_changed_update)
    p_m.element_statuses_changed.set_connect_to(set_element_status_changed_update)
    #
    window.set_window_close_connect_to(p_m.set_stop)
    if completed_fnc is not None:
        p_m.completed.set_connect_to(completed_fnc)
    #
    p_m.set_start()
    create_process.set_start()


def _set_texture_jpg_repath(texture_references, includes):
    textures_opt = utl_dcc_operators.DccTexturesOpt(
        texture_references,
        includes=includes,
    )
    textures_opt.set_jpg_repath()


class AbsSceneTextureManagerPanel(
    prx_widgets.PrxToolWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/texture-manager'
    HELP_FILE_PATH = utl_configure.MainData.get_help_file('utility/panel/texture-manager')
    #
    DCC_SELECTION_CLS = None
    DCC_NAMESPACE = 'dcc'
    #
    ITEM_FRAME_SIZE = 96, 144
    ITEM_NAME_FRAME_SIZE = 48, 48
    #
    DSC_IDX_USED_COLORS_SPACE = 1
    DSC_IDX_COLORS_SPACE = 2
    def __init__(self, *args, **kwargs):
        super(AbsSceneTextureManagerPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_configure.MainData.get_as_configure(
            self.CONFIGURE_FILE_PATH
        )
        self.set_window_title(
            self._window_configure.get('window.name')
        )
        self.set_definition_window_size(
            self._window_configure.get('window.size')
        )
        #
        self._set_panel_build_()
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )
        #
        self._dcc_objs = []

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()
        #
        self._refresh_button_0 = prx_widgets.PrxPressItem()
        self._refresh_button_0.set_name('Refresh')
        self.set_button_add(self._refresh_button_0)
        self._refresh_button_0.set_press_clicked_connect_to(self._set_refresh_all_)

    def _set_tool_panel_setup_(self):
        self._set_refresh_all_()

    def _set_refresh_all_(self, includes=None):
        self._set_dcc_texture_references_update_()
        self._set_gui_texture_refresh_(includes)
        #
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def _set_viewer_groups_build_(self):
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
        #
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.set_widget_add(self._obj_tree_viewer_0)
        self._obj_list_viewer_0 = prx_widgets.PrxListView()
        h_splitter_0.set_widget_add(self._obj_list_viewer_0)
        #
        self._obj_list_viewer_0.set_item_frame_size(*self.ITEM_FRAME_SIZE)
        self._obj_list_viewer_0.set_item_name_frame_size(*self.ITEM_NAME_FRAME_SIZE)
        #
        self._obj_list_viewer_0.set_item_icon_frame_draw_enable(True)
        self._obj_list_viewer_0.set_item_name_frame_draw_enable(True)
        self._obj_list_viewer_0.set_item_image_frame_draw_enable(True)
        #
        h_splitter_0.set_stretches([2, 4, 4])
        #
        self._set_viewer_setup_()

    def _set_configure_groups_build_(self):
        self._set_tool_group_0_build_()
        self._set_tool_group_1_build_()
        self._set_tool_group_2_build_()

    def _set_tool_group_0_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Tool(s)')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._tool_node_prx = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._tool_node_prx.widget)
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('auto_switch_color_space', 'Auto Switch Color-space(s)')
        )
        _port.set_tool_tip(
            [
                'auto switch color-space for display (only supported for maya)',
                'more see menu-bar > Show(s) > Help'
            ]
        )
        _port.set(self.set_color_space_auto_switch)
        # tx-create
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxPortForBoolean('create_and_repath_to_tx_force', 'Create & Repath to tx(s) force', join_to_next=True)
        )
        _port.set_tool_tip(
            [
                'if is "on" create tx force however "texture-tx" is exists',
            ]
        )
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxSubProcessPort('create_and_repath_to_tx', 'Create & Repath to tx(s)', join_to_next=True)
        )
        _port.set_tool_tip(
            [
                'create new "texture-tx" and repath to "texture-tx"',
            ]
        )
        _port.set(self.set_tx_create_and_repath_use_thread)
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('repath_tx_to_orig', 'Repath tx(s) to Orig EXT')
        )
        _port.set_tool_tip(
            [
                'repath "texture-tx" to orig "ext", etc: "exr"',
            ]
        )
        _port.set(self.set_tx_repath_to_orig)
        # jpg-create
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxPortForBoolean('create_and_repath_to_jpg_force', 'Create & Repath to jpg(s) force', join_to_next=True)
        )
        _port.set_tool_tip(
            [
                'if is "on" create jpg force however "texture-tx" is exists',
            ]
        )
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxSubProcessPort('create_and_repath_to_jpg', 'Create & Repath to jpg(s)', join_to_next=True)
        )
        _port.set_tool_tip(
            [
                'create new "texture-tx" and repath to "texture-tx"',
            ]
        )
        _port.set(self.set_jpg_create_and_repath_use_thread)
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('repath_jpg_to_orig', 'Repath jpg(s) to Orig EXT')
        )
        _port.set_tool_tip(
            [
                'repath "texture-jpg" to orig "ext", etc: "exr"',
            ]
        )
        _port.set(self.set_jpg_repath_to_orig)
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('map_to_windows', 'Map to Platform')
        )
        _port.set(
            self.set_map_to_platform_platform
        )
    # search
    def _set_tool_group_1_build_(self):
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
            prx_widgets.PrxDirectoryOpenPort('target_directory', 'Target-directory')
        )
        _port = self._search_node_gui.set_port_add(
            prx_widgets.PrxPortForBoolean('ignore_source_resolved', 'Ignore Source-resolved')
        )
        _port.set(True)
        _port = self._search_node_gui.set_port_add(
            prx_widgets.PrxButtonPort('search', 'Search in Directory(s)')
        )
        _port.set_tool_tip(
            [
                'enter one or more path in "Target-directory" and press "Search in Directory(s)"',
                'sep is ",", etc: "/data/a, /data/b"'
            ]
        )
        _port.set(self.set_search)
    # copy & repath
    def _set_tool_group_2_build_(self):
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
            prx_widgets.PrxDirectoryOpenPort('target_directory', 'Target-directory')
        )
        _port = self._copy_and_repath_node_gui.set_port_add(
            prx_widgets.PrxButtonPort('copy_and_repath', 'Copy & Repath to target')
        )
        _port.set_tool_tip(
            [
                'enter one path in "Target-directory" and press "Copy & Repath to target"',
            ]
        )
        _port.set(self.set_copy_and_repath)

    def _set_viewer_setup_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0] * (1.0 / 4.0) - 20
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        #
        self._obj_tree_viewer_0.set_header_view_create(
            [('Name(s)', 2), ('Used-Color-space(s)', 1), ('Color-space(s)', 1)],
            self.get_definition_window_size()[0] * (3.0 / 4.0) - 40
        )
        #
        self._obj_tree_viewer_0.set_selection_use_single()
        #
        self._prx_stg_obj_tree_view_add_opt = utl_prx_operators.PrxStgTextureTreeViewAddOpt(
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
        self._obj_tree_viewer_0.set_item_select_changed_connect_to(
            self._set_stg_file_list_item_prxes_refresh_
        )

    def _set_gui_texture_refresh_(self, includes=None):
        self._prx_stg_obj_tree_view_add_opt.set_restore()
        if self._texture_references is not None:
            if includes:
                [self._texture_references._set_obj_reference_update_(i) for i in includes]
            else:
                self._dcc_objs = self._texture_references.get_objs()
            #
            if self._dcc_objs:
                with utl_core.gui_progress(maximum=len(self._dcc_objs), label='gui-add for texture') as g_p:
                    for i_dcc_obj in self._dcc_objs:
                        g_p.set_update()
                        i_files = i_dcc_obj.get_file_objs()
                        if i_files:
                            for j_file in i_files:
                                j_is_create, j_file_prx_item = self._prx_stg_obj_tree_view_add_opt.set_prx_item_add_as(
                                    j_file,
                                    mode='list',
                                    use_show_thread=True
                                )
                                if j_file_prx_item is not None:
                                    if j_is_create is True:
                                        if j_file.get_is_exists() is True:
                                            # tx_is_exists = j_file.get_is_exists_as_tx()
                                            # if tx_is_exists is True:
                                            #     j_file_prx_item.set_state(utl_gui_core.State.NORMAL)
                                            # else:
                                            #     j_file_prx_item.set_state(utl_gui_core.State.WARNING)
                                            #
                                            texture_color_space = j_file.get_color_space()
                                            j_file_prx_item.set_name(
                                                texture_color_space, self.DSC_IDX_COLORS_SPACE
                                            )
                                            j_file_prx_item.set_icon_by_name_text(
                                                texture_color_space, self.DSC_IDX_COLORS_SPACE
                                            )
                                            #
                                            texture_used_color_space = j_file.get_tx_color_space()
                                            j_file_prx_item.set_name(
                                                texture_used_color_space, self.DSC_IDX_USED_COLORS_SPACE
                                            )
                                            j_file_prx_item.set_icon_by_name_text(
                                                texture_used_color_space, self.DSC_IDX_USED_COLORS_SPACE
                                            )
                                    #
                                    i_dcc_prx_item = self._prx_dcc_obj_tree_view_add_opt._set_prx_item_add_2_(
                                        i_dcc_obj,
                                        j_file_prx_item
                                    )
                                    i_dcc_obj.set_obj_gui(i_dcc_prx_item)
                                    #
                                    ext = j_file.type
                                    ext_key = 'ext.{}'.format(ext)
                                    self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                                        ext_key, i_dcc_prx_item
                                    )
                                    #
                                    node_color_space = i_dcc_obj.get_color_space()
                                    color_space_key = 'color-space.{}'.format(node_color_space)
                                    self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                                        color_space_key, i_dcc_prx_item
                                    )
                                    #
                                    i_dcc_prx_item.set_name(
                                        node_color_space, self.DSC_IDX_USED_COLORS_SPACE
                                    )
                                    i_dcc_prx_item.set_icon_by_name_text(
                                        node_color_space, self.DSC_IDX_USED_COLORS_SPACE
                                    )
                #
                # self._obj_tree_viewer_0.set_items_expand_by_depth(depth=2)

    def _set_stg_file_list_item_prxes_refresh_(self):
        def set_show_fnc_(stg_file_, i_list_item_prx_):
            def show_fnc_():
                thumbnail_file_path = stg_file_.get_thumbnail_file_path()
                if thumbnail_file_path:
                    i_list_item_prx_.set_image(thumbnail_file_path)
                    i_list_item_prx_.set_names(
                        [stg_file_.name]
                    )
            #
            i_list_item_prx_.set_show_method(show_fnc_)
        #
        self._obj_list_viewer_0.set_clear()
        tree_item_prxes = self._obj_tree_viewer_0.get_selected_items()
        if tree_item_prxes:
            tree_item_prx = tree_item_prxes[-1]
            _ = tree_item_prx.get_gui_dcc_obj(namespace='storage')
            if _ is not None:
                if _.get_is_directory():
                    descendants = tree_item_prx.get_descendants()
                    c = len(descendants)
                    if c > 100:
                        w = utl_core.DialogWindow.set_create(
                            'List all Texture(s)',
                            content='list {} texture units from "{}", press "Yes" to continue'.format(
                                c,
                                _.path
                            ),
                            status=utl_core.DialogWindow.ValidatorStatus.Warning,
                        )
                        result = w.get_result()
                        if result is not True:
                            return
                    #
                    for i_item_prx in descendants:
                        # self._obj_list_viewer_0.set_loading_update()
                        i_file = i_item_prx.get_gui_dcc_obj(namespace='storage-file')
                        if i_file is not None:
                            if i_file.get_is_exists() is True:
                                i_list_item_prx = self._obj_list_viewer_0.set_item_add()
                                i_list_item_prx.set_gui_dcc_obj(i_file, namespace='storage')
                                set_show_fnc_(i_file, i_list_item_prx)
                else:
                    file_units = _.get_exists_files_()
                    c = len(file_units)
                    if c > 50:
                        w = utl_core.DialogWindow.set_create(
                            'List all Texture-unit(s)',
                            content='list {} texture units from "{}", press "Yes" to continue'.format(
                                c,
                                _.path
                            ),
                            status=utl_core.DialogWindow.ValidatorStatus.Warning,
                        )
                        result = w.get_result()
                        if result is not True:
                            return
                    #
                    for i_file_unit in file_units:
                        i_list_item_prx = self._obj_list_viewer_0.set_item_add()
                        set_show_fnc_(i_file_unit, i_list_item_prx)

    def _set_dcc_texture_references_update_(self):
        self._texture_references = None
    #
    def _get_checked_dcc_objs_(self):
        lis = []
        for i_dcc_obj in self._dcc_objs:
            item_prx = i_dcc_obj.get_obj_gui()
            if item_prx is not None:
                if item_prx.get_is_checked() is True:
                    lis.append(i_dcc_obj)
        return lis
    #
    def set_color_space_auto_switch(self):
        if self._texture_references is not None:
            includes = self._get_checked_dcc_objs_()
            utl_dcc_operators.DccTexturesOpt(
                self._texture_references,
                includes=includes
            ).set_color_space_auto_switch()
            #
            self._set_refresh_all_(includes)

    def set_tx_create_and_repath_use_thread(self):
        def complete_fnc():
            _set_texture_tx_repath(self._texture_references, includes)
            self._set_refresh_all_()

        method_signals = utl_gui_qt_core.QtMethodSignals(self.widget)
        method_signals.stated.connect(complete_fnc)

        if self._texture_references is not None:
            force = self._tool_node_prx.get_port('create_and_repath_to_tx_force').get()
            includes = self._get_checked_dcc_objs_()
            #
            _set_texture_tx_create(
                self,
                self._tool_node_prx.get_port('create_and_repath_to_tx'),
                self._texture_references,
                includes,
                force,
                completed_fnc=method_signals.stated.emit
            )

    def set_tx_repath_to_orig(self):
        if self._texture_references is not None:
            includes = self._get_checked_dcc_objs_()
            utl_dcc_operators.DccTexturesOpt(
                self._texture_references,
                includes=includes
            ).set_tx_repath_to_orig()
            #
            self._set_refresh_all_(includes)

    def set_jpg_create_and_repath_use_thread(self):
        def complete_fnc():
            _set_texture_jpg_repath(self._texture_references, includes)
            self._set_refresh_all_()

        method_signals = utl_gui_qt_core.QtMethodSignals(self.widget)
        method_signals.stated.connect(complete_fnc)

        if self._texture_references is not None:
            force = self._tool_node_prx.get_port('create_and_repath_to_jpg_force').get()
            includes = self._get_checked_dcc_objs_()
            #
            _set_texture_jpg_create(
                self,
                self._tool_node_prx.get_port('create_and_repath_to_jpg'),
                self._texture_references,
                includes,
                force,
                completed_fnc=method_signals.stated.emit
            )

    def set_jpg_repath_to_orig(self):
        if self._texture_references is not None:
            includes = self._get_checked_dcc_objs_()
            utl_dcc_operators.DccTexturesOpt(
                self._texture_references,
                includes=includes
            ).set_repath_to_orig_as_tgt_ext('.jpg')
            #
            self._set_refresh_all_(includes)

    def set_map_to_platform_platform(self):
        if self._texture_references is not None:
            includes = self._get_checked_dcc_objs_()
            utl_dcc_operators.DccTexturesOpt(
                self._texture_references,
                includes=includes
            ).set_map_to_platform()
            #
            self._set_refresh_all_()

    def set_search(self):
        target_directory = self._search_node_gui.get_port('target_directory').get()
        ignore_source_resolved = self._search_node_gui.get_port('ignore_source_resolved')
        target_directory_paths = [
            i.lstrip().rstrip() for i in target_directory.split(',')
        ]
        if self._texture_references is not None:
            if target_directory_paths:
                includes = self._get_checked_dcc_objs_()
                utl_dcc_operators.DccTexturesOpt(
                    self._texture_references,
                    includes=includes
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
                includes = self._get_checked_dcc_objs_()
                utl_dcc_operators.DccTexturesOpt(
                    self._texture_references,
                    includes=includes
                ).set_copy_and_repath_to(target_directory)
        #
        self._set_refresh_all_()


class AbsShotgunEntitiesCreatorPanel(
    prx_widgets.PrxToolWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/shotgun-entity-creator'
    HELP_FILE_PATH = utl_configure.MainData.get_help_file(
        'utility/panel/shotgun-entity-creator'
    )
    #
    PROJECT_INCLUDES = ['lib']
    STUDIO_INCLUDES = ['CG']
    def __init__(self, *args, **kwargs):
        super(AbsShotgunEntitiesCreatorPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_configure.MainData.get_as_configure(
            self.CONFIGURE_FILE_PATH
        )
        self.set_window_title(
            self._window_configure.get('window.name')
        )
        self.set_definition_window_size(
            self._window_configure.get('window.size')
        )
        #
        self._shotgun_template_configure = utl_configure.MainData.get_as_configure(
            'shotgun/template'
        )
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        self._set_tool_group_0_build_()

    def _set_tool_panel_setup_(self):
        self._set_refresh_all_()

    def _set_tool_group_0_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Create-tool(s)')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._tool_node_prx = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._tool_node_prx.widget)
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxPortForEnumerate('project', 'Project-name')
        )
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxPortForEnumerate('task_template', 'Task-template')
        )
        _port.set_tool_tip(self._shotgun_template_configure.get_str_as_yaml_style())
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxPortForString('entities', 'Entity-name(s)')
        )
        _port.set_tool_tip(
            [
                'enter one or more "entity-name"',
                'sep is ","',
            ]
        )
        #
        _port = self._tool_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('create', 'Create')
        )
        _port.set_tool_tip(
            [
                'press to create entities'
            ]
        )
        _port.set(
            self._set_create_
        )

    def _set_refresh_all_(self):
        self._set_projects_refresh_()
        self._set_task_templates_refresh_()
        # self._tool_node_prx.get_port('entities').set('asset_add_0_test, asset_add_1_test')
    # project
    def _set_projects_refresh_(self):
        if self.PROJECT_INCLUDES is None:
            projects = self._get_projects_()
        else:
            projects = self.PROJECT_INCLUDES
        #
        _port = self._tool_node_prx.get_port('project')
        _port.set(projects)
        if projects:
            _port.set_current(projects[0])

    def _get_projects_(self):
        raise NotImplementedError()

    def _get_project_(self):
        return self._tool_node_prx.get_port('project').get()
    
    def _set_task_templates_refresh_(self):
        templates = self._shotgun_template_configure.get_branch_keys('task-templates')
        _port = self._tool_node_prx.get_port('task_template')
        _port.set(templates)
        _port.set_current(
            templates[0]
        )

    def _get_task_template_(self):
        return self._tool_node_prx.get_port('task_template').get()

    def _get_entity_key_(self):
        template = self._get_task_template_()
        return self._shotgun_template_configure.get('task-templates.{}.entity-key'.format(template))

    def _get_task_keys_(self):
        template = self._get_task_template_()
        return self._shotgun_template_configure.get('task-templates.{}.task-keys'.format(template))

    def _get_entities_(self):
        _ = self._tool_node_prx.get_port('entities').get()
        if _:
            return [i.lstrip().rstrip() for i in _.split(',')]
        return []

    def _set_create_(self):
        raise NotImplementedError()


class AbsDatabaseGeometryManagerPanel(
    prx_widgets.PrxToolWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/database-geometry-manager'
    def __init__(self, *args, **kwargs):
        super(AbsDatabaseGeometryManagerPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_configure.MainData.get_as_configure(
            self.CONFIGURE_FILE_PATH
        )
        self.set_window_title(
            self._window_configure.get('window.name')
        )
        self.set_definition_window_size(
            self._window_configure.get('window.size')
        )
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        self._set_utility_group_build_()
        self._set_database_export_group_build_()
        self._set_database_import_group_build_()
        self._set_hash_uv_group_build_()

    def _set_utility_group_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Utility')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._utility_node_prx = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._utility_node_prx.widget)
        #
        _port = self._utility_node_prx.set_port_add(
            prx_widgets.PrxFileSavePort('save_usd_file', 'Save USD-file')
        )
        _port.set_ext_filter('All USD File (*.usd *.usda)')
        _port.set_tool_tip(
            [
                'choose / enter a usd "file-path"'
            ]
        )
        #
        _port = self._utility_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('export_select_to_usd_file', 'Export Select(s) to USD-file')
        )
        _port.set_tool_tip(
            [
                'press to export select(s) to usd "Save USD-file"'
            ]
        )
        _port.set(self._set_usd_file_export_)
        #
        _port = self._utility_node_prx.set_port_add(
            prx_widgets.PrxFileOpenPort('open_usd_file', 'Open USD-file')
        )
        _port.set_ext_filter('All USD File (*.usd *.usda)')
        _port.set_tool_tip(
            [
                'choose / enter a usd "file-path"'
            ]
        )
        #
        _port = self._utility_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('import_from_usd_file', 'Import from USD-file')
        )
        _port.set_tool_tip(
            [
                'press to import geometry from usd "Open USD-file"'
            ]
        )
        _port.set(self._set_usd_file_import_)

    def _set_database_export_group_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Database Export')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._database_export_node_prx = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._database_export_node_prx.widget)
        #
        _port = self._database_export_node_prx.set_port_add(
            prx_widgets.PrxPortForBoolean('export_uv_map_force', 'Export UV-map(s) Force')
        )
        _port.set_tool_tip(
            [
                'override data in database if is "checked"'
            ]
        )
        _port = self._database_export_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('export_uv_map_to_database_from_select', 'Export Database UV-map(s) from Select(s)')
        )
        _port.set_tool_tip(
            [
                '"LMB-click" to export selected mesh(s) to database'
            ]
        )
        _port.set(self._set_database_uv_map_export_)

    def _set_database_import_group_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Database Import')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._database_import_node_prx = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._database_import_node_prx.widget)
        #
        _port = self._database_import_node_prx.set_port_add(
            prx_widgets.PrxButtonPort('import_database_uv_map_to_select', 'Import Database UV-map(s) to Select(s)')
        )
        _port.set_tool_tip(
            [
                'press to import geometry from database to selected geometry(s)'
            ]
        )
        _port.set(self._set_database_uv_map_import_)

    def _set_hash_uv_group_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Database Extend')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._hash_uv_node_prx = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._hash_uv_node_prx.widget)
        #
        _port = self._hash_uv_node_prx.set_port_add(
            prx_widgets.PrxSubProcessPort('geometry_unify', 'Unify Geometry by Select(s)')
        )
        _port.set(self._set_geometry_unify_run_)
        _port.set_menu_raw(
            [
                ('Stop Deadline-job', None, self._set_geometry_unify_ddl_job_stop_)
            ]
        )
        #
        self._geometry_unify_ddl_job_process = None
        self.set_window_close_connect_to(self._set_geometry_unify_ddl_job_stop_)
        #
        _port = self._hash_uv_node_prx.set_port_add(
            prx_widgets.PrxSubProcessPort('geometry_uv_map_assign', 'Assign Geometry UV-map By Select(s)')
        )
        _port.set(self._set_geometry_uv_map_assign_run_)
        _port.set_menu_raw(
            [
                ('Stop Deadline-job', None, self._set_geometry_uv_map_assign_ddl_job_stop_)
            ]
        )
        self._geometry_uv_assign_ddl_job_process = None

    def _set_tool_panel_setup_(self):
        self._set_refresh_all_()

    def _set_refresh_all_(self):
        pass

    def _set_usd_file_export_(self):
        pass

    def _set_usd_file_import_(self):
        pass

    def _set_geometry_unify_run_(self):
        raise NotImplementedError()

    def _set_database_uv_map_export_(self):
        raise NotImplementedError()

    def _set_database_uv_map_import_(self):
        raise NotImplementedError()

    def _set_geometry_unify_ddl_job_stop_(self):
        if self._geometry_unify_ddl_job_process is not None:
            self._geometry_unify_ddl_job_process.set_stop()

    def _set_geometry_unify_ddl_job_processing_(self, running_time_cost):
        raise NotImplementedError()

    def _set_geometry_unify_ddl_job_status_changed_(self, process_status):
        raise NotImplementedError()
    #
    def _set_geometry_uv_map_assign_run_(self):
        raise NotImplementedError()
    #
    def _set_geometry_uv_map_assign_ddl_job_stop_(self):
        if self._geometry_uv_assign_ddl_job_process is not None:
            self._geometry_uv_assign_ddl_job_process.set_stop()

    def _set_geometry_uv_map_assign_ddl_job_processing_(self, running_time_cost):
        raise NotImplementedError()

    def _set_geometry_uv_map_assign_ddl_job_status_changed_(self, process_status):
        raise NotImplementedError()


class AbsGeometryCheckerPanel(
    prx_widgets.PrxToolWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/geometry-checker'
    def __init__(self, *args, **kwargs):
        super(AbsGeometryCheckerPanel, self).__init__(*args, **kwargs)
        self._window_configure = utl_configure.MainData.get_as_configure(
            self.CONFIGURE_FILE_PATH
        )
        self.set_window_title(
            self._window_configure.get('window.name')
        )
        self.set_definition_window_size(
            self._window_configure.get('window.size')
        )
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        pass

    def _set_tool_panel_setup_(self):
        self._set_refresh_all_()

    def _set_refresh_all_(self):
        pass


class AbsFncPanel(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(AbsFncPanel, self).__init__(*args, **kwargs)
        #
        self.set_definition_window_size((480, 320))
        #
        self._set_panel_build_()

    def _set_panel_build_(self):
        self._node_prx_0 = prx_widgets.PrxNode()
        self.set_widget_add(self._node_prx_0)
