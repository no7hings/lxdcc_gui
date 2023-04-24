# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets

import lxuniverse.objects as unr_objects


class W(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        c = prx_widgets.PrxNGGraph()
        self.set_widget_add(c)
        u = unr_objects.ObjUniverse()

        o_t = u.get_or_create_obj_type('lynxi', 'shader')

        t = u._get_type_force_(u.Category.CONSTANT, u.Type.NODE)

        r = u.get_root()

        r.set_input_port_create(
            t, 'input'
        )
        r.set_output_port_create(
            t, 'output'
        )

        p_n = None
        for i in range(10):
            i_n = o_t.set_obj_create(
                '/test_{}'.format(i)
            )
            i_n.set_input_port_create(
                t, 'input'
            )
            i_n.set_output_port_create(
                t, 'output'
            )
            if p_n is not None:
                p_n.get_input_port('input').set_source(i_n.get_output_port('output'))
            else:
                i_n.get_output_port('output').set_target(r.get_input_port('input'))
            #
            if not i % 10:
                p_n = i_n
            else:
                i_n.get_output_port('output').set_target(r.get_input_port('input'))

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
