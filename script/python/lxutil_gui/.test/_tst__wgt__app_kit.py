# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxsession.commands as ssn_commands

utl_core.Environ.set_add(
    bsc_core.RscFileMtd.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)


class AppKit(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(AppKit, self).__init__(*args, **kwargs)
        #
        self._group_dict = {}
        self._list_view_dict = {}
        #
        self.get_log_bar().set_expanded(True)
        #
        self.set_window_title('App-kit')
        for i_key in [
            'rsv-panels/asset-loader',
        ]:
            i_hook_args = ssn_commands.get_hook_args(
                i_key
            )
            if i_hook_args is not None:
                i_session, i_execute_fnc = i_hook_args
                if i_session.get_is_loadable() is True:
                    i_gui_option = i_session.gui_configure
                    #
                    i_group_name = i_gui_option.get('group_name')
                    if i_group_name in self._list_view_dict:
                        i_list_view = self._list_view_dict[i_group_name]
                    else:
                        #
                        i_group = prx_widgets.PrxExpandedGroup()
                        self.add_widget(i_group)
                        i_group.set_name(i_group_name)
                        i_group.set_icon_by_name(i_group_name)
                        i_group.set_expanded(True)
                        #
                        i_list_view = prx_widgets.PrxListView()
                        i_group.add_widget(i_list_view)
                        #
                        i_list_view.set_item_frame_size_basic(48, 120)
                        #
                        i_list_view.set_item_name_frame_size(48, 72)
                        self._list_view_dict[i_group_name] = i_list_view
                    #
                    i_list_item = i_list_view.set_item_add()
                    i_name = i_gui_option.get('name')
                    i_tool_tip = i_gui_option.get('tool_tip')
                    i_list_item.set_name(i_name)
                    i_list_item.set_image_by_name(i_name)
                    i_list_item.connect_press_db_clicked_to(
                        i_execute_fnc
                    )
                    i_list_item.set_tool_tip(i_tool_tip)

                    i_list_item.set_menu_raw(
                        [
                            ('edit python-file', None, i_session.set_hook_python_file_open),
                            ('edit yaml-file', None, i_session.set_hook_yaml_file_open),
                        ]
                    )

    def test(self):
        pass


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = AppKit()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
