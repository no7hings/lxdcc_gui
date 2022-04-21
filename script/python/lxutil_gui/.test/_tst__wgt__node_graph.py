# coding:utf-8
from lxutil import utl_configure

import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_chart, _utl_gui_qt_wgt_view

from lxobj import core_objects


class W(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        c = prx_widgets.PrxNodeGraph()
        self.set_widget_add(c)
        u = core_objects.ObjUniverse()

        o_t = u._get_obj_type_force_('lynxi', 'shader')

        n_0 = o_t.set_obj_create('/test_0')

        n_1 = o_t.set_obj_create('/test_1')

        t = u._get_type_force_(u.Category.CONSTANT, u.Type.NODE)

        for i in [n_0, n_1]:
            i.set_input_port_create(
                t, 'input'
            )
            i.set_output_port_create(
                t, 'output'
            )

        n_0.get_input_port('input').set_source(n_1.get_output_port('output'))

        c.set_node_universe(u)

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
