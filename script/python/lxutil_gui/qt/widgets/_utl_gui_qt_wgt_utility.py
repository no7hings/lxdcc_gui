# coding=utf-8
import collections

import os

import functools

from lxbasic import bsc_configure

from lxbasic.objects import bsc_obj_abs

from lxutil_gui.qt import utl_gui_qt_abstract

from lxutil_gui.qt.utl_gui_qt_core import *

import lxutil.methods as utl_methods

from lxutil_gui import utl_gui_core


class QtItemDelegate(QtWidgets.QItemDelegate):
    def sizeHint(self, option, index):
        size = super(QtItemDelegate, self).sizeHint(option, index)
        size.setHeight(utl_configure.GuiSize.item_height)
        return size


class QtWidget(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtStatusDef
):
    def __init__(self, *args, **kwargs):
        super(QtWidget, self).__init__(*args, **kwargs)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        #
        self.setAutoFillBackground(True)
        #
        self._set_status_def_init_()

    def _set_wgt_update_draw_(self):
        self.update()

    def paintEvent(self, event):
        if self._get_is_status_enable_() is True:
            painter = QtPainter(self)
            #
            if self._status in [
                bsc_configure.GuiStatus.Error
            ]:
                pox_x, pos_y = 0, 0
                width, height = self.width(), self.height()
                frame_rect = QtCore.QRect(
                    pox_x, pos_y, width, height
                )
                #
                painter._set_frame_draw_by_rect_(
                    frame_rect,
                    border_color=(255, 0, 63, 255),
                    background_color=(0, 0, 0, 0),
                    border_width=2,
                    border_radius=2
                )
            elif self._status in [
                bsc_configure.GuiStatus.Warning
            ]:
                pox_x, pos_y = 0, 0
                width, height = self.width(), self.height()
                frame_rect = QtCore.QRect(
                    pox_x, pos_y, width, height
                )
                #
                painter._set_frame_draw_by_rect_(
                    frame_rect,
                    border_color=(255, 255, 63, 255),
                    background_color=(0, 0, 0, 0),
                    border_width=2,
                    border_radius=2
                )
            elif self._status in [
                bsc_configure.GuiStatus.Correct
            ]:
                pox_x, pos_y = 0, 0
                width, height = self.width(), self.height()
                frame_rect = QtCore.QRect(
                    pox_x, pos_y, width, height
                )
                #
                painter._set_frame_draw_by_rect_(
                    frame_rect,
                    border_color=(63, 255, 127, 255),
                    background_color=(0, 0, 0, 0),
                    border_width=2,
                    border_radius=2
                )


class _QtLine(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef
):
    def __init__(self, *args, **kwargs):
        super(_QtLine, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._set_frame_def_init_()

        self._frame_border_color = 95, 95, 95, 255
        self._frame_background_color = 0, 0, 0, 0

    def _set_wgt_update_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = QtPainter(self)

        x, y = 0, 0
        w, h = self.width(), self.height()
        rect = QtCore.QRect(x, y, w, h)
        painter._set_line_draw_by_rect_(
            rect,
            self._frame_border_color,
            self._frame_background_color
        )


class _QtTranslucentWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtTranslucentWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


class QtFrame(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(QtFrame, self).__init__(*args, **kwargs)


class QtPainterPath(QtGui.QPainterPath):
    def __init__(self, *args):
        super(QtPainterPath, self).__init__(*args)
        self.setFillRule(QtCore.Qt.WindingFill)
    #
    def _set_points_add_(self, points):
        points_ = [QtCore.QPointF(x, y) for x, y in points]
        self.addPolygon(QtGui.QPolygonF(points_))


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

    def _set_popup_frame_draw_(self, rect, margin, side, shadow_radius, region, border_color, background_color):
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
        self._set_border_color_(0, 0, 0, 64)
        self._set_background_color_(0, 0, 0, 64)
        shadowPath = path1_+path2_
        self.drawPath(shadowPath)
        #
        self._set_border_color_(border_color)
        self._set_background_color_(background_color)
        framePath = path1+path2
        self.drawPath(framePath)

    def _set_font_color_(self, *args):
        self._set_border_color_(*args)

    def _set_border_color_(self, *args):
        qt_color = Color._get_qt_color_(*args)
        pen = QtGui.QPen(qt_color)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
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

    def _set_file_icon_draw_by_rect_(self, rect, file_path, offset=0):
        if file_path:
            if file_path.endswith('.svg'):
                self._set_svg_image_draw_by_rect_(rect, file_path, offset=offset)
            else:
                if offset != 0:
                    rect_ = QtCore.QRect(
                        rect.x()+offset, rect.y()+offset,
                        rect.width()-offset, rect.height()-offset
                    )
                else:
                    rect_ = rect
                #
                rect_size = rect.size()
                image = QtGui.QImage(file_path)
                new_image = image.scaled(
                    rect_size,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )
                pixmap = QtGui.QPixmap(new_image)
                self.drawPixmap(
                    rect_,
                    pixmap
                )
                #
                self.device()

    def _set_any_image_draw_by_rect_(self, rect, file_path, offset=0):
        if file_path:
            if os.path.isfile(file_path):
                if file_path.endswith('.svg'):
                    self._set_svg_image_draw_by_rect_(rect, file_path, offset)
                elif file_path.endswith('.exr'):
                    self._set_exr_image_draw_by_rect_(rect, file_path, offset)
                elif file_path.endswith('.mov'):
                    self._set_mov_image_draw_by_rect_(rect, file_path, offset)
                else:
                    self._set_image_draw_by_rect_(rect, file_path, offset)

    def _set_image_draw_by_rect_(self, rect, file_path, offset):
        if offset != 0:
            rect_ = QtCore.QRect(
                rect.x() + offset, rect.y() + offset,
                rect.width() - offset, rect.height() - offset
            )
        else:
            rect_ = rect
        #
        rect_size = rect_.size()
        image = QtGui.QImage(file_path)
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

    def _set_antialiasing_(self):
        self.setRenderHint(self.Antialiasing)

    def _set_loading_draw_by_rect_(self, rect, loading_index):
        self.setRenderHint(self.Antialiasing)
        self._set_border_color_(QtBackgroundColor.ItemLoading)
        self._set_background_color_(QtBackgroundColor.ItemLoading)
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
        self._set_border_color_(QtFontColor.Basic)
        self.drawText(
            process_frame,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            'loading .{}'.format('.'*(loading_index % 3))
        )

    def _set_svg_image_draw_by_rect_(self, rect, file_path, offset=0):
        rectF = QtCore.QRectF(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        svg_render = QtSvg.QSvgRenderer(file_path)
        svg_render.render(self, rectF)
        #
        self.device()

    def _set_exr_image_draw_by_rect_(self, rect, file_path, offset=0):
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )
        #
        thumbnail_file_path = bsc_core.ImageOpt(file_path).get_thumbnail()
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
        thumbnail_file_path = bsc_core.VedioOpt(file_path).get_thumbnail()
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
        self._set_background_color_(QtBackgroundColor.Transparent)
        border_color = self._get_item_border_color_(ellipse_rect, is_hovered, is_selected, is_actioned)
        self._set_border_color_(border_color)
        self._set_border_color_alpha_(127)
        #
        self._set_border_width_(border_width)
        self.setRenderHint(self.Antialiasing)
        self.drawEllipse(ellipse_rect)
        self._set_path_draw_by_coords_(points)

    def _set_path_draw_by_coords_(self, points):
        path = QtPainterPath()
        path._set_points_add_(points)
        self.drawPath(path)
        return path

    def _set_color_icon_draw_(self, rect, color, offset=0):
        r, g, b = color
        border_color = QtBorderColor.Icon
        self._set_border_width_(1)
        self._set_border_color_(border_color)
        self._set_background_color_(r, g, b, 255)
        #
        rect_ = QtCore.QRect(
            rect.x()+offset, rect.y()+offset,
            rect.width()-offset, rect.height()-offset
        )

        self.drawRect(rect_)

    def _set_icon_name_text_draw_by_rect_(self, rect, text, border_color=None, background_color=None, text_color=None, offset=0, border_radius=0, border_width=1, is_hovered=False, is_enable=True):
        self.setRenderHint(self.Antialiasing)
        #
        x, y = rect.x()+offset, rect.y()+offset
        w, h = rect.width()-offset, rect.height()-offset
        #
        frame_rect = QtCore.QRect(
            x, y,
            w, h
        )
        #
        if is_hovered is True:
            border_color = QtBorderColor.IconHovered
        else:
            border_color = QtBorderColor.Icon
        #
        self._set_border_color_(border_color)
        self._set_border_width_(1)
        #
        if background_color is not None:
            background_color_ = background_color
            # background_qt_color_ = Color._get_qt_color_(background_color_)
            text_color_ = QtFontColor.Basic
        else:
            background_color_ = bsc_core.TextOpt(text).to_rgb()
            t_r, t_g, t_b = bsc_core.ColorMtd.get_complementary_rgb(*background_color_)
            t_r = QtGui.qGray(t_r, t_g, t_b)
            if t_r >= 127:
                t_r_1 = 223
            else:
                t_r_1 = 63
            text_color_ = QtGui.QColor(t_r_1, t_r_1, t_r_1)

        if text_color is not None:
            text_color_ = text_color
        #
        self._set_background_color_(background_color_)
        self._set_border_width_(border_width)
        #
        b_ = border_width / 2
        if border_radius > 0:
            border_radius_ = b_+border_radius
            self.setRenderHint(self.Antialiasing)
            self.drawRoundedRect(
                frame_rect,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        elif border_radius == -1:
            border_radius = frame_rect.height()/2
            border_radius_ = b_+border_radius
            self.setRenderHint(self.Antialiasing)
            self.drawRoundedRect(
                frame_rect,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self.drawRect(frame_rect)
        #
        self._set_border_color_(text_color_)
        # self._set_border_width_(border_width)
        #
        r = min(w, h)
        t_f_s = int(r*.675)
        t_o = 0
        text_rect_0 = QtCore.QRect(
            x+(w-t_f_s)/2+t_o, y+(h-t_f_s)/2,
            t_f_s, t_f_s
        )
        #
        t_f_s = max(t_f_s, 1)
        #
        self._set_font_(
            get_font(size=t_f_s, italic=True)
        )
        self.drawText(
            text_rect_0,
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            str(text[0]).capitalize()
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

    def _set_frame_draw_by_rect_(self, rect, border_color, background_color, background_style=None, offset=0, border_radius=0, border_width=1):
        self.setRenderHint(self.Antialiasing)
        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        self._set_background_color_(background_color)
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
            self.setRenderHint(self.Antialiasing)
            self.drawRoundedRect(
                rect_,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        elif border_radius == -1:
            border_radius = rect_.height()/2
            border_radius_ = b_+border_radius
            self.setRenderHint(self.Antialiasing)
            self.drawRoundedRect(
                rect_,
                border_radius_, border_radius_,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self.drawRect(rect_)

    def _set_line_draw_by_rect_(self, rect, border_color, background_color, border_width=1):
        self._set_border_color_(border_color)
        self._set_border_width_(border_width)
        self._set_background_color_(background_color)
        #
        line = QtCore.QLine(
            rect.topLeft(), rect.bottomLeft()
        )
        self.drawLine(line)

    def _set_status_draw_by_rect_(self, rect, color, offset=0, border_radius=0):
        self._set_border_color_(QtBackgroundColor.Transparent)
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
        gradient_color.setColorAt(.75, QtBackgroundColor.Transparent)
        self._set_background_color_(gradient_color)
        #
        if border_radius > 0:
            self.setRenderHint(self.Antialiasing)
            self.drawRoundedRect(
                rect_,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
        else:
            self.drawRect(rect_)

    def _set_elements_status_draw_by_rect_(self, rect, colors, offset=0, border_radius=0):
        if colors:
            if offset != 0:
                rect_ = QtCore.QRect(
                    rect.x() + offset, rect.y() + offset,
                    rect.width() - offset, rect.height() - offset
                )
            else:
                rect_ = rect
            #
            gradient_color = QtGui.QLinearGradient(rect_.topLeft(), rect_.topRight())
            c = len(colors)
            for seq, color in enumerate(colors):
                _ = float(seq) / float(c)
                index = max(min(_, 1), 0)
                gradient_color.setColorAt(index, self._get_qt_color_(color))
            #
            self._set_background_color_(gradient_color)
            #
            if border_radius > 0:
                self.setRenderHint(self.Antialiasing)
                self.drawRoundedRect(
                    rect_,
                    border_radius, border_radius,
                    QtCore.Qt.AbsoluteSize
                )
            else:
                self.drawRect(rect_)

    def _set_text_draw_by_rect_(self, rect, text, font_color=None, font=None, offset=0, text_option=None, word_warp=False, is_hovered=False, is_selected=False):
        if font_color is not None:
            self._set_border_color_(font_color)
        else:
            self._set_border_color_(QtFontColor.Basic)
        #
        if is_hovered is True or is_selected is True:
            self._set_border_color_(QtFontColor.Hovered)
        #
        if offset != 0:
            rect_ = QtCore.QRect(
                rect.x()+offset, rect.y()+offset,
                rect.width()-offset, rect.height()-offset
            )
        else:
            rect_ = rect
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
            text_ = self.fontMetrics().elidedText(
                text,
                QtCore.Qt.ElideLeft,
                rect.width(),
                QtCore.Qt.TextShowMnemonic
            )
        #
        rect_f_ = QtCore.QRectF(
            rect_.x(), rect_.y(),
            rect_.width(), rect_.height()
        )
        self.drawText(
            rect_f_,
            text_,
            text_option__,
        )

    def _set_text_draw_by_rect_use_key_value_(self, rect, key_text, value_text, key_text_width, key_color=None, value_color=None, offset=0, is_hovered=False, is_selected=False):
        if key_color is not None:
            key_color_ = key_color
        else:
            key_color_ = QtFontColor.KeyBasic
        #
        if value_color is not None:
            value_color_ = value_color
        else:
            value_color_ = QtFontColor.ValueBasic
        #
        if is_hovered is True or is_selected is True:
            key_color_ = QtFontColor.KeyHovered
            value_color_ = QtFontColor.ValueHovered
        #
        sep_text = ':'
        sep_text_width = 8
        #
        x, y = rect.x() + offset, rect.y() + offset
        w, h = rect.width() - offset, rect.height() - offset
        # key
        self._set_font_color_(key_color_)
        key_text_rect = QtCore.QRect(
            x, y, key_text_width, h
        )
        key_text_option = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        self._set_font_(Font.NameTextKey)
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
        self._set_font_(Font.NameTextValue)
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
        condition = [is_hovered, is_actioned]
        if condition == [False, False]:
            return QtBackgroundColor.Transparent
        elif condition == [False, True]:
            return QtBackgroundColor.Actioned
        elif condition == [True, False]:
            return QtBackgroundColor.Hovered
        elif condition == [True, True]:
            color_0 = QtBackgroundColor.Hovered
            color_1 = QtBackgroundColor.Actioned
            start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
            color = QtGui.QLinearGradient(start_pos, end_pos)
            color.setColorAt(0, color_0)
            color.setColorAt(1, color_1)
            return color
    @classmethod
    def _get_item_background_color_by_rect_(cls, rect, is_hovered=False, is_selected=False, is_actioned=False, default_background_color=None):
        condition = [is_hovered, is_selected]
        if condition == [False, False]:
            if default_background_color is not None:
                return default_background_color
            return QtBackgroundColor.Transparent
        elif condition == [False, True]:
            return QtBackgroundColor.Selected
        elif condition == [True, False]:
            if is_actioned:
                color_0 = QtBackgroundColor.Hovered
                color_1 = QtBackgroundColor.Actioned
                start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
                color = QtGui.QLinearGradient(start_pos, end_pos)
                color.setColorAt(0, color_0)
                color.setColorAt(1, color_1)
                return color
            return QtBackgroundColor.Hovered
        elif condition == [True, True]:
            color_0 = QtBackgroundColor.Hovered
            if is_actioned:
                color_1 = QtBackgroundColor.Actioned
            else:
                color_1 = QtBackgroundColor.Selected
            #
            start_pos, end_pos = rect.topLeft(), rect.bottomLeft()
            color = QtGui.QLinearGradient(start_pos, end_pos)
            color.setColorAt(0, color_0)
            color.setColorAt(1, color_1)
            return color
    @classmethod
    def _get_item_border_color_(cls, rect, is_hovered=False, is_selected=False, is_actioned=False):
        if is_actioned:
            return QtBackgroundColor.Actioned
        if is_hovered:
            return QtBackgroundColor.Hovered
        elif is_selected:
            return QtBackgroundColor.Selected
        return QtBackgroundColor.White

    def _set_sector_chart_draw_(self, chart_draw_data, background_color, border_color, hover_point):
        if chart_draw_data is not None:
            basic_data = chart_draw_data['basic']
            for i in basic_data:
                (
                    i_background_rgba, i_border_rgba,
                    i_total_path, i_occupy_path,
                    i_text_point, i_text_line, i_text_ellipse, i_text
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
                i_r, i_g, i_b = bsc_core.ColorMtd.hsv2rgb(140 * i_color_percent, 1, 1)
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
                        bsc_core.IntegerMtd.get_prettify_(current_y, mode=mode)
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
                    text = bsc_core.IntegerMtd.get_prettify_(
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

    def _set_tab_button_draw_(self, rect, name_text, icon_name_text=None, border_width=1, offset=0, is_hovered=False, is_current=False):
        self._set_border_color_(47, 47, 47, 255)
        self._set_border_width_(border_width)
        a = 255
        if is_current:
            color = QtGui.QColor(63, 63, 63, a)
        else:
            color = QtGui.QColor(95, 95, 95, a)
        #
        if is_hovered is True:
            color_hovered = QtGui.QColor(127, 127, 127, a)
        else:
            color_hovered = color
        #
        start_coord, end_coord = rect.topLeft(), rect.bottomLeft()
        l_color = QtGui.QLinearGradient(start_coord, end_coord)
        l_color.setColorAt(0, color_hovered)
        l_color.setColorAt(0.5, color)
        self._set_background_color_(l_color)
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
        r = h
        s = 4
        x_0, y_0 = x, y+2
        w_0, h_0 = w+r, h-2

        if is_current is True:
            coords = [
                (x_0, y_0 + h_0), (x_0 + h_0, y_0), (x_0 + w_0 - h_0, y_0), (x_0 + w_0, y_0 + h_0), (x_0, y_0 + h_0)
            ]
        else:
            coords = [
                (x_0, y_0 + h_0), (x_0 + h_0, y_0), (x_0 + w_0 - h_0, y_0), (x_0 + w_0, y_0 + h_0), (x_0, y_0 + h_0)
            ]
        #
        self._set_path_draw_by_coords_(coords)
        i_f_x, i_f_y = x_0+r, y_0
        i_f_w, i_f_h = h_0, h_0
        i_w, i_h = 12, 12
        t_x = i_f_x+s
        t_w = w
        if icon_name_text is not None:
            icon_rect = QtCore.QRect(
                i_f_x+s, i_f_y+(i_f_h-i_h)/2, i_w, i_h
            )
            t_x += i_w+s
            t_w -= i_f_w

            self._set_icon_name_text_draw_by_rect_(
                icon_rect,
                icon_name_text,
                border_radius=i_h/2
            )
        #
        if name_text is not None:
            text_rect = QtCore.QRect(
                t_x, y_0, t_w, h_0
            )
            text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
            self._set_font_(
                get_font(size=10)
            )
            self._set_font_color_(255, 255, 255, 255)
            self.drawText(
                text_rect,
                text_option,
                name_text,
            )


class QtNGPainter(QtPainter):
    def __init__(self, *args, **kwargs):
        super(QtNGPainter, self).__init__(*args, **kwargs)
    @classmethod
    def _get_ng_node_background_color_(cls, rect, is_hovered=False, is_selected=False, is_actioned=False):
        condition = [is_hovered, is_selected]
        a = 255
        color_hovered = QtGui.QColor(255, 127, 63, a)
        color_selected = QtGui.QColor(63, 127, 255, a)
        color_actioned = QtGui.QColor(63, 255, 127, a)
        color = QtGui.QColor(191, 191, 191, a)
        if condition == [False, False]:
            return color
        elif condition == [False, True]:
            return color_selected
        elif condition == [True, False]:
            if is_actioned:
                color_0 = color_hovered
                color_1 = color_actioned
                start_coord, end_coord = rect.topLeft(), rect.bottomLeft()
                l_color = QtGui.QLinearGradient(start_coord, end_coord)
                l_color.setColorAt(0, color_0)
                l_color.setColorAt(1, color_1)
                return l_color
            return color_hovered
        elif condition == [True, True]:
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
        self.setRenderHint(self.Antialiasing)
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
        self.setRenderHint(self.Antialiasing)
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
        self._set_path_draw_by_coords_(coords)

    def _set_ng_node_resize_button_draw_(self, rect, border_width, mode, is_current, is_hovered):
        self.setRenderHint(self.Antialiasing)
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
        self.setRenderHint(self.Antialiasing)
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
        self.setRenderHint(self.Antialiasing)
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


class QtIconButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(QtIconButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)
        self.setMaximumSize(20, 20)
        self.setMinimumSize(20, 20)
        #
        self._icon_file_path = None
        self._color_icon_rgb = None
        #
        self._file_icon_size = 16, 16
        self._color_icon_size = 8, 8
        self._frame_size = 20, 20
        self._is_hovered = False
        #
        self.installEventFilter(self)
        #
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._menu_raw = []

    def _set_menu_raw_(self, menu_raw):
        self._menu_raw = menu_raw

    def _get_menu_raw_(self):
        return self._menu_raw

    def _set_menu_show_(self):
        menu_raw = self._get_menu_raw_()
        if menu_raw:
            qt_menu = QtMenu(self)
            qt_menu._set_menu_raw_(menu_raw)
            qt_menu._set_show_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._is_hovered = False
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._is_hovered = True
                self._set_menu_show_()
                self.update()
        return False

    def paintEvent(self, event):
        w, h = self.width(), self.height()
        f_w, f_h = self._frame_size
        i_w, i_h = self._file_icon_size
        painter = QtPainter(self)
        #
        f_x, f_y = (w-i_w) / 2, (h-i_h) / 2
        #
        bkg_rect = QtCore.QRect(1, 1, w-1, h-1)
        bkg_color = [QtBackgroundColor.Transparent, QtBackgroundColor.Hovered][self._is_hovered]
        painter._set_frame_draw_by_rect_(
            bkg_rect,
            border_color=bkg_color,
            background_color=bkg_color,
            border_radius=4
        )
        if self._icon_file_path is not None:
            icn = QtCore.QRect(f_x, f_y, i_w, i_h)
            painter._set_svg_image_draw_by_rect_(icn, self._icon_file_path)
        elif self._color_icon_rgb is not None:
            pass


class QtPressButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(QtPressButton, self).__init__(*args, **kwargs)
        self.setFont(Font.NAME)
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setAutoFillBackground(True)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        # self.setFlat(True)


class QtMenuBar(QtWidgets.QMenuBar):
    def __init__(self, *args, **kwargs):
        super(QtMenuBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setAutoFillBackground(True)
        #
        self.setFont(Font.NAME)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QMenuBar')
        )


class QtMenu(QtWidgets.QMenu):
    def __init__(self, *args, **kwargs):
        super(QtMenu, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setAutoFillBackground(True)
        #
        self.setFont(Font.NAME)
        #
        # if bsc_core.SystemMtd.get_is_windows():
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QMenu')
        )
    @classmethod
    def _set_cmd_run_(cls, cmd_str):
        exec cmd_str
    @classmethod
    def _set_action_add_(cls, qt_menu, action_args):
        def set_disable_fnc_(qt_widget_action_):
            qt_widget_action_.setFont(Font.disable)
            qt_widget_action_.setDisabled(True)
        #
        if action_args:
            if len(action_args) == 1:
                s = qt_menu.addSeparator()
                s.setFont(Font.SEPARATOR)
                s.setText(action_args[0])
            elif len(action_args) >= 3:
                name, icon_name, method_args = action_args[:3]
                qt_widget_action = QtWidgetAction(qt_menu)
                qt_widget_action.setFont(Font.NAME)
                qt_menu.addAction(qt_widget_action)
                #
                qt_widget_action.setText(name)
                if icon_name is not None:
                    if isinstance(icon_name, (str, unicode)):
                        if icon_name:
                            qt_widget_action.setIcon(QtUtilMtd.get_qt_icon(icon_name))
                        else:
                            qt_widget_action.setIcon(
                                QtUtilMtd.get_name_text_icon_(name, background_color=(64, 64, 64))
                            )
                else:
                    qt_widget_action.setIcon(
                        QtUtilMtd.get_name_text_icon_(name, background_color=(64, 64, 64))
                    )
                #
                if method_args is None:
                    set_disable_fnc_(qt_widget_action)
                else:
                    if isinstance(method_args, (types.FunctionType, types.MethodType, functools.partial)):
                        fnc = method_args
                        qt_widget_action.triggered.connect(fnc)
                    elif isinstance(method_args, (str, unicode)):
                        cmd_str = method_args
                        qt_widget_action.triggered.connect(lambda *args, **kwargs: cls._set_cmd_run_(cmd_str))
                    elif isinstance(method_args, (tuple, list)):
                        if len(method_args) == 2:
                            enable_fnc, fnc = method_args
                            if isinstance(enable_fnc, (types.FunctionType, types.MethodType)):
                                enable = enable_fnc()
                            else:
                                enable = enable_fnc
                            #
                            qt_widget_action.setCheckable(True)
                            if isinstance(enable, bool):
                                qt_widget_action.setChecked(enable_fnc())
                                qt_widget_action.toggled.connect(fnc)
                            else:
                                set_disable_fnc_(qt_widget_action)
                        elif len(method_args) == 3:
                            enable_fnc, fnc, _ = method_args
                            if isinstance(enable_fnc, (types.FunctionType, types.MethodType)):
                                enable = enable_fnc()
                            else:
                                enable = enable_fnc
                            #
                            if isinstance(enable, bool):
                                if enable is False:
                                    qt_widget_action.setDisabled(True)
                                    qt_widget_action.setFont(Font.disable)
                                else:
                                    qt_widget_action.setDisabled(False)
                                    qt_widget_action.setFont(Font.NAME)
                            #
                            qt_widget_action.triggered.connect(fnc)
                #
                if len(action_args) >= 4:
                    shortcut = action_args[3]
                    qt_widget_action.setShortcut(shortcut)
                    qt_widget_action.setShortcutContext(QtCore.Qt.WidgetShortcut)
        else:
            qt_menu.addSeparator()
    @classmethod
    def _set_color_icon_rgb_(cls, qt_widget, color):
        icon = QtGui.QIcon()
        f_w, f_h = 13, 13
        c_w, c_h = 12, 12
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = QtPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            QtCore.Qt.white
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        icon_rect = QtCore.QRect(
            x+(w-c_w)/2, y+(h-c_h)/2,
            c_w, c_h
        )
        painter._set_color_icon_draw_(
            icon_rect, color
        )
        painter.end()
        # painter.device()
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        qt_widget.setIcon(icon)

    def _set_menu_raw_(self, menu_raw):
        """
        :param menu_raw: [
            ('Label', 'icon_name', fnc),
            (),
            [
                'Label', 'icon_name', [
                    ()
                ]
            ]
        ]
        :return:
        """
        if menu_raw:
            for i in menu_raw:
                if isinstance(i, tuple):
                    self._set_action_add_(self, i)
                # sub menu
                elif isinstance(i, list):
                    i_name, i_icon_name, sub_menu_raws = i
                    qt_action_item = self.addAction(i_name)
                    if i_icon_name is not None:
                        if isinstance(i_icon_name, (str, unicode)):
                            qt_action_item.setIcon(QtUtilMtd.get_qt_icon(i_icon_name))
                    else:
                        qt_action_item.setIcon(QtUtilMtd.get_name_text_icon_(i_name, background_color=(64, 64, 64)))
                    #
                    sub_menu = self.__class__(self.parent())
                    qt_action_item.setMenu(sub_menu)
                    for j in sub_menu_raws:
                        self._set_action_add_(sub_menu, j)

    def _set_title_text_(self, text):
        # self.setTearOffEnabled(True)
        self.setTitle(text)
        self.setIcon(
            QtGui.QIcon(
                utl_core.Icon.get('menu_h')
            )
        )

    def _set_show_(self):
        self.popup(
            QtGui.QCursor().pos()
        )

    def _set_menu_content_(self, content):
        QtMenuOpt(self).set_create_by_content(content)
        # if isinstance(content, bsc_obj_abs.AbsContent):
        #     keys = content.get_keys(regex='*.properties')
        #     for i_key in keys:
        #         type_ = content.get('{}.type'.format(i_key))
        #         i_content = content.get_content(i_key)
        #         if type_ == 'separator':
        #             self._set_separator_add__(self, i_content)
        #         elif type_ == 'action':
        #             self._set_action_add__(self, i_content)
    @classmethod
    def _set_action_create_by_menu_content_(cls, menu):
        menu.clear()
    @classmethod
    def _set_separator_add__(cls, menu, content):
        name = content.get('name')
        separator = menu.addSeparator()
        separator.setFont(Font.SEPARATOR)
        separator.setText(name)
    @classmethod
    def _set_action_add__(cls, menu, content):
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
            widget_action.triggered.connect(fnc)
        elif isinstance(execute_fnc, (str, unicode)):
            cmd_str = execute_fnc
            widget_action.triggered.connect(lambda *args, **kwargs: cls._set_cmd_run_(cmd_str))


class _QtLabel(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtLabel, self).__init__(*args, **kwargs)
        self._name = None

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._name is not None:
            pass


class QtAction(QtWidgets.QAction):
    def __init__(self, *args, **kwargs):
        super(QtAction, self).__init__(*args, **kwargs)
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        #
        self.setFont(Font.NAME)


class QtLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(QtLabel, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)


class QtScrollArea(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super(QtScrollArea, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWidgetResizable(True)
        widget = QtWidget()
        self.setWidget(widget)
        self._layout = QtVBoxLayout(widget)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(*[0]*4)
        self._layout.setSpacing(Util.LAYOUT_SPACING)
        #
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollArea')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )


class QtThreadDef(object):
    def _set_thread_def_init_(self):
        pass

    def _set_thread_create_(self):
        return QtMethodThread(self)


class QtMainWindow(
    QtWidgets.QMainWindow,
    utl_gui_qt_abstract.AbsQtIconDef,
    QtThreadDef
):
    close_clicked = qt_signal()
    key_escape_pressed = qt_signal()
    size_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtMainWindow, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setAutoFillBackground(True)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setFont(Font.NAME)
        #
        set_shadow(self, radius=2)
        #
        self._set_icon_def_init_()

        self._window_system_tray_icon = None
    #
    def _set_wgt_update_draw_(self):
        self.update()
    #
    def _set_icon_name_text_(self, text):
        self.setWindowIcon(QtUtilMtd.get_name_text_icon_(text))

    def _set_icon_name_(self, icon_name):
        self.setWindowIcon(QtIconMtd.get_by_icon_name(icon_name))

    def _set_window_system_tray_icon_(self, widget):
        self._window_system_tray_icon = widget
    @property
    def lynxi_window(self):
        return True

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if hasattr(event, 'type'):
                if event.type() == QtCore.QEvent.Close:
                    if hasattr(self, 'gui_proxy'):
                        self.gui_proxy.set_window_close()
                        self.hide()
                elif event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_Escape:
                        self.key_escape_pressed.emit()
                elif event.type() == QtCore.QEvent.Resize:
                    self.size_changed.emit()
        return False

    def _set_size_changed_connect_to_(self, fnc):
        self.size_changed.connect(fnc)
    # def close(self):
    #     self.close_clicked.emit()
    #     return super(QtMainWindow, self).close()

    def _set_close_(self):
        self.close()
        self.deleteLater()

    def _set_close_later_(self, time):
        close_timer = QtCore.QTimer(self)
        close_timer.timeout.connect(self._set_close_)
        close_timer.start(time)


class QtDialog(
    QtWidgets.QDialog,
    utl_gui_qt_abstract._QtStatusDef,
    QtThreadDef
):
    size_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtDialog, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setWindowModality(
            QtCore.Qt.ApplicationModal
        )
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        #
        self.setFont(Font.NAME)
        #
        set_shadow(self, radius=2)
        #
        self.installEventFilter(self)
        #
        self._set_status_def_init_()
    #
    def _set_wgt_update_draw_(self):
        self.update()
    #
    def _set_icon_name_text_(self, text):
        self.setWindowIcon(
            QtUtilMtd.get_name_text_icon_(text, background_color=(64, 64, 64))
        )

    def _set_yes_run_(self):
        print 'you choose yes'
        self.accept()

    def _set_no_run_(self):
        print 'you choose no'
        self.reject()

    def _set_cancel_run_(self):
        print 'you choose cancel'
        self.reject()

    def _get_is_yes_(self):
        return bool(self.result())

    def _set_close_(self):
        self.close()
        self.deleteLater()

    def _set_close_later_(self, time):
        close_timer = QtCore.QTimer(self)
        close_timer.timeout.connect(self._set_close_)
        close_timer.start(time)

    def _set_size_changed_connect_to_(self, fnc):
        self.size_changed.connect(fnc)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if hasattr(event, 'type'):
                if event.type() == QtCore.QEvent.Close:
                    if hasattr(self, 'gui_proxy'):
                        self.gui_proxy.set_window_close()
                        self.hide()
                elif event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_Escape:
                        self.key_escape_pressed.emit()
                elif event.type() == QtCore.QEvent.Resize:
                    self.size_changed.emit()
        return False


class QtCommonStyle(QtWidgets.QCommonStyle):
    def __init__(self):
        super(QtCommonStyle, self).__init__()

    def drawPrimitive(self, *args):
        element, option, painter, widget = args
        if element == QtWidgets.QStyle.PE_FrameFocusRect:
            return
        elif element == QtWidgets.QStyle.PE_IndicatorBranch:
            return
        else:
            QtWidgets.QCommonStyle().drawPrimitive(element, option, painter, widget)


class _QtSpacer(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtSpacer, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)


class QtStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(QtStyledItemDelegate, self).__init__(parent)
        self._file_icon_size = QtCore.QSize(20, 20)

    def paint(self, painter, option, index):
        _ = index.data(QtCore.Qt.DisplayRole)
        if _:
            user_data = index.data(QtCore.Qt.UserRole)
            if user_data:
                filter_keyword = user_data.get('filter_keyword')
                filter_occurrence = user_data.get('filter_occurrence', False)
                if filter_keyword is not None:
                    content = index.data(QtCore.Qt.DisplayRole)
                    if content:
                        rect = option.rect
                        x, y = rect.x(), rect.y()
                        w, h = rect.width(), rect.height()
                        spans = methods.String.find_spans(content, filter_keyword)
                        if spans:
                            line = QtCore.QLine(
                                x, y+h, x+w, y+h
                            )
                            if filter_occurrence is True:
                                painter.setPen(Color.text_filter_occurrence)
                            else:
                                painter.setPen(Color.text_filter)
                            painter.drawLine(line)

                            # for seq, span in enumerate(spans):
                            #     start, end = span
                            #     b = Color.text_filter
                            #     qt_painter.fillRect(rect, b)
        super(QtStyledItemDelegate, self).paint(painter, option, index)

    def updateEditorGeometry(self, editor, option, index):
        super(QtStyledItemDelegate, self).updateEditorGeometry(editor, option, index)

    def sizeHint(self, option, index):
        size = super(QtStyledItemDelegate, self).sizeHint(option, index)
        size.setHeight(utl_configure.GuiSize.item_height)
        return size


class QtLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(QtLineEdit, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)
        #
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def _set_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())

    def _set_use_as_float_(self):
        self.setValidator(QtGui.QDoubleValidator())

    def _set_value_maximum_(self, value):
        pass

    def _set_value_minimum_(self, value):
        pass

    def _set_value_range_(self, maximum, minimum):
        pass


class QtCheckBox(QtWidgets.QCheckBox):
    def __init__(self, *args, **kwargs):
        super(QtCheckBox, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)


class QtRadioButton(QtWidgets.QRadioButton):
    def __init__(self, *args, **kwargs):
        super(QtRadioButton, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)


class QtComboBox(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super(QtComboBox, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setItemDelegate(QtStyledItemDelegate())
        self.view().setAlternatingRowColors(True)
        self.setFont(Font.NAME)
        #
        self.setLineEdit(QtLineEdit())


class QtProgressDialog(QtWidgets.QProgressDialog):
    def __init__(self, *args, **kwargs):
        super(QtProgressDialog, self).__init__(*args, **kwargs)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setCancelButton(None)


class _QtProgressBar(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtProgressDef
):
    def __init__(self, *args, **kwargs):
        super(_QtProgressBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMaximumHeight(4)
        self.setMinimumHeight(4)
        #
        self._set_progress_def_init_()

    def _set_wgt_update_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._get_is_progress_enable_() is True:
            if self._progress_raw:
                cur_rect = None
                w, h = self.width(), self.height()
                w -= 2
                layer_count = len(self._progress_raw)
                r, g, b = utl_methods.Color.hsv2rgb(120, .5, 1)
                for layer_index, i in enumerate(self._progress_raw):
                    i_minimum, i_maximum, percent, label = i
                    p_w = w*(i_maximum-i_minimum)*percent
                    p_h = 2
                    #
                    i_x, i_y = w*i_minimum, (h-p_h)/2
                    i_x += 1
                    i_rect = QtCore.QRect(i_x, i_y, p_w+1, p_h)
                    #
                    i_p = float(layer_index)/float(layer_count)
                    r_1, g_1, b_1 = utl_methods.Color.hsv2rgb(120*i_p, .5, 1)
                    i_cur_color = QtGui.QColor(r_1, g_1, b_1, 255)
                    if layer_index == 0:
                        i_pre_color = QtGui.QColor(r, g, b, 255)
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(.5, i_pre_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_background_color = i_gradient_color
                    else:
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(0, QtBackgroundColor.Transparent)
                        i_gradient_color.setColorAt(.5, i_cur_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_gradient_color.setColorAt(1, QtBackgroundColor.Transparent)
                        i_background_color = i_gradient_color
                    #
                    painter._set_frame_draw_by_rect_(
                        i_rect,
                        border_color=QtBorderColor.Transparent,
                        background_color=i_background_color,
                        border_radius=1,
                    )
                    cur_rect = i_rect
                #
                if cur_rect is not None:
                    c_x, c_y = cur_rect.x(), cur_rect.y()
                    c_w, c_h = cur_rect.width(), cur_rect.height()
                    rect = QtCore.QRect(
                        c_x+c_w-2, 0, 2, h
                    )
                    painter._set_frame_draw_by_rect_(
                        rect,
                        border_color=QtBorderColor.Transparent,
                        background_color=(255, 255, 255, 255),
                        border_radius=1,
                    )


class _AbsQtSplitterHandle(QtWidgets.QWidget):
    QT_ORIENTATION = None
    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitterHandle, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._swap_enable = True
        #
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        #
        self._contract_icon_name_l = ['contract_h_l', 'contract_v_l'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._contract_icon_name_r = ['contract_h_r', 'contract_v_r'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._swap_icon_name = ['swap_h', 'swap_v'][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        #
        self._contract_frame_size = [(20, 10), (10, 20)][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        self._contract_icon_size = [(16, 8), (8, 16)][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        #
        self._is_contract_l = False
        self._is_contract_r = False
        #
        self._qt_layout_class = [QtHBoxLayout, QtVBoxLayout][self.QT_ORIENTATION == QtCore.Qt.Horizontal]
        #
        self._size_l = 0
        self._size_r = 0
        self._sizes = []
        #
        self._index = 0
        #
        layout = self._qt_layout_class(self)
        layout.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._contract_l_button = QtIconButton()
        self._contract_l_button._frame_size = self._contract_frame_size
        self._contract_l_button._file_icon_size = self._contract_icon_size
        self._contract_l_button.setMaximumSize(*self._contract_frame_size)
        self._contract_l_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._contract_l_button)
        self._contract_l_button.clicked.connect(self._set_contract_l_switch_)
        self._contract_l_button.setToolTip(
            '"LMB-click" to contact left/top.'
        )
        #
        self._swap_button = QtIconButton()
        #
        self._swap_button._icon_file_path = utl_core.Icon.get(self._swap_icon_name)
        self._swap_button._frame_size = self._contract_frame_size
        self._swap_button._file_icon_size = self._contract_icon_size
        self._swap_button.setMaximumSize(*self._contract_frame_size)
        self._swap_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._swap_button)
        self._swap_button.clicked.connect(self._set_swap_)
        self._swap_button.setToolTip(
            '"LMB-click" to swap.'
        )
        #
        self._contract_r_button = QtIconButton()
        self._contract_r_button._frame_size = self._contract_frame_size
        self._contract_r_button._file_icon_size = self._contract_icon_size
        self._contract_r_button.setMaximumSize(*self._contract_frame_size)
        self._contract_r_button.setMinimumSize(*self._contract_frame_size)
        layout.addWidget(self._contract_r_button)
        self._contract_r_button.clicked.connect(self._set_contract_r_update_)
        self._contract_r_button.setToolTip(
            '"LMB-click" to contact right/bottom.'
        )
        #
        self._set_contract_buttons_update_()
        #
        self.installEventFilter(self)
        self._is_hovered = False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._is_hovered = True
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self.setCursor(QtCore.Qt.SplitHCursor)
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self.setCursor(QtCore.Qt.SplitVCursor)
                self._set_update_()
            elif event.type() == QtCore.QEvent.Leave:
                self._is_hovered = False
                self.setCursor(QtCore.Qt.ArrowCursor)
                self._set_update_()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_move_(event)
        return False

    def _set_contract_l_switch_(self):
        if self._is_contract_r is True:
            self._set_contract_r_update_()
        else:
            splitter = self.splitter()
            index_l = splitter.indexOf(self)-1
            index_r = splitter.indexOf(self)
            indices = index_l, index_r
            # switch
            self._is_contract_l = not self._is_contract_l
            if self._is_contract_l is True:
                # record size
                self._sizes = splitter._get_sizes_(indices)
                #
                sizes = [0, sum(self._sizes)]
                splitter._set_adjacent_sizes_(indices, sizes, )
            else:
                splitter._set_adjacent_sizes_(indices, self._sizes)
            #
            self._set_contract_buttons_update_()

    def _set_contract_r_update_(self):
        if self._is_contract_l is True:
            self._set_contract_l_switch_()
        else:
            splitter = self.splitter()
            index_l = splitter.indexOf(self)-1
            index_r = splitter.indexOf(self)
            indices = index_l, index_r
            # switch
            self._is_contract_r = not self._is_contract_r
            if self._is_contract_r is True:
                # record size
                self._sizes = splitter._get_sizes_(indices)
                #
                sizes = [sum(self._sizes), 0]
                splitter._set_adjacent_sizes_(indices, sizes)
            else:
                splitter._set_adjacent_sizes_(indices, self._sizes)
            #
            self._set_contract_buttons_update_()

    def _set_swap_(self):
        splitter = self.splitter()
        index_l = splitter.indexOf(self)-1
        index_r = splitter.indexOf(self)
        widgets = splitter._get_widgets_()
        widget_l = splitter._get_widget_(index_l)
        widget_r = splitter._get_widget_(index_r)
        widgets[index_l], widgets[index_r] = widget_r, widget_l
        splitter._set_update_()

    def _set_contract_buttons_update_(self):
        icon_name_l = [self._contract_icon_name_l, self._contract_icon_name_r][self._is_contract_l]
        self._contract_l_button._icon_file_path = utl_core.Icon.get(icon_name_l)
        self._contract_l_button.update()
        icon_name_r = [self._contract_icon_name_r, self._contract_icon_name_l][self._is_contract_r]
        self._contract_r_button._icon_file_path = utl_core.Icon.get(icon_name_r)
        self._contract_r_button.update()

    def _set_update_(self):
        pass

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def splitter(self):
        return self.parent()

    def _set_move_(self, event):
        p = event.pos()
        x, y = p.x(), p.y()
        splitter = self.splitter()
        index_l = splitter.indexOf(self)-1
        index_r = splitter.indexOf(self)
        indices = index_l, index_r
        s_l_o, s_r_o = splitter._get_size_(index_l), splitter._get_size_(index_r)
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            s_l, s_r = s_l_o+x, s_r_o-x
            splitter._set_adjacent_sizes_(indices, [s_l, s_r])
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            s_l, s_r = s_l_o+y, s_r_o-y
            splitter._set_adjacent_sizes_(indices, [s_l, s_r])


class _QtHSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitterHandle, self).__init__(*args, **kwargs)


class _QtVSplitterHandle(_AbsQtSplitterHandle):
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitterHandle, self).__init__(*args, **kwargs)


class _AbsQtSplitter(QtWidgets.QWidget):
    QT_HANDLE_CLASS = None
    #
    QT_ORIENTATION = None
    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitter, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._handle_list = []
        self._widget_list = []
        self._rect_list = []
        #
        self._spacing = 4
        self._contents_margins = 0, 0, 0, 0
        #
        self._size_dict = collections.OrderedDict()
        self._pos_dict = collections.OrderedDict()
        self._sizes = []

    def addWidget(self, widget):
        index = len(self._handle_list)
        #
        widget.setParent(self)
        self._widget_list.append(widget)
        # widget.hide()
        #
        handle = self.QT_HANDLE_CLASS()
        handle.setParent(self)
        self._handle_list.append(handle)
        #
        if index not in self._size_dict:
            self._size_dict[index] = 1
        #
        self._rect_list.append(QtCore.QRect())

    def resizeEvent(self, event):
        self._set_update_()

    def _set_update_(self):
        self._set_update_by_size_()
        self._set_widget_geometry_update_()

    def _set_update_by_size_(self):
        ss = self._size_dict
        maximum_size = sum(ss.values())
        if maximum_size > 0:
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [w*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx])+x
                    self._size_dict[idx] = size
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [h*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx])+y
                    self._size_dict[idx] = size
            else:
                raise TypeError()

    def _set_widget_geometry_update_(self):
        w, h = self.width(), self.height()
        c = len(self._handle_list)
        for idx in range(c):
            handle = self._handle_list[idx]
            widget = self._widget_list[idx]
            rect = self._rect_list[idx]
            #
            p = self._pos_dict[idx]
            s = self._size_dict[idx]
            ps = self._size_dict.get(idx-1)
            ns = self._size_dict.get(idx+1)
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                # handle
                hx, hy = p, 0
                hw, hh = 12, h
                if idx == 0:
                    hx, hy = p-12, 0
                else:
                    if s == 0:
                        hx, hy = p-12, 0
                handle.setGeometry(
                    hx, hy, hw, hh
                )
                rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = p+12, 0
                ww, wh = s-12, h
                if idx == 0:
                    wx, wy = p, 0
                    ww, wh = s, h
                if ns == 0:
                    ww, wh = s-12, h
                #
                widget.setGeometry(
                    wx, wy, ww, wh
                )
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                # handle
                hx, hy = 0, p
                hw, hh = w, 12
                if idx == 0:
                    hx, hy = 0, p-12
                if s == 0:
                    hx, hy = 0, p-12
                handle.setGeometry(
                    hx, hy, hw, hh
                )
                rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = 0, p+12
                ww, wh = w, s-12
                if idx == 0:
                    wx, wy = 0, p
                    ww, wh = w, s
                if ns == 0:
                    ww, wh = w, s-12
                #
                widget.setGeometry(
                    wx, wy, ww, wh
                )

    def _get_size_(self, index):
        return self._size_dict[index]

    def _set_size_(self, index, size):
        self._size_dict[index] = size
        #
        self._set_update_()

    def _get_sizes_(self, indices=None):
        if indices is not None:
            return [self._size_dict[i] for i in indices]
        return [i for i in self._size_dict.values()]

    def _set_adjacent_sizes_(self, indices, sizes):
        i_l, i_r = indices[:indices[0]], indices[indices[1]:]
        #
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            size_min, size_max = 0+len(i_l)*12, self.width()-len(i_r)*12
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            size_min, size_max = 0+len(i_l)*12, self.height()-len(i_r)*12
        else:
            raise TypeError()
        for seq, size in enumerate(sizes):
            # clamp size
            if size <= size_min:
                size = size_min
            elif size >= size_max:
                size = size_max
            idx = indices[seq]
            self._size_dict[idx] = size
        #
        self._set_update_()

    def _get_indices_(self):
        return self._size_dict.keys()

    def _get_widgets_(self):
        return self._widget_list

    def _get_widget_(self, index):
        return self._widget_list[index]

    def _get_cur_index_(self, qt_point):
        for idx, rect in enumerate(self._rect_list):
            if rect.contains(qt_point) is True:
                return idx

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def _set_stretch_factor_(self, index, size):
        self._size_dict[index] = size

    def _get_stretch_factor_(self, index):
        return self._size_dict[index]

    def setSizes(self, sizes):
        pass

    def widget(self, index):
        return self._widget_list[index]

    def indexOf(self, handle):
        return self._handle_list.index(handle)

    def setCollapsible(self, index, boolean):
        pass


class _QtHSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _QtHSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitter, self).__init__(*args, **kwargs)


class _QtVSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _QtVSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitter, self).__init__(*args, **kwargs)


class QtHSplitter(QtWidgets.QSplitter):
    def __init__(self, *args, **kwargs):
        super(QtHSplitter, self).__init__(*args, **kwargs)
        self.setHandleWidth(2)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QSplitter')
        )


class QtFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QtFileDialog, self).__init__(*args, **kwargs)
