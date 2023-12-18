# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.session.core as bsc_ssn_core

import lxresource.core as rsc_core

import lxcontent.core as ctt_core

import lxgui.core as gui_core


class KitDesktopHook(object):
    class PageKey(object):
        Department = 'Department'
        User = 'User'

    DEFAULT_PAGE_KEYS = [
        'Studio',
        'Share',
    ]

    @classmethod
    def get_args(cls, key):
        _ = rsc_core.ResourceDesktopTool.get_args(
                key
            )
        if _:
            hook_type, hook_key, hook_configure, yaml_file_path, python_file_path, shell_file_path = _

            session = bsc_ssn_core.CommandSession(
                type=hook_type,
                hook=hook_key,
                configure=hook_configure
            )
            session.set_configure_yaml_file(yaml_file_path)
            if python_file_path is not None:
                session.set_python_script_file(python_file_path)
            if shell_file_path:
                session.set_shell_script_file(shell_file_path)

            fnc = functools.partial(session.execute)
            return session, fnc

    @classmethod
    def find_all_tool_keys_at(cls, page_name):
        return rsc_core.ResourceDesktopTool.find_all_tool_keys_at(page_name)

    @classmethod
    def find_all_page_keys_at(cls, page_name):
        return rsc_core.ResourceDesktopTool.find_all_page_keys_at(page_name)

    @classmethod
    def get_current_user_group_key(cls):
        return '{}/{}'.format(
            cls.PageKey.User, bsc_core.SysBaseMtd.get_user_name()
        )


class KitPermissionQuery(object):
    @classmethod
    def get_default_args(cls, key):
        # is_executable, is_editable
        return True, True

    @classmethod
    def get_department_args(cls, key):
        # check user is in group?
        # is_executable, is_editable
        return True, False

    @classmethod
    def get_user_args(cls, key):
        # check user is current
        # is_executable, is_editable
        if key == KitDesktopHook.get_current_user_group_key():
            return True, True
        return True, False


class KitDesktopHookAddOpt(object):
    CUSTOMIZE_PATH = '/l/resource/td/tools/desktop'

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
        return cls.CUSTOMIZE_PATH+'/share'

    @classmethod
    def get_user_directory(cls):
        return cls.CUSTOMIZE_PATH+'/{}'.format(bsc_core.SysBaseMtd.get_user_name())

    @classmethod
    def get_all_hook_keys_from_fnc(cls, path):
        list_ = []
        for i in [path+'/hooks']:
            for j in bsc_core.StgDirectoryOpt(i).get_all_file_paths(ext_includes=['.yml']) or []:
                j_name = bsc_core.StgFileOpt(j).get_path_base()[len(i)+1:]
                list_.append(j_name)
        return list_

    def accept_create(self, mode='create'):
        page_name = self._options.get('gui.group_name')
        group_sub_name = self._options.get('gui.group_sub_name')

        directory_path = self.CUSTOMIZE_PATH
        directory_path = bsc_core.StgPathMapper.map_to_current(directory_path)

        name = self._options.get('name')
        hook_key = '{}/{}'.format(page_name, name)

        configure_file_path = '{}/{}.yml'.format(directory_path, hook_key)

        python_file_path = '{}/{}.py'.format(directory_path, hook_key)
        linux_file_path = '{}/{}.sh'.format(directory_path, hook_key)
        windows_file_path = '{}/{}.bat'.format(directory_path, hook_key)
        configure_file_opt = bsc_core.StgFileOpt(configure_file_path)
        if mode is 'create':
            if configure_file_opt.get_is_file() is True:
                gui_core.GuiDialog.create(
                    self._session.gui_name,
                    content='name "{}" is exists, entry a new name to continue'.format(name),
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    yes_visible=False,
                    no_visible=False,
                )
                return

        default_configue_file_path = bsc_core.ResourceConfigure.get(
            'session/default-hook-configure.yml'
        )
        c = ctt_core.Content(value=default_configue_file_path)

        type_ = self._options.get('type')
        c.set('option.type', type_)

        gui_name = self._options.get('gui.name')
        if not gui_name:
            gui_name = bsc_core.RawTextMtd.to_prettify(name)

        c.set('option.gui.name', gui_name)
        if group_sub_name != 'None':
            c.set('option.gui.group_sub_name', group_sub_name)

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
        c.set('option.gui.icon_style', self._options.get('gui.icon_style'))
        c.set('option.gui.icon_color', self._options.get('gui.icon_color'))
        c.set('option.gui.tool_tip', self._options.get('gui.tool_tip'))

        python_script = self._options.get('script.python')
        windows_shell_script = self._options.get('script.windows')
        linux_shell_script = self._options.get('script.linux')

        bsc_core.StgPathPermissionMtd.create_directory(
            bsc_core.StgFileMtd.get_directory(configure_file_path)
        )

        if type_ == 'python-command':
            if not python_script:
                gui_core.GuiDialog.create(
                    self._session.gui_name,
                    content='python script is empty, entry script to continue',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
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
                gui_core.GuiDialog.create(
                    self._session.gui_name,
                    content='shell script is empty, entry script to continue',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
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

        c.save_to(configure_file_path)

        self._window.gui_refresh_group(self._options.get('gui.group_name'))

        self._window.switch_to_main_layer()


class KitDesktop(object):
    def show_window(self):
        pass


if __name__ == '__main__':
    import lxbasic.session.core as bsc_ssn_core

    print KitDesktopHook.get_args(
        'Share/quixel_python'
    )
    # s, e = KitDesktopHook.get_args(
    #     'BUILTIN/main'
    # )
    # e()
    s, e = bsc_ssn_core.Hook.get_args(
        'rsv-panels/asset-loader'
    )
    e()
