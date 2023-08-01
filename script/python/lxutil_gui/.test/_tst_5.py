# coding:utf-8

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _gui_prx_wdt_node, _utl_gui_prx_wgt_view

from lxutil_gui.qt.widgets import _gui_qt_wgt_chart, _utl_gui_qt_wgt_view


class TestWindow(_utl_gui_prx_wdt_utility.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        wdt = _utl_gui_prx_wgt_view.PrxListView()
        wdt.set_clear()
        self.add_widget(wdt)
        for i in range(50):
            item_prx = wdt.create_item(name=str(i))
            item_prx.set_image('/data/f/vedio_test/laohu_da.rig.layout_rigging.v002.thumbnail.jpg')
            item_prx.set_icon_by_file('application/maya')
            item_prx.set_name(str(i).zfill(9))
            # item_prx.set_icon_by_text('asset')
            item_prx.set_gui_menu_raw(
                [
                    ('Open folder', 'file/open-folder', None),
                ]
            )


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
    w._test_()
    #
    sys.exit(app.exec_())
