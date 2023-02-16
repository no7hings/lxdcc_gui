# coding:utf-8
import six

import math

import re

from lxbasic import bsc_core

from lxutil import utl_configure

from lxutil_gui import utl_gui_configure

import lxbasic.objects as bsc_objects


class HtmlText(object):
    @classmethod
    def get_color(cls, *args):
        arg = args[0]
        if isinstance(arg, (float, int)):
            return utl_gui_configure.Html.COLORS[int(arg)]
        elif isinstance(arg, six.string_types):
            return utl_gui_configure.Html.COLOR_DICT.get(arg, '#dfdfdf')
        return '#dfdfdf'
    @classmethod
    def get_text(cls, text, font_color=utl_gui_configure.Html.WHITE, font_family='Arial', font_size=8):
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


class PanelsConfigure(object):
    def __init__(self):
        self._configure = utl_configure.MainData.get_as_configure('utility/panel/main')

    def get_window(self, panel_key):
        key_path = 'panels.{}.window'.format(panel_key)
        return self._configure.get_content(key_path)


class ChartMethod(object):
    FNC_ANGLE = math.radians
    FNC_SIN = math.sin
    FNC_COS = math.cos
    FNC_TAN = math.tan
    FNC_FLOOR = math.floor
    @classmethod
    def get_regular_polygon_points(cls, pos_x, pos_y, side_count, radius, side):
        lis = []
        for seq in range(side_count):
            a = 360 / side_count * seq
            x = math.sin(math.radians(a)) * (radius - side) + pos_x
            y = math.cos(math.radians(a)) * (radius - side) + pos_y
            lis.append((x, y))
        if lis:
            lis.append(lis[0])
        return lis
    @classmethod
    def get_angle_by_coord(cls, x1, y1, x2, y2):
        radian = 0.0
        #
        r0 = 0.0
        r90 = math.pi / 2.0
        r180 = math.pi
        r270 = 3.0 * math.pi / 2.0
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
            radian = math.atan2((-x1 + x2), (-y1 + y2))
        elif x1 < x2 and y1 > y2:
            radian = r90 + math.atan2((y1 - y2), (-x1 + x2))
        elif x1 > x2 and y1 > y2:
            radian = r180 + math.atan2((x1 - x2), (y1 - y2))
        elif x1 > x2 and y1 < y2:
            radian = r270 + math.atan2((-y1 + y2), (x1 - x2))
        #
        return radian * 180 / math.pi
    @classmethod
    def get_length_by_coord(cls, x1, y1, x2, y2):
        return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


class Ellipse2dMtd(object):
    @classmethod
    def get_coord_at_angle(cls, start, radius, angle):
        x, y = start
        xp = math.sin(math.radians(angle)) * radius / 2 + x + radius / 2
        yp = math.cos(math.radians(angle)) * radius / 2 + y + radius / 2
        return xp, yp

    @classmethod
    def get_coord_at_angle_(cls, center, radius, angle):
        x, y = center
        xp = math.sin(math.radians(angle)) * radius/2 + x
        yp = math.cos(math.radians(angle)) * radius/2 + y
        return xp, yp


class State(object):
    NORMAL = 'normal'
    ENABLE = 'enable'
    DISABLE = 'disable'
    WARNING = 'warning'
    ERROR = 'error'
    LOCKED = 'locked'
    LOST = 'lost'


class RscIconFile(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'
    @classmethod
    def get(cls, key):
        return bsc_core.RscFileMtd.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_(cls, key):
        _ = re.findall(
            re.compile(cls.ICON_KEY_PATTERN, re.S), key
        )
        if _:
            cls.get(_)


class RcsIconDirectory(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'
    @classmethod
    def get(cls, key):
        return bsc_core.RscFileMtd.get(
            '{}/{}'.format(cls.BRANCH, key)
        )


class RscFontFile(object):
    BRANCH = 'fonts'
    @classmethod
    def get(cls, key):
        return bsc_core.RscFileMtd.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_all(cls, sub_key='*'):
        return bsc_core.RscFileMtd.get_all(
            '{}/{}.*'.format(cls.BRANCH, sub_key)
        )


class QtStyleMtd(object):
    CONFIGURE = bsc_objects.Configure(
        value='{}/qt-style.yml'.format(utl_gui_configure.Data.DATA_ROOT)
    )
    CONFIGURE.set(
        'option.icon-dir', RcsIconDirectory.get('qt-style')
    )
    CONFIGURE.set_flatten()
    @classmethod
    def get(cls, key):
        return cls.CONFIGURE.get(
            'widget.{}'.format(key)
        )
    @classmethod
    def get_border(cls, key):
        return eval(
            cls.CONFIGURE.get(
                'option.border.{}'.format(key)
            )
        )
    @classmethod
    def get_background(cls, key):
        return eval(
            cls.CONFIGURE.get(
                'option.background.{}'.format(key)
            )
        )
    @classmethod
    def get_font(cls, key):
        return eval(
            cls.CONFIGURE.get(
                'option.font.{}'.format(key)
            )
        )


if __name__ == '__main__':
    import os
    os.environ['LYNXI_RESOURCES'] = '/data/e/myworkspace/td/lynxi/script/python/.resources'
    print RcsIconDirectory.get('qt-style')
