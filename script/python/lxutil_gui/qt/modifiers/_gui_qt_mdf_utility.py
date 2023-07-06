# coding:utf-8


def set_show_standalone(fnc):
    def fnc_(*args, **kw):
        import sys
        #
        from PySide2 import QtWidgets
        #
        app = QtWidgets.QApplication(sys.argv)
        fnc(*args, **kw)
        #
        sys.exit(app.exec_())
    return fnc_
