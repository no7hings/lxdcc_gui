# coding:utf-8
from lxutil_gui import utl_gui_configure

import lxutil_gui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        h_s = prx_widgets.PrxHSplitter()
        self.add_widget(h_s)

        v_s_0 = prx_widgets.PrxVSplitter()
        h_s.add_widget(v_s_0)

        t_0 = prx_widgets.PrxTreeView()
        h_s.add_widget(t_0)
        t_1 = prx_widgets.PrxTreeView()
        v_s_0.add_widget(
            t_1
        )
        t_2 = prx_widgets.PrxTreeView()
        v_s_0.add_widget(
            t_2
        )

        v_s_1 = prx_widgets.PrxVSplitter()
        h_s.add_widget(
            v_s_1
        )

        t_3 = prx_widgets.PrxUsdStageView()
        v_s_1.add_widget(t_3)
        t_4 = prx_widgets.PrxListView()
        v_s_1.add_widget(t_4)

        # h_s.set_widget_hide_at(0)

        h_s.set_fixed_size_at(0, 320)
        h_s.set_fixed_size_at(2, 320)

        # h_s.set_contract_left_or_top_at(0)
        h_s.set_contract_right_or_bottom_at(2)

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
    w.set_definition_window_size((1280, 960))
    w.set_window_show()
    #
    sys.exit(app.exec_())
