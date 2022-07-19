# coding:utf-8
from lxutil import utl_core

job_id = '62cfbaa8e127c60c888793a4'


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtCore, QtWidgets

    #
    app = QtWidgets.QApplication(sys.argv)

    utl_core.DDlMonitor.set_create(
        'test', job_id
    )

    sys.exit(app.exec_())
