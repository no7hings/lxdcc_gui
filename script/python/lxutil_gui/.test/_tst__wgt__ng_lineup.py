# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxuniverse.objects as unr_objects


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        c = prx_widgets.PrxNGImageGraph()
        self.add_widget(c)
        u = unr_objects.ObjUniverse()

        o_t = u.generate_obj_type('lynxi', 'shader')

        t = u.generate_type(u.Category.CONSTANT, u.Type.STRING)

        r = u.get_root()

        r.generate_input_port(
            t, 'input'
        )
        r.generate_output_port(
            t, 'output'
        )
        d = utl_dcc_objects.OsDirectory_('/l/temp/td/dongchangbao/lineup-test')

        for i in d.get_all_file_paths():
            i_f = utl_dcc_objects.OsFile(i)
            i_n = o_t.set_obj_create(
                '/{}'.format(i_f.name_base)
            )
            i_p = i_n.generate_variant_port(
                t, 'image'
            )
            i_p.set(i)

        c.set_universe(u)
        c.set_node_show()

    def test(self):
        pass


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
