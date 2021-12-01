# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt import utl_gui_qt_abstract

from lxbasic import bsc_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility


class _QtColorChooseChart(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtColorChooseChart, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.initUi()
    #
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # Press
            self._pressFlag = True
            # Move
            self._moveFlag = True
        elif event.button() == QtCore.Qt.RightButton:
            # Track
            self._track_start_pos = event.globalPos()
            self._trackFlag = True
            # Zoom
            self._zoomFlag = False
        elif event.button() == QtCore.Qt.MidButton:
            # Circle
            point = event.pos()
            self._circleStartAngle = self.getCircleAngle(point)
            self._circleFlag = True
        # Zoom
        self._zoomFlag = False
    #
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self._pressFlag is True:
                self.cls_colorPoint = event.pos()
                #
                self.update()
            #
            self._moveFlag = True
        elif event.button() == QtCore.Qt.RightButton:
            # Track
            self._xTempTrackOffset = self._track_offset_x
            self._yTempTrackOffset = self._yTrackOffset
            self._trackFlag = True
        elif event.button() == QtCore.Qt.MidButton:
            # Circle
            self._tempCircleAngle = self._circleAngle
            self._circleFlag = True
        # Zoom
        self._zoomFlag = True
    #
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # Press
            self._pressFlag = False
            # Move
            self._moveFlag = True
            #
            self.cls_colorPoint = event.pos()
            #
            self.update()
        elif event.buttons() == QtCore.Qt.RightButton:
            # Track
            self._trackFlag = True
            point = event.globalPos() - self._track_start_pos
            self.trackAction(point)
        elif event.buttons() == QtCore.Qt.MidButton:
            # Circle
            self._circleFlag = True
            #
            point = event.pos()
            self.circleAction(point)
    #
    def wheelEvent(self, event):
        if self._zoomFlag is True:
            delta = event.angleDelta().y()
            self.zoomAction(delta)
        #
        self._pressFlag = False
        self._moveFlag = False
        self._circleFlag = False
        self._trackFlag = False
    #
    def resizeEvent(self, event):
        self._pressFlag = False
        self._moveFlag = False
        self._circleFlag = False
        self._trackFlag = False
    #
    def paintEvent(self, event):
        def setDrawColor():
            def setDrawBranch(x, y):
                p = x, y
                if not p in points:
                    points.append(p)
                    colorPoint = QtCore.QPoint(x, y)
                    if mainColorPath.contains(colorPoint):
                        #
                        subPoints = gui_core.ChartMethod.get_regular_polygon_points(
                            x, y, sideCount, subRadius, side=0
                        )
                        color_path = _utl_gui_qt_wgt_utility.QtPainterPath()
                        color_path._set_points_add_(subPoints)
                        #
                        angle = gui_core.ChartMethod.get_angle_by_coord(x, y, xPos, yPos)
                        length = gui_core.ChartMethod.get_length_by_coord(x, y, xPos, yPos)
                        #
                        h = -angle - hOffset
                        #
                        r1 = mainRadius
                        a1 = angle
                        d1 = 360.0 / sideCount
                        d2 = 360.0 / sideCount / 2
                        of = -d2
                        a2 = a1 + of - gui_core.ChartMethod.FNC_FLOOR(a1 / d1) * d1
                        l = [gui_core.ChartMethod.FNC_SIN(gui_core.ChartMethod.FNC_ANGLE(d1)) / gui_core.ChartMethod.FNC_COS(gui_core.ChartMethod.FNC_ANGLE(a2)) * r1, r1][a1 % 180 == 0]
                        #
                        s = length / (l - subRadius)
                        s = float(max(min(s, 1.0), 0.0))
                        v = vMult / 100.0
                        v = float(max(min(v, 1.0), 0.0))
                        #
                        r, g, b = bsc_core.ColorMtd.hsv2rgb(h, s, v)
                        i_background_rgba = r, g, b, 255
                        i_border_rgba = 0, 0, 0, 255
                        #
                        if self._pressFlag is True or self._moveFlag is True or self._circleFlag is True or self._trackFlag is True:
                            if color_path.contains(pressPoint):
                                self._rbgColor = r, g, b
                                self._hsvColor = h, s, v
                                self._htmlColor = hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
                        #
                        painter._set_border_color_(i_border_rgba)
                        painter._set_background_color_(i_background_rgba)
                        #
                        painter._set_border_width_(2)
                        painter.drawPath(color_path)
                        #
                        self.cls_colorPathDic[(r, g, b)] = color_path, colorPoint
            #
            xPos = width / 2
            yPos = height / 2
            #
            pressPoint = self.cls_colorPoint
            #
            count = self._count
            #
            hOffset = self._circleAngle
            vMult = self._vMult
            #
            side = 16
            sideCount = 6
            #
            mainRadius = min(width, height) / 2 - side
            #
            subRadius = float(mainRadius) / count
            #
            mainPoints = gui_core.ChartMethod.get_regular_polygon_points(
                xPos, yPos, sideCount, mainRadius, subRadius / 2
            )
            mainColorPath = _utl_gui_qt_wgt_utility.QtPainterPath()
            mainColorPath._set_points_add_(mainPoints)
            #
            xCount = int(count * .75)
            yCount = int(count * .75)
            #
            for xSeq in range(xCount):
                for ySeq in range(yCount):
                    xOffset = gui_core.ChartMethod.FNC_SIN(gui_core.ChartMethod.FNC_ANGLE(60)) * subRadius
                    #
                    xSubR = xOffset * xSeq * 2 - xOffset * (ySeq % 2)
                    ySubR = ySeq * subRadius * 1.5
                    #
                    xSubPos = xSubR + xPos
                    _ySubPos = ySubR + yPos
                    #
                    _xSubPos = width / 2 - xSubR
                    ySubPos = height / 2 - ySubR
                    #
                    setDrawBranch(xSubPos, ySubPos)
                    setDrawBranch(_xSubPos, ySubPos)
                    setDrawBranch(xSubPos, _ySubPos)
                    setDrawBranch(_xSubPos, _ySubPos)
        #
        self.cls_colorPathDic = {}
        points = []
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        # painter.begin(self)  # for pyside2
        painter.setRenderHint(painter.Antialiasing)
        #
        width = self.width()
        height = self.height()
        #
        setDrawColor()
        #
        if self._rbgColor is not None:
            textRect = QtCore.QRect(
                8, 8,
                width, height
            )
            #
            painter._set_border_color_(223, 223, 223, 255)
            painter.setFont(get_font(size=12, weight=75))
            painter._set_border_width_(1)
            painter.drawText(
                textRect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                'R : {0}\r\nG : {1}\r\nB : {2}'.format(*self._rbgColor)
            )
            #
            if self._rbgColor in self.cls_colorPathDic:
                selPath, selPoint = self.cls_colorPathDic[self._rbgColor]
                painter._set_background_color_(0, 0, 0, 0)
                painter._set_border_color_(223, 223, 223, 255)
                #
                painter._set_border_width_(4)
                painter.drawPath(selPath)
                #
                self.cls_colorPoint = selPoint
        if self._rbgColor is not None:
            sh, ss, sv = self._hsvColor
            textRect = QtCore.QRect(
                8, 80,
                width, height
            )
            #
            painter._set_border_color_(223, 223, 223, 255)
            painter.setFont(get_font(size=12, weight=75))
            painter._set_border_width_(1)
            painter.drawText(
                textRect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                'H : {0}\r\nS : {1}\r\nV : {2}'.format(round(sh % 360, 2), round(ss, 2), round(sv, 2))
            )
        if self._htmlColor is not None:
            textRect = QtCore.QRect(
                8, 152,
                width, height
            )
            #
            painter._set_border_color_(223, 223, 223, 255)
            painter.setFont(get_font(size=12, weight=75))
            painter._set_border_width_(1)
            painter.drawText(
                textRect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                '#{}'.format(self._htmlColor)
            )

        # painter.end()  # for pyside2
    #
    def zoomAction(self, delta):
        radix = 3
        #
        self._count = bsc_core.ValueMtd.step_to(
            value=self._count, delta=-delta, step=radix,
            valueRange=(self._countMinimum, self._countMaximum)
        )
        #
        self.update()
    #
    def circleAction(self, point):
        angle_ = self.getCircleAngle(point)
        #
        angle = self._tempCircleAngle + self._circleStartAngle
        angle -= angle_
        #
        if self._circleFlag is True:
            self._circleAngle = angle
        #
        self.update()
    #
    def trackAction(self, point):
        xDelta = point.x()
        yDelta = point.y()
        xRadix = 5.0
        yRadix = 5.0
        self._vMult = bsc_core.ValueMtd.step_to(
            value=self._vMult, delta=-yDelta, step=yRadix,
            valueRange=(self._vMultMinimum, self._vMultMaximum)
        )
        #
        self.update()
    #
    def resizeAction(self, size):
        pass
    #
    def getDragPos(self, xPos, yPos, width, height):
        point = self.cls_colorPoint
        pos0 = self._tempCenterCoord
        #
        width0, height0 = self._tempSize
        #
        scale = float(min(width, height)) / float(min(width0, height0))
        #
        x = point.x()
        y = point.y()
        #
        x -= (pos0[0] - xPos)
        y -= (pos0[1] - yPos)
        return QtCore.QPoint(x, y)
    #
    def getCircleAngle(self, point):
        width = self.width()
        height = self.height()
        #
        xPos = width / 2
        yPos = height / 2
        #
        x = point.x()
        y = point.y()
        #
        return gui_core.ChartMethod.get_angle_by_coord(x, y, xPos, yPos)
    #
    def getCurrentRgb(self):
        print self._rbgColor
    #
    def initUi(self):
        self._rbgColor = None
        self._hsvColor = None
        self._htmlColor = None
        #
        self.cls_colorPath = None
        #
        self.cls_colorPathDic = {}
        #
        self._zoomFlag = True
        #
        self._pressFlag = True
        self._moveFlag = False
        #
        self._track_start_pos = QtCore.QPoint(0, 0)
        #
        self.cls_colorPoint = QtCore.QPoint(0, 0)
        self._tempColorPoint = QtCore.QPoint(0, 0)
        self._tempCenterCoord = 0, 0
        self._tempSize = 240, 240
        #
        self._circleStartAngle = 0.0
        #
        self._circleFlag = False
        #
        self._tempCircleAngle = 0.0
        self._circleAngle = 0.0
        #
        self._trackFlag = False
        self._tmp_track_offset_x = 0
        self._yTempTrackOffset = 0
        self._track_offset_x = 0
        self._yTrackOffset = 0
        #
        self._zoomFlag = True
        #
        self._count = 13
        self._countMaximum = 34
        self._countMinimum = 4
        #
        self._vMult = 100.0
        self._vMultMaximum = 100.0
        self._vMultMinimum = 0.0
    #
    def setUiSize(self):
        self.setMaximumSize(166667, 166667)
        self.setMinimumSize(240, 240)


class _QtSectorChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtChartDef
):
    def _set_widget_update_(self):
        self.update()

    def _set_chart_data_update_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = QtSectorChartDrawData(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=16,
            mode=self._chart_mode
        ).get()
    #
    def __init__(self, *args, **kwargs):
        super(_QtSectorChart, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._set_chart_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_chart_data_update_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseMove:
                self._hover_point = event.pos()
                self.update()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        # painter.begin(self)  # for pyside2
        painter.setRenderHint(painter.Antialiasing)
        #
        if self._chart_draw_data is not None:
            painter._set_sector_chart_draw_(
                chart_draw_data=self._chart_draw_data,
                background_color=self._chart_background_color,
                border_color=self._chart_border_color,
                hover_point=self._hover_point,
            )


class _QtRadarChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtChartDef
):
    def _set_widget_update_(self):
        self.update()

    def _set_chart_data_update_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = QtRadarChartDrawData(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=16,
            mode=self._chart_mode
        ).get()
    #
    def __init__(self, *args, **kwargs):
        super(_QtRadarChart, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._map_background_color = 63, 127, 255, 255
        self._map_border_color = 159, 159, 159, 255
        self._rim_background_color = 39, 39, 39, 255
        self._rim_border_color = 95, 95, 95, 255
        #
        self._set_chart_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_chart_data_update_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseMove:
                self._hover_point = event.pos()
                self.update()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        # painter.begin(self)  # for pyside2
        painter.setRenderHint(painter.Antialiasing)
        if self._chart_draw_data is not None:
            basic_data = self._chart_draw_data['basic']
            map_data = self._chart_draw_data['map']
            mark_data = self._chart_draw_data['mark']
            hoverPoint = self._hover_point
            #
            if basic_data is not None:
                for seq, i in enumerate(basic_data):
                    painter._set_background_color_(self._rim_background_color)
                    painter._set_border_color_(self._rim_border_color)
                    painter._set_background_style_(QtCore.Qt.FDiagPattern)
                    if seq == 0:
                        painter.drawPolygon(i)
                    else:
                        painter.drawPolyline(i)
            #
            if map_data is not None:
                i_map_brush, i_map_polygon_src, i_map_polygon_tgt = map_data
                #
                painter._set_background_color_(self._map_background_color)
                painter._set_border_color_(self._map_border_color)
                #
                painter._set_background_style_(QtCore.Qt.Dense5Pattern)
                # painter.drawPolygon(i_map_polygon_src)
                #
                painter._set_background_brush_(i_map_brush)
                painter._set_border_color_(self._map_border_color)
                painter.drawPolygon(i_map_polygon_tgt)
            #
            if mark_data:
                for i in mark_data:
                    (
                        i_background_rgba, i_border_rgba,
                        i_basic_path,
                        i_text_point_0, i_text_point_1,
                        i_text_0, i_text_1,
                        i_point_src, i_point_tgt,
                        i_text_ellipse
                    ) = i
                    #
                    r, g, b, a = i_background_rgba
                    painter._set_background_color_([(r*.75, g*.75, b*.75, 255), (r, g, b, 255)][i_text_ellipse.contains(hoverPoint)])
                    painter._set_border_color_(i_border_rgba)
                    #
                    painter.drawEllipse(i_text_ellipse)
                    #
                    painter.drawText(i_text_point_0, i_text_0)
                    painter.drawText(i_text_point_1, i_text_1)


class _QtPieChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtChartDef
):
    def _set_widget_update_(self):
        self.update()

    def _set_chart_data_update_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = QtPieChartDrawData(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=self._side_w,
            mode=self._chart_mode
        ).get()
        self._basic_data = self._chart_draw_data
    #
    def __init__(self, *args, **kwargs):
        super(_QtPieChart, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._side_w = 8
        self._xOffset = 0
        self._yOffset = 0
        #
        self._explainWidth = 240
        self._explainHeight = 20
        #
        self._current_name_text = None
        self._current_percent = None
        self._current_value = None
        self._pen = QtGui.QPen(QtGui.QColor(223, 223, 223, 255))
        #
        self._set_chart_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_chart_data_update_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_press_update_(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._set_press_update_(event)
                else:
                    self._hover_point = event.pos()
                    self.update()
        return False
    #
    def _set_press_update_(self, event):
        i_enable = False
        offset_x, offset_y = 8, 8
        if self._basic_data:
            for seq, i in enumerate(self._basic_data):
                i_color, i_name, i_value, i_percent, i_path, i_shadow_path, i_pos, i_is_selected = i
                x, y = i_pos
                if i_path.contains(event.pos()) is True:
                    if i_is_selected is False:
                        i_is_selected = True
                        self._current_name_text = i_name
                        self._current_percent = i_percent
                        i_path.translate(x, y)
                        i_shadow_path.translate(x + offset_x, y + offset_y)
                    #
                    i_enable = True
                elif i_path.contains(event.pos()) is False:
                    if i_is_selected is True:
                        i_is_selected = False
                        i_path.translate(-x, -y)
                        i_shadow_path.translate(-x - offset_x, -y - offset_y)
                #
                self._basic_data[seq] = i_color, i_name, i_value, i_percent, i_path, i_shadow_path, i_pos, i_is_selected
        #
        if not i_enable:
            self._current_name_text = None
            self._current_percent = None
        #
        self.update()

    def paintEvent(self, event):
        width, height = self.width(), self.height()
        side = self._side_w
        #
        radius = min(width, height)
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        if self._basic_data:
            current_shadow_path = None
            for i in self._basic_data:
                i_color, i_name, i_value, i_percent, i_path, i_sub_path, i_pos, i_is_selected = i
                i_shadow_path = i_sub_path - i_path
                painter._set_background_color_(i_color)
                if i_is_selected is True:
                    painter._set_border_color_(self._hover_chart_border_color)
                    current_shadow_path = i_shadow_path
                else:
                    painter._set_border_color_(self._chart_border_color)
                #
                painter._set_border_width_(1)
                painter.drawPath(i_path)
            #
            if current_shadow_path is not None:
                painter._set_background_color_(0, 0, 0, 64)
                painter._set_border_color_(0, 0, 0, 64)
                painter._set_border_width_(1)
                painter._set_background_style_(QtCore.Qt.FDiagPattern)
                painter.drawPath(current_shadow_path)
            # Explain
            rect = QtCore.QRect(
                side, side,
                radius - side * 2, radius - side * 2
            )
            if self._current_name_text and self._current_percent:
                painter.setPen(self._pen)
                painter.setFont(get_font(size=12))
                painter.drawText(
                    rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, 
                    '{}: {}'.format(self._current_name_text, self._current_percent)
                )


class _QtHistogramChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtChartDef
):
    def _set_widget_update_(self):
        self.update()

    def _set_chart_data_update_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = QtHistogramChartDrawData(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=16,
            mode=self._chart_mode
        ).get()
        self._basic_data = self._chart_draw_data

        self._value_array = self._chart_data
    #
    def __init__(self, *args, **kwargs):
        super(_QtHistogramChart, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self.initUi()
        #
        self.setUiSize()
        #
        self._set_chart_def_init_()

    def _set_labels_(self, labels):
        self._xValueExplain, self._yValueExplain = labels

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_chart_data_update_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    x = event.pos().x() - self._track_offset_x - self._grid_offset_x
                    self._selectedIndex = int(x / int(self._grid_w / 2))
                    #
                    self.update()
                    # Drag Select
                    self._moveFlag = True
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    # Track
                    self._track_start_pos = event.globalPos()
                    self._trackFlag = True
                    # Zoom
                    self._zoomFlag = False
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._moveFlag = False
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    # Track
                    self._tmp_track_offset_x = self._track_offset_x
                    self._trackFlag = False
                    # Zoom
                    self._zoomFlag = True
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._moveFlag is True:
                        self._set_selection_action_update_(event)
                        #
                        self.update()
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    # Track
                    if self._trackFlag is True:
                        point = event.globalPos() - self._track_start_pos
                        self._set_track_action_update_(point)
                else:
                    event.ignore()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                if self._zoomFlag is True:
                    delta = event.angleDelta().y()
                    self.zoomAction(delta)
        return False
    #
    def paintEvent(self, event):
        x = 0
        y = 0
        #
        width = self.width()
        height = self.height()
        #
        gridSize = self._grid_w
        #
        grid_offset_x = self._grid_offset_x
        grid_offset_y = gridSize
        #
        track_offset_x, track_offset_y = self._track_offset_x, 0
        #
        value_scale_x, value_scale_y = 1, 1
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        painter._set_grid_draw_(
            width, height, (1, -1),
            gridSize, (track_offset_x, track_offset_y), (grid_offset_x, grid_offset_y),
            self._grid_border_color
        )
        #
        if self._value_array:
            value_maximum = max(self._value_array)
            value_scale_x, value_scale_y = self._grid_scale_w, int(float('1' + len(str(value_maximum)) * '0') / float(self._grid_scale_h))
            #
            painter._set_histogram_draw_(
                value_array=self._value_array,
                value_scale=(value_scale_x, value_scale_y),
                value_offset=(self._xValueOffset, self._yValueOffset),
                label=(self._xValueExplain, self._yValueExplain),
                pos=(x, y),
                size=(width, height),
                mode=self._useMode,
                grid_scale=(self._grid_scale_w, self._grid_scale_h),
                grid_size=(gridSize, gridSize),
                grid_offset=(self._grid_offset_x, gridSize),
                track_offset=(self._track_offset_x, 0),
                current_index=self._selectedIndex
            )
        #
        painter._set_grid_axis_draw_(
            width,
            height,
            (track_offset_x, track_offset_y),
            (grid_offset_x - 1, grid_offset_y - 1),
            self._axis_border_color
        )
        painter._set_grid_mark_draw_(
            width,
            height,
            (1, -1),
            gridSize, (track_offset_x, track_offset_y), (grid_offset_x, grid_offset_y),
            (value_scale_x, value_scale_y), (self._xValueOffset, self._yValueOffset),
            self._mark_border_color,
            self._useMode
        )
    #
    def _set_selection_action_update_(self, event):
        x = event.pos().x() - self._track_offset_x - self._grid_offset_x
        self._selectedIndex = int(x / int(self._grid_w / self._grid_scale_w))
    #
    def _set_track_action_update_(self, point):
        radix = self._grid_w / 2
        track_offset_x = self._tmp_track_offset_x
        track_offset_x += point.x()
        #
        if self._limitEnabled is True:
            track_offset_x = [0, track_offset_x][track_offset_x < 0]
        # Track
        if self._trackFlag is True:
            self._track_offset_x = int(track_offset_x/radix)*radix
        #
        self.update()
    #
    def zoomAction(self, delta):
        radix = 2.5
        if radix >= self._grid_scale_h:
            self._grid_scale_h += [0, radix][delta > 0]
        elif radix < self._grid_scale_h < self._grid_w:
            self._grid_scale_h += [-radix, radix][delta > 0]
        elif self._grid_scale_h >= self._grid_w:
            self._grid_scale_h += [-radix, 0][delta > 0]
        #
        self.update()
    #
    def setSelected(self, index):
        self._selectedIndex = index
    #
    def setUiSize(self):
        self.setMaximumSize(166667, 166667)
        self.setMinimumSize(0, 0)
    #
    def initUi(self):
        self._grid_border_color = 71, 71, 71, 255
        self._mark_border_color = 191, 191, 191, 255
        self._axis_border_color = 191, 191, 191, 255
        #
        self._useMode = 1
        #
        self._zoomFlag = True
        #
        self._limitEnabled = True
        self._trackFlag = False
        self._track_start_pos = QtCore.QPoint(0, 0)
        self._tmp_track_offset_x = 0
        self._track_offset_x = 0
        #
        self._moveFlag = False
        #
        self._grid_w = 20
        #
        self._grid_scale_w = 2
        self._grid_scale_h = 10
        #
        self._grid_offset_x = self._grid_w*2
        #
        self._value_array = []
        #
        self._xValueOffset = 0
        self._yValueOffset = 0
        #
        self._xValueExplain = 'X'
        self._yValueExplain = 'Y'
        #
        self._selectedIndex = -1
