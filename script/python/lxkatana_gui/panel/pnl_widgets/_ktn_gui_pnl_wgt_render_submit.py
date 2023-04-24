# coding:utf-8
import collections

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil_gui import utl_gui_core

from lxkatana import ktn_core

import lxkatana.scripts as ktn_scripts

import lxutil_gui.panel.abstracts as utl_gui_panel_abstracts

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class PnlRenderSubmitter(utl_gui_panel_abstracts.AbsPnlRenderSubmitter):
    """
    # coding:utf-8
    import lxkatana

    lxkatana.set_reload()
    import lxsession.commands as ssn_commands; ssn_commands.set_hook_execute("dcc-tool-panels/katana/asset-render-submitter")
    """
    DCC_NAMESPACE = 'katana'
    def __init__(self, *args, **kwargs):
        super(PnlRenderSubmitter, self).__init__(*args, **kwargs)
    @classmethod
    def _to_render_layer_(cls, opt_opt):
        parent_opt = opt_opt.get_parent_opt()
        if parent_opt.get('type') == 'RenderLayer_Wsp':
            return parent_opt

    def post_setup_fnc(self):
        file_path = ktn_dcc_objects.Scene.get_current_file_path()
        self._options_prx_node.set('scene', file_path)
        self._options_prx_node.get_port('scene').set_locked(True)

        self._result_list_view.connect_refresh_action_to(self.set_refresh_all)

    def set_refresh_all(self):
        self.gui_add_all_render_nodes()

    def node_selection_fnc(self):
        list_ = []
        prx_items = self._result_list_view.get_selected_items()
        for i_prx_item in prx_items:
            i_render_node_opt = i_prx_item.get_gui_dcc_obj(
                namespace=self.DCC_NAMESPACE
            )
            if i_render_node_opt is not None:
                i_render_layer_opt = self._to_render_layer_(i_render_node_opt)
                if i_render_layer_opt is not None:
                    list_.append(i_render_layer_opt.get_path())
                else:
                    list_.append(i_render_node_opt.get_path())

        ktn_dcc_objects.Selection(list_).select_all()

    def get_all_render_layers(self):
        return ktn_core.NGObjsMtd.find_nodes(
            type_name='Render'
        )

    def gui_add_all_render_nodes(self):
        self._render_layer_pattern_dict = {}
        #
        self._result_list_view.set_restore()
        #
        ns = self.get_all_render_layers()
        c = len(ns)
        with utl_core.GuiProgressesRunner.create(maximum=c, label='gui build render layer') as g_p:
            for i in ns:
                g_p.set_update()
                i_opt = ktn_core.NGObjOpt(i)
                self._gui_add_render_node_(i_opt)

    def gui_refresh_all_render_nodes(self):
        self._render_layer_pattern_dict = {}
        prx_items = self._result_list_view.get_all_items()
        for i_prx_item in prx_items:
            self._gui_refresh_render_node_(i_prx_item)

    def _gui_refresh_render_node_(self, prx_item):
        render_node_opt = prx_item.get_gui_dcc_obj(
            namespace=self.DCC_NAMESPACE
        )

        if render_node_opt.get_is_bypassed(ancestors=True) is True:
            prx_item.set_visible(False)
        else:
            prx_item.set_visible(True)

        prx_item.set_check_enable(True)

        prx_item.set_image(
            utl_gui_core.RscIconFile.get('image_loading_failed_error')
        )

        default_render_version = self._options_prx_node.get('render.version')
        default_render_frames = self._options_prx_node.get('render.frames')

        name_dict = collections.OrderedDict()
        render_node_name = render_node_opt.get_name()
        name_dict['node'] = render_node_name
        render_layer_opt = ktn_scripts.ScpRenderLayer._to_render_layer_(render_node_opt)
        descriptions = []
        if render_layer_opt is not None:
            render_layer_scp = ktn_scripts.ScpRenderLayer(render_layer_opt)

            render_version_mode = render_layer_opt.get('parameters.render.version.mode')
            render_version = render_layer_scp.get_render_version(default_render_version)
            name_dict['version'] = '{} [{}]'.format(render_version, render_version_mode)
            #
            render_frames_mode = render_layer_opt.get('parameters.render.frames.mode')
            render_frames = render_layer_scp.get_render_frames(default_render_frames)
            name_dict['frames'] = '{} [{}]'.format(render_frames, render_frames_mode)

            render_output_directory_path = render_layer_scp.get_render_output_directory(default_render_version)
            name_dict['output-directory'] = render_output_directory_path
            #
            latest_render_output_image_file_path = render_layer_scp.get_latest_render_output_image()
            if latest_render_output_image_file_path is not None:
                image_file_paths = bsc_core.StgFileMultiplyMtd.get_exists_tiles(
                    latest_render_output_image_file_path
                )
                if image_file_paths:
                    image_file_path = image_file_paths[0]
                    thumbnail = bsc_core.ImgFileOpt(image_file_path).get_thumbnail()
                    if thumbnail:
                        prx_item.set_image(thumbnail)
        else:
            name_dict['frames'] = default_render_frames

        prx_item.set_name_dict(
            name_dict
        )

        prx_item.set_tool_tip(
            descriptions
        )

    def _gui_add_menu_(self, prx_item):
        def open_fnc_():
            _name_dict = prx_item.get_name_dict()
            if _name_dict:
                if 'output-directory' in _name_dict:
                    _directory_path = _name_dict['output-directory']
                    _exist_comp = bsc_core.StgExtraMtd.get_exists_component(_directory_path)
                    if _exist_comp is not None:
                        bsc_core.StgExtraMtd.set_directory_open(
                            _exist_comp
                        )

        def enable_fnc_():
            _name_dict = prx_item.get_name_dict()
            if _name_dict:
                if 'output-directory' in _name_dict:
                    _directory_path = _name_dict['output-directory']
                    return bsc_core.StgPathMtd.get_is_exists(_directory_path)
            return False

        menu_raw = [
            ('basic',),
            ('open output directory', 'file/folder', (enable_fnc_, open_fnc_, False)),
            ('open output directory (force)', 'file/folder', (True, open_fnc_, False))
        ]

        prx_item.set_menu_raw(
            menu_raw
        )

    def _gui_add_render_node_(self, render_node_opt):
        def cache_fnc_():
            _list = []
            return _list

        def build_fnc_(data):
            self._gui_refresh_render_node_(
                prx_item
            )
            self._gui_add_menu_(
                prx_item
            )

        prx_item = self._result_list_view.set_item_add()
        # print path, semantic_tag_filter_data
        prx_item.set_gui_dcc_obj(
            render_node_opt, namespace=self.DCC_NAMESPACE
        )
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )

    def get_checked_render_nodes(self):
        list_ = []
        prx_items = self._result_list_view.get_all_items()
        for i_prx_item in prx_items:
            if i_prx_item.get_is_checked() is True and i_prx_item.get_is_visible() is True:
                i_render_node_opt = i_prx_item.get_gui_dcc_obj(
                    namespace=self.DCC_NAMESPACE
                )
                if i_render_node_opt is not None:
                    if i_render_node_opt.get_is_bypassed(ancestors=True) is False:
                        list_.append(i_render_node_opt.get_name())
        return list_

    def submit_to_farm(self):
        def yes_fnc_():
            default_render_version = self._options_prx_node.get('render.version')
            default_render_frames = self._options_prx_node.get('render.frames')

            j_option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key='rsv-project-methods/asset/katana/render-build',
                    #
                    file=file_path,
                    #
                    render_nodes=render_nodes,
                    default_render_version=default_render_version,
                    default_render_frames=default_render_frames,
                    auto_convert_mov=True,
                    #
                    td_enable=bsc_core.EnvExtraMtd.get_td_enable(),
                    rez_beta=bsc_core.EnvExtraMtd.get_rez_beta(),
                )
            )
            #
            session = ssn_commands.set_option_hook_execute_by_deadline(
                option=j_option_opt.to_string()
            )
            ddl_job_id = session.get_ddl_job_id()
            if ddl_job_id:
                w.set_completed_content(
                    (
                        'Deadline job submit is completed, job id is: "{}"\n'
                        '\n'
                        'Press "Close" to continue'
                    ).format(ddl_job_id)
                )

        from lxbasic import bsc_core

        import lxsession.commands as ssn_commands

        ktn_dcc_objects.Scene.save_file_with_dialog()

        file_path = self._options_prx_node.get('scene')

        render_file_path = bsc_core.StgFileOpt(file_path).get_render_file_path()
        if bsc_core.StgPathMtd.get_is_exists(render_file_path) is True:
            w = utl_core.DialogWindow.set_create(
                label=self._session.gui_name,
                content=u'Scene is non changed for submit, render file for this scene is exists:\n"{}"'.format(
                    render_file_path
                ),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                window_size=(480, 160),
                no_visible=False,
                #
                yes_label='Ignore',
                parent=self.widget,
            )
            if w.get_result() is not True:
                return
        #
        render_nodes = self.get_checked_render_nodes()
        if not render_nodes:
            w = utl_core.DialogWindow.set_create(
                label=self._session.gui_name,
                content=(
                    'No render-node is checked, check at least one render-node'
                ),
                status=utl_core.DialogWindow.ValidatorStatus.Warning,
                window_size=(480, 160),
                yes_visible=False,
                no_visible=False,
                parent=self.widget,
            )
            return

        w = utl_core.DialogWindow.set_create(
            label=self._session.gui_name,
            content=(
                'Submit render to deadline for render node:\n'
                '{}\n'
                '\n'
                'Press "Confirm" to continue'
            ).format(
                ',\n'.join(['    "{}"'.format(i) for i in render_nodes])
            ),
            #
            yes_label='Confirm',
            #
            yes_method=yes_fnc_,
            #
            no_visible=False,
            show=False,
            #
            window_size=(480, 240),
            #
            parent=self.widget,
            #
            use_exec=False,
            #
            use_window_modality=False
        )
        w.set_yes_completed_notify_enable(True)

        w.set_window_close_connect_to(
            self.widget.show
        )

        self.widget.hide()

        w.set_window_show()
