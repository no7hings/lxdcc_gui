# coding:utf-8
from lxgui.qt.wrap import *

import math

import os

import time

import lxbasic.core as bsc_core

import lxgui.core as gui_core

from ..core import _gui_qt_cor_base


class QtPainterPath(QtGui.QPainterPath):
    def __init__(self, *args):
        super(QtPainterPath, self).__init__(*args)
        self.setFillRule(QtCore.Qt.WindingFill)

    def _set_points_add_(self, points):
        points_ = [QtCore.QPointF(x, y) for x, y in points]
        self.addPolygon(QtGui.QPolygonF(points_))


class QtPainter(QtGui.QPainter):

    def __init__(self, *args, **kwargs):
        super(QtPainter, self).__init__(*args, **kwargs)
        self.setRenderHint(self.Antialiasing)

    def _draw_capsule_by_rects_(
        self, rects, texts, checked_indices, index_hover, index_pressed, use_exclusive=False, is_enable=True
    ):
        c = len(texts)
        self._set_antialiasing_(True)
        for i, i_text in enumerate(texts):
            i_rect = rects[i]
            i_x, i_y = i_rect.x()+1, i_rect.y()
            i_w, i_h = i_rect.width()-2, i_rect.height()
            i_is_pressed = i == index_pressed
            if i_is_pressed:
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

            i_is_hovered = i == index_hover
            i_is_checked = checked_indices[i]
            if i_is_checked is True:
                i_border_width = 1
                self._set_border_color_(_gui_qt_cor_base.QtColors.CapsuleBorderChecked)
                if use_exclusive is True:
                    i_background_color, i_font_color = _gui_qt_cor_base.QtBackgroundColors.Selected, \
                        _gui_qt_cor_base.QtFontColors.Black
                else:
                    i_background_color, i_font_color = _gui_qt_cor_base.GuiQtColor.generate_color_args_by_text(i_text)
                self._set_background_color_(i_background_color)
            else:
                i_border_width = 1
                i_font_color = _gui_qt_cor_base.QtFontColors.Dark
                self._set_border_color_(_gui_qt_cor_base.QtColors.CapsuleBorderUnchecked)
                if is_enable is True:
                    self._set_background_color_(_gui_qt_cor_base.QtColors.CapsuleBackground)
                else:
                    self._set_background_color_(_gui_qt_cor_base.QtColors.CapsuleBackgroundDisable)
            #
            if i_is_pressed is True:
                i_border_width = 2
                self._set_border_color_(_gui_qt_cor_base.QtColors.CapsuleBorderActioned)
            elif i_is_hovered:
                i_border_width = 2
                self._set_border_color_(_gui_qt_cor_base.QtColors.CapsuleBorderHover)
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
            self._set_font_(_gui_qt_cor_base.QtFonts.Label)
            self._set_text_color_(i_font_color)
            # noinspection PyArgumentEqualDefault
            self.drawText(
                i_new_rect, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                i_text
            )

    def _draw_tab_left_tool_box_by_rect_(self, rect):
        color = QtGui.QLinearGradient(
            rect.topLeft(), rect.topRight()
        )
        color.setColorAt(
            0, _gui_qt_cor_base.QtBackgroundColors.Dark
        )
        color.setColorAt(
            0.95, _gui_qt_cor_base.QtBackgroundColors.Dark
        )
        color.setColorAt(
            1, _gui_qt_cor_base.QtBackgroundColors.Transparent
        )
        self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Transparent)
        self._set_background_color_(color)
        self.drawRect(rect)

    def _draw_tab_right_tool_box_by_rect_(self, rect):
        color = QtGui.QLinearGradient(
            rect.topLeft(), rect.topRight()
        )
        color.setColorAt(
            0, _gui_qt_cor_base.QtBackgroundColors.Transparent
        )
        color.setColorAt(
            0.05, _gui_qt_cor_base.QtBackgroundColors.Dark
        )
        color.setColorAt(
            1, _gui_qt_cor_base.QtBackgroundColors.Dark
        )
        self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Transparent)
        self._set_background_color_(color)
        self.drawRect(rect)

    def _draw_tab_buttons_by_rects_(
        self, frame_rect, virtual_items, index_hover, index_pressed,
        index_current
    ):
        self._draw_frame_by_rect_(
            rect=frame_rect,
            border_color=_gui_qt_cor_base.QtBorderColors.Transparent,
            background_color=_gui_qt_cor_base.QtBackgroundColors.Dark,
        )
        if virtual_items:
            for i_index, i_virtual_item in enumerate(virtual_items):
                i_name_text = i_virtual_item.name_text
                i_draw_rect = i_virtual_item.get_draw_rect()
                i_icon_text = i_virtual_item.icon_text
                i_is_hovered = i_index == index_hover
                i_is_pressed = i_index == index_pressed
                i_is_current = i_index == index_current
                if i_is_current is False:
                    self._draw_tab_button_at_(
                        frame_rect, i_draw_rect, i_name_text, i_icon_text, i_is_hovered, i_is_pressed, i_is_current
                    )
            # draw current
            for i_index, i_virtual_item in enumerate(virtual_items):
                i_name_text = i_virtual_item.name_text
                i_draw_rect = i_virtual_item.get_draw_rect()
                i_icon_text = i_virtual_item.icon_text
                i_is_hovered = i_index == index_hover
                i_is_pressed = i_index == index_pressed
                i_is_current = i_index == index_current
                if i_is_current is True:
                    self._draw_tab_button_at_(
                        frame_rect, i_draw_rect, i_name_text, i_icon_text, i_is_hovered, i_is_pressed, i_is_current
                    )
        else:
            f_x, f_y = frame_rect.x(), frame_rect.y()
            f_w, f_h = frame_rect.width(), frame_rect.height()
            self._set_border_color_(_gui_qt_cor_base.QtColors.TabBorderCurrent)
            self._set_border_width_(1)
            frame_coords = [(f_x, f_y+f_h), (f_w, f_y+f_h)]
            self._draw_path_by_coords_(frame_coords, antialiasing=False)

    def _draw_tab_button_at_(
        self, frame_rect, rect, text, icon_name_text, is_hovered, is_pressed, is_current
    ):
        f_x, f_y = frame_rect.x(), frame_rect.y()
        f_w, f_h = frame_rect.width(), frame_rect.height()
        a = 255

        if is_current is True:
            border_color = _gui_qt_cor_base.QtColors.TabBorderCurrent
        else:
            border_color = _gui_qt_cor_base.QtColors.TabBorder

        if is_current is True or is_hovered is True:
            background_color = _gui_qt_cor_base.QtColors.TabBackgroundCurrent
            text_color = _gui_qt_cor_base.QtColors.Text
        else:
            background_color = _gui_qt_cor_base.QtColors.TabBackground
            text_color = _gui_qt_cor_base.QtColors.TextTemporary

        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        if is_pressed is True:
            offset = 2
            x += offset
            y += offset
            w -= offset
            h -= offset

        r = h
        if is_current is True:
            frm_x, frm_y = x, y
            frm_w, frm_h = w+r, h-1
            border_width = 1
            frame_coords = [
                (f_x, frm_y+frm_h),
                # bottom left, top left, top right, bottom right, ...
                (frm_x, frm_y+frm_h), (frm_x+frm_h, frm_y), (frm_x+frm_w-frm_h, frm_y), (frm_x+frm_w, frm_y+frm_h),
                (f_w, frm_y+frm_h),
            ]
            font_size = 10
        else:
            frm_x, frm_y = x, y+4
            frm_w, frm_h = w+r, h-5
            border_width = 1
            frame_coords = [
                (frm_x, frm_y+frm_h), (frm_x+frm_h, frm_y), (frm_x+frm_w-frm_h, frm_y), (frm_x+frm_w, frm_y+frm_h),
            ]
            font_size = 8

        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        self._set_background_color_(background_color)

        self._draw_path_by_coords_(frame_coords, antialiasing=False)
        # icon
        if icon_name_text is not None:
            icn_w = 16
            icon_coords = [
                # bottom left, top left, top right, bottom right, ...
                (frm_x+frm_w-icn_w, frm_y+frm_h), (frm_x+frm_w-frm_h-icn_w, frm_y+1), (frm_x+frm_w-frm_h, frm_y+1),
                (frm_x+frm_w-1, frm_y+frm_h),
                (frm_x+frm_w-icn_w, frm_y+frm_h),
            ]
            i_r, i_g, i_b = bsc_core.RawTextOpt(icon_name_text).to_rgb_0(s_p=50, v_p=50)
            self._set_border_width_(1)
            self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Transparent)
            icn_bkg_color = QtGui.QColor(i_r, i_g, i_b, a)
            if is_hovered is True:
                self._set_background_color_(icn_bkg_color)
            else:
                self._set_background_color_(i_r, i_g, i_b)
            self._draw_path_by_coords_(icon_coords)
        else:
            icn_w = 0

        if is_pressed is True or is_hovered is True:
            if is_pressed is True:
                act_bkg_color = QtGui.QColor(*gui_core.GuiRgba.LightBlue)
            elif is_hovered is True:
                act_bkg_color = QtGui.QColor(*gui_core.GuiRgba.LightOrange)
            else:
                act_bkg_color = background_color

            act_w, act_h = 32, 2
            self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Transparent)
            self._set_background_color_(act_bkg_color)
            action_rect = QtCore.QRect(
                frm_x+f_h*1.5, f_y+f_h-act_h-1, frm_w-f_h*3-icn_w, act_h
            )
            self.drawRoundedRect(action_rect, act_h/2, act_h/2, QtCore.Qt.AbsoluteSize)
        # text
        if text is not None:
            txt_rect = QtCore.QRect(
                frm_x, frm_y, frm_w-icn_w, frm_h
            )
            text_option = QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter
            self._set_font_(
                _gui_qt_cor_base.GuiQtFont.generate(size=font_size, weight=75)
            )

            self._set_text_color_(text_color)

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
            (frm_x+bsc_w-frm_w*2, frm_y+frm_h), (frm_x+bsc_w-frm_w, frm_y), (frm_x+bsc_w, frm_y),
            (frm_x+bsc_w, frm_y+frm_h)
        ]
        i_r, i_g, i_b = bsc_core.RawTextOpt(text).to_rgb_0(s_p=50, v_p=50)
        self._set_background_color_(i_r, i_g, i_b)
        self._draw_path_by_coords_(coords)
        #
        txt_rect = QtCore.QRect(
            frm_x+bsc_w-frm_w-frm_w*.25, frm_y, frm_w, frm_h
        )
        self._set_font_(
            _gui_qt_cor_base.GuiQtFont.generate(size=int(frm_h*.675), weight=75, italic=True)
        )
        self._set_text_color_(i_r*.75, i_g*.75, i_b*.75)
        self.drawText(
            txt_rect, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
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
        self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Transparent)
        self._set_background_color_(_gui_qt_cor_base.QtBackgroundColors.Dark)
        self._draw_path_by_coords_(coords)

        txt_r = 12
        txt_w, txt_h = txt_r-offset, txt_r-offset
        txt_x, txt_y = x+w-txt_r+offset-2, y+offset+2
        txt_rect = QtCore.QRect(
            txt_x, txt_y, txt_w, txt_h
        )
        self._set_text_color_(_gui_qt_cor_base.QtFontColors.Dark)
        self._set_font_(
            _gui_qt_cor_base.GuiQtFont.generate(size=int(txt_r*.5)-offset, italic=True)
        )
        self.drawText(
            txt_rect, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop,
            text
        )

    def _draw_popup_frame_(
        self, rect, margin, side, shadow_radius, region, border_color, background_color, border_width=1
    ):
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
            path2_.addPolygon(
                QtGui.QPolygonF(
                    [QtCore.QPointF(x1+_s, y1+_s), QtCore.QPointF(x2+_s, y2+_s), QtCore.QPointF(x3+_s, y3+_s)]
                )
            )
        elif region == 1:
            path2.addPolygon(
                QtGui.QPolygonF([QtCore.QPointF(_x1, y1), QtCore.QPointF(_x2, y2), QtCore.QPointF(_x3, y3)])
            )
            path2_.addPolygon(
                QtGui.QPolygonF(
                    [QtCore.QPointF(_x1+_s, y1+_s), QtCore.QPointF(_x2+_s, y2+_s), QtCore.QPointF(_x3+_s, y3+_s)]
                )
            )
        elif region == 2:
            path2.addPolygon(
                QtGui.QPolygonF([QtCore.QPointF(x1, _y1), QtCore.QPointF(x2, _y2), QtCore.QPointF(x3, _y3)])
            )
            path2_.addPolygon(
                QtGui.QPolygonF(
                    [QtCore.QPointF(x1+_s, _y1+_s), QtCore.QPointF(x2+_s, _y2+_s), QtCore.QPointF(x3+_s, _y3+_s)]
                )
            )
        else:
            path2.addPolygon(
                QtGui.QPolygonF([QtCore.QPointF(_x1, _y1), QtCore.QPointF(_x2, _y2), QtCore.QPointF(_x3, _y3)])
            )
            path2_.addPolygon(
                QtGui.QPolygonF(
                    [QtCore.QPointF(_x1+_s, _y1+_s), QtCore.QPointF(_x2+_s, _y2+_s), QtCore.QPointF(_x3+_s, _y3+_s)]
                )
            )
        #
        self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Transparent)
        self._set_background_color_(_gui_qt_cor_base.QtBackgroundColors.Shadow)
        shadow_path = path1_+path2_
        self.drawPath(shadow_path)
        #
        self._set_border_color_(border_color)
        self._set_background_color_(background_color)
        self._set_border_width_(border_width)
        frame_path = path1+path2
        self._set_antialiasing_(False)
        self.drawPath(frame_path)

    def _set_text_color_(self, *args):
        self._set_border_color_(*args)

    def _set_border_color_(self, *args):
        qt_color = _gui_qt_cor_base.GuiQtColor.to_qt_color(*args)
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
        qt_color = _gui_qt_cor_base.GuiQtColor.to_qt_color(*args)
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

    def _set_font_pixel_size_(self, size):
        f = self.font()
        f.setPixelSize(size)
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
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
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
            new_pixmap = _gui_qt_cor_base.GuiQtPixmap._to_gray_(new_pixmap)
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
        frm_r = max(min(r*.5, 128), 32)
        frm_w, frm_h = frm_r, frm_r
        rect = QtCore.QRect(
            x+(w-frm_w)/2, y+(h-frm_h)/2, frm_w, frm_h
        )
        self._draw_icon_file_by_rect_(
            rect=rect, file_path=gui_core.GuiIcon.get(icon_name)
        )

    @classmethod
    def _get_font_test_size_(cls, font, text):
        fmt = QtGui.QFontMetrics(font)
        f_w, f_h = fmt.width(text), fmt.height()
        return f_w, f_h

    def _draw_empty_text_by_rect_(self, rect, text, text_sub=None, draw_drop_icon=False):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        frm_w, frm_h = max(min(w, 200), 100), max(min(h, 40), 20)
        frm_x, frm_y = x+(w-frm_w)/2, y+(h-frm_h)/2
        #
        f_w_t, f_h_t = self._get_font_test_size_(_gui_qt_cor_base.GuiQtFont.generate(size=12, weight=75), text)
        txt_x, txt_y, txt_w, txt_h = bsc_core.RawSizeMtd.fit_to(
            (f_w_t, f_h_t), (frm_w, frm_h)
        )
        text_size = txt_h/2
        text_font = _gui_qt_cor_base.GuiQtFont.generate(size=text_size, weight=75)
        text_sub_font = _gui_qt_cor_base.GuiQtFont.generate(size=10, weight=50, italic=True)
        t_w_n, t_h_n = self._get_font_test_size_(text_font, text)
        self._set_border_color_((31, 31, 31, 255))
        if text_sub:
            txt_s_w, txt_s_h = self._get_font_test_size_(text_sub_font, text)
        else:
            txt_s_w, txt_s_h = 0, 0
        #
        if draw_drop_icon is True:
            icon_rect = QtCore.QRect(
                x+(w-t_w_n)/2-txt_h/2, frm_y+txt_y-txt_s_h, txt_h, txt_h
            )
            self._draw_icon_file_by_rect_(
                rect=icon_rect, file_path=gui_core.GuiIcon.get(
                    'drag-and-drop'
                )
            )
            text_rect = QtCore.QRect(
                x+txt_h/2, frm_y+txt_y-txt_s_h, w, txt_h
            )
        else:
            text_rect = QtCore.QRect(
                x, frm_y+txt_y, w, txt_h
            )
        #
        self._set_font_(text_font)
        self.drawText(
            text_rect,
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            text
        )
        if text_sub:
            sub_text_rect = QtCore.QRect(
                x, frm_y+txt_y+txt_h-txt_s_h, w, txt_s_h
            )
            self._set_font_(text_sub_font)
            self.drawText(
                sub_text_rect,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                text_sub
            )

    def _draw_icon_by_rect_(self, icon, rect, offset):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        rect_ = QtCore.QRect(
            x+offset, y+offset,
            w-offset, h-offset
        )

        pixmap = icon.pixmap(w, h)
        self.drawPixmap(
            rect_,
            pixmap
        )
        self.device()

    def _draw_icon_file_by_rect_(
        self, rect, file_path,
        offset=0, frame_rect=None, is_hovered=False, hover_color=None, is_pressed=False
    ):
        if file_path:
            # draw frame rect
            if frame_rect is not None:
                background_color = self._get_item_background_color_1_by_rect_(
                    frame_rect,
                    is_hovered=is_hovered
                )
                self._draw_frame_by_rect_(
                    frame_rect,
                    border_color=_gui_qt_cor_base.QtBorderColors.Transparent,
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
                    is_pressed=is_pressed,
                )
            else:
                self._draw_image_by_rect_(
                    rect=rect,
                    file_path=file_path,
                    offset=offset,
                    is_hovered=is_hovered,
                    hover_color=hover_color,
                    is_pressed=is_pressed,
                )

    def _draw_image_use_file_path_by_rect_(
        self, rect, file_path,
        offset=0, draw_frame=False, background_color=None, border_color=None, border_radius=0,
        is_hovered=False, is_pressed=False,
    ):
        if file_path:
            if draw_frame is True:
                self._draw_frame_by_rect_(
                    rect=rect,
                    offset=offset,
                    border_color=border_color,
                    background_color=background_color,
                    border_radius=border_radius
                )
            #
            if os.path.isfile(file_path):
                if file_path.endswith('.svg'):
                    self._draw_svg_by_rect_(
                        rect, file_path, offset,
                        is_hovered=is_hovered, is_pressed=is_pressed
                    )
                elif file_path.endswith('.exr'):
                    self._set_exr_image_draw_by_rect_(rect, file_path, offset)
                elif file_path.endswith('.mov'):
                    self._set_mov_image_draw_by_rect_(rect, file_path, offset)
                else:
                    self._draw_image_by_rect_(
                        rect, file_path, offset,
                        cache_resize=True,
                        is_hovered=is_hovered
                    )

    def _draw_pixmap_by_rect_(self, rect, pixmap, offset=0):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        self.drawPixmap(
            rect_,
            pixmap
        )
        #
        self.device()

    def _draw_svg_by_rect_(self, rect, file_path, offset=0, is_hovered=False, hover_color=None, is_pressed=False):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        r_f = QtCore.QRectF(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        svg_render = QtSvg.QSvgRenderer(file_path)
        svg_render.render(self, r_f)
        if is_pressed is True:
            p_over = self._get_svg_rgba_over_(rect_, svg_render, gui_core.GuiRgba.LightBlue)
            self.drawPixmap(
                rect_,
                p_over
            )
        elif is_hovered is True:
            p_over = self._get_svg_rgba_over_(rect_, svg_render, gui_core.GuiRgba.LightOrange)
            self.drawPixmap(
                rect_,
                p_over
            )
        #
        self.device()

    @classmethod
    def _get_svg_rgba_over_(cls, rect, svg_render, rgba, alpha=63, mask_color=None):
        w, h = rect.width(), rect.height()
        i_new = QtGui.QImage(
            w, h, QtGui.QImage.Format_ARGB32
        )
        if mask_color is None:
            mask_color = QtCore.Qt.black
        i_new.fill(mask_color)
        painter = QtGui.QPainter(i_new)
        svg_render.render(painter, QtCore.QRectF(0, 0, w, h))
        painter.end()
        #
        p_mask = QtGui.QPixmap(i_new).createMaskFromColor(mask_color)
        r, g, b, a = rgba
        c = QtGui.QColor(r, g, b, alpha)
        #
        p_over = QtGui.QPixmap(i_new)
        p_over.fill(QtGui.QColor(c.red(), c.green(), c.blue(), alpha))
        p_over.setMask(p_mask)
        return p_over

    @classmethod
    def _get_pixmap_with_rgba_over_(cls, pixmap, rgba, alpha=63):
        w, h = pixmap.width(), pixmap.height()
        image_new = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
        image = pixmap.toImage()
        r, g, b, a = rgba
        p_0, p_1 = (255-alpha)/255.0, alpha/255.0
        for i_x in range(w):
            for i_y in range(h):
                i_c = image.pixelColor(i_x, i_y)
                i_r, i_g, i_b, i_a = i_c.red(), i_c.green(), i_c.blue(), i_c.alpha()
                i_g_c = QtGui.QColor(i_r*p_0+r*p_1, i_g*p_0+g*p_1, i_b*p_0+b*p_1, i_a)
                image_new.setPixel(i_x, i_y, i_g_c.rgba())
        #
        if QT_LOAD_INDEX == 0:
            pixmap_new = pixmap.fromImage(image_new)
            p_mask = cls._get_pixmap_mask_(pixmap)
            pixmap_new.setMask(p_mask)
        else:
            i_alpha = image.alphaChannel()
            image_new.setAlphaChannel(i_alpha)
            pixmap_new = pixmap.fromImage(image_new)
        return pixmap_new

    @classmethod
    def _get_pixmap_mask_(cls, pixmap):
        w, h = pixmap.width(), pixmap.height()
        image_new = QtGui.QImage(
            w*4, h*4, QtGui.QImage.Format_ARGB32
        )
        image_new.fill(QtCore.Qt.black)
        painter = QtGui.QPainter(image_new)
        painter.drawPixmap(QtCore.QRect(0, 0, w*4, h*4), pixmap)
        painter.end()
        image_new = image_new.scaled(
            pixmap.size(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        p = QtGui.QPixmap(image_new)
        # bug: in PyQt5 mask not be a QPixmap, mask a QBitmap
        pixmap_mask = p.createMaskFromColor(QtCore.Qt.black)
        return pixmap_mask

    def _draw_image_by_rect_(
        self, rect, file_path, offset=0, is_hovered=False, hover_color=None, is_pressed=False, cache_resize=False
    ):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        #
        rect_size = rect_.size()
        w, h = rect_size.width(), rect_size.height()
        image = QtGui.QImage(file_path)
        img_scaled = image.scaled(
            rect_size,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        if cache_resize is True:
            if file_path.endswith('.png'):
                tmp_path = bsc_core.StgTmpThumbnailMtd.get_qt_file_path_(file_path, width=max(w, h), ext='.png')
                if bsc_core.StgPathMtd.get_is_exists(tmp_path) is False:
                    bsc_core.StgFileOpt(tmp_path).create_directory()
                    img_scaled.save(tmp_path)
                #
                img_scaled = QtGui.QImage(tmp_path)
        #
        pixmap = QtGui.QPixmap(img_scaled)
        if is_pressed is True:
            pixmap = self._get_pixmap_with_rgba_over_(pixmap, gui_core.GuiRgba.LightBlue, alpha=63)
        elif is_hovered is True:
            pixmap = self._get_pixmap_with_rgba_over_(pixmap, gui_core.GuiRgba.LightOrange, alpha=63)
        #
        self.drawPixmap(
            rect_,
            pixmap
        )
        #
        self.device()

    def _draw_image_data_by_rect_(self, rect, image_data, offset=0, text=None):
        if offset != 0:
            rect_offset = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_offset = rect
        #
        if image_data is not None:
            image = QtGui.QImage()
            image.loadFromData(image_data)
            if image.isNull() is False:
                # draw frame
                self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Icon)
                self._set_background_color_(_gui_qt_cor_base.QtBackgroundColors.Icon)
                self.drawRect(
                    rect_offset
                )
                #
                frm_x, frm_y = rect_offset.x(), rect_offset.y()
                frm_w, frm_h = rect_offset.width(), rect_offset.height()
                img_w, img_h = image.width(), image.height()

                img_rect_x, img_rect_y, img_rect_w, img_rect_h = bsc_core.RawRectMtd.fit_to(
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
        if text is not None and text:
            draw_text = text[0]
        else:
            draw_text = 'N/a'

        w, h = rect.width(), rect.height()
        r = min(w, h)
        txt_size = int(r*.5)
        #
        txt_size = max(txt_size, 1)
        #
        self._set_font_(
            _gui_qt_cor_base.GuiQtFont.generate(size=txt_size)
        )
        #
        background_color, font_color = _gui_qt_cor_base.GuiQtColor.generate_color_args_by_text(text)
        self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Icon)
        self._set_background_color_(background_color)
        self.drawRect(
            rect
        )
        self._set_text_color_(font_color)
        self.drawText(
            rect,
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            draw_text.capitalize()
        )

    def _set_antialiasing_(self, boolean=True):
        self.setRenderHint(self.Antialiasing, boolean)

    def _draw_loading_by_rect_(self, rect, loading_index):
        self._set_border_color_(_gui_qt_cor_base.QtBorderColors.Basic)
        self._draw_alternating_colors_by_rect_(
            rect=rect,
            colors=((0, 0, 0, 63), (0, 0, 0, 0)),
            # border_radius=4,
            running=True
        )
        self._set_font_(_gui_qt_cor_base.QtFonts.Loading)
        self._set_border_color_(_gui_qt_cor_base.QtFontColors.Basic)
        self.drawText(
            rect,
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            'loading .{}'.format('.'*int((loading_index/10)%3))
        )

    def _set_exr_image_draw_by_rect_(self, rect, file_path, offset=0, is_hovered=False):
        thumbnail_file_path = bsc_core.ImgFileOpt(file_path).get_thumbnail()
        self._draw_image_by_rect_(
            rect=rect, file_path=thumbnail_file_path, offset=offset, is_hovered=is_hovered
        )

    def _set_mov_image_draw_by_rect_(self, rect, file_path, offset=0):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
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

    def _set_movie_play_button_draw_by_rect_(
        self, rect, scale=1.0, offset=0, border_width=4, is_hovered=False, is_selected=False, is_actioned=False
    ):
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
        x_, y_ = (width-r_)/2+x, (height-r_)/2+y
        #
        ellipse_rect = QtCore.QRect(x_-4, y_-4, r_+8, r_+8)
        coords = [
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x_, y_), radius=r_, angle=90),
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x_, y_), radius=r_, angle=210),
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x_, y_), radius=r_, angle=330),
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x_, y_), radius=r_, angle=90)
        ]
        #
        self._set_background_color_(_gui_qt_cor_base.QtBackgroundColors.Transparent)
        border_color = self._get_item_border_color_(ellipse_rect, is_hovered, is_selected, is_actioned)
        self._set_border_color_(border_color)
        self._set_border_color_alpha_(127)
        #
        self._set_border_width_(border_width)
        self.drawEllipse(ellipse_rect)
        self._draw_path_by_coords_(coords)

    def _draw_path_by_coords_(self, coords, antialiasing=True):
        path = QtPainterPath()
        path._set_points_add_(coords)
        self._set_antialiasing_(antialiasing)
        self.drawPath(path)
        return path

    def _set_color_icon_draw_(self, rect, color, offset=0):
        r, g, b = color
        border_color = _gui_qt_cor_base.QtBorderColors.Icon
        self._set_border_width_(1)
        self._set_border_color_(border_color)
        self._set_background_color_(r, g, b, 255)
        #
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )

        self.drawRect(rect_)

    def _draw_image_use_text_by_rect_(
        self, rect, text, border_color=None, background_color=None, font_color=None, offset=0, border_radius=0,
        border_width=1, is_hovered=False, is_enable=True, is_pressed=False
    ):
        if offset != 0:
            rect_offset = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_offset = rect

        x, y = rect_offset.x(), rect_offset.y()
        w, h = rect_offset.width(), rect_offset.height()

        frame_rect = QtCore.QRect(
            x, y,
            w, h
        )
        if border_color is not None:
            border_color_ = border_color
        else:
            border_color_ = _gui_qt_cor_base.QtBorderColors.Icon
        #
        if background_color is not None:
            background_color__ = _gui_qt_cor_base.GuiQtColor.to_rgba(background_color)
        else:
            background_color__ = bsc_core.RawTextOpt(text).to_rgb_0(s_p=50, v_p=50)

        background_color_, text_color_ = _gui_qt_cor_base.GuiQtColor.generate_color_args_by_rgb(*background_color__)
        if font_color is not None:
            text_color_ = font_color

        r = min(w, h)

        if border_width == 'auto':
            if r >= 32:
                border_width = 2
            else:
                border_width = 1

        self._set_background_color_(background_color_)
        self._set_border_color_(border_color_)
        self._set_border_width_(border_width)

        b_ = border_width/2
        if border_radius > 0:
            self._set_antialiasing_()
            self.drawRoundedRect(
                frame_rect,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
            if is_pressed:
                self._set_background_color_(
                    47, 179, 255, 63
                )
                self.drawRoundedRect(
                    frame_rect,
                    border_radius, border_radius,
                    QtCore.Qt.AbsoluteSize
                )
            elif is_hovered is True:
                self._set_background_color_(
                    255, 179, 47, 63
                )
                self.drawRoundedRect(
                    frame_rect,
                    border_radius, border_radius,
                    QtCore.Qt.AbsoluteSize
                )
        elif border_radius == -1:
            self._set_antialiasing_()
            border_radius = frame_rect.height()/2
            border_radius_ = b_+border_radius
            self.drawRoundedRect(
                frame_rect,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
            if is_pressed:
                self._set_background_color_(
                    47, 179, 255, 63
                )
                self.drawRoundedRect(
                    frame_rect,
                    border_radius_, border_radius_,
                    QtCore.Qt.AbsoluteSize
                )
            elif is_hovered is True:
                self._set_background_color_(
                    255, 179, 47, 63
                )
                self.drawRoundedRect(
                    frame_rect,
                    border_radius_, border_radius_,
                    QtCore.Qt.AbsoluteSize
                )
        else:
            self._set_antialiasing_(False)
            self.drawRect(frame_rect)
            if is_pressed:
                self._set_background_color_(
                    47, 179, 255, 63
                )
                self.drawRect(frame_rect)
            elif is_hovered is True:
                self._set_background_color_(
                    255, 127, 63, 63
                )
                self.drawRect(frame_rect)

        if r >= 31:
            texts = bsc_core.RawTextMtd.find_words(text)
            if len(texts) > 1:
                txt_size = int(r*.5)
                text_draw = (texts[0][0]+texts[1][0]).upper()
            else:
                txt_size = int(r*.675)
                text_draw = text[:2].capitalize()
        else:
            txt_size = int(r*.675)
            text_draw = text[0].upper()

        txt_size = max(txt_size, 1)

        txt_rect = QtCore.QRect(
            x, y,
            w, h
        )
        self._set_font_(
            _gui_qt_cor_base.GuiQtFont.generate(size=txt_size)
        )
        self._set_text_color_(text_color_)

        self.drawText(
            txt_rect,
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            text_draw
        )

    def _draw_styled_button_use_text_by_rect_(
        self, rect, text, icon_style, background_color=None, offset=0,
        is_hovered=False, is_enable=True, is_pressed=False
    ):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        r_f = QtCore.QRectF(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )

        x, y = rect_.x(), rect_.y()
        w, h = rect_.width(), rect_.height()

        if background_color is not None:
            background_color__ = _gui_qt_cor_base.GuiQtColor.to_rgba(background_color)
        else:
            r_, g_, b_ = bsc_core.RawTextOpt(text).to_rgb_0(s_p=100, v_p=100)
            background_color__ = r_, g_, b_, 255

        icon_file_path = gui_core.GuiIcon.get(icon_style)
        if icon_file_path is None:
            icon_file_path = gui_core.GuiIcon.get('tool_style/tool-style-1')

        svg_render = QtSvg.QSvgRenderer(icon_file_path)
        svg_render.render(self, r_f)
        # over color
        self.setCompositionMode(self.CompositionMode_Multiply)
        p_over_0 = self._get_svg_rgba_over_(
            rect_, svg_render, background_color__,
            alpha=255, mask_color=QtGui.QColor(255, 0, 0, 255)
        )
        self.drawPixmap(
            rect_,
            p_over_0
        )
        self.setCompositionMode(self.CompositionMode_SourceOver)

        if is_pressed is True:
            p_over_1 = self._get_svg_rgba_over_(
                rect_, svg_render, gui_core.GuiRgba.LightBlue,
                alpha=63, mask_color=QtGui.QColor(255, 0, 0, 255)
            )
            self.drawPixmap(
                rect_,
                p_over_1
            )
        elif is_hovered is True:
            p_over_1 = self._get_svg_rgba_over_(
                rect_, svg_render, gui_core.GuiRgba.LightOrange,
                alpha=63, mask_color=QtGui.QColor(255, 0, 0, 255)
            )
            self.drawPixmap(
                rect_,
                p_over_1
            )

        text_color_ = 255, 255, 255, 255

        x_0, y_0 = x, y
        w_0, h_0 = 64.0, 64.0
        c_x, c_y = 10.0, 19.0
        c_w, c_h = 40.0, 30.0
        x_1, y_1 = int(x_0+c_x/w_0*w), int(y_0+c_y/h_0*h)
        w_1, h_1 = int(c_w/w_0*w), int(c_h/h_0*h)

        texts = bsc_core.RawTextMtd.find_words(text)
        txt_size = (h_1*0.75)
        if len(texts) > 1:
            text_draw = (texts[0][0]+texts[1][0]).upper()
        else:
            text_draw = text[:2].capitalize()

        txt_rect = QtCore.QRect(
            x_1+offset, y_1+offset,
            w_1-offset, h_1-offset
        )

        # print x_1, y_1, w_1, h_1

        self._set_font_(
            _gui_qt_cor_base.GuiQtFont.generate(size=txt_size)
        )
        self._set_text_color_(text_color_)

        # self.fillRect(txt_rect, _gui_qt_cor_base.QtColors.Yellow)

        self.drawText(
            txt_rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            text_draw
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

    def _draw_frame_by_rect_(
        self, rect, border_color, background_color, background_style=None, offset=0, border_radius=0,
        border_width=1, border_style=None
    ):
        self._set_border_color_(border_color)
        self._set_background_color_(background_color)
        self._set_border_width_(border_width)
        if border_style is not None:
            self._set_border_style_(border_style)
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
        self._set_background_color_(_gui_qt_cor_base.QtBackgroundColors.Transparent)
        #
        line = QtCore.QLine(
            point_0, point_1
        )
        self.drawLine(line)

    def _set_status_draw_by_rect_(self, rect, color, offset=0, border_radius=0):
        self._set_border_color_(_gui_qt_cor_base.QtBackgroundColors.Transparent)
        #
        if offset != 0:
            rect_ = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_ = rect
        #
        gradient_color = QtGui.QLinearGradient(rect_.topLeft(), rect_.bottomLeft())
        gradient_color.setColorAt(0, _gui_qt_cor_base.GuiQtColor.to_qt_color(color))
        gradient_color.setColorAt(.5, _gui_qt_cor_base.QtBackgroundColors.Transparent)
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
                    rect.x()+offset, rect.y()+offset,
                    rect.width()-offset, rect.height()-offset
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
                _ = float(seq)/float(c)
                i_index = max(min(_, 1), 0)
                i_qt_color = _gui_qt_cor_base.GuiQtColor.to_qt_color(i_color)
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
            x_o = (time_offset%(width*2))
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
            i_qt_color = _gui_qt_cor_base.GuiQtColor.to_qt_color(i_color)
            gradient_color.setColorAt(i_index, i_qt_color)
            gradient_color.setColorAt(i_index+p*.9, i_qt_color)
        return gradient_color

    def _draw_alternating_frame_by_rect_(self, rect, colors, border_radius=0):
        rect_offset = rect
        background_color = self._get_alternating_color_(
            rect, colors, 20
        )
        self._set_border_color_(colors[0])
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

    def _draw_size_bubble_by_rect_(self, rect, orientation):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        if orientation == QtCore.Qt.Horizontal:
            text = str(w)
        elif orientation == QtCore.Qt.Vertical:
            text = str(h)
        else:
            raise TypeError()

        self._set_font_pixel_size_(12)

        w_t, h_t = self.fontMetrics().width(text), self.fontMetrics().height()/2

        w_f, h_f = w_t+4, h_t+4

        self._set_antialiasing_(False)

        self._set_border_color_(
            _gui_qt_cor_base.QtColors.ToolTipBorder
        )
        self._set_background_color_(
            _gui_qt_cor_base.QtColors.ToolTipBackground
        )
        rect_frame = QtCore.QRect(
            x+(w-w_f)/2, y+(h-h_f)/2-1, w_f, h_f
        )
        self.drawRect(
            rect_frame
        )

        self._set_text_color_(
            _gui_qt_cor_base.QtColors.ToolTipText
        )
        rect_text = QtCore.QRect(
            x+(w-w_t)/2-2, y+(h-h_t)/2-2, w_t+4, h_t+4
        )
        self.drawText(
            rect_text,
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            text
        )

    def _draw_alternating_colors_by_rect_(self, rect, colors, offset=0, border_radius=0, border_width=1, running=False):
        if offset != 0:
            rect_offset = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_offset = rect
        #
        self._set_border_color_(colors[0])
        background_color = self._get_alternating_color_(
            rect_offset, colors, 20, int(time.time()*10), running
        )
        #
        self._set_background_color_(background_color)
        self._set_border_width_(border_width)
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

    def _draw_text_by_rect_(
        self, rect, text, font_color=None, font=None, offset=0, text_option=None, word_warp=False, is_hovered=False,
        is_selected=False
    ):
        if font_color is not None:
            self._set_border_color_(font_color)
        else:
            self._set_border_color_(_gui_qt_cor_base.QtFontColors.Basic)
        #
        if is_hovered is True or is_selected is True:
            self._set_border_color_(_gui_qt_cor_base.QtFontColors.Hovered)
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
            text_option_ = QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
        #
        if font is not None:
            self._set_font_(font)
        else:
            self._set_font_(_gui_qt_cor_base.QtFonts.Default)
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
            text_option__.setWrapMode( text_option__.NoWrap)
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
        txt_w = max(ss)+text_size/2
        for seq, (k, v) in enumerate(text_dict.items()):
            i_rect = QtCore.QRect(x, y+seq*(text_height+text_spacing), w, text_height)
            self._set_text_draw_by_rect_use_key_value_(
                rect=i_rect,
                key_text=k,
                value_text=v,
                key_text_width=txt_w,
                key_text_size=text_size, value_text_size=text_size,
                key_text_weight=text_weight, value_text_weight=text_weight,
                key_text_color=font_color, value_text_color=font_color,
            )

    def _set_radar_chart_draw_by_rect_(self, rect, chart_data):
        pass

    def _set_text_draw_by_rect_use_key_value_(
        self, rect, key_text, value_text, key_text_width, key_text_size=8, value_text_size=8, key_text_weight=50,
        value_text_weight=50, key_text_color=None, value_text_color=None, offset=0, is_hovered=False,
        is_selected=False
    ):
        x, y = rect.x()+offset, rect.y()+offset
        w, h = rect.width()-offset, rect.height()-offset
        if w > 0 and h > 0:
            if key_text_color is not None:
                key_color_ = key_text_color
            else:
                key_color_ = _gui_qt_cor_base.QtFontColors.KeyBasic
            #
            if value_text_color is not None:
                value_color_ = value_text_color
            else:
                value_color_ = _gui_qt_cor_base.QtFontColors.ValueBasic
            #
            # if is_hovered is True or is_selected is True:
            #     key_color_ = _gui_qt_cor_base.QtFontColors.KeyHovered
            #     value_color_ = _gui_qt_cor_base.QtFontColors.ValueHovered
            #
            sep_text = ':'
            sep_text_width = key_text_size
            # key
            self._set_text_color_(key_color_)
            key_text_rect = QtCore.QRect(
                x, y, key_text_width, h
            )
            key_text_option = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
            key_text_font = _gui_qt_cor_base.QtFonts.NameKey
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
            sep_text_option = QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
            self.drawText(
                sep_text_rect,
                sep_text_option,
                sep_text,
            )
            # value
            self._set_text_color_(value_color_)
            value_text_rect_f = QtCore.QRectF(
                x+key_text_width+sep_text_width, y, w-sep_text_width-key_text_width, h
            )
            qt_value_text_option = QtGui.QTextOption()
            qt_value_text_option.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            qt_value_text_option.setUseDesignMetrics(True)
            value_text_ = self.fontMetrics().elidedText(
                value_text,
                QtCore.Qt.ElideLeft,
                value_text_rect_f.width(),
                QtCore.Qt.TextShowMnemonic
            )
            value_text_font = _gui_qt_cor_base.QtFonts.NameValue
            value_text_font.setPointSize(value_text_size)
            value_text_font.setWeight(value_text_weight)
            self._set_font_(value_text_font)
            self.drawText(
                value_text_rect_f,
                value_text_,
                qt_value_text_option,
            )

    def set_button_draw(
        self, rect, background_color, border_color, border_radius=4, border_width=1, border_style='solid'
    ):
        self._set_background_color_(background_color)
        self._set_border_color_(border_color)
        #
        p0, p1, p2, p3 = rect.topLeft(), rect.bottomLeft(), rect.bottomRight(), rect.topRight()
        w, h = rect.width(), rect.height()
        cx, cy = p0.x()+w/2, p0.y()+h/2
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
        br0, bb0, bg0, ba0 = min(br*1.25, 255), min(bb*1.25, 255), min(bg*1.25, 255), ba
        br1, bb1, bg1, ba1 = min(br*1.5, 255), min(bb*1.5, 255), min(bg*1.5, 255), ba
        br3, bb3, bg3, ba3 = min(br*.875, 255), min(bb*.875, 255), min(bg*.875, 255), ba
        br4, bb4, bg4, ba4 = min(br*.725, 255), min(bb*.725, 255), min(bg*.725, 255), ba
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
                p = float(a)/float(360)
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
        rect_ = QtCore.QRect(p0.x()+border_width, p0.y()+border_width, w-border_width*2, h-border_width*2)
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
            return _gui_qt_cor_base.QtBackgroundColors.Transparent
        elif conditions == [False, True]:
            return _gui_qt_cor_base.QtBackgroundColors.Actioned
        elif conditions == [True, False]:
            return _gui_qt_cor_base.QtBackgroundColors.Hovered
        elif conditions == [True, True]:
            color_0 = _gui_qt_cor_base.QtBackgroundColors.Hovered
            color_1 = _gui_qt_cor_base.QtBackgroundColors.Actioned
            start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
            color = QtGui.QLinearGradient(start_pos, end_pos)
            color.setColorAt(0, color_0)
            color.setColorAt(1, color_1)
            return color

    @classmethod
    def _get_item_background_color_by_rect_(
        cls, rect, is_hovered=False, is_selected=False, is_actioned=False, default_background_color=None
    ):
        conditions = [is_hovered, is_selected]
        if conditions == [False, False]:
            if default_background_color is not None:
                return default_background_color
            return _gui_qt_cor_base.QtBackgroundColors.Transparent
        elif conditions == [False, True]:
            return _gui_qt_cor_base.QtBackgroundColors.Selected
        elif conditions == [True, False]:
            if is_actioned:
                color_0 = _gui_qt_cor_base.QtBackgroundColors.Hovered
                color_1 = _gui_qt_cor_base.QtBackgroundColors.Actioned
                start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
                color = QtGui.QLinearGradient(start_pos, end_pos)
                color.setColorAt(0, color_0)
                color.setColorAt(1, color_1)
                return color
            return _gui_qt_cor_base.QtBackgroundColors.Hovered
        elif conditions == [True, True]:
            color_0 = _gui_qt_cor_base.QtBackgroundColors.Hovered
            if is_actioned:
                color_1 = _gui_qt_cor_base.QtBackgroundColors.Actioned
            else:
                color_1 = _gui_qt_cor_base.QtBackgroundColors.Selected
            #
            start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
            color = QtGui.QLinearGradient(start_pos, end_pos)
            color.setColorAt(0, color_0)
            color.setColorAt(1, color_1)
            return color

    @classmethod
    def _get_frame_background_color_by_rect_(
        cls, rect, check_is_hovered=False, is_checked=False, press_is_hovered=False, is_pressed=False,
        is_selected=False, delete_is_hovered=False
    ):
        conditions = [check_is_hovered, is_checked, press_is_hovered, is_pressed, is_selected]
        if True not in conditions:
            return _gui_qt_cor_base.QtBackgroundColors.Transparent
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
                (check_index, _gui_qt_cor_base.QtBackgroundColors.CheckHovered),
                (.25, _gui_qt_cor_base.QtBackgroundColors.Checked)
            ]
        elif check_conditions == [True, False]:
            check_args = [
                (check_index, _gui_qt_cor_base.QtBackgroundColors.CheckHovered)
            ]
        elif check_conditions == [False, True]:
            check_args = [
                (check_index, _gui_qt_cor_base.QtBackgroundColors.Checked)
            ]
        #
        if True in check_args:
            pass
        #
        if is_selected is True:
            select_args = [
                (select_index, _gui_qt_cor_base.QtBackgroundColors.Selected)
            ]
        else:
            select_args = []
        #
        if delete_is_hovered is True:
            press_index = .75
        #
        press_conditions = (press_is_hovered, is_pressed)
        press_args = []
        if press_conditions == (True, True):
            press_args = [
                (select_index, _gui_qt_cor_base.QtBackgroundColors.Pressed),
                (press_index, _gui_qt_cor_base.QtBackgroundColors.PressedHovered),
            ]
        elif press_conditions == (True, False):
            press_args = [
                (press_index, _gui_qt_cor_base.QtBackgroundColors.PressedHovered),
            ]
        elif press_conditions == (False, True):
            press_args = [
                (press_index, _gui_qt_cor_base.QtBackgroundColors.Pressed),
            ]
        #
        delete_args = []
        if delete_is_hovered is True:
            delete_args = [
                (1, _gui_qt_cor_base.QtBackgroundColors.DeleteHovered)
            ]
        #
        for i_args in check_args+select_args+press_args+delete_args:
            i_index, i_color = i_args
            color.setColorAt(i_index, i_color)
        return color

    @classmethod
    def _get_item_border_color_(cls, rect, is_hovered=False, is_selected=False, is_actioned=False):
        if is_actioned:
            return _gui_qt_cor_base.QtBackgroundColors.Actioned
        if is_hovered:
            return _gui_qt_cor_base.QtBackgroundColors.Hovered
        elif is_selected:
            return _gui_qt_cor_base.QtBackgroundColors.Selected
        return _gui_qt_cor_base.QtBackgroundColors.White

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
                    [(i_r, i_g, i_b, 96), (i_r, i_g, i_b, 255)][
                        i_total_path.contains(hover_point) or i_text_ellipse.contains(hover_point)]
                )
                self._set_border_color_(i_border_rgba)
                self.drawPath(i_occupy_path)
                #
                self.drawPolyline(i_text_line)
                self.drawEllipse(i_text_ellipse)
                #
                self._set_font_(
                    _gui_qt_cor_base.GuiQtFont.generate()
                )
                #
                self.drawText(i_text_point, i_text)

    def _set_histogram_draw_(
        self, rect, value_array, value_scale, value_offset, label, grid_scale, grid_size, grid_offset, translate,
        current_index, mode
    ):
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
            column_w = grid_w/grid_scale_x
            #
            minimum_h = grid_w/grid_scale_y
            #
            current_x, current_y = None, None
            for i_index, i_value in enumerate(value_array):
                i_color_percent = float(i_value)/float(maximum)
                #
                i_r, i_g, i_b = bsc_core.RawColorMtd.hsv2rgb(140*i_color_percent, 1, 1)
                #
                self._set_background_color_(i_r, i_g, i_b, 255)
                self._set_border_color_(i_r, i_g, i_b, 255)
                #
                i_value_percent = float(i_value)/float(value_scale_y)
                i_pos_x = pos_x+column_w*i_index+grid_offset_x+translate_x+1
                i_pos_y = (height-minimum_h*i_value_percent*grid_scale_y-grid_offset_y+translate_y)
                # filter visible
                if grid_offset_x <= i_pos_x <= width:
                    i_w, i_h = column_w-spacing, (minimum_h*i_value_percent)*grid_scale_y
                    i_rect = QtCore.QRect(
                        i_pos_x, i_pos_y,
                        i_w, i_h
                    )
                    self.drawRect(i_rect)
                    #
                    if i_index == current_index:
                        current_x = i_index+value_offset_x
                        current_y = i_value+value_offset_y
                        #
                        self._set_background_color_(0, 0, 0, 0)
                        self._set_border_color_(223, 223, 223, 255)
                        #
                        selection_rect = QtCore.QRect(
                            i_pos_x, 0,
                            column_w-2, height-grid_offset_y
                        )
                        #
                        self.drawRect(selection_rect)
            #
            if current_x is not None and current_y is not None:
                current_label_rect = QtCore.QRect(
                    grid_offset_x+8, 0+8,
                    width, height
                )
                #
                self._set_border_color_(223, 223, 223, 255)
                self._set_font_(_gui_qt_cor_base.GuiQtFont.generate(size=12, weight=75))
                #
                self.drawText(
                    current_label_rect,
                    QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop,
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
            for i_y in range(height/grid_h):
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
            for i_x in range(width/grid_h):
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

    def _set_grid_mark_draw_(
        self, rect, axis_dir, grid_size, translate, grid_offset, grid_scale, grid_value_offset, grid_border_color,
        grid_value_show_mode
    ):
        def set_branch_draw_fnc_(points, axis_index, scale, value_offset):
            for seq, i_point in enumerate(points):
                if (seq-axis_index)%5 == 0:
                    value = (seq-axis_index)/scale+value_offset
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
        self._set_font_(_gui_qt_cor_base.GuiQtFont.generate(size=6))
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

    def _set_node_frame_draw_by_rect_(
        self, rect, offset=0, border_radius=0, border_width=1, is_hovered=False, is_selected=False,
        is_actioned=False
    ):
        conditions = [is_hovered, is_selected]
        if conditions == [False, False]:
            color = _gui_qt_cor_base.QtBorderColors.Transparent
        elif conditions == [True, False]:
            color = _gui_qt_cor_base.QtBorderColors.Hovered
        elif conditions == [False, True]:
            color = _gui_qt_cor_base.QtBorderColors.Selected
        elif conditions == [True, True]:
            color_0 = _gui_qt_cor_base.QtBackgroundColors.Hovered
            if is_actioned:
                color_1 = _gui_qt_cor_base.QtBackgroundColors.Actioned
            else:
                color_1 = _gui_qt_cor_base.QtBackgroundColors.Selected
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
        self.setBrush(QtGui.QBrush(_gui_qt_cor_base.QtBorderColors.Transparent))

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
            self.drawRoundedRect(
                rect_,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        elif border_radius == -1:
            border_radius = rect_.height()/2
            border_radius_ = b_+border_radius
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
        color_hovered = QtGui.QColor(255, 179, 47, a)
        color_selected = QtGui.QColor(79, 95, 151, a)
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
                start_p, end_p = rect.topLeft(), rect.bottomLeft()
                l_color = QtGui.QLinearGradient(start_p, end_p)
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
            start_p, end_p = rect.topLeft(), rect.bottomLeft()
            l_color = QtGui.QLinearGradient(start_p, end_p)
            l_color.setColorAt(0, color_0)
            l_color.setColorAt(1, color_1)
            return l_color

    def _set_ng_node_input_draw_(self, rect, border_width, offset):
        self._set_border_color_(191, 191, 191, 255)
        self._set_border_width_(border_width)
        self._set_background_color_(63, 255, 127, 255)
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
        self.drawRect(rect_)

    def _set_ng_node_output_draw_(self, rect, border_width, offset):
        self._set_border_color_(191, 191, 191, 255)
        self._set_border_width_(border_width)
        self._set_background_color_(255, 63, 31, 255)
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
        x, y = rect_.x(), rect_.y()
        w, h = rect_.width(), rect_.height()
        #
        r = h
        coords = [
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x, y), radius=r, angle=90),
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x, y), radius=r, angle=210),
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x, y), radius=r, angle=330),
            gui_core.GuiEllipse2d.get_coord_at_angle(start=(x, y), radius=r, angle=90)
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

    def _set_ng_node_frame_head_draw_(
            self, rect, border_color, border_width, border_radius, is_hovered=False, is_selected=False,
            is_actioned=False
    ):
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
        w_0, h_0 = w, h-border_radius-border_width
        x_1, y_1 = x, y+border_radius+border_width
        w_1, h_1 = w, h-border_radius-border_width
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
        self.drawPath(path_0+path_1)


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

            painter._set_font_(_gui_qt_cor_base.GuiQtFont.generate(g_h*.8))

            i_t_r, i_t_g, i_t_b = bsc_core.RawColorMtd.get_complementary_rgb(*i_background_rgb)
            i_t_a = QtGui.qGray(i_t_r, i_t_g, i_t_b)
            if i_t_a >= 127:
                i_t_r_ = 223
            else:
                i_t_r_ = 63
            #
            i_t_r__ = QtGui.QColor(i_t_r_, i_t_r_, i_t_r_)

            i_text_option = QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter

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
