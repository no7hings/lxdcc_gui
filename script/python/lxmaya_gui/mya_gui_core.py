# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds, mel


class ProgressWindowOpt(object):
    def __init__(self, maximum, label):
        self._label = label
        self._value = 0
        self._maximum = maximum

    def set_show(self):
        cmds.progressWindow(
            label=self._label,
            maxValue=self._maximum,
            progress=self._value,
            status='0%',
            isInterruptable=False
        )

    def set_update(self):
        self._value += 1
        cmds.progressWindow(
            edit=True,
            progress=self._value,
            status=('{}%'.format(self._value/self._maximum*100))
        )
        if self._value == self._maximum:
            self._value = 0
            self.set_stop()
    @classmethod
    def set_stop(cls):
        cmds.progressWindow(endProgress=1)


class ProgressBarOpt(object):
    KEY = None
    def __init__(self, maximum, label):
        self._label = label
        self._value = 0
        self._maximum = maximum
    #
    def updateProgressBar(self):
        if self.KEY is None:
            self.KEY = mel.eval('$lynxiProgressVar = $gMainProgressBar')
    #
    def set_show(self):
        if self._maximum > 0:
            self.updateProgressBar()
            self._value = 0
            #
            cmds.progressBar(
                self.KEY,
                edit=True,
                beginProgress=True,
                isInterruptable=True,
                status=self._label,
                maxValue=self._maximum
            )
        return self
    #
    def set_update(self, sub_label=None):
        if self.KEY is not None:
            self._value += 1
            if self._value == self._maximum:
                self._value = 0
                self.set_stop()
            else:
                cmds.progressBar(self.KEY, edit=True, step=1)
                if sub_label is not None:
                    cmds.progressBar(self.KEY, edit=True, status='{} ( {} )'.format(self._label, sub_label))
    #
    def set_stop(self):
        cmds.progressBar(
            self.KEY,
            edit=True,
            endProgress=True
        )


if __name__ == '__main__':
    import lxmaya

    lxmaya.Packages.set_reload()

    from lxmaya_gui import mya_gui_core

    p = mya_gui_core.ProgressBarOpt(10, 'test').set_show()

    p.set_stop()
