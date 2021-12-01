# coding:utf-8

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wdt_node, _utl_gui_prx_wgt_view, _utl_gui_prx_wgt_window


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    for i in range(20):
        if i == 10:
            w = _utl_gui_prx_wgt_window.PrxDialogWindow1()
            w.set_yes_label('Save')
            w.set_content_text_size(10)
            w.set_content('test')
            #
            w.widget.exec_()
            # w.set_window_show()
            print w.get_result()
    #
    sys.exit(app.exec_())
