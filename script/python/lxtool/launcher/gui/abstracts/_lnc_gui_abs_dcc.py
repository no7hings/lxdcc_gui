# coding:utf-8
from lxbasic import bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets


class AbsPnlDccLauncher(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlDccLauncher, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):

        self._sub_label = qt_widgets.QtTextItem()
        self.add_widget(self._sub_label)
        self._sub_label.setFixedHeight(20)
        self._sub_label._set_name_draw_font_(gui_qt_core.QtFonts.SubTitle)
        self._sub_label._set_name_text_option_to_align_center_()

        self._ipt = prx_widgets.PrxInputAsStgTask()
        self.add_widget(self._ipt)

        self._ipt.set_focus_in()

        self.get_widget().key_escape_pressed.connect(
            self.__do_cancel
        )

        self._tip = prx_widgets.PrxTextBrowser()
        self.add_widget(self._tip)
        self._tip.set_focus_enable(False)

        self._ipt.connect_result_to(
            self._do_accept
        )
        self._ipt.connect_tip_trace_to(
            self._do_tip_trace
        )

        self._ipt.setup()

        self.__application = 'maya'

        self.__set_application(
            self._session.configure.get('option.extend.application')
        )

    def __set_application(self, application):
        self.__application = application
        self._sub_label._set_name_text_(application)

    def __get_application(self):
        return self.__application

    def _do_accept(self, dict_):
        if dict_:
            option_opt = bsc_core.ArgDictStringOpt(dict_)
            option_opt.set('application', self.__get_application())
            option = option_opt.to_string()

            cmd = bsc_core.PkgContextNew(
                ' '.join(['lxdcc'])
            ).get_command(
                args_execute=[
                    '-- lxapp -o \\\"{}\\\"'.format(
                        option
                    )
                ],
            )

            bsc_core.ExcExtra.execute_shell_script_use_terminal(
                '"{}"'.format(cmd), **dict(title=self.__get_application())
            )
            self.close_window_later()

    def _do_tip_trace(self, text):
        self._tip.set_content(text)

    def __do_cancel(self):
        if self._ipt.has_focus() is False:
            self.close_window_later()
