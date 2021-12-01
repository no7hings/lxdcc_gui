# coding:utf-8
from lxbasic import bsc_core

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wdt_node, _utl_gui_prx_wgt_view

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_chart, _utl_gui_qt_wgt_view


class TestWindow(_utl_gui_prx_wdt_utility.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        def add_fnc_(i_):
            def show_fnc_():
                thumbnail_file_path = bsc_core.ImageOpt(
                    '/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/09-ADVANCED/Del_Cracks_11_1_1_1.jpg'
                ).get_thumbnail()
                wdt.set_loading_update()
                item_prx.set_image(thumbnail_file_path)
                item_prx.set_image_loading_start()

            item_prx = wdt.set_item_add()
            item_prx.set_show_method(show_fnc_)
        #
        wdt = _utl_gui_prx_wgt_view.PrxListView()
        wdt.set_clear()
        self.set_widget_add(wdt)
        for i in range(10):
            add_fnc_(i)


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_definition_window_size((960, 480))
    w.set_window_show()
    w._test_()
    #
    sys.exit(app.exec_())
