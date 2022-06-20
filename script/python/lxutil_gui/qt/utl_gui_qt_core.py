# coding:utf-8
import functools
import glob

import sys
#
import cgitb
#
import math
#
import threading

import types
#
from lxbasic import bsc_configure, bsc_core

from lxbasic.objects import bsc_obj_abs

import lxutil.modifiers as utl_modifiers
#
from lxutil import utl_configure, utl_core, utl_abstract, methods

from lxutil_gui import utl_gui_core

import lxutil.objects as utl_objects

import subprocess

_pyqt5 = utl_objects.PyModule('PyQt5')

if _pyqt5.get_is_exists() is True:
    LOAD_INDEX = 0
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg
else:
    LOAD_INDEX = 1
    _pyside2 = utl_objects.PyModule('PySide2')
    if _pyside2.get_is_exists() is True:
        # noinspection PyUnresolvedReferences
        from PySide2 import QtGui, QtCore, QtWidgets, QtSvg
    else:
        raise ImportError()

cgitb.enable(
    logdir=bsc_core.SystemMtd.get_debug_directory_path(tag='qt', create=True),
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
    module = utl_objects.PyModule(load_dic[key][LOAD_INDEX][0])
    method = module.get_method(method_name)
    return method(*args)


def qt_wrapinstance(*args):
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    module_name, method_name = load_dic[key][LOAD_INDEX]
    module = utl_objects.PyModule(load_dic[key][LOAD_INDEX][0])
    method = module.get_method(method_name)
    return method(*args)


def qt_is_deleted(*args):
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    module_name, method_name = load_dic[key][LOAD_INDEX]
    module = utl_objects.PyModule(load_dic[key][LOAD_INDEX][0])
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


def set_shadow(qt_widget, radius):
    shadow = QtWidgets.QGraphicsDropShadowEffect()
    shadow.setBlurRadius(radius)
    shadow.setColor(QtBackgroundColor.Black)
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
        window = args[0].widget
        # window.setCursor(QtCore.Qt.BusyCursor)
        prx_window.set_waiting_start()
        _method = method(*args, **kwargs)
        # window.unsetCursor()
        prx_window.set_waiting_stop()
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
    GROUP = get_font(size=10, weight=75, italic=True)
    #
    default = get_font()
    title = get_font(size=12)
    #
    disable = get_font(italic=True, strike_out=True)
    #
    button = get_font(size=10)


class TextMtd(object):
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


class QtBorderColor(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *utl_gui_core.QtStyleMtd.get_border(key)
        )

    Transparent = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-transparent')
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
    IconHovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-icon-hovered')
    )

    Button = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_border('color-button')
    )


class QtBackgroundColor(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *utl_gui_core.QtStyleMtd.get_background(key)
        )

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

    Selected = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-selected')
    )
    Actioned = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-actioned')
    )
    Hovered = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-hovered')
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
    ItemLoading = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_background('color-item-loading')
    )


class QtFontColor(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *utl_gui_core.QtStyleMtd.get_font(key)
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

    Disable = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-disable')
    )

    ToolTip = QtGui.QColor(
        *utl_gui_core.QtStyleMtd.get_font('color-tool-tip')
    )


class Brush(object):
    text = QtGui.QBrush(QtGui.QColor(191, 191, 191, 255))
    TEXT_NORMAL = QtGui.QBrush(QtFontColor.Basic)
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
        os_icon_file = utl_core.Icon.get(icon_name)
        qt_icon = QtGui.QIcon()
        qt_icon.addPixmap(
            QtGui.QPixmap(os_icon_file),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        return qt_icon
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
    def get_qt_palette(cls, tool_tip=False):
        palette = QtGui.QPalette()
        palette.setColor(palette.All, palette.Shadow, QtBackgroundColor.Black)
        palette.setColor(palette.All, palette.Dark, QtBackgroundColor.Dim)
        palette.setColor(palette.All, palette.Background, QtBackgroundColor.Basic)
        palette.setColor(palette.All, palette.NoRole, QtBackgroundColor.Dark)
        palette.setColor(palette.All, palette.Base, QtBackgroundColor.Dark)
        palette.setColor(palette.All, palette.Light, QtBackgroundColor.Light)
        palette.setColor(palette.All, palette.Highlight, QtBackgroundColor.Selected)
        palette.setColor(palette.All, palette.Button, QtBackgroundColor.Button)
        #
        palette.setColor(palette.All, palette.Window, QtBackgroundColor.Basic)
        #
        palette.setColor(palette.All, palette.Text, QtFontColor.Basic)
        palette.setColor(palette.All, palette.BrightText, QtFontColor.Light)
        palette.setColor(palette.All, palette.WindowText, QtFontColor.Basic)
        palette.setColor(palette.All, palette.ButtonText, QtFontColor.Basic)
        palette.setColor(palette.All, palette.HighlightedText, QtFontColor.Light)
        #
        palette.setColor(palette.All, palette.AlternateBase, QtBackgroundColor.Basic)
        # tool-tip
        if tool_tip is True:
            p = QtWidgets.QToolTip.palette()
            p.setColor(palette.All, p.ToolTipBase, QtBackgroundColor.ToolTip)
            p.setColor(palette.All, palette.ToolTipText, QtFontColor.ToolTip)
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
        painter.setPen(QtGui.QColor(QtBorderColor.Icon))
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
            QtBorderColor.Icon
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        rd = min(w, h)
        icon_rect = QtCore.QRect(
            x + (w - c_w) / 2, y + (h - c_h) / 2,
            c_w, c_h
        )
        if text is not None:
            name = text.split('/')[-1] or ' '
            painter.setPen(QtBorderColor.Icon)
            if background_color is not None:
                r, g, b = background_color
                text_color_ = QtFontColor.Basic
            else:
                r, g, b = bsc_core.TextOpt(name).to_rgb()
                t_r, t_g, t_b = bsc_core.ColorMtd.get_complementary_rgb(r, g, b)
                t_r = QtGui.qGray(t_r, t_g, t_b)
                if t_r >= 127:
                    t_r_1 = 223
                else:
                    t_r_1 = 63
                text_color_ = QtGui.QColor(t_r_1, t_r_1, t_r_1)
            #
            painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
            # painter.drawRect(
            #     icon_rect,
            # )
            painter.drawRoundedRect(icon_rect, 2, 2, QtCore.Qt.AbsoluteSize)
            painter.setPen(text_color_)
            painter.setFont(get_font(size=int(rd*.675), italic=True))
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


class QtIconMtd(object):
    @classmethod
    def get_by_icon_name(cls, icon_name):
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
            QtBorderColor.Icon
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        icon_rect = QtCore.QRect(
            x + (w - c_w) / 2, y + (h - c_h) / 2,
            c_w, c_h
        )
        if text is not None:
            name = text.split('/')[-1] or ' '
            painter.setPen(QtBorderColor.Icon)
            r, g, b = bsc_core.TextOpt(name).to_rgb()
            if background_color is not None:
                r, g, b = background_color
            painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
            painter.drawRect(icon_rect)
            # painter.drawRoundedRect(icon_rect, f_w/2, f_w/2, QtCore.Qt.AbsoluteSize)
            #
            # t_r, t_g, t_b = bsc_core.ColorMtd.get_complementary_rgb(r, g, b)
            painter.setPen(QtFontColor.Basic)
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
                i_g = QtGui.qGray(i_p)
                i_g_c = QtGui.QColor(i_g, i_g, i_g)
                image_gray.setPixel(i_x, i_y, i_g_c.rgb())
        #
        image_gray.setAlphaChannel(image_alpha)
        return pixmap.fromImage(image_gray)
    @classmethod
    def get_by_file(cls, file_path, size=(20, 20)):
        pixmap = QtGui.QPixmap(file_path)
        new_pixmap = pixmap.scaled(
            QtCore.QSize(*size),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        return new_pixmap
    @classmethod
    def get_by_file_ext(cls, ext, size=(20, 20), gray=False):
        _ = utl_core.FileIcon.get_by_file_ext(ext)
        if _ is not None:
            pixmap = cls.get_by_file(_, size)
            if gray is True:
                return cls._to_gray_(pixmap)
            return pixmap
        return cls.get_by_name(
            ext[1:]
        )
    @classmethod
    def get_by_file_ext_with_tag(cls, ext, tag, size=(20, 20), gray=False):
        pixmap = cls.get_by_file_ext(
            ext=ext,
            size=size,
            gray=gray
        )
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(painter.Antialiasing)
        rect = pixmap.rect()
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        rd = min(w, h)
        tag_rect = QtCore.QRect(
            x+rd/2-1, y+rd/2-1, rd/2, rd/2
        )
        painter.setPen(QtBorderColor.Icon)
        r, g, b = bsc_core.TextOpt(tag).to_rgb()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
        painter.drawRoundedRect(tag_rect, rd/8, rd/8, QtCore.Qt.AbsoluteSize)
        #
        t_r, t_g, t_b = bsc_core.ColorMtd.get_complementary_rgb(r, g, b)
        t_r = QtGui.qGray(t_r, t_g, t_b)
        if t_r >= 127:
            t_r_1 = 223
        else:
            t_r_1 = 63
        #
        text_color_ = QtGui.QColor(t_r_1, t_r_1, t_r_1)
        painter.setPen(text_color_)
        painter.setFont(get_font(size=int(rd/2*.675), italic=True))
        painter.drawText(
            tag_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(tag[0]).capitalize()
        )
        painter.end()
        return pixmap
    @classmethod
    def get_by_name(cls, text, rounded=False, background_color=None):
        f_w, f_h = 14, 14
        c_w, c_h = 13, 13
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = QtGui.QPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            QtBorderColor.Icon
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        rd = min(w, h)
        icon_rect = QtCore.QRect(
            x + (w - c_w) / 2, y + (h - c_h) / 2,
            c_w, c_h
        )
        if text is not None:
            name = text.split('/')[-1] or ' '
            painter.setPen(QtBorderColor.Icon)
            r, g, b = bsc_core.TextOpt(name).to_rgb()
            if background_color is not None:
                r, g, b = background_color
            painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
            painter.drawRect(icon_rect)
            # painter.drawRoundedRect(icon_rect, f_w/2, f_w/2, QtCore.Qt.AbsoluteSize)
            #
            # t_r, t_g, t_b = bsc_core.ColorMtd.get_complementary_rgb(r, g, b)
            painter.setPen(QtFontColor.Basic)
            painter.setFont(get_font(size=int(rd*.6), italic=True))
            painter.drawText(
                rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                str(name[0]).capitalize()
            )
        #
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
    def get_main_window(cls):
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
    def get_main_window(cls):
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
        main_window = cls.get_main_window()
        if main_window:
            return main_window.getMenuBar()
        else:
            utl_core.Log.set_module_warning_trace(
                'qt-katana',
                'main-window is non-exists'
            )
    @classmethod
    def get_menu(cls, name):
        menu_bar = cls.get_menu_bar()
        if menu_bar:
            for i_child in menu_bar.children():
                if isinstance(i_child, QtWidgets.QMenu):
                    i_name = i_child.title()
                    if i_name == name:
                        return i_child
        else:
            utl_core.Log.set_module_warning_trace(
                'qt-katana',
                'menu-bar is non-exists'
            )


class QtDccMtd(utl_abstract.AbsDccMtd):
    MAIN_WINDOW = None
    @classmethod
    def get_qt_main_window(cls):
        if cls.get_is_maya():
            return QtMayaMtd.get_qt_main_window()
        elif cls.get_is_houdini():
            return QtHoudiniMtd.get_main_window()
        elif cls.get_is_katana():
            return QtKatanaMtd.get_main_window()
        #
        if cls.MAIN_WINDOW is not None:
            return cls.MAIN_WINDOW
        #
        _ = QtWidgets.QApplication.topLevelWidgets()
        if _:
            cls.MAIN_WINDOW = _[0]
        return QtWidgets.QApplication.activeWindow()
    @classmethod
    def get_qt_icon(cls, icon_name):
        if cls.get_is_maya():
            return QtMayaMtd.get_qt_icon(icon_name)
        elif cls.get_is_houdini():
            return QtHoudiniMtd.get_qt_icon(icon_name)
    @classmethod
    def get_qt_palette_(cls):
        if cls.get_is_maya():
            return QtMayaMtd.get_qt_main_window().palette()
        elif cls.get_is_houdini():
            return QtHoudiniMtd.get_main_window().palette()
        elif cls.get_is_katana():
            return QtKatanaMtd.get_main_window().palette()
        else:
            return QtUtilMtd.get_qt_palette()
    @classmethod
    def get_qt_palette(cls):
        if cls.get_is_maya():
            return QtUtilMtd.get_qt_palette()
        elif cls.get_is_houdini():
            return QtUtilMtd.get_qt_palette()
        elif cls.get_is_katana():
            return QtUtilMtd.get_qt_palette()
        else:
            return QtUtilMtd.get_qt_palette(tool_tip=True)


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
                array_grid = methods.List.set_grid_to(foregrounds, 8)
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


class QtMethodSignals(QtCore.QObject):
    stated = qt_signal()
    running = qt_signal()
    stopped = qt_signal()
    #
    completed = qt_signal()
    error_occurred = qt_signal()


class QtMethodThread(QtCore.QThread):
    stated = qt_signal()
    running = qt_signal()
    stopped = qt_signal()
    #
    completed = qt_signal()
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
        #
        for i in self._methods:
            i()
        #
        self.run_finished.emit()


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
            #
            finally:
                self.run_finished.emit()
                self.set_status(self.Status.Finished)


class QtBuildThreadsRunner(QtCore.QObject):
    run_started = qt_signal()
    run_finished = qt_signal()
    run_resulted = qt_signal(list)
    def __init__(self, *args, **kwargs):
        super(QtBuildThreadsRunner, self).__init__(*args, **kwargs)
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
        index = self._threads.index(thread)
        self._results[index] = result
        if sum(self._results) == len(self._results):
            self.run_finished.emit()

    def set_kill(self):
        [i.set_kill() for i in self._threads]
        # self._mutex.unlock()

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


class QtCmdSubProcessThread(QtCore.QThread):
    Status = bsc_configure.Status
    def __init__(self, *args, **kwargs):
        super(QtCmdSubProcessThread, self).__init__(*args, **kwargs)
        self._cmd = None

        self._status = self.Status.Waiting

    def set_cmd(self, cmd):
        self._cmd = cmd

    def set_status(self, status):
        pass

    def run(self):
        if self._status == self.Status.Waiting:
            self.set_status(self.Status.Running)
            try:
                results = bsc_core.SubProcessMtd.set_run_as_block(
                    self._cmd
                )
                self.set_status(self.Status.Completed)
                self.set_completed(results)
            except subprocess.CalledProcessError:
                self.set_status(self.Status.Error)


class QtHBoxLayout(QtWidgets.QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtHBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*Util.LAYOUT_MARGINS)
        self.setSpacing(Util.LAYOUT_SPACING)

    def _set_align_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignTop
        )


class QtVBoxLayout(QtWidgets.QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtVBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*Util.LAYOUT_MARGINS)
        self.setSpacing(Util.LAYOUT_SPACING)

    def _set_align_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignTop
        )


class QtGridLayout(QtWidgets.QGridLayout):
    def __init__(self, *args, **kwargs):
        super(QtGridLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*Util.LAYOUT_MARGINS)
        self.setSpacing(Util.LAYOUT_SPACING)


class QtFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QtFileDialog, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())


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
        eR = 4
        ia = 90
        offset_x, offset_y = offset
        explain, maxValue, value = subDatum
        percent = float(value) / float(max(maxValue, 1))
        #
        text = '{} : {}%'.format(explain, bsc_core.ValueMtd.get_percent_prettify(value=value, maximum=maxValue))
        #
        color_percent = max(min(percent, 1), .005)
        if maxValue == 0:
            border_rgba = 95, 95, 95, 255
            background_rgba = 95, 95, 95, 255
        else:
            if percent == 1:
                r, g, b = 63, 255, 127
                if mode is utl_configure.GuiSectorChartMode.Error:
                    r, g, b = 255, 0, 63
            elif percent == 0:
                r, g, b = 255, 0, 63
                if mode is utl_configure.GuiSectorChartMode.Error:
                    r, g, b = 63, 255, 127
            #
            elif percent > 1:
                r, g, b = bsc_core.ColorMtd.hsv2rgb(240 - min(percent * 15, 45), 1, 1)
            else:
                r, g, b = bsc_core.ColorMtd.hsv2rgb(45 * color_percent, 1, 1)
                if mode is utl_configure.GuiSectorChartMode.Error:
                    r, g, b = bsc_core.ColorMtd.hsv2rgb(45 - 45 * color_percent, 1, 1)
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
        cx, cy = out_x + out_r / 2, out_y + out_r / 2
        #
        rim_sub_path = QtGui.QPainterPath()
        rim_sub_path.moveTo(cx, cy)
        sub_angle = -360 * .25
        rim_sub_path.arcTo(out_x - 1, out_y - 1, out_r + 2, out_r + 2, ia, sub_angle)
        #
        percent_sub_path = QtGui.QPainterPath()
        percent_sub_path.moveTo(cx, cy)
        percentSubAngle = -360 * (1 - draw_percent)
        percent_sub_path.arcTo(out_x - 1, out_y - 1, out_r + 2, out_r + 2, ia, percentSubAngle)
        #
        total_path = rim_path - rim_sub_path
        occupy_path = rim_path - percent_sub_path
        #
        x1, y1 = cx, out_y + (tape_w - spacing) / 4
        x2, y2 = x1 + tape_w / 4, y1
        x3, y3 = x2 + tape_w / 4, y2 + tape_w / 4
        x4, y4 = x3 + tape_w / 4, y3
        text_line = QtGui.QPolygon(
            [QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2), QtCore.QPoint(x3, y3), QtCore.QPoint(x4 - eR, y4)]
        )
        text_point = QtCore.QPoint(x4 + eR + 4, y4 + 4)
        text_ellipse = QtCore.QRect(x4 - eR, y4 - eR, eR * 2, eR * 2)
        return background_rgba, border_rgba, total_path, occupy_path, text_point, text_line, text_ellipse, text

    @classmethod
    def _get_basic_data_(cls, data, offset, radius, tape_w, spacing, mode):
        lis = []
        if data:
            for i_index, i_datum in enumerate(data):
                subDrawDatum = cls._get_basic_data_at_(
                    i_index, i_datum, offset, radius, tape_w, spacing, mode
                )
                lis.append(subDrawDatum)
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
            tape_w = int(radius / count * .75)
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
        ia = 90
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
        g_c = QtGui.QConicalGradient(cx, cy, ia)
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
        eR = 4
        ia = -90
        explain, value_src, value_tgt = data
        #
        percent_src = float(value_src) / float(max(value_maximum, 1))
        percent_tgt = float(value_tgt) / float(max(value_maximum, 1))
        #
        value_sub = value_tgt - value_src
        percent_sub = float(value_sub) / float(max(value_src, 1))
        text_0 = explain
        if value_sub == 0:
            text_1 = '{}'.format(bsc_core.IntegerMtd.get_prettify(value_tgt))
        else:
            text_1 = '{} ( {}% )'.format(
                bsc_core.IntegerMtd.get_prettify(value_tgt),
                bsc_core.ValueMtd.get_percent_prettify(value=value_sub, maximum=value_src)
            )
        #
        if value_maximum == 0:
            border_rgba = 95, 95, 95, 255
            background_rgba = 95, 95, 95, 255
        else:
            if percent_sub == 0:
                r, g, b = 64, 255, 127
            elif percent_sub > 0:
                r, g, b = bsc_core.ColorMtd.hsv2rgb(45 * (1 - min(percent_sub, 1)), 1, 1)
            else:
                r, g, b = bsc_core.ColorMtd.hsv2rgb(120 + 45 * (1 - min(percent_sub, 1)), 1, 1)
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
        basic_path.arcTo(x, y, r, r, angle_start + ia, angle_end + ia)
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
        mark_ellipse = QtCore.QRect(map_x_0 - eR, map_y_0 - eR, eR * 2, eR * 2)
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
                subDrawDatum = cls._get_mark_data_at_(
                    i_index,
                    index_maximum,
                    value_maximum,
                    i_data,
                    offset_x, offset_y,
                    radius,
                    spacing
                )
                lis.append(subDrawDatum)
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
            _i_color = bsc_core.TextOpt(_i_name).to_rgb()
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
                bsc_core.ValueMtd.get_percent_prettify(value=_i_value, maximum=maximum)
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
    @utl_modifiers.set_method_exception_catch
    def _set_cmd_debug_run_(self, cmd_str):
        exec cmd_str
    @utl_modifiers.set_method_exception_catch
    def _set_fnc_debug_run_(self, fnc):
        fnc()

    def set_create_by_content(self, content):
        self._root_menu.clear()
        self._item_dic = {
            '/': self._root_menu
        }
        if isinstance(content, bsc_obj_abs.AbsContent):
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
            QtIconMtd.get_by_icon_name('file/folder')
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
                QtIconMtd.get_by_icon_name(icon_name)
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
        elif isinstance(execute_fnc, (str, unicode)):
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


def set_gui_proxy_set_print(gui_proxy, text):
    if hasattr(gui_proxy, 'set_print_add_use_thread'):
        gui_proxy.set_print_add_use_thread(text)


# log
def set_qt_log_result_trace(text):
    windows = get_all_lx_windows()
    if windows:
        window = windows[0]
        window_gui_proxy = window.gui_proxy
        if hasattr(window_gui_proxy, 'PRX_TYPE'):
            if window_gui_proxy.PRX_TYPE == 'tool_window':
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
    utl_core.__dict__['QT_LOG_RESULT_TRACE_METHOD'] = set_qt_log_result_trace
    utl_core.__dict__['QT_LOG_WARNING_TRACE_METHOD'] = set_qt_log_result_trace
    utl_core.__dict__['QT_LOG_ERROR_TRACE_METHOD'] = set_qt_log_result_trace


def set_log_write(text):
    windows = get_all_lx_windows()
    lis = []
    for window in windows:
        if hasattr(window, 'gui_proxy'):
            window_gui_proxy = window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_TYPE'):
                if window_gui_proxy.PRX_TYPE == 'tool_window':
                    lis.append(window_gui_proxy)
    if lis:
        lis[0].set_log_write(text)


def get_all_tool_windows():
    windows = get_all_lx_windows()
    lis = []
    for window in windows:
        if hasattr(window, 'gui_proxy'):
            window_gui_proxy = window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_TYPE'):
                if window_gui_proxy.PRX_TYPE == 'tool_window':
                    lis.append(window_gui_proxy)
    return lis


def set_log_writer_connect():
    utl_core.__dict__['LOG_WRITE_METHOD'] = set_log_write


# progress
def set_qt_progress_create(maximum, label=None):
    lis = []
    windows = get_all_lx_windows()
    for window in windows:
        if hasattr(window, 'gui_proxy'):
            window_gui_proxy = window.gui_proxy
            if hasattr(window_gui_proxy, 'PRX_TYPE'):
                if window_gui_proxy.PRX_TYPE == 'tool_window':
                    p = window_gui_proxy.set_progress_create(maximum, label=label)
                    lis.append(p)
    return lis


def set_qt_progress_connect_create():
    utl_core.__dict__['QT_PROGRESS_CREATE_METHOD'] = set_qt_progress_create


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
            elif isinstance(method, (str, unicode)):
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
            if isinstance(i_key, (str, unicode)):
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
        widget_action.setIcon(QtIconMtd.get_by_icon_name('window/close'))
        menu.addAction(widget_action)
        widget_action.triggered.connect(
            self._window.close
        )


def set_window_show_standalone(window_class, **kwargs):
    exists_app = QtWidgets.QApplication.instance()
    if exists_app is None:
        app = QtWidgets.QApplication(sys.argv)
        app.setPalette(QtDccMtd.get_qt_palette())

        QtUtilMtd.set_fonts_add(
            utl_gui_core.RscFontFile.get_all()
        )
        prx_window = window_class(**kwargs)
        window = prx_window.widget
        system_tray_icon = QtSystemTrayIcon(window)
        # a = utl_gui_qt_core.QtWidgets.QAction('show', triggered=window.widget.show)
        system_tray_icon.setIcon(window.windowIcon())
        system_tray_icon.show()
        window._set_window_system_tray_icon_(system_tray_icon)
        prx_window.set_window_show()
        sys.exit(app.exec_())
    else:
        prx_window = window_class(**kwargs)
        prx_window.set_window_show()
