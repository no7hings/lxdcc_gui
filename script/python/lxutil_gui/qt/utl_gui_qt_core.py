# coding:utf-8
import time

import six

import functools

import glob

import os

import sys
#
import cgitb
#
import math

import types
#
from lxbasic import bsc_configure, bsc_core

import lxbasic.abstracts as bsc_abstracts

import lxbasic.objects as bsc_objects

from lxutil.core import _utl_cor_utility
#
from lxutil import utl_core, utl_abstract

from lxutil_gui import utl_gui_configure, utl_gui_core

_pyqt5 = bsc_objects.PyModule('PyQt5')

if _pyqt5.get_is_exists() is True:
    LOAD_INDEX = 0
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg, QtOpenGL
else:
    LOAD_INDEX = 1
    _pyside2 = bsc_objects.PyModule('PySide2')
    if _pyside2.get_is_exists() is True:
        # noinspection PyUnresolvedReferences
        from PySide2 import QtGui, QtCore, QtWidgets, QtSvg, QtOpenGL
    else:
        raise ImportError()

cgitb.enable(
    logdir=(bsc_core.EnvExtraMtd.get_user_debug_directory(tag='qt', create=True) or bsc_core.StgUserMtd.get_user_debug_directory(tag='qt', create=True)),
    format='text'
)

load_dic = {
    'qt_property': [
        ("PyQt5.QtCore", "pyqtProperty"),
        ("PySide2.QtCore", "Property"),
        ("PySide2.QtCore", "Property")
    ],
    'qt_signal': [
        ("PyQt5.QtCore", "pyqtSignal"),
        ("PySide2.QtCore", "Signal"),
        ("PySide2.QtCore", "Signal")
    ],
    'qt_wrapinstance': [
        ("sip", "wrapinstance"),
        ("shiboken2", "wrapInstance"),
        ("PySide2.shiboken2", "wrapInstance")
    ],
    'qt_is_deleted': [
        ("sip", "isdeleted"),
        ("shiboken2", "isValid"),
        ("PySide2.shiboken2", "isValid")
    ]
}

misplaced_dic = {
    "QtCore.pyqtProperty": "QtCore.Property",
    "QtCore.pyqtSignal": "QtCore.Signal",
    "QtCore.pyqtSlot": "QtCore.Slot",
    "QtCore.QAbstractProxyModel": "QtCore.QAbstractProxyModel",
    "QtCore.QSortFilterProxyModel": "QtCore.QSortFilterProxyModel",
    "QtCore.QStringListModel": "QtCore.QStringListModel",
    "QtCore.QItemSelection": "QtCore.QItemSelection",
    "QtCore.QItemSelectionModel": "QtCore.QItemSelectionModel",
    "QtCore.QItemSelectionRange": "QtCore.QItemSelectionRange",
    "uic.loadUi": "QtCompat.loadUi",
    "sip.wrapinstance": "QtCompat.wrapInstance",
    "sip.unwrapinstance": "QtCompat.getCppPointer",
    "sip.isdeleted": "QtCompat.isValid",
    "QtWidgets.qApp": "QtWidgets.QApplication.instance()",
    "QtCore.QCoreApplication.translate": "QtCompat.translate",
    "QtWidgets.QApplication.translate": "QtCompat.translate",
    "QtCore.qInstallMessageHandler": "QtCompat.qInstallMessageHandler",
    "QtWidgets.QStyleOptionViewItem": "QtCompat.QStyleOptionViewItemV4",
}


def qt_signal(*args):
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    module_name, method_name = load_dic[key][LOAD_INDEX]
    module = bsc_objects.PyModule(load_dic[key][LOAD_INDEX][0])
    method = module.get_method(method_name)
    return method(*args)


def qt_wrapinstance(*args):
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    module_name, method_name = load_dic[key][LOAD_INDEX]
    module = bsc_objects.PyModule(load_dic[key][LOAD_INDEX][0])
    method = module.get_method(method_name)
    return method(*args)


def qt_is_deleted(*args):
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    module_name, method_name = load_dic[key][LOAD_INDEX]
    module = bsc_objects.PyModule(load_dic[key][LOAD_INDEX][0])
    method = module.get_method(method_name)
    return method(*args)


def DpiScale(*args):
    return args[0]


def get_font(size=8, weight=50, italic=False, underline=False, strike_out=False, family='Arial'):
    font = QtGui.QFont()
    # print font.family()
    font.setPointSize(size)
    font.setFamily(family)
    # print font.family()
    font.setWeight(weight)
    font.setItalic(italic)
    font.setUnderline(underline)
    font.setWordSpacing(1)
    font.setStrikeOut(strike_out)
    return font


def get_qt_widget_by_class(widget_class):
    lis = []
    # noinspection PyArgumentList
    widgets = QtWidgets.QApplication.topLevelWidgets()
    if widgets:
        for w in widgets:
            if widget_class.__name__ == w.__class__.__name__:
                lis.append(w)
    return lis


def get_all_lx_windows():
    lis = []
    widgets = QtWidgets.QApplication.topLevelWidgets()
    for i in widgets:
        if hasattr(i, 'lynxi_window'):
            lis.append(i)
    return lis


def get_all_visible_lx_windows():
    lis = []
    widgets = QtWidgets.QApplication.topLevelWidgets()
    for i in widgets:
        if hasattr(i, 'lynxi_window'):
            if i.isHidden() is False:
                lis.append(i)
    return lis


def get_active_lx_window():
    for i in get_all_lx_windows():
        if i.isActiveWindow() is True:
            return i


def get_qt_widget_is_deleted(widget):
    import shiboken2
    return shiboken2.isValid(widget)


def get_active_window():
    return QtWidgets.QApplication.activeWindow()


def get_qt_desktop(*args):
    # noinspection PyArgumentList
    return QtWidgets.QApplication.desktop(*args)


def get_qt_desktop_primary_rect(*args):
    # noinspection PyArgumentList
    desktop = QtWidgets.QApplication.desktop(*args)
    return desktop.availableGeometry(desktop.primaryScreen())


def get_qt_desktop_rect(*args):
    # noinspection PyArgumentList
    desktop = QtWidgets.QApplication.desktop(*args)
    return desktop.rect()


def get_qt_cursor_pos(*args):
    return QtGui.QCursor.pos(*args)


def set_shadow(qt_widget, radius):
    shadow = QtWidgets.QGraphicsDropShadowEffect()
    shadow.setBlurRadius(radius)
    shadow.setColor(QtBackgroundColors.Black)
    shadow.setOffset(2, 2)
    qt_widget.setGraphicsEffect(shadow)


def set_text_copy_to_clipboard(text):
    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(text)


def set_loading_cursor():
    QtWidgets.QApplication.setOverrideCursor(
        QtCore.Qt.BusyCursor
    )


def set_action_cursor():
    QtWidgets.QApplication.setOverrideCursor(
        QtCore.Qt.PointingHandCursor
    )


def set_normal_cursor():
    QtWidgets.QApplication.setOverrideCursor(
        QtCore.Qt.CustomCursor
    )


def set_prx_window_waiting(method):
    def sub_method(*args, **kwargs):
        prx_window = args[0]
        prx_window.start_waiting()
        _method = method(*args, **kwargs)
        prx_window.stop_waiting()
        return _method

    return sub_method


class Util(object):
    LAYOUT_MARGINS = 2, 2, 2, 2
    LAYOUT_SPACING = 2
    STYLE_TEXT_RGBA = '223, 223, 223, 255'


class CSSRgba(object):
    text = '191, 191, 191, 255'
    background_0 = '63, 63, 63, 255'
    background_1 = '95, 95, 95, 255'


class Font(object):
    INDEX = get_font()
    NAME = get_font(size=8)
    SEPARATOR = get_font(italic=True)
    CONTENT = get_font(size=8)
    LOADING = get_font(size=10, weight=75, italic=True)
    DESCRIPTION = get_font(size=10)
    #
    NameTextKey = get_font(size=8, italic=True)
    NameTextValue = get_font(size=8)
    #
    GROUP = get_font(size=9, weight=75, italic=True)
    #
    default = get_font()
    title = get_font(size=12)
    #
    disable = get_font(italic=True, strike_out=True)
    #
    button = get_font(size=8)


class RawTextMtd(object):
    @classmethod
    def get_size(cls, font_size, text):
        f = get_font()
        f.setPointSize(font_size)
        m = QtGui.QFontMetrics(f)
        w = m.width(text)
        h = m.height()
        return w, h


class Color(object):
    NORMAL = QtGui.QColor(223, 223, 223, 255)
    ENABLE = QtGui.QColor(63, 255, 127, 255)
    DISABLE = QtGui.QColor(127, 127, 127, 255)
    WARNING = QtGui.QColor(255, 255, 63, 255)
    ERROR = QtGui.QColor(255, 0, 63, 255)
    LOCKED = QtGui.QColor(127, 127, 255, 255)
    LOST = QtGui.QColor(127, 127, 127, 255)
    CORRECT = QtGui.QColor(63, 255, 127, 255)
    ACTIVE = QtGui.QColor(63, 127, 255, 255)
    #
    text_filter = QtGui.QColor(255, 127, 63, 255)
    text_filter_occurrence = QtGui.QColor(255, 63, 63, 255)
    #
    BUTTON_BORDER_DISABLE = QtGui.QColor(79, 79, 79, 255)
    #
    BUTTON_BACKGROUND_NORMAL = QtGui.QColor(103, 103, 103, 255)
    BUTTON_BACKGROUND_HIGHLIGHT = QtGui.QColor(127, 127, 127, 255)
    BUTTON_BACKGROUND_DISABLE = QtGui.QColor(71, 71, 71, 255)
    #
    ENTRY_BORDER_ENTRY_ON = QtGui.QColor(63, 127, 255, 255)
    ENTRY_BORDER_ENTRY_OFF = QtGui.QColor(119, 119, 119, 255)
    ENTRY_BACKGROUND_ENTRY_ON = QtGui.QColor(47, 47, 47, 255)
    ENTRY_BACKGROUND_ENTRY_OFF = QtGui.QColor(55, 55, 55, 255)
    #
    label = QtGui.QColor(95, 95, 95, 255)
    #
    BAR_FRAME_NORMAL = QtGui.QColor(47, 47, 47, 255)
    bar_background = QtGui.QColor(95, 95, 95, 255)
    #
    BAR_NORMAL = QtGui.QColor(95, 95, 95, 255)
    BAR_HIGHLIGHT = QtGui.QColor(127, 127, 127, 255)
    #
    TRANSPARENT = QtGui.QColor(0, 0, 0, 0)
    PROGRESS = QtGui.QColor(63, 255, 127, 255)
    BACKGROUND_TRANSPARENT = QtGui.QColor(0, 0, 0, 0)
    BACKGROUND_HIGHLIGHT = QtGui.QColor(255, 127, 63, 127)
    #
    DESCRIPTION_TEXT = QtGui.QColor(0, 0, 0, 255)
    DESCRIPTION_BACKGROUND = QtGui.QColor(255, 255, 191, 255)
    @classmethod
    def _get_qt_color_(cls, *args):
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, (QtGui.QColor, QtGui.QLinearGradient, QtGui.QConicalGradient)):
                return _
            elif isinstance(_, (tuple, list)):
                return cls._to_qt_color_(*_)
            else:
                raise TypeError()
        else:
            return cls._to_qt_color_(*args)
    @classmethod
    def _to_qt_color_(cls, *args):
        if len(args) == 3:
            r, g, b = args
            a = 255
        elif len(args) == 4:
            r, g, b, a = args
        else:
            raise TypeError()
        return QtGui.QColor(r, g, b, a)
    @classmethod
    def _get_rgb_(cls, *args):
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, QtGui.QColor):
                return _.red(), _.green(), _.blue()
            elif isinstance(_, (tuple, list)):
                return cls._to_rgb_(*_)
            else:
                return 0, 0, 0
        else:
            return cls._to_rgb_(*args)
    @classmethod
    def _to_rgb_(cls, *args):
        if len(args) == 3:
            r, g, b = args
        elif len(args) == 4:
            r, g, b, a = args
        else:
            raise TypeError()
        return r, g, b
    @classmethod
    def _get_rgba_(cls, *args):
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, QtGui.QColor):
                return _.red(), _.green(), _.blue(), _.alpha()
            elif isinstance(_, (tuple, list)):
                return cls._to_rgba_(*_)
            else:
                return 0, 0, 0, 0
        else:
            return cls._to_rgba_(*args)
    @classmethod
    def _to_rgba_(cls, *args):
        if len(args) == 3:
            r, g, b = args
            a = 255
        elif len(args) == 4:
            r, g, b, a = args
        else:
            raise TypeError()
        return r, g, b, a


class QtBorderColors(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *utl_gui_core.QtStyleMtd.get_border(key)
        )

    Transparent = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-transparent')
    )

    Dim = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-dim')
    )
    Dark = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-dark')
    )
    Basic = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-basic')
    )
    Light = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-light')
    )
    HighLight = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-high-light')
    )
    Selected = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-selected')
    )
    Actioned = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-actioned')
    )
    Hovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-hovered')
    )

    Icon = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-icon')
    )

    Button = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-button')
    )
    ButtonDisable = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-button-disable')
    )

    Popup = QtGui.QColor(63, 255, 127, 255)
    SplitMoving = QtGui.QColor(127, 127, 127, 255)


class QtBackgroundColors(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *utl_gui_core.QtStyleMtd.get_background(key)
        )

    Shadow = QtGui.QColor(0, 0, 0, 31)

    Transparent = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-transparent')
    )
    Black = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-black')
    )
    Dim = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-dim')
    )
    Dark = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-dark')
    )
    Basic = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-basic')
    )
    Light = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-light')
    )
    White = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-white')
    )

    Hovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-hovered')
    )
    Selected = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-selected')
    )
    #
    Checked = QtGui.QColor(127, 63, 127, 255)
    CheckHovered = QtGui.QColor(191, 127, 191, 255)
    #
    DeleteHovered = QtGui.QColor(255, 63, 127, 255)
    #
    Pressed = QtGui.QColor(95, 255, 159, 255)
    PressedHovered = QtGui.QColor(255, 159, 95, 255)
    #
    Actioned = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-actioned')
    )
    #
    Icon = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-icon')
    )
    #
    Button = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-button')
    )
    ButtonHovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-button-hovered')
    )
    ButtonDisable = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-button-disable')
    )
    ToolTip = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-tool-tip')
    )
    #
    ItemSelected = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-item-selected')
    )
    ItemSelectedIndirect = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-item-selected-indirect')
    )
    ItemHovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-item-hovered')
    )
    #
    ItemLoading = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-item-loading')
    )
    Error = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-error')
    )

    Bubble = QtGui.QColor(191, 191, 191, 255)
    BubbleHovered = QtGui.QColor(255, 159, 95, 255)


class QtFontColors(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *utl_gui_core.QtStyleMtd.get_font(key)
        )

    Black = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-black')
    )
    Dark = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-dark')
    )
    Basic = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-basic')
    )
    Light = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-light')
    )
    Hovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-hovered')
    )
    Selected = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-selected')
    )

    KeyBasic = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-key-basic')
    )
    KeyHovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-key-hovered')
    )
    ValueBasic = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-value-basic')
    )
    ValueHovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-value-hovered')
    )

    ToolTip = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-tool-tip')
    )
    #
    Normal = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-normal')
    )
    Correct = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-correct')
    )
    Warning = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-warning')
    )
    Error = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-error')
    )
    Active = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-active')
    )
    Disable = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-disable')
    )

    Bubble = QtGui.QColor(15, 15, 15, 255)


class QtStatusColors(object):
    Locked = QtGui.QColor(127, 127, 255, 255)


class QtFonts(object):
    Default = get_font(size=8)
    Label = get_font(size=8)
    Button = get_font(size=9)
    Group = get_font(size=10, weight=75, italic=True)
    Chart = get_font(size=10, italic=True)


class Brush(object):
    text = QtGui.QBrush(QtGui.QColor(191, 191, 191, 255))
    TEXT_NORMAL = QtGui.QBrush(QtFontColors.Basic)
    #
    BACKGROUND_NORMAL = QtGui.QBrush(QtGui.QColor(63, 63, 63, 255))
    #
    default_text = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
    warning_text = QtGui.QBrush(QtGui.QColor(255, 255, 63, 255))
    error_text = QtGui.QBrush(QtGui.QColor(255, 0, 63, 255))
    adopt_text = QtGui.QBrush(QtGui.QColor(63, 255, 127, 255))
    temporary_text = QtGui.QBrush(QtGui.QColor(95, 95, 95, 255))
    current_text = QtGui.QBrush(QtGui.QColor(63, 127, 255, 255))
    selected_background = QtGui.QBrush(QtGui.QColor(255, 127, 63, 255))
    #
    disable_text = QtGui.QBrush(QtGui.QColor(127, 0, 255, 255))
    #
    tree_branch = QtGui.QBrush(QtGui.QColor(127, 127, 127, 255))
    tree_branch_highlight = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))


class QtUtilMtd(object):
    ICON_KEY_PATTERN = r'[@](.*?)[@]'
    @classmethod
    def set_fonts_add(cls, fonts):
        for i in fonts:
            QtGui.QFontDatabase.addApplicationFont(
                i
            )
    @classmethod
    def get_qt_icon(cls, icon_name):
        if QtWidgets.QApplication.instance() is not None:
            return QtIconMtd.create_by_icon_name(icon_name)
    @classmethod
    def _get_qt_icon_(cls, file_path):
        qt_icon = QtGui.QIcon()
        qt_icon.addPixmap(
            QtGui.QPixmap(file_path),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        return qt_icon
    @classmethod
    def get_palette(cls, tool_tip=False):
        palette = QtGui.QPalette()
        palette.setColor(palette.All, palette.Shadow, QtBackgroundColors.Black)
        palette.setColor(palette.All, palette.Dark, QtBackgroundColors.Dim)
        palette.setColor(palette.All, palette.Background, QtBackgroundColors.Basic)
        palette.setColor(palette.All, palette.NoRole, QtBackgroundColors.Dark)
        palette.setColor(palette.All, palette.Base, QtBackgroundColors.Dark)
        palette.setColor(palette.All, palette.Light, QtBackgroundColors.Light)
        palette.setColor(palette.All, palette.Highlight, QtGui.QColor(255, 255, 255, 0))
        palette.setColor(palette.All, palette.Button, QtBackgroundColors.Button)
        #
        palette.setColor(palette.All, palette.Window, QtBackgroundColors.Basic)
        #
        palette.setColor(palette.All, palette.Text, QtFontColors.Basic)
        palette.setColor(palette.All, palette.BrightText, QtFontColors.Light)
        palette.setColor(palette.All, palette.WindowText, QtFontColors.Basic)
        palette.setColor(palette.All, palette.ButtonText, QtFontColors.Basic)
        palette.setColor(palette.All, palette.HighlightedText, QtFontColors.Light)
        #
        palette.setColor(palette.All, palette.AlternateBase, QtBackgroundColors.Dark)
        # tool-tip
        if tool_tip is True:
            p = QtWidgets.QToolTip.palette()
            p.setColor(palette.All, p.ToolTipBase, QtBackgroundColors.ToolTip)
            p.setColor(palette.All, palette.ToolTipText, QtFontColors.ToolTip)
            #
            QtWidgets.QToolTip.setPalette(p)
            QtWidgets.QToolTip.setFont(Font.DESCRIPTION)
        #
        return palette
    @classmethod
    def get_color_icon(cls, rgb):
        icon = QtGui.QIcon()
        f_w, f_h = 13, 13
        c_w, c_h = 12, 12
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = QtGui.QPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            QtCore.Qt.white
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        icon_rect = QtCore.QRect(
            x + (w - c_w) / 2, y + (h - c_h) / 2,
            c_w, c_h
        )
        r, g, b = rgb
        painter.setPen(QtGui.QColor(QtBorderColors.Icon))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
        #
        painter.drawRect(icon_rect)
        painter.end()
        # painter.device()
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        return icon
    @classmethod
    def get_name_text_icon_(cls, text, background_color=None):
        icon = QtGui.QIcon()
        f_w, f_h = 16, 16
        c_w, c_h = 14, 14
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(painter.Antialiasing)
        rect = pixmap.rect()
        pixmap.fill(
            QtBorderColors.Icon
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        rd = min(w, h)
        icon_rect = QtCore.QRect(
            x+(w-c_w)/2, y+(h-c_h)/2,
            c_w, c_h
        )
        if text is not None:
            name = text.split('/')[-1] or ' '
            painter.setPen(QtBorderColors.Icon)
            if background_color is not None:
                r, g, b = background_color
            else:
                r, g, b = bsc_core.RawTextOpt(name).to_rgb()

            background_color_, text_color_ = QtRawColorMtd._get_image_draw_args_by_color_(r, g, b)
            #
            painter.setPen(QtBorderColors.Icon)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(*background_color_)))
            painter.drawRoundedRect(icon_rect, 2, 2, QtCore.Qt.AbsoluteSize)
            painter.setPen(QtGui.QColor(*text_color_))
            painter.setFont(get_font(size=int(rd*.675), italic=True))
            painter.drawText(
                rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(bsc_core.RawTextMtd.get_first_word(name)).capitalize()
            )
        #
        painter.end()
        # painter.device()
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        return icon


class QtIconMtd(object):
    @classmethod
    def create_by_icon_name(cls, icon_name):
        icon = QtGui.QIcon()
        file_path = utl_gui_core.RscIconFile.get(icon_name)
        if file_path:
            icon.addPixmap(
                QtGui.QPixmap(file_path),
                QtGui.QIcon.Normal,
                QtGui.QIcon.On
            )
        return icon
    @classmethod
    def get_by_text(cls, text, rounded=False, background_color=None):
        icon = QtGui.QIcon()
        f_w, f_h = 14, 14
        c_w, c_h = 13, 13
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = QtGui.QPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            QtBorderColors.Icon
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        icon_rect = QtCore.QRect(
            x + (w - c_w) / 2, y + (h - c_h) / 2,
            c_w, c_h
        )
        if text is not None:
            name = text.split('/')[-1] or ' '
            painter.setPen(QtBorderColors.Icon)
            r, g, b = bsc_core.RawTextOpt(name).to_rgb()
            if background_color is not None:
                r, g, b = background_color
            painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
            painter.drawRect(icon_rect)
            # painter.drawRoundedRect(icon_rect, f_w/2, f_w/2, QtCore.Qt.AbsoluteSize)
            #
            # t_r, t_g, t_b = bsc_core.RawColorMtd.get_complementary_rgb(r, g, b)
            painter.setPen(QtFontColors.Basic)
            painter.setFont(get_font(italic=True))
            painter.drawText(
                rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(name[0]).capitalize()
            )
        #
        painter.end()
        # painter.device()
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        return icon


class QtPixmapMtd(object):
    @classmethod
    def _to_gray_(cls, pixmap):
        w, h = pixmap.width(), pixmap.height()
        image_gray = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
        image = pixmap.toImage()
        image_alpha = image.alphaChannel()
        for i_x in range(w):
            for i_y in range(h):
                i_p = image.pixel(i_x, i_y)
                i_a = QtGui.qGray(i_p)
                i_g_c = QtGui.QColor(i_a, i_a, i_a)
                image_gray.setPixel(i_x, i_y, i_g_c.rgb())
        #
        image_gray.setAlphaChannel(image_alpha)
        return pixmap.fromImage(image_gray)
    @classmethod
    def _to_hovered_(cls, pixmap):
        pass
    @classmethod
    def get_by_name(cls, text, size=(20, 20), icon_percent=.75, rounded=False, background_color=None):
        x, y = 0, 0
        w, h = size
        pixmap = QtGui.QPixmap(w, h)
        painter = QtGui.QPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            QtBorderColors.Icon
        )
        rd = min(w, h)
        icon_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        if text is not None:
            name = text.split('/')[-1] or ' '
            painter.setPen(QtBorderColors.Icon)
            r, g, b = bsc_core.RawTextOpt(name).to_rgb_0(s_p=50, v_p=50)
            if background_color is not None:
                r, g, b = background_color
            painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
            if rounded is True:
                painter.drawRoundedRect(icon_rect, w/2, h/2, QtCore.Qt.AbsoluteSize)
            else:
                painter.drawRect(icon_rect)
            #
            painter.setPen(QtFontColors.Basic)
            painter.setFont(get_font(size=int(rd*.6), italic=True))
            painter.drawText(
                rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                str(name[0]).capitalize()
            )
        #
        painter.end()
        return pixmap
    @classmethod
    def get_by_file(cls, file_path, size=(20, 20), icon_percent=.75):
        pixmap = QtGui.QPixmap(file_path)
        new_pixmap = pixmap.scaled(
            QtCore.QSize(*size),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        return new_pixmap
    @classmethod
    def get_by_file_ext(cls, ext, size=(20, 20), icon_percent=.75, gray=False):
        _ = utl_gui_core.RscIconFile.get('file/{}'.format(ext[1:]))
        if _ is not None:
            pixmap = cls.get_by_file(
                file_path=_,
                size=size,
                icon_percent=icon_percent
            )
            if gray is True:
                return cls._to_gray_(pixmap)
            return pixmap
        return cls.get_by_name(
            text=ext[1:],
            size=size
        )
    @classmethod
    def get_by_file_ext_with_tag(cls, ext, tag, frame_size=(20, 20), icon_percent=.75, gray=False):
        x, y = 0, 0
        frm_w, frm_h = frame_size
        icn_w, icn_h = frm_w * icon_percent, frm_h * icon_percent
        base_pixmap = cls.get_by_file_ext(
            ext=ext,
            size=(icn_w, icn_h),
            icon_percent=icon_percent,
            gray=gray
        )
        base_rect = QtCore.QRect(
            x, y, icn_w, icn_h
        )

        pixmap = QtGui.QPixmap(frm_w, frm_h)
        rect = pixmap.rect()
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(painter.Antialiasing)
        painter.fillRect(
            rect, QtBackgroundColors.Light
        )
        painter.drawPixmap(
            base_rect, base_pixmap
        )
        w, h = rect.width(), rect.height()
        rd = min(w, h)
        txt_w, txt_h = rd/2, rd/2
        tag_rect = QtCore.QRect(
            x+w-txt_w-2, y+h-txt_h-2, txt_w, txt_h
        )
        background_color_, text_color_ = QtRawColorMtd._get_image_draw_args_by_text_(tag)
        painter.setPen(QtBorderColors.Icon)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(*background_color_)))
        painter.drawRoundedRect(tag_rect, txt_w/2, txt_h/2, QtCore.Qt.AbsoluteSize)
        painter.setPen(QtGui.QColor(*text_color_))
        painter.setFont(get_font(size=int(txt_w*.625)))
        painter.drawText(
            tag_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(tag[0]).capitalize()
        )
        painter.end()
        return pixmap


class QtTextMtd(object):
    @classmethod
    def get_draw_width(cls, widget, text=None):
        return widget.fontMetrics().width(text)
    @classmethod
    def get_draw_width_maximum(cls, widget, texts):
        lis = []
        for i_text in texts:
            lis.append(widget.fontMetrics().width(i_text))
        return max(lis)


class AbsQtDccMtd(object):
    @classmethod
    def exist_fnc(cls, app):
        sys.exit(app.exec_())


class QtMayaMtd(object):
    @classmethod
    def get_qt_object(cls, ptr, base=QtWidgets.QWidget):
        from shiboken2 import wrapInstance
        return wrapInstance(long(ptr), base)
    @classmethod
    def get_qt_menu_bar(cls):
        qt_main_window = cls.get_qt_main_window()
        if qt_main_window:
            children = qt_main_window.children()
            for i_child in children:
                if i_child:
                    if isinstance(i_child, QtWidgets.QMenuBar):
                        return i_child
    @classmethod
    def get_qt_menu(cls, text):
        qt_menu_bar = cls.get_qt_menu_bar()
        if qt_menu_bar:
            children = qt_menu_bar.children()
            for i_child in children:
                if isinstance(i_child, QtWidgets.QMenu):
                    i_name = i_child.title()
                    if i_name == text:
                        return i_child
    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        from maya import OpenMayaUI
        #
        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window:
            return cls.get_qt_object(
                main_window,
                QtWidgets.QMainWindow
            )
    @classmethod
    def get_qt_icon(cls, icon_name):
        # noinspection PyUnresolvedReferences
        from maya import OpenMayaUI
        ptr = OpenMayaUI.MQtUtil.createIcon(icon_name)
        if ptr is None:
            ptr = OpenMayaUI.MQtUtil.createIcon('default')
        return cls.get_qt_object(ptr, QtGui.QIcon)
    @classmethod
    def get_qt_widget_by_class(cls, widget_class):
        lis = []
        # noinspection PyArgumentList
        widgets = QtWidgets.QApplication.allWidgets()
        if widgets:
            for w in widgets:
                if widget_class.__name__ == w.__class__.__name__:
                    lis.append(w)
        return lis
    @classmethod
    def _test(cls):
        # # noinspection PyUnresolvedReferences
        # from maya import cmds, mel, OpenMayaUI
        # from shiboken2 import wrapInstance, getCppPointer
        # width, height = 400, 400
        # control_name = 'lynxi_tool'
        # control_label = 'Lynxi Tool'
        # if cmds.workspaceControl(control_name, query=1, exists=1):
        #     cmds.workspaceControl(
        #         control_name, edit=1, visible=1, restore=1,
        #         initialWidth=width,
        #         minimumWidth=height
        #     )
        # else:
        #     LEcomponent = mel.eval(r'getUIComponentDockControl("Channel Box / Layer Editor", false);')
        #     cmds.workspaceControl(
        #         control_name,
        #         label=control_label, tabToControl=(LEcomponent, -1),
        #         initialWidth=width, initialHeight=height,
        #         widthProperty='free', heightProperty='free'
        #     )
        #     parentPtr = OpenMayaUI.MQtUtil.getCurrentParent()
        #     parentWidget = wrapInstance(parentPtr, QtWidgets.QWidget)
        #     from lxmaya.panel import widgets
        #     p = widgets.AnimationValidationPanel()
        #     p.widget.setParent(parentWidget)
        #     OpenMayaUI.MQtUtil.addWidgetToMayaLayout(
        #         long(getCppPointer(p.widget)[0]), long(parentPtr)
        #     )
        pass


class QtHoudiniMtd(object):
    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        import hou
        return hou.qt.mainWindow()
    @classmethod
    def get_qt_icon(cls, icon_name):
        # noinspection PyUnresolvedReferences
        import hou
        if icon_name is not None:
            return hou.qt.Icon(icon_name)
        return hou.qt.Icon('MISC_python')


class QtKatanaMtd(object):
    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        import UI4
        return UI4.App.MainWindow.GetMainWindow()
    @classmethod
    def get_qt_icon(cls, icon_name):
        # noinspection PyUnresolvedReferences
        import UI4
        return UI4.Util.ScenegraphIconManager.GetIcon(icon_name, 32)
    @classmethod
    def get_menu_bar(cls):
        main_window = cls.get_qt_main_window()
        if main_window is None:
            utl_core.Log.set_module_warning_trace(
                'qt-katana',
                'main-window is non-exists'
            )
            return
        #
        return main_window.getMenuBar()
    @classmethod
    def get_menu(cls, name):
        menu_bar = cls.get_menu_bar()
        if menu_bar is None:
            utl_core.Log.set_module_warning_trace(
                'qt-katana',
                'menu-bar is non-exists'
            )
            return
        #
        for i_child in menu_bar.children():
            if isinstance(i_child, QtWidgets.QMenu):
                i_name = i_child.title()
                if i_name == name:
                    return i_child


class QtWindowForClarisse(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtWindowForClarisse, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)

    def pos(self):
        # noinspection PyUnresolvedReferences
        import ix
        x, y = ix.application.get_event_window().get_position()
        return QtCore.QPoint(
            x, y
        )

    def width(self):
        # noinspection PyUnresolvedReferences
        import ix
        w, h = ix.application.get_event_window().get_size()
        return w

    def height(self):
        # noinspection PyUnresolvedReferences
        import ix
        w, h = ix.application.get_event_window().get_size()
        return h


class QtClarisseMtd(object):
    QT_MAIN_WINDOW = None
    @classmethod
    def get_qt_main_window_(cls):
        if cls.QT_MAIN_WINDOW is None:
            # noinspection PyUnresolvedReferences
            import ix
            # noinspection PyUnresolvedReferences
            import pyqt_clarisse
            #
            if QtWidgets.QApplication.instance() is None:
                app = QtWidgets.QApplication(sys.argv)
            else:
                app = QtWidgets.QApplication.instance()
            #
            ix.enable_command_history()
            ix.begin_command_batch('ClarisseMainWindowCreate')
            #
            w = QtWindowForClarisse()
            w.show()
            #
            w.setGeometry(
                0, 0, 1, 1
            )
            pyqt_clarisse.exec_(app)
            #
            ix.end_command_batch()
            ix.disable_command_history()
            cls.QT_MAIN_WINDOW = w
            return w
        return cls.QT_MAIN_WINDOW
    @classmethod
    def get_qt_main_window(cls):
        return None
    @classmethod
    def get_qt_main_window_geometry(cls):
        # noinspection PyUnresolvedReferences
        import ix
        x, y = ix.application.get_event_window().get_position()
        w, h = ix.application.get_event_window().get_size()
        return x, y, w, h


class QtDccMtd(utl_abstract.AbsDccMtd):
    QT_MAIN_WINDOW = None
    @classmethod
    def get_qt_main_window(cls):
        if cls.get_is_maya():
            return QtMayaMtd.get_qt_main_window()
        elif cls.get_is_houdini():
            return QtHoudiniMtd.get_qt_main_window()
        elif cls.get_is_katana():
            return QtKatanaMtd.get_qt_main_window()
        elif cls.get_is_clarisse():
            return QtClarisseMtd.get_qt_main_window()
        #
        if cls.QT_MAIN_WINDOW is not None:
            return cls.QT_MAIN_WINDOW
        #
        _ = QtWidgets.QApplication.topLevelWidgets()
        if _:
            cls.QT_MAIN_WINDOW = _[0]
        return QtWidgets.QApplication.activeWindow()
    @classmethod
    def get_active_window(cls):
        return QtWidgets.QApplication.activeWindow()
    @classmethod
    def get_qt_icon(cls, icon_name):
        if cls.get_is_maya():
            return QtMayaMtd.get_qt_icon(icon_name)
        elif cls.get_is_houdini():
            return QtHoudiniMtd.get_qt_icon(icon_name)
    @classmethod
    def get_palette(cls):
        if cls.get_is_maya():
            return QtUtilMtd.get_palette()
        elif cls.get_is_houdini():
            return QtUtilMtd.get_palette()
        elif cls.get_is_katana():
            return QtUtilMtd.get_palette()
        elif cls.get_is_clarisse():
            return QtUtilMtd.get_palette(tool_tip=True)
        else:
            return QtUtilMtd.get_palette(tool_tip=True)
    @classmethod
    def get_current_main_window(cls):
        return QtWidgets.QApplication.activeWindow()
    @classmethod
    def exit_app(cls, app):
        if cls.get_is_clarisse():
            # noinspection PyUnresolvedReferences
            import pyqt_clarisse
            pyqt_clarisse.exec_(app)
        else:
            sys.exit(app.exec_())
    @classmethod
    def get_main_window_geometry(cls):
        if cls.get_is_clarisse():
            return QtClarisseMtd.get_qt_main_window_geometry()


def set_qt_window_show(qt_window, pos=None, size=None, use_exec=False):
    if size is not None:
        w_0, h_0 = size
    else:
        q_size = qt_window.baseSize()
        w_0, h_0 = q_size.width(), q_size.height()
    #
    q_margin = qt_window.contentsMargins()
    wl, wt, wr, wb = q_margin.left(), q_margin.top(), q_margin.right(), q_margin.bottom()
    vl, vt, vr, vb = 0, 0, 0, 0
    w_1, h_1 = w_0 + sum([wl, vl, wr, vr]), h_0 + sum([wt, vt, wb, vb])

    p = qt_window.parent()
    if p:
        p_w, p_h = p.width(), p.height()
        o_x, o_y = p.pos().x(), p.pos().y()
    else:
        desktop_rect = get_qt_desktop_primary_rect()
        p_w, p_h = desktop_rect.width(), desktop_rect.height()
        o_x, o_y = 0, 0

    if hasattr(qt_window, '_main_window_geometry'):
        if qt_window._main_window_geometry is not None:
            o_x, o_y, p_w, p_h = qt_window._main_window_geometry

    if pos is not None:
        x, y = pos[0] + o_x, pos[1] + o_y
    else:
        x, y = (p_w - w_1) / 2 + o_x, (p_h - h_1) / 2 + o_y
    #
    qt_window.setGeometry(
        max(x, 0), max(y, 0), w_1, h_1
    )
    #
    if use_exec is True:
        qt_window.exec_()
    else:
        qt_window.show()
        qt_window.raise_()


def set_window_show_standalone(prx_window_class, show_kwargs=None, **kwargs):
    exists_app = QtWidgets.QApplication.instance()
    if exists_app is None:
        app = QtWidgets.QApplication(sys.argv)
        app.setPalette(QtDccMtd.get_palette())

        QtUtilMtd.set_fonts_add(
            utl_gui_core.RscFontFile.get_all()
        )
        prx_window = prx_window_class(**kwargs)
        prx_window.set_main_window_geometry(QtDccMtd.get_main_window_geometry())
        window = prx_window.widget
        system_tray_icon = QtSystemTrayIcon(window)
        # a = utl_gui_qt_core.QtWidgets.QAction('show', triggered=window.widget.show)
        system_tray_icon.setIcon(window.windowIcon())
        system_tray_icon.show()
        window._set_window_system_tray_icon_(system_tray_icon)
        if isinstance(show_kwargs, dict):
            prx_window.set_window_show(**show_kwargs)
        else:
            prx_window.set_window_show()
        # sys.exit(app.exec_())
        QtDccMtd.exit_app(app)
    else:
        prx_window = prx_window_class(**kwargs)
        prx_window.set_main_window_geometry(QtDccMtd.get_main_window_geometry())
        if isinstance(show_kwargs, dict):
            prx_window.set_window_show(**show_kwargs)
        else:
            prx_window.set_window_show()
        if QtDccMtd.get_is_clarisse():
            QtDccMtd.exit_app(exists_app)


class QtTreeMtd(object):
    @classmethod
    def _get_item_has_visible_children_(cls, qt_tree_widget, qt_tree_widget_item):
        qt_model_index = qt_tree_widget.indexFromItem(qt_tree_widget_item)
        raw_count = qt_tree_widget.model().rowCount(qt_model_index)
        for row in range(raw_count):
            child_index = qt_model_index.child(row, qt_model_index.column())
            if child_index.isValid():
                if qt_tree_widget.itemFromIndex(child_index).isHidden() is False:
                    return True
        return False
    @classmethod
    def get_item_is_ancestor_hidden(cls, qt_tree_widget, qt_tree_widget_item):
        qt_model_index = qt_tree_widget.indexFromItem(qt_tree_widget_item)
        ancestor_indices = cls._get_index_ancestor_indices_(qt_model_index)
        for ancestor_index in ancestor_indices:
            if qt_tree_widget.itemFromIndex(ancestor_index).isHidden() is True:
                return True
        return False
    @classmethod
    def _get_index_ancestor_indices_(cls, qt_model_index):
        def _rcs_fnc(index_):
            _parent = index_.parent()
            if _parent.isValid():
                lis.append(_parent)
                _rcs_fnc(_parent)

        lis = []
        _rcs_fnc(qt_model_index)
        return lis
    @classmethod
    def _set_item_row_draw_(cls, qt_painter, qt_option, qt_model_index):
        user_data = qt_model_index.data(QtCore.Qt.UserRole)
        if user_data:
            rect = qt_option.rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            b_w, b_h = 2, 2
            foregrounds = user_data.get('foregrounds')
            if foregrounds is not None:
                array_grid = bsc_core.RawListMtd.set_grid_to(foregrounds, 8)
                for column, a in enumerate(array_grid):
                    for row, b in enumerate(a):
                        b_x, b_y = x + (w - b_w * column) - 2, y + (h - b_h * row) - 4
                        box_rect = QtCore.QRect(
                            b_x, b_y,
                            b_w, b_h
                        )
                        qt_painter.fillRect(box_rect, b)


class QtTimer(QtCore.QTimer):
    def __init__(self, *args, **kwargs):
        super(QtTimer, self).__init__(*args, **kwargs)


class QtPrintSignals(QtCore.QObject):
    added = qt_signal(str)
    overed = qt_signal(str)
    #
    print_add_accepted = qt_signal(str)
    print_over_accepted = qt_signal(str)


class QtMethodSignals(QtCore.QObject):
    stated = qt_signal()
    running = qt_signal()
    stopped = qt_signal()
    #
    completed = qt_signal()
    error_occurred = qt_signal()


class QtCommandSignals(QtCore.QObject):
    completed = qt_signal(tuple)
    failed = qt_signal(tuple)
    #
    finished = qt_signal(tuple)


class QtMethodThread(QtCore.QThread):
    stated = qt_signal()
    running = qt_signal()
    stopped = qt_signal()
    #
    completed = qt_signal()
    failed = qt_signal(str)
    error_occurred = qt_signal()
    #
    run_started = qt_signal()
    run_finished = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtMethodThread, self).__init__(*args, **kwargs)
        self._methods = []

    def set_method_add(self, method):
        self._methods.append(method)

    def run(self):
        self.run_started.emit()
        # noinspection PyBroadException
        try:
            for i in self._methods:
                i()
            #
            self.completed.emit()
        except:
            bsc_core.ExceptionMtd.set_print()
            self.failed.emit(bsc_core.ExceptionMtd.get_stack_())
        finally:
            #
            self.run_finished.emit()

    def set_quit(self):
        self.quit()
        self.wait()
        self.deleteLater()


class QtBuildThread(QtCore.QThread):
    cache_started = qt_signal()
    cache_finished = qt_signal()
    #
    built = qt_signal(list)
    #
    run_started = qt_signal()
    run_finished = qt_signal()

    run_failed = qt_signal()

    status_changed = qt_signal(int)

    Status = bsc_configure.Status
    def __init__(self, *args, **kwargs):
        super(QtBuildThread, self).__init__(*args, **kwargs)
        self._cache_fnc = None
        self._is_killed = False

        self._status = self.Status.Waiting

    def set_cache_fnc(self, method):
        self._cache_fnc = method

    def set_mutex(self):
        pass

    def set_kill(self):
        self._status = self.Status.Killed

    def set_status(self, status):
        self._status = status
        self.status_changed.emit(status)

    def set_quit(self):
        self.set_kill()
        #
        self.quit()
        self.wait()
        self.deleteLater()

    def run(self):
        if self._status == self.Status.Waiting:
            self.run_started.emit()
            self.set_status(self.Status.Started)
            # noinspection PyBroadException
            try:
                self.cache_started.emit()
                cache = self._cache_fnc()
                self.cache_finished.emit()
                #
                self.built.emit(cache)
            except:
                self.run_failed.emit()
                self.set_status(self.Status.Failed)
                print bsc_core.ExceptionMtd.get_stack_()
            #
            finally:
                self.run_finished.emit()
                self.set_status(self.Status.Finished)


class QtBuildThreadStack(QtCore.QObject):
    run_started = qt_signal()
    run_finished = qt_signal()
    run_resulted = qt_signal(list)
    def __init__(self, *args, **kwargs):
        super(QtBuildThreadStack, self).__init__(*args, **kwargs)
        #
        self._widget = self.parent()

        self._threads = []
        self._results = []

        # self._mutex = QtCore.QMutex()

    def set_thread_create(self, cache_fnc, build_fnc, post_fnc=None):
        thread = QtBuildThread(self._widget)
        thread.set_cache_fnc(cache_fnc)
        thread.built.connect(build_fnc)
        if post_fnc is not None:
            thread.run_finished.connect(post_fnc)
        return thread

    def set_register(self, cache_fnc, build_fnc, post_fnc=None):
        thread = self.set_thread_create(cache_fnc, build_fnc, post_fnc)
        self._threads.append(thread)
        self._results.append(0)
        return thread

    def set_result_at(self, thread, result):
        if thread in self._threads:
            index = self._threads.index(thread)
            self._results[index] = result
            if sum(self._results) == len(self._results):
                self.run_finished.emit()

    def set_kill(self):
        [i.set_kill() for i in self._threads]
        # self._mutex.unlock()

    def set_quit(self):
        self.set_kill()
        for seq, i in enumerate(self._threads):
            i.quit()
            i.wait()
            i.deleteLater()
            # release
            del self._threads[seq]

    def set_start(self):
        # self._mutex.lock()
        self.run_started.emit()
        c_t = None
        for i_t in self._threads:
            i_t.run_finished.connect(
                functools.partial(self.set_result_at, i_t, 1)
            )
            #
            if c_t is None:
                i_t.start()
            else:
                c_t.run_finished.connect(i_t.start)
            #
            c_t = i_t

        # self._mutex.unlock()


class QtBuildSignals(QtCore.QObject):
    cache_started = qt_signal()
    cache_finished = qt_signal()
    #
    built = qt_signal(list)
    #
    run_started = qt_signal()
    run_finished = qt_signal()


class QtBuildRunnable(QtCore.QRunnable):
    Status = bsc_configure.Status
    def __init__(self, pool):
        super(QtBuildRunnable, self).__init__()
        self._pool = pool

        self._build_signals = QtBuildSignals()
        self._cache_fnc = None

        self._status = self.Status.Waiting

        self.setAutoDelete(True)

    def set_cache_fnc(self, method):
        self._cache_fnc = method

    def set_kill(self):
        self._status = self.Status.Killed

    def set_stop(self):
        self._status = self.Status.Stopped

    def run(self):
        if self._status == self.Status.Waiting:
            self._build_signals.run_started.emit()
            #
            self._build_signals.cache_started.emit()
            cache = self._cache_fnc()
            self._build_signals.cache_finished.emit()
            #
            self._build_signals.built.emit(cache)
            #
            self._build_signals.run_finished.emit()

    def set_start(self):
        self._pool.start(self)


class QtBuildRunnableRunner(QtCore.QObject):
    run_started = qt_signal()
    run_finished = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtBuildRunnableRunner, self).__init__(*args, **kwargs)
        #
        self._widget = self.parent()

        self._pool = QtCore.QThreadPool(self.parent())
        self._pool.setMaxThreadCount(100)
        #
        self._cache_fncs = []
        self._build_fncs = []

        self._threads = []
        self._results = []

    def set_thread_create(self, cache_fnc, build_fnc, post_fnc=None):
        runnable = QtBuildRunnable(self._pool)
        runnable.set_cache_fnc(cache_fnc)
        runnable._build_signals.built.connect(build_fnc)
        if post_fnc is not None:
            runnable._build_signals.run_finished.connect(post_fnc)
        return runnable

    def set_register(self, cache_fnc, build_fnc, post_fnc=None):
        thread = self.set_thread_create(cache_fnc, build_fnc, post_fnc)
        self._threads.append(thread)
        self._results.append(0)
        return thread

    def set_result_at(self, thread, result):
        index = self._threads.index(thread)
        self._results[index] = result
        if sum(self._results) == len(self._results):
            self.run_finished.emit()

    def set_start_by_runnable(self, runnable):
        self._pool.start(runnable)

    def set_kill(self):
        [i.set_kill() for i in self._threads]

    def set_start(self):
        self.run_started.emit()
        c_t = None
        for i_t in self._threads:
            i_t._build_signals.run_finished.connect(
                functools.partial(self.set_result_at, i_t, 1)
            )
            #
            if c_t is None:
                i_t.set_start()
            else:
                c_t._build_signals.run_finished.connect(i_t.set_start)
            #
            c_t = i_t


class QtHBoxLayout(QtWidgets.QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtHBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*Util.LAYOUT_MARGINS)
        self.setSpacing(Util.LAYOUT_SPACING)

    def _set_align_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignTop
        )

    def _set_align_left_(self):
        self.setAlignment(
            QtCore.Qt.AlignLeft
        )

    def _get_all_widgets_(self):
        list_ = []
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                item = layout.itemAt(i)
                if item:
                    widget = item.widget()
                    list_.append(widget)
        return list_

    def _delete_latest_(self):
        layout = self
        c = layout.count()
        if c:
            item = layout.itemAt(c-1)
            if item:
                widget = item.widget()
                widget.close()
                widget.deleteLater()

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.close()
                    i_widget.deleteLater()


class QtVBoxLayout(QtWidgets.QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtVBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*Util.LAYOUT_MARGINS)
        self.setSpacing(Util.LAYOUT_SPACING)

    def _set_align_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignTop
        )

    def _set_contents_margins_clear_(self):
        self.setContentsMargins(0, 0, 0, 0)


class QtGridLayout(QtWidgets.QGridLayout):
    def __init__(self, *args, **kwargs):
        super(QtGridLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*Util.LAYOUT_MARGINS)
        self.setSpacing(Util.LAYOUT_SPACING)

    def _get_widget_count_(self):
        return self.count()

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.deleteLater()

    def _add_widget_(self, widget, d=2):
        c = self.count()

        index = c
        #
        column = index % d
        row = int(index/d)
        self.addWidget(widget, row, column, 1, 1)


class QtFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QtFileDialog, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_palette())


class QtSectorChartDrawData(object):
    def __init__(self, data, position, size, align, side_w, mode):
        """
        :param data: [
            (<label>, <total-count>, <occupy-count>),
            ...
        ]
        :param position: (int(x), int(y))
        :param size: (int(w), int(h))
        :param align:
        :param side_w: int(w)
        :param mode: GuiSectorChartMode
        """
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )
    @classmethod
    def _get_basic_data_at_(cls, index, subDatum, offset, radius, tape_w, spacing, mode):
        e_r = 4
        start_angle = 90
        offset_x, offset_y = offset
        explain, value_maximum, value = subDatum
        percent = float(value) / float(max(value_maximum, 1))
        #
        text = '{} : {}%'.format(explain, bsc_core.RawValueMtd.get_percent_prettify(value=value, maximum=value_maximum))
        #
        color_percent = max(min(percent, 1), .005)
        if value_maximum == 0:
            border_rgba = 95, 95, 95, 255
            background_rgba = 95, 95, 95, 255
        else:
            if percent == 1:
                r, g, b = 63, 255, 127
                if mode is utl_gui_configure.SectorChartMode.Error:
                    r, g, b = 255, 0, 63
            elif percent == 0:
                r, g, b = 255, 0, 63
                if mode is utl_gui_configure.SectorChartMode.Error:
                    r, g, b = 63, 255, 127
            #
            elif percent > 1:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(240 - min(percent * 15, 45), 1, 1)
            else:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(45 * color_percent, 1, 1)
                if mode is utl_gui_configure.SectorChartMode.Error:
                    r, g, b = bsc_core.RawColorMtd.hsv2rgb(45 - 45 * color_percent, 1, 1)
            #
            background_rgba = r, g, b, 255
            border_rgba = r, g, b, 255
        #
        draw_percent = color_percent * .75
        #
        out_x, out_y = offset_x + index * tape_w / 2, offset_y + index * tape_w / 2
        in_x, in_y = out_x + (tape_w - spacing) / 2, out_y + (tape_w - spacing) / 2
        out_r = radius - index * tape_w
        in_r = out_r - tape_w + spacing
        #
        rim_path = QtGui.QPainterPath()
        rim_path.addEllipse(
            out_x, out_y, out_r, out_r
        )
        rim_path.addEllipse(
            in_x, in_y, in_r, in_r
        )
        #
        cx, cy = out_x + out_r/2, out_y + out_r/2
        #
        rim_sub_path = QtGui.QPainterPath()
        rim_sub_path.moveTo(cx, cy)
        sub_angle = -360 * .25
        rim_sub_path.arcTo(out_x - 1, out_y - 1, out_r + 2, out_r + 2, start_angle, sub_angle)
        #
        percent_sub_path = QtGui.QPainterPath()
        percent_sub_path.moveTo(cx, cy)
        percent_sub_angle = -360 * (1 - draw_percent)
        percent_sub_path.arcTo(out_x - 1, out_y - 1, out_r + 2, out_r + 2, start_angle, percent_sub_angle)
        #
        total_path = rim_path - rim_sub_path
        occupy_path = rim_path - percent_sub_path
        #
        x1, y1 = cx, out_y + (tape_w - spacing)/4
        x2, y2 = x1 + tape_w/4, y1
        x3, y3 = x2 + tape_w/4, y2 + tape_w/4
        x4, y4 = x3 + tape_w/4, y3
        text_line = QtGui.QPolygon(
            [QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2), QtCore.QPoint(x3, y3), QtCore.QPoint(x4 - e_r, y4)]
        )
        text_point = QtCore.QPoint(x4 + e_r + 4, y4 + 4)
        text_ellipse = QtCore.QRect(x4 - e_r, y4 - e_r, e_r * 2, e_r * 2)
        text_size = tape_w/3
        return background_rgba, border_rgba, total_path, occupy_path, text_point, text_line, text_ellipse, text_size, text
    @classmethod
    def _get_basic_data_(cls, data, offset, radius, tape_w, spacing, mode):
        lis = []
        if data:
            for i_index, i_datum in enumerate(data):
                lis.append(
                    cls._get_basic_data_at_(
                        i_index, i_datum, offset, radius, tape_w, spacing, mode
                    )
                )
        return lis
    @classmethod
    def _get_data_(cls, data, position, size, align, side_w, mode):
        if data:
            count = len(data)
            #
            pos_x, pos_y = position
            size_w, size_h = size
            align_h, align_v = align
            #
            radius = int(min(size_w, size_h)) - side_w * 2
            tape_w = int(radius/count*.75)
            #
            spacing = 8
            #
            if align_h is QtCore.Qt.AlignLeft:
                offset_x = pos_x + side_w
            elif align_h is QtCore.Qt.AlignHCenter:
                offset_x = pos_x + (size_w - radius) / 2
            else:
                offset_x = size_w - radius - side_w
            if align_v is QtCore.Qt.AlignTop:
                offset_y = pos_y + side_w
            elif align_v is QtCore.Qt.AlignVCenter:
                offset_y = pos_y + (size_h - radius) / 2
            else:
                offset_y = size_h - radius - side_w
            #
            basic_data = cls._get_basic_data_(
                data, (offset_x, offset_y), radius, tape_w, spacing, mode
            )
            return dict(
                basic=basic_data
            )

    def get(self):
        return self._draw_data


class QtProgressingChartDrawMtd(object):
    @classmethod
    def _get_basic_data_(cls, rect, index, percent, percent_range, label, show_percent, tape_w=8, spacing=8):
        percent_start, percent_end = percent_range
        start_angle = 360*(1-percent_end)
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        radius = int(min(w, h))
        rim_out_x, rim_out_y = x-index*(tape_w+spacing)/2, y-index*(tape_w+spacing)/2
        rim_in_x, rim_in_y = rim_out_x+tape_w/2, rim_out_y+tape_w/2
        #
        rim_out_r = radius+index*(tape_w+spacing)
        rim_in_r = rim_out_r-tape_w
        #
        rim_path = QtGui.QPainterPath()
        rim_path.addEllipse(
            rim_out_x, rim_out_y, rim_out_r, rim_out_r
        )
        rim_path.addEllipse(
            rim_in_x, rim_in_y, rim_in_r, rim_in_r
        )
        #
        cx, cy = rim_out_x+rim_out_r/2, rim_out_y+rim_out_r/2
        rim_sub_path = QtGui.QPainterPath()
        rim_sub_path.moveTo(cx, cy)
        percent_sub_angle = 360*(1-percent)
        rim_sub_path.arcTo(rim_out_x-1, rim_out_y-1, rim_out_r+2, rim_out_r+2, start_angle, percent_sub_angle)

        annulus_sector_path = rim_path - rim_sub_path

        annulus_sector_color = QtGui.QConicalGradient(cx, cy, start_angle)
        c = 10
        colors = []
        for i in range(c):
            i_p = float(i)/float(c)
            i_color = QtGui.QColor(*bsc_core.RawColorMtd.hsv2rgb(140*(1-i_p), .5, 1))
            colors.append(i_color)
            annulus_sector_color.setColorAt(i_p, i_color)

        annulus_sector_color.setColorAt(1, colors[0])
        #
        text_w, text_h = 240, 16
        text_spacing = 2
        #
        t_x, t_y = x+w/2, y+h+index*(text_h+text_spacing)+48
        show_name_rect_f = QtCore.QRectF(
            t_x-text_w-4, t_y, text_w, text_h
        )
        show_name_option = QtGui.QTextOption(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )
        show_percent_rect_f = QtCore.QRectF(
            t_x+4, t_y, text_w, text_h
        )
        show_percent_option = QtGui.QTextOption(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        if label:
            show_name = label
        else:
            show_name = 'process-{}'.format(index)
        #
        text_color = QtGui.QColor(*bsc_core.RawColorMtd.hsv2rgb(140*percent, .5, 1))
        return (
            annulus_sector_path, annulus_sector_color,
            show_name_rect_f, show_name_option, show_name,
            show_percent_rect_f, show_percent_option, show_percent,
            text_color
        )


class QtRadarChartDrawData(object):
    fnc_angle = math.radians
    fnc_sin = math.sin
    fnc_cos = math.cos
    fnc_tan = math.tan

    def __init__(self, data, position, size, align, side_w, mode):
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )

    def _get_data_(self, data, position, size, align, side_w, mode):
        if data:
            pos_x, pos_y = position
            size_w, size_h = size
            align_h, align_v = align
            #
            radius = int(min(size_w, size_h)) - side_w * 2
            #
            spacing = 8
            #
            if align_h is QtCore.Qt.AlignLeft:
                offset_x = pos_x + side_w
            elif align_h is QtCore.Qt.AlignHCenter:
                offset_x = pos_x + (size_w - radius) / 2
            else:
                offset_x = size_w - radius - side_w
            if align_v is QtCore.Qt.AlignTop:
                offset_y = pos_y + side_w
            elif align_v is QtCore.Qt.AlignVCenter:
                offset_y = pos_y + (size_h - radius) / 2
            else:
                offset_y = size_h - radius - side_w
            #
            mark_data = self._get_mark_data_(
                data,
                (offset_x, offset_y),
                radius,
                spacing
            )
            #
            basic_data = self._get_basic_data_(
                data, (offset_x, offset_y), radius, spacing
            )
            image_data = self._get_image_data_(
                data, (offset_x, offset_y), radius, spacing
            )
            map_data = self._get_map_data_(
                mark_data, (offset_x, offset_y), radius
            )
            return dict(
                image=image_data,
                basic=basic_data,
                map=map_data,
                mark=mark_data
            )
    @classmethod
    def _get_basic_data_points_(cls, cx, cy, radius, count):
        lis = []
        for seq in range(count):
            angle = 360 * float(seq) / float(count) + 180
            x, y = cx + cls.fnc_sin(cls.fnc_angle(angle)) * radius / 2, cy + cls.fnc_cos(
                cls.fnc_angle(angle)) * radius / 2
            lis.append(QtCore.QPoint(x, y))
        #
        return lis + lis[0:1]
    @classmethod
    def _get_basic_data_(cls, data, offset, radius, spacing):
        offset_x, offset_y = offset
        count = len(data)
        cx, cy = offset_x + radius / 2, offset_y + radius / 2
        #
        basic_polygons = []
        for i in range(6):
            r = radius * float(i + 1) / float(6)
            i_polygon = QtGui.QPolygon(
                cls._get_basic_data_points_(cx, cy, r, count)
            )
            basic_polygons.append(i_polygon)
        #
        basic_polygons.reverse()
        return basic_polygons
    @classmethod
    def _get_image_data_(cls, data, offset, radius, spacing):
        offset_x, offset_y = offset
        count = len(data)
        cx, cy = offset_x + radius / 2, offset_y + radius / 2
        #
        image_path = QtGui.QPainterPath()
        image_path.addPolygon(
            QtGui.QPolygonF(cls._get_basic_data_points_(cx, cy, radius, count))
        )
        #
        return image_path
    @classmethod
    def _get_map_data_(cls, mark_data, offset, radius):
        offset_x, offset_y = offset
        start_angle = 90
        cx, cy = offset_x + radius / 2, offset_y + radius / 2
        #
        points_src = []
        points_tgt = []
        colors = []
        if mark_data:
            for i in mark_data:
                background_rgba, border_rgba, basicPath, textPoint0, textPoint1, text_0, text_1, serverMapPoint, localMapPoint, mapEllipse = i
                points_src.append(serverMapPoint)
                points_tgt.append(localMapPoint)
                colors.append(background_rgba)
        #
        g_c = QtGui.QConicalGradient(cx, cy, start_angle)
        for seq, i_rgba in enumerate(colors):
            i_r, i_g, i_b, i_a = i_rgba
            g_c.setColorAt(float(seq) / float(len(colors)), QtGui.QColor(i_r, i_g, i_b, 127))
        #
        r, g, b, a = colors[0]
        g_c.setColorAt(1, QtGui.QColor(r, g, b, 127))
        #
        map_brush = QtGui.QBrush(g_c)
        #
        map_polygon_src = QtGui.QPolygon(points_src)
        map_polygon_tgt = QtGui.QPolygon(points_tgt)
        return map_brush, map_polygon_src, map_polygon_tgt
    @classmethod
    def _get_mark_data_at_(cls, index, index_maximum, value_maximum, data, offset_x, offset_y, radius, spacing):
        e_r = 4
        start_angle = -90
        explain, value_src, value_tgt = data
        #
        percent_src = float(value_src) / float(max(value_maximum, 1))
        percent_tgt = float(value_tgt) / float(max(value_maximum, 1))
        #
        value_sub = value_tgt - value_src
        percent_sub = float(value_sub) / float(max(value_src, 1))
        text_0 = explain
        if value_sub == 0:
            text_1 = '{}'.format(bsc_core.RawIntegerMtd.get_prettify(value_tgt))
        else:
            text_1 = '{} ( {}% )'.format(
                bsc_core.RawIntegerMtd.get_prettify(value_tgt),
                bsc_core.RawValueMtd.get_percent_prettify(value=value_sub, maximum=value_src)
            )
        #
        if value_maximum == 0:
            border_rgba = 95, 95, 95, 255
            background_rgba = 95, 95, 95, 255
        else:
            if percent_sub == 0:
                r, g, b = 64, 255, 127
            elif percent_sub > 0:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(45 * (1 - min(percent_sub, 1)), 1, 1)
            else:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(120 + 45 * (1 - min(percent_sub, 1)), 1, 1)
            #
            background_rgba = r, g, b, 255
            border_rgba = r, g, b, 255
        #
        draw_percent_src = percent_src * .75
        draw_percent_tgt = percent_tgt * .75
        #
        x, y = offset_x, offset_y
        r = radius
        cx, cy = x + r / 2, y + r / 2
        basic_path = QtGui.QPainterPath()
        basic_path.moveTo(cx, cy)
        angle_start = 360 * (float(index) / float(index_maximum)) + 180
        angle_end = 360 * (float(index + 1) / float(index_maximum)) + 180
        basic_path.arcTo(x, y, r, r, angle_start + start_angle, angle_end + start_angle)
        #
        text_x_0, text_y_0 = cx + cls.fnc_sin(cls.fnc_angle(angle_start)) * radius / 2, cy + cls.fnc_cos(
            cls.fnc_angle(angle_start)) * radius / 2
        #
        map_x_0, map_y_0 = cx + cls.fnc_sin(
            cls.fnc_angle(angle_start)) * radius / 2 * draw_percent_tgt, cy + cls.fnc_cos(
            cls.fnc_angle(angle_start)) * radius / 2 * draw_percent_tgt
        map_x_1, map_y_1 = cx + cls.fnc_sin(
            cls.fnc_angle(angle_start)) * radius / 2 * draw_percent_src, cy + cls.fnc_cos(
            cls.fnc_angle(angle_start)) * radius / 2 * draw_percent_src
        #
        f = QtGui.QFont()
        f.setPointSize(8)
        m = QtGui.QFontMetrics(f)
        text_w_0 = m.width(explain)
        text_w_1 = m.width(text_1)
        text_h = m.height()
        #
        text_point_0 = QtCore.QPoint(text_x_0 - text_w_0 / 2, text_y_0 - text_h / 2)
        text_point_1 = QtCore.QPoint(text_x_0 - text_w_1 / 2, text_y_0 + text_h / 2)
        mark_ellipse = QtCore.QRect(map_x_0 - e_r, map_y_0 - e_r, e_r * 2, e_r * 2)
        #
        point_tgt = QtCore.QPoint(map_x_0, map_y_0)
        point_src = QtCore.QPoint(map_x_1, map_y_1)
        return background_rgba, border_rgba, basic_path, text_point_0, text_point_1, text_0, text_1, point_src, point_tgt, mark_ellipse
    @classmethod
    def _get_mark_data_(cls, data, offset, radius, spacing):
        offset_x, offset_y = offset
        lis = []
        if data:
            index_maximum = len(data)
            value_maximum = max([i[2] for i in data])
            for i_index, i_data in enumerate(data):
                lis.append(
                    cls._get_mark_data_at_(
                        i_index,
                        index_maximum,
                        value_maximum,
                        i_data,
                        offset_x, offset_y,
                        radius,
                        spacing
                    )
                )
        return lis

    def get(self):
        return self._draw_data


class QtPieChartDrawData(object):
    fnc_angle = math.radians
    fnc_sin = math.sin
    fnc_cos = math.cos
    fnc_tan = math.tan

    def __init__(self, data, position, size, align, side_w, mode):
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )

    def _get_data_(self, data, position, size, align, side_w, mode):
        if data:
            basic_data = self._get_basic_data_(data, position, size, side_w)
            return basic_data
        return
    @classmethod
    def _get_basic_data_(cls, data, position, size, side):
        def rcs_fnc_(i_data_, i_seq_=0, qa=90, ma=0):
            _i_name, _i_value, color = i_data_[i_seq_]
            _i_color = bsc_core.RawTextOpt(_i_name).to_rgb()
            #
            p = float(_i_value) / float(maximum)
            _a = 360 * p
            a = 360 - _a
            s = ma + _a / 2
            _xo = cls.fnc_sin(cls.fnc_angle(s)) * (side / 4)
            _yo = cls.fnc_cos(cls.fnc_angle(s)) * (side / 4)
            #
            piePath = QtGui.QPainterPath()
            _s = 4
            cx = w1 / 2 + _s / 2 + x1
            cy = w1 / 2 + _s / 2 + y1
            piePath.moveTo(cx, cy)
            piePath.arcTo(x1 - _s / 2, y1 - _s / 2, w1 + _s, w1 + _s, qa, a)
            #
            _i_path = rimPath - piePath
            _i_shadow_path = rimPath - piePath
            #
            _i_percent = '{}%'.format(
                bsc_core.RawValueMtd.get_percent_prettify(value=_i_value, maximum=maximum)
            )
            #
            lis.append(
                (_i_color, _i_name, _i_value, _i_percent, _i_path, _i_shadow_path, (_xo, -_yo), False)
            )
            #
            i_seq_ += 1
            qa += a
            ma += _a
            if i_seq_ <= dataCount - 1:
                rcs_fnc_(i_data_, i_seq_, qa, ma)

        #
        pos_x, pos_y = position
        width, height = size
        lis = []
        if data:
            dataCount = len(data)
            maximum = sum([i[1] for i in data])
            if maximum > 0:
                radius = min(width, height)
                w = radius - side * 2
                x = side
                y = side
                #
                x1 = x
                y1 = y
                w1 = w
                rimPath = QtGui.QPainterPath()
                rimPath.addEllipse(x1, y1, w1, w1)
                #
                w2 = w1 / 2
                x2 = (w1 - w2) / 2 + x1
                y2 = (w1 - w2) / 2 + y1
                rimPath.addEllipse(x2, y2, w2, w2)
                #
                rcs_fnc_(data)
        return lis

    def get(self):
        return self._draw_data


class QtHistogramChartDrawData(object):
    def __init__(self, data, position, size, align, side_w, mode):
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )

    def _get_data_(self, data, position, size, align, side_w, mode):
        if data:
            basic_data = self._get_basic_data_(data, position, size, side_w)
            return basic_data
        return

    @classmethod
    def _get_basic_data_(cls, data, position, size, side):
        pass

    def get(self):
        return self._draw_data


class QtWidgetAction(QtWidgets.QWidgetAction):
    def __init__(self, *args, **kwargs):
        super(QtWidgetAction, self).__init__(*args, **kwargs)
        #
        self.setFont(Font.NAME)


class QtMenuOpt(object):
    def __init__(self, menu):
        if isinstance(menu, QtWidgets.QMenu):
            self._root_menu = menu
            self._item_dic = {
                '/': self._root_menu
            }
        else:
            raise RuntimeError()
    @utl_core.Modifier.exception_catch
    def _set_cmd_debug_run_(self, cmd_str):
        exec cmd_str
    @utl_core.Modifier.exception_catch
    def _set_fnc_debug_run_(self, fnc):
        fnc()

    def set_create_by_content(self, content):
        self._root_menu.clear()
        self._item_dic = {
            '/': self._root_menu
        }
        if isinstance(content, bsc_abstracts.AbsContent):
            keys = content.get_keys(regex='*.properties')
            for i_key in keys:
                i_atr_path_opt = bsc_core.DccAttrPathOpt(i_key)
                i_obj_path = i_atr_path_opt.obj_path
                i_obj_path_opt = bsc_core.DccPathDagOpt(i_obj_path)
                i_content = content.get_content(i_key)
                i_type = i_content.get('type')
                if i_obj_path_opt.get_is_root():
                    pass
                else:
                    menu = self.__get_menu_(i_obj_path_opt.get_parent())
                    if i_type == 'separator':
                        self.set_separator_add(menu, i_content)
                    elif i_type == 'action':
                        self.set_action_add(menu, i_content)

    def __get_menu_(self, path_opt):
        cur_menu = self._root_menu
        components = path_opt.get_components()
        components.reverse()
        for i_component in components:
            cur_menu = self.__get_menu_force_(cur_menu, i_component)
        return cur_menu

    def __get_menu_force_(self, menu, path_opt):
        path = path_opt.path
        if path in self._item_dic:
            return self._item_dic[path]
        #
        name = path_opt.name
        widget_action = QtWidgetAction(menu)
        menu.addAction(widget_action)
        widget_action.setFont(Font.NAME)
        widget_action.setText(name)
        widget_action.setIcon(
            QtIconMtd.create_by_icon_name('file/folder')
        )
        sub_menu = menu.__class__(menu)
        sub_menu.setTearOffEnabled(True)
        widget_action.setMenu(sub_menu)
        self._item_dic[path] = sub_menu
        return sub_menu
    #
    @classmethod
    def set_separator_add(cls, menu, content):
        name = content.get('name')
        separator = menu.addSeparator()
        separator.setFont(Font.SEPARATOR)
        separator.setText(name)
        return separator

    def set_action_add(self, menu, content):
        def set_disable_fnc_(widget_action_):
            widget_action_.setFont(Font.disable)
            widget_action_.setDisabled(True)

        #
        name = content.get('name')
        icon_name = content.get('icon_name')
        executable_fnc = content.get('executable_fnc')
        execute_fnc = content.get('execute_fnc')
        widget_action = QtWidgetAction(menu)
        widget_action.setFont(Font.NAME)
        widget_action.setText(name)
        menu.addAction(widget_action)
        if icon_name:
            widget_action.setIcon(
                QtIconMtd.create_by_icon_name(icon_name)
            )
        else:
            widget_action.setIcon(
                QtUtilMtd.get_name_text_icon_(name, background_color=(64, 64, 64))
            )
        #
        if isinstance(executable_fnc, (bool, int)):
            executable = executable_fnc
            if executable is False:
                set_disable_fnc_(widget_action)
        elif isinstance(executable_fnc, (types.FunctionType, types.MethodType)):
            executable = executable_fnc()
            if executable is False:
                set_disable_fnc_(widget_action)
        #
        if isinstance(execute_fnc, (types.FunctionType, types.MethodType)):
            fnc = execute_fnc
            widget_action.triggered.connect(
                fnc
            )
        elif isinstance(execute_fnc, six.string_types):
            cmd = execute_fnc
            widget_action.triggered.connect(
                lambda *args, **kwargs: self._set_cmd_debug_run_(cmd)
            )
        return widget_action


class ApplicationOpt(object):
    def __init__(self, app=None):
        if app is None:
            self._instance = QtWidgets.QApplication.instance()
        else:
            self._instance = None

    def set_process_run_0(self):
        if self._instance:
            self._instance.processEvents(
                QtCore.QEventLoop.ExcludeUserInputEvents
            )

    def set_process_run_1(self):
        if self._instance:
            self._instance.processEvents()


class QtPainterPath(QtGui.QPainterPath):
    def __init__(self, *args):
        super(QtPainterPath, self).__init__(*args)
        self.setFillRule(QtCore.Qt.WindingFill)
    #
    def _set_points_add_(self, points):
        points_ = [QtCore.QPointF(x, y) for x, y in points]
        self.addPolygon(QtGui.QPolygonF(points_))


class QtRawColorMtd(object):
    @classmethod
    def _get_image_draw_args_by_text_(cls, text):
        return cls._get_image_draw_args_by_color_(
            *bsc_core.RawTextOpt(text).to_rgb_0(s_p=50, v_p=50)
        )
    @classmethod
    def _get_image_draw_args_by_color_(cls, *args):
        if len(args) == 3:
            b_r, b_g, b_b = args
            b_a = 255
        elif len(args) == 4:
            b_r, b_g, b_b, b_a = args
        else:
            raise TypeError()
        t_r, t_g, t_b = bsc_core.RawColorMtd.get_complementary_rgb(b_r, b_g, b_b)
        b_l = QtGui.qGray(t_r, t_g, t_b)
        if b_l >= 127:
            t_l = 239
        else:
            t_l = 15
        return (b_r, b_g, b_b, b_a), (t_l, t_l, t_l, 255)


class QtPainter(QtGui.QPainter):
    @classmethod
    def _get_qt_color_(cls, *args):
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, (QtGui.QColor, QtGui.QLinearGradient, QtGui.QConicalGradient)):
                return _
            elif isinstance(_, (tuple, list)):
                return cls._to_qt_color_(*_)
        else:
            return cls._to_qt_color_(*args)
    @classmethod
    def _to_qt_color_(cls, *args):
        if len(args) == 3:
            r, g, b = args
            a = 255
        elif len(args) == 4:
            r, g, b, a = args
        else:
            raise TypeError()
        return QtGui.QColor(r, g, b, a)
    #
    def __init__(self, *args, **kwargs):
        super(QtPainter, self).__init__(*args, **kwargs)
        self.setRenderHint(self.Antialiasing)

    def _draw_capsule_by_rects_(self, rects, texts, states, hovered_index, pressed_index, use_exclusive=False):
        c = len(texts)
        self._set_antialiasing_()
        for i, i_text in enumerate(texts):
            i_rect = rects[i]
            i_x, i_y = i_rect.x()+1, i_rect.y()
            i_w, i_h = i_rect.width()-2, i_rect.height()
            if i == pressed_index:
                i_x += 2
                i_w -= 2
                i_y += 2
                i_h -= 2
            #
            i_new_rect = QtCore.QRect(
                i_x, i_y, i_w, i_h
            )
            if use_exclusive is True:
                i_border_radius = 3
            else:
                i_border_radius = i_h/2

            i_state = states[i]
            if i_state is True:
                i_border_width = 2
                if use_exclusive is True:
                    i_background_color, i_font_color = QtBackgroundColors.Selected, QtFontColors.Black
                else:
                    i_background_color, i_font_color = QtRawColorMtd._get_image_draw_args_by_text_(i_text)
                self._set_background_color_(i_background_color)
                self._set_border_color_(QtBorderColors.Button)
            else:
                i_border_width = 1
                i_font_color = QtFontColors.Dark
                self._set_background_color_(QtBackgroundColors.Dim)
                self._set_border_color_(QtBorderColors.Dim)
            #
            if i == hovered_index:
                self._set_border_color_(QtBorderColors.Hovered)
            #
            self._set_border_width_(i_border_width)
            # left
            if i == 0:
                if c == 1:
                    i_path_0 = QtGui.QPainterPath()
                    i_path_0.addRoundedRect(
                        QtCore.QRectF(i_x, i_y, i_w, i_h),
                        i_border_radius, i_border_radius, QtCore.Qt.AbsoluteSize
                    )
                    self.drawPath(
                        i_path_0
                    )
                else:
                    i_path_0 = QtGui.QPainterPath()
                    i_path_0.addRoundedRect(
                        QtCore.QRectF(i_x, i_y, i_w-2, i_h),
                        i_border_radius, i_border_radius, QtCore.Qt.AbsoluteSize
                    )
                    i_path_1 = QtGui.QPainterPath()
                    i_path_1.addRect(
                        QtCore.QRectF(i_x+i_w/2, i_y, i_w/2, i_h)
                    )
                    self.drawPath(
                        i_path_0+i_path_1
                    )
            # right
            elif i == (c-1):
                if c > 1:
                    i_path_0 = QtGui.QPainterPath()
                    i_path_0.addRoundedRect(
                        QtCore.QRectF(i_x, i_y, i_w, i_h),
                        i_border_radius, i_border_radius, QtCore.Qt.AbsoluteSize
                    )
                    i_path_1 = QtGui.QPainterPath()
                    i_path_1.addRect(
                        QtCore.QRectF(i_x, i_y, i_w/2, i_h)
                    )
                    self.drawPath(
                        i_path_0+i_path_1
                    )
            # middle
            else:
                if c > 1:
                    self.drawRect(
                        i_new_rect
                    )
            #
            self._set_font_(QtFonts.Label)
            self._set_font_color_(i_font_color)
            # noinspection PyArgumentEqualDefault
            self.drawText(
                i_new_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                i_text
            )

    def _draw_tab_buttons_by_rects_(self, frame_rect, rects, name_texts, icon_name_texts, hovered_index, pressed_index, current_index):
        for i_index, i_name_text in enumerate(name_texts):
            i_rect = rects[i_index]
            i_icon_name_text = icon_name_texts[i_index]
            i_is_hovered = i_index == hovered_index
            i_is_pressed = i_index == pressed_index
            i_is_current = i_index == current_index
            if i_is_current is False:
                self._draw_tab_button_at_(
                    frame_rect, i_rect, i_name_text, i_icon_name_text, i_is_hovered, i_is_pressed, i_is_current
                )
        # draw current
        for i_index, i_name_text in enumerate(name_texts):
            i_rect = rects[i_index]
            i_icon_name_text = icon_name_texts[i_index]
            i_is_hovered = i_index == hovered_index
            i_is_pressed = i_index == pressed_index
            i_is_current = i_index == current_index
            if i_is_current is True:
                self._draw_tab_button_at_(
                    frame_rect, i_rect, i_name_text, i_icon_name_text, i_is_hovered, i_is_pressed, i_is_current
                )

    def _draw_tab_button_at_(self, frame_rect, rect, text, icon_name_text, is_hovered, is_pressed, is_current):
        f_x, f_y = frame_rect.x(), frame_rect.y()
        f_w, f_h = frame_rect.width(), frame_rect.height()
        a = 255
        if is_current:
            background_color = QtGui.QColor(63, 63, 63, a)
        else:
            background_color = QtGui.QColor(95, 95, 95, a)
        #
        if is_hovered is True:
            color_hovered = QtGui.QColor(127, 127, 127, a)
        else:
            color_hovered = background_color
        #
        start_coord, end_coord = rect.topLeft(), rect.bottomLeft()
        l_color_0 = QtGui.QLinearGradient(start_coord, end_coord)
        l_color_1 = QtGui.QLinearGradient(start_coord, end_coord)
        l_color_0.setColorAt(0, color_hovered)
        l_color_1.setColorAt(0, color_hovered)
        l_color_0.setColorAt(0.5, background_color)
        #
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        if is_pressed is True:
            offset = 2
            x += offset
            y += offset
            w -= offset
            h -= offset
        #
        r = h
        if is_current is True:
            frm_x, frm_y = x, y+1
            frm_w, frm_h = w+r, h-1
            border_width = 2
            frame_coords = [
                (f_x, frm_y+frm_h),
                # bottom left, top left, top right, bottom right, ...
                (frm_x, frm_y+frm_h), (frm_x+frm_h, frm_y), (frm_x+frm_w-frm_h, frm_y), (frm_x+frm_w, frm_y+frm_h),
                (f_w, frm_y+frm_h),
            ]
        else:
            frm_x, frm_y = x, y+2
            frm_w, frm_h = w+r, h-2
            border_width = 1
            frame_coords = [
                (frm_x, frm_y+frm_h), (frm_x+frm_h, frm_y), (frm_x+frm_w-frm_h, frm_y), (frm_x+frm_w, frm_y+frm_h),
            ]
        #
        self._set_border_color_(QtBorderColors.Dim)
        self._set_border_width_(border_width)
        self._set_background_color_(l_color_0)
        #
        self._draw_path_by_coords_(frame_coords)
        #
        if icon_name_text is not None:
            coords = [
                (frm_x+frm_w-frm_h, frm_y+frm_h), (frm_x+frm_w-frm_h*2, frm_y+1), (frm_x+frm_w-frm_h, frm_y+1), (frm_x+frm_w-1, frm_y+frm_h),
                (frm_x+frm_w-frm_h, frm_y+frm_h),
            ]
            i_r, i_g, i_b = bsc_core.RawTextOpt(icon_name_text).to_rgb_0(s_p=50, v_p=50)
            self._set_border_width_(1)
            self._set_border_color_(QtBorderColors.Transparent)
            l_color_1.setColorAt(0.5, QtGui.QColor(i_r, i_g, i_b, a))
            if is_hovered is True:
                self._set_background_color_(l_color_1)
            else:
                self._set_background_color_(i_r, i_g, i_b)
            self._draw_path_by_coords_(coords)
        #
        if text is not None:
            txt_rect = QtCore.QRect(
                frm_x, frm_y, frm_w, frm_h
            )
            text_option = QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
            self._set_font_(
                get_font(size=10, weight=75)
            )
            self._set_font_color_(QtFontColors.Basic)
            self.drawText(
                txt_rect,
                text_option,
                text,
            )

    def _draw_frame_color_with_name_text_by_rect_(self, rect, text, offset):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        frm_x, frm_y = x+offset, y+offset
        frm_w = frm_h = h-offset
        bsc_w, bsc_h = w-offset, h-offset
        coords = [
            (frm_x+bsc_w-frm_w*2, frm_y+frm_h), (frm_x+bsc_w-frm_w, frm_y), (frm_x+bsc_w, frm_y), (frm_x+bsc_w, frm_y+frm_h)
        ]
        i_r, i_g, i_b = bsc_core.RawTextOpt(text).to_rgb_0(s_p=50, v_p=50)
        self._set_background_color_(i_r, i_g, i_b)
        self._draw_path_by_coords_(coords)
        #
        txt_rect = QtCore.QRect(
            frm_x+bsc_w-frm_w-frm_w*.25, frm_y, frm_w, frm_h
        )
        self._set_font_(
            get_font(size=int(frm_h*.675), weight=75, italic=True)
        )
        self._set_font_color_(i_r*.75, i_g*.75, i_b*.75)
        self.drawText(
            txt_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(text[0]).upper()
        )

    def _draw_index_by_rect_(self, rect, text, offset):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        frm_r = 20
        frm_w, frm_h = frm_r-offset, frm_r-offset
        frm_x, frm_y = x+w-frm_r+offset, y+offset

        coords = [
            (frm_x, frm_y), (frm_x+frm_w, frm_y), (frm_x+frm_w, frm_y+frm_h),
            (frm_x, frm_y),
        ]
        self._set_border_color_(QtBorderColors.Transparent)
        self._set_background_color_(QtBackgroundColors.Dark)
        self._draw_path_by_coords_(coords)

        txt_r = 12
        txt_w, txt_h = txt_r-offset, txt_r-offset
        txt_x, txt_y = x+w-txt_r+offset-2, y+offset+2
        txt_rect = QtCore.QRect(
            txt_x, txt_y, txt_w, txt_h
        )
        self._set_font_color_(QtFontColors.Dark)
        self._set_font_(
            get_font(size=int(txt_r*.5)-offset, italic=True)
        )
        self.drawText(
            txt_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop,
            text
        )

    def _draw_popup_frame_(self, rect, margin, side, shadow_radius, region, border_color, background_color, border_width=1):
        x, y = rect.x(), rect.y()
        #
        w, h = rect.width(), rect.height()
        #
        _s = shadow_radius
        #
        f_x, f_y = x+margin+side, y+margin+side
        f_w, f_h = w-margin*2-_s-side*2, h-margin*2-_s-side*2
        # frame
        path1 = QtGui.QPainterPath()
        path1.addRect(QtCore.QRectF(f_x, f_y, f_w, f_h))
        path2 = QtGui.QPainterPath()
        # shadow
        path1_ = QtGui.QPainterPath()
        path1_.addRect(QtCore.QRectF(f_x+_s-1, f_y+_s-1, f_w, f_h))
        path2_ = QtGui.QPainterPath()
        #
        x1, x2, x3 = f_x+margin, f_x+margin*2, f_x+margin*3
        _x1, _x2, _x3 = f_x+f_w-margin*3, f_x+f_w-margin*2, f_x+f_w-margin
        #
        y1, y2, y3 = f_y+1, f_y-margin+1, f_y+1
        _y1, _y2, _y3 = f_y+f_h-1, f_y+f_h+margin-1, f_y+f_h-1
        if region == 0:
            path2.addPolygon(QtGui.QPolygonF([QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2), QtCore.QPointF(x3, y3)]))
            path2_.addPolygon(QtGui.QPolygonF([QtCore.QPointF(x1+_s, y1+_s), QtCore.QPointF(x2+_s, y2+_s), QtCore.QPointF(x3+_s, y3+_s)]))
        elif region == 1:
            path2.addPolygon(QtGui.QPolygonF([QtCore.QPointF(_x1, y1), QtCore.QPointF(_x2, y2), QtCore.QPointF(_x3, y3)]))
            path2_.addPolygon(QtGui.QPolygonF([QtCore.QPointF(_x1+_s, y1+_s), QtCore.QPointF(_x2+_s, y2+_s), QtCore.QPointF(_x3+_s, y3+_s)]))
        elif region == 2:
            path2.addPolygon(QtGui.QPolygonF([QtCore.QPointF(x1, _y1), QtCore.QPointF(x2, _y2), QtCore.QPointF(x3, _y3)]))
            path2_.addPolygon(QtGui.QPolygonF([QtCore.QPointF(x1+_s, _y1+_s), QtCore.QPointF(x2+_s, _y2+_s), QtCore.QPointF(x3+_s, _y3+_s)]))
        else:
            path2.addPolygon(QtGui.QPolygonF([QtCore.QPointF(_x1, _y1), QtCore.QPointF(_x2, _y2), QtCore.QPointF(_x3, _y3)]))
            path2_.addPolygon(QtGui.QPolygonF([QtCore.QPointF(_x1+_s, _y1+_s), QtCore.QPointF(_x2+_s, _y2+_s), QtCore.QPointF(_x3+_s, _y3+_s)]))
        #
        self._set_border_color_(QtBorderColors.Transparent)
        self._set_background_color_(QtBackgroundColors.Shadow)
        shadow_path = path1_+path2_
        self.drawPath(shadow_path)
        #
        self._set_border_color_(border_color)
        self._set_background_color_(background_color)
        self._set_border_width_(border_width)
        frame_path = path1+path2
        self._set_antialiasing_(False)
        self.drawPath(frame_path)

    def _set_font_color_(self, *args):
        self._set_border_color_(*args)

    def _set_border_color_(self, *args):
        qt_color = Color._get_qt_color_(*args)
        pen = QtGui.QPen(qt_color)
        pen.setCapStyle(QtCore.Qt.SquareCap)
        pen.setJoinStyle(QtCore.Qt.BevelJoin)
        self.setPen(pen)

    def _set_border_style_(self, style):
        pen = self.pen()
        pen.setStyle(style)
        self.setPen(pen)

    def _set_border_color_alpha_(self, alpha):
        color = self.pen().color()
        color.setAlpha(alpha)
        self.setPen(QtGui.QPen(color))

    def _get_border_color_(self):
        return self.pen().color()

    def _set_background_color_(self, *args):
        qt_color = Color._get_qt_color_(*args)
        self.setBrush(QtGui.QBrush(qt_color))

    def _get_background_color_(self):
        return self.brush().color()

    def _set_background_style_(self, style):
        brush = self.brush()
        brush.setStyle(style)
        self.setBrush(brush)

    def _set_background_brush_(self, brush):
        self.setBrush(brush)

    def _get_font_(self):
        return self.font()

    def _set_font_(self, font):
        self.setFont(font)

    def _set_font_size_(self, size):
        f = self.font()
        f.setPointSize(size)
        self.setFont(f)

    def _set_font_option_(self, size, weight):
        f = self.font()
        f.setPointSize(size)
        f.setWeight(weight)
        self.setFont(f)

    def _set_border_width_(self, size):
        pen = self.pen()
        pen.setWidth(size)
        self.setPen(pen)

    def _set_border_join_(self, join):
        pen = self.pen()
        pen.setJoinStyle(join)
        self.setPen(pen)

    def _set_pixmap_draw_by_rect_(self, rect, pixmap, offset=0, enable=True):
        if offset != 0:
            rect_ = QtCore.QRect(
                rect.x() + offset, rect.y() + offset,
                rect.width() - offset, rect.height() - offset
            )
        else:
            rect_ = rect
        #
        rect_size = rect.size()
        # QtGui.QPixmap()
        new_pixmap = pixmap.scaled(
            rect_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        if enable is False:
            new_pixmap = QtPixmapMtd._to_gray_(new_pixmap)
        #
        self.drawPixmap(
            rect_,
            new_pixmap
        )
        #
        self.device()

    def _draw_empty_image_by_rect_(self, rect, icon_name=None):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        r = min(w, h)
        frm_r = max(min(r * .5, 128), 32)
        frm_w, frm_h = frm_r, frm_r
        rect = QtCore.QRect(
            x + (w - frm_w) / 2, y + (h - frm_h) / 2, frm_w, frm_h
        )
        self._draw_icon_file_by_rect_(
            rect=rect, file_path=utl_gui_core.RscIconFile.get(icon_name)
        )

    def _draw_empty_text_by_rect_(self, rect, text, sub_text=None):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        r = min(w, h)
        r = max(min(r*.5, 128), 32)
        font = get_font(size=r*.5, weight=75, italic=True)
        self._set_font_(font)
        self._set_border_color_((31, 31, 31, 255))
        f_h = self.fontMetrics().height()
        f_w = self.fontMetrics().width(text)+f_h
        #
        f_x, f_y = x+(w-f_w)/2, y+(h-f_h)/2
        text_rect = QtCore.QRect(
            f_x, f_y, f_w, f_h
        )
        self.drawText(
            text_rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            text
        )
        if sub_text:
            self._set_font_(get_font(size=10, weight=75, italic=True))
            sub_text_rect = QtCore.QRect(
                x, y+(h-f_h)/2+f_h, w, 20
            )
            self.drawText(
                sub_text_rect,
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                sub_text
            )

    def _draw_icon_file_by_rect_(self, rect, file_path, offset=0, frame_rect=None, is_hovered=False, hover_color=None):
        if file_path:
            if frame_rect is not None:
                background_color = self._get_item_background_color_1_by_rect_(
                    frame_rect,
                    is_hovered=is_hovered
                )
                self._draw_frame_by_rect_(
                    frame_rect,
                    border_color=QtBorderColors.Transparent,
                    background_color=background_color,
                    border_radius=4,
                    offset=offset
                )
            #
            if file_path.endswith('.svg'):
                self._draw_svg_by_rect_(
                    rect=rect,
                    file_path=file_path,
                    offset=offset,
                    is_hovered=is_hovered,
                    hover_color=hover_color,
                )
            else:
                self._draw_image_by_rect_(
                    rect=rect,
                    file_path=file_path,
                    offset=offset,
                    is_hovered=is_hovered,
                    hover_color=hover_color,
                )

    def _set_any_image_draw_by_rect_(self, rect, file_path, offset=0):
        if file_path:
            if os.path.isfile(file_path):
                if file_path.endswith('.svg'):
                    self._draw_svg_by_rect_(rect, file_path, offset)
                elif file_path.endswith('.exr'):
                    self._set_exr_image_draw_by_rect_(rect, file_path, offset)
                elif file_path.endswith('.mov'):
                    self._set_mov_image_draw_by_rect_(rect, file_path, offset)
                else:
                    self._draw_image_by_rect_(
                        rect, file_path, offset,
                        cache_resize=True
                    )

    def _draw_svg_by_rect_(self, rect, file_path, offset=0, is_hovered=False, hover_color=None):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        rectF = QtCore.QRectF(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        svg_render = QtSvg.QSvgRenderer(file_path)
        svg_render.render(self, rectF)
        if is_hovered is True:
            m_w, m_h = rect_.width()*2, rect_.height()*2
            mask_image = QtGui.QImage(
                m_w, m_h, QtGui.QImage.Format_ARGB32
            )
            mask_image.fill(QtCore.Qt.black)
            painter = QtGui.QPainter(mask_image)
            svg_render.render(painter, QtCore.QRectF(0, 0, m_w, m_h))
            painter.end()
            #
            hover_pixmap = QtGui.QPixmap(mask_image)
            mask_pixmap = QtGui.QPixmap(mask_image)
            mask = mask_pixmap.createMaskFromColor(QtCore.Qt.black)
            mask.scaled(
                rect_.size(),
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            c = hover_color or QtGui.QColor(255, 127, 63, 127)
            hover_pixmap.fill(QtGui.QColor(c.red(), c.green(), c.blue(), 127))
            hover_pixmap.setMask(mask)
            rect__ = QtCore.QRect(
                rect_.x(), rect_.y(),
                rect_.width(), rect_.height()
            )
            self.drawPixmap(
                rect__,
                hover_pixmap
            )
        #
        self.device()

    def _draw_image_by_rect_(self, rect, file_path, offset=0, is_hovered=False, hover_color=None, cache_resize=False):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        #
        rect_size = rect_.size()
        w, h = rect_size.width(), rect_size.height()
        image = QtGui.QImage(file_path)
        scaled_image = image.scaled(
            rect_size,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        if cache_resize is True:
            if file_path.endswith('.png'):
                tmp_path = bsc_core.StgTmpThumbnailMtd.get_qt_file_path_(file_path, width=max(w, h), ext='.png')
                if bsc_core.StgPathMtd.get_is_exists(tmp_path) is False:
                    bsc_core.StgFileOpt(tmp_path).create_directory()
                    scaled_image.save(tmp_path)
                #
                scaled_image = QtGui.QImage(tmp_path)
        #
        new_pixmap = QtGui.QPixmap(scaled_image)
        self.drawPixmap(
            rect_,
            new_pixmap
        )
        if is_hovered:
            m_w, m_h = rect_.width()*2, rect_.height()*2
            image = QtGui.QImage(
                m_w, m_h, QtGui.QImage.Format_ARGB32
            )
            image.fill(QtCore.Qt.black)
            painter = QtGui.QPainter(image)
            painter.drawPixmap(QtCore.QRect(0, 0, m_w, m_h), new_pixmap)
            painter.end()
            #
            hover_pixmap = QtGui.QPixmap(image)
            mask_pixmap = QtGui.QPixmap(image)
            mask = mask_pixmap.createMaskFromColor(QtCore.Qt.black)
            mask.scaled(
                rect_.size(),
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            c = hover_color or QtGui.QColor(255, 127, 63, 127)
            hover_pixmap.fill(QtGui.QColor(c.red(), c.green(), c.blue(), 127))
            hover_pixmap.setMask(mask)
            rect__ = QtCore.QRect(
                rect.x(), rect.y(),
                rect.width(), rect.height()
            )
            self.drawPixmap(
                rect__,
                hover_pixmap
            )
        #
        self.device()

    def _draw_image_data_by_rect_(self, rect, image_data, offset=0, text=None):
        if offset != 0:
            rect_offset = QtCore.QRect(
                rect.x() + offset, rect.y() + offset,
                rect.width() - offset, rect.height() - offset
            )
        else:
            rect_offset = rect
        #
        if image_data is not None:
            image = QtGui.QImage()
            image.loadFromData(image_data)
            if image.isNull() is False:
                # draw frame
                self._set_border_color_(QtBorderColors.Icon)
                self._set_background_color_(QtBackgroundColors.Icon)
                self.drawRect(
                    rect_offset
                )
                #
                frm_x, frm_y = rect_offset.x(), rect_offset.y()
                frm_w, frm_h = rect_offset.width(), rect_offset.height()
                img_w, img_h = image.width(), image.height()

                img_rect_x, img_rect_y, img_rect_w, img_rect_h = bsc_core.RawRectMtd.set_fit_to(
                    (frm_x, frm_y), (img_w, img_h), (frm_w, frm_h)
                )

                img_rect = QtCore.QRect(
                    img_rect_x, img_rect_y, img_rect_w, img_rect_h
                )

                new_image = image.scaled(
                    img_rect.size(),
                    QtCore.Qt.IgnoreAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )
                pixmap = QtGui.QPixmap(new_image)
                self.drawPixmap(
                    img_rect,
                    pixmap
                )
                #
                self.device()
            else:
                self._draw_image_by_rect_use_text_(
                    rect_offset, text
                )
        else:
            self._draw_image_by_rect_use_text_(
                rect_offset, text
            )

    def _draw_image_by_rect_use_text_(self, rect, text=None):

        if text is not None:
            draw_text = text[0]
        else:
            draw_text = 'N/a'

        w, h = rect.width(), rect.height()
        r = min(w, h)
        t_f_s = int(r*.5)
        #
        t_f_s = max(t_f_s, 1)
        #
        self._set_font_(
            get_font(size=t_f_s)
        )
        #
        background_color, font_color = QtRawColorMtd._get_image_draw_args_by_text_(text)
        self._set_border_color_(QtBorderColors.Icon)
        self._set_background_color_(background_color)
        self.drawRect(
            rect
        )
        self._set_font_color_(font_color)
        self.drawText(
            rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            draw_text.upper()
        )

    def _set_antialiasing_(self, boolean=True):
        self.setRenderHint(self.Antialiasing, boolean)

    def _set_loading_draw_by_rect_(self, rect, loading_index):
        self._set_border_color_(QtBackgroundColors.ItemLoading)
        self._set_background_color_(QtBackgroundColors.ItemLoading)
        # self._set_background_style_(QtCore.Qt.FDiagPattern)
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        self.drawRect(rect)
        process_frame = QtCore.QRect(
            x+8, h/2-10, w-16, 20
        )
        # self._set_border_color_(255, 255, 255)
        # self._set_background_color_(255, 255, 255, 63)
        # self.drawRoundedRect(
        #     process_frame,
        #     10, 10,
        #     QtCore.Qt.AbsoluteSize
        # )
        #
        self._set_font_(Font.LOADING)
        self._set_border_color_(QtFontColors.Basic)
        self.drawText(
            process_frame,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            'loading .{}'.format('.'*(loading_index % 3))
        )

    def _set_exr_image_draw_by_rect_(self, rect, file_path, offset=0):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        #
        thumbnail_file_path = bsc_core.ImgFileOpt(file_path).get_thumbnail()
        rect_size = rect.size()
        image = QtGui.QImage(thumbnail_file_path)
        new_image = image.scaled(
            rect_size,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        pixmap = QtGui.QPixmap(new_image)
        self.drawPixmap(
            rect_,
            pixmap
        )
        #
        self.device()

    def _set_mov_image_draw_by_rect_(self, rect, file_path, offset=0):
        rect_ = QtCore.QRect(
            rect.x() + offset, rect.y() + offset,
            rect.width() - offset, rect.height() - offset
        )
        #
        thumbnail_file_path = bsc_core.VdoFileOpt(file_path).get_thumbnail()
        rect_size = rect.size()
        image = QtGui.QImage(thumbnail_file_path)
        new_image = image.scaled(
            rect_size,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        pixmap = QtGui.QPixmap(new_image)
        self.drawPixmap(
            rect_,
            pixmap
        )
        #
        self.device()

    def _set_movie_play_button_draw_by_rect_(self, rect, scale=1.0, offset=0, border_width=4, is_hovered=False, is_selected=False, is_actioned=False):
        if offset != 0:
            rect_ = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_ = rect
        #
        self._set_antialiasing_()
        #
        x, y = rect_.x(), rect_.y()
        width = rect_.width()
        height = rect_.height()
        #
        r_ = height*scale
        x_, y_ = (width - r_)/2 + x, (height - r_)/2 + y
        #
        ellipse_rect = QtCore.QRect(x_-4, y_-4, r_+8, r_+8)
        points = [
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x_, y_), radius=r_, angle=90),
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x_, y_), radius=r_, angle=210),
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x_, y_), radius=r_, angle=330),
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x_, y_), radius=r_, angle=90)
        ]
        #
        self._set_background_color_(QtBackgroundColors.Transparent)
        border_color = self._get_item_border_color_(ellipse_rect, is_hovered, is_selected, is_actioned)
        self._set_border_color_(border_color)
        self._set_border_color_alpha_(127)
        #
        self._set_border_width_(border_width)
        self.drawEllipse(ellipse_rect)
        self._draw_path_by_coords_(points)

    def _draw_path_by_coords_(self, points):
        path = QtPainterPath()
        path._set_points_add_(points)
        self._set_antialiasing_(False)
        self.drawPath(path)
        return path

    def _set_color_icon_draw_(self, rect, color, offset=0):
        r, g, b = color
        border_color = QtBorderColors.Icon
        self._set_border_width_(1)
        self._set_border_color_(border_color)
        self._set_background_color_(r, g, b, 255)
        #
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )

        self.drawRect(rect_)

    def _draw_icon_use_text_by_rect_(self, rect, text, border_color=None, background_color=None, font_color=None, offset=0, border_radius=0, border_width=1, is_hovered=False, is_enable=True):
        if offset != 0:
            rect_offset = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_offset = rect
        #
        x, y = rect_offset.x(), rect_offset.y()
        w, h = rect_offset.width(), rect_offset.height()
        #
        frame_rect = QtCore.QRect(
            x, y,
            w, h
        )
        if border_color is not None:
            border_color_ = border_color
        else:
            border_color_ = QtBorderColors.Icon
        #
        if background_color is not None:
            background_color__ = Color._get_rgba_(background_color)
        else:
            background_color__ = bsc_core.RawTextOpt(text).to_rgb_0(s_p=50, v_p=50)

        background_color_, text_color_ = QtRawColorMtd._get_image_draw_args_by_color_(*background_color__)
        if font_color is not None:
            text_color_ = font_color
        #
        self._set_background_color_(background_color_)
        self._set_border_color_(border_color_)
        self._set_border_width_(border_width)
        #
        b_ = border_width/2
        if border_radius > 0:
            self._set_antialiasing_(True)
            self.drawRoundedRect(
                frame_rect,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
            if is_hovered is True:
                self._set_background_color_(
                    255, 127, 63, 63
                )
                self.drawRoundedRect(
                    frame_rect,
                    border_radius, border_radius,
                    QtCore.Qt.AbsoluteSize
                )
        elif border_radius == -1:
            self._set_antialiasing_(True)
            border_radius = frame_rect.height()/2
            border_radius_ = b_+border_radius
            self.drawRoundedRect(
                frame_rect,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
            if is_hovered is True:
                self._set_background_color_(
                    255, 127, 63, 63
                )
                self.drawRoundedRect(
                    frame_rect,
                    border_radius_, border_radius_,
                    QtCore.Qt.AbsoluteSize
                )
        else:
            self._set_antialiasing_(False)
            self.drawRect(frame_rect)
            if is_hovered is True:
                self._set_background_color_(
                    255, 127, 63, 63
                )
                self.drawRect(frame_rect)
        #
        r = min(w, h)
        t_f_s = int(r*.675)
        #
        t_f_s = max(t_f_s, 1)
        #
        txt_rect = QtCore.QRect(
            x, y,
            w, h
        )
        self._set_font_(
            get_font(size=t_f_s)
        )
        self._set_font_color_(text_color_)
        self.drawText(
            txt_rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            text[0].capitalize()
        )

    def set_image_draw_highlight(self, rect, file_path, color=None):
        pixmap = QtGui.QPixmap(file_path)
        mask_bitmap = QtGui.QBitmap(file_path)
        mask = mask_bitmap.createHeuristicMask()
        pixmap.fill(color)
        pixmap.setMask(mask)
        #
        self.drawPixmap(
            rect, pixmap
        )

    def _draw_frame_by_rect_(self, rect, border_color, background_color, background_style=None, offset=0, border_radius=0, border_width=1):
        self._set_border_color_(border_color)
        self._set_background_color_(background_color)
        self._set_border_width_(border_width)
        if background_style is not None:
            self._set_background_style_(background_style)
        #
        b_ = border_width/2
        if offset != 0:
            offset_ = b_+offset
            rect_ = QtCore.QRect(
                rect.x()+offset_, rect.y()+offset_,
                rect.width()-offset_, rect.height()-offset_
            )
        else:
            rect_ = rect
        #
        if border_radius > 0:
            border_radius_ = b_+border_radius
            self._set_antialiasing_()
            self.drawRoundedRect(
                rect_,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        elif border_radius == -1:
            border_radius = rect_.height()/2
            border_radius_ = b_+border_radius
            self._set_antialiasing_()
            self.drawRoundedRect(
                rect_,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self._set_antialiasing_(False)
            self.drawRect(rect_)

    def _draw_focus_frame_by_rect_(self, rect, border_color=None, background_color=None, border_width=1, offset=0):
        if background_color is None:
            background_color = 0, 0, 0, 0
        if border_color is None:
            border_color = 63, 255, 127, 255
        #
        self._set_background_color_(background_color)
        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        #
        l_ = 32
        p1, p2, p3, p4 = rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = (p1.x(), p1.y()), (p2.x(), p2.y()), (p3.x(), p3.y()), (p4.x(), p4.y())
        point_coords = (
            ((x1, y1+l_), (x1, y1), (x1+l_, y1)),
            ((x2-l_, y2), (x2, y2), (x2, y2+l_)),
            ((x3, y3-l_), (x3, y3), (x3-l_, y3)),
            ((x4+l_, y4), (x4, y4), (x4, y4-l_))
        )
        [self._draw_path_by_coords_(i) for i in point_coords]

    def _draw_line_by_rect_(self, rect, border_color, background_color, border_width=1):
        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        self._set_background_color_(background_color)
        #
        line = QtCore.QLine(
            rect.topLeft(), rect.bottomLeft()
        )
        self.drawLine(line)

    def _draw_line_by_points_(self, point_0, point_1, border_color, border_width=1):
        self._set_antialiasing_(False)
        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        self._set_background_color_(QtBackgroundColors.Transparent)
        #
        line = QtCore.QLine(
            point_0, point_1
        )
        self.drawLine(line)

    def _set_status_draw_by_rect_(self, rect, color, offset=0, border_radius=0):
        self._set_border_color_(QtBackgroundColors.Transparent)
        #
        if offset != 0:
            rect_ = QtCore.QRect(
                rect.x() + offset, rect.y() + offset,
                rect.width() - offset, rect.height() - offset
            )
        else:
            rect_ = rect
        #
        gradient_color = QtGui.QLinearGradient(rect_.topLeft(), rect_.bottomLeft())
        gradient_color.setColorAt(0, self._get_qt_color_(color))
        gradient_color.setColorAt(.5, QtBackgroundColors.Transparent)
        self._set_background_color_(gradient_color)
        #
        if border_radius > 0:
            self.drawRoundedRect(
                rect_,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self.drawRect(rect_)

    def _draw_process_statuses_by_rect_(self, rect, colors, offset=0, border_radius=0):
        if colors:
            if offset != 0:
                rect_offset = QtCore.QRect(
                    rect.x() + offset, rect.y() + offset,
                    rect.width() - offset, rect.height() - offset
                )
            else:
                rect_offset = rect
            #
            self._set_background_color_(31, 31, 31, 255)
            self.drawRect(rect_offset)
            #
            gradient_color = QtGui.QLinearGradient(rect_offset.topLeft(), rect_offset.topRight())
            c = len(colors)
            p = 1/float(c)
            for seq, i_color in enumerate(colors):
                _ = float(seq) / float(c)
                i_index = max(min(_, 1), 0)
                i_qt_color = self._get_qt_color_(i_color)
                gradient_color.setColorAt(i_index, i_qt_color)
                gradient_color.setColorAt(i_index+p*.9, i_qt_color)
            #
            self._set_background_color_(gradient_color)
            #
            if border_radius > 0:
                self.drawRoundedRect(
                    rect_offset,
                    border_radius, border_radius,
                    QtCore.Qt.AbsoluteSize
                )
            else:
                self.drawRect(rect_offset)
    @classmethod
    def _get_alternating_color_(cls, rect, colors, width, time_offset=0, running=False):
        if running is True:
            x_o = (time_offset % (width*2))
        else:
            x_o = 0
        x, y = rect.x(), rect.y()
        gradient_color = QtGui.QLinearGradient(
            QtCore.QPoint(x+x_o, y), QtCore.QPoint(x+width+x_o, y+width)
        )
        gradient_color.setSpread(gradient_color.RepeatSpread)
        c = len(colors)
        p = 1/float(c)
        for seq, i_color in enumerate(colors):
            _ = float(seq)/float(c)
            i_index = max(min(_, 1), 0)
            i_qt_color = cls._get_qt_color_(i_color)
            gradient_color.setColorAt(i_index, i_qt_color)
            gradient_color.setColorAt(i_index+p*.9, i_qt_color)
        return gradient_color

    def _draw_alternating_frame_by_rect_(self, rect, colors, border_radius=0):
        rect_offset = rect
        background_color = self._get_alternating_color_(
            rect, colors, 20
        )
        self._set_background_color_(background_color)
        if border_radius > 0:
            self._set_antialiasing_()
            self.drawRoundedRect(
                rect_offset,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
        elif border_radius == -1:
            border_radius = rect_offset.height()/2
            self._set_antialiasing_()
            self.drawRoundedRect(
                rect_offset,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self._set_antialiasing_(False)
            self.drawRect(rect_offset)

    def _draw_alternating_colors_by_rect_(self, rect, colors, offset=0, border_radius=0, border_width=1, running=False):
        if offset != 0:
            rect_offset = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_offset = rect
        #
        background_color = self._get_alternating_color_(
            rect_offset, colors, 20, int(time.time()*10), running
        )
        #
        self._set_background_color_(background_color)
        if border_radius > 0:
            self._set_antialiasing_()
            self.drawRoundedRect(
                rect_offset,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
        elif border_radius == -1:
            border_radius = rect_offset.height()/2
            self._set_antialiasing_()
            self.drawRoundedRect(
                rect_offset,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self._set_antialiasing_(False)
            self.drawRect(rect_offset)

    def _draw_text_by_rect_(self, rect, text, font_color=None, font=None, offset=0, text_option=None, word_warp=False, is_hovered=False, is_selected=False):
        if font_color is not None:
            self._set_border_color_(font_color)
        else:
            self._set_border_color_(QtFontColors.Basic)
        #
        if is_hovered is True or is_selected is True:
            self._set_border_color_(QtFontColors.Hovered)
        #
        if offset != 0:
            rect_offset = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_offset = rect
        #
        if text_option is not None:
            text_option_ = text_option
        else:
            text_option_ = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        #
        if font is not None:
            self._set_font_(font)
        else:
            self._set_font_(get_font())
        #
        text_option__ = QtGui.QTextOption(
            text_option_
        )
        if word_warp is True:
            text_ = text
            text_option__.setWrapMode(
                text_option__.WrapAtWordBoundaryOrAnywhere
            )
        else:
            text_option__.setUseDesignMetrics(True)
            #
            text_ = self.fontMetrics().elidedText(
                text,
                QtCore.Qt.ElideLeft,
                rect_offset.width(),
                QtCore.Qt.TextShowMnemonic
            )
        #
        rect_f_ = QtCore.QRectF(
            rect_offset.x(), rect_offset.y(),
            rect_offset.width(), rect_offset.height()
        )
        self.drawText(
            rect_f_,
            text_,
            text_option__,
        )

    def _set_text_draw_by_rect_use_dict_(self, rect, text_dict, text_size, text_weight, font_color):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        self._set_font_option_(text_size, text_weight)
        ss = [self.fontMetrics().width(i) for i in text_dict.keys()]
        text_height = int(text_size*1.5)
        text_spacing = int(text_size*.2)
        t_w = max(ss)+text_size/2
        for seq, (k, v) in enumerate(text_dict.items()):
            i_rect = QtCore.QRect(x, y+seq*(text_height+text_spacing), w, text_height)
            self._set_text_draw_by_rect_use_key_value_(
                rect=i_rect,
                key_text=k,
                value_text=v,
                key_text_width=t_w,
                key_text_size=text_size, value_text_size=text_size,
                key_text_weight=text_weight, value_text_weight=text_weight,
                key_text_color=font_color, value_text_color=font_color,
            )

    def _set_radar_chart_draw_by_rect_(self, rect, chart_data):
        pass

    def _set_text_draw_by_rect_use_key_value_(self, rect, key_text, value_text, key_text_width, key_text_size=8, value_text_size=8, key_text_weight=50, value_text_weight=50, key_text_color=None, value_text_color=None, offset=0, is_hovered=False, is_selected=False):
        x, y = rect.x()+offset, rect.y()+offset
        w, h = rect.width()-offset, rect.height()-offset
        if w > 0 and h > 0:
            if key_text_color is not None:
                key_color_ = key_text_color
            else:
                key_color_ = QtFontColors.KeyBasic
            #
            if value_text_color is not None:
                value_color_ = value_text_color
            else:
                value_color_ = QtFontColors.ValueBasic
            #
            # if is_hovered is True or is_selected is True:
            #     key_color_ = QtFontColors.KeyHovered
            #     value_color_ = QtFontColors.ValueHovered
            #
            sep_text = ':'
            sep_text_width = key_text_size
            # key
            self._set_font_color_(key_color_)
            key_text_rect = QtCore.QRect(
                x, y, key_text_width, h
            )
            key_text_option = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            key_text_font = Font.NameTextKey
            key_text_font.setPointSize(key_text_size)
            key_text_font.setWeight(key_text_weight)
            self._set_font_(key_text_font)
            self.drawText(
                key_text_rect,
                key_text_option,
                key_text,
            )
            # sep
            sep_text_rect = QtCore.QRect(
                x+key_text_width, y, sep_text_width, h
            )
            sep_text_option = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
            self.drawText(
                sep_text_rect,
                sep_text_option,
                sep_text,
            )
            # value
            self._set_font_color_(value_color_)
            value_text_rect_f = QtCore.QRectF(
                x+key_text_width+sep_text_width, y, w-sep_text_width-key_text_width, h
            )
            qt_value_text_option = QtGui.QTextOption()
            qt_value_text_option.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            qt_value_text_option.setUseDesignMetrics(True)
            value_text_ = self.fontMetrics().elidedText(
                value_text,
                QtCore.Qt.ElideLeft,
                value_text_rect_f.width(),
                QtCore.Qt.TextShowMnemonic
            )
            value_text_font = Font.NameTextValue
            value_text_font.setPointSize(value_text_size)
            value_text_font.setWeight(value_text_weight)
            self._set_font_(value_text_font)
            self.drawText(
                value_text_rect_f,
                value_text_,
                qt_value_text_option,
            )

    def set_button_draw(self, rect, background_color, border_color, border_radius=4, border_width=1, border_style='solid'):
        self._set_background_color_(background_color)
        self._set_border_color_(border_color)
        #
        p0, p1, p2, p3 = rect.topLeft(), rect.bottomLeft(), rect.bottomRight(), rect.topRight()
        w, h = rect.width(), rect.height()
        cx, cy = p0.x()+w / 2, p0.y()+h / 2
        #
        angles = []
        for p in [p0, p1, p2, p3]:
            a = self.mtd_raw_position_2d.toAngle(
                position0=(p.x(), p.y()),
                position1=(cx, cy)
            )
            angles.append(a)
        #
        br, bb, bg, ba = border_color.red(), border_color.green(), border_color.blue(), border_color.alpha()
        br0, bb0, bg0, ba0 = min(br * 1.25, 255), min(bb * 1.25, 255), min(bg * 1.25, 255), ba
        br1, bb1, bg1, ba1 = min(br * 1.5, 255), min(bb * 1.5, 255), min(bg * 1.5, 255), ba
        br3, bb3, bg3, ba3 = min(br * .875, 255), min(bb * .875, 255), min(bg * .875, 255), ba
        br4, bb4, bg4, ba4 = min(br * .725, 255), min(bb * .725, 255), min(bg * .725, 255), ba
        self.setBorderRgba((0, 0, 0, 0))
        if border_style == 'solid':
            self._set_border_color_(border_color)
            self.drawRoundedRect(
                rect,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
        else:
            if border_style == 'outset':
                a = 90
            elif border_style == 'inset':
                a = -90
            else:
                a = 90
            color = QtGui.QConicalGradient(cx, cy, a)
            color.setColorAt(0, QtGui.QColor(br0, bb0, bg0, ba0))
            for seq, a in enumerate(angles):
                p = float(a) / float(360)
                if seq == 0:
                    color.setColorAt(p, QtGui.QColor(br1, bb1, bg1, ba1))
                elif seq == 1:
                    color.setColorAt(p-.0125, QtGui.QColor(br1, bb1, bg1, ba1))
                    color.setColorAt(p, QtGui.QColor(br4, bb4, bg4, ba4))
                elif seq == 2:
                    color.setColorAt(p, QtGui.QColor(br4, bb4, bg4, ba4))
                elif seq == 3:
                    color.setColorAt(p-.0125, QtGui.QColor(br3, bb3, bg3, ba3))
                    color.setColorAt(p, QtGui.QColor(br0, bb0, bg0, ba0))
            color.setColorAt(1, QtGui.QColor(br0, bb0, bg0, ba0))
            #
            brush = QtGui.QBrush(color)
            self.setBrush(brush)
            self.drawRoundedRect(rect, border_radius, border_radius, QtCore.Qt.AbsoluteSize)
        #
        rect_ = QtCore.QRect(p0.x()+border_width, p0.y()+border_width, w-border_width * 2, h-border_width * 2)
        self._set_background_color_(background_color)
        self.drawRoundedRect(
            rect_,
            border_radius-border_width, border_radius-border_width,
            QtCore.Qt.AbsoluteSize
        )
    @classmethod
    def _get_item_background_color_1_by_rect_(cls, rect, is_hovered=False, is_actioned=False):
        conditions = [is_hovered, is_actioned]
        if conditions == [False, False]:
            return QtBackgroundColors.Transparent
        elif conditions == [False, True]:
            return QtBackgroundColors.Actioned
        elif conditions == [True, False]:
            return QtBackgroundColors.Hovered
        elif conditions == [True, True]:
            color_0 = QtBackgroundColors.Hovered
            color_1 = QtBackgroundColors.Actioned
            start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
            color = QtGui.QLinearGradient(start_pos, end_pos)
            color.setColorAt(0, color_0)
            color.setColorAt(1, color_1)
            return color
    @classmethod
    def _get_item_background_color_by_rect_(cls, rect, is_hovered=False, is_selected=False, is_actioned=False, default_background_color=None):
        conditions = [is_hovered, is_selected]
        if conditions == [False, False]:
            if default_background_color is not None:
                return default_background_color
            return QtBackgroundColors.Transparent
        elif conditions == [False, True]:
            return QtBackgroundColors.Selected
        elif conditions == [True, False]:
            if is_actioned:
                color_0 = QtBackgroundColors.Hovered
                color_1 = QtBackgroundColors.Actioned
                start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
                color = QtGui.QLinearGradient(start_pos, end_pos)
                color.setColorAt(0, color_0)
                color.setColorAt(1, color_1)
                return color
            return QtBackgroundColors.Hovered
        elif conditions == [True, True]:
            color_0 = QtBackgroundColors.Hovered
            if is_actioned:
                color_1 = QtBackgroundColors.Actioned
            else:
                color_1 = QtBackgroundColors.Selected
            #
            start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
            color = QtGui.QLinearGradient(start_pos, end_pos)
            color.setColorAt(0, color_0)
            color.setColorAt(1, color_1)
            return color
    @classmethod
    def _get_frame_background_color_by_rect_(cls, rect, check_is_hovered=False, is_checked=False, press_is_hovered=False, is_pressed=False, is_selected=False, delete_is_hovered=False):
        conditions = [check_is_hovered, is_checked, press_is_hovered, is_pressed, is_selected]
        if True not in conditions:
            return QtBackgroundColors.Transparent
        #
        start_pos, end_pos = rect.topLeft(), rect.bottomRight()
        color = QtGui.QLinearGradient(start_pos, end_pos)
        #
        check_index = 0
        select_index = .5
        press_index = 1
        check_conditions = [check_is_hovered, is_checked]
        check_args = []
        if check_conditions == [True, True]:
            check_args = [
                (check_index, QtBackgroundColors.CheckHovered),
                (.25, QtBackgroundColors.Checked)
            ]
        elif check_conditions == [True, False]:
            check_args = [
                (check_index, QtBackgroundColors.CheckHovered)
            ]
        elif check_conditions == [False, True]:
            check_args = [
                (check_index, QtBackgroundColors.Checked)
            ]
        #
        if True in check_args:
            pass
        #
        if is_selected is True:
            select_args = [
                (select_index, QtBackgroundColors.Selected)
            ]
        else:
            select_args = []
        #
        if delete_is_hovered is True:
            press_index = .75
        #
        press_conditions = [press_is_hovered, is_pressed]
        press_args = []
        if press_conditions == [True, True]:
            press_args = [
                (select_index, QtBackgroundColors.Pressed),
                (press_index, QtBackgroundColors.PressedHovered),
            ]
        elif press_conditions == [True, False]:
            press_args = [
                (press_index, QtBackgroundColors.PressedHovered),
            ]
        elif press_conditions == [False, True]:
            press_args = [
                (press_index, QtBackgroundColors.Pressed),
            ]
        #
        delete_args = []
        if delete_is_hovered is True:
            delete_args = [
                (1, QtBackgroundColors.DeleteHovered)
            ]
        #
        for i_args in check_args+select_args+press_args+delete_args:
            i_index, i_color = i_args
            color.setColorAt(i_index, i_color)
        return color
    @classmethod
    def _get_item_border_color_(cls, rect, is_hovered=False, is_selected=False, is_actioned=False):
        if is_actioned:
            return QtBackgroundColors.Actioned
        if is_hovered:
            return QtBackgroundColors.Hovered
        elif is_selected:
            return QtBackgroundColors.Selected
        return QtBackgroundColors.White

    def _set_sector_chart_draw_(self, chart_draw_data, background_color, border_color, hover_point):
        if chart_draw_data is not None:
            basic_data = chart_draw_data['basic']
            for i in basic_data:
                (
                    i_background_rgba, i_border_rgba,
                    i_total_path, i_occupy_path,
                    i_text_point, i_text_line, i_text_ellipse, i_text_size, i_text
                ) = i
                #
                self._set_background_color_(background_color)
                self._set_border_color_(border_color)
                self._set_background_style_(QtCore.Qt.FDiagPattern)
                self.drawPath(i_total_path)
                #
                i_r, i_g, i_b, i_a = i_background_rgba
                self._set_background_color_(
                    [(i_r, i_g, i_b, 96), (i_r, i_g, i_b, 255)][i_total_path.contains(hover_point) or i_text_ellipse.contains(hover_point)]
                )
                self._set_border_color_(i_border_rgba)
                self.drawPath(i_occupy_path)
                #
                self.drawPolyline(i_text_line)
                self.drawEllipse(i_text_ellipse)
                #
                self._set_font_(
                    get_font()
                )
                #
                self.drawText(i_text_point, i_text)

    def _set_histogram_draw_(self, rect, value_array, value_scale, value_offset, label, grid_scale, grid_size, grid_offset, translate, current_index, mode):
        maximum = max(value_array)
        spacing = 2
        if maximum:
            pos_x, pos_y = rect.x(), rect.y()
            width, height = rect.width(), rect.height()
            value_offset_x, value_offset_y = value_offset
            #
            label_x, label_y = label
            #
            grid_scale_x, grid_scale_y = grid_scale
            grid_offset_x, grid_offset_y = grid_offset
            translate_x, translate_y = translate
            value_scale_x, value_scale_y = value_scale
            #
            grid_w, grid_h = grid_size
            column_w = grid_w / grid_scale_x
            #
            minimum_h = grid_w / grid_scale_y
            #
            current_x, current_y = None, None
            for i_index, i_value in enumerate(value_array):
                i_color_percent = float(i_value) / float(maximum)
                #
                i_r, i_g, i_b = bsc_core.RawColorMtd.hsv2rgb(140 * i_color_percent, 1, 1)
                #
                self._set_background_color_(i_r, i_g, i_b, 255)
                self._set_border_color_(i_r, i_g, i_b, 255)
                #
                i_value_percent = float(i_value) / float(value_scale_y)
                i_pos_x = pos_x + column_w * i_index + grid_offset_x + translate_x + 1
                i_pos_y = (height - minimum_h * i_value_percent * grid_scale_y - grid_offset_y + translate_y)
                # filter visible
                if grid_offset_x <= i_pos_x <= width:
                    i_w, i_h = column_w - spacing, (minimum_h * i_value_percent) * grid_scale_y
                    i_rect = QtCore.QRect(
                        i_pos_x, i_pos_y,
                        i_w, i_h
                    )
                    self.drawRect(i_rect)
                    #
                    if i_index == current_index:
                        current_x = i_index + value_offset_x
                        current_y = i_value + value_offset_y
                        #
                        self._set_background_color_(0, 0, 0, 0)
                        self._set_border_color_(223, 223, 223, 255)
                        #
                        selection_rect = QtCore.QRect(
                            i_pos_x, 0,
                            column_w - 2, height - grid_offset_y
                        )
                        #
                        self.drawRect(selection_rect)
            #
            if current_x is not None and current_y is not None:
                current_label_rect = QtCore.QRect(
                    grid_offset_x + 8, 0 + 8,
                    width, height
                )
                #
                self._set_border_color_(223, 223, 223, 255)
                self._set_font_(get_font(size=12, weight=75))
                #
                self.drawText(
                    current_label_rect,
                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                    '{2} ( {0} )\r\n{3} ( {1} )'.format(
                        label_x, label_y,
                        current_x,
                        bsc_core.RawIntegerMtd.get_prettify_(current_y, mode=mode)
                    )
                )

    def _set_grid_draw_(self, rect, axis_dir, grid_size, grid_scale, translate, grid_offset, border_color):
        def set_branch_draw_fnc_(lines, axis_index, scale):
            for seq, line_points in enumerate(lines):
                # if (seq - axis_index)/scale % 10 == 0:
                #     self._set_border_width_(2)
                # else:
                #     self._set_border_width_(1)
                self.drawLine(*line_points)
        #
        def get_lines_h_fnc_():
            lis = []
            for i_y in range(height / grid_h):
                pox_x_1, pox_x_2 = grid_offset_x, width
                #
                if axis_dir_y == -1:
                    pos_y_1 = pos_y_2 = height-grid_h*(i_y-index_y)-translate_y+grid_offset_y
                else:
                    pos_y_1 = pos_y_2 = grid_h*(i_y-index_y)+translate_y+grid_offset_y
                #
                lis.append(
                    (QtCore.QPointF(pox_x_1, pos_y_1), QtCore.QPointF(pox_x_2, pos_y_2))
                )
            return lis
        #
        def get_lines_v_fnc_():
            lis = []
            for i_x in range(width / grid_h):
                if axis_dir_x == -1:
                    pox_x_1 = pox_x_2 = width-grid_w*(i_x-index_x)-translate_x+grid_offset_x
                else:
                    pox_x_1 = pox_x_2 = grid_w*(i_x-index_x)+translate_x+grid_offset_x
                #
                pos_y_1, pos_y_2 = height, grid_offset_y
                #
                lis.append(
                    (QtCore.QPointF(pox_x_1, pos_y_1), QtCore.QPointF(pox_x_2, pos_y_2))
                )
            return lis
        #
        width, height = rect.width(), rect.height()
        grid_w, grid_h = grid_size
        grid_scale_x, grid_scale_y = grid_scale
        axis_dir_x, axis_dir_y = axis_dir
        #
        translate_x, translate_y = translate
        grid_offset_x, grid_offset_y = grid_offset
        index_x = translate_x/grid_w
        index_y = translate_y/grid_w
        #
        lines_h, lines_v = get_lines_h_fnc_(), get_lines_v_fnc_()
        #
        self._set_background_color_(0, 0, 0, 0)
        self._set_border_color_(border_color)
        #
        set_branch_draw_fnc_(lines_h, index_y, grid_scale_y)
        set_branch_draw_fnc_(lines_v, index_x, grid_scale_x)

    def _set_grid_mark_draw_(self, rect, axis_dir, grid_size, translate, grid_offset, grid_scale, grid_value_offset, grid_border_color, grid_value_show_mode):
        def set_branch_draw_fnc_(points, axis_index, scale, value_offset):
            for seq, i_point in enumerate(points):
                if (seq - axis_index) % 5 == 0:
                    value = (seq - axis_index)/scale+value_offset
                    text = bsc_core.RawIntegerMtd.get_prettify_(
                        value,
                        grid_value_show_mode
                    )
                    self.drawText(
                        i_point, text
                    )
        #
        def get_h_points():
            lis = []
            for i_x in range(width/grid_w):
                if axis_dir_x == -1:
                    i_p_x = width-grid_w*(i_x-index_x)-translate_x+grid_offset_x
                else:
                    i_p_x = grid_w*(i_x-index_x)+translate_x+grid_offset_x
                #
                if axis_dir_y == -1:
                    i_p_y = height
                else:
                    i_p_y = text_h
                #
                lis.append(
                    QtCore.QPointF(i_p_x, i_p_y)
                )
            #
            return lis
        #
        def get_v_points():
            lis = []
            for i_y in range(height/grid_h):
                if axis_dir_x == -1:
                    i_p_x = width-text_h
                else:
                    i_p_x = 0
                #
                if axis_dir_y == -1:
                    i_p_y = height-grid_h*(i_y-index_y)-translate_y+grid_offset_y
                else:
                    i_p_y = grid_h*(i_y-index_y)+translate_y+grid_offset_y
                #
                lis.append(
                    QtCore.QPointF(i_p_x, i_p_y)
                )
            #
            return lis
        #
        width, height = rect.width(), rect.height()
        grid_w, grid_h = grid_size
        #
        axis_dir_x, axis_dir_y = axis_dir
        translate_x, translate_y = translate
        grid_offset_x, grid_offset_y = grid_offset
        value_scale_x, value_scale_y = grid_scale
        value_offset_x, value_offset_y = grid_value_offset
        index_x = translate_x/grid_w
        index_y = translate_y/grid_h
        #
        self._set_border_color_(grid_border_color)
        self._set_font_(get_font(size=6))
        text_h = self.fontMetrics().height()
        points_h, points_v = get_h_points(), get_v_points()
        #
        set_branch_draw_fnc_(
            points_h, index_x, value_scale_x, value_offset_x
        )
        set_branch_draw_fnc_(
            points_v, index_y, value_scale_y, value_offset_y
        )

    def _set_grid_axis_draw_(self, rect, axis_dir, translate, grid_offset, grid_axis_lock, grid_border_colors):
        width, height = rect.width(), rect.height()
        axis_dir_x, axis_dir_y = axis_dir
        #
        translate_x, translate_y = translate
        grid_offset_x, grid_offset_y = grid_offset
        grid_axis_lock_x, grid_axis_lock_y = grid_axis_lock
        if grid_axis_lock_y:
            if axis_dir_y == -1:
                h_y_0 = height-grid_offset_y-1
            else:
                h_y_0 = 0
        else:
            h_y_0 = height-grid_offset_y-translate_y-1
        #
        points_h = (
            QtCore.QPointF(grid_offset_x, h_y_0),
            QtCore.QPointF(width, h_y_0)
        )
        #
        if grid_axis_lock_x:
            v_x_0 = 0+grid_offset_x
        else:
            v_x_0 = grid_offset_x+translate_x
        #
        points_v = (
            QtCore.QPointF(v_x_0, -grid_offset_y),
            QtCore.QPointF(v_x_0, height-grid_offset_y))

        #
        border_color_x, border_color_y = grid_border_colors
        self._set_background_color_(0, 0, 0, 0)
        self._set_border_color_(border_color_x)
        self.drawLine(points_h[0], points_h[1])
        #
        self._set_border_color_(border_color_y)
        self.drawLine(points_v[0], points_v[1])

    def _set_dotted_frame_draw_(self, rect, border_color, background_color, border_width=2):
        self._set_background_color_(background_color)
        self._set_border_color_(border_color)
        self._set_border_width_(2)
        self._set_border_style_(QtCore.Qt.DashLine)
        #
        self.drawRect(rect)

    def _set_node_frame_draw_by_rect_(self, rect, offset=0, border_radius=0, border_width=1, is_hovered=False, is_selected=False, is_actioned=False):
        conditions = [is_hovered, is_selected]
        if conditions == [False, False]:
            color = QtBorderColors.Transparent
        elif conditions == [True, False]:
            color = QtBorderColors.Hovered
        elif conditions == [False, True]:
            color = QtBorderColors.Selected
        elif conditions == [True, True]:
            color_0 = QtBackgroundColors.Hovered
            if is_actioned:
                color_1 = QtBackgroundColors.Actioned
            else:
                color_1 = QtBackgroundColors.Selected
            #
            start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
            color = QtGui.QLinearGradient(start_pos, end_pos)
            color.setColorAt(0, color_0)
            color.setColorAt(1, color_1)
        else:
            raise RuntimeError()

        brush = QtGui.QBrush(color)
        pen = QtGui.QPen(brush, border_width)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.setPen(pen)
        self.setBrush(QtGui.QBrush(QtBorderColors.Transparent))

        b_ = border_width / 2
        if offset != 0:
            offset_ = b_ + offset
            rect_ = QtCore.QRect(
                rect.x() + offset_, rect.y() + offset_,
                rect.width() - offset_, rect.height() - offset_
            )
        else:
            rect_ = rect
        #
        if border_radius > 0:
            border_radius_ = b_ + border_radius
            self.drawRoundedRect(
                rect_,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        elif border_radius == -1:
            border_radius = rect_.height() / 2
            border_radius_ = b_ + border_radius
            self.drawRoundedRect(
                rect_,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self.drawRect(rect_)

    def _set_screenshot_draw_by_rect_(self, rect_0, rect_1, border_color, background_color):
        rect_f_0 = QtCore.QRectF(
            rect_0.x(), rect_0.y(), rect_0.width(), rect_0.height()
        )
        path_0 = QtGui.QPainterPath()
        path_0.addRect(rect_f_0)

        rect_f_1 = QtCore.QRectF(
            rect_1.x(), rect_1.y(), rect_1.width(), rect_1.height()
        )
        path_1 = QtGui.QPainterPath()
        path_1.addRect(rect_f_1)

        path_2 = path_0-path_1

        self._set_background_color_(background_color)
        self._set_border_color_(border_color)
        self._set_border_width_(2)
        self._set_border_style_(QtCore.Qt.DashLine)
        #
        self.drawPath(path_2)


class QtNGPainter(QtPainter):
    def __init__(self, *args, **kwargs):
        super(QtNGPainter, self).__init__(*args, **kwargs)
    @classmethod
    def _get_ng_node_background_color_(cls, rect, is_hovered=False, is_selected=False, is_actioned=False):
        conditions = [is_hovered, is_selected]
        a = 255
        color_hovered = QtGui.QColor(255, 127, 63, a)
        color_selected = QtGui.QColor(63, 127, 255, a)
        color_actioned = QtGui.QColor(63, 255, 127, a)
        color = QtGui.QColor(191, 191, 191, a)
        if conditions == [False, False]:
            return color
        elif conditions == [False, True]:
            return color_selected
        elif conditions == [True, False]:
            if is_actioned:
                color_0 = color_hovered
                color_1 = color_actioned
                start_coord, end_coord = rect.topLeft(), rect.bottomLeft()
                l_color = QtGui.QLinearGradient(start_coord, end_coord)
                l_color.setColorAt(0, color_0)
                l_color.setColorAt(1, color_1)
                return l_color
            return color_hovered
        elif conditions == [True, True]:
            color_0 = color_hovered
            if is_actioned:
                color_1 = color_actioned
            else:
                color_1 = color_selected
            #
            start_coord, end_coord = rect.topLeft(), rect.bottomLeft()
            l_color = QtGui.QLinearGradient(start_coord, end_coord)
            l_color.setColorAt(0, color_0)
            l_color.setColorAt(1, color_1)
            return l_color

    def _set_ng_node_input_draw_(self, rect, border_width, offset):
        self._set_border_color_(191, 191, 191, 255)
        self._set_border_width_(border_width)
        self._set_background_color_(63, 255, 127, 255)
        #
        b_ = border_width / 2
        if offset != 0:
            offset_ = b_ + offset
            rect_ = QtCore.QRect(
                rect.x() + offset_, rect.y() + offset_,
                rect.width() - offset_, rect.height() - offset_
            )
        else:
            rect_ = rect
        #
        self.drawRect(rect_)

    def _set_ng_node_output_draw_(self, rect, border_width, offset):
        self._set_border_color_(191, 191, 191, 255)
        self._set_border_width_(border_width)
        self._set_background_color_(255, 63, 31, 255)
        #
        b_ = border_width / 2
        if offset != 0:
            offset_ = b_ + offset
            rect_ = QtCore.QRect(
                rect.x() + offset_, rect.y() + offset_,
                rect.width() - offset_, rect.height() - offset_
            )
        else:
            rect_ = rect
        #
        x, y = rect_.x(), rect_.y()
        w, h = rect_.width(), rect_.height()
        #
        r = h
        coords = [
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x, y), radius=r, angle=90),
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x, y), radius=r, angle=210),
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x, y), radius=r, angle=330),
            utl_gui_core.Ellipse2dMtd.get_coord_at_angle(start=(x, y), radius=r, angle=90)
        ]
        #
        self._draw_path_by_coords_(coords)

    def _set_ng_node_resize_button_draw_(self, rect, border_width, mode, is_current, is_hovered):
        if is_current is True:
            self._set_border_color_(127, 127, 127, 255)
        else:
            self._set_border_color_(63, 63, 63, 255)
        #
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        c = 4
        m = mode
        for i in range(4):
            if 0 < i < c:
                if i <= m:
                    self._set_border_color_(127, 127, 127, 255)
                else:
                    self._set_border_color_(63, 63, 63, 255)
                self._set_border_width_(border_width)
                self._set_background_color_(0, 0, 0, 0)
                i_p_0, i_p_1 = QtCore.QPoint(x, y+i*h/c), QtCore.QPoint(x+w, y+i*h/c)
                self.drawLine(i_p_0, i_p_1)

    def _set_ng_node_frame_head_draw_(self, rect, border_color, border_width, border_radius, is_hovered=False, is_selected=False, is_actioned=False):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        x_0, y_0 = x, y
        w_0, h_0 = w, h-border_radius-border_width
        x_1, y_1 = x, y+border_radius+border_width
        w_1, h_1 = w, h-border_radius-border_width
        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        self._set_border_join_(QtCore.Qt.MiterJoin)
        background_color = self._get_ng_node_background_color_(
            rect,
            is_hovered, is_selected, is_actioned
        )
        self._set_background_color_(background_color)
        path_0 = QtGui.QPainterPath()
        path_0.addRoundedRect(
            QtCore.QRectF(x_0, y_0, w_0, h_0),
            border_radius, border_radius, QtCore.Qt.AbsoluteSize
        )
        path_1 = QtGui.QPainterPath()
        path_1.addRect(
            QtCore.QRectF(x_1, y_1, w_1, h_1)
        )
        self.drawPath(path_0+path_1)

    def _set_ng_node_frame_body_draw_(self, rect, border_color, border_width, border_radius):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        x_0, y_0 = x, y
        w_0, h_0 = w, h - border_radius - border_width
        x_1, y_1 = x, y + border_radius + border_width
        w_1, h_1 = w, h - border_radius - border_width
        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        self._set_border_join_(QtCore.Qt.MiterJoin)
        self._set_background_color_(127, 127, 127, 63)
        path_0 = QtGui.QPainterPath()
        path_0.addRect(
            QtCore.QRectF(x_0, y_0, w_0, h_0)
        )
        path_1 = QtGui.QPainterPath()
        path_1.addRoundedRect(
            QtCore.QRectF(x_1, y_1, w_1, h_1),
            border_radius, border_radius, QtCore.Qt.AbsoluteSize
        )
        self.drawPath(path_0 + path_1)


def set_gui_proxy_set_print(gui_proxy, text):
    if hasattr(gui_proxy, 'add_content_with_thread'):
        gui_proxy.add_content_with_thread(text)


# log
def set_qt_log_result_trace(text):
    windows = get_all_lx_windows()
    if windows:
        window = windows[0]
        window_gui_proxy = window.gui_proxy
        if hasattr(window_gui_proxy, 'PRX_CATEGORY'):
            if window_gui_proxy.PRX_CATEGORY == 'tool_window':
                return set_gui_proxy_set_print(window_gui_proxy, text)


def set_qt_log_warning_trace(text):
    windows = get_all_lx_windows()
    if windows:
        window = windows[0]
        gui_proxy = window.gui_proxy
        return set_gui_proxy_set_print(gui_proxy, text)


def set_qt_log_error_trace(text):
    windows = get_all_lx_windows()
    if windows:
        window = windows[0]
        gui_proxy = window.gui_proxy
        return set_gui_proxy_set_print(gui_proxy, text)


def set_qt_log_connect_create():
    _utl_cor_utility.__dict__['QT_LOG_RESULT_TRACE_METHOD'] = set_qt_log_result_trace
    _utl_cor_utility.__dict__['QT_LOG_WARNING_TRACE_METHOD'] = set_qt_log_result_trace
    _utl_cor_utility.__dict__['QT_LOG_ERROR_TRACE_METHOD'] = set_qt_log_result_trace


def set_log_write(text):
    windows = get_all_lx_windows()
    lis = []
    for window in windows:
        if hasattr(window, 'gui_proxy'):
            window_gui_proxy = window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_CATEGORY'):
                if window_gui_proxy.PRX_CATEGORY == 'tool_window':
                    lis.append(window_gui_proxy)
    if lis:
        lis[0].set_log_write(text)


def get_all_tool_windows():
    windows = get_all_lx_windows()
    lis = []
    for window in windows:
        if hasattr(window, 'gui_proxy'):
            window_gui_proxy = window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_CATEGORY'):
                if window_gui_proxy.PRX_CATEGORY == 'tool_window':
                    lis.append(window_gui_proxy)
    return lis


def set_log_writer_connect():
    _utl_cor_utility.__dict__['LOG_WRITE_METHOD'] = set_log_write


# progress
def create_gui_progress_method(maximum, label=None):
    lis = []
    windows = get_all_lx_windows()
    for i_window in windows:
        if hasattr(i_window, 'gui_proxy'):
            window_gui_proxy = i_window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_CATEGORY'):
                if window_gui_proxy.PRX_CATEGORY in {'tool_window', 'dialog_window'}:
                    p = window_gui_proxy.set_progress_create(maximum, label=label)
                    lis.append(p)
    return lis


def set_qt_progress_connect_create():
    _utl_cor_utility.__dict__['QT_PROGRESS_CREATE_METHOD'] = create_gui_progress_method


def set_qt_layout_clear(layout):
    def rcs_fnc_(layout_):
        c = layout_.count()
        for i in range(c):
            i_item = layout_.takeAt(0)
            if i_item is not None:
                i_widget = i_item.widget()
                if i_widget:
                    i_widget.deleteLater()
                else:
                    _i_layout = i_item.layout()
                    if _i_layout:
                        rcs_fnc_(_i_layout)
                    else:
                        spacer = i_item.spacerItem()
                        if spacer:
                            spacer.deleteLater()

    #
    rcs_fnc_(layout)


def get_lx_window_by_unique_id(unique_id):
    windows = get_all_lx_windows()
    for i_window in windows:
        if hasattr(i_window, 'gui_proxy'):
            window_gui_proxy = i_window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_CATEGORY'):
                if window_gui_proxy.get_window_unique_id() == unique_id:
                    return window_gui_proxy


def get_session_window_by_name(name):
    windows = get_all_lx_windows()
    for i_window in windows:
        if hasattr(i_window, 'gui_proxy'):
            window_gui_proxy = i_window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_TYPE'):
                if window_gui_proxy.PRX_TYPE == 'session_window':
                    if window_gui_proxy.session.get_name() == name:
                        return window_gui_proxy


class AsbQtMenuSetup(object):
    def __init__(self, *args):
        pass
    @classmethod
    def get_menu(cls, menu_title):
        raise NotImplementedError()
    @classmethod
    def get_fnc(cls, text):
        exec text
    @classmethod
    def set_action_add(cls, action_item, action_data):
        name, icon_name, method = action_data
        #
        action_item.setText(name)
        #
        icon = QtUtilMtd.get_name_text_icon_(name)
        action_item.setIcon(icon)
        if method is not None:
            if isinstance(method, (types.FunctionType, types.MethodType)):
                action_item.triggered.connect(method)
            elif isinstance(method, six.string_types):
                action_item.triggered.connect(lambda *args, **kwargs: cls.get_fnc(method))
    @classmethod
    def set_menu_setup(cls, menu, menu_raw):
        if menu_raw:
            for i in menu_raw:
                if i:
                    if len(i) > 0:
                        if isinstance(i, tuple):
                            if i:
                                name = i[0]
                                action_item = menu.addAction(name)
                                cls.set_action_add(action_item, i)
                        elif isinstance(i, list):
                            sub_name, sub_icon_name, sub_menu_data = i
                            action_item = menu.addAction(sub_name)
                            icon = QtUtilMtd.get_name_text_icon_(sub_name)
                            action_item.setIcon(icon)
                            #
                            i_menu = QtWidgets.QMenu()
                            action_item.setMenu(i_menu)
                            for j in sub_menu_data:
                                if j:
                                    if len(j) > 0:
                                        sub_name = j[0]
                                        sub_action_item = i_menu.addAction(sub_name)
                                        cls.set_action_add(sub_action_item, j)
                                    else:
                                        pass
                                else:
                                    i_menu.addSeparator()
                    else:
                        pass
                else:
                    menu.addSeparator()
    @classmethod
    def set_menu_build_by_configure(cls, configure):
        menu_raw = []
        #
        name = configure.get('option.name')
        keys = configure.get('option.tool')
        for i_key in keys:
            if isinstance(i_key, six.string_types):
                if i_key.startswith('separator'):
                    menu_raw.append(())
                else:
                    i_type = configure.get('tools.{}.type'.format(i_key))
                    i_name = configure.get('tools.{}.name'.format(i_key))
                    i_icon = configure.get('tools.{}.icon'.format(i_key))
                    i_command = configure.get('tools.{}.command'.format(i_key))
                    if i_type == 'item':
                        menu_raw.append(
                            (i_name, i_icon, i_command)
                        )
                    elif i_type == 'group':
                        i_menu_raw = []
                        i_sub_raw = [i_name, i_icon, i_menu_raw]
                        i_keys = configure.get('tools.{}.items'.format(i_key))
                        for j_key in i_keys:
                            if j_key.startswith('separator'):
                                i_menu_raw.append(())
                            else:
                                j_type = configure.get('tools.{}.type'.format(j_key))
                                j_name = configure.get('tools.{}.name'.format(j_key))
                                j_icon = configure.get('tools.{}.icon'.format(j_key))
                                j_command = configure.get('tools.{}.command'.format(j_key))
                                if j_type == 'item':
                                    i_menu_raw.append(
                                        (j_name, j_icon, j_command)
                                    )
                        #
                        menu_raw.append(i_sub_raw)
            else:
                pass
        #
        menu = cls.get_menu(name)
        if menu is not None:
            menu.clear()
            cls.set_menu_setup(menu, menu_raw)
    @classmethod
    def set_menu_build_by_menu_content(cls, menu, menu_content):
        if menu is not None:
            menu.clear()


class QtSystemTrayIcon(QtWidgets.QSystemTrayIcon):
    press_clicked = qt_signal()
    press_db_clicked = qt_signal()
    press_toggled = qt_signal(bool)

    def __init__(self, *args, **kwargs):
        super(QtSystemTrayIcon, self).__init__(*args, **kwargs)
        menu = QtWidgets.QMenu()
        self.setContextMenu(
            menu
        )
        #
        self._window = self.parent()
        self._set_quit_action_add_(menu)
        self.activated.connect(self._set_window_show_normal_)

    def _set_window_show_normal_(self, *args):
        r = args[0]
        # if r == self.Trigger:
        #     # print 'AAA'
        #     # if self._window.isVisible():
        #     #     self._window.hide()
        #     # else:
        #     #     self._window.show()
        #     if self._window.isMinimized():
        #         self._window.showNormal()
        #     else:
        #         self._window.showMinimized()
        if r == self.DoubleClick:
            if self._window.isVisible():
                self._window.hide()
            else:
                self._window.show()

    def _set_quit_action_add_(self, menu):
        widget_action = QtWidgetAction(menu)
        widget_action.setFont(Font.NAME)
        widget_action.setText('quit')
        widget_action.setIcon(QtIconMtd.create_by_icon_name('window/close'))
        menu.addAction(widget_action)
        widget_action.triggered.connect(
            self._window.close
        )


class QtPixmapDrawer(object):
    @classmethod
    def test(cls):
        r, g, b, a = 47, 47, 47, 255
        w, h = 2048, 2048
        g_w, g_h = w, 48
        pixmap = QtGui.QPixmap(QtCore.QSize(w, h))
        pixmap.fill(QtGui.QColor(r, g, b, a))
        painter = QtPainter(pixmap)

        file_path = '/data/f/test_rvio/test_guide_1.png'

        guide_data = [
            ('primary', 8),
            ('object-color', 8),
            ('wire', 8),
            ('density', 8)
        ]
        max_c = sum([i[1] for i in guide_data])
        border_rgb = 255, 255, 255
        i_x_0, i_y_0 = 0, h-g_h
        for i in guide_data:
            i_text, i_c = i
            i_background_rgb = bsc_core.RawTextOpt(i_text).to_rgb()
            # background
            i_p = i_c/float(max_c)
            i_x_1, i_y_1 = int(i_x_0+i_p*w), h-1
            i_g_w = w*i_p
            i_g_rect = QtCore.QRect(
                i_x_0, i_y_0, i_g_w, g_h
            )

            painter._set_border_color_(*border_rgb)
            painter._set_background_color_(*i_background_rgb)
            painter.drawRect(
                i_g_rect
            )

            painter._set_font_(get_font(g_h*.8))

            i_t_r, i_t_g, i_t_b = bsc_core.RawColorMtd.get_complementary_rgb(*i_background_rgb)
            i_t_a = QtGui.qGray(i_t_r, i_t_g, i_t_b )
            if i_t_a >= 127:
                i_t_r_ = 223
            else:
                i_t_r_ = 63
            #
            i_t_r__ = QtGui.QColor(i_t_r_, i_t_r_, i_t_r_)

            i_text_option = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

            painter._set_border_color_(i_t_r__)
            painter.drawText(
                i_g_rect,
                i_text_option,
                i_text,
            )

            i_x_0 = i_x_1

        painter.end()

        format_ = 'png'
        pixmap.save(
            file_path,
            format_
        )
    @classmethod
    def get_image_by_data(cls, data, file_path):
        x, y = 0, 0
        w, h = data.get('image.size')

        pixmap = QtGui.QPixmap(QtCore.QSize(w, h))
        r, g, b, a = data.get('image.background')
        pixmap.fill(QtGui.QColor(r, g, b, a))

        painter = QtPainter(pixmap)
        m = 48
        if data.get('draw.text'):
            text_content = data.get('draw.text.content')
            text_size = data.get('draw.text.size')
            text_weight = data.get('draw.text.weight')
            font_color = data.get('draw.text.color')
            txt_rect = QtCore.QRect(x+m, y+m, w, h/2)
            if isinstance(text_content, dict):
                painter._set_text_draw_by_rect_use_dict_(
                    txt_rect, text_content, text_size, text_weight, font_color
                )

        painter.end()

        format_ = os.path.splitext(file_path)[-1][1:]

        pixmap.save(
            file_path,
            format_
        )


class QtItemSignals(
    QtCore.QObject
):
    visible = qt_signal(bool)
    expanded = qt_signal(bool)
    #
    pressed = qt_signal(object, int)
    #
    press_db_clicked = qt_signal(object, int)
    press_clicked = qt_signal(object, int)
    #
    check_clicked = qt_signal(object, int)
    check_toggled = qt_signal(object, int, bool)

    user_check_clicked = qt_signal(object, int)
    user_check_toggled = qt_signal(object, int, bool)
    #
    drag_pressed = qt_signal(tuple)
    drag_move = qt_signal(tuple)
    drag_released = qt_signal(tuple)


if __name__ == '__main__':
    pass

