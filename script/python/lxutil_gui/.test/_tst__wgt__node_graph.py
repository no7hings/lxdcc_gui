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

        o_c = u.set_obj_category_create(
            'test'
        )

        o_t = o_c.set_type_create(
            'lynxi'
        )

        o_0 = o_t.set_obj_create('/test_0')

        o_1 = o_t.set_obj_create('/test_1')

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
