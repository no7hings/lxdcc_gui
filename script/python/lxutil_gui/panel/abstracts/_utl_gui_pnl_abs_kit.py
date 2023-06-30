# coding:utf-8
import copy

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
    CUSTOMIZE_PATH = '/l/resource/td/user-resources'
    DEFAULT_GROUP_NAMES = [
        'Studio',
        'Share',
    ]
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
        group_name = self._options.get('gui.group_name')
        if group_name in self.DEFAULT_GROUP_NAMES:
            directory_path = '{}/hooks'.format(self.CUSTOMIZE_PATH)
        else:
            directory_path = '{}/hooks'.format(self.CUSTOMIZE_PATH)
        #
        name = self._options.get('name')
        if mode == 'create':
            if group_name in self.DEFAULT_GROUP_NAMES:
                hook_key = '{}/{}'.format(group_name, name)
            else:
                hook_key = '{}/User/{}'.format(group_name, name)
        else:
            hook_key = name
        #
        configure_file_path = '{}/{}.yml'.format(directory_path, hook_key)
        python_file_path = '{}/{}.py'.format(directory_path, hook_key)
        linux_file_path = '{}/{}.sh'.format(directory_path, hook_key)
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

        gui_name = self._options.get('gui.name')
        if not gui_name:
            gui_name = bsc_core.RawTextMtd.to_prettify(hook_key)
        #
        c.set('option.gui.name', gui_name)
        group_sub_name = self._options.get('gui.group_sub_name')
        if group_sub_name != 'None':
            c.set('option.gui.group_sub_name', group_sub_name)
        #
        icon_name = self._options.get('gui.icon_name')
        if icon_name != 'None':
            c.set('option.gui.icon_name', icon_name)
        if type_ == 'python-command':
            icon_sub_name = 'application/python'
        elif type_ == 'shell-command':
            icon_sub_name = 'application/shell'
        else:
            raise RuntimeError()
        c.set('option.gui.icon_sub_name', icon_sub_name)
        c.set('option.gui.tool_tip', self._options.get('gui.tool_tip'))
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

        self._window.gui_refresh_group(self._options.get('gui.group_name'))

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

    def restore_variants(self):
        self._group_names_all = HookAddOpt.DEFAULT_GROUP_NAMES
        self._group_names_current = copy.copy(
            HookAddOpt.DEFAULT_GROUP_NAMES
        )
        self._user_group_names_all = self.get_all_user_group_names()
        self._user_group_names_current = [
            bsc_core.SystemMtd.get_user_name()
        ]
        self._user_name_current = bsc_core.SystemMtd.get_user_name()
        self._hook_dict = {}
        self._option_hook_dict = {}
        #
        self._tool_group_layout_dict = {}
        self._tool_group_dict = {}
        self._tool_dict = {}

    def set_all_setup(self):
        self.set_main_style_mode(1)
        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)
        self._tab_view.set_add_enable(True)
        self._tab_view.set_add_menu_data_gain_fnc(self.tab_add_menu_gain_fnc)
        self._tab_view.set_current_changed_connect_to(self.save_tab_history)
        self._tab_view.connect_delete_accepted_to(self.gui_tab_delete_group_fnc)
        #
        self.build_create_layer()
        self.build_modify_layer()
        #
        self.gui_refresh_all()
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

        self.connect_refresh_action_to(
            self.refresh_current_group
        )

    def gui_tab_add_group_fnc(self, group_name):
        if group_name in self._group_names_all:
            self._group_names_current.append(group_name)
            self.gui_add_group_for(group_name)
        elif group_name in self._user_group_names_all:
            self._user_group_names_current.append(group_name)
            self.gui_add_group_for(group_name)

    def gui_tab_delete_group_fnc(self, group_name):
        if group_name in self._group_names_current:
            self._group_names_current.remove(group_name)
            self.gui_delete_group_for(group_name)
        elif group_name in self._user_group_names_current:
            self._user_group_names_current.remove(group_name)
            self.gui_delete_group_for(group_name)

    def tab_add_menu_gain_fnc(self):
        list_ = []
        for i_group_name in self._group_names_all:
            if i_group_name not in self._group_names_current:
                list_.append(
                    (
                        i_group_name, 'user', functools.partial(self.gui_tab_add_group_fnc, i_group_name)
                    )
                )
        if list_:
            list_.append(())
        user_group_names = self._user_group_names_all
        for i_user_group_name in user_group_names:
            if i_user_group_name not in self._user_group_names_current:
                list_.append(
                    (
                        i_user_group_name, 'user', functools.partial(self.gui_tab_add_group_fnc, i_user_group_name)
                    )
                )
        return list_

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
    @classmethod
    def get_all_user_group_names(cls):
        list_ = []
        directory_path = HookAddOpt.CUSTOMIZE_PATH
        user_directory_path = '{}/hooks/User'.format(directory_path)
        user_directory_opt = bsc_core.StgDirectoryOpt(user_directory_path)
        s = user_directory_opt.get_directory_paths()
        for i in s:
            list_.append(bsc_core.StgDirectoryOpt(i).get_name())
        return list_

    def gui_refresh_all(self):
        self._hook_dict = {}
        self._option_hook_dict = {}
        #
        self._tool_group_layout_dict = {}
        self._tool_group_dict = {}
        self._tool_dict = {}
        c = self._session.get_configure()
        ms = [
            (self.gui_build_for_customize, ()),
            #
            (self.gui_build_for_hook, (c.get('app.hooks') or [], )),
            (self.gui_build_for_option_hook, (c.get('app.option-hooks') or [], )),
        ]
        with utl_core.GuiProgressesRunner.create(maximum=len(ms), label='script gui-build method') as g_p:
            for i_m, i_as in ms:
                g_p.set_update()
                if i_as:
                    i_m(*i_as)
                else:
                    i_m()

    def gui_build_for_hook(self, data):
        with self.gui_progressing(maximum=len(data), label='gui-add for hook') as g_p:
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
                    self.gui_add_hook(i_hook_args, **i_extend_kwargs)

    def gui_build_for_option_hook(self, data):
        with self.gui_progressing(maximum=len(data), label='gui-add for option-hook') as g_p:
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
                    self.gui_add_option_hook(i_hook_args, **i_extend_kwargs)
    @classmethod
    def get_group_args(cls, session, **kwargs):
        gui_configure = session.gui_configure
        group_name = gui_configure.get('group_name')
        group_sub_name = gui_configure.get('group_sub_name') or 'Tool'
        if 'gui_parent' in kwargs:
            group_path = kwargs.get('gui_parent')
            group_opts = bsc_core.DccPathDagOpt(group_path).get_components()
            group_opt = group_opts[1]
            group_name = group_opt.get_name()
            group_sub_opt = group_opts[0]
            group_sub_name = group_sub_opt.get_name()
        #
        if 'group_name' in kwargs:
            group_name = kwargs['group_name']
        #
        if 'group_sub_name' in kwargs:
            group_sub_name = kwargs['group_sub_name']
        #
        gui_configure.set('group_name', group_name)
        gui_configure.set('group_sub_name', group_sub_name)
        return group_name, group_sub_name

    def gui_get_group_args(self, group_name, tool_data=None):
        group_path = '/{}'.format(group_name)
        if group_path in self._tool_group_layout_dict:
            layout = self._tool_group_layout_dict[group_path]
        else:
            scroll_area = prx_widgets.PrxVScrollArea()
            self._tab_view.create_item(
                scroll_area,
                name=group_name,
                icon_name_text=group_name,
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
                # for i_data in tool_data:
                #     i_tool_box_name, i_tool_data = i_data
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
            #
            layout = qt_widgets.QtVBoxLayout(w_1)
            layout.setContentsMargins(0, 0, 0, 0)
            self._tool_group_layout_dict[group_path] = layout
        return layout

    def gui_get_view_args(self, group_name=None, group_sub_name=None, tool_data=None, group_name_over=None):
        group_path = '/{}'.format(group_name)
        if group_path in self._tool_group_layout_dict:
            layout = self._tool_group_layout_dict[group_path]
        else:
            scroll_area = prx_widgets.PrxVScrollArea()
            self._tab_view.create_item(
                scroll_area,
                name=group_name_over or group_name,
                icon_name_text=group_name_over or group_name,
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
                # for i_data in tool_data:
                #     i_tool_box_name, i_tool_data = i_data
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
            #
            layout = qt_widgets.QtVBoxLayout(w_1)
            layout.setContentsMargins(0, 0, 0, 0)
            self._tool_group_layout_dict[group_path] = layout
        #
        group_sub_path = '/{}/{}'.format(group_name, group_sub_name)
        if group_sub_path in self._tool_group_dict:
            tool_group, layout_view = self._tool_group_dict[group_sub_path]
        else:
            tool_group = prx_widgets.PrxHToolGroup_()
            layout.addWidget(tool_group._qt_widget)

            tool_group.set_size_mode(1)
            tool_group.set_name(group_sub_name)
            tool_group.set_expanded(True)
            #
            layout_view = prx_widgets.PrxLayoutView()
            self._tool_group_dict[group_sub_path] = tool_group, layout_view
            tool_group.add_widget(layout_view)
            layout_view.set_item_size(*self.session.gui_configure.get('item_frame_size'))
        return layout_view

    def gui_build_for_customize(self):
        for i_group_name in HookAddOpt.DEFAULT_GROUP_NAMES:
            self.gui_add_customize_by_group_name(i_group_name)
        #
        group_names = self._user_group_names_current
        for i_group_name in group_names:
            self.gui_add_customize_by_group_name(i_group_name)

    def gui_add_hook(self, hook_args, **kwargs):
        session, _ = hook_args
        group_name, group_sub_name = self.get_group_args(
            session, **kwargs
        )
        self._hook_dict.setdefault(
            group_name, []
        ).append(
            (hook_args, group_name, group_sub_name)
        )
        self.add_tool(
            hook_args, group_name, group_sub_name
        )

    def gui_add_option_hook(self, hook_args, **kwargs):
        session, _ = hook_args
        group_name, group_sub_name = self.get_group_args(
            session, **kwargs
        )
        self._option_hook_dict.setdefault(
            group_name, []
        ).append(
            (hook_args, group_name, group_sub_name)
        )
        self.add_option_tool(
            hook_args, group_name, group_sub_name
        )

    def gui_add_by_group_name_from_cache(self, group_name):
        if group_name in self._hook_dict:
            hook_data = self._hook_dict[group_name]
            for i_hook_args, i_group_name, i_grou_sub_name in hook_data:
                self.add_tool(
                    i_hook_args, i_group_name, i_grou_sub_name
                )
        if group_name in self._option_hook_dict:
            option_hook_data = self._option_hook_dict[group_name]
            for i_hook_args, i_group_name, i_grou_sub_name in option_hook_data:
                self.add_option_tool(
                    i_hook_args, i_group_name, i_grou_sub_name
                )

    def gui_add_customize_by_group_name(self, group_name):
        self.gui_get_group_args(
            group_name,
            tool_data=[
                ('create new for share', 'file/add-file', functools.partial(self.show_create_fnc, group_name)),
            ]
        )
        directory_path = HookAddOpt.CUSTOMIZE_PATH
        hook_keys = HookAddOpt.get_all_hook_keys_from_fnc(directory_path)
        hook_keys_matched = bsc_core.PtnFnmatch.filter(
            hook_keys, '*{}/*'.format(group_name)
        )
        if hook_keys_matched:
            with self.gui_progressing(maximum=len(hook_keys_matched), label='build for'.format(group_name)) as g_p:
                for i_hook_key in hook_keys_matched:
                    g_p.set_update()
                    self.add_customize_by_hook_key(i_hook_key, group_name)

    def add_customize_by_hook_key(self, hook_key, group_name):
        directory_path = HookAddOpt.CUSTOMIZE_PATH
        hook_args = ssn_commands.get_hook_args(
            hook_key, search_paths=[directory_path]
        )
        session, _ = hook_args
        group_name, group_sub_name = self.get_group_args(
            session, group_name=group_name
        )
        self.add_tool(
            hook_args,
            group_name, group_sub_name,
            menu_data=[
                ('modify', 'file/file', functools.partial(self.show_modify_fnc, session)),
                (),
                ('open folder', 'file/folder', session.open_configure_directory),
                (),
            ]
        )

    def show_create_fnc(self, group_name):
        self.show_layer('create_layer')
        self._create_option_prx_node.set('gui.group_name', group_name)

    def show_modify_fnc(self, session):
        self.show_layer('modify_layer')
        gui_configure = session.get_gui_configure()
        type_ = session.get_type()
        configure_file_path = session.get_configure_yaml_file()
        configure_file_opt = bsc_core.StgFileOpt(configure_file_path)
        self._modify_option_prx_node.set('type', session.get_type())
        self._modify_option_prx_node.set('name', session.get_name())
        self._modify_option_prx_node.set('gui.name', gui_configure.get('name'))
        self._modify_option_prx_node.set('gui.group_name', gui_configure.get('group_name'))
        self._modify_option_prx_node.set('gui.group_sub_name', gui_configure.get('group_sub_name'))
        self._modify_option_prx_node.set('gui.icon_name', gui_configure.get('icon_name'))
        self._modify_option_prx_node.set('gui.icon_sub_name', gui_configure.get('icon_sub_name'))
        self._modify_option_prx_node.set('gui.tool_tip', gui_configure.get('tool_tip'))
        python_file_path = '{}.py'.format(configure_file_opt.path_base)
        if bsc_core.StgPathMtd.get_is_file(python_file_path):
            self._modify_option_prx_node.set(
                'script.python', bsc_core.StgFileOpt(python_file_path).set_read()
            )
        else:
            self._modify_option_prx_node.set(
                'script.python', ''
            )
        windows_shell_file_path = '{}.bat'.format(configure_file_opt.path_base)
        if bsc_core.StgPathMtd.get_is_file(windows_shell_file_path):
            self._modify_option_prx_node.set(
                'script.windows', bsc_core.StgFileOpt(windows_shell_file_path).set_read()
            )
        else:
            self._modify_option_prx_node.set(
                'script.windows', ''
            )
        linux_shell_file_path = '{}.sh'.format(configure_file_opt.path_base)
        if bsc_core.StgPathMtd.get_is_file(linux_shell_file_path):
            self._modify_option_prx_node.set(
                'script.linux', bsc_core.StgFileOpt(linux_shell_file_path).set_read()
            )
        else:
            self._modify_option_prx_node.set(
                'script.linux', ''
            )

    def gui_delete_group_for(self, group_name):
        self.gui_delete_tool_groups_for(group_name)
        group_path = '/{}'.format(group_name)
        self._tool_group_layout_dict.pop(group_path)

    def gui_add_group_for(self, group_name):
        self.gui_add_customize_by_group_name(group_name)
        self.gui_add_by_group_name_from_cache(group_name)

    def gui_delete_tool_groups_for(self, group_name):
        tool_group_keys = self._tool_group_dict.keys()
        tool_group_keys_matched = bsc_core.PtnFnmatch.filter(
            tool_group_keys, '/{}/*'.format(group_name)
        )
        if tool_group_keys_matched:
            [self._tool_group_dict.pop(i) for i in tool_group_keys_matched]

        #
        tool_keys = self._tool_dict.keys()
        tool_keys_matched = bsc_core.PtnFnmatch.filter(
            tool_keys, '/{}/*'.format(group_name)
        )
        if tool_keys_matched:
            [self._tool_dict.pop(i) for i in tool_keys_matched]
        #
        group_path = '/{}'.format(group_name)
        if group_path in self._tool_group_layout_dict:
            layout = self._tool_group_layout_dict[group_path]
            layout._clear_all_widgets_()

    def gui_refresh_group(self, group_name):
        self.gui_delete_tool_groups_for(group_name)
        self.gui_add_customize_by_group_name(group_name)
        self.gui_add_by_group_name_from_cache(group_name)

    def refresh_current_group(self):
        name = self._tab_view.get_current_name()
        if name in HookAddOpt.DEFAULT_GROUP_NAMES:
            self.gui_refresh_group(
                self._tab_view.get_current_name()
            )
        elif name in [
            self._user_name_current
        ]:
            self.gui_refresh_group(
                self._tab_view.get_current_name()
            )

    def _execute_fnc_as_bustling_(self, fnc):
        with self.gui_bustling():
            fnc()

    def add_tool(self, hook_args, group_name, group_sub_name, menu_data=None):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            key = session.get_name()
            gui_configure = session.gui_configure
            layout_view = self.gui_get_view_args(
                group_name, group_sub_name
            )
            app_path = '/{}/{}/{}'.format(group_name, group_sub_name, key)
            if app_path in self._tool_dict:
                prx_item = self._tool_dict[app_path]
            else:
                prx_item = prx_widgets.PrxIconPressItem()
                self._tool_dict[app_path] = prx_item
                layout_view.add_item(prx_item)
                session.set_gui(prx_item._qt_widget)
                prx_item.connect_press_db_clicked_to(execute_fnc)
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
            prx_item.set_tool_tip(tool_tip)
            return prx_item

    def add_option_tool(self, hook_args, group_name, group_sub_name, menu_data=None):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            gui_configure = session.gui_configure
            layout_view = self.gui_get_view_args(
                group_name, group_sub_name
            )
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

    def gui_get_view_args(self, group_path):
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

    def add_tool(self, hook_args, kwargs_extend):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            if session.get_is_match_condition(
                self._match_dict
            ) is True:
                gui_configure = session.gui_configure
                if 'gui_parent' in kwargs_extend:
                    gui_configure.set('group_name', kwargs_extend.get('gui_parent'))
                #
                group_path = gui_configure.get('group_name')
                layout_view = self.gui_get_view_args(group_path)
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
