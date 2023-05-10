# coding:utf-8
import lxutil_gui.proxy.widgets as utl_prx_widgets

import lxresolver.commands as rsv_commands


class TestWindow(utl_prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        tool_bar = utl_prx_widgets.PrxHToolBar()
        self.set_widget_add(tool_bar)
        tool_bar.set_expanded(True)
        tool_group_0 = utl_prx_widgets.PrxHToolBox()
        tool_bar.set_widget_add(tool_group_0)

        tool = utl_prx_widgets.PrxIconPressItem()
        tool_group_0.set_widget_add(tool)
        tool.set_icon_name('application/python')

        tool_bar.set_expanded(True)
        tool_group_1 = utl_prx_widgets.PrxHToolBox()
        tool_bar.set_widget_add(tool_group_1)
        tool_group_1.set_size_mode(1)

        tool = utl_prx_widgets.PrxFilterBar()
        tool_group_1.set_widget_add(tool)
        # r = rsv_commands.get_resolver()
        # n = utl_prx_widgets.PrxNode_('root')
        # self.set_widget_add(n)
        # assets = r.get_rsv_resources(
        #     project='cgm', branch='asset'
        # )
        # p = n.set_port_add(
        #     utl_prx_widgets.PrxRsvObjChoosePort(
        #         'test'
        #     )
        # )
        # p.set(
        #     assets
        # )


if __name__ == '__main__':
    import time
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()
    #
    sys.exit(app.exec_())
