# coding:utf-8
import os

import six

import math

import re

import copy

import platform

import lxlog.core as log_core

import lxresource.core as rsc_core

import lxcontent.core as ctt_core

import lxcontent.objects as ctt_objects

import lxgui.configure as gui_configure


class GuiUtil(object):

    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'

    @classmethod
    def get_is_maya(cls):
        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False

    @classmethod
    def get_is_houdini(cls):
        _ = os.environ.get('HIP')
        if _:
            return True
        return False

    @classmethod
    def get_is_katana(cls):
        _ = os.environ.get('KATANA_ROOT')
        if _:
            return True
        return False

    @classmethod
    def get_is_clarisse(cls):
        _ = os.environ.get('IX_PYTHON2HOME')
        if _:
            return True
        return False

    @classmethod
    def get_windows_user_directory(cls):
        return '{}/{}/.lynxi'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', 'c:/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_user_directory(cls):
        return '{}/.lynxi'.format(
            os.environ.get('HOME', '/temp')
        )

    @classmethod
    def get_user_directory(cls):
        if cls.get_is_windows():
            return cls.get_windows_user_directory()
        elif cls.get_is_linux():
            return cls.get_linux_user_directory()
        raise SystemError()

    @classmethod
    def get_user_history_file(cls):
        return '{}/history.yml'.format(
            cls.get_user_directory()
        )


class GuiXml(object):
    @classmethod
    def get_color(cls, *args):
        arg = args[0]
        if isinstance(arg, (float, int)):
            return gui_configure.XmlColor.All[int(arg)]
        elif isinstance(arg, six.string_types):
            return gui_configure.XmlColor.Dict.get(arg, '#dfdfdf')
        return '#dfdfdf'

    @classmethod
    def get_text(cls, text, font_color=gui_configure.XmlColor.White, font_family='Arial', font_size=8):
        html_color = cls.get_color(font_color)
        #
        text = text.replace(' ', '&nbsp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        _ = text.split('\n')
        if len(_) > 1:
            raw = u''.join([u'{}<br>'.format(i) for i in _])
        else:
            raw = text
        #
        return u'''
<html>
    <head>
        <style>
            p.s{{line-height: 100%; font-family: '{font_family}'; font-size: {font_size}pt; color: {font_color}; word-spacing: normal;}}
        </style>
    </head>
    <body>
        <p class="s">{raw}</p>
    </body>
</html>
        '''.format(
            **dict(
                font_family=font_family,
                font_size=font_size,
                font_color=html_color,
                raw=raw
            )
        )


class GuiChat(object):
    FNC_ANGLE = math.radians
    FNC_SIN = math.sin
    FNC_COS = math.cos
    FNC_TAN = math.tan
    FNC_FLOOR = math.floor

    @classmethod
    def get_regular_polygon_points(cls, pos_x, pos_y, side_count, radius, side):
        lis = []
        for seq in range(side_count):
            a = 360/side_count*seq
            x = math.sin(math.radians(a))*(radius-side)+pos_x
            y = math.cos(math.radians(a))*(radius-side)+pos_y
            lis.append((x, y))
        if lis:
            lis.append(lis[0])
        return lis

    @classmethod
    def get_angle_by_coord(cls, x1, y1, x2, y2):
        radian = 0.0
        #
        r0 = 0.0
        r90 = math.pi/2.0
        r180 = math.pi
        r270 = 3.0*math.pi/2.0
        #
        if x1 == x2:
            if y1 < y2:
                radian = r0
            elif y1 > y2:
                radian = r180
        elif y1 == y2:
            if x1 < x2:
                radian = r90
            elif x1 > x2:
                radian = r270
        elif x1 < x2 and y1 < y2:
            radian = math.atan2((-x1+x2), (-y1+y2))
        elif x1 < x2 and y1 > y2:
            radian = r90+math.atan2((y1-y2), (-x1+x2))
        elif x1 > x2 and y1 > y2:
            radian = r180+math.atan2((x1-x2), (y1-y2))
        elif x1 > x2 and y1 < y2:
            radian = r270+math.atan2((-y1+y2), (x1-x2))
        #
        return radian*180/math.pi

    @classmethod
    def get_length_by_coord(cls, x1, y1, x2, y2):
        return math.sqrt(((x1-x2)**2)+((y1-y2)**2))


class GuiEllipse2d(object):
    @classmethod
    def get_coord_at_angle(cls, start, radius, angle):
        x, y = start
        xp = math.sin(math.radians(angle))*radius/2+x+radius/2
        yp = math.cos(math.radians(angle))*radius/2+y+radius/2
        return xp, yp

    @classmethod
    def get_coord_at_angle_(cls, center, radius, angle):
        x, y = center
        xp = math.sin(math.radians(angle))*radius/2+x
        yp = math.cos(math.radians(angle))*radius/2+y
        return xp, yp


class State(object):
    NORMAL = 'normal'
    ENABLE = 'enable'
    DISABLE = 'disable'
    WARNING = 'warning'
    ERROR = 'error'
    LOCKED = 'locked'
    LOST = 'lost'


class GuiIcon(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'

    @classmethod
    def get(cls, key):
        return rsc_core.Resource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def get_(cls, key):
        _ = re.findall(
            re.compile(cls.ICON_KEY_PATTERN, re.S), key
        )
        if _:
            cls.get(_)

    @classmethod
    def get_directory(cls):
        return cls.get('file/folder')

    @classmethod
    def get_by_file(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        if ext:
            _ = cls.get('file/{}'.format(ext[1:]))
            if _:
                return _
        return cls.get('file/file')

    @classmethod
    def find_all_keys_at(cls, group_branch):
        return rsc_core.Resource.find_all_file_keys_at(
            cls.BRANCH, group_branch, ext_includes={'.png', '.svg'}
        )


class GuiIconDirectory(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'

    @classmethod
    def get(cls, key):
        return rsc_core.Resource.get(
            '{}/{}'.format(cls.BRANCH, key)
        )


class GuiQtFont(object):
    BRANCH = 'fonts'

    @classmethod
    def get(cls, key):
        return rsc_core.Resource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def get_all(cls, sub_key='*'):
        return rsc_core.Resource.get_all(
            '{}/{}.*'.format(cls.BRANCH, sub_key)
        )


class GuiModifier(object):
    @staticmethod
    def debug_run(fnc):
        def fnc_(*args, **kwargs):
            # noinspection PyBroadException
            try:
                _fnc = fnc(*args, **kwargs)
                return _fnc
            except Exception:
                log_core.LogException.trace()
                raise
        return fnc_


class GuiDialog(object):
    ValidationStatus = gui_configure.ValidationStatus

    @classmethod
    def create(
        cls,
        label,
        sub_label=None,
        content=None,
        content_text_size=10,
        window_size=(480, 160),
        yes_method=None,
        yes_label=None,
        yes_visible=True,
        #
        no_method=None,
        no_label=None,
        no_visible=True,
        #
        cancel_fnc=None,
        cancel_label=None,
        cancel_visible=True,
        #
        tip_visible=True,
        #
        button_size=160,
        status=None,
        use_as_error=False,
        use_as_warning=False,
        show=True,
        use_exec=True,
        options_configure=None,
        use_thread=True,
        parent=None,
        #
        use_window_modality=True
    ):
        import lxgui.proxy.widgets as prx_widgets
        #
        if use_exec is True:
            w = prx_widgets.PrxDialogWindow1(parent=parent)
        else:
            w = prx_widgets.PrxDialogWindow0(parent=parent)
        #
        w.set_window_modality(use_window_modality)
        #
        w.set_use_thread(use_thread)
        w.set_window_title(label)
        #
        if sub_label is not None:
            w.set_sub_label(sub_label)
        #
        if content is not None:
            w.set_content(content)
        #
        w.set_content_font_size(content_text_size)
        w.set_definition_window_size(window_size)
        if yes_label is not None:
            w.set_yes_label(yes_label)
        if yes_method is not None:
            w.connect_yes_to(yes_method)
        w.set_yes_visible(yes_visible)
        #
        if no_label is not None:
            w.set_no_label(no_label)
        if no_method is not None:
            w.connect_no_to(no_method)
        w.set_no_visible(no_visible)
        #
        if cancel_label is not None:
            w.set_cancel_label(cancel_label)
        if cancel_fnc is not None:
            w.connect_cancel_method(cancel_fnc)
        w.set_cancel_visible(cancel_visible)
        #
        if status is not None:
            w.set_window_title(label)
            w.set_status(status)
        #
        if options_configure is not None:
            w.set_options_group_enable()
            w.set_options_create_by_configure(options_configure)
        #
        w.set_tip_visible(tip_visible)
        #
        if show is True:
            w.set_window_show()
        return w


class GuiMonitorForDeadline(object):
    @classmethod
    def set_create(cls, label, job_id, parent=None):
        import lxgui.proxy.widgets as prx_widgets

        import lxdeadline.core as ddl_core

        w = prx_widgets.PrxMonitorWindow(parent=parent)
        w.set_window_title(
            '{}({})'.format(
                label, job_id
            )
        )
        button = w.get_status_button()
        j_m = ddl_core.DdlJobMonitor(job_id)
        button.set_statuses(j_m.get_task_statuses())
        button.set_initialization(j_m.get_task_count())
        j_m.logging.connect_to(w.set_logging)
        j_m.task_status_changed_at.connect_to(w.set_status_at)
        j_m.task_finished_at.connect_to(w.set_finished_at)
        j_m.set_start()

        w.connect_window_close_to(j_m.set_stop)

        w.set_window_show(size=(480, 240))


class GuiDpiScale(object):
    @classmethod
    def get(cls, *args):
        return args[0]


class GuiHistory(object):
    KEY = 'gui history'
    MAXIMUM = 20

    FILE_PATH = GuiUtil.get_user_history_file()
    CACHE = None

    @classmethod
    def __pre_run(cls):
        if os.path.isfile(cls.FILE_PATH) is False:
            ctt_core.CttFile(cls.FILE_PATH).write({})

    @classmethod
    def __is_valid(cls):
        return os.path.isfile(cls.FILE_PATH) is True

    # @classmethod
    # def __get_content(cls):
    #     if cls.CACHE is not None:
    #         return cls.CACHE
    #
    #     cls.CACHE = ctt_objects.Content(
    #         value=cls.FILE_PATH
    #     )
    #     log_core.Log.trace_method_result(
    #         cls.KEY, 'load history from "{}"'.format(cls.FILE_PATH)
    #     )
    #     return cls.CACHE

    @classmethod
    def __get_content(cls):
        return ctt_objects.Content(
            value=cls.FILE_PATH
        )

    @classmethod
    def set_one(cls, key, value):
        cls.__pre_run()
        if cls.__is_valid() is True:
            c = cls.__get_content()
            c.set(key, value)
            c.save()

    @classmethod
    def get_one(cls, key):
        cls.__pre_run()
        if cls.__is_valid() is True:
            c = cls.__get_content()
            return c.get(key)

    @classmethod
    def set_array(cls, key, array):
        cls.__pre_run()
        if cls.__is_valid() is True:
            c = cls.__get_content()
            c.set(key, array)
            c.save()

    @classmethod
    def get_array(cls, key):
        cls.__pre_run()
        if cls.__is_valid() is True:
            c = cls.__get_content()
            return c.get(key)
        return []

    @classmethod
    def append(cls, key, value):
        cls.__pre_run()
        if cls.__is_valid() is True:
            c = cls.__get_content()
            values_exists = c.get(key) or []
            # move end
            if value in values_exists:
                values_exists.remove(value)
            values_exists.append(value)
            #
            values_exists = values_exists[-cls.MAXIMUM:]
            c.set(key, values_exists)
            c.save()
            return True
        return False

    @classmethod
    def extend(cls, key, values):
        cls.__pre_run()
        #
        if cls.__is_valid() is True:
            c = cls.__get_content()
            values_exists = c.get(key) or []
            for i_value in values:
                if i_value not in values_exists:
                    values_exists.append(i_value)
            #
            values_exists = values_exists[-cls.MAXIMUM:]
            c.set(key, values_exists)
            c.save()
            return True
        return False

    @classmethod
    def get_all(cls, key):
        cls.__pre_run()
        c = cls.__get_content()
        return copy.copy(c.get(key)) or []

    @classmethod
    def get_latest(cls, key):
        cls.__pre_run()
        if cls.__is_valid() is True:
            c = cls.__get_content()
            _ = c.get(key)
            if _:
                return _[-1]


if __name__ == '__main__':
    print GuiXml.get_text(
        'test'
    )
