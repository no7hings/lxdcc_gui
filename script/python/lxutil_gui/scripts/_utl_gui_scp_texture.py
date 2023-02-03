# coding:utf-8
from lxbasic import bsc_core

from lxutil_gui.qt import utl_gui_qt_core


class ScpGuiTextureCreate(object):
    def __init__(self, window, button):
        self._window = window
        self._button = button
        self._cmds = []
        self._ts = []

        self._build_warning_texts = []
        self._execute_warning_texts = []

    def build_for_data(self):
        raise NotImplementedError()

    def execute_by_data(self, button, cmds):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            print '\n'.join(results)

        def status_changed_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            self._ts = []
            #
            for _i_index, _i_cmd in enumerate(self._cmds):
                bsc_core.PrcCmdThread.set_wait()
                #
                _i_t = bsc_core.PrcCmdThread.set_start(_i_cmd, _i_index)
                self._ts.append(_i_t)
                _i_t.status_changed.set_connect_to(status_changed_fnc_)
                _i_t.finished.set_connect_to(finished_fnc_)

        def quit_fnc_():
            button.set_stopped()
            #
            for _i in self._ts:
                _i.set_kill()
            #
            q_t.set_quit()

        contents = []
        if cmds:
            button.set_stopped(False)

            c = len(cmds)

            button.set_status(bsc_core.PrcCmdThread.Status.Started)
            button.set_initialization(c, bsc_core.PrcCmdThread.Status.Started)

            q_t = utl_gui_qt_core.QtMethodThread(self._window.widget)
            q_t.set_method_add(
                run_fnc_
            )
            q_t.start()

            self._window.set_window_close_connect_to(quit_fnc_)
        else:
            button.set_restore()
            contents = self._execute_warning_texts

        if contents:
            self.show_warning(contents)
            return False
        else:
            return True

    def set_build_warning_texts(self, texts):
        self._build_warning_texts = texts

    def set_execute_warning_texts(self, texts):
        self._execute_warning_texts = texts

    def show_warning(self, texts):
        pass

    def restore(self):
        self._cmds = []
        self._ts = []

    def append_cmd(self, cmd):
        self._cmds.append(cmd)

    def extend_cmds(self, cmds):
        self._cmds.extend(cmds)

    def run(self):
        self.restore()
        self.build_for_data()
        self.execute_by_data(self._button, self._cmds)

