# coding:utf-8
import collections

import six

from lxbasic import bsc_configure, bsc_core

import lxresolver.scripts as rsv_scripts

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets


class AbsPnlToolKit(prx_widgets.PrxSessionWindow):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()
import lxsession.commands as ssn_commands; ssn_commands.set_hook_execute("dcc-tool-panels/gen-tool-kit")
    """
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlToolKit, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._scroll_bar = prx_widgets.PrxScrollArea()
        self.set_widget_add(self._scroll_bar)

        self.connect_refresh_action_to(self.refresh_all)

        self.refresh_all()

    def refresh_all(self):
        self._match_dict = rsv_scripts.ScpEnvironmentOpt.get_as_dict()
        self._tool_group_dict = {}
        #
        self._scroll_bar.restore()

        c = self._session.get_configure()

        self.build_tool_by_hook_data(c.get('hooks'))
        self.build_tool_by_option_hook_data(c.get('option-hooks'))

    def build_tool_by_hook_data(self, data):
        import lxsession.commands as ssn_commands

        d = 2

        with utl_core.GuiProgressesRunner.create(maximum=len(data), label='gui-add for hook') as g_p:
            for i_args in data:
                g_p.set_update()
                if isinstance(i_args, six.string_types):
                    i_key = i_args
                    i_extend_kwargs = {}
                    i_hook_args = ssn_commands.get_hook_args(
                        i_key
                    )
                elif isinstance(i_args, dict):
                    i_key = i_args.keys()[0]
                    i_extend_kwargs = i_args.values()[0]
                    i_hook_args = ssn_commands.get_hook_args(
                        i_key
                    )
                else:
                    raise RuntimeError()
                #
                if i_hook_args is not None:
                    i_session, i_execute_fnc = i_hook_args
                    if i_session.get_is_loadable() is True:
                        if i_session.get_is_match_condition(
                            self._match_dict
                        ) is True:
                            i_gui_configure = i_session.gui_configure
                            if 'gui_parent' in i_extend_kwargs:
                                i_gui_configure.set('group_name', i_extend_kwargs.get('gui_parent'))
                            #
                            i_group_name = i_gui_configure.get('group_name')
                            if i_group_name not in self._tool_group_dict:
                                i_expanded_group = prx_widgets.PrxExpandedGroup()
                                self._scroll_bar.set_widget_add(i_expanded_group)
                                i_expanded_group.set_name(i_group_name)
                                i_expanded_group.set_expanded(True)
                                #
                                i_tool_group = prx_widgets.PrxToolGroup()
                                i_expanded_group.set_widget_add(i_tool_group)
                                self._tool_group_dict[i_group_name] = i_tool_group
                            else:
                                i_tool_group = self._tool_group_dict[i_group_name]

                            i_name = i_gui_configure.get('name')
                            i_icon_name = i_gui_configure.get('icon_name')
                            i_tool_tip = i_gui_configure.get('tool_tip') or ''

                            i_press_item = prx_widgets.PrxPressItem()
                            i_tool_group.set_widget_add(i_press_item)
                            i_press_item.set_name(i_name)
                            if i_icon_name:
                                i_press_item.set_icon_name(i_icon_name)
                            else:
                                i_press_item.set_icon_color_by_name(i_name)

                            if i_session.configure.get('option.type').endswith('-panel'):
                                i_tool_tip = '"LMB-click" to open tool-panel'
                                i_press_item.set_option_click_enable(True)
                            else:
                                i_tool_tip = '"LMB-click" to execute'

                            i_press_item.set_tool_tip(i_tool_tip)

                            i_press_item.connect_press_clicked_to(
                                i_execute_fnc
                            )

    def build_tool_by_option_hook_data(self, data):
        import lxsession.commands as ssn_commands

        d = 2

        with utl_core.GuiProgressesRunner.create(maximum=len(data), label='gui-add for hook') as g_p:
            for i_args in data:
                g_p.set_update()
                if isinstance(i_args, six.string_types):
                    i_key = i_args
                    i_extend_kwargs = {}
                    i_hook_args = ssn_commands.get_option_hook_args(
                        i_key
                    )
                elif isinstance(i_args, dict):
                    i_key = i_args.keys()[0]
                    i_extend_kwargs = i_args.values()[0]
                    i_hook_args = ssn_commands.get_option_hook_args(
                        i_key
                    )
                else:
                    raise RuntimeError()
                #
                if i_hook_args is not None:
                    i_session, i_execute_fnc = i_hook_args
                    if i_session.get_is_loadable() is True:
                        if i_session.get_is_match_condition(
                                self._match_dict
                        ) is True:
                            i_gui_configure = i_session.gui_configure
                            if 'gui_parent' in i_extend_kwargs:
                                i_gui_configure.set('group_name', i_extend_kwargs.get('gui_parent'))
                            #
                            i_group_name = i_gui_configure.get('group_name')
                            if i_group_name not in self._tool_group_dict:
                                i_expanded_group = prx_widgets.PrxExpandedGroup()
                                self._scroll_bar.set_widget_add(i_expanded_group)
                                i_expanded_group.set_name(i_group_name)
                                i_expanded_group.set_expanded(True)
                                #
                                i_tool_group = prx_widgets.PrxToolGroup()
                                i_expanded_group.set_widget_add(i_tool_group)
                                self._tool_group_dict[i_group_name] = i_tool_group
                            else:
                                i_tool_group = self._tool_group_dict[i_group_name]

                            i_name = i_gui_configure.get('name')
                            i_icon_name = i_gui_configure.get('icon_name')
                            i_tool_tip = i_gui_configure.get('tool_tip') or ''

                            i_press_item = prx_widgets.PrxPressItem()
                            i_tool_group.set_widget_add(i_press_item)
                            i_press_item.set_name(i_name)
                            if i_icon_name:
                                i_press_item.set_icon_name(i_icon_name)
                            else:
                                i_press_item.set_icon_color_by_name(i_name)

                            if i_session.configure.get('option.type').endswith('-panel'):
                                i_tool_tip = '"LMB-click" to open tool-panel'
                                i_press_item.set_option_click_enable(True)
                            else:
                                i_tool_tip = '"LMB-click" to execute'

                            i_press_item.set_tool_tip(i_tool_tip)

                            i_press_item.connect_press_clicked_to(
                                i_execute_fnc
                            )
