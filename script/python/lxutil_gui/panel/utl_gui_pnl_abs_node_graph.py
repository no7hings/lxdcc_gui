# coding:utf-8
from lxbasic import bsc_core

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

from lxutil_gui.qt import utl_gui_qt_core

from lxobj import core_objects

import lxsession.commands as ssn_commands


class AbsRezGraph(prx_widgets.PrxToolWindow):
    OPTION_HOOK_KEY = None
    def __init__(self, hook_option, *args, **kwargs):
        super(AbsRezGraph, self).__init__(*args, **kwargs)
        if hook_option is not None:
            self._hook_option_opt = bsc_core.KeywordArgumentsOpt(hook_option)
            self._hook_option_opt.set(
                'option_hook_key', self.OPTION_HOOK_KEY
            )
            #
            self._option_hook_configure = ssn_commands.get_option_hook_configure(
                self._hook_option_opt.to_string()
            )
            #
            self._hook_gui_configure = self._option_hook_configure.get_content('option.gui')
            # self._hook_build_configure = self._option_hook_configure.get_content('build')
            #
            raw = bsc_core.EnvironMtd.get('REZ_BETA')
            if raw:
                self._rez_beta = True
            else:
                self._rez_beta = False

            if self._rez_beta:
                self.set_window_title(
                    '[BETA] {}'.format(self._hook_gui_configure.get('name'))
                )
            else:
                self.set_window_title(
                    self._hook_gui_configure.get('name')
                )
            #
            self.set_window_icon_name_text(
                self._hook_gui_configure.get('name')
            )
            self.set_definition_window_size(
                self._hook_gui_configure.get('size')
            )

            self.set_loading_start(
                time=1000,
                method=self._set_tool_panel_setup_
            )

    def _set_tool_panel_setup_(self):
        h_s = prx_widgets.PrxHSplitter()
        self.set_widget_add(h_s)
        self._node_tree = prx_widgets.PrxNodeTree()
        h_s.set_widget_add(self._node_tree)
        self._node_graph = prx_widgets.PrxNodeGraph()
        h_s.set_widget_add(self._node_graph)

        h_s.set_stretches([1, 3])

        packages = self._hook_option_opt.get('packages', as_array=True)
        self.test(packages)

        self.set_window_loading_end()

    def test(self, packages):
        import rez.resolved_context as r_c
        u = core_objects.ObjUniverse()

        r_s_t = u._get_obj_type_force_('rez', 'system')
        r_p_t = u._get_obj_type_force_('rez', 'package')
        r_v_t = u._get_obj_type_force_('rez', 'v')

        t = u._get_type_force_(u.Category.CONSTANT, u.Type.NODE)

        # ps = utl_core.MayaLauncher(
        #     project='cgm'
        # ).get_rez_packages()

        # ps = ['lxdcc']
        r = r_c.ResolvedContext(
            packages,
            package_paths=[
                bsc_core.StoragePathMtd.set_map_to_platform(i) for i in [
                    "/l/packages/pg/prod",
                    "/l/packages/pg/dept",
                    "/l/packages/pg/third_party/app",
                    "/l/packages/pg/third_party/plugin",
                    "/l/packages/pg/third_party/ocio"
                ]
            ]
        )

        root = u.get_root()
        root.set_input_port_create(
            t, 'input'
        )
        root.set_output_port_create(
            t, 'output'
        )

        path_dict = {}
        for i_key in packages:
            if '-' in i_key:
                i_type = r_v_t
                i_package, i_version = i_key.split('-')
                i_path = '/{}-{}'.format(i_package, i_version)
                i_n = i_type.set_obj_create(
                    i_path
                )
                i_n.set_input_port_create(
                    t, 'input'
                )
                i_n.set_output_port_create(
                    t, 'output'
                )
                root.get_input_port(
                    'input'
                ).set_source(
                    i_n.get_output_port(
                        'output'
                    )
                )
            else:
                i_package = i_key
                i_type = r_p_t
                i_path = '/{}'.format(i_package)

                i_p_n = i_type.set_obj_create(
                    i_path
                )
                i_p_n.set_input_port_create(
                    t, 'input'
                )
                i_p_n.set_output_port_create(
                    t, 'output'
                )
                root.get_input_port(
                    'input'
                ).set_source(
                    i_p_n.get_output_port(
                        'output'
                    )
                )

        g = r.graph()

        for i in g.nodes():
            i_atr = g.node_attributes(i)
            i_key = i_atr[0][1]
            if i_key.startswith('~'):
                i_type = r_s_t
                i_path = '/{}'.format(i_key)
            else:
                if '-' in i_key:
                    i_type = r_v_t
                    i_name, i_version = i_key.split('-')
                    if '[' in i_version:
                        if '[]' in i_version:
                            i_version_ = i_version[:-2]
                            i_path = '/{}-{}'.format(i_name, i_version_)
                        else:
                            i_version_ = i_version.split('[')[0]
                            i_index = i_version.split('[')[-1][:-1]
                            i_path = '/{}-{}-({})'.format(i_name, i_version_, i_index)
                    else:
                        i_path = '/{}-{}'.format(i_name, i_version)
                else:
                    i_type = r_p_t
                    i_path = '/{}'.format(i_key)
            #
            i_n = i_type.set_obj_create(
                i_path
            )
            i_n.set_input_port_create(
                t, 'input'
            )
            i_n.set_output_port_create(
                t, 'output'
            )
            path_dict[i] = i_path

        for i in g.edges():
            i_tgt, i_src = i
            i_src_path, i_tgt_path = path_dict[i_src], path_dict[i_tgt]
            i_n_src = u.get_obj(i_src_path)
            i_n_tgt = u.get_obj(i_tgt_path)
            i_n_src.get_output_port('output').set_connect_to(
                i_n_tgt.get_input_port('input')
            )

        self._node_graph.set_node_universe(u)
        self._node_graph.set_node_show()

        self._node_tree.set_node_universe(u)

        menu = self.set_menu_add(
            'Tool(s)'
        )
        menu.set_menu_raw(
            [
                ('Save Graph', None, self._set_graph_save_),
            ]
        )

    def _set_graph_save_(self):
        size = self._node_graph.widget.size()
        p = utl_gui_qt_core.QtGui.QPixmap(size)
        p.fill(utl_gui_qt_core.QtCore.Qt.transparent)
        self._node_graph.widget.render(
            p
        )
        p.save('/data/f/rez_test/png/test_0.png', 'PNG')