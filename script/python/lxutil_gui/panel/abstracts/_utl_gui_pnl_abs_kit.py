# coding:utf-8
import six

import os

import functools

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

from lxutil_gui import utl_gui_core

import lxutil_gui.qt.widgets as qt_widgets

import lxutil_gui.proxy.widgets as prx_widgets

import lxsession.commands as ssn_commands


class HookAddOpt(object):
    CUSTOMIZE_PATH = '/l/resource/td/customize-resource'
    SHARE_GROUP_PATH = '/Share/Tool'
    USER_GROUP_PATH = '/User/Tool'
    def __init__(self, window, session, options):
        self._window = window
        self._session = session
        self._options = options

    def get_is_exists(self):
        pass
    @classmethod
    def get_share_directory(cls):
        return cls.CUSTOMIZE_PATH + '/share'
    @classmethod
    def get_user_directory(cls):
        return cls.CUSTOMIZE_PATH + '/{}'.format(bsc_core.SystemMtd.get_user_name())
    @classmethod
    def get_all_hook_keys_from_fnc(cls, path):
        list_ = []
        for i in [path + '/hooks']:
            for j in bsc_core.StgDirectoryOpt(i).get_all_file_paths(include_exts=['.yml']) or []:
                j_name = bsc_core.StgFileOpt(j).get_path_base()[len(i)+1:]
                list_.append(j_name)
        return list_

    def accept_create(self, mode='create'):
        space = self._options.get('space')
        if space == 'share':
            directory_path = self.get_share_directory()
        elif space == 'user':
            directory_path = self.get_user_directory()
        else:
            raise RuntimeError()
        #
        hook_key = self._options.get('name')

        configure_file_path = '{}/hooks/{}.yml'.format(directory_path, hook_key)
        python_file_path = '{}/hooks/{}.py'.format(directory_path, hook_key)
        linux_file_path = '{}/hooks/{}.sh'.format(directory_path, hook_key)
        windows_file_path = '{}/{}.bat'.format(directory_path, hook_key)
        configure_file_opt = bsc_core.StgFileOpt(configure_file_path)
        if mode is 'create':
            if configure_file_opt.get_is_file() is True:
                utl_core.DialogWindow.set_create(
                    self._session.gui_name,
                    content='app is exists, entry a new name to continue',
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    yes_visible=False,
                    no_visible=False,
                )
                return
        #
        default_configue_file_path = bsc_core.CfgFileMtd.get(
            'session/default-hook-configure.yml'
        )
        c = bsc_objects.Content(value=default_configue_file_path)

        type_ = self._options.get('type')
        c.set('option.type', type_)
        if type_ == 'python-command':
            icon_sub_name = 'application/python'
        elif type_ == 'shell-command':
            icon_sub_name = 'application/shell'
        else:
            raise RuntimeError()

        gui_name = self._options.get('gui.name')
        if not gui_name:
            gui_name = bsc_core.RawTextMtd.to_prettify(hook_key)
        #
        c.set('option.gui.name', gui_name)

        c.set('option.gui.tool_tip', self._options.get('gui.tool_tip'))
        gui_icon_name = self._options.get('gui.icon_name')
        c.set('option.gui.icon_sub_name', icon_sub_name)
        #
        python_script = self._options.get('script.python')
        windows_shell_script = self._options.get('script.windows')
        linux_shell_script = self._options.get('script.linux')

        bsc_core.StgPathPermissionMtd.create_directory(
            bsc_core.StgFileMtd.get_directory(configure_file_path)
        )

        if type_ == 'python-command':
            if not python_script:
                utl_core.DialogWindow.set_create(
                    self._session.gui_name,
                    content='python script is empty, entry script to continue',
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    yes_visible=False,
                    no_visible=False,
                )
                return
            #
            bsc_core.StgFileOpt(python_file_path).set_write(
                python_script
            )
        elif type_ == 'shell-command':
            if (not windows_shell_script) and (not linux_shell_script):
                utl_core.DialogWindow.set_create(
                    self._session.gui_name,
                    content='shell script is empty, entry script to continue',
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    yes_visible=False,
                    no_visible=False,
                )
                return
            if windows_shell_script:
                bsc_core.StgFileOpt(windows_file_path).set_write(
                    windows_shell_script
                )
            if linux_shell_script:
                bsc_core.StgFileOpt(linux_file_path).set_write(
                    linux_shell_script
                )
        else:
            raise RuntimeError()

        c.set_save_to(configure_file_path)

        if space == 'share':
            self._window.add_for_share(
                hook_key
            )
        elif space == 'user':
            self._window.add_for_user(
                hook_key
            )
        self._window.show_main_layer()

    def accept_modify(self):
        pass


class AbsPnlAppKit(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlAppKit, self).__init__(session, *args, **kwargs)

    def _set_environ_show_(self):
        utl_core.DialogWindow.set_create(
            'environ',
            content=u'\n'.join(
                [u'{} = {}'.format(k, v) for k, v in bsc_core.DictMtd.sort_key_to(os.environ).items()]
            ),
            window_size=(960, 480),
            yes_visible=False,
            no_visible=False,
            cancel_label='Close'
        )

    def _set_rez_graph_show_(self):
        _ = os.environ.get('REZ_USED_REQUEST')
        if _:
            packages = _.split(' ')

            from lxutil_gui.qt import utl_gui_qt_core

            import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

            _option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    packages=packages
                )
            )

            utl_gui_qt_core.set_window_show_standalone(
                utl_pnl_widgets.RezGraph, hook_option=_option_opt.to_string()
            )

    def save_tab_history(self):
        current_name = self._tab_view.get_current_name()
        utl_core.History.set_one('app-kit.tab', current_name)

    def set_all_setup(self):
        self.set_main_style_mode(1)
        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)
        self._tab_view.set_current_changed_connect_to(
            self.save_tab_history
        )

        self.build_apps()
        self.build_create_layer()
        self.build_modify_layer()
        #
        menu = self.create_menu('debug')
        menu.set_menu_data(
            [
                ('show environ', None, self._set_environ_show_),
                ('show rez graph', None, self._set_rez_graph_show_),
            ]
        )
        #
        self._tab_view.set_current_by_name(
            utl_core.History.get_one('app-kit.tab')
        )

    def build_create_layer(self):
        layer_widget = self.create_layer_widget('create_layer', 'Create')
        sa_2 = prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(sa_2)
        self._create_option_prx_node = prx_widgets.PrxNode_('options')
        self._create_option_prx_node.create_ports_by_configure(
            self._session.configure.get('build.node.create_options'),
        )
        sa_2.add_widget(self._create_option_prx_node.widget)

        text_browser = prx_widgets.PrxTextBrowser()
        sa_2.add_widget(text_browser)
        text_browser.set_content(
            self._session.configure.get('build.node.create_content')
        )
        text_browser.set_font_size(12)
        #
        tool_bar = prx_widgets.PrxHToolBar()
        sa_2.add_widget(tool_bar.widget)
        tool_bar.set_expanded(True)
        button = prx_widgets.PrxPressItem()
        tool_bar.add_widget(button)
        button.set_name('Apply')
        button.connect_press_clicked_to(
            self.create_apply_fnc
        )

    def build_modify_layer(self):
        layer_widget = self.create_layer_widget('modify_layer', 'Modify')
        sa_2 = prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(sa_2)
        self._modify_option_prx_node = prx_widgets.PrxNode_('options')
        self._modify_option_prx_node.create_ports_by_configure(
            self._session.configure.get('build.node.modify_options'),
        )
        sa_2.add_widget(self._modify_option_prx_node.widget)

        text_browser = prx_widgets.PrxTextBrowser()
        sa_2.add_widget(text_browser)
        text_browser.set_content(
            self._session.configure.get('build.node.modify_content')
        )
        text_browser.set_font_size(12)
        #
        tool_bar = prx_widgets.PrxHToolBar()
        sa_2.add_widget(tool_bar.widget)
        tool_bar.set_expanded(True)
        button = prx_widgets.PrxPressItem()
        tool_bar.add_widget(button)
        button.set_name('Apply')
        button.connect_press_clicked_to(
            self.modify_apply_fnc
        )

    def create_apply_fnc(self):
        options = self._create_option_prx_node.get_as_kwargs()
        HookAddOpt(
            self,
            self._session,
            options
        ).accept_create()

    def modify_apply_fnc(self):
        options = self._modify_option_prx_node.get_as_kwargs()
        HookAddOpt(
            self,
            self._session,
            options
        ).accept_create(mode='modify')

    def build_apps(self):
        self._scroll_area_dict = {}
        self._tool_group_dict = {}
        self._view_dict = {}
        self._app_dict = {}
        c = self._session.get_configure()
        ms = [
            (self.build_app_hook_data, (c.get('app.hooks') or [], )),
            (self.build_by_option_hook_data, (c.get('app.option-hooks') or [], )),
            (self.build_for_share, ()),
            (self.build_for_user, ()),
        ]

        with utl_core.GuiProgressesRunner.create(maximum=len(ms), label='script gui-build method') as g_p:
            for i_m, i_as in ms:
                g_p.set_update()
                if i_as:
                    i_m(*i_as)
                else:
                    i_m()

        # self.show_option_unit()

    def get_view_args(self, group_path, tool_data=None, tab_name=None):
        group_opts = bsc_core.DccPathDagOpt(group_path).get_components()
        group_main_opt = group_opts[1]
        group_main_path = group_main_opt.get_path()
        if group_main_path in self._scroll_area_dict:
            layout = self._scroll_area_dict[group_main_path]
        else:
            scroll_area = prx_widgets.PrxVScrollArea()
            self._tab_view.create_item(
                scroll_area,
                name=tab_name or group_main_opt.get_name(),
                icon_name_text=group_main_opt.get_path(),
            )
            #
            w_0 = qt_widgets.QtWidget()
            scroll_area.add_widget(w_0)
            l_0 = qt_widgets.QtVBoxLayout(w_0)
            l_0.setContentsMargins(0, 0, 0, 0)
            #
            top_tool_bar = prx_widgets.PrxHToolBar()
            l_0.addWidget(top_tool_bar._qt_widget)
            top_tool_bar.set_expanded(True)
            top_tool_bar.set_left_alignment_mode()
            #
            if tool_data:
                tool_box = prx_widgets.PrxHToolBox_()
                top_tool_bar.add_widget(tool_box)
                tool_box.set_expanded(True)
                for i_data in tool_data:
                    i_name, i_icon_name, i_fnc = i_data
                    i_tool = prx_widgets.PrxIconPressItem()
                    tool_box.add_widget(i_tool)
                    i_tool.set_name(i_name)
                    i_tool.set_icon_name(i_icon_name)
                    i_tool.connect_press_clicked_to(i_fnc)
            #
            w_1 = qt_widgets.QtWidget()
            l_0.addWidget(w_1)
            layout = qt_widgets.QtVBoxLayout(w_1)
            layout.setContentsMargins(0, 0, 0, 0)
            self._scroll_area_dict[group_main_path] = layout
        #
        group_sub_opt = group_opts[0]
        group_sub_path = group_sub_opt.get_path()
        if group_sub_path in self._view_dict:
            tool_group = self._tool_group_dict[group_main_path]
            layout_view = self._view_dict[group_sub_path]
        else:
            tool_group = prx_widgets.PrxHToolGroup_()
            self._tool_group_dict[group_main_path] = tool_group
            layout.addWidget(tool_group._qt_widget)

            tool_group.set_size_mode(1)
            tool_group.set_name(group_sub_opt.get_name())
            tool_group.set_expanded(True)
            #
            layout_view = prx_widgets.PrxLayoutView()
            self._view_dict[group_sub_path] = layout_view
            tool_group.add_widget(layout_view)
            layout_view.set_item_size(*self.session.gui_configure.get('item_frame_size'))

        return layout_view

    def build_app_hook_data(self, data):
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
                    self.add_one(i_hook_args, i_extend_kwargs)

    def build_by_option_hook_data(self, data):
        with utl_core.GuiProgressesRunner.create(maximum=len(data), label='gui-add for option-hook') as g_p:
            for i_args in data:
                g_p.set_update()
                if isinstance(i_args, six.string_types):
                    i_key = i_args
                    i_extend_kwargs = {}
                    i_hook_option = 'option_hook_key={}'.format(i_key)
                    i_hook_args = ssn_commands.get_option_hook_args(
                        i_hook_option
                    )
                elif isinstance(i_args, dict):
                    i_key = i_args.keys()[0]
                    i_extend_kwargs = i_args.values()[0]
                    i_hook_option = 'option_hook_key={}'.format(i_key)
                    i_hook_args = ssn_commands.get_option_hook_args(
                        i_hook_option
                    )
                else:
                    raise RuntimeError()
                #
                if i_hook_args is not None:
                    self.add_option_one(i_hook_args, i_extend_kwargs)

    def build_for_share(self):
        group_path = HookAddOpt.SHARE_GROUP_PATH
        self.get_view_args(
            group_path,
            tool_data=[
                ('create new for share', 'file/add-file', functools.partial(self.show_create_fnc, 'share')),
            ]
        )
        directory_path = HookAddOpt.get_share_directory()
        hook_keys = HookAddOpt.get_all_hook_keys_from_fnc(directory_path)
        for i_hook_key in hook_keys:
            self.add_for_share(i_hook_key)

    def add_for_share(self, hook_key):
        group_path = HookAddOpt.SHARE_GROUP_PATH
        extend_kwargs = dict(gui_parent=group_path)
        directory_path = HookAddOpt.get_share_directory()
        hook_args = ssn_commands.get_hook_args(
            hook_key, search_paths=[directory_path]
        )
        session = hook_args[0]
        self.add_one(
            hook_args, extend_kwargs,
            menu_data=[
                ('modify', 'file/file', functools.partial(self.show_modify_fnc, session, 'share')),
                (),
                ('open folder', 'file/folder', session.open_configure_directory),
                (),
            ]
        )

    def build_for_user(self):
        group_path = HookAddOpt.USER_GROUP_PATH
        self.get_view_args(
            group_path,
            tool_data=[
                ('create new for user', 'file/add-file', functools.partial(self.show_create_fnc, 'user')),
            ],
            tab_name=bsc_core.SystemMtd.get_user_name()
        )
        #
        directory_path = HookAddOpt.get_user_directory()
        hook_keys = HookAddOpt.get_all_hook_keys_from_fnc(directory_path)
        for i_hook_key in hook_keys:
            self.add_for_user(i_hook_key)

    def add_for_user(self, hook_key):
        group_path = HookAddOpt.USER_GROUP_PATH
        extend_kwargs = dict(gui_parent=group_path)
        directory_path = HookAddOpt.get_user_directory()
        hook_args = ssn_commands.get_hook_args(
            hook_key, search_paths=[directory_path]
        )
        session = hook_args[0]
        self.add_one(
            hook_args, extend_kwargs,
            menu_data=[
                ('modify', 'file/file', functools.partial(self.show_modify_fnc, session, 'user')),
                (),
                ('open folder', 'file/folder', session.open_configure_directory),
                (),
            ]
        )

    def show_create_fnc(self, space):
        self.show_layer('create_layer')
        self._create_option_prx_node.set('space', space)
        if space == 'share':
            self._create_option_prx_node.set('gui.group_name', HookAddOpt.SHARE_GROUP_PATH)
        elif space == 'user':
            self._create_option_prx_node.set('gui.group_name', HookAddOpt.USER_GROUP_PATH)

    def show_modify_fnc(self, session, space):
        self.show_layer('modify_layer')
        gui_configure = session.get_gui_configure()
        type_ = session.get_type()
        configure_file_path = session.get_configure_yaml_file()
        configure_file_opt = bsc_core.StgFileOpt(configure_file_path)
        self._modify_option_prx_node.set('space', space)
        self._modify_option_prx_node.set('type', session.get_type())
        self._modify_option_prx_node.set('name', session.get_name())
        self._modify_option_prx_node.set('gui.name', gui_configure.get('name'))
        self._modify_option_prx_node.set('gui.group_name', gui_configure.get('group_name'))
        self._modify_option_prx_node.set('gui.tool_tip', gui_configure.get('tool_tip'))
        if type_ == 'python-command':
            python_file_path = '{}.py'.format(configure_file_opt.path_base)
            if bsc_core.StgPathMtd.get_is_file(python_file_path):
                self._modify_option_prx_node.set(
                    'script.python', bsc_core.StgFileOpt(python_file_path).set_read()
                )
        elif type_ == 'shell-command':
            windows_shell_file_path = '{}.bat'.format(configure_file_opt.path_base)
            if bsc_core.StgPathMtd.get_is_file(windows_shell_file_path):
                self._modify_option_prx_node.set(
                    'windows.linux', bsc_core.StgFileOpt(windows_shell_file_path).set_read()
                )
            linux_shell_file_path = '{}.sh'.format(configure_file_opt.path_base)
            if bsc_core.StgPathMtd.get_is_file(linux_shell_file_path):
                self._modify_option_prx_node.set(
                    'script.linux', bsc_core.StgFileOpt(linux_shell_file_path).set_read()
                )

    def add_one(self, hook_args, extend_kwargs, menu_data=None):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            key = session.get_name()
            gui_configure = session.gui_configure
            if 'gui_parent' in extend_kwargs:
                gui_configure.set('group_name', extend_kwargs.get('gui_parent'))
            #
            group_path = gui_configure.get('group_name')
            layout_view = self.get_view_args(group_path)
            #
            app_path = '{}/{}'.format(group_path, key)
            if app_path in self._app_dict:
                prx_item = self._app_dict[app_path]
            else:
                prx_item = prx_widgets.PrxIconPressItem()
                self._app_dict[app_path] = prx_item
                layout_view.add_item(prx_item)
            #
            name = gui_configure.get('name')
            icon_name = gui_configure.get('icon_name')
            icon_sub_name = gui_configure.get('icon_sub_name')
            tool_tip = gui_configure.get('tool_tip')
            prx_item.set_name(name)
            if icon_name:
                prx_item.set_icon_name(icon_name)
            else:
                prx_item.set_icon_by_text(name)
            #
            if icon_sub_name:
                prx_item.set_icon_sub_name(icon_sub_name)
            #
            if menu_data is not None:
                prx_item.set_menu_data(menu_data)
            #
            prx_item.connect_press_db_clicked_to(
                execute_fnc
            )
            prx_item.set_tool_tip(tool_tip)
            return prx_item

    def add_option_one(self, hook_args, extend_kwargs):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            gui_configure = session.gui_configure
            if 'gui_parent' in extend_kwargs:
                gui_configure.set('group_name', extend_kwargs.get('gui_parent'))
            #
            group_path = gui_configure.get('group_name')
            layout_view = self.get_view_args(group_path)
            #
            prx_item = prx_widgets.PrxIconPressItem()
            layout_view.add_item(prx_item)
            name = gui_configure.get('name')
            icon_name = gui_configure.get('icon_name')
            icon_sub_name = gui_configure.get('icon_sub_name')
            tool_tip = gui_configure.get('tool_tip') or ''
            prx_item.set_name(name)
            if icon_name:
                prx_item.set_icon_name(icon_name)
            else:
                prx_item.set_icon_by_text(name)
            #
            if icon_sub_name:
                prx_item.set_icon_sub_name(icon_sub_name)
            #
            prx_item.connect_press_db_clicked_to(
                execute_fnc
            )
            prx_item.set_tool_tip(tool_tip)
            #
            i_hs = session.get_extra_hook_options()

            i_menu_content = ssn_commands.get_menu_content_by_hook_options(i_hs)

            prx_item.set_menu_content(
                i_menu_content
            )


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
        self._top_prx_tool_bar = prx_widgets.PrxHToolBar()
        self.add_widget(self._top_prx_tool_bar)
        self._top_prx_tool_bar.set_expanded(True)
        self._top_prx_tool_bar.set_left_alignment_mode()

        self._switch_tool_box = prx_widgets.PrxHToolBox()
        self._top_prx_tool_bar.add_widget(self._switch_tool_box)
        self._switch_tool_box.set_expanded(True)

        self._filter_tool_box = prx_widgets.PrxHToolBox()
        self._top_prx_tool_bar.add_widget(self._filter_tool_box)

        self._filter_bar = prx_widgets.PrxFilterBar()
        self._filter_tool_box.add_widget(self._filter_bar)

        self._scroll_bar = prx_widgets.PrxVScrollArea()
        self.add_widget(self._scroll_bar)

        self._w_p, self._h_p = .5, .25

        self._w = 440
        self._h = 80

        self._percent_args = [('small', .25, .25), ('medium', 0.5, .25), ('large', 1.0, .25)]

        self.add_layout_buttons()

        self.connect_refresh_action_to(self.refresh_all)

        self.refresh_all()

    def add_layout_buttons(self):
        def click_fnc_(p_):
            _pre = self._w_p, self._h_p
            if p_ != _pre:
                _w_p, _h_p = p_
                self._w_p, self._h_p = _w_p, _h_p
                for k, v in self._view_dict.items():
                    v.set_item_size(
                        self._w*self._w_p, self._h*self._h_p
                    )
                    v.refresh_widget()

        import functools
        tools = []
        for i_key, i_w_p, i_h_p in self._percent_args:
            i_b = prx_widgets.PrxEnableItem()
            self._switch_tool_box.add_widget(i_b)
            i_b.set_icon_name('tool/icon-{}'.format(i_key))
            if i_w_p == self._w_p:
                i_b.set_checked(True)
            i_b.connect_check_changed_as_exclusive_to(
                functools.partial(click_fnc_, (i_w_p, i_h_p))
            )
            i_b._qt_widget._set_exclusive_widgets_(tools)
            tools.append(i_b._qt_widget)

    def refresh_all(self):
        import lxresolver.scripts as rsv_scripts

        self._match_dict = rsv_scripts.ScpEnvironment.get_as_dict()

        self.build_tools()

    def build_tools(self):
        self._view_dict = {}
        self._scroll_bar.restore()
        c = self._session.get_configure()
        self.build_tool_by_hook_data(c.get('hooks') or [])
        self.build_tool_by_option_hook_data(c.get('option-hooks') or [])

    def get_view_args(self, group_path):
        if group_path not in self._view_dict:
            tool_group = prx_widgets.PrxHToolGroup_()
            self._scroll_bar.add_widget(tool_group)
            tool_group.set_expanded(True)
            tool_group.set_name(group_path)
            #
            layout_view = prx_widgets.PrxLayoutView()
            self._view_dict[group_path] = layout_view
            tool_group.add_widget(layout_view)
            layout_view.set_item_size(self._w*self._w_p, self._h*self._h_p)
        else:
            layout_view = self._view_dict[group_path]
        return layout_view

    def build_tool_by_hook_data(self, data):
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
                    self.add_tool(i_hook_args, i_extend_kwargs)

    def build_tool_by_option_hook_data(self, data):
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
                    self.add_tool(i_hook_args, i_extend_kwargs)

    def add_tool(self, hook_args, extend_kwargs):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            if session.get_is_match_condition(
                self._match_dict
            ) is True:
                gui_configure = session.gui_configure
                if 'gui_parent' in extend_kwargs:
                    gui_configure.set('group_name', extend_kwargs.get('gui_parent'))
                #
                group_path = gui_configure.get('group_name')
                layout_view = self.get_view_args(group_path)
                #
                name = gui_configure.get('name')
                icon_name = gui_configure.get('icon_name')
                tool_tip_ = gui_configure.get('tool_tip') or ''

                press_item = prx_widgets.PrxPressItem()
                layout_view.add_item(press_item)
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
