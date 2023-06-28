# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_entry_base, _utl_gui_qt_wgt_popup, _utl_gui_qt_wgt_chart

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class AbsQtHeadFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    utl_gui_qt_abstract.AbsQtIconBaseDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForExpandDef,
):
    def __init__(self, *args, **kwargs):
        super(AbsQtHeadFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        #
        self._init_frame_base_def_(self)
        self._init_name_base_def_(self)
        self._name_draw_font = Font.GROUP
        #
        self._init_icon_base_def_(self)
        self._icon_name_is_enable = True
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expanded = False
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('expandopen')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('expandclose')

        self._expand_sub_icon_file_path_0 = None
        self._expand_sub_icon_file_path_1 = None

        self._is_hovered = False
        #
        self._refresh_expand_()
        #
        r, g, b = 207, 207, 207
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._name_color = color
        self._hover_name_color = hover_color
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        # font
        self.setFont(self._name_draw_font)

        self._line_draw_points = QtCore.QPoint(), QtCore.QPoint()

        self._icon_draw_percent = .65

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        #
        self._set_frame_draw_rect_(
            c_x+1, c_y+1, w-2, h-2
        )
        frm_w = frm_h = h
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_frm_m_w, icn_frm_m_h = (frm_w-icn_frm_w)/2, (frm_h-icn_frm_h)/2
        icn_w, icn_h = icn_frm_w*self._icon_draw_percent, icn_frm_h*self._icon_draw_percent

        if self._icon_sub_file_path is not None:
            frm_x, frm_y = c_x+(frm_w-icn_frm_w)/2, c_y+(frm_h-icn_frm_h)/2
            sub_icn_w, sub_icn_h = icn_frm_w*self._icon_sub_draw_percent, icn_frm_h*self._icon_sub_draw_percent
            self._set_icon_file_draw_rect_(
                 c_x+icn_frm_m_w, c_y+icn_frm_m_h, icn_w, icn_h
            )
            self._set_sub_icon_file_draw_rect_(
                frm_x+frm_w-sub_icn_w-icn_frm_m_w, frm_y+frm_h-sub_icn_h-icn_frm_m_h, sub_icn_w, sub_icn_h
            )
        else:
            self._set_icon_file_draw_rect_(
                c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
            )
        #
        c_x += icn_frm_w+spacing
        #
        if self._name_text:
            self._set_name_draw_rect_(
                c_x, c_y, w-c_x, frm_h
            )

    def _set_expand_icon_file_path_(self, icon_file_path_0, icon_file_path_1):
        self._expand_icon_file_path_0 = icon_file_path_0
        self._expand_icon_file_path_1 = icon_file_path_1
        self._refresh_expand_()

    def _set_expand_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get(icon_name_0)
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get(icon_name_1)
        self._refresh_expand_()

    def _set_expand_sub_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_sub_icon_file_path_0 = utl_gui_core.RscIconFile.get(icon_name_0)
        self._expand_sub_icon_file_path_1 = utl_gui_core.RscIconFile.get(icon_name_1)
        self._refresh_expand_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.ExpandClick)
                    #
                    self.press_toggled.emit(True)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.ExpandClick:
                        self._execute_action_expand_()
                    #
                    self.press_toggled.emit(False)
                #
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        background_color = self._frame_background_color
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            # border_radius=1,
            offset=offset
        )
        # name-icon
        if self._icon_name_is_enable is True:
            if self._icon_name_text is not None:
                painter._draw_frame_color_with_name_text_by_rect_(
                    rect=self._frame_draw_rect,
                    text=self._icon_name_text,
                    offset=offset,
                )
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._is_hovered
        )
        # text
        if self._name_text is not None:
            color = self._name_color
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=self._name_draw_font,
                font_color=color,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
        )
        self._set_icon_sub_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._is_expanded]
        )
        #
        self._refresh_widget_draw_()


class QtHHeadFrame(AbsQtHeadFrame):
    def __init__(self, *args, **kwargs):
        super(QtHHeadFrame, self).__init__(*args, **kwargs)


class QtHHeadFrame_(AbsQtHeadFrame):
    def __init__(self, *args, **kwargs):
        super(QtHHeadFrame_, self).__init__(*args, **kwargs)

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        c_x, c_y = x, y
        w, h = self.width(), self.height()
        spacing = 2
        #
        self._set_frame_draw_rect_(
            c_x+1, c_y+1, w-2, h-2
        )
        frm_w = frm_h = h
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_frm_m_w, icn_frm_m_h = (frm_w-icn_frm_w)/2, (frm_h-icn_frm_h)/2
        icn_w, icn_h = icn_frm_w*self._icon_draw_percent, icn_frm_h*self._icon_draw_percent

        if self._icon_sub_file_path is not None:
            frm_x, frm_y = c_x+(frm_w-icn_frm_w)/2, c_y+(frm_h-icn_frm_h)/2
            sub_icn_w, sub_icn_h = icn_frm_w*self._icon_sub_draw_percent, icn_frm_h*self._icon_sub_draw_percent
            self._set_icon_file_draw_rect_(
                 c_x+icn_frm_m_w, c_y+icn_frm_m_h, icn_w, icn_h
            )
            self._set_sub_icon_file_draw_rect_(
                frm_x+frm_w-sub_icn_w-icn_frm_m_w, frm_y+frm_h-sub_icn_h-icn_frm_m_h, sub_icn_w, sub_icn_h
            )
        else:
            self._set_icon_file_draw_rect_(
                c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
            )
        #
        c_x += icn_frm_w+spacing
        #
        if self._name_text:
            t_w = self._get_name_text_draw_width_(self._name_text) + 8
            self._set_name_draw_rect_(
                c_x, c_y, t_w, frm_h
            )
            c_x += t_w
        #
        if self._is_expanded is True:
            self._line_draw_points[0].setX(x)
            self._line_draw_points[0].setY(y+h-1)
            self._line_draw_points[1].setX(w)
            self._line_draw_points[1].setY(y+h-1)
        else:
            self._line_draw_points[0].setX(c_x)
            self._line_draw_points[0].setY(c_y+h/2)
            self._line_draw_points[1].setX(w)
            self._line_draw_points[1].setY(c_y+h/2)

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        background_color = self._frame_background_color
        #
        painter._draw_line_by_points_(
            point_0=self._line_draw_points[0], point_1=self._line_draw_points[1],
            border_color=background_color,
            # border_width=1
        )
        # name-icon
        if self._icon_name_is_enable is True:
            if self._icon_name_text is not None:
                painter._draw_frame_color_with_name_text_by_rect_(
                    rect=self._frame_draw_rect,
                    text=self._icon_name_text,
                    offset=offset,
                )
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._is_hovered
        )
        # text
        if self._name_text is not None:
            color = self._name_color
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=self._name_text,
                font=self._name_draw_font,
                font_color=color,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )


class AbsQtExpandHead1(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    utl_gui_qt_abstract.AbsQtIconBaseDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForExpandDef,
):
    toggled = qt_signal(bool)
    def __init__(self, *args, **kwargs):
        super(AbsQtExpandHead1, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self._init_frame_base_def_(self)
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expand_enable = True
        self._is_expanded = False
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
        self._expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-up')
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        #
        self._refresh_expand_()
        # font
        self.setFont(Font.NAME)

    def _refresh_widget_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        frame_color = Color.BAR_FRAME_NORMAL
        painter._set_border_color_(frame_color)
        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=self._frame_background_color,
            # border_radius=self._frame_border_radius,
            offset=offset
        )
        # icon
        painter._draw_icon_file_by_rect_(
            rect=self._icon_draw_rect,
            file_path=self._icon_file_path,
            offset=offset,
            is_hovered=self._is_hovered
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.ExpandClick)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.ExpandClick:
                        self._execute_action_expand_()
                #
                self._clear_all_action_flags_()
        return False

    def _refresh_expand_(self):
        if self._is_expanded is True:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
            )
        else:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
        #
        if self._expand_direction == self.ExpandDirection.TopToBottom:
            self._set_icon_file_path_(
                [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
            )
        elif self._expand_direction == self.ExpandDirection.BottomToTop:
            self._set_icon_file_path_(
                [self._expand_icon_file_path_1, self._expand_icon_file_path_2][self._is_expanded]
            )
        #
        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._set_frame_draw_rect_(
            x+1, y+1, w-2, h-2
        )
        #
        icn_frm_w, icn_frm_h = 12, 12
        i_w, i_h = 8, 8
        #
        if self._expand_direction == self.ExpandDirection.TopToBottom:
            self._set_icon_file_draw_rect_(
                x+(icn_frm_w-i_w)/2, y+(icn_frm_h-i_h)/2,
                i_w, i_h
            )
        elif self._expand_direction == self.ExpandDirection.BottomToTop:
            self._set_icon_file_draw_rect_(
                x+(icn_frm_w-i_w)/2, y+h-icn_frm_h+(icn_frm_h-i_h)/2,
                i_w, i_h
            )


class QtHExpandHead1(AbsQtExpandHead1):
    def __init__(self, *args, **kwargs):
        super(QtHExpandHead1, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
        self._expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-up')


class QtVExpandHead1(AbsQtExpandHead1):
    def __init__(self, *args, **kwargs):
        super(QtVExpandHead1, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('qt-style/arrow-right')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('qt-style/arrow-down')
        self._expand_icon_file_path_2 = utl_gui_core.RscIconFile.get('qt-style/arrow-left')


class AbsQtExpandHead2(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    utl_gui_qt_abstract.AbsQtIconBaseDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionForExpandDef,
):
    def __init__(self, *args, **kwargs):
        super(AbsQtExpandHead2, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        #
        self._name_draw_font = Font.GROUP
        #
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._icon_name_is_enable = True
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expanded = False
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('v-bar-open')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('v-bar-close')

        self._expand_sub_icon_file_path_0 = None
        self._expand_sub_icon_file_path_1 = None

        self._is_hovered = False
        #
        self._refresh_expand_()
        #
        r, g, b = 207, 207, 207
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._name_color = color
        self._hover_name_color = hover_color
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        # font
        self.setFont(Font.NAME)

        self._icon_frame_draw_size = 12, 24
        self._icon_draw_percent = 1

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        #
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_p = self._icon_draw_percent
        icn_w, icn_h = icn_frm_w*icn_p, icn_frm_h*icn_p
        self._set_icon_file_draw_rect_(
            c_x+(w-icn_w)/2, c_y+(h-icn_h)/2, icn_w, icn_h
        )

    def _set_expand_icon_file_path_(self, icon_file_path_0, icon_file_path_1):
        self._expand_icon_file_path_0 = icon_file_path_0
        self._expand_icon_file_path_1 = icon_file_path_1
        self._refresh_expand_()

    def _set_expand_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get(icon_name_0)
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get(icon_name_1)
        self._refresh_expand_()

    def _set_expand_sub_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_sub_icon_file_path_0 = utl_gui_core.RscIconFile.get(icon_name_0)
        self._expand_sub_icon_file_path_1 = utl_gui_core.RscIconFile.get(icon_name_1)
        self._refresh_expand_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.ExpandClick)
                    #
                    self.press_toggled.emit(True)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.ExpandClick:
                        self._execute_action_expand_()
                    #
                    self.press_toggled.emit(False)
                #
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._is_hovered
        )

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_1, self._expand_icon_file_path_0][self._is_expanded]
        )
        self._set_icon_sub_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._is_expanded]
        )
        #
        self._refresh_widget_draw_()


class QtHExpandHead2(AbsQtExpandHead2):
    def __init__(self, *args, **kwargs):
        super(QtHExpandHead2, self).__init__(*args, **kwargs)
        self._icon_frame_draw_size = 12, 24
        self._icon_draw_percent = .75
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('v-bar-open')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('v-bar-close')


class QtVExpandHead2(AbsQtExpandHead2):
    def __init__(self, *args, **kwargs):
        super(QtVExpandHead2, self).__init__(*args, **kwargs)
        self._icon_frame_draw_size = 24, 12
        self._icon_draw_percent = .75
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('h-bar-open')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('h-bar-close')


class AbsQtToolBox(QtWidgets.QWidget):
    QT_HEAD_CLS = None
    QT_ORIENTATION = None
    QT_HEAD_W, QT_HEAD_H = 12, 24
    def __init__(self, *args, **kwargs):
        super(AbsQtToolBox, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self._build_widget_()

    def _build_widget_(self):
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self)
        else:
            raise RuntimeError()
        layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.setContentsMargins(*[0]*4)
        layout.setSpacing(0)
        # header
        self._head = self.QT_HEAD_CLS()
        layout.addWidget(self._head)
        self._head.expand_toggled.connect(self._set_expanded_)
        self._head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        self._head.setFixedSize(self.QT_HEAD_W, self.QT_HEAD_H)
        #
        self._container = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        layout.addWidget(self._container)
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            self._qt_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._container)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            self._qt_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._container)
        else:
            raise RuntimeError()
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)
        self._qt_layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #
        self._refresh_expand_()

    def _refresh_expand_(self):
        self._container.setVisible(self._head._get_is_expanded_())
        self._head._refresh_expand_()
        self._refresh_widget_size_()

    def _refresh_widget_size_(self):
        if self._head._get_is_expanded_() is True:
            s = self._qt_layout.minimumSize()
            w, h = s.width(), s.height()
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                self.setFixedSize(self.QT_HEAD_W+w, self.QT_HEAD_H)
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                self.setFixedSize(self.QT_HEAD_W, self.QT_HEAD_H+h)
        else:
            self.setFixedSize(self.QT_HEAD_W, self.QT_HEAD_H)

    def _set_expanded_(self, boolean):
        self._head._set_expanded_(boolean)
        self._refresh_expand_()
        
    def _refresh_container_size_(self):
        pass

    def _get_is_expanded_(self):
        return self._head._get_is_expanded_()

    def _add_widget_(self, widget):
        if isinstance(widget, QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget._qt_widget)
        #
        self._refresh_widget_size_()

    def _set_name_text_(self, text):
        self._head._set_name_text_(text)


class QtHToolBox(AbsQtToolBox):
    QT_HEAD_CLS = QtHExpandHead2
    QT_ORIENTATION = QtCore.Qt.Horizontal
    QT_HEAD_W, QT_HEAD_H = 12, 24
    def __init__(self, *args, **kwargs):
        super(QtHToolBox, self).__init__(*args, **kwargs)


class QtVToolBox(AbsQtToolBox):
    QT_HEAD_CLS = QtVExpandHead2
    QT_ORIENTATION = QtCore.Qt.Vertical
    QT_HEAD_W, QT_HEAD_H = 24, 12
    def __init__(self, *args, **kwargs):
        super(QtVToolBox, self).__init__(*args, **kwargs)
