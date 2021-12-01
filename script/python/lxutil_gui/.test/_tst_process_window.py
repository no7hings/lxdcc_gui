# coding:utf-8
from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_item, _utl_gui_prx_wgt_window


class W(_utl_gui_prx_wdt_utility.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        b = _utl_gui_prx_wdt_utility.PrxPressItem()
        self.set_button_add(b)
        b.set_name('Test')
        b.set_press_clicked_connect_to(
            self.test
        )

    def test(self):
        utl_core.SubProcessRunner.set_run_with_log(
            'Test', 'rez-env lxdcc -c "lxscript -p cjd -a houdini -s set_geometry_unify_by_usd_file -o \"file=/home/dongchangbao/.lynxi/temporary/2021_0903/test.usd\""'
        )


if __name__ == '__main__':
    import sys
    #
    from lxutil import utl_core
    #
    from lxutil_gui.proxy.widgets import _utl_gui_prx_wgt_window
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_window_show()
    #
    sys.exit(app.exec_())
