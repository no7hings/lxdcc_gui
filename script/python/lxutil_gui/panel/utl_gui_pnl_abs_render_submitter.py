# coding:utf-8
from lxbasic import bsc_core

import lxutil_gui.qt.widgets as qt_widgets

from lxutil import utl_configure, utl_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxbasic.objects as bsc_objects

import lxresolver.commands as rsv_commands

import lxutil_gui.proxy.operators as utl_prx_operators

import lxusd.rsv.objects as usd_rsv_objects

import lxsession.commands as ssn_commands


class AbsAssetRenderSubmitter(
    prx_widgets.PrxToolWindow
):
    ITEM_FRAME_SIZE = 128, 192
    OPTION_HOOK_KEY = None
    #
    def __init__(self, hook_option=None, *args, **kwargs):
        super(AbsAssetRenderSubmitter, self).__init__(*args, **kwargs)
        if hook_option is not None:
            self._hook_option_opt = bsc_core.KeywordArgumentsOpt(hook_option)
            self._file_path = self._hook_option_opt.get('file')
            self._hook_option_opt.set(
                'option_hook_key', self.OPTION_HOOK_KEY
            )
            self._option_hook_configure = ssn_commands.get_option_hook_configure(
                self._hook_option_opt.to_string()
            )
            self._option_hook_gui_configure = self._option_hook_configure.get_content('option.gui')
            self._option_hook_build_configure = self._option_hook_configure.get_content('build')
            #
            self.set_window_title(
                self._option_hook_gui_configure.get('name')
            )
            self._rez_beta = bsc_core.EnvironMtd.get('REZ_BETA')
            if self._rez_beta:
                self.set_window_title(
                    '[BETA] {}'.format(self._option_hook_gui_configure.get('name'))
                )
            #
            self.set_definition_window_size(
                self._option_hook_gui_configure.get('size')
            )
        else:
            self._file_path = None
        #
        self._rsv_task = None
        self._rsv_render_movie_file_unit = None
        #
        self._variable_keys = []
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_prx_node_build_()
        self.set_all_refresh()

    def _set_viewer_groups_build_(self):
        h_splitter_0 = prx_widgets.PrxHSplitter()
        self.set_widget_add(h_splitter_0)
        #
        v_splitter_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.set_widget_add(v_splitter_0)
        qt_scroll_area_0 = qt_widgets.QtScrollArea()
        v_splitter_0.set_widget_add(qt_scroll_area_0)
        qt_layout_0 = qt_scroll_area_0._layout
        #
        self._prx_schemes_node = prx_widgets.PrxNode_('scheme')
        qt_layout_0.addWidget(self._prx_schemes_node.widget)
        #
        self._prx_options_node = prx_widgets.PrxNode_('options')
        qt_layout_0.addWidget(self._prx_options_node.widget)
        #
        prx_expanded_group_0 = prx_widgets.PrxExpandedGroup()
        v_splitter_0.set_widget_add(prx_expanded_group_0)
        prx_expanded_group_0.set_name('variables')
        prx_expanded_group_0.set_expanded(True)
        #
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        prx_expanded_group_0.set_widget_add(self._filter_tree_viewer_0)
        v_splitter_0.set_stretches([2, 1])
        #
        prx_expanded_group_1 = prx_widgets.PrxExpandedGroup()
        h_splitter_0.set_widget_add(prx_expanded_group_1)
        prx_expanded_group_1.set_expanded(True)
        prx_expanded_group_1.set_name('renderers')
        self._rsv_renderer_list_view = prx_widgets.PrxListView()
        prx_expanded_group_1.set_widget_add(self._rsv_renderer_list_view)

        qt_scroll_area_1 = qt_widgets.QtScrollArea()
        qt_layout_1 = qt_scroll_area_1._layout
        h_splitter_0.set_widget_add(qt_scroll_area_1)
        #
        self._prx_usd_node = prx_widgets.PrxNode_('usd')
        qt_layout_1.addWidget(self._prx_usd_node.widget)
        #
        self._prx_settings_node = prx_widgets.PrxNode_('settings')
        qt_layout_1.addWidget(self._prx_settings_node.widget)
        #
        h_splitter_0.set_stretches([1, 2, 1])
        #
        self._set_obj_viewer_build_()

    def _set_obj_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/5.0) - 24
        )
        self._filter_tree_viewer_0.set_single_selection()

        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._rsv_renderer_list_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

        self._rsv_renderer_list_view.set_item_frame_size(*self.ITEM_FRAME_SIZE)
        self._rsv_renderer_list_view.set_item_icon_frame_draw_enable(True)
        self._rsv_renderer_list_view.set_item_name_frame_draw_enable(True)
        self._rsv_renderer_list_view.set_item_image_frame_draw_enable(True)

    def _set_prx_node_build_(self):
        #
        self._prx_schemes_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.schemes')
        )
        self._prx_schemes_node.set_changed_connect_to(
            'variables', self.set_filter_scheme_load_from_scheme
        )

        self._prx_schemes_node.set(
            'save', self.set_scheme_save
        )
        #
        self._prx_options_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.options')
        )

        self._prx_options_node.set(
            'refresh', self.set_options_node_refresh
        )

        # self._prx_options_node.get_port(
        #     'version'
        # ).set_changed_connect_to(
        #     self.set_settings_node_refresh
        # )

        self._prx_options_node.get_port(
            'shot'
        ).set_changed_connect_to(
            self.__set_usd_node_refresh_
        )

        self._prx_options_node.get_port(
            'shot'
        ).set_changed_connect_to(
            self.set_settings_node_refresh
        )
        # usd
        self._prx_usd_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.usd')
        )

        self._prx_usd_node.get_port(
            'variants.asset_version'
        ).set_expanded(False)
        self._prx_usd_node.get_port(
            'variants.asset_version_override'
        ).set_expanded(False)

        self._prx_usd_node.get_port(
            'variants.shot_version'
        ).set_expanded(False)
        self._prx_usd_node.get_port(
            'variants.shot_version_override'
        ).set_expanded(False)

        self._prx_settings_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.settings')
        )

        self._prx_settings_node.set(
            'submit', self.set_submit
        )

    def set_all_refresh(self):
        if self._file_path:
            self._file_path = bsc_core.StoragePathMtd.set_map_to_platform(self._file_path)
            self._resolver = rsv_commands.get_resolver()
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(self._file_path)
            if self._rsv_scene_properties:
                self._rsv_task = self._resolver.get_rsv_task(
                    **self._rsv_scene_properties.value
                )
                self._rsv_entity = self._rsv_task.get_rsv_entity()
                self._rsv_render_movie_file_unit = self._rsv_task.get_rsv_unit(
                    keyword='asset-output-katana-render-movie-file'
                )
                #
                self.set_options_node_refresh()
                self.__set_usd_node_refresh_()
                self.set_settings_node_refresh()
                #
                self.set_renderers_refresh()
                self.set_filter_refresh()

    def set_scheme_save(self):
        filter_dict = self._prx_dcc_obj_tree_view_tag_filter_opt.get_filter_dict()
        # print filter_dict
        bsc_objects.Configure(value=filter_dict).set_print_as_yaml_style()

    def set_options_node_refresh(self):
        self._prx_options_node.set(
            'task', self._rsv_task.path
        )
        rsv_asset = self._rsv_task.get_rsv_entity()
        branch = self._rsv_task.get('branch')
        step = self._rsv_task.get('step')
        if step in ['mod']:
            self._prx_schemes_node.set(
                'variables', 'model'
            )
        elif step in ['srf']:
            self._prx_schemes_node.set(
                'variables', 'surface'
            )
        elif step in ['grm']:
            self._prx_schemes_node.set(
                'variables', 'groom'
            )
        else:
            self._prx_schemes_node.set(
                'variables', 'asset'
            )
        #
        application = self._rsv_scene_properties.get('application')
        if application == 'maya':
            keyword = '{}-work-{}-scene-src-file'.format(
                branch, application
            )
            self._prx_options_node.set('choice_scheme', 'asset-work-maya')
        elif application == 'katana':
            keyword = '{}-work-{}-scene-src-file'.format(
                branch, application
            )
            self._prx_options_node.set('choice_scheme', 'asset-work-katana')
        else:
            raise RuntimeError()

        any_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword)
        rsv_versions = any_scene_file_rsv_unit.get_rsv_versions()

        self._prx_options_node.set('version', rsv_versions)

        self._rsv_asset_set_usd_creator = usd_rsv_objects.RsvAssetSetUsdCreator(rsv_asset)
        if bsc_core.SystemMtd.get_is_linux():
            if bsc_core.SystemMtd.get_application() not in ['maya']:
                rsv_shots = self._rsv_asset_set_usd_creator.get_rsv_asset_shots()
                self._prx_options_node.set('shot', rsv_shots)

    def __set_rsv_unit_gui_show_deferred_(self, prx_item, variants):
        names = ['{}={}'.format(k, v) for k, v in variants.items()]
        #
        hook_options = []
        #
        variable_name = '.'.join(variants.values())
        # print variable_name
        movie_file_path = self._rsv_render_movie_file_unit.get_result(
            version='latest',
            extend_variants=variants
        )
        if movie_file_path:
            rsv_properties = self._rsv_render_movie_file_unit.get_properties(
                movie_file_path
            )
            version = rsv_properties.get('version')
            names.append('version={}'.format(version))
            image_file_path, image_sub_process_cmds = bsc_core.VedioOpt(movie_file_path).get_thumbnail_create_args()
            prx_item.set_image(image_file_path)
            prx_item.set_movie_enable(True)
            #
            session, execute_fnc = ssn_commands.get_option_hook_args(
                bsc_core.KeywordArgumentsOpt(
                    dict(
                        option_hook_key='actions/movie-open',
                        file=movie_file_path,
                        gui_group_name='movie',
                        gui_name='open movie'
                    )
                ).to_string()
            )
            #
            prx_item.set_press_db_clicked_connect_to(
                execute_fnc
            )
            #
            hook_options.extend(
                [
                    bsc_core.KeywordArgumentsOpt(
                        dict(
                            option_hook_key='actions/movie-open',
                            file=movie_file_path,
                            gui_group_name='movie',
                            gui_name='open movie'
                        )
                    ).to_string(),
                    bsc_core.KeywordArgumentsOpt(
                        dict(
                            option_hook_key='actions/file-directory-open',
                            file=movie_file_path,
                            gui_group_name='movie',
                            gui_name='open movie-directory'
                        )
                    ).to_string()
                ]
            )
            if image_sub_process_cmds is not None:
                if prx_item.get_image_show_sub_process() is None:
                    image_sub_process = bsc_objects.SubProcess(image_sub_process_cmds)
                    image_sub_process.set_start()
                    prx_item.set_image_show_sub_process(image_sub_process)
                    # prx_item.set_image_loading_start()
        else:
            names.append('version=null')
            prx_item.set_image(
                utl_core.Icon._get_file_path_('@image_loading_failed@')
            )

        menu_content = ssn_commands.get_menu_content_by_hook_options(hook_options)
        prx_item.set_menu_content(menu_content)

        prx_item.set_names(names)
        r, g, b = bsc_core.TextOpt(variable_name).to_rgb()
        prx_item.set_name_frame_background_color((r, g, b, 127))

        prx_item.set_tool_tip(
            '\n'.join(names)
        )

    def set_renderers_refresh(self):
        def set_thread_create_fnc_(prx_item_, variants_):
            prx_item_.set_show_method(
                lambda *args, **kwargs: self.__set_rsv_unit_gui_show_deferred_(
                    prx_item_, variants_
                )
            )
        #
        self._rsv_renderer_list_view.set_clear()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_restore()
        #
        self._variable_variants_dic = self._option_hook_build_configure.get('variables.character')
        self._variable_keys = self._option_hook_build_configure.get_branch_keys(
            'variables.character'
        )
        combinations = bsc_core.VariablesMtd.get_all_combinations(
            self._variable_variants_dic
        )
        for i_seq, i_variants in enumerate(combinations):
            # print i_seq, i_variants
            i_prx_item = self._rsv_renderer_list_view.set_item_add()
            set_thread_create_fnc_(i_prx_item, i_variants)
            for j_key in self._variable_keys:
                self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                    '{}.{}'.format(j_key, i_variants[j_key]), i_prx_item
                )

        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def __set_usd_node_refresh_(self):
        rsv_asset = self._rsv_task.get_rsv_entity()
        rsv_shot = self._prx_options_node.get(
            'shot'
        )
        if rsv_asset is not None and rsv_shot is not None:
            asset_usd_variant_dict = self._rsv_asset_set_usd_creator._get_asset_usd_set_dress_variant_dict_(rsv_asset)
            for k, v in asset_usd_variant_dict.items():
                i_port_path = v['port_path']
                i_variant_names = v['variant_names']
                i_current_variant_name = v['variant_name']
                self._prx_usd_node.set(
                    i_port_path, i_variant_names
                )
                self._prx_usd_node.set(
                    i_port_path, i_current_variant_name
                )
                self._prx_usd_node.set_default(
                    i_port_path, i_current_variant_name
                )
            #
            # shot_usd_variant_dict = self._rsv_asset_set_usd_creator._get_shot_usd_set_dress_variant_dict_(rsv_shot)
            # for k, v in shot_usd_variant_dict.items():
            #     i_port_path = v['port_path']
            #     i_variant_names = v['variant_names']
            #     i_current_variant_name = v['variant_name']
            #     self._prx_usd_node.set(
            #         i_port_path, i_variant_names
            #     )
            #     self._prx_usd_node.set(
            #         i_port_path, i_current_variant_name
            #     )

    def set_filter_refresh(self):
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh(expand_depth=1)
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()
        #
        self.set_filter_scheme_load_from_scheme()
    
    def set_filter_scheme_load_from_scheme(self):
        filter_scheme = self._prx_schemes_node.get('variables')
        filter_dict = self._option_hook_build_configure.get(
            'scheme.variables.{}'.format(filter_scheme)
        )
        if filter_dict:
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_by_dict(
                filter_dict
            )

    def set_settings_node_refresh(self):
        rsv_task = self._rsv_task
        if rsv_task is not None:
            rsv_shot = self._prx_options_node.get(
                'shot'
            )
            if rsv_shot is not None:
                frame_range = self._rsv_asset_set_usd_creator._get_shot_frame_range_(
                    rsv_shot
                )
                if frame_range is not None:
                    self._prx_settings_node.set(
                        'render.shot.frame_range', frame_range
                    )

    def _get_hook_option_dic_(self):
        dic = {}
        rsv_task = self._rsv_task
        if rsv_task is not None:
            dic['file'] = self._file_path
            #
            rsv_shot = self._prx_options_node.get(
                'shot'
            )
            if rsv_shot:
                dic['shot'] = rsv_shot.name
            #
            dic['choice_scheme'] = self._prx_options_node.get('choice_scheme')
            #
            settings_dic = self._get_settings_dic_()
            dic.update(settings_dic)

            variable_dic = self._get_variables_dic_()
            dic.update(variable_dic)

        return dic

    def _get_settings_dic_(self):
        dic = {}
        render_asset_frame_range = self._prx_settings_node.get('render.asset.frame_range')
        render_asset_frame_step = self._prx_settings_node.get('render.asset.frame_step')
        render_shot_frame_range = self._prx_settings_node.get('render.shot.frame_range')
        render_shot_frame_step = self._prx_settings_node.get('render.shot.frame_step')
        #
        dic['render_asset_frames'] = bsc_core.FrameMtd.get(
            render_asset_frame_range, render_asset_frame_step
        )
        dic['render_shot_frames'] = bsc_core.FrameMtd.get(
            render_shot_frame_range, render_shot_frame_step
        )
        # dic['render_file'] = self._prx_settings_node.get('render.scene_file')
        # dic['render_output_directory'] = self._prx_settings_node.get('render.output_directory')
        dic['rez_beta'] = self._prx_settings_node.get('rez_beta')
        return dic

    def _get_variables_dic_(self):
        def update_fnc(key_):
            _ks = c.get_keys('/{}/*'.format(key_))
            _key = key_mapper[key_]
            for _i_k in _ks:
                if c.get(_i_k) is True:
                    _name = bsc_core.DccPathDagOpt(_i_k).get_name()
                    dic.setdefault(_key, []).append(_name)

        key_mapper = {
            'camera': 'cameras',
            'layer': 'layers',
            'light_pass': 'light_passes',
            'look_pass': 'look_passes',
            'quality': 'qualities'
        }
        dic = {}
        filter_dic = self._prx_dcc_obj_tree_view_tag_filter_opt.get_filter_dict()
        c = bsc_objects.Configure(value=filter_dic)
        for i in self._variable_keys:
            update_fnc(i)
        return dic
    @classmethod
    def _get_frames_(cls, frame_range, frame_step):
        pass

    def set_submit(self):
        hook_option_dic = self._get_hook_option_dic_()
        hook_option_dic['user'] = bsc_core.SystemMtd.get_user_name()
        hook_option_dic['rez_beta'] = True
        # hook_option_dic['td_enable'] = True
        hook_option_dic['option_hook_key'] = 'rsv-task-batchers/asset/combination-render-submit'
        option_opt = bsc_core.KeywordArgumentsOpt(hook_option_dic)
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=option_opt.to_string()
        )


class AbsShotRenderSubmitter(
    prx_widgets.PrxToolWindow
):
    ITEM_FRAME_SIZE = 128, 192
    OPTION_HOOK_KEY = None
    #
    def __init__(self, hook_option=None, *args, **kwargs):
        super(AbsShotRenderSubmitter, self).__init__(*args, **kwargs)
        if hook_option is not None:
            self._hook_option_opt = bsc_core.KeywordArgumentsOpt(hook_option)
            self._file_path = self._hook_option_opt.get('file')
            self._hook_option_opt.set(
                'option_hook_key', self.OPTION_HOOK_KEY
            )
            self._option_hook_configure = ssn_commands.get_option_hook_configure(
                self._hook_option_opt.to_string()
            )
            self._option_hook_gui_configure = self._option_hook_configure.get_content('option.gui')
            self._option_hook_build_configure = self._option_hook_configure.get_content('build')
            #
            self.set_window_title(
                self._option_hook_gui_configure.get('name')
            )
            self._rez_beta = bsc_core.EnvironMtd.get('REZ_BETA')
            if self._rez_beta:
                self.set_window_title(
                    '[BETA] {}'.format(self._option_hook_gui_configure.get('name'))
                )
            #
            self.set_definition_window_size(
                self._option_hook_gui_configure.get('size')
            )
        else:
            self._file_path = None
        #
        self._rsv_task = None
        self._rsv_render_movie_file_unit = None
        #
        self._variable_keys = []
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_viewer_groups_build_(self):
        h_splitter_0 = prx_widgets.PrxHSplitter()
        self.set_widget_add(h_splitter_0)
        #
        v_splitter_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.set_widget_add(v_splitter_0)
        qt_scroll_area_0 = qt_widgets.QtScrollArea()
        v_splitter_0.set_widget_add(qt_scroll_area_0)
        qt_layout_0 = qt_scroll_area_0._layout
        #
        self._prx_schemes_node = prx_widgets.PrxNode_('scheme')
        qt_layout_0.addWidget(self._prx_schemes_node.widget)
        #
        self._prx_options_node = prx_widgets.PrxNode_('options')
        qt_layout_0.addWidget(self._prx_options_node.widget)
        #
        prx_expanded_group_0 = prx_widgets.PrxExpandedGroup()
        v_splitter_0.set_widget_add(prx_expanded_group_0)
        prx_expanded_group_0.set_name('variables')
        prx_expanded_group_0.set_expanded(True)
        #
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        prx_expanded_group_0.set_widget_add(self._filter_tree_viewer_0)
        v_splitter_0.set_stretches([2, 1])
        #
        prx_expanded_group_1 = prx_widgets.PrxExpandedGroup()
        h_splitter_0.set_widget_add(prx_expanded_group_1)
        prx_expanded_group_1.set_expanded(True)
        prx_expanded_group_1.set_name('renderers')
        self._rsv_renderer_list_view = prx_widgets.PrxListView()
        prx_expanded_group_1.set_widget_add(self._rsv_renderer_list_view)

        qt_scroll_area_1 = qt_widgets.QtScrollArea()
        qt_layout_1 = qt_scroll_area_1._layout
        h_splitter_0.set_widget_add(qt_scroll_area_1)
        #
        self._prx_usd_node = prx_widgets.PrxNode_('usd')
        qt_layout_1.addWidget(self._prx_usd_node.widget)
        #
        self._prx_settings_node = prx_widgets.PrxNode_('settings')
        qt_layout_1.addWidget(self._prx_settings_node.widget)
        #
        h_splitter_0.set_stretches([1, 2, 1])
        #
        self._set_obj_viewer_build_()

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()

    def _set_tool_panel_setup_(self):
        self.set_window_loading_end()
        self._set_prx_node_build_()
        self.set_all_refresh()

    def _set_prx_node_build_(self):
        self._prx_schemes_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.schemes')
        )
        self._prx_schemes_node.set_changed_connect_to(
            'variables', self.set_filter_scheme_load_from_scheme
        )
        #
        self._prx_options_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.options')
        )
        self._prx_options_node.get_port(
            'version'
        ).set_changed_connect_to(
            self.set_settings_node_refresh
        )
        # usd
        self._prx_usd_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.usd')
        )
        # settings
        self._prx_settings_node.set_ports_create_by_configure(
            self._option_hook_build_configure.get('node.settings')
        )
        self._prx_settings_node.set(
            'submit', self.set_submit
        )

    def _set_obj_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('Name(s)', 3), ('Count(s)', 1)],
            self.get_definition_window_size()[0]*(1.0/5.0) - 24
        )
        self._filter_tree_viewer_0.set_single_selection()

        self._prx_dcc_obj_tree_view_tag_filter_opt = utl_prx_operators.PrxDccObjTreeViewTagFilterOpt(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._rsv_renderer_list_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

        self._rsv_renderer_list_view.set_item_frame_size(*self.ITEM_FRAME_SIZE)
        self._rsv_renderer_list_view.set_item_icon_frame_draw_enable(True)
        self._rsv_renderer_list_view.set_item_name_frame_draw_enable(True)
        self._rsv_renderer_list_view.set_item_image_frame_draw_enable(True)

    def __set_rsv_unit_gui_show_deferred_(self, prx_item, variants):
        names = ['{}={}'.format(k, v) for k, v in variants.items()]

        hook_options = []
        #
        variable_name = '.'.join(variants.values())
        # print variable_name
        movie_file_path = self._rsv_render_movie_file_unit.get_result(
            version='latest',
            extend_variants=variants
        )
        if movie_file_path:
            rsv_properties = self._rsv_render_movie_file_unit.get_properties(
                movie_file_path
            )
            version = rsv_properties.get('version')
            names.append('version={}'.format(version))
            image_file_path, image_sub_process_cmds = bsc_core.VedioOpt(movie_file_path).get_thumbnail_create_args()
            prx_item.set_image(image_file_path)
            prx_item.set_movie_enable(True)
            #
            session, execute_fnc = ssn_commands.get_option_hook_args(
                bsc_core.KeywordArgumentsOpt(
                    dict(
                        option_hook_key='actions/movie-open',
                        file=movie_file_path,
                        gui_group_name='movie',
                        gui_name='open movie'
                    )
                ).to_string()
            )
            #
            prx_item.set_press_db_clicked_connect_to(
                execute_fnc
            )
            #
            hook_options.extend(
                [
                    bsc_core.KeywordArgumentsOpt(
                        dict(
                            option_hook_key='actions/movie-open',
                            file=movie_file_path,
                            gui_group_name='movie',
                            gui_name='open movie'
                        )
                    ).to_string(),
                    bsc_core.KeywordArgumentsOpt(
                        dict(
                            option_hook_key='actions/file-directory-open',
                            file=movie_file_path,
                            gui_group_name='movie',
                            gui_name='open movie-directory'
                        )
                    ).to_string()
                ]
            )
            if image_sub_process_cmds is not None:
                if prx_item.get_image_show_sub_process() is None:
                    image_sub_process = bsc_objects.SubProcess(image_sub_process_cmds)
                    image_sub_process.set_start()
                    prx_item.set_image_show_sub_process(image_sub_process)
                    # prx_item.set_image_loading_start()
        else:
            names.append('version=null')
            prx_item.set_image(
                utl_core.Icon._get_file_path_('@image_loading_failed@')
            )

        menu_content = ssn_commands.get_menu_content_by_hook_options(hook_options)
        prx_item.set_menu_content(menu_content)

        prx_item.set_names(names)
        r, g, b = bsc_core.TextOpt(variable_name).to_rgb()
        prx_item.set_name_frame_background_color((r, g, b, 127))

        prx_item.set_tool_tip(
            '\n'.join(names)
        )

    def set_all_refresh(self):
        if self._file_path:
            self._file_path = bsc_core.StoragePathMtd.set_map_to_platform(self._file_path)
            self._resolver = rsv_commands.get_resolver()
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(self._file_path)
            if self._rsv_scene_properties:
                self._rsv_task = self._resolver.get_rsv_task(
                    **self._rsv_scene_properties.value
                )
                self._rsv_entity = self._rsv_task.get_rsv_entity()
                self._rsv_render_movie_file_unit = self._rsv_task.get_rsv_unit(
                    keyword='shot-output-katana-render-movie-file'
                )
                #
                self.set_options_node_refresh()
                self.set_renderers_refresh()
                self.set_filter_refresh()

    def set_filter_refresh(self):
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh(expand_depth=1)
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()
        #
        self.set_filter_scheme_load_from_scheme()

    def set_filter_scheme_load_from_scheme(self):
        filter_scheme = self._prx_schemes_node.get('variables')
        filter_dict = self._option_hook_build_configure.get(
            'scheme.variables.{}'.format(filter_scheme)
        )
        if filter_dict:
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_by_dict(
                filter_dict
            )

    def set_options_node_refresh(self):
        self._prx_options_node.set(
            'task', self._rsv_task.path
        )
        rsv_asset = self._rsv_task.get_rsv_entity()
        branch = self._rsv_task.get('branch')
        application = self._rsv_scene_properties.get('application')

        if application == 'maya':
            keyword = '{}-work-{}-scene-src-file'.format(
                branch, application
            )
            self._prx_options_node.set('choice_scheme', 'asset-work-maya')
        elif application == 'katana':
            keyword = '{}-work-{}-scene-src-file'.format(
                branch, application
            )
            self._prx_options_node.set('choice_scheme', 'asset-work-katana')
        else:
            raise RuntimeError()

        any_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword)
        rsv_versions = any_scene_file_rsv_unit.get_rsv_versions()

        self._prx_options_node.set('version', rsv_versions)

    def set_settings_node_refresh(self):
        rsv_task = self._rsv_task
        if rsv_task is not None:
            rsv_shot = self._rsv_entity
            if rsv_shot is not None:
                frame_range = usd_rsv_objects.RsvAssetSetUsdCreator._get_shot_frame_range_(
                    rsv_shot
                )
                if frame_range is not None:
                    self._prx_settings_node.set(
                        'render.shot.frame_range', frame_range
                    )

    def set_renderers_refresh(self):
        def set_thread_create_fnc_(prx_item_, variants_):
            prx_item_.set_show_method(
                lambda *args, **kwargs: self.__set_rsv_unit_gui_show_deferred_(
                    prx_item_, variants_
                )
            )
        #
        self._rsv_renderer_list_view.set_clear()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_restore()
        #
        self._variable_variants_dic = self._option_hook_build_configure.get('variables.character')
        self._variable_keys = self._option_hook_build_configure.get_branch_keys(
            'variables.character'
        )
        combinations = bsc_core.VariablesMtd.get_all_combinations(
            self._variable_variants_dic
        )
        for i_seq, i_variants in enumerate(combinations):
            # print i_seq, i_variants
            i_prx_item = self._rsv_renderer_list_view.set_item_add()
            set_thread_create_fnc_(i_prx_item, i_variants)
            for j_key in self._variable_keys:
                self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                    '{}.{}'.format(j_key, i_variants[j_key]), i_prx_item
                )

        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def set_submit(self):
        cmd_pattern = self._option_hook_configure.get('command')
        if self._rsv_task:
            c = bsc_objects.Configure(value={})
            c.set('project', self._rsv_task.get('project'))
            c.set('shot', self._rsv_task.get('shot'))
            c.set('step', self._rsv_task.get('step'))
            c.set('task', self._rsv_task.get('task'))

            c.set('shading', 'default')

            c.set('user', bsc_core.SystemMtd.get_user_name())

            c.set('render_shot_frames', '1001,1002')
            c.set('render_shot_frame_step', int(self._prx_settings_node.get('render.frame_step')))
            c.set('render_motion_enable', int(self._prx_settings_node.get('render.motion_enable')))
            c.set('render_instance_enable', int(self._prx_settings_node.get('render.instance_enable')))
            c.set('render_bokeh_enable', int(self._prx_settings_node.get('render.bokeh_enable')))
            c.set('render_background_enable', int(self._prx_settings_node.get('render.background_enable')))
            c.set('render_chunk', self._prx_settings_node.get('render.chunk'))

            c.set('arnold_aa_sample', self._prx_settings_node.get('render.arnold.aa_sample'))

            c.set('user_publish_enable', int(self._prx_settings_node.get('user.publish_enable')))
            c.set('user_tech_review_enable', int(self._prx_settings_node.get('user.tech_review_enable')))
            c.set('user_description', self._prx_settings_node.get('user.description'))

            cmd = cmd_pattern.format(
                **c.value
            )

            utl_core.SubProcessRunner.set_run_with_result(
                cmd
            )
