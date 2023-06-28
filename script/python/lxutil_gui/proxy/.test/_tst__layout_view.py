# coding:utf-8
from lxutil_gui import utl_gui_configure

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        s = prx_widgets.PrxVScrollArea()
        self.add_widget(s)

        tool_group = prx_widgets.PrxHToolGroup_()
        s.add_widget(tool_group)
        tool_group.set_expanded(True)
        tool_group.set_name('Test')
        g = prx_widgets.PrxLayoutView()
        tool_group.add_widget(g)
        g.set_item_size(96, 20)

        for i in range(10):
            i_item = prx_widgets.PrxPressItem()
            i_item.set_name(str(i).zfill(4))
            g.add_item(i_item)

        tool_group = prx_widgets.PrxHToolGroup_()
        s.add_widget(tool_group)
        tool_group.set_expanded(True)
        g = prx_widgets.PrxLayoutView()
        tool_group.add_widget(g)
        g.set_item_size(200, 20)

        for i in range(10):
            i_item = prx_widgets.PrxPressItem()
            i_item.set_name(str(i).zfill(4))
            g.add_item(i_item)


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
