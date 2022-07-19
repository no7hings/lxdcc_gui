# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt import utl_gui_qt_abstract

from lxbasic import bsc_configure, bsc_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility


class _QtColorChooseChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract._QtChartDef,
):
    color_choose_changed = qt_signal()
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_chart_update_data_(self):
        def set_branch_draw_fnc_(x, y, radius_, color_h_offset_, color_h_multiply_):
            _i_pos = x, y
            if not _i_pos in poses:
                poses.append(_i_pos)
                _i_color_point = QtCore.QPoint(x, y)
                if color_path_main.contains(_i_color_point):
                    _i_sub_points = utl_gui_core.ChartMethod.get_regular_polygon_points(
                        x, y, side_count, subRadius-1, side=0
                    )
                    _i_color_path = _utl_gui_qt_wgt_utility.QtPainterPath()
                    _i_color_path._set_points_add_(_i_sub_points)
                    #
                    angle = utl_gui_core.ChartMethod.get_angle_by_coord(x, y, pos_x, pos_y)
                    length = utl_gui_core.ChartMethod.get_length_by_coord(x, y, pos_x, pos_y)
                    #
                    _color_h = -angle - color_h_offset_
                    #
                    r1 = radius_
                    a1 = angle
                    d1 = 360.0 / side_count
                    d2 = 360.0 / side_count / 2
                    of = -d2
                    a2 = a1+of - utl_gui_core.ChartMethod.FNC_FLOOR(a1 / d1) * d1
                    _l = [
                        utl_gui_core.ChartMethod.FNC_SIN(utl_gui_core.ChartMethod.FNC_ANGLE(d1)) / utl_gui_core.ChartMethod.FNC_COS(utl_gui_core.ChartMethod.FNC_ANGLE(a2)) * r1,
                        r1
                    ][a1 % 180 == 0]
                    #
                    s = length / (_l - subRadius)
                    s = float(max(min(s, 1.0), 0.0))
                    v = color_h_multiply_ / 100.0
                    v = float(max(min(v, 1.0), 0.0))
                    #
                    r, g, b = bsc_core.ColorMtd.hsv2rgb(_color_h, s, v)
                    i_background_rgba = r, g, b, 255
                    i_border_rgba = 0, 0, 0, 0
                    #
                    self._chart_draw_data[i_background_rgba] = _i_color_path, _i_color_point, i_border_rgba
        #
        self._chart_draw_data = {}
        width, height = self.width(), self.height()
        #
        poses = []
        #
        pos_x, pos_y = width / 2, height / 2
        #
        count = self._count
        #
        side = 16
        side_count = 6
        #
        mainRadius = min(width, height) / 2 - side
        #
        subRadius = float(mainRadius) / count
        #
        points_main = utl_gui_core.ChartMethod.get_regular_polygon_points(
            pos_x, pos_y, side_count, mainRadius, subRadius / 2
        )
        color_path_main = _utl_gui_qt_wgt_utility.QtPainterPath()
        color_path_main._set_points_add_(points_main)
        #
        x_count = int(count * .75)
        y_count = int(count * .75)
        #
        for i_x in range(x_count):
            for i_y in range(y_count):
                x_offset = utl_gui_core.ChartMethod.FNC_SIN(utl_gui_core.ChartMethod.FNC_ANGLE(60)) * subRadius
                #
                xSubR = x_offset * i_x * 2 - x_offset * (i_y % 2)
                ySubR = i_y * subRadius * 1.5
                #
                xSubPos = xSubR+pos_x
                _ySubPos = ySubR+pos_y
                #
                _xSubPos = width / 2 - xSubR
                ySubPos = height / 2 - ySubR
                #
                set_branch_draw_fnc_(xSubPos, ySubPos, mainRadius, self._color_h_offset, self._color_v_multiply)
                set_branch_draw_fnc_(_xSubPos, ySubPos, mainRadius, self._color_h_offset, self._color_v_multiply)
                set_branch_draw_fnc_(xSubPos, _ySubPos, mainRadius, self._color_h_offset, self._color_v_multiply)
                set_branch_draw_fnc_(_xSubPos, _ySubPos, mainRadius, self._color_h_offset, self._color_v_multiply)

    def __init__(self, *args, **kwargs):
        super(_QtColorChooseChart, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.installEventFilter(self)
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
        self._set_action_def_init_(self)
        self._set_chart_def_init_()
        self._set_build_()
    #
    def paintEvent(self, event):
        self._color_path_dict = {}
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        # painter.begin(self)  # for pyside2
        painter.setRenderHint(painter.Antialiasing)
        #
        width = self.width()
        height = self.height()
        #
        if self._chart_draw_data:
            for i_background_rgba, v in self._chart_draw_data.items():
                _i_color_path, _i_color_point, i_border_rgba,  = v
                painter._set_border_color_(i_border_rgba)
                painter._set_background_color_(i_background_rgba)
                #
                # painter._set_border_width_(2)
                painter.drawPath(_i_color_path)

        if self._color_rgba_255 is not None:
            if self._color_rgba_255 in self._chart_draw_data:
                _i_color_path, _i_color_point, i_border_rgba = self._chart_draw_data[self._color_rgba_255]
                painter._set_background_color_(0, 0, 0, 0)
                painter._set_border_color_(255, 255, 255, 255)
                #
                painter._set_border_width_(4)
                painter.drawPath(_i_color_path)
                #
                self._color_point_temp = _i_color_point

        if self._color_rgba_255 is not None:
            painter._set_border_color_(255, 255, 255, 255)
            #
            text_rect = QtCore.QRect(
                8, 8,
                width, height
            )
            #
            painter.setFont(get_font())
            painter._set_border_width_(1)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                'R : {0}\r\nG : {1}\r\nB : {2}'.format(*self._color_rgba_255[:3])
            )
            #
            sh, ss, sv = self._color_hsv
            text_rect = QtCore.QRect(
                8, 64,
                width, height
            )
            #
            painter._set_font_(get_font())
            painter._set_border_width_(1)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                'H : {0}\r\nS : {1}\r\nV : {2}'.format(round(sh % 360, 2), round(ss, 2), round(sv, 2))
            )
            #
            text_rect = QtCore.QRect(
                8, 128,
                width, height
            )
            #
            painter._set_border_color_(223, 223, 223, 255)
            painter.setFont(get_font())
            painter._set_border_width_(1)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                '#{}'.format(self._color_css).upper()
            )

        # painter.end()  # for pyside2

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    # Press
                    self._color_point = event.pos()
                    self._set_choose_color_update_()
                    # Move
                    self._move_flag = True
                    self._set_action_flag_(self.ActionFlag.PressClick)
                elif event.button() == QtCore.Qt.RightButton:
                    # Track
                    self._track_offset_start_point = event.globalPos()
                    self._track_offset_flag = True
                elif event.button() == QtCore.Qt.MidButton:
                    # Circle
                    point = event.pos()
                    self._circle_angle_start = self._get_angle_at_circle_(point)
                    self._circle_flag = True
                    self._set_action_flag_(self.ActionFlag.TrackClick)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    # Press
                    self._set_action_flag_(self.ActionFlag.PressMove)
                    # Move
                    self._move_flag = True
                    #
                    self._color_point = event.pos()
                    self._set_choose_color_update_()
                    #
                    self.update()
                elif event.buttons() == QtCore.Qt.RightButton:
                    # Track
                    self._track_offset_flag = True
                    point = event.globalPos() - self._track_offset_start_point
                    self._set_track_offset_action_run_(point)
                elif event.buttons() == QtCore.Qt.MidButton:
                    # Circle
                    self._circle_flag = True
                    #
                    self._set_track_circle_action_run_(event)
                    self._set_action_flag_(self.ActionFlag.TrackCircle)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.PressClick
                    ):
                        self._set_press_click_action_run_(event)
                    #
                    self._move_flag = True
                elif event.button() == QtCore.Qt.RightButton:
                    # Track
                    self._tmp_track_offset_x = self._track_offset_x
                    self._track_offset_y_temp = self._track_offset_y
                    self._track_offset_flag = True
                elif event.button() == QtCore.Qt.MidButton:
                    # Circle
                    self._circle_angle_temp = self._color_h_offset
                    self._circle_flag = True
                self._set_action_flag_clear_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._set_action_flag_(
                    self.ActionFlag.ZoomWheel
                )
                self._set_zoom_scale_action_run_(event)
                #
                self._move_flag = False
                self._circle_flag = False
                self._track_offset_flag = False
            elif event.type() == QtCore.QEvent.Resize:
                self._move_flag = False
                self._circle_flag = False
                self._track_offset_flag = False
                self._set_chart_update_data_()
                self._set_wgt_update_draw_()
        return False

    def _set_choose_color_update_(self):
        pre_color = self._color_rgba_255
        cur_color = self._color_rgba_255
        if self._chart_draw_data:
            for i_background_rgba, v in self._chart_draw_data.items():
                _i_color_path, _i_color_point, i_border_rgba = v
                if _i_color_path.contains(self._color_point):
                    cur_color = i_background_rgba
        #
        if pre_color != cur_color:
            r, g, b, a = cur_color
            self._color_rgba_255 = r, g, b, a
            self._color_hsv = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
            self._color_css = hex(r)[2:].zfill(2)+hex(g)[2:].zfill(2)+hex(b)[2:].zfill(2)
            #
            self.color_choose_changed.emit()
            #
            self._set_wgt_update_draw_()
    #
    def _set_press_click_action_run_(self, event):
        self._color_point = event.pos()
        self._set_choose_color_update_()
    #
    def _set_zoom_scale_action_run_(self, event):
        delta = event.angleDelta().y()
        #
        radix = 3
        #
        pre_count = self._count
        cur_count = bsc_core.ValueMtd.step_to(
            value=pre_count,
            delta=-delta,
            step=radix,
            value_range=(self._count_minimum, self._count_maximum),
            direction=1
        )
        if pre_count != cur_count:
            self._count = cur_count
            self._set_chart_update_data_()
            self._set_wgt_update_draw_()
            self._set_choose_color_update_()
    #
    def _set_track_circle_action_run_(self, event):
        point = event.pos()
        #
        angle_ = self._get_angle_at_circle_(point)
        #
        angle = self._circle_angle_temp+self._circle_angle_start
        angle -= angle_
        #
        if self._circle_flag is True:
            self._color_h_offset = angle
        #
        self._set_chart_update_data_()
        self._set_wgt_update_draw_()
        self._set_choose_color_update_()
    #
    def _set_track_offset_action_run_(self, point):
        xDelta = point.x()
        yDelta = point.y()
        xRadix = 5.0
        yRadix = 5.0
        self._color_v_multiply = bsc_core.ValueMtd.step_to(
            value=self._color_v_multiply,
            delta=-yDelta,
            step=yRadix,
            value_range=(self._mult_v_minimum, self._mult_v_maximum),
            direction=1
        )
        #
        self.update()
    #
    def _set_resize_action_run_(self, size):
        pass
    #
    def _get_popup_pos_(self, xPos, yPos, width, height):
        point = self._color_point
        pos0 = self._color_center_coord
        #
        width0, height0 = self._size_temp
        #
        scale = float(min(width, height)) / float(min(width0, height0))
        #
        x = point.x()
        y = point.y()
        #
        x -= (pos0[0]-xPos)
        y -= (pos0[1]-yPos)
        return QtCore.QPoint(x, y)
    #
    def _get_angle_at_circle_(self, point):
        width = self.width()
        height = self.height()
        #
        xPos = width / 2
        yPos = height / 2
        #
        x = point.x()
        y = point.y()
        #
        return utl_gui_core.ChartMethod.get_angle_by_coord(x, y, xPos, yPos)
    #
    def _get_color_rgb_255_(self):
        return self._color_rgba_255

    def _get_color_rgba_(self):
        return tuple(map(lambda x: float(x/255.0), self._color_rgba_255))
    #
    def _set_color_rgba_(self, r, g, b, a):
        self._color_rgba_255 = tuple(map(lambda x: int(x*255), (r, g, b, a)))
    #
    def _set_build_(self):
        self._color_rgba_255 = 255, 255, 255, 255
        self._color_hsv = 0, 0, 1
        self._color_css = 'FFFFFF'
        #
        self.cls_colorPath = None
        #
        self._color_path_dict = {}
        #
        self._move_flag = False
        #
        self._track_offset_start_point = QtCore.QPoint(0, 0)
        #
        self._color_point = QtCore.QPoint(0, 0)
        self._color_point_temp = QtCore.QPoint(0, 0)
        self._color_center_coord = 0, 0
        self._size_temp = 240, 240
        #
        self._circle_angle_start = 0.0
        #
        self._circle_flag = False
        #
        self._circle_angle_temp = 0.0
        self._color_h_offset = 0.0
        #
        self._track_offset_flag = False
        self._tmp_track_offset_x = 0
        self._track_offset_y_temp = 0
        self._track_offset_x = 0
        self._track_offset_y = 0
        #
        self._count = 3*3+1
        self._count_maximum = 3*10+1
        self._count_minimum = 3*1+1
        #
        self._color_v_multiply = 100.0
        self._mult_v_maximum = 100.0
        self._mult_v_minimum = 0.0


class _QtWaitingChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtChartDef,
):
    def _set_wgt_update_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtWaitingChart, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)

        self._set_chart_def_init_()
        self._c = 10
        self._w, self._h = 64, 64
        self._i_w, self._i_h = 10, 10
        self._basic_rect = QtCore.QRect()
        self._positions = []
        self._timestamp = 0

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(0)
        self._timer.timeout.connect(
            self._set_waiting_update_
        )

    def _set_waiting_start_(self):
        self._timer.start(0)
        # ApplicationOpt().set_process_run_0()

    def _set_waiting_stop_(self):
        self._timer.stop()
        # ApplicationOpt().set_process_run_0()

    def _set_chart_update_data_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        c_w, c_h = self._w, self._h
        self._basic_rect.setRect(
            x, y, w, h
        )
        start = x+(w-c_w)/2, y+(h-c_h)/2
        radius = min(c_w, c_h)
        self._positions = []
        for i in range(self._c):
            i_angle = 360.0/self._c*i
            i_x, i_y = utl_gui_core.Ellipse2dMtd.get_coord_at_angle(
                start=start, radius=radius, angle=i_angle
            )
            self._positions.append(
                (i_x, i_y)
            )

        self._set_wgt_update_draw_()

    def _set_waiting_update_(self):
        self._timestamp = int(bsc_core.SystemMtd.get_timestamp() * 5)
        self._set_wgt_update_draw_()
        # ApplicationOpt().set_process_run_0()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_chart_update_data_()
                event.accept()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        painter._set_border_color_(0, 0, 0, 0)
        painter._set_antialiasing_()

        painter._set_border_color_(0, 0, 0, 0)
        painter._set_background_color_(31, 31, 31, 63)
        painter.drawRect(
            self._basic_rect
        )
        c = self._c
        timestamp = self._timestamp
        for seq, i in enumerate(self._positions):
            i_x, i_y = i

            cur_index = self._c - timestamp % (c+1)
            i_c_h = abs(cur_index-seq) * (360 / c)
            i_h, i_s, i_v = i_c_h, 0.5, 1.0
            i_c_r, i_c_g, i_c_b = bsc_core.ColorMtd.hsv2rgb(i_h, i_s, i_v)
            i_r = 12
            #
            painter._set_border_color_(0, 0, 0, 0)
            painter._set_background_color_(i_c_r, i_c_g, i_c_b, 255)
            #
            if seq == cur_index:
                painter.drawEllipse(
                    i_x-i_r/2, i_y-i_r/2, i_r, i_r
                )
            else:
                i_a = 360.0/c*seq
                i_coords = [
                    utl_gui_core.Ellipse2dMtd.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-90+i_a),
                    utl_gui_core.Ellipse2dMtd.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-210+i_a),
                    utl_gui_core.Ellipse2dMtd.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-330+i_a),
                    utl_gui_core.Ellipse2dMtd.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-90+i_a)
                ]
                painter._set_path_draw_by_coords_(
                    i_coords
                )


class _QtSectorChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtChartDef
):
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_chart_update_data_(self):
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
        self.installEventFilter(self)
        #
        self._set_chart_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_chart_update_data_()
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
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_chart_update_data_(self):
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
                self._set_chart_update_data_()
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
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_chart_update_data_(self):
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
    def __set_press_update_(self, event):
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
                        i_shadow_path.translate(x+offset_x, y+offset_y)
                    #
                    i_enable = True
                elif i_path.contains(event.pos()) is False:
                    if i_is_selected is True:
                        i_is_selected = False
                        i_path.translate(-x, -y)
                        i_shadow_path.translate(-x-offset_x, -y-offset_y)
                #
                self._basic_data[seq] = i_color, i_name, i_value, i_percent, i_path, i_shadow_path, i_pos, i_is_selected
        #
        if not i_enable:
            self._current_name_text = None
            self._current_percent = None
        #
        self.update()
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
                self._set_chart_update_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self.__set_press_update_(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self.__set_press_update_(event)
                else:
                    self._hover_point = event.pos()
                    self.update()
        return False

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
                i_shadow_path = i_sub_path-i_path
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
                radius-side * 2, radius-side * 2
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
    utl_gui_qt_abstract.AbsQtDrawGridDef,
    #
    utl_gui_qt_abstract.AbsQtTrackActionDef,
    utl_gui_qt_abstract.AbsQtZoomActionDef,
    #
    utl_gui_qt_abstract._QtChartDef,
):
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_chart_update_data_(self):
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
    def __set_selection_update_(self, event):
        x = event.pos().x()-self._track_offset_x-self._grid_offset_x
        self._selectedIndex = int(x / int(self._grid_width / self._zoom_scale_x))
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
        self._set_draw_grid_def_init_(self)
        self._grid_axis_lock_x, self._grid_axis_lock_y = 1, 1
        self._grid_dir_x, self._grid_dir_y = 1, -1
        # self._grid_offset_x, self._grid_offset_y = 20, 20
        #
        self._set_track_action_def_init_(self)
        self._track_offset_direction_x, self._track_offset_direction_y = self._grid_dir_x, self._grid_dir_y
        self._track_offset_minimum_x, self._track_offset_minimum_y = -10000, -10000
        self._track_offset_maximum_x, self._track_offset_maximum_y = 0, 0
        #
        self._set_zoom_action_def_init_(self)
        #
        self._set_chart_def_init_()
        #
        self._set_build_()

    def _set_labels_(self, labels):
        self._xValueExplain, self._yValueExplain = labels

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_chart_update_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    x = event.pos().x()-self._track_offset_x-self._grid_offset_x
                    self._selectedIndex = int(x / int(self._grid_width / 2))
                    #
                    self.update()
                    # Drag Select
                    self._move_flag = True
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_tack_offset_action_start_(event)
                    # Zoom
                    self._zoom_scale_flag = False
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._move_flag = False
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    # Track
                    self._set_track_offset_action_end_(event)
                    # Zoom
                    self._zoom_scale_flag = True
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._move_flag is True:
                        self.__set_selection_update_(event)
                        #
                        self.update()
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    # Track
                    if self._track_offset_flag is True:
                        self._set_track_offset_action_run_(event)
                else:
                    event.ignore()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                if self._zoom_scale_flag is True:
                    self._set_zoom_scale_action_run_(event)
        return False
    #
    def paintEvent(self, event):
        x = 0
        y = 0
        #
        width = self.width()
        height = self.height()
        #
        value_scale_x, value_scale_y = self._zoom_scale_x, self._zoom_scale_y
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        rect = QtCore.QRect(
            x, y, width, height
        )
        painter._set_grid_draw_(
            rect,
            axis_dir=(self._grid_dir_x, self._grid_dir_y),
            grid_size=(self._grid_width, self._grid_height),
            grid_scale=(1.0, self._zoom_scale_y),
            translate=(self._track_offset_x, 0),
            grid_offset=(self._grid_offset_x, self._grid_offset_y),
            border_color=self._grid_border_color
        )
        #
        if self._value_array:
            value_maximum = max(self._value_array)
            value_scale_x, value_scale_y = 1.0, int(float('1'+len(str(value_maximum))*'0') / float(self._zoom_scale_y))
            #
            painter._set_histogram_draw_(
                rect,
                value_array=self._value_array,
                value_scale=(value_scale_x, value_scale_y),
                value_offset=(self._grid_value_offset_x, self._grid_value_offset_y),
                label=(self._xValueExplain, self._yValueExplain),
                grid_scale=(1.0, self._zoom_scale_y),
                grid_size=(self._grid_width, self._grid_height),
                grid_offset=(self._grid_offset_x, self._grid_offset_y),
                translate=(self._track_offset_x, 0),
                current_index=self._selectedIndex,
                mode=self._grid_value_show_mode,
            )
        #
        painter._set_grid_axis_draw_(
            rect,
            (self._grid_dir_x, self._grid_dir_y),
            (self._track_offset_x, 0),
            (self._grid_offset_x, self._grid_offset_y),
            (self._grid_axis_lock_x, self._grid_axis_lock_y),
            (self._grid_axis_border_color_x, self._grid_axis_border_color_y)
        )
        painter._set_grid_mark_draw_(
            rect,
            (self._grid_dir_x, self._grid_dir_y),
            (self._grid_width, self._grid_height),
            (self._track_offset_x, 0),
            (self._grid_offset_x, self._grid_offset_y),
            (value_scale_x, value_scale_y),
            (self._grid_value_offset_x, self._grid_value_offset_y),
            self._grid_mark_border_color,
            self._grid_value_show_mode
        )
    #
    def _set_selected_at_(self, index):
        self._selectedIndex = index
    #
    def _set_build_(self):
        self._value_array = []
        #
        self._xValueExplain = 'X'
        self._yValueExplain = 'Y'
        #
        self._selectedIndex = -1


class _QtSequenceChart(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract._QtChartDef,
    utl_gui_qt_abstract._QtStatusDef,
    #
    utl_gui_qt_abstract.AbsQtMenuDef,
):
    QT_MENU_CLASS = _utl_gui_qt_wgt_utility.QtMenu
    def _set_chart_update_data_(self):
        data = self._chart_data
        if data is not None:
            index_array, index_range, name_text = data
            self._chart_index_array = index_array
            self._chart_index_range = min(index_array), max(index_array)
            #
            index_array_0 = range(index_range[0], index_range[1]+1)
            self._chart_index_array = index_array
            index_array_1 = bsc_core.ListMtd.get_intersection(
                index_array_0, index_array
            )
            self._chart_index_merge_array = bsc_core.IntegerArrayMtd.set_merge_to(
                index_array_1
            )
            self._chart_index_lost_array = bsc_core.ListMtd.get_addition(
                index_array_0, index_array_1
            )
            self._chart_index_lost_merge_array = bsc_core.IntegerArrayMtd.set_merge_to(
                self._chart_index_lost_array
            )
            self._chart_index_check_range = index_range
            self._name_text = '{} [{}-{}]'.format(
                name_text, *self._chart_index_range
            )
            #
            if self._chart_index_lost_array:
                self._status = bsc_configure.Status.Error
            else:
                self._status = bsc_configure.Status.Completed
            #
            self.setToolTip(
                (
                    'key="{}"\n'
                    'lost={}'
                ).format(
                    name_text,
                    str(self._chart_index_lost_merge_array)
                )
            )
            #
            self.update()

    def _set_wgt_update_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtSequenceChart, self).__init__(*args, **kwargs)
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
        self._set_build_()
        #
        self._set_name_def_init_()
        self._set_chart_def_init_()
        self._set_status_def_init_()
        #
        self._set_menu_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                # self._set_chart_update_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._hover_flag = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._hover_flag = False
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                #
                elif event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._hover_point = event.pos()
                self.update()
        return False
    #
    def paintEvent(self, event):
        pos_x, pos_y = 0, 0
        width, height = self.width(), self.height()
        #
        side = 2
        spacing = 4
        name_w = self._name_width
        #
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        #
        painter.setFont(get_font())
        #
        index_minimum, index_maximum = self._chart_index_check_range
        #
        count = index_maximum-index_minimum+1
        #
        if count > 0:
            name_rect = QtCore.QRect(
                pos_x+side, pos_y+side, name_w, height-side * 2
            )
            painter._set_font_(get_font(size=10))
            painter._set_border_color_(self._name_color)
            if self._hover_flag is True:
                if name_rect.contains(self._hover_point):
                    painter._set_border_color_(self._hover_name_color)
            #
            text_ = painter.fontMetrics().elidedText(
                self._name_text, QtCore.Qt.ElideLeft, name_rect.width(), QtCore.Qt.TextShowMnemonic
            )
            painter.drawText(
                name_rect,
                QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
                text_
            )
            painter._set_border_color_(self._chart_border_color)
            painter._set_background_color_(self._chart_background_color)
            painter._set_background_style_(QtCore.Qt.FDiagPattern)
            #
            x, y = pos_x+name_w+side+spacing, pos_y+side
            sequence_w = width-name_w-spacing-side*2
            sequence_rect = QtCore.QRect(
                x, y, sequence_w, height-side * 2
            )
            painter.drawRect(sequence_rect)
            #
            c_h, c_s, c_v = 60, .75, .75
            if isinstance(self._chart_index_merge_array, (tuple, list)):
                d_w = float(sequence_w) / float(count)
                i_s = side+2
                for i_raw in self._chart_index_merge_array:
                    if isinstance(i_raw, (int, float)):
                        i_index = i_raw
                        i_x = x+int((i_index-index_minimum)*d_w)
                        i_y = i_s-1
                        i_w = int(d_w)
                        i_h = height-i_s * 2+2
                        #
                        i_percent = float(1) / float(count)
                        #
                        i_rect = QtCore.QRect(i_x, i_y, i_w, i_h)
                        i_c_h = c_h-(1-i_percent)*c_h
                        i_c_r, i_c_g, i_c_b = bsc_core.ColorMtd.hsv2rgb(i_c_h, c_s, c_v)
                        if self._hover_flag is True:
                            if i_rect.contains(self._hover_point):
                                i_c_r, i_c_g, i_c_b = bsc_core.ColorMtd.hsv2rgb(i_c_h, c_s*.75, c_v)
                        #
                        painter._set_border_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter._set_background_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter.drawRect(i_rect)
                        #
                        painter._set_font_(get_font())
                        painter._set_border_color_(self._chart_text_color)
                        painter._set_background_color_(0, 0, 0, 0)
                        i_point = QtCore.QPoint(i_x, i_y+i_h/2+4)
                        painter.drawText(
                            i_point,
                            str(i_raw)
                        )
                    elif isinstance(i_raw, (tuple, list)):
                        i_start_index, i_end_index = i_raw
                        i_x = x+int((i_start_index-index_minimum) * d_w)
                        i_y = i_s-1
                        i_w = int((i_end_index-i_start_index+1) * d_w)
                        i_h = height-i_s*2+2
                        #
                        i_percent = float(i_end_index-i_start_index+1)/float(count)
                        #
                        i_rect = QtCore.QRect(i_x, i_y, i_w, i_h)
                        i_c_h = c_h-(1-i_percent)*c_h
                        if i_percent == 1:
                            i_c_h = 140
                        i_c_r, i_c_g, i_c_b = bsc_core.ColorMtd.hsv2rgb(i_c_h, c_s, c_v)
                        if self._hover_flag is True:
                            if i_rect.contains(self._hover_point):
                                i_c_r, i_c_g, i_c_b = bsc_core.ColorMtd.hsv2rgb(i_c_h, c_s*.75, c_v)
                        #
                        painter._set_border_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter._set_background_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter.drawRect(i_rect)
                        #
                        painter._set_font_(get_font())
                        painter._set_border_color_(self._chart_text_color)
                        painter._set_background_color_(0, 0, 0, 0)
                        i_point = QtCore.QPoint(i_x, i_y+i_h/2+4)
                        painter.drawText(
                            i_point,
                            '{}-{}'.format(i_start_index, i_end_index)
                        )
    #
    def _set_build_(self):
        self._chart_index_array = []
        self._chart_index_range = 0, 0
        #
        self._chart_index_merge_array = []
        self._chart_index_check_range = 0, 0

    def _get_index_range_(self):
        return self._chart_index_range
