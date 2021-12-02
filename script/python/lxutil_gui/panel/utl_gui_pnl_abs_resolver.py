# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

import lxutil_gui.proxy.operators as utl_prx_operators

import lxutil_gui.qt.widgets as qt_widgets

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxresolver import rsv_configure, rsv_core

import lxresolver.commands as rsv_commands

from lxutil_gui.qt import utl_gui_qt_core


class AbsEntitiesLoaderPanel(prx_widgets.PrxToolWindow):
    PANEL_KEY = None
    DCC_NAMESPACE = 'resolver'
    RESOLVER_FILTER = None
    #
    ITEM_FRAME_ICON_SIZE = 40, 128
    ITEM_FRAME_IMAGE_SIZE = 128, 128
    ITEM_FRAME_NAME_SIZE = 128, 40
    #
    WINDOW_NAME = 'Entities Loader'
    WINDOW_SIZE = 1280, 960
    def __init__(self, *args, **kwargs):
        super(AbsEntitiesLoaderPanel, self).__init__(*args, **kwargs)
        #
        self._rsv_option_opt = bsc_core.KeywordArgumentsOpt(self.RESOLVER_FILTER)
        #
        self._filter_project = self._rsv_option_opt.get('project')
        #
        self.set_window_title(
            self.WINDOW_NAME
        )
        self.set_definition_window_size(
            self.WINDOW_SIZE
        )
        #
        self.get_log_bar().set_expanded(True)
        #
        self._set_panel_build_()
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )
        #
        self._rsv_entity_show_thread_timers = []
        self._rsv_task_show_thread_timers = []
    #
    def _set_rsv_option_update_(self, raw):
        pass

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_refresh_all_()

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        #
        self._prx_obj_guide_bar = prx_widgets.PrxGuideBar()
        expand_box_0.set_widget_add(self._prx_obj_guide_bar)
        #
        h_splitter_0 = prx_widgets.PrxHSplitter()
        expand_box_0.set_widget_add(h_splitter_0)
        v_splitter_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.set_widget_add(v_splitter_0)
        self._rsv_obj_tree_view_0 = prx_widgets.PrxTreeView()
        v_splitter_0.set_widget_add(self._rsv_obj_tree_view_0)
        #
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        v_splitter_0.set_widget_add(self._filter_tree_viewer_0)
        #
        self._rsv_uint_list_view_0 = prx_widgets.PrxListView()
        h_splitter_0.set_widget_add(self._rsv_uint_list_view_0)
        #
        v_splitter_0.set_stretches([1, 1])
        h_splitter_0.set_stretches([1, 3])
        #
        self._set_obj_viewer_build_()

    def _set_configure_groups_build_(self):
        expand_box_0 = prx_widgets.PrxExpandedGroup()
        expand_box_0.set_name('Configure(s)')
        expand_box_0.set_expanded(True)
        self.set_widget_add(expand_box_0)
        #
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.set_widget_add(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._configure_gui = prx_widgets.PrxNode()
        qt_layout_0.addWidget(self._configure_gui.widget)
        #
        if self._filter_project is not None:
            projects = [self._filter_project]
        else:
            projects = [
                'shl',
                'cg7',
                'cjd',
                'lib',
            ]
        current_project = self._get_current_project_()
        if current_project:
            if current_project in projects:
                projects.remove(current_project)
            #
            projects.append(current_project)
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxEnumeratePort('project', 'Project-name')
        )
        _port.set(projects)
        #
        _port = self._configure_gui.set_port_add(
            prx_widgets.PrxButtonPort('refresh', 'Refresh')
        )
        _port.set(self._set_refresh_all_)

    def _set_obj_viewer_build_(self):
        self._rsv_obj_tree_view_0.set_header_view_create(
            [('Name(s)', 3)],
            self.get_definition_window_size()[0]*(1.0/4.0) - 24
        )
        self._rsv_obj_tree_view_0.set_single_selection()
        #
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/4.0) - 24
        )
        self._filter_tree_viewer_0.set_single_selection()
        #
        self._prx_dcc_obj_tree_view_add_opt = utl_prx_operators.PrxRsvObjTreeViewAddOpt(
            prx_tree_view=self._rsv_obj_tree_view_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._rsv_obj_tree_view_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        #
        self._rsv_obj_tree_view_0.set_item_select_changed_connect_to(
            self._set_guide_bar_update_
        )
        self._rsv_obj_tree_view_0.set_item_select_changed_connect_to(
            self._set_rsv_unit_viewer_refresh_
        )
        #
        self._rsv_uint_list_view_0.set_item_frame_icon_size(*self.ITEM_FRAME_ICON_SIZE)
        self._rsv_uint_list_view_0.set_item_frame_image_size(*self.ITEM_FRAME_IMAGE_SIZE)
        self._rsv_uint_list_view_0.set_item_frame_name_size(*self.ITEM_FRAME_NAME_SIZE)
        #
        self._rsv_uint_list_view_0.set_item_select_changed_connect_to(
            self._set_guide_bar_update_
        )
        #
        self._prx_obj_guide_bar.set_item_clicked_connect_to(self._set_rsv_obj_select_)
        # self._prx_obj_guide_bar.set_item_changed_connect_to(self._set_rsv_obj_select_)
    @utl_gui_qt_core.set_window_prx_loading_modifier
    def _set_rsv_obj_viewer_refresh_(self):
        self._resolver = rsv_commands.get_resolver()
        if self._filter_project is not None:
            project = self._filter_project
        else:
            project = self._configure_gui.get_port(
                'project'
            ).get()
        #
        self._rsv_project = self._resolver.get_rsv_project(project=project)
        #
        self._prx_dcc_obj_tree_view_add_opt.set_restore()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_restore()
        self._prx_obj_guide_bar.set_clear()
        #
        rsv_tags = self._rsv_project.get_rsv_tags(
            **self._rsv_option_opt.value
        )
        self._set_rsv_obj_guis_add_use_thread_(
            rsv_tags, self._set_rsv_tag_gui_add_
        )
        #
        self._rsv_obj_tree_view_0.set_items_expand_by_depth(depth=2)
        #
        self._set_rsv_entity_guis_refresh_(rsv_tags)

    def _set_rsv_entity_guis_refresh_(self, rsv_objs):
        if rsv_objs:
            gp = utl_core.GuiProgressesRunner(maximum=len(rsv_objs))
            for rsv_obj in rsv_objs:
                gp.set_update()
                rsv_entities = rsv_obj.get_rsv_entities()
                self._set_rsv_obj_guis_add_use_thread_(
                    rsv_entities, self._set_rsv_entity_gui_add_
                )
            gp.set_stop()
    #
    def _set_rsv_obj_guis_add_use_thread_(self, rsv_objs, add_fnc):
        for rsv_obj in rsv_objs:
            add_fnc(rsv_obj)
            self._rsv_obj_tree_view_0.set_loading_update()
    # ================================================================================================================ #
    def _set_rsv_tag_gui_add_(self, rsv_tag):
        is_create, rsv_tag_item_prx, show_threads = self._prx_dcc_obj_tree_view_add_opt.set_item_prx_add_as_tree_mode(
            rsv_tag
        )
        if is_create is True:
            # rsv_tag_item_prx.set_loading_start()
            #
            # self._rsv_obj_tree_view_0.set_item_expand_connect_to(
            #     rsv_tag_item_prx, lambda *args, **kwargs: self._set_rsv_task_guis_add_(rsv_tag), time=250
            # )
            pass
        return show_threads

    def _set_rsv_entity_gui_add_(self, rsv_entity):
        is_create, rsv_entity_gui, show_threads = self._prx_dcc_obj_tree_view_add_opt.set_item_prx_add_as_tree_mode(
            rsv_entity
        )
        if is_create is True:
            rsv_entity_gui.set_loading_start()
            #
            branch = rsv_entity.properties.get('branch')
            if branch == 'asset':
                menu_content = self.get_rsv_entity_menu_content(rsv_entity)
                if menu_content:
                    rsv_entity.set_gui_menu_content(
                        menu_content
                    )
            #
            self._rsv_obj_tree_view_0.set_item_expand_connect_to(
                rsv_entity_gui, lambda *args, **kwargs: self._set_rsv_task_guis_add_(rsv_entity)
            )
        return show_threads
    @utl_gui_qt_core.set_window_prx_loading_modifier
    def _set_rsv_task_guis_add_(self, rsv_obj):
        rsv_obj_item_prx = rsv_obj.get_obj_gui()
        #
        rsv_tasks = rsv_obj.get_rsv_tasks(**self._rsv_option_opt.value)
        self._set_rsv_obj_guis_add_use_thread_(
            rsv_tasks, self._set_rsv_task_gui_add_
        )
        #
        rsv_obj_item_prx.set_loading_end()
        #
        self.set_filter_update()

    def _set_rsv_task_gui_add_(self, rsv_task):
        is_create, rsv_task_item_prx, show_threads = self._prx_dcc_obj_tree_view_add_opt.set_item_prx_add_as_tree_mode(
            rsv_task
        )
        if is_create is True:
            step = rsv_task.properties.get('step')
            task = rsv_task.properties.get('task')
            #
            menu_content = self.get_rsv_task_menu_content(rsv_task)
            if menu_content:
                rsv_task.set_gui_menu_content(
                    menu_content
                )
            #
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                '{}.{}'.format(step, task), rsv_task_item_prx
            )
        return show_threads

    def get_rsv_entity_menu_content(self, rsv_entity):
        raise NotImplementedError()

    def get_rsv_task_menu_content(self, rsv_task):
        raise NotImplementedError()

    def get_rsv_task_unit_menu_content(self, rsv_task):
        raise NotImplementedError()

    def get_rsv_task_unit_show_raw(self, rsv_task):
        raise NotImplementedError()

    def _set_guide_bar_update_(self):
        list_item_prxes = self._rsv_uint_list_view_0.get_selected_items()
        rsv_obj = None
        if list_item_prxes:
            list_item_prx = list_item_prxes[-1]
            rsv_obj = list_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
        else:
            tree_item_prxes = self._rsv_obj_tree_view_0.get_selected_items()
            if tree_item_prxes:
                tree_item_prx = tree_item_prxes[-1]
                rsv_obj = tree_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
        #
        if rsv_obj is not None:
            self._prx_obj_guide_bar.set_path_args(
                rsv_obj.get_path_args()
            )
            dag_components = rsv_obj.get_ancestors()
            if dag_components:
                dag_components.reverse()
                for index, i in enumerate(dag_components):
                    content = [i.name for i in i.get_children()]
                    self._prx_obj_guide_bar.set_item_contents_at(content, index)

    def _set_rsv_obj_select_(self):
        obj_path = self._prx_obj_guide_bar.get_current_path()
        if obj_path is not None:
            self._rsv_obj_tree_view_0.set_item_select_by_filter_key(
                obj_path,
                exclusive=True
            )
    @utl_gui_qt_core.set_window_prx_loading_modifier
    def _set_rsv_unit_viewer_refresh_(self):
        tree_item_prxes = self._rsv_obj_tree_view_0.get_selected_items()
        self._rsv_uint_list_view_0.set_clear()
        if tree_item_prxes:
            tree_item_prx = tree_item_prxes[-1]
            rsv_obj = tree_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
            if rsv_obj is not None:
                obj_type_name = rsv_obj.type_name
                if obj_type_name in [
                    'role', 'sequence',
                    'asset', 'shot',
                ]:
                    self._set_rsv_task_guis_add_(rsv_obj)
                #
                rsv_tasks = []
                if obj_type_name in [
                    'role', 'sequence',
                    'asset', 'shot',
                    'step'
                ]:
                    rsv_tasks = [i for i in rsv_obj.get_descendants() if i.type == 'task']
                elif obj_type_name in ['task']:
                    rsv_tasks = [rsv_obj]
                #
                rsv_tasks = rsv_core.ResolverMtd.set_rsv_obj_sort(rsv_tasks)
                #
                self._set_rsv_task_unit_guis_refresh_(rsv_tasks)

    def _set_rsv_task_unit_guis_refresh_(self, rsv_tasks):
        for rsv_task in rsv_tasks:
            self._set_rsv_task_unit_gui_add_(rsv_task)
            self._rsv_obj_tree_view_0.set_loading_update()
        #
        self._rsv_uint_list_view_0.set_visible_tgt_raw_update()
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()
    #
    def _set_rsv_task_unit_gui_add_(self, rsv_task):
        def set_thread_create_fnc_(rsv_task_, rsv_task_unit_args_lis_, i_rsv_unit_item_prx_):
            i_rsv_unit_item_prx_.set_show_method(
                lambda *args, **kwargs: self._set_rsv_unit_gui_show_deferred_(
                    rsv_task_, i_rsv_unit_item_prx_, rsv_task_unit_args_lis_
                )
            )
        #
        rsv_task_gui = rsv_task.get_obj_gui()
        #
        enable, rsv_task_unit_show_raw = self.get_rsv_task_unit_show_raw(rsv_task)
        if enable is True:
            rsv_task_unit_gui = self._rsv_uint_list_view_0.set_item_add()
            rsv_task_unit_gui.set_gui_dcc_obj(rsv_task, namespace=self.DCC_NAMESPACE)
            #
            key = rsv_task.path
            rsv_task_gui.set_visible_connect_to(
                key, rsv_task_unit_gui
            )
            #
            set_thread_create_fnc_(
                rsv_task,
                rsv_task_unit_show_raw,
                rsv_task_unit_gui
            )

    def _set_rsv_unit_gui_show_deferred_(self, rsv_task, rsv_task_unit_gui, rsv_task_unit_show_raw):
        task_properties = rsv_task.properties
        branch = task_properties.get('branch')
        name = task_properties.get(branch)
        step = task_properties.get('step')
        task = task_properties.get('task')
        #
        name_texts = [name, step, task]
        pixmap_icons = []
        for i_enable, i_rsv_unit, i_rsv_unit_file_path in rsv_task_unit_show_raw:
            if i_enable is True:
                # i_result_properties = i_rsv_unit.get_properties_by_result(i_rsv_unit_file_path)
                # version = i_result_properties.get('version')
                #
                i_rsv_unit_file = utl_dcc_objects.OsFile(i_rsv_unit_file_path)
                # i_user = i_rsv_unit_file.get_user()
                # i_time = i_rsv_unit_file.get_time()
                # icon_names.append(icon_name)
                i_icon_pixmap = utl_gui_qt_core.QtPixmapMtd.get_by_ext(i_rsv_unit_file.ext)
                pixmap_icons.append(i_icon_pixmap)
            else:
                i_rsv_unit_file = utl_dcc_objects.OsFile(i_rsv_unit_file_path)
                i_icon_pixmap = utl_gui_qt_core.QtPixmapMtd.get_by_ext(i_rsv_unit_file.ext, gray=not i_enable)
                pixmap_icons.append(i_icon_pixmap)
        #
        rsv_task_unit_gui.set_names(name_texts)
        rsv_task_unit_gui.set_pixmap_icons(pixmap_icons)
        rsv_task_unit_gui.set_tool_tip(
            task_properties.get_str_as_yaml_style()
        )
        #
        review_rsv_unit = rsv_task.get_rsv_unit(keyword='{}-review-file'.format(branch))
        vedio_file_path = review_rsv_unit.get_result(
            version=rsv_configure.Version.LATEST
        )
        if vedio_file_path:
            image_file_path, image_sub_process_cmds = bsc_core.VedioOpt(vedio_file_path).get_thumbnail_create_args()
            rsv_task_unit_gui.set_image(image_file_path)
            if image_sub_process_cmds is not None:
                image_sub_process = bsc_objects.SubProcess(image_sub_process_cmds)
                image_sub_process.set_start()
                rsv_task_unit_gui.set_image_show_sub_process(image_sub_process)
                rsv_task_unit_gui.set_image_loading_start()
        else:
            rsv_task_unit_gui.set_image(
                utl_core.Icon._get_file_path_('@image_loading_failed@')
            )
        #
        menu_content = self.get_rsv_task_unit_menu_content(rsv_task)
        if menu_content:
            rsv_task_unit_gui.set_menu_content(menu_content)

        self._rsv_uint_list_view_0.set_loading_update()

    def _set_refresh_all_(self):
        self._set_rsv_obj_viewer_refresh_()
        self.set_filter_refresh()

    def set_filter_update(self):
        self._rsv_uint_list_view_0.set_visible_tgt_raw_update()
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_update()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def set_filter_refresh(self):
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh(expand_depth=1)
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()
    @classmethod
    def _get_current_application_(cls):
        return utl_core.Application.get_current()
    @classmethod
    def _get_current_project_(cls):
        import os
        #
        _ = os.environ.get('PG_SHOW')
        if _:
            return _.lower()
