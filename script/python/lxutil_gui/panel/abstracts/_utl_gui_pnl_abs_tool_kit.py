# coding:utf-8
import six

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
        self._tool_bar = prx_widgets.PrxHToolBar()
        self.set_widget_add(self._tool_bar)
        self._tool_bar.set_expanded(True)
        #
        self._scroll_bar = prx_widgets.PrxScrollArea()
        self.set_widget_add(self._scroll_bar)

        self._d = 2

        self.add_layout_buttons()

        self.connect_refresh_action_to(self.refresh_all)

        self.refresh_all()

    def add_layout_buttons(self):
        def click_fnc_(i_):
            _pre = self._d
            if i_ != _pre:
                self._d = i_
                self.build_tools()

        import functools

        for i in range(4):
            i_b = prx_widgets.PrxIconPressItem()
            self._tool_bar.set_widget_add(i_b)
            i_b.set_icon_by_name_text(str(i+1))
            i_b.connect_press_clicked_to(
                functools.partial(click_fnc_, i+1)
            )

    def refresh_all(self):
        import lxresolver.scripts as rsv_scripts

        self._match_dict = rsv_scripts.ScpEnvironment.get_as_dict()

        self.build_tools()

    def build_tools(self):
        self._tool_group_dict = {}
        self._scroll_bar.restore()
        c = self._session.get_configure()
        self.build_tool_by_hook_data(c.get('hooks'))
        self.build_tool_by_option_hook_data(c.get('option-hooks'))

    def build_tool_by_hook_data(self, data):
        import lxsession.commands as ssn_commands

        d = self._d

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
                    self.add_tool(i_hook_args, i_extend_kwargs, d)

    def build_tool_by_option_hook_data(self, data):
        import lxsession.commands as ssn_commands

        d = self._d

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
                    self.add_tool(i_hook_args, i_extend_kwargs, d)

    def add_tool(self, hook_args, extend_kwargs, d):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            if session.get_is_match_condition(
                    self._match_dict
            ) is True:
                gui_configure = session.gui_configure
                if 'gui_parent' in extend_kwargs:
                    gui_configure.set('group_name', extend_kwargs.get('gui_parent'))
                #
                group_name = gui_configure.get('group_name')
                if group_name not in self._tool_group_dict:
                    expanded_group = prx_widgets.PrxExpandedGroup()
                    self._scroll_bar.set_widget_add(expanded_group)
                    expanded_group.set_name(group_name)
                    expanded_group.set_expanded(True)
                    #
                    tool_group = prx_widgets.PrxButtonGroup()
                    expanded_group.set_widget_add(tool_group)
                    self._tool_group_dict[group_name] = tool_group
                else:
                    tool_group = self._tool_group_dict[group_name]

                name = gui_configure.get('name')
                icon_name = gui_configure.get('icon_name')
                tool_tip_ = gui_configure.get('tool_tip') or ''

                press_item = prx_widgets.PrxPressItem()
                tool_group.set_widget_add(press_item, d)
                press_item.set_name(name)
                if icon_name:
                    press_item.set_icon_name(icon_name)
                else:
                    press_item.set_icon_color_by_name(name)

                tool_tip = []
                if session.configure.get('option.type').endswith('-panel'):
                    tool_tip_add = '"LMB-click" to open tool-panel'
                    press_item.set_option_click_enable(True)
                else:
                    tool_tip_add = '"LMB-click" to execute'

                tool_tip.append(tool_tip_add)

                if isinstance(tool_tip_, (tuple, list)):
                    tool_tip.extend(tool_tip_)
                elif isinstance(tool_tip_, six.string_types):
                    tool_tip.append(tool_tip_)

                press_item.set_tool_tip(tool_tip)

                press_item.connect_press_clicked_to(
                    execute_fnc
                )
