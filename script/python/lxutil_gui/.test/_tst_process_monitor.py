# coding:utf-8
from lxarnold import and_setup

and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

import os

os.environ['OCIO'] = '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxutil.dcc.dcc_objects as utl_dcc_objets

from lxutil_gui.proxy.widgets import _utl_gui_prx_wgt_window

import lxutil.dcc.dcc_operators as utl_dcc_operators

job_id = '6154393fe127c60a24809539'


def set_processing_update(time_cost):
    c = '{} [ {} ]'.format(
        str(p_m.get_status()), bsc_core.IntegerMtd.second_to_time_prettify(time_cost)
    )
    w._wait_button.set_name(c)


def set_status_changed_update(status):
    c = '{} [ {} ]'.format(
        str(status),
        bsc_core.IntegerMtd.second_to_time_prettify(p_m.get_running_time_cost())
    )
    w._wait_button.set_name(c)
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
    w.set_window_show(size=(480, 160))
    d = utl_dcc_objets.OsDirectory_(
        '/data/f/texture-tx-test/v002'
    )
    fs = d.get_all_file_paths()
    for i_f_p in fs:
        i_f = utl_dcc_objets.OsTexture(i_f_p)
        if i_f.ext == '.jpg':
            i_f.set_delete()
    #
    p = utl_dcc_operators.TextureJpgMainProcess(d.get_all_file_paths())
    p.set_name('texture-jpg-create')
    p_m = bsc_objects.ProcessMonitor(p)
    p_m.logging.set_connect_to(set_logging_update)
    p_m.processing.set_connect_to(set_processing_update)
    p_m.status_changed.set_connect_to(set_status_changed_update)
    p_m.element_statuses_changed.set_connect_to(set_element_status_changed_update)
    p_m.set_start()
    p.set_start()
    w.set_window_close_connect_to(p_m.set_stop)

    sys.exit(app.exec_())
