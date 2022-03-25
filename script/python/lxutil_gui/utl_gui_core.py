# coding:utf-8
import math

import enum

from lxutil import utl_configure, utl_core

from lxutil_gui import utl_gui_configure

import lxbasic.objects as bsc_objects


class HtmlText(object):
    @classmethod
    def get_color(cls, *args):
        arg = args[0]
        if isinstance(arg, (float, int)):
            return utl_gui_configure.Html.COLORS[int(arg)]
        elif isinstance(arg, (str, unicode)):
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
    def get_regular_polygon_points(cls, xPos, yPos, sideCount, radius, side):
        lis = []
        for seq in range(sideCount):
            a = 360 / sideCount * seq
            x = math.sin(math.radians(a)) * (radius - side) + xPos
            y = math.cos(math.radians(a)) * (radius - side) + yPos
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


class SizeMtd(object):
    @classmethod
    def set_remap_to(cls, width, height, maximum):
        maxValue = max([width, height])
        if maxValue > maximum:
            if width > height:
                return maximum, maximum*(float(height)/float(width))
            elif width < height:
                return maximum*(float(width)/float(height)), maximum
        return width, height
    @classmethod
    def set_fit_to(cls, size_0, size_1):
        w0, h0 = size_0
        w1, h1 = size_1
        p_0 = float(w0) / float(h0)
        p_1 = float(w1) / float(h1)
        smax1 = max(w1, h1)
        smin1 = min(w1, h1)
        if p_0 > 1:
            if p_0 > p_1:
                w, h = w1, w1/p_0
            elif p_0 < p_1:
                w, h = h1*p_0, h1
            else:
                w, h = w1, h1
        elif p_0 < 1:
            if p_0 > p_1:
                w, h = w1, w1/p_0
            elif p_0 < p_1:
                w, h = h1*p_0, h1
            else:
                w, h = w1, h1
        else:
            w, h = smin1, smin1
        x, y = int((w1-w)/2), int((h1-h)/2)
        return x, y, w, h
    @classmethod
    def set_fill_to(cls, size_0, size_1):
        w0, h0 = size_0
        w1, h1 = size_1
        p_0 = float(w0) / float(h0)
        p_1 = float(w1) / float(h1)


class Ellipse2dMtd(object):
    @classmethod
    def get_position_at_angle(cls, center, radius, angle):
        x, y = center
        xp = math.sin(math.radians(angle)) * radius / 2 + x + radius / 2
        yp = math.cos(math.radians(angle)) * radius / 2 + y + radius / 2
        return xp, yp


class State(object):
    NORMAL = 'normal'
    ENABLE = 'enable'
    DISABLE = 'disable'
    WARNING = 'warning'
    ERROR = 'error'


class QtStyleMtd(object):
    CONFIGURE = bsc_objects.Configure(
        value='{}/qt-style.yml'.format(utl_gui_configure.Data.DATA_ROOT)
    )
    CONFIGURE.set(
        'option.icon-dir', utl_core.Icon.ROOT_PATH
    )
    CONFIGURE.set_flatten()
    @classmethod
    def get(cls, key):
        return cls.CONFIGURE.get(
            'widget.{}'.format(key)
        )
    @classmethod
    def get_border_color(cls, key):
        return eval(
            cls.CONFIGURE.get(
                'option.border.{}'.format(key)
            )
        )
    @classmethod
    def get_background_color(cls, key):
        return eval(
            cls.CONFIGURE.get(
                'option.background.{}'.format(key)
            )
        )


class Icons(object):
    BRANCH = 'icons'
    @classmethod
    def get(cls, key):
        return utl_core.Resources.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )


class Fonts(object):
    BRANCH = 'fonts'
    @classmethod
    def get(cls, key):
        return utl_core.Resources.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_all(cls, sub_key='*'):
        return utl_core.Resources.get_all(
            '{}/{}.*'.format(cls.BRANCH, sub_key)
        )


if __name__ == '__main__':
    import os
    os.environ['LYNXI_RESOURCES'] = '/data/e/myworkspace/td/lynxi/script/python/.resources'
    print Fonts.get_all()
