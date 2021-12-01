# coding:utf-8
from PySide2 import QtCore, QtWidgets


class W(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setFixedSize(800, 600)
        #
        w_ = QtWidgets.QWidget()
        self.setCentralWidget(w_)
        #
        l_ = QtWidgets.QHBoxLayout(w_)

        self._file = QtWidgets.QLineEdit()
        l_.addWidget(self._file)

        b_ = QtWidgets.QPushButton()
        b_.setText('Open')
        l_.addWidget(b_)
        b_.clicked.connect(self.open_file)

        b_1 = QtWidgets.QPushButton()
        l_.addWidget(b_1)
        b_1.setText('Copy')
        b_1.clicked.connect(self.copy_file)

    def open_file(self):
        f = QtWidgets.QFileDialog()
        s = f.getOpenFileName(
            self._file,
            caption='open file',
            dir='',
            filter='All File(s) (*.*)'
        )
        if s:
            self._file.setText(
                s[0]
            )

    def copy_file(self):
        f = self._file.text()
        print f


if __name__ == '__main__':
    import sys
    #
    app = QtWidgets.QApplication(sys.argv)
    w = W()
    #
    w.show()
    #
    sys.exit(app.exec_())
