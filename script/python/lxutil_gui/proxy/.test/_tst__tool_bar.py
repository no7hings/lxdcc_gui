# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets

import lxresolver.commands as rsv_commands


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        tool_bar = prx_widgets.PrxHToolBar()
        self.add_widget(tool_bar)
        tool_bar.set_left_alignment_mode()
        tool_bar.set_expanded(True)
        #
        tool_box = prx_widgets.PrxHToolBox_()
        tool_bar.add_widget(tool_box)
        tool_box.set_expanded(True)

        for i in range(20):
            i_tool = prx_widgets.PrxIconPressItem()
            tool_box.add_widget(i_tool)
            i_tool.set_icon_name('application/python')


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