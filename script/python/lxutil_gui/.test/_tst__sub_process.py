# coding:utf-8
import os

from lxutil_gui.proxy.widgets import _utl_gui_prx_wgt_window_base, _utl_gui_prx_wdt_utility

from lxutil_gui.qt.gui_qt_core import *


class W(_utl_gui_prx_wgt_window_base.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        b = _utl_gui_prx_wdt_utility.PrxPressItem()
        self.add_button(b)
        b.set_name('Test')

        f = '/l/prod/cjd/publish/assets/chr/nn_gongshifu/srf/surfacing/nn_gongshifu.srf.surfacing.v019/review/nn_gongshifu.srf.surfacing.v019.mov'
        f_o = '/data/f/vedio_to_thumbnail_test/test_1.jpg'

        self._timer = QtCore.QTimer(self.widget)
        self._sub_process = None
        if os.path.exists(f):
            thumbnail_file_path, cmds = bsc_core.VdoFileOpt(f).get_thumbnail_create_args()
            if cmds:
                pass
            else:
                pass

    def _update_(self):
        if self._sub_process is not None:
            self._sub_process.set_update()
            print self._sub_process.get_status()


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_window_show()
    #
    sys.exit(app.exec_())
