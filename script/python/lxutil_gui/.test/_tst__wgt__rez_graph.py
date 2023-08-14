# coding:utf-8
import rez.resolved_context as r_c

from lxutil import utl_configure

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil import utl_core

from lxutil_gui.qt import gui_qt_core

import lxuniverse.objects as unr_objects


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.start_loading(
            time=1000,
            method=self._set_tool_panel_setup_
        )

    def _set_tool_panel_setup_(self):
        self.test()

    def test(self):
        self._g = prx_widgets.PrxNGGraph()
        self.add_widget(self._g)
        u = unr_objects.ObjUniverse()

        r_s_t = u.generate_obj_type('rez', 'system')
        r_p_t = u.generate_obj_type('rez', 'package')
        r_v_t = u.generate_obj_type('rez', 'v')

        t = u.generate_type(u.Category.CONSTANT, u.Type.NODE)

        ps = utl_core.MayaLauncher(
            project='cgm'
        ).get_rez_packages()

        # ps = ['lxdcc']
        r = r_c.ResolvedContext(
            ps,
            package_paths=[
                "/l/packages/pg/prod",
                "/l/packages/pg/dept",
                "/l/packages/pg/third_party/app",
                "/l/packages/pg/third_party/plugin",
                "/l/packages/pg/third_party/ocio"
            ]
        )

        root = u.get_root()
        root.generate_input_port(
            t, 'input'
        )
        root.generate_output_port(
            t, 'output'
        )

        path_dict = {}
        for i in ps:
            i_path = '/{}'.format(i)
            i_p_n = r_p_t.set_obj_create(
                i_path
            )
            i_p_n.generate_input_port(
                t, 'input'
            )
            i_p_n.generate_output_port(
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
                            i_path = '/{}-{}-()'.format(i_name, i_version_)
                        else:
                            i_version_ = i_version.split('[')[0]
                            i_index = i_version.split('[')[-1][:-1]
                            i_path = '/{}-{}-({})'.format(i_name, i_version_, i_index)
                    else:
                        i_path = '/{}-{}'.format(i_name, i_version)
                else:
                    i_type = r_p_t
                    i_path = '/{}'.format(i_key)

            i_color = i_atr[1][1]
            if i_color == '#AAFFAA':
                pass
            elif i_color == '#F6F6F6':
                pass
            else:
                pass
            #
            i_n = i_type.set_obj_create(
                i_path
            )
            i_n.generate_input_port(
                t, 'input'
            )
            i_n.generate_output_port(
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

        self._g.set_universe(u)
        self._g.set_node_show()

        menu = self.create_menu(
            'Tool(s)'
        )
        menu.set_menu_data(
            [
                ('Save Graph', None, self._set_graph_save_),
            ]
        )

    def _set_graph_save_(self):
        size = self._g.widget.size()
        p = gui_qt_core.QtGui.QPixmap(size)
        p.fill(gui_qt_core.QtCore.Qt.transparent)
        self._g.widget.render(
            p
        )
        p.save('/data/f/rez_test/png/test_0.png', 'PNG')


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((800, 800))
    w.set_window_show()
    #
    sys.exit(app.exec_())