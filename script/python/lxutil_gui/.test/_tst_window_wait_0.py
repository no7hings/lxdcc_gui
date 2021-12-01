# coding:utf-8
from lxbasic import bsc_core

import lxdeadline.objects as ddl_objects

from lxutil_gui.proxy.widgets import _utl_gui_prx_wgt_window

job_id = '6154393fe127c60a24809539'


def set_processing_update(time_cost):
    print bsc_core.IntegerMtd.second_to_time_prettify(time_cost)


def set_status_changed_update(status):
    w._wait_button.set_name(str(status))
    w._wait_button.set_status(status)


def set_element_status_changed_update(element_statuses):
    w._wait_button.set_element_statuses(element_statuses)


def set_logging_update(text):
    pass
    # w.set_content_add(text)


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtCore, QtWidgets

    #
    app = QtWidgets.QApplication(sys.argv)
    w = _utl_gui_prx_wgt_window.PrxWaitWindow()

    j_m = ddl_objects.DdlJobProcess(job_id)
    j_m.logging.set_connect_to(set_logging_update)
    j_m.processing.set_connect_to(set_processing_update)
    j_m.status_changed.set_connect_to(set_status_changed_update)
    j_m.element_statuses_changed.set_connect_to(set_element_status_changed_update)
    j_m.set_start()
    w.set_window_close_connect_to(j_m.set_stop)

    w.set_window_show(size=(480, 160))

    sys.exit(app.exec_())
