# coding=utf-8
import collections

import enum

import fnmatch

import urllib

from contextlib import contextmanager

import six
from lxutil_gui.qt.utl_gui_qt_core import *


class AbsQtWidgetBaseDef(object):
    def _init_widget_base_def_(self, widget):
        self._widget = widget
        self._basic_rect = QtCore.QRect()
        self._w, self._h = 0, 0

    def _get_text_draw_width_(self, text=None):
        return self._widget.fontMetrics().width(text)

    def _set_size_(self, w, h):
        self._widget.setFixedSize(QtCore.QSize(w, h))


class AbsQtBusyBaseDef(object):
    def _init_busy_base_def_(self, widget):
        self._widget = widget
    @contextmanager
    def _gui_bustling_(self):
        self._widget.setCursor(QtCore.Qt.BusyCursor)
        yield self
        self._widget.unsetCursor()


class AbsQtFocusDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_focus_draw_geometry_(self):
        raise NotImplementedError()

    def _init_focus_def_(self, widget):
        self._widget = widget
        self._is_focused = False
        self._focus_rect = QtCore.QRect()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        if boolean is True:
            self._widget.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self._widget.setFocus(
                QtCore.Qt.NoFocusReason
            )
        self._refresh_focus_draw_geometry_()
        self._refresh_widget_draw_()

    def _get_is_focused_(self):
        return self._is_focused

    def _set_focused_rect_(self, x, y, w, h):
        self._focus_rect.setRect(
            x, y, w, h
        )

    def _get_focus_rect_(self):
        return self._focus_rect


class AbsQtEmptyBaseDef(object):
    def _init_empty_base_def_(self, widget):
        self._widget = widget

        self._empty_icon_name = 'placeholder/default'
        self._empty_text = None
        self._empty_sub_text = None

    def _set_empty_icon_name_(self, text):
        self._empty_icon_name = text
        self._widget.update()

    def _set_empty_text_(self, text):
        self._empty_text = text
        self._widget.update()

    def _set_empty_sub_text_(self, text):
        self._empty_sub_text = text
        self._widget.update()


class AbsQtMenuBaseDef(object):
    QT_MENU_CLS = None
    def _init_menu_base_def_(self, widget):
        self._widget = widget
        self._menu_title_text = None
        self._menu_raw = []
        self._menu_content = None
        self._menu_data_gain_fnc = None

    def _set_menu_title_text_(self, text):
        self._menu_title_text = text

    def _set_menu_data_(self, data):
        """
        :param data: list, etc.
        [
            ('VBO Info (Quads/Tris)', None, None),
            () # sep,
            ('VBO Info', None, None),
            ('Camera/Complexity', None, None),
            ('Performance', None, None),
            ('GPU stats', None, None),
        ]
        :return:
        """
        self._menu_raw = data

    def _add_menu_data_(self, data):
        if isinstance(data, list):
            self._menu_raw.extend(data)
        elif isinstance(data, tuple):
            self._menu_raw.append(data)

    def _extend_menu_data_(self, raw):
        self._menu_raw.extend(raw)

    def _get_menu_data_(self):
        return self._menu_raw

    def _set_menu_data_gain_fnc_(self, fnc):
        self._menu_data_gain_fnc = fnc

    def _popup_menu_(self):
        menu_content = self._get_menu_content_()
        menu_data = self._get_menu_data_()
        #
        menu = None
        #
        if menu_content:
            if menu_content.get_is_empty() is False:
                if menu is None:
                    menu = self.QT_MENU_CLS(self)
                    #
                    if self._menu_title_text is not None:
                        menu._set_title_text_(self._menu_title_text)
                #
                menu._set_menu_content_(menu_content)
                menu._set_show_()
        #
        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
                #
                if self._menu_title_text is not None:
                    menu._set_title_text_(self._menu_title_text)
            #
            menu._set_menu_data_(menu_data)
            menu._set_show_()
        #
        if self._menu_data_gain_fnc is not None:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
                #
                if self._menu_title_text is not None:
                    menu._set_title_text_(self._menu_title_text)
            #
            menu_data = self._menu_data_gain_fnc()
            if menu_data:
                menu._set_menu_data_(menu_data)
                menu._set_show_()

    def _set_menu_content_(self, content):
        self._menu_content = content

    def _get_menu_content_(self):
        return self._menu_content


class AbsQtStatusBaseDef(object):
    Status = bsc_configure.Status
    ShowStatus = bsc_configure.ShowStatus
    ValidationStatus = bsc_configure.ValidatorStatus
    StatusRgba = bsc_configure.StatusRgba
    #
    @classmethod
    def _get_rgb_args_(cls, r, g, b, a):
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        r_, g_, b_ = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        return (r_, g_, b_, a), (r, g, b, a)
    @classmethod
    def _get_sub_process_status_rgba_args_(cls, status):
        if status in {bsc_configure.Status.Started}:
            return cls._get_rgb_args_(*cls.StatusRgba.Opacity)
        elif status in {bsc_configure.Status.Failed, bsc_configure.Status.Error, bsc_configure.Status.Killed}:
            return cls._get_rgb_args_(*cls.StatusRgba.Red)
        elif status in {bsc_configure.Status.Waiting}:
            return cls._get_rgb_args_(*cls.StatusRgba.Orange)
        elif status in {bsc_configure.Status.Suspended}:
            return cls._get_rgb_args_(*cls.StatusRgba.Yellow)
        elif status in {bsc_configure.Status.Running}:
            return cls._get_rgb_args_(*cls.StatusRgba.Blue)
        elif status in {bsc_configure.Status.Completed}:
            return cls._get_rgb_args_(*cls.StatusRgba.Green)
        return cls._get_rgb_args_(*cls.StatusRgba.Opacity)
    @classmethod
    def _get_text_color_by_validator_status_rgba_args_(cls, status):
        if status in {bsc_configure.ValidatorStatus.Warning}:
            return cls._get_rgb_args_(*cls.StatusRgba.Yellow)
        elif status in {bsc_configure.ValidatorStatus.Error}:
            return cls._get_rgb_args_(*cls.StatusRgba.Red)
        elif status in {bsc_configure.ValidatorStatus.Correct}:
            return cls._get_rgb_args_(*cls.StatusRgba.Green)
        elif status in {bsc_configure.ValidatorStatus.Locked}:
            return cls._get_rgb_args_(*cls.StatusRgba.Purple)
        elif status in {bsc_configure.ValidatorStatus.Active}:
            return cls._get_rgb_args_(*cls.StatusRgba.Blue)
        return cls._get_rgb_args_(*cls.StatusRgba.White)
    @classmethod
    def _get_border_color_by_validator_status_rgba_args_(cls, status):
        if status in [bsc_configure.ValidatorStatus.Warning]:
            return cls._get_rgb_args_(*cls.StatusRgba.Yellow)
        elif status in [bsc_configure.ValidatorStatus.Error]:
            return cls._get_rgb_args_(*cls.StatusRgba.Red)
        elif status in [bsc_configure.ValidatorStatus.Correct]:
            return cls._get_rgb_args_(*cls.StatusRgba.Green)
        elif status in [bsc_configure.ValidatorStatus.Locked]:
            return cls._get_rgb_args_(*cls.StatusRgba.Purple)
        elif status in [bsc_configure.ValidatorStatus.Active]:
            return cls._get_rgb_args_(*cls.StatusRgba.Blue)
        return cls._get_rgb_args_(*cls.StatusRgba.Opacity)
    @classmethod
    def _get_background_color_by_validator_status_rgba_args_(cls, status):
        if status in [bsc_configure.ValidatorStatus.Warning]:
            return cls._get_rgb_args_(*cls.StatusRgba.Yellow)
        elif status in [bsc_configure.ValidatorStatus.Error]:
            return cls._get_rgb_args_(*cls.StatusRgba.Red)
        elif status in [bsc_configure.ValidatorStatus.Correct]:
            return cls._get_rgb_args_(*cls.StatusRgba.Green)
        elif status in [bsc_configure.ValidatorStatus.Locked]:
            return cls._get_rgb_args_(*cls.StatusRgba.Purple)
        elif status in [bsc_configure.ValidatorStatus.Active]:
            return cls._get_rgb_args_(*cls.StatusRgba.Blue)
        return cls._get_rgb_args_(*cls.StatusRgba.Opacity)

    def _init_status_base_def_(self, widget):
        self._widget = widget
        #
        self._is_status_enable = False
        #
        self._status = bsc_configure.Status.Stopped
        #
        self._status_color = QtBackgroundColors.Transparent
        self._hover_status_color = QtBackgroundColors.Transparent
        #
        self._status_rect = QtCore.QRect()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_status_(self, status):
        self._is_status_enable = True
        #
        self._status = status
        #
        if status in {bsc_configure.Status.Running}:
            self._widget.setCursor(QtCore.Qt.BusyCursor)
        else:
            self._widget.unsetCursor()
        #
        self._status_color, self._hover_status_color = self._get_sub_process_status_rgba_args_(
            self._status
        )
        self._refresh_widget_draw_()

    def _get_status_(self):
        return self._status

    def _get_status_is_enable_(self):
        return self._is_status_enable


class AbsQtSubProcessDef(object):
    def _set_sub_process_def_init_(self):
        self._sub_process_is_enable = False
        #
        self._sub_process_statuses = []

        self._sub_process_status_text = ''
        #
        self._sub_process_status_colors = []
        self._hover_sub_process_status_colors = []
        #
        self._sub_process_status_rect = QtCore.QRect()

        self._sub_process_finished_results = []

        self._sub_process_timestamp_started = 0
        self._sub_process_timestamp_costed = 0
        #
        self._sub_process_finished_timestamp_estimated = 0

        self._sub_process_finished_value = 0
        self._sub_process_finished_maximum = 0

        self._sub_process_status_text_format_0 = '[{costed_time}]'
        self._sub_process_status_text_format_1 = '[{value}/{maximum}][{costed_time}]'
        self._sub_process_status_text_format_2 = '[{value}/{maximum}][{costed_time}/{estimated_time}]'

        # self._sub_process_timer = QtCore.QTimer(self)

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_sub_process_initialization_(self, count, status):
        if count > 0:
            self._sub_process_is_enable = True
            self._sub_process_statuses = [status]*count
            color, hover_color = AbsQtStatusBaseDef._get_sub_process_status_rgba_args_(status)
            self._sub_process_status_colors = [color]*count
            self._hover_sub_process_status_colors = [hover_color]*count
            self._sub_process_finished_results = [False]*count
            self._sub_process_finished_maximum = len(self._sub_process_finished_results)
            self._sub_process_timestamp_started = bsc_core.TimeMtd.get_timestamp()
        else:
            self._set_sub_process_restore_()

        self._refresh_widget_draw_()

    def _set_sub_process_statuses_(self, statuses):
        if statuses:
            count = len(statuses)
            self._sub_process_is_enable = True
            self._sub_process_statuses = statuses
            self._sub_process_status_colors = []
            self._hover_sub_process_status_colors = []
            for i_status in statuses:
                i_color, i_hover_color = AbsQtStatusBaseDef._get_sub_process_status_rgba_args_(i_status)
                self._sub_process_status_colors.append(i_color)
                self._hover_sub_process_status_colors.append(i_hover_color)

            self._sub_process_finished_results = [False]*count
            self._sub_process_timestamp_started = bsc_core.TimeMtd.get_timestamp()
        else:
            self._set_sub_process_restore_()
        #
        self._refresh_widget_draw_()

    def _set_sub_process_status_at_(self, index, status):
        self._sub_process_statuses[index] = status
        #
        color, hover_color = AbsQtStatusBaseDef._get_sub_process_status_rgba_args_(status)
        self._sub_process_status_colors[index] = color
        self._hover_sub_process_status_colors[index] = hover_color
        #
        self._refresh_widget_draw_()

    def _set_sub_process_restore_(self):
        self._sub_process_is_enable = False
        self._sub_process_statuses = []
        self._sub_process_status_colors = []
        self._hover_sub_process_status_colors = []
        self._sub_process_finished_results = []

        self._sub_process_status_text = ''

    def _set_sub_process_finished_at_(self, index, status):
        self._sub_process_finished_results[index] = True
        #
        self._set_sub_process_finished_update_()
        #
        self._refresh_widget_draw_()

    def _set_sub_process_finished_update_(self):
        self._sub_process_finished_value = sum(self._sub_process_finished_results)
        self._sub_process_finished_maximum = len(self._sub_process_finished_results)
        #
        self._sub_process_timestamp_costed = bsc_core.TimeMtd.get_timestamp()-self._sub_process_timestamp_started
        if self._sub_process_finished_value > 1:
            self._sub_process_finished_timestamp_estimated = (self._sub_process_timestamp_costed/self._sub_process_finished_value)*self._sub_process_finished_maximum
        else:
            self._sub_process_finished_timestamp_estimated = 0

    def _refresh_sub_process_draw_(self):
        self._sub_process_timestamp_costed = bsc_core.TimeMtd.get_timestamp()-self._sub_process_timestamp_started
        self._refresh_widget_draw_()

    def _get_sub_process_status_text_(self):
        if self._sub_process_is_enable is True:
            kwargs = dict(
                value=self._sub_process_finished_value,
                maximum=self._sub_process_finished_maximum,
                costed_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                    self._sub_process_timestamp_costed,
                    mode=1
                ),
                estimated_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                    self._sub_process_finished_timestamp_estimated,
                    mode=1
                ),
            )
            if int(self._sub_process_finished_timestamp_estimated) > 0:
                return self._sub_process_status_text_format_2.format(
                    **kwargs
                )
            else:
                return self._sub_process_status_text_format_1.format(
                    **kwargs
                )
        return ''

    def _get_sub_process_is_finished_(self):
        # completed is True
        return sum(self._sub_process_finished_results) == len(self._sub_process_finished_results)

    def _set_sub_process_enable_(self, boolean):
        self._sub_process_is_enable = boolean

    def _get_sub_process_is_enable_(self):
        return self._sub_process_is_enable

    def _set_sub_process_finished_connect_to_(self, fnc):
        raise NotImplementedError()


class AbsQtValidatorDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_validator_def_init_(self, widget):
        self._widget = widget

        self._validator_is_enable = False
        self._validator_statuses = []
        self._validator_status_colors = []
        self._hover_validator_status_colors = []

        self._validator_status_rect = QtCore.QRect()

    def _set_validator_status_at_(self, index, status):
        self._validator_statuses[index] = status
        color, hover_color = AbsQtStatusBaseDef._get_background_color_by_validator_status_rgba_args_(status)
        self._validator_status_colors[index] = color
        self._hover_validator_status_colors[index] = hover_color
        #
        self._refresh_widget_draw_()

    def _set_validator_restore_(self):
        self._validator_is_enable = False
        self._validator_statuses = []
        self._validator_status_colors = []
        self._hover_validator_status_colors = []

    def _set_validator_statuses_(self, statuses):
        if statuses:
            self._validator_is_enable = True
            self._validator_statuses = statuses
            self._validator_status_colors = []
            self._hover_validator_status_colors = []
            for i_status in statuses:
                i_color, i_hover_color = AbsQtStatusBaseDef._get_background_color_by_validator_status_rgba_args_(i_status)
                self._validator_status_colors.append(i_color)
                self._hover_validator_status_colors.append(i_hover_color)
        else:
            self._set_validator_restore_()

        self._refresh_widget_draw_()

    def _get_validator_is_enable_(self):
        return self._validator_is_enable


class AbsQtFrameBaseDef(object):
    def _init_frame_base_def_(self, widget):
        self._widget = widget
        self._frame_border_color = QtBackgroundColors.Transparent
        self._hovered_frame_border_color = QtBackgroundColors.Transparent
        self._selected_frame_border_color = QtBackgroundColors.Transparent
        self._actioned_frame_border_color = QtBackgroundColors.Transparent
        #
        self._frame_background_color = QtBackgroundColors.Transparent
        self._hovered_frame_background_color = QtBackgroundColors.Transparent
        self._selected_frame_background_color = QtBackgroundColors.Transparent
        self._actioned_frame_background_color = QtBackgroundColors.Transparent
        #
        self._frame_border_radius = 0
        #
        self._frame_draw_is_enable = False
        self._frame_draw_rect = QtCore.QRect()
        self._frame_draw_margins = 0, 0, 0, 0
        self._frame_size = 20, 20
        self._frame_border_draw_style = QtCore.Qt.SolidLine
        self._frame_border_draw_width = 1

        self._frame_draw_rects = [QtCore.QRect()]

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_border_color_(self, color):
        self._frame_border_color = Color._get_qt_color_(color)
        self._refresh_widget_draw_()

    def _set_background_color_(self, color):
        self._frame_background_color = Color._get_qt_color_(color)
        self._refresh_widget_draw_()

    def _get_border_color_(self):
        return self._frame_border_color

    def _get_background_color_(self):
        return self._frame_background_color

    def _set_frame_draw_rect_(self, x, y, w, h):
        self._frame_draw_rect.setRect(
            x, y, w, h
        )

    def _get_frame_rect_(self):
        return self._frame_draw_rect

    def _set_frame_size_(self, w, h):
        self._frame_size = w, h

    def _set_frame_draw_enable_(self, boolean):
        self._frame_draw_is_enable = boolean
        self._refresh_widget_draw_()

    def _set_frame_border_radius_(self, radius):
        self._frame_border_radius = radius


class AbsQtResizeBaseDef(object):
    ResizeOrientation = utl_gui_configure.Orientation
    ResizeAlignment = utl_gui_configure.Alignment
    def _init_resize_base_def_(self, widget):
        self._widget = widget

        self._resize_orientation = self.ResizeOrientation.Horizontal
        self._resize_alignment = self.ResizeAlignment.Right

        self._resize_is_enable = False
        self._resize_draw_rect = QtCore.QRect()
        self._resize_action_rect = QtCore.QRect()

        self._resize_icon_file_paths = [
            utl_gui_core.RscIconFile.get('resize-left'), utl_gui_core.RscIconFile.get('resize-right')
        ]
        self._resize_icon_file_path = self._resize_icon_file_paths[self._resize_alignment]
        #
        self._resize_frame_draw_size = 20, 20
        self._resize_icon_draw_size = 16, 16
        self._resize_icon_draw_rect = QtCore.QRect()

        self._resize_point_start = QtCore.QPoint()
        self._resize_value_temp = 0

        self._resize_target = None
        self._resize_minimum = 20
        self._resize_maximum = 960

    def _set_resize_enable_(self, boolean):
        self._resize_is_enable = boolean

    def _set_resize_target_(self, widget):
        self._resize_target = widget

    def _set_resize_minimum_(self, value):
        self._resize_minimum = value

    def _set_resize_maximum_(self, value):
        self._resize_maximum = value

    def _set_resize_orientation_(self, value):
        self._resize_orientation = value

    def _set_resize_alignment_(self, value):
        self._resize_alignment = value
        self._resize_icon_file_path = self._resize_icon_file_paths[self._resize_alignment]

    def _set_resize_icon_file_paths_(self, file_paths):
        self._resize_icon_file_paths = file_paths
        self._resize_icon_file_path = self._resize_icon_file_paths[self._resize_alignment]


class AbsQtPopupBaseDef(object):
    #
    user_popup_choose_finished = qt_signal()
    #
    user_popup_choose_text_accepted = qt_signal(str)
    user_popup_choose_texts_accepted = qt_signal(list)
    def _init_popup_base_def_(self, widget):
        self._widget = widget
        self._popup_region = 0
        self._popup_side = 2
        self._popup_margin = 8
        self._popup_shadow_radius = 4
        self._popup_offset = 0, 0

        self._popup_entry = None
        self._popup_entry_frame = None

        self._popup_is_activated = False

        self._popup_width_minimum = 160

        self._popup_toolbar_h = 20
        self._popup_toolbar_draw_rect = QtCore.QRect()
        self._popup_toolbar_draw_tool_tip_rect = QtCore.QRect()

        self._popup_auto_resize_is_enable = False
    @classmethod
    def _get_popup_press_point_(cls, widget, rect=None):
        if rect is None:
            rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        return widget.mapToGlobal(rect.center())

    def _get_popup_pos_(self, widget):
        rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        p = widget.mapToGlobal(rect.topLeft())
        o_x, o_y = self._popup_offset
        return p.x() + o_x, p.y() + o_y
    @classmethod
    def _get_popup_pos_0_(cls, widget):
        rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        p = widget.mapToGlobal(rect.bottomLeft())
        return p.x(), p.y() + 1
    @classmethod
    def _get_popup_size_(cls, widget):
        rect = widget.rect()
        return rect.width(), rect.height()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_geometry_(self):
        raise NotImplementedError()

    def _execute_popup_start_(self, *args, **kwargs):
        raise NotImplementedError()

    def _execute_popup_end_(self, *args, **kwargs):
        raise NotImplementedError()

    def _close_popup_(self, *args, **kwargs):
        self._widget.close()
        self._widget.deleteLater()

    def _set_popup_activated_(self, boolean):
        self._popup_is_activated = boolean
        if boolean is True:
            self._widget.show()
        else:
            self._widget.hide()

    def _show_popup_0_(self, press_point, press_rect, desktop_rect, view_width, view_height):
        press_x, press_y = press_point.x(), press_point.y()
        press_w, press_h = press_rect.width(), press_rect.height()
        #
        width_maximum = desktop_rect.width()
        height_maximum = desktop_rect.height()
        #
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        o_x = 0
        o_y = 0
        #
        width_ = view_width + margin*2 + side*2 + shadow_radius
        height_ = view_height + margin*2 + side*2 + shadow_radius
        #
        r_x, r_y, region = bsc_core.RawCoordMtd.set_region_to(
            position=(press_x, press_y),
            size=(width_, height_),
            maximum_size=(width_maximum, height_maximum),
            offset=(o_x, o_y)
        )
        self._popup_region = region
        #
        if region in [0, 1]:
            y_ = r_y - side + press_h / 2
        else:
            y_ = r_y + side + shadow_radius - press_h / 2
        #
        if region in [0, 2]:
            x_ = r_x - margin*3
        else:
            x_ = r_x + margin*3 + side + shadow_radius
        #
        self._widget.setGeometry(
            x_, y_,
            width_, height_
        )
        #
        self._refresh_widget_draw_geometry_()
        #
        self._widget.show()
        self._refresh_widget_draw_()

    def _show_popup_(self, pos, size):
        x, y = pos
        w, h = size
        # desktop_rect = get_qt_desktop_rect()
        self._widget.setGeometry(
            x, y,
            w, h
        )
        self._refresh_widget_draw_geometry_()
        #
        self._widget.show()
        #
        self._widget.update()

    def _set_popup_entry_(self, widget):
        self._popup_entry = widget
        self._popup_entry.installEventFilter(self._widget)

    def _set_popup_entry_frame_(self, widget):
        self._popup_entry_frame = widget

    def _set_popup_offset_(self, x, y):
        self._popup_offset = x, y

    def _execute_popup_scroll_to_pre_(self):
        pass

    def _execute_popup_scroll_to_next_(self):
        pass

    def _set_popup_auto_resize_enable_(self, boolean):
        self._popup_auto_resize_is_enable = boolean


class AbsQtValueDef(object):
    def _set_value_def_init_(self, widget):
        self._widget = widget
        self._value_validation_fnc = None

        self._value_type = None
        self._value = None

    def _set_value_validation_fnc_(self, fnc):
        self._value_validation_fnc = fnc

    def _get_value_is_valid_(self, value):
        if self._value_validation_fnc is not None:
            return self._value_validation_fnc(value)
        return True

    def _get_value_(self):
        raise NotImplementedError()


class AbsQtValueDefaultDef(object):
    def _init_value_default_def_(self):
        self._item_value_default = None

    def _get_value_(self):
        raise NotImplementedError()

    def _set_value_default_(self, value):
        self._item_value_default = value

    def _get_value_default_(self):
        return self._item_value_default

    def _get_value_is_default_(self):
        return self._get_value_() == self._get_value_default_()


class AbsQtValuesDef(object):
    def _set_values_def_init_(self, widget):
        self._widget = widget
        self._values = []

    def _append_value_(self, value):
        if value not in self._values:
            self._values.append(value)
            return True
        return False

    def _delete_value_(self, value):
        if value in self._values:
            self._values.remove(value)
            return True
        return False

    def _get_values_(self):
        return self._values


class AbsQtEntryBaseDef(object):
    def _init_entry_base_def_(self, widget):
        self._widget = widget
        #
        self._value_entry_frame = None
        #
        self._entry_is_enable = False
        #
        self._entry_use_as_storage = False
        self._entry_use_as_file = False
        self._entry_use_as_file_multiply = False

        self._value_type = None

    def _set_entry_enable_(self, boolean):
        self._entry_is_enable = boolean

    def _set_entry_frame_(self, widget):
        self._value_entry_frame = widget

    def _get_entry_frame_(self):
        if self._value_entry_frame is not None:
            return self._value_entry_frame
        return self._widget.parent()

    def _set_use_as_storage_(self, boolean):
        self._entry_use_as_storage = boolean

    def _set_use_as_file_(self, boolean):
        self._entry_use_as_file = boolean

    def _set_use_as_file_multiply_(self, boolean):
        self._entry_use_as_file_multiply = boolean

    def _set_value_type_(self, value_type):
        self._value_type = value_type

    def _get_value_type_(self):
        return self._value_type


class AbsQtDropBaseDef(object):
    def _init_drop_base_def_(self, widget):
        self._widget = widget
        self._action_drop_is_enable = False

    def _set_drop_enable_(self, boolean):
        self._action_drop_is_enable = boolean


class AbsQtActionDragDef(object):
    def _init_action_drag_def_(self, widget):
        self._widget = widget
        self._drag_is_enable = False

        self._drag_point_offset = QtCore.QPoint(0, 0)
        self._drag_urls = []
        self._drag_data = {}

        self._drag_mime_data = QtCore.QMimeData()

    def _set_drag_enable_(self, boolean):
        self._drag_is_enable = boolean

    def _set_drag_urls_(self, urls):
        self._drag_urls = urls

    def _get_drag_urls_(self):
        return self._drag_urls

    def _set_drag_data_(self, data):
        if isinstance(data, dict):
            self._drag_data = data

    def _update_mime_data_(self):
        self._drag_mime_data = QtCore.QMimeData()
        for k, v in self._drag_data.items():
            self._drag_mime_data.setData(
                bsc_core.auto_encode(k), bsc_core.auto_encode(v)
            )
        #
        if self._drag_urls:
            self._drag_mime_data.setUrls(
                [QtCore.QUrl.fromLocalFile(i) for i in self._drag_urls]
            )

    def _get_drag_data_(self):
        return self._drag_data

    def _get_drag_mime_data_(self):
        return self._drag_mime_data


class AbsQtIconBaseDef(object):
    class IconGeometryMode(object):
        Square = 0
        Auto = 1
    #
    def _init_icon_base_def_(self, widget):
        self._widget = widget
        #
        self._icon_geometry_mode = self.IconGeometryMode.Square
        #
        self._icon_is_enable = False
        #
        self._icon_file_path = None
        self._icon_sub_file_path = None
        self._icon_file_is_enable = False
        self._hover_icon_file_path = None
        #
        self._icon_color_rgb = None
        self._icon_name_text = None
        self._icon_sub_text = None
        self._icon_name_is_enable = False
        #
        self._icon = None
        #
        self._icon_frame_draw_rect = QtCore.QRect()
        self._icon_draw_rect = QtCore.QRect()
        self._icon_sub_draw_rect = QtCore.QRect()
        #
        self._icon_color_draw_rect = QtCore.QRect()
        self._icon_name_draw_rect = QtCore.QRect()
        #
        self._icon_hover_color = QtBackgroundColors.PressedHovered
        #
        self._icon_frame_draw_size = 20, 20
        #
        self._icon_draw_size = 16, 16
        self._icon_draw_percent = .8
        self._sub_icon_draw_size = 10, 10
        self._icon_sub_draw_percent = .5
        #
        self._icon_color_draw_size = 12, 12
        self._icon_name_draw_size = 12, 12
        self._icon_name_draw_percent = .675
        #
        self._icon_state_draw_is_enable = False
        self._icon_state_draw_rect = QtCore.QRect()
        self._icon_state_rect = QtCore.QRect()
        self._icon_state_file_path = None
        self._icon_state_draw_percent = .25
        self._icon_state_draw_rgb = 72, 72, 72

    def _set_icon_geometry_mode_(self, mode):
        self._icon_geometry_mode = mode

    def _set_icon_enable_(self, boolean):
        self._icon_is_enable = boolean

    def _set_icon_state_draw_enable_(self, boolean):
        self._icon_state_draw_is_enable = boolean

    def _set_icon_state_rgb_(self, color):
        pass

    def _set_icon_hover_color_(self, qt_color):
        self._icon_hover_color = qt_color

    def _set_icon_(self, icon):
        self._icon = icon

    def _set_icon_name_enable_(self, boolean):
        self._icon_name_is_enable = boolean

    def _set_icon_file_path_(self, file_path):
        self._icon_is_enable = True
        self._icon_file_path = file_path
        self._widget.update()

    def _set_icon_name_(self, name):
        self._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(name)
        )

    def _set_icon_sub_file_path_(self, file_path):
        self._icon_sub_file_path = file_path
        self._widget.update()

    def _set_icon_sub_text_(self, text):
        self._icon_sub_text = text
        self._widget.update()

    def _set_icon_sub_name_(self, name):
        self._set_icon_sub_file_path_(
            utl_gui_core.RscIconFile.get(name)
        )

    def _set_icon_state_name_(self, name):
        self._set_icon_state_file_path_(
            utl_gui_core.RscIconFile.get(name)
        )

    def _set_icon_state_file_path_(self, file_path):
        self._set_icon_state_draw_enable_(True)
        self._icon_state_file_path = file_path

    def _set_hover_icon_file_path_(self, file_path):
        self._hover_icon_file_path = file_path

    def _set_icon_frame_draw_size_(self, w, h):
        self._icon_frame_draw_size = w, h

    def _set_icon_file_draw_size_(self, w, h):
        self._icon_draw_size = w, h

    def _set_icon_file_draw_percent_(self, p):
        self._icon_draw_percent = p

    def _get_icon_file_path_(self):
        if self._icon_is_enable is True:
            return self._icon_file_path

    def _set_color_icon_rgb_(self, rgb):
        self._icon_is_enable = True
        self._icon_color_rgb = rgb
        self._widget.update()

    def _set_icon_text_(self, text):
        self._icon_is_enable = True
        self._icon_name_text = text
        self._widget.update()

    def _set_color_icon_rect_(self, x, y, w, h):
        self._icon_color_draw_rect.setRect(
            x, y, w, h
        )

    def _set_icon_name_draw_rect_(self, x, y, w, h):
        self._icon_name_draw_rect.setRect(
            x, y, w, h
        )

    def _get_icon_name_text_(self):
        if self._icon_is_enable is True:
            return self._icon_name_text

    def _set_icon_frame_draw_rect_(self, x, y, w, h):
        self._icon_frame_draw_rect.setRect(
            x, y, w, h
        )

    def _set_icon_file_draw_rect_(self, x, y, w, h):
        self._icon_draw_rect.setRect(
            x, y, w, h
        )

    def _set_sub_icon_file_draw_rect_(self, x, y, w, h):
        self._icon_sub_draw_rect.setRect(
            x, y, w, h
        )

    def _get_file_icon_rect_(self):
        return self._icon_draw_rect


class AbsQtIconsDef(object):
    def _init_icons_def_(self, widget):
        self._widget = widget
        #
        self._icons_enable = False
        self._icon_pixmaps = []
        self._icon_file_paths = []
        self._icon_name_texts = []
        self._icon_indices = []
        self._icon_rects = []
        #
        self._icon_frame_draw_size = 20, 20
        self._icon_draw_size = 16, 16
        self._icon_frame_draw_enable = False
        #
        self._icon_frame_draw_rect = QtCore.QRect()

    def _set_icon_file_path_(self, file_path):
        self._set_icon_file_paths_(
            [file_path]
        )

    def _set_icon_file_path_at_(self, file_path, index=0):
        self._icon_file_paths[index] = file_path

    def _get_icon_file_path_at_(self, index=0):
        if index in self._get_icon_indices_():
            return self._icon_file_paths[index]

    def _set_icon_rect_at_(self, x, y, w, h, index=0):
        self._icon_rects[index].setRect(
            x, y, w, h
        )

    def _get_icon_rect_at_(self, index=0):
        if index in self._get_icon_indices_():
            return self._icon_rects[index]

    def _set_icon_pixmaps_(self, pixmaps):
        self._icon_pixmaps = pixmaps
        self._icon_indices = range(len(pixmaps))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _get_icon_as_pixmap_at_(self, index):
        if index in self._get_icon_indices_():
            return self._icon_pixmaps[index]

    def _get_icons_as_pixmap_(self):
        return self._icon_pixmaps

    def _set_icon_file_paths_(self, file_paths):
        self._icon_file_paths = file_paths
        self._icon_indices = range(len(self._icon_file_paths))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _set_icons_by_name_text_(self, texts):
        self._icon_name_texts = texts
        self._icon_indices = range(len(self._icon_name_texts))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _get_icon_name_text_at_(self, index=0):
        return self._icon_name_texts[index]

    def _set_icon_name_rect_at_(self, index, name_text):
        self._icon_name_texts[index] = name_text

    def _set_icon_file_path_add_(self, file_path):
        self._icon_file_paths.append(file_path)
        self._icon_rects.append(QtCore.QRect())

    def _get_icon_file_paths_(self):
        return self._icon_file_paths

    def _get_icon_indices_(self):
        return self._icon_indices

    def _get_has_icons_(self):
        return self._icon_indices != []

    def _get_icon_count_(self):
        return len(self._icon_indices)

    def _set_icon_frame_draw_size_(self, w, h):
        self._icon_frame_draw_size = w, h

    def _set_icon_size_(self, w, h):
        self._icon_draw_size = w, h

    def _set_icon_frame_draw_enable_(self, boolean):
        self._icon_frame_draw_enable = boolean


class AbsQtIndexDef(object):
    def _init_index_def_(self):
        self._index_draw_enable = False
        self._index = 0
        self._index_text = None
        self._index_text_color = QtFontColors.Dark
        self._index_text_font = Font.INDEX
        self._index_text_option = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        #
        self._index_frame_rect = QtCore.QRect()
        self._index_rect = QtCore.QRect()
        #
        self._index_frame_draw_enable = False
        self._index_draw_enable = False

    def _set_index_draw_enable_(self, boolean):
        self._index_draw_enable = boolean

    def _set_index_(self, index):
        self._index = index
        self._index_text = str(index + 1)

    def _get_index_(self):
        return self._index

    def _get_index_text_(self):
        return self._index_text

    def _set_index_draw_rect_(self, x, y, w, h):
        self._index_rect.setRect(
            x, y, w, h
        )

    def _get_index_rect_(self):
        return self._index_rect


class AbsQtTypeDef(object):
    def _init_type_def_(self, widget):
        self._widget = widget
        #
        self._type_text = None
        self._type_rect = QtCore.QRect()
        self._type_color = QtGui.QColor(127, 127, 127, 255)

    def _set_type_text_(self, text):
        self._type_text = text or ''
        self._type_color = bsc_core.RawTextOpt(
            self._type_text
        ).to_rgb()

    def _set_type_draw_rect_(self, x, y, w, h):
        self._type_rect.setRect(
            x, y, w, h
        )


class AbsQtPathBaseDef(object):
    def _init_path_base_def_(self, widget):
        self._widget = widget

        self._path_text = None
        self._path_rect = QtCore.QRect()

    def _set_path_text_(self, text):
        self._path_text = text
        self._widget.update()

    def _get_path_text_(self):
        return self._path_text

    def _set_path_rect_(self, x, y, w, h):
        self._path_rect.setRect(x, y, w, h)


class AbsQtValueBaseDef(object):
    def _init_value_base_def_(self, widget):
        self._widget = widget

        self._value = None

    def _set_value_(self, value):
        self._value = value

    def _get_value_(self):
        return self._value


class AbsQtNameBaseDef(object):
    AlignRegion = utl_gui_configure.AlignRegion
    def _init_name_base_def_(self, widget):
        self._widget = widget
        #
        self._name_enable = False
        self._name_text = None
        self._name_text_orig = None
        self._name_draw_font = Font.NAME
        #
        self._name_align = self.AlignRegion.Center
        #
        self._name_color = QtFontColors.Basic
        self._hover_name_color = QtFontColors.Light
        self._name_text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        #
        self._name_word_warp = True
        #
        self._name_width = 160
        #
        self._name_frame_size = 20, 20
        self._name_draw_size = 16, 16
        self._name_frame_draw_rect = QtCore.QRect()
        self._name_draw_rect = QtCore.QRect()

        self._tool_tip_text = None

    def _set_name_align_(self, align):
        self._name_align = align

    def _set_name_color_(self, color):
        self._name_color = color

    def _get_name_text_draw_width_(self, text=None):
        if text is None:
            text = self._name_text
        # print self._widget.fontMetrics().width(text), text
        return self._widget.fontMetrics().width(text)

    def _set_name_text_(self, text):
        self._name_enable = True
        self._name_text = text
        #
        if self._tool_tip_text is not None:
            self._set_tool_tip_text_(self._tool_tip_text)
        #
        self._widget.update()

    def _get_name_text_(self):
        if self._name_enable is True:
            return self._name_text

    def _get_name_text_option_(self):
        return self._name_text_option

    def _set_name_text_option_(self, option):
        self._name_text_option = option

    def _set_name_width_(self, w):
        self._name_width = w

    def _set_name_frame_rect_(self, x, y, w, h):
        self._name_frame_draw_rect.setRect(
            x, y, w, h
        )

    def _set_name_draw_rect_(self, x, y, w, h):
        self._name_draw_rect.setRect(
            x, y, w, h
        )

    def _get_name_rect_(self):
        return self._name_draw_rect

    def _set_tool_tip_(self, raw, **kwargs):
        if isinstance(raw, (tuple, list)):
            _ = '\n'.join(raw)
        elif isinstance(raw, six.string_types):
            _ = raw
        else:
            raise TypeError()
        #
        self._set_tool_tip_text_(_, **kwargs)

    def _set_tool_tip_text_(self, text, **kwargs):
        self._tool_tip_text = text
        if hasattr(self, 'setToolTip'):
            if isinstance(text, six.text_type):
                text = text.encode('utf-8')
            text = text.replace(' ', '&nbsp;')
            text = text.replace('<', '&lt;')
            text = text.replace('>', '&gt;')
            #
            css = '<html>\n<body>\n<style>.no_wrap{white-space:nowrap;}</style>\n<style>.no_warp_and_center{white-space:nowrap;text-align: center;}</style>\n'
            name_text = self._name_text
            if 'name' in kwargs:
                name_text = kwargs['name']
            #
            if name_text:
                if isinstance(name_text, six.text_type):
                    name_text = name_text.encode('utf-8')
                #
                name_text = name_text.replace('<', '&lt;').replace('>', '&gt;')
                css += '<h3><p class="no_warp_and_center">{}</p></h3>\n'.format(name_text)
            # add split line
            css += '<p><hr></p>\n'
            if isinstance(text, six.string_types):
                texts = text.split('\n')
            else:
                texts = text
            #
            for i_text in texts:
                if '"LMB-click"' in i_text:
                    i_text = i_text.replace(
                        '"LMB-click"',
                        '<img src="{}">\n"LMB-click"'.format(
                            utl_gui_core.RscIconFile.get('mouse/LMB-click')
                        )
                    )
                if '"LMB-move"' in i_text:
                    i_text = i_text.replace(
                        '"LMB-move"',
                        '<img src="{}">\n"LMB-move"'.format(
                            utl_gui_core.RscIconFile.get('mouse/LMB-click')
                        )
                    )
                if '"RMB-click"' in i_text:
                    i_text = i_text.replace(
                        '"RMB-click"',
                        '<img src="{}">\n"RMB-click"'.format(
                            utl_gui_core.RscIconFile.get('mouse/RMB-click')
                        )
                    )
                if '"MMB-wheel"' in i_text:
                    i_text = i_text.replace(
                        '"MMB-wheel"',
                        '<img src="{}">\n"MMB-wheel"'.format(
                            utl_gui_core.RscIconFile.get('mouse/MMB-wheel')
                        )
                    )
                css += '<p class="no_wrap">{}</p>\n'.format(i_text)
            #
            css += '</body>\n</html>'
            # noinspection PyCallingNonCallable
            # self._tool_tip_text = css
            self.setToolTip(css)

    def _set_name_font_size_(self, size):
        font = self._widget.font()
        font.setPointSize(size)
        self._name_draw_font = font
        self._widget.setFont(self._name_draw_font)

    def _set_name_draw_font_(self, font):
        self._name_draw_font = font
        self._widget.setFont(self._name_draw_font)

    def _set_name_text_orig_(self, text):
        self._name_text_orig = text

    def _get_name_text_orig_(self):
        return self._name_text_orig


class AbsQtNamesBaseDef(AbsQtNameBaseDef):
    def _refresh_widget_(self):
        pass

    def _init_names_base_def_(self, widget):
        self._init_name_base_def_(widget)
        #
        self._widget = widget
        #
        self._names_enable = False
        self._name_texts = []
        self._name_indices = []
        self._name_draw_rects = []
        #
        self._name_text_dict = collections.OrderedDict()
        self._name_key_rect = []
        self._name_value_rect = []
        #
        self._name_frame_size = 20, 20
        self._name_size = 16, 16
        self._name_frame_draw_enable = False
        #
        self._name_word_warp = True
        #
        self._name_frame_border_color = 0, 0, 0, 0
        self._name_frame_background_color = 95, 95, 95, 127
        #
        self._names_draw_range = None
        #
        self._name_frame_draw_rect = QtCore.QRect(0, 0, 0, 0)

    def _set_name_text_at_(self, text, index=0):
        self._name_texts[index] = text

    def _get_name_text_at_(self, index=0):
        if index in self._get_name_indices_():
            return self._name_texts[index]

    def _set_name_text_draw_rect_at_(self, x, y, w, h, index=0):
        self._name_draw_rects[index].setRect(
            x, y, w, h
        )

    def _set_name_text_(self, text):
        self._set_name_texts_([text])
        self._name_text = text

    def _get_name_text_(self):
        if self._name_texts:
            return self._name_texts[0]
        return self._name_text

    def _set_name_texts_(self, texts):
        self._name_texts = texts
        self._name_indices = range(len(texts))
        self._name_draw_rects = []
        for _ in self._get_name_indices_():
            self._name_draw_rects.append(
                QtCore.QRect()
            )
        #
        self._refresh_widget_()

    def _get_name_texts_(self):
        return self._name_texts

    def _set_name_text_dict_(self, text_dict):
        self._name_text_dict = text_dict
        self._set_name_texts_(
            [v if seq == 0 else '{}: {}'.format(k, v) for seq, (k, v) in enumerate(self._name_text_dict.items())]
        )
        self._refresh_widget_()

    def _get_show_name_texts_(self):
        if self._name_text_dict:
            return ['{}: {}'.format(k, v) for seq, (k, v) in enumerate(self._name_text_dict.items())]
        return self._get_name_texts_()

    def _get_name_text_dict_(self):
        return self._name_text_dict

    def _set_names_draw_range_(self, range_):
        self._names_draw_range = range_

    def _set_name_frame_border_color_(self, color):
        self._name_frame_border_color = color

    def _get_name_frame_border_color_(self):
        return self._name_frame_border_color

    def _set_name_frame_background_color_(self, color):
        self._name_frame_background_color = color

    def _get_name_frame_background_color_(self):
        return self._name_frame_background_color

    def _get_name_rect_at_(self, index=0):
        return self._name_draw_rects[index]

    def _get_name_indices_(self):
        return self._name_indices

    def _get_has_names_(self):
        return self._name_indices != []

    def _set_name_frame_size_(self, w, h):
        self._name_frame_size = w, h

    def _set_name_size_(self, w, h):
        self._name_size = w, h

    def _set_name_frame_draw_enable_(self, boolean):
        self._name_frame_draw_enable = boolean

    def _set_tool_tip_(self, raw, **kwargs):
        if raw is not None:
            if isinstance(raw, (tuple, list)):
                _ = u'\n'.join(raw)
            elif isinstance(raw, six.string_types):
                _ = raw
            else:
                raise TypeError()
            #
            self._set_tool_tip_text_(_, **kwargs)

    def _set_tool_tip_text_(self, text, **kwargs):
        if hasattr(self, 'setToolTip'):
            css = u'<html>\n<body>\n<style>.no_wrap{white-space:nowrap;float:right;}</style>\n<style>.no_warp_and_center{white-space:nowrap;text-align:center;}</style>\n'
            #
            name_text = self._name_text
            if name_text:
                css += u'<h2><p class="no_warp_and_center">{}</p></h2>\n'.format(name_text)
                css += u'<p><hr></p>\n'
            #
            texts = self._get_show_name_texts_()
            if texts:
                for seq, i_text in enumerate(texts):
                    i_text = i_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                    css += u'<p class="no_wrap">{}</p>\n'.format(i_text)
            #
            css += u'<p><hr></p>\n'
            if isinstance(text, six.string_types):
                texts_extend = text.split('\n')
            else:
                texts_extend = text
            #
            for i_text in texts_extend:
                i_text = i_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                css += u'<p class="no_wrap">{}</p>\n'.format(i_text)
            css += u'</body>\n</html>'
            self.setToolTip(css)


class AbsQtRgbaDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_rgba_def_init_(self):
        self._color_rgba = 1.0, 1.0, 1.0, 1.0
        self._color_rect = QtCore.QRect()

    def _set_color_rgba_(self, r, g, b, a):
        self._color_rgba = r, g, b, a
        self._refresh_widget_draw_()

    def _get_color_rgba_(self):
        return self._color_rgba

    def _get_color_rgba_255_(self):
        return tuple(map(lambda x: int(x*255), self._color_rgba))

    def _get_color_rect_(self):
        return self._color_rect


class AbsQtProgressDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_geometry_(self):
        pass

    def _set_progress_def_init_(self):
        self._progress_height = 2
        #
        self._progress_maximum = 0
        self._progress_value = 0
        #
        self._progress_map_maximum = 10
        self._progress_map_value = 0
        #
        self._progress_rect = QtCore.QRect()
        #
        self._progress_raw = []

    def _set_progress_height_(self, value):
        self._progress_height = value

    def _set_progress_run_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()
        #
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_progress_maximum_(self, value):
        self._progress_maximum = value

    def _set_progress_map_maximum_(self, value):
        self._progress_map_maximum = value

    def _set_progress_value_(self, value):
        self._progress_value = value
        #
        if self._progress_map_maximum > 1:
            map_value = int(
                bsc_core.RawValueRangeMtd.set_map_to(
                    (1, self._progress_maximum), (1, self._progress_map_maximum),
                    self._progress_value
                )
            )
            self._set_progress_map_value_(map_value)

    def _set_progress_map_value_(self, map_value):
        if map_value != self._progress_map_value:
            self._progress_map_value = map_value
            #
            self._set_progress_run_()

    def _set_progress_update_(self):
        self._set_progress_value_(self._progress_value + 1)

    def _stop_progress_(self):
        self._set_progress_value_(0)
        self._progress_raw = []
        #
        self._refresh_widget_draw_()

    def _get_progress_percent_(self):
        return float(self._progress_map_value) / float(self._progress_map_maximum)

    def _set_progress_raw_(self, raw):
        self._progress_raw = raw

    def _get_progress_is_enable_(self):
        return self._progress_map_value != 0


class AbsQtImageBaseDef(object):
    def _init_image_base_def_(self):
        self._image_enable = False
        self._image_draw_is_enable = False
        #
        self._image_file_path = None
        self._image_sub_file_path = None
        self._image_text = None
        self._image_data = None
        self._image_pixmap = None
        #
        self._image_frame_size = 32, 32
        self._image_draw_size = 30, 30
        self._image_draw_percent = .75
        self._image_frame_draw_enable = False
        #
        self._image_frame_rect = QtCore.QRect(0, 0, 0, 0)
        self._image_draw_rect = QtCore.QRect(0, 0, 0, 0)
        self._image_sub_draw_rect = QtCore.QRect(0, 0, 0, 0)

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_image_file_path_(self, arg):
        self._image_enable = True
        self._image_draw_is_enable = True
        if isinstance(arg, six.string_types):
            self._image_file_path = arg
        elif isinstance(arg, QtGui.QPixmap):
            self._image_pixmap = arg
        self._refresh_widget_draw_()

    def _set_image_sub_file_path_(self, file_path):
        self._image_sub_file_path = file_path
        self._refresh_widget_draw_()

    def _set_image_text_(self, text):
        self._image_text = text
        self._refresh_widget_draw_()

    def _set_image_url_(self, url):
        self._image_draw_is_enable = True
        # noinspection PyBroadException
        try:
            self._image_data = urllib.urlopen(url).read()
        except:
            pass

        self._refresh_widget_draw_()

    def _set_image_draw_enable_(self, boolean):
        self._image_draw_is_enable = boolean

    def _get_image_data(self):
        if self._image_enable is True:
            return self._image_data

    def _set_image_draw_size_(self, w, h):
        self._image_draw_size = w, h

    def _get_image_draw_size_(self):
        return self._image_draw_size

    def _get_image_size_(self):
        if self._image_file_path is not None:
            if os.path.isfile(self._image_file_path):
                ext = os.path.splitext(self._image_file_path)[-1]
                if ext in ['.jpg', '.png']:
                    image = QtGui.QImage(self._image_file_path)
                    if image.isNull() is False:
                        # image.save(self._image_file_path, 'PNG')
                        s = image.size()
                        return s.width(), s.height()
                elif ext in ['.mov']:
                    pass
        return self._image_draw_size

    def _get_image_file_path_(self):
        if self._image_enable is True:
            return self._image_file_path

    def _set_image_rect_(self, x, y, w, h):
        self._image_draw_rect.setRect(
            x, y, w, h
        )

    def _get_image_rect_(self):
        return self._image_draw_rect

    def _get_has_image_(self):
        return (
                self._image_file_path is not None or
                self._image_sub_file_path is not None or
                self._image_text is not None or
                self._image_pixmap is not None
        )

    def _set_image_frame_draw_enable_(self, boolean):
        self._image_frame_draw_enable = boolean

    def _get_image_frame_rect_(self):
        return self._image_frame_rect


class AbsQtMovieDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()
    #
    def _set_movie_def_init_(self):
        self._play_draw_enable = False
        self._movie_rect = QtCore.QRect()

    def _get_play_draw_is_enable_(self):
        return self._play_draw_enable

    def _set_play_draw_enable_(self, boolean):
        self._play_draw_enable = boolean

    def _set_movie_rect_(self, x, y, w, h):
        self._movie_rect.setRect(x, y, w, h)


class AbsQtChartBaseDef(object):
    def _init_chart_base_def_(self, widget):
        self._widget = widget
        self._chart_data = None
        self._chart_draw_data = None
        self._chart_mode = utl_gui_configure.SectorChartMode.Completion
        #
        self._hover_flag = False
        self._hover_point = QtCore.QPoint()
        #
        r, g, b = 143, 143, 143
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._chart_border_color = color
        self._hover_chart_border_color = hover_color
        self._chart_background_color = 39, 39, 39, 255
        #
        self._chart_text_color = 0, 0, 0, 255

    def _set_chart_data_(self, data, mode):
        self._chart_data = data
        self._chart_mode = mode
        #
        self._refresh_chart_data_()
        #
        self._set_chart_data_post_run_()
        #
        self._widget.update()

    def _set_chart_data_post_run_(self):
        pass

    def _refresh_chart_data_(self):
        raise NotImplementedError()

    def _set_height_(self, h):
        # noinspection PyUnresolvedReferences
        self.setMaximumHeight(h)
        # noinspection PyUnresolvedReferences
        self.setMinimumHeight(h)


class AbsQtActionBaseDef(object):
    ActionFlag = utl_gui_configure.ActionFlag
    ActionState = bsc_configure.ActionState
    def _init_action_base_def_(self, widget):
        self._widget = widget
        self._action_flag = None
        #
        self._action_is_enable = True
        #
        self._action_mdf_flags = []

        self._action_state = self.ActionState.Normal
        self._action_state_rect = QtCore.QRect()

        self._action_is_busied = False

    def _get_action_is_busied_(self):
        return self._action_is_busied

    def _set_action_busied_(self, boolean):
        self._action_is_busied = boolean
        if boolean is True:
            self._widget.setCursor(QtCore.Qt.BusyCursor)
        else:
            self._widget.unsetCursor()

    def _set_action_enable_(self, boolean):
        self._action_is_enable = boolean
        if boolean is False:
            self._action_state = self.ActionState.Disable
        else:
            self._action_state = self.ActionState.Enable
        #
        self._widget._refresh_widget_draw_geometry_()
        self._widget._refresh_widget_draw_()

    def _get_action_is_enable_(self):
        return self._action_is_enable

    def _set_action_flag_(self, flag):
        if flag is not None:
            self._action_flag = flag
            self._update_action_cursor_()
        #
        self._widget.update()

    def _set_action_mdf_flags_(self, flags):
        self._action_mdf_flags = flags

    def _set_action_mdf_flag_add_(self, flag):
        if flag is not None:
            if flag not in self._action_mdf_flags:
                self._action_mdf_flags.append(flag)
        #
        self._widget.update()

    def _update_action_cursor_(self):
        if self._action_is_busied is False:
            if self._action_flag is not None:
                if self._action_flag in {
                    self.ActionFlag.PressClick,
                    self.ActionFlag.PressDbClick,
                    #
                    self.ActionFlag.TrackClick,
                    #
                    self.ActionFlag.CheckClick,
                    self.ActionFlag.ExpandClick,
                    self.ActionFlag.OptionClick,
                    self.ActionFlag.ChooseClick,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtCore.Qt.PointingHandCursor
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.PressMove,
                }:
                    self._widget.setCursor(
                        QtCore.Qt.OpenHandCursor
                    )
                elif self._action_flag in {
                    self.ActionFlag.TrackMove,
                    self.ActionFlag.ZoomMove,
                    self.ActionFlag.NGNodePressMove
                }:
                    p = QtGui.QPixmap(20, 20)
                    p.load(utl_gui_core.RscIconFile.get('system/track-move'))
                    self._widget.setCursor(
                        QtGui.QCursor(
                            p,
                            10, 10
                        )
                    )
                elif self._action_flag in [
                    self.ActionFlag.TrackCircle,
                ]:
                    p = QtGui.QPixmap(20, 20)
                    p.load(utl_gui_core.RscIconFile.get('system/track-circle'))
                    self._widget.setCursor(
                        QtGui.QCursor(
                            p,
                            10, 10
                        )
                    )
                # split
                elif self._action_flag in {
                    self.ActionFlag.SplitHHover,
                    self.ActionFlag.SplitHPress,
                    self.ActionFlag.SplitHMove,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/resize-h'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.SplitVHover,
                    self.ActionFlag.SplitVPress,
                    self.ActionFlag.SplitVMove
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/resize-v'))
                        )
                    )
                # resize
                elif self._action_flag in {
                    self.ActionFlag.ResizeLeft,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/resize-left'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.ResizeRight,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/resize-right'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.ResizeUp,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/resize-up'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.ResizeDown,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/resize-down'))
                        )
                    )
                # swap
                elif self._action_flag in {
                    self.ActionFlag.SwapH,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/swap-h'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.SwapV,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(utl_gui_core.RscIconFile.get('system/swap-v'))
                        )
                    )
                #
                elif self._action_flag in {
                    self.ActionFlag.RectSelectMove,
                }:
                    p = QtGui.QPixmap(20, 20)
                    p.load(utl_gui_core.RscIconFile.get('system/rect-select'))
                    self._widget.setCursor(
                        QtGui.QCursor(
                            p,
                            10, 10
                        )
                    )
            else:
                self._widget.unsetCursor()

    def _get_action_flag_(self):
        return self._action_flag

    def _clear_all_action_flags_(self):
        self._action_flag = None
        #
        self._update_action_cursor_()
        #
        self._widget.update()

    def _set_action_mdf_flag_clear_(self):
        self._action_mdf_flags = []
        self._widget.update()

    def _get_action_flag_is_match_(self, *args):
        if isinstance(args, int):
            return self._action_flag == args[0]
        elif isinstance(args, (tuple, list)):
            return self._action_flag in args

    def _get_action_mdf_flags_is_include_(self, flag):
        return flag in self._action_mdf_flags

    def _get_action_mdf_flags_(self):
        return self._action_mdf_flags

    def _get_is_actioned_(self):
        return self._action_flag is not None

    def _get_action_offset_(self):
        if self._action_flag is not None:
            return 2
        return 0

    def _set_action_state_(self, state):
        self._action_flag = state

    def _get_action_state_(self):
        return self._action_state


class AbsQtActionForHoverDef(object):
    def _init_action_for_hover_def_(self, widget):
        self._widget = widget
        #
        self._is_hovered = False

    def _set_action_hovered_(self, boolean):
        self._is_hovered = boolean
        #
        self._widget.update()

    def _get_is_hovered_(self):
        return self._is_hovered

    def _execute_action_hover_by_filter_(self, event):
        if event.type() == QtCore.QEvent.Enter:
            self._set_action_hovered_(True)
        elif event.type() == QtCore.QEvent.Leave:
            self._set_action_hovered_(False)

    def _do_hover_move_(self, event):
        pass


class AbsQtActionForPressDef(object):
    pressed = qt_signal()
    press_clicked = qt_signal()
    press_db_clicked = qt_signal()
    press_toggled = qt_signal(bool)
    #
    clicked = qt_signal()
    #
    ActionFlag = utl_gui_configure.ActionFlag

    def _init_action_for_press_def_(self, widget):
        self._widget = widget
        #
        self._press_is_enable = True
        self._is_pressed = False
        #
        self._press_is_hovered = False
        #
        self._press_action_rect = QtCore.QRect()

        self._action_press_db_clicked_methods = []

    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _get_action_flag_is_match_(self, flag):
        raise NotImplementedError()

    def _get_action_press_is_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._press_is_enable
        return False

    def _set_pressed_(self, boolean):
        self._is_pressed = boolean
        self._widget.update()

    def _get_is_pressed_(self):
        return self._is_pressed

    def _send_press_clicked_emit_(self):
        self.clicked.emit()
        self.press_clicked.emit()

    def _set_action_press_db_click_emit_send_(self):
        self.press_db_clicked.emit()

    def _get_action_press_flag_is_click_(self):
        return self._get_action_flag_is_match_(
            self.ActionFlag.PressClick
        )

    def _set_action_press_db_clicked_method_add_(self, fnc):
        self._action_press_db_clicked_methods.append(fnc)


class AbsQtCheckBaseDef(object):
    check_clicked = qt_signal()
    check_toggled = qt_signal(bool)
    user_check_clicked = qt_signal()
    user_check_toggled = qt_signal(bool)
    #
    user_check_clicked_as_exclusive = qt_signal()
    check_changed_as_exclusive = qt_signal()
    check_swapped_as_exclusive = qt_signal()
    #
    ActionFlag = utl_gui_configure.ActionFlag
    def _init_check_base_def_(self, widget):
        self._widget = widget
        #
        self._check_action_is_enable = False
        #
        self._is_checked = False
        self._check_rect = QtCore.QRect()
        self._check_icon_frame_draw_rect = QtCore.QRect()
        self._check_icon_draw_rect = QtCore.QRect()
        self._check_is_pressed = False
        self._check_is_hovered = False
        #
        self._check_icon_frame_draw_percent = .875
        self._check_icon_frame_draw_size = 20, 20
        self._check_icon_draw_percent = .8
        self._check_icon_draw_size = 16, 16
        #
        self._check_icon_file_path_0 = utl_gui_core.RscIconFile.get('box_unchecked')
        self._check_icon_file_path_1 = utl_gui_core.RscIconFile.get('box_checked')
        self._check_icon_file_path_current = self._check_icon_file_path_0

        self._check_is_enable = False

        self._check_exclusive_widgets = []

        self._check_state_draw_rect = QtCore.QRect()

    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _set_check_action_enable_(self, boolean):
        self._check_action_is_enable = boolean

    def _get_check_action_is_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._check_action_is_enable
        return False

    def _set_check_enable_(self, boolean):
        self._check_is_enable = boolean

    def _get_check_is_enable_(self):
        return self._check_is_enable

    def _set_checked_(self, boolean):
        self._is_checked = boolean
        self.check_clicked.emit()
        self.check_toggled.emit(boolean)
        self._refresh_check_draw_()

    def _set_exclusive_widgets_(self, widgets):
        self._check_exclusive_widgets = widgets

    def _get_is_checked_(self):
        return self._is_checked

    def _execute_check_swap_(self):
        if self._check_exclusive_widgets:
            self._update_check_exclusive_()
        else:
            self._set_checked_(not self._is_checked)
        #
        self._refresh_check_draw_()

    def _update_check_exclusive_(self):
        if self._check_exclusive_widgets:
            for i in self._check_exclusive_widgets:
                if i == self:
                    value_pre = self._get_is_checked_()
                    self._set_checked_(True)
                    if value_pre is not True:
                        self.check_changed_as_exclusive.emit()
                    else:
                        self.check_swapped_as_exclusive.emit()
                    #
                    self.user_check_clicked_as_exclusive.emit()
                else:
                    i._set_checked_(False)

    def _refresh_check_draw_(self):
        self._check_icon_file_path_current = [
            self._check_icon_file_path_0, self._check_icon_file_path_1
        ][self._is_checked]
        #
        self._widget.update()

    def _set_check_icon_frame_draw_rect_(self, x, y, w, h):
        self._check_icon_frame_draw_rect.setRect(
            x, y, w, h
        )

    def _set_check_action_rect_(self, x, y, w, h):
        self._check_rect.setRect(
            x, y, w, h
        )

    def _set_check_icon_draw_rect_(self, x, y, w, h):
        self._check_icon_draw_rect.setRect(
            x, y, w, h
        )

    def _send_check_emit_(self):
        self._execute_check_swap_()
        #
        self.user_check_clicked.emit()
        self.user_check_toggled.emit(self._is_checked)

    def _set_item_check_changed_connect_to_(self, fnc):
        self.check_clicked.connect(fnc)

    def _set_action_check_execute_(self, event):
        self._execute_check_swap_()

    def _set_check_icon_file_paths_(self, file_path_0, file_path_1):
        self._check_icon_file_path_0 = file_path_0
        self._check_icon_file_path_1 = file_path_1
        self._refresh_check_draw_()

    def _get_action_check_is_valid_(self, event):
        if self._check_action_is_enable is True:
            p = event.pos()
            return self._check_rect.contains(p)
        return False


class AbsQtActionForExpandDef(object):
    class ExpandDirection(enum.IntEnum):
        TopToBottom = 0
        BottomToTop = 1

    class CollapseDirection(enum.IntEnum):
        RightToLeft = 0
        LeftToRight = 1
    #
    expand_clicked = qt_signal()
    expand_toggled = qt_signal(bool)
    #
    EXPAND_TOP_TO_BOTTOM = 0
    EXPAND_BOTTOM_TO_TOP = 1
    #
    ActionFlag = utl_gui_configure.ActionFlag

    def _init_action_for_expand_def_(self, widget):
        self._widget = widget
        #
        self._is_expand_enable = False
        #
        self._expand_icon_file_path = None
        self._expand_icon_file_path_0 = utl_gui_core.RscIconFile.get('box_checked')
        self._expand_icon_file_path_1 = utl_gui_core.RscIconFile.get('box_unchecked')
        self._is_expanded = False
        #
        self._expand_frame_rect = QtCore.QRect()
        self._expand_icon_draw_rect = QtCore.QRect()
        #
        self._expand_direction = self.ExpandDirection.TopToBottom

    def _set_expanded_(self, boolean):
        self._is_expanded = boolean
        self._refresh_expand_()

    def _get_is_expanded_(self):
        return self._is_expanded

    def _swap_expand_(self):
        self._is_expanded = not self._is_expanded
        self._refresh_expand_()

    def _refresh_expand_(self):
        pass

    def _set_expand_direction_(self, direction):
        self._expand_direction = direction
        self._refresh_expand_()

    def _execute_action_expand_(self):
        self._swap_expand_()
        # noinspection PyUnresolvedReferences
        self.expand_clicked.emit()
        self.expand_toggled.emit(self._is_expanded)


class AbsQtActionForOptionPressDef(object):
    checked = qt_signal()
    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _init_action_for_option_press_def_(self, widget):
        self._widget = widget
        #
        self._option_click_is_enable = False
        self._option_icon_file_path = utl_gui_core.RscIconFile.get('option')
        #
        self._option_click_rect = QtCore.QRect()
        self._option_click_icon_rect = QtCore.QRect()

    def _set_option_click_enable_(self, boolean):
        self._option_click_is_enable = boolean
        #
        self._widget.update()

    def _get_option_click_is_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._option_click_is_enable
        return False


class AbsQtThreadBaseDef(object):
    def _init_thread_base_def_(self, widget):
        self._widget = widget

        self._qt_thread_enable = bsc_core.EnvironMtd.get_qt_thread_enable()

        self._thread_draw_is_enable = False
        self._thread_load_index = 0

        self._thread_running_timer = QtCore.QTimer()
        self._thread_running_timer.timeout.connect(self._refresh_thread_draw_)

        self._threads = []

    def _set_action_busied_(self, *args, **kwargs):
        raise NotImplementedError()

    def _start_thread_draw_(self):
        self._set_action_busied_(True)
        self._thread_draw_is_enable = True
        self._thread_load_index = 0
        self._thread_running_timer.start(100)
        self._refresh_thread_draw_()

    def _stop_thread_draw_(self):
        self._set_action_busied_(False)
        self._thread_draw_is_enable = False
        self._thread_running_timer.stop()
        self._thread_load_index = 0
        self._refresh_thread_draw_()

    def _thread_start_accept_fnc_(self, thread):
        self._threads.append(thread)
        if self._thread_draw_is_enable is False:
            self._start_thread_draw_()

    def _thread_finish_accept_fnc_(self, thread):
        self._threads.remove(thread)
        if not self._threads:
            self._stop_thread_draw_()

    def _refresh_thread_draw_(self):
        self._thread_load_index += 1
        self._widget.update()

    def _run_build_use_thread_(self, cache_fnc, build_fnc, post_fnc):
        if self._qt_thread_enable is True:
            t = QtBuildThread(self._widget)
            t.set_cache_fnc(cache_fnc)
            t.built.connect(build_fnc)
            t.run_finished.connect(post_fnc)
            t.start_accepted.connect(self._thread_start_accept_fnc_)
            t.finish_accepted.connect(self._thread_finish_accept_fnc_)
            t.start()
        else:
            build_fnc(cache_fnc())
            post_fnc()

    def _run_fnc_use_thread_(self, fnc):
        if self._qt_thread_enable is True:
            t = QtMethodThread(self._widget)
            t.append_method(fnc)
            t.start_accepted.connect(self._thread_start_accept_fnc_)
            t.finish_accepted.connect(self._thread_finish_accept_fnc_)
            t.start()


class AbsQtChooseBaseDef(object):
    choose_changed = qt_signal()
    user_choose_changed = qt_signal()
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_choose_base_def_(self):
        self._choose_expand_icon_file_path = utl_gui_core.RscIconFile.get('choose_expand')
        self._choose_collapse_icon_file_path = utl_gui_core.RscIconFile.get('choose_collapse')
        #
        self._choose_is_activated = False

        self._choose_values = []
        self._choose_values_current = []

        self._choose_keyword_filter_dict = {}
        self._choose_tag_filter_dict = {}

        self._choose_item_icon_file_path = None
        self._choose_item_icon_file_path_dict = {}
        self._choose_image_url_dict = {}

        self._choose_multiply_is_enable = False

        self._choose_popup_gui = None

    def _get_choose_is_activated_(self):
        return self._choose_is_activated

    def _set_choose_activated_(self, boolean):
        self._choose_is_activated = boolean

    def _set_item_choose_content_raw_(self, raw):
        if isinstance(raw, (tuple, list)):
            self._choose_values = list(raw)

    def _set_choose_values_(self, values, *args, **kwargs):
        self._choose_values = values

    def _clear_choose_values_(self):
        self._choose_values = []
        self._choose_values_current = []

        self._choose_keyword_filter_dict = {}
        self._choose_tag_filter_dict = {}

        self._choose_item_icon_file_path_dict = {}
        self._choose_image_url_dict = {}

    def _set_choose_keyword_filter_dict_(self, dict_):
        self._choose_keyword_filter_dict = dict_

    def _get_choose_keyword_filter_dict_(self):
        return self._choose_keyword_filter_dict

    def _set_choose_tag_filter_dict_(self, dict_):
        self._choose_tag_filter_dict = dict_

    def _get_choose_tag_filter_dict_(self):
        return self._choose_tag_filter_dict

    def _set_choose_image_url_dict_(self, dict_):
        self._choose_image_url_dict = dict_

    def _get_choose_image_url_dict_(self):
        return self._choose_image_url_dict

    def _get_choose_values_(self):
        return self._choose_values

    def _get_choose_current_values_(self):
        pass

    def _get_choose_value_at_(self, index):
        return self._choose_values[index]

    def _get_choose_current_values_append_(self, value):
        self._choose_values_current.append(value)

    def _extend_choose_current_values_(self, values):
        pass

    def _get_choose_item_icon_file_dict_(self):
        return self._choose_item_icon_file_path_dict

    def _set_choose_item_icon_file_path_at_(self, key, file_path):
        self._choose_item_icon_file_path_dict[key] = file_path

    def _set_choose_item_icon_file_path_(self, file_path):
        self._choose_item_icon_file_path = file_path

    def _get_choose_item_icon_file_path_(self):
        return self._choose_item_icon_file_path

    def _choose_value_completion_gain_fnc_(self, *args, **kwargs):
        return bsc_core.PtnFnmatch.filter(
            self._choose_values, '*{}*'.format(bsc_core.auto_encode((args[0])))
        )


class AbsQtChooseExtraDef(object):
    QT_POPUP_CHOOSE_CLS = None
    # when popup item choose, send choose text form this emit
    user_choose_finished = qt_signal()
    #
    user_choose_text_accepted = qt_signal(str)
    user_choose_texts_accepted = qt_signal(list)
    def _init_choose_extra_def_(self, widget):
        self._widget = widget

    def _get_value_entry_(self):
        raise NotImplementedError()

    def _build_choose_extra_(self, entry_gui, entry_frame_gui):
        self._popup_choose_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._popup_choose_widget._set_popup_auto_resize_enable_(True)
        self._popup_choose_widget._set_popup_entry_(entry_gui)
        self._popup_choose_widget._set_popup_entry_frame_(entry_frame_gui)
        self._popup_choose_widget.hide()
        #
        entry_gui.key_up_pressed.connect(
            self._popup_choose_widget._execute_popup_scroll_to_pre_
        )
        entry_gui.key_down_pressed.connect(
            self._popup_choose_widget._execute_popup_scroll_to_next_
        )
        # when press "Key_Enter"
        entry_gui.user_entry_finished.connect(
            self._popup_choose_widget._execute_popup_end_
        )
        #
        self._popup_choose_widget.user_popup_choose_finished.connect(
            self.user_choose_finished
        )
        self._popup_choose_widget.user_popup_choose_text_accepted.connect(
            self.user_choose_text_accepted.emit
        )
        self._popup_choose_widget.user_popup_choose_texts_accepted.connect(
            self.user_choose_texts_accepted.emit
        )

    def _start_choose_extra_fnc_(self):
        self._popup_choose_widget._execute_popup_start_()

    def _close_choose_extra_fnc_(self):
        self._popup_choose_widget._close_popup_()

    def _set_choose_extra_auto_resize_enable_(self, boolean):
        self._popup_choose_widget._set_popup_auto_resize_enable_(boolean)

    def _get_choose_extra_gui_(self):
        return self._popup_choose_widget

    def _set_choose_extra_tag_filter_enable_(self, boolean):
        self._popup_choose_widget._set_popup_tag_filter_enable_(boolean)

    def _set_choose_extra_keyword_filter_enable_(self, boolean):
        self._popup_choose_widget._set_popup_keyword_filter_enable_(boolean)

    def _set_choose_extra_multiply_enable_(self, boolean):
        self._popup_choose_widget._set_popup_choose_multiply_enable_(boolean)

    def _set_choose_extra_item_size_(self, w, h):
        self._popup_choose_widget._set_popup_item_size_(w, h)


class AbsQtCompletionExtraDef(object):
    """
    for completion entry as a popup choose frame
    """
    QT_POPUP_COMPLETION_CLS = None
    #
    user_completion_finished = qt_signal()
    user_completion_text_accepted = qt_signal(str)
    def _init_completion_extra_def_(self, widget):
        self._widget = widget
        self._completion_extra_gain_fnc = None

    def _build_completion_extra_(self, entry_gui, entry_frame_gui):
        self._completion_value_entry = entry_gui
        self._completion_value_entry_frame = entry_frame_gui
        #
        self._completion_extra_widget = self.QT_POPUP_COMPLETION_CLS(self)
        self._completion_extra_widget.hide()
        self._completion_extra_widget._set_popup_entry_(entry_gui)
        self._completion_extra_widget._set_popup_entry_frame_(entry_frame_gui)
        #
        entry_gui.user_entry_changed.connect(
            self._start_completion_extra_fnc_
        )
        entry_gui.user_entry_cleared.connect(
            self._close_completion_extra_fnc_
        )
        entry_gui.key_up_pressed.connect(
            self._completion_extra_widget._execute_popup_scroll_to_pre_
        )
        entry_gui.key_down_pressed.connect(
            self._completion_extra_widget._execute_popup_scroll_to_next_
        )
        # press entry
        entry_gui.user_entry_finished.connect(
            self._completion_extra_widget._execute_popup_end_
        )
        #
        self._completion_extra_widget.user_popup_choose_finished.connect(
            self.user_completion_finished.emit
        )
        self._completion_extra_widget.user_popup_choose_text_accepted.connect(
            self.user_completion_text_accepted.emit
        )

    def _set_completion_extra_gain_fnc_(self, fnc):
        self._completion_extra_gain_fnc = fnc

    def _get_completion_extra_data_(self):
        if self._completion_extra_gain_fnc is not None:
            keyword = self._completion_value_entry._get_value_()
            return self._completion_extra_gain_fnc(keyword) or []
        return []
    #
    def _start_completion_extra_fnc_(self):
        self._completion_extra_widget._execute_popup_start_()

    def _close_completion_extra_fnc_(self):
        self._completion_extra_widget._close_popup_()


class AbsQtHistoryExtraDef(object):
    QT_POPUP_HISTORY_CLS = None
    user_history_text_accepted = qt_signal(str)
    def _init_history_as_extra_def_(self, widget):
        self._widget = widget
        self._history_extra_is_enable = False
        self._history_extra_key = None
        self._history_extra_value_validation_fnc = None

    def _build_history_extra_(self, entry_gui, entry_frame_gui):
        self._history_extra_widget = self.QT_POPUP_HISTORY_CLS(self)
        self._history_extra_widget._set_popup_name_text_('choose a record ...')
        self._history_extra_widget._set_popup_entry_(entry_gui)
        self._history_extra_widget._set_popup_entry_frame_(entry_frame_gui)
        entry_gui.key_up_pressed.connect(
            self._history_extra_widget._execute_popup_scroll_to_pre_
        )
        entry_gui.key_down_pressed.connect(
            self._history_extra_widget._execute_popup_scroll_to_next_
        )
        self._history_extra_widget.hide()

        self._history_extra_widget.user_popup_choose_text_accepted.connect(
            self.user_history_text_accepted.emit
        )

    def _set_history_extra_enable_(self, boolean):
        self._history_extra_is_enable = boolean

    def _set_history_extra_validation_fnc_(self, fnc):
        self._history_extra_value_validation_fnc = fnc

    def _get_history_extra_value_is_valid_(self, value):
        if self._history_extra_value_validation_fnc is not None:
            return self._history_extra_value_validation_fnc(value)
        return True

    def _set_history_extra_key_(self, key):
        self._history_extra_is_enable = True
        #
        self._history_extra_key = key

        self._setup_history_extra_()

    def _add_history_extra_value_(self, *args, **kwargs):
        pass

    def _setup_history_extra_(self):
        raise NotImplementedError()

    def _refresh_history_extra_(self):
        pass

    def _set_history_extra_show_latest_(self):
        pass


class AbsQtActionForEntryDef(object):
    entry_changed = qt_signal()
    entry_cleared = qt_signal()
    # change
    user_entry_changed = qt_signal()
    # clear
    user_entry_cleared = qt_signal()
    def _init_set_action_for_entry_def_(self, widget):
        pass


class AbsQtGuideBaseDef(object):
    guide_press_clicked = qt_signal()
    guide_press_db_clicked = qt_signal()
    #
    guide_text_accepted = qt_signal(str)
    guide_text_choose_accepted = qt_signal(str)
    guide_text_press_accepted = qt_signal(str)
    #
    QT_GUIDE_RECT_CLS = None
    def _init_guide_base_def_(self, widget):
        self._widget = widget
        #
        self._guide_items = []
        self._guide_index_current = None

        self._guide_type_texts = []
        self._guide_dict = {}
        #
        self._guide_item_extend = None

    def _set_guide_type_texts_(self, texts):
        self._guide_type_texts = texts

    def _set_guide_dict_(self, dict_):
        self._guide_dict = dict_

    def _create_guide_item_(self):
        item = self.QT_GUIDE_RECT_CLS()
        self._guide_items.append(item)
        return item

    def _get_guide_items_(self):
        return self._guide_items

    def _get_guide_item_indices_(self):
        return range(len(self._get_guide_items_()))

    def _get_guide_item_at_(self, index=0):
        if self._guide_items:
            if index < len(self._guide_items):
                return self._guide_items[index]

    def _restore_guide_(self):
        self._guide_items = []
        self._guide_index_current = None

    def _clear_all_guide_items_(self):
        self._guide_items = []

    def _set_guide_current_index_(self, index):
        self._guide_index_current = index

    def _clear_guide_current_(self):
        self._guide_index_current = None

    def _set_guide_name_text_at_(self, name_text, index=0):
        item = self._get_guide_item_at_(index)
        path_text = item._path_text
        child_path_text = bsc_core.DccPathDagMtd.get_dag_child_path(path_text, name_text)
        #
        self._set_guide_path_text_(child_path_text)
        return child_path_text

    def _set_guide_path_text_(self, path_text):
        pass

    def _get_guide_name_text_at_(self, index=0):
        return self._get_guide_item_at_(index)._get_name_text_()

    def _get_guide_path_text_at_(self, index=0):
        return self._get_guide_item_at_(index)._path_text


class AbsQtGuideEntryDef(AbsQtGuideBaseDef):
    QT_POPUP_GUIDE_CHOOSE_CLS = None
    def _init_guide_entry_def_(self, widget):
        self._init_guide_base_def_(widget)
        #
        self._popup_guide_choose_widget = None
        #
        self._guide_choose_index_current = None

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _get_action_flag_is_match_(self, flag):
        raise NotImplementedError()

    def _get_guide_choose_point_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        rect = item._icon_frame_draw_rect
        return self._widget.mapToGlobal(rect.center())

    def _get_guide_choose_rect_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        rect = item._icon_frame_draw_rect
        return rect

    def _set_guide_choose_item_current_at_(self, text, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            item._set_name_text_(text)

    def _get_guide_choose_item_current_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return item._name_text
    #
    def _set_guide_choose_item_content_at_(self, raw, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            item._set_item_choose_content_raw_(raw)
    #
    def _get_guide_child_name_texts_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return self._get_guide_child_name_texts_from_(item)

    def _get_guide_sibling_name_texts_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return self._get_guide_sibling_name_texts_from_(item)

    def _get_guide_child_name_texts_from_(self, item):
        return bsc_core.DccPathDagMtd.get_dag_child_names(
            item._path_text, self._get_guide_valid_path_texts_()
        )

    def _get_guide_sibling_name_texts_from_(self, item):
        return bsc_core.DccPathDagMtd.get_dag_sibling_names(
            item._path_text, self._get_guide_valid_path_texts_()
        )

    def _get_guide_valid_path_texts_(self):
        # todo, fnc "get_is_enable" is from proxy
        return [k for k, v in self._guide_dict.items() if v is None or v.get_is_enable() is True]

    def _start_guide_choose_item_popup_at_(self, index=0):
        self._popup_guide_choose_widget = self.QT_POPUP_GUIDE_CHOOSE_CLS(self)
        self._popup_guide_choose_widget._set_popup_entry_(self._widget)
        self._popup_guide_choose_widget._set_popup_entry_frame_(self._widget)
        self._popup_guide_choose_widget._execute_popup_start_(index)

    def _set_guide_choose_item_expanded_at_(self, boolean, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            item._set_choose_activated_(boolean)

    def _get_guide_choose_item_is_expanded_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return item._get_choose_is_activated_()

    def _set_guide_choose_item_expand_at_(self, index=0):
        self._set_guide_choose_item_expanded_at_(True, index)

    def _set_guide_choose_item_collapse_at_(self, index=0):
        self._set_guide_choose_item_expanded_at_(False, index)
        self._widget.update()

    def _get_is_guide_choose_flag_(self):
        return self._get_action_flag_is_match_(
            utl_gui_configure.ActionFlag.ChooseClick
        )

    def _restore_guide_(self):
        self._guide_items = []
        self._guide_choose_index_current = None
        self._guide_index_current = None

    def _set_guide_choose_current_index_(self, index):
        self._guide_choose_index_current = index

    def _clear_guide_choose_current_(self):
        self._guide_choose_index_current = None

    def _restore_guide_choose_(self):
        widget_pre = self._popup_guide_choose_widget
        if widget_pre is not None:
            widget_pre._close_popup_()


class AbsQtPressSelectExtraDef(object):
    user_press_select_accepted = qt_signal(bool)
    def _refresh_widget_draw_(self):
        raise NotImplementedError()
    #
    def _init_press_select_extra_def_(self, widget):
        self._widget = widget
        #
        self._is_selected = False

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _set_selected_(self, boolean):
        self._is_selected = boolean
        self._refresh_widget_draw_()

    def _get_is_selected_(self):
        return self._is_selected


class AbsQtItemMovieActionDef(object):
    movie_play_press_clicked = qt_signal()

    def _set_item_movie_action_def_init_(self):
        self._item_movie_play_rect = QtCore.QRect()

    def _set_item_movie_play_rect_(self, x, y, w, h):
        self._item_movie_play_rect.setRect(x, y, w, h)

    def _set_item_movie_play_press_clicked_connect_to_(self, fnc):
        pass

    def _set_item_movie_pay_press_clicked_emit_send_(self):
        self.movie_play_press_clicked.emit()


class AbsQtItemWidgetExtra(object):
    def _init_item_widget_extra_(self, widget):
        self._widget = widget
        self._item = None

    def _set_item_(self, item):
        self._item = item

    def _get_item_(self):
        return self._item


class AbsQtBuildViewDef(object):
    def _set_build_view_def_init_(self):
        pass

    def _set_build_view_setup_(self, view):
        self._build_runnable_stack = QtBuildRunnableStack(
            view
        )


class AbsQtViewSelectActionDef(object):
    def _set_view_select_action_def_init_(self):
        self._pre_selected_items = []

    def _set_view_item_selected_(self, item, boolean):
        raise NotImplementedError()

    def _set_item_widget_selected_(self, item, boolean):
        raise NotImplementedError()

    def _get_selected_items_(self):
        raise NotImplementedError()

    def _get_selected_item_widgets_(self):
        raise NotImplementedError()

    def _view_item_select_cbk(self):
        raise NotImplementedError()

    def _set_selection_use_multiply_(self):
        pass

    def _set_selection_use_single_(self):
        pass

    def _get_is_multiply_selection_(self):
        pass

    def _clear_selection_(self):
        pass


class AbsQtViewScrollActionDef(object):
    def _set_view_scroll_action_def_init_(self):
        self._scroll_is_enable = True

    def _set_scroll_enable_(self, boolean):
        self._scroll_is_enable = boolean

    def _get_view_h_scroll_bar_(self):
        raise NotImplementedError()

    def _get_view_v_scroll_bar_(self):
        raise NotImplementedError()

    def _get_view_v_scroll_value_(self):
        return self._get_view_v_scroll_bar_().value()

    def _get_v_minimum_scroll_value_(self):
        return self._get_view_v_scroll_bar_().minimum()

    def _get_v_maximum_scroll_value_(self):
        return self._get_view_v_scroll_bar_().maximum()

    def _get_v_scroll_percent_(self):
        v = self._get_view_v_scroll_value_()
        v_min, v_max = self._get_v_minimum_scroll_value_(), self._get_v_maximum_scroll_value_()
        if v_max > 0:
            return float(v) / float(v_max)
        return 0


class AbsQtItemFilterDef(object):
    TagFilterMode = utl_gui_configure.TagFilterMode
    def _init_item_filter_extra_def_(self, widget):
        self._widget = widget
        self._item_keyword_filter_mode = self.TagFilterMode.MatchAll
        #
        self._item_tag_filter_mode = self.TagFilterMode.MatchAll
        self._item_tag_filter_keys_src = set()
        self._item_tag_filter_keys_tgt = set()
        #
        self._item_semantic_tag_filter_mode = self.TagFilterMode.MatchAll
        self._item_semantic_tag_filter_keys_tgt = dict()
        #
        self._item_keyword_filter_keys_tgt = set()
        #
        self._item_tag_filter_tgt_statistic_enable = False
        #
        self._item_keyword_filter_keys_tgt_cache = None

    def _set_item_keyword_filter_keys_tgt_(self, keys):
        self._item_keyword_filter_keys_tgt = set(keys)

    def _add_item_keyword_filter_key_tgt_(self, key):
        self._item_keyword_filter_keys_tgt.add(key)

    def _update_item_keyword_filter_keys_tgt_(self, keys):
        self._item_keyword_filter_keys_tgt.update(set(keys))

    def _get_keyword_filter_keys_tgt_(self):
        return list(self._item_keyword_filter_keys_tgt)

    def _get_keyword_filter_keys_tgt_as_split_(self):
        return [j for i in self._get_keyword_filter_keys_tgt_() for j in bsc_core.RawTextMtd.find_words(i)]

    def _get_keyword_filter_keys_auto_(self):
        keys = self._get_keyword_filter_keys_tgt_()
        if keys:
            return [i for i in keys if i]
        else:
            if hasattr(self, '_get_name_texts_'):
                if self._get_name_texts_():
                    return [i for i in self._get_name_texts_() if i]
            if hasattr(self, '_get_name_text_'):
                return [self._get_name_text_()]
        return []

    def _get_keyword_filter_keys_auto_use_cache_(self):
        if self._item_keyword_filter_keys_tgt_cache is not None:
            return self._item_keyword_filter_keys_tgt_cache
        self._item_keyword_filter_keys_tgt_cache = self._get_keyword_filter_keys_auto_()
        return self._item_keyword_filter_keys_tgt_cache

    def _get_keyword_filter_keys_auto_as_split_(self):
        return [j for i in self._get_keyword_filter_keys_auto_use_cache_() for j in bsc_core.RawTextMtd.split_any_to(i)]

    def _get_item_keyword_filter_context_(self):
        return '+'.join(self._get_keyword_filter_keys_auto_use_cache_())

    def _get_item_keyword_filter_match_args_(self, texts):
        # todo: use match all mode then, maybe use match one mode also
        if texts:
            context = self._get_item_keyword_filter_context_()
            context = context.lower()
            for i_text in texts:
                # do not encode, keyword can be use unicode
                i_text = i_text.lower()
                if '*' in i_text:
                    i_filter_key = six.u('*{}*').format(i_text.lstrip('*').rstrip('*'))
                    if not fnmatch.filter([context], i_filter_key):
                        return True, True
                else:
                    if i_text not in context:
                        return True, True
            return True, False
        return False, False

    def _set_item_tag_filter_mode_(self, mode):
        self._item_tag_filter_mode = mode

    def _get_item_tag_filter_mode_(self):
        return self._item_tag_filter_mode
    # tag filter source
    def _set_item_tag_filter_keys_src_add_(self, key):
        self._item_tag_filter_keys_src.add(key)

    def _set_item_tag_filter_keys_src_update_(self, keys):
        self._item_tag_filter_keys_src.update(set(keys))

    def _get_item_tag_filter_keys_src_(self):
        return list(self._item_tag_filter_keys_src)
    # tag filter target
    def _set_item_tag_filter_keys_tgt_add_(self, key, ancestors=False):
        self._item_tag_filter_keys_tgt.add(key)
        #
        if ancestors is True:
            self._set_item_tag_filter_tgt_ancestors_update_()

    def _set_item_tag_filter_keys_tgt_update_(self, keys):
        self._item_tag_filter_keys_tgt.update(set(keys))

    def _get_item_tag_filter_keys_tgt_(self):
        return self._item_tag_filter_keys_tgt

    def _set_item_tag_filter_tgt_ancestors_update_(self):
        pass

    def _set_item_tag_filter_tgt_statistic_enable_(self, boolean):
        self._item_tag_filter_tgt_statistic_enable = boolean

    def _get_item_tag_filter_tgt_statistic_enable_(self):
        return self._item_tag_filter_tgt_statistic_enable

    def _get_item_tag_filter_tgt_match_args_(self, data_src):
        data_tgt = self._item_tag_filter_keys_tgt
        mode = self._item_tag_filter_mode
        if data_tgt:
            if mode == self.TagFilterMode.MatchAll:
                for i_key_tgt in data_tgt:
                    if i_key_tgt not in data_src:
                        return True, True
                return True, False
            elif mode == self.TagFilterMode.MatchOne:
                for i_key_tgt in data_tgt:
                    if i_key_tgt in data_src:
                        return True, False
                return True, True
            return True, False
        return False, False
    # semantic tag filter
    def _set_item_semantic_tag_filter_key_add_(self, key, value):
        self._item_semantic_tag_filter_keys_tgt.setdefault(
            key, set()
        ).add(value)

    def _update_item_semantic_tag_filter_keys_tgt_(self, data):
        self._item_semantic_tag_filter_keys_tgt.update(data)

    def _get_item_semantic_tag_filter_keys_tgt_(self):
        return self._item_semantic_tag_filter_keys_tgt

    def _get_item_semantic_tag_filter_tgt_match_args_(self, data_src):
        data_tgt = self._item_semantic_tag_filter_keys_tgt
        mode = self._item_semantic_tag_filter_mode
        if data_tgt:
            if mode == self.TagFilterMode.MatchAll:
                for k, v_tgt in data_tgt.items():
                    if k in data_src:
                        v_src = data_src[k]
                        if not v_tgt.intersection(v_src):
                            return True, True
                return True, False
            elif mode == self.TagFilterMode.MatchOne:
                for k, v_tgt in data_tgt.items():
                    if k in data_src:
                        v_src = data_src[k]
                        if v_tgt.intersection(v_src):
                            return True, False
                return True, True
            return True, False
        return False, False
    # todo: filter highlight for draw
    def _set_item_filter_occurrence_(self, boolean, column=0):
        pass
        # _ = self._widget.data(column, QtCore.Qt.UserRole)
        # if isinstance(_, dict):
        #     user_data = _
        # else:
        #     user_data = {}
        # #
        # user_data['filter_occurrence'] = boolean
        # self._widget.setData(
        #     column, QtCore.Qt.UserRole,
        #     user_data
        # )


class AbsQtViewFilterExtraDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _init_view_filter_extra_def_(self, widget):
        self._widget = widget
        self._view_tag_filter_data_src = []
        self._view_semantic_tag_filter_data_src = {}
        self._view_keyword_filter_data_src = []
        self._view_keyword_filter_match_items = []
        #
        self._view_keyword_filter_bar = None
        #
        self._view_keyword_filter_occurrence_index_current = None

    def _set_view_keyword_filter_bar_(self, widget):
        self._view_keyword_filter_bar = widget

    def _get_view_tag_filter_tgt_statistic_raw_(self):
        dic = {}
        items = self._get_all_items_()
        for i_item in items:
            enable = i_item._get_item_tag_filter_tgt_statistic_enable_()
            if enable is True:
                i_keys = i_item._get_item_tag_filter_keys_tgt_()
                for j_key in i_keys:
                    dic.setdefault(j_key, []).append(i_item)
        return dic

    def _set_view_tag_filter_data_src_(self, data_src):
        self._view_tag_filter_data_src = data_src

    def _get_view_tag_filter_data_src_(self):
        return self._view_tag_filter_data_src

    def _get_view_semantic_tag_filter_data_src_(self):
        return self._view_semantic_tag_filter_data_src

    def _set_view_semantic_tag_filter_data_src_(self, data_src):
        self._view_semantic_tag_filter_data_src = data_src

    def _set_view_keyword_filter_data_src_(self, data_src):
        self._view_keyword_filter_data_src = data_src

    def _refresh_view_items_visible_by_any_filter_(self):
        tag_filter_data_src = self._view_tag_filter_data_src
        semantic_tag_filter_data_src = self._view_semantic_tag_filter_data_src
        keyword_filter_data_src = self._view_keyword_filter_data_src
        self._view_keyword_filter_match_items = []
        #
        items = self._get_all_items_()
        for i_item in items:
            i_tag_filter_hidden_ = False
            i_semantic_filter_hidden_ = False
            i_keyword_filter_hidden_ = False
            # tag filter
            if tag_filter_data_src:
                i_is_enable, i_is_hidden = i_item._get_item_tag_filter_tgt_match_args_(tag_filter_data_src)
                if i_is_enable is True:
                    i_tag_filter_hidden_ = i_is_hidden
            # semantic tag filter
            if semantic_tag_filter_data_src:
                i_is_enable, i_is_hidden = i_item._get_item_semantic_tag_filter_tgt_match_args_(semantic_tag_filter_data_src)
                if i_is_enable is True:
                    i_semantic_filter_hidden_ = i_is_hidden
            # keyword filter
            if keyword_filter_data_src:
                i_is_enable, i_is_hidden = i_item._get_item_keyword_filter_match_args_(keyword_filter_data_src)
                if i_is_enable is True:
                    i_keyword_filter_hidden_ = i_is_hidden
                    if i_keyword_filter_hidden_ is False:
                        self._view_keyword_filter_match_items.append(i_item)
            #
            if True in [i_tag_filter_hidden_, i_semantic_filter_hidden_, i_keyword_filter_hidden_]:
                is_hidden = True
            else:
                is_hidden = False
            #
            i_item._set_hidden_(is_hidden)
            # for tree
            for i in i_item._get_ancestors_():
                if is_hidden is False:
                    i._set_hidden_(False)
            #
            if self._view_keyword_filter_bar is not None:
                if self._view_keyword_filter_match_items:
                    self._view_keyword_filter_bar._set_filter_result_count_(
                        len(self._view_keyword_filter_match_items)
                    )
                else:
                    self._view_keyword_filter_bar._set_filter_result_count_(None)

    def _has_keyword_filter_results_(self):
        return self._view_keyword_filter_match_items != []
    # keyword filter action
    def _execute_view_keyword_filter_occurrence_to_current_(self):
        items = self._view_keyword_filter_match_items
        if items:
            idx_cur = 0
            item_cur = items[idx_cur]
            #
            item_cur._set_item_filter_occurrence_(True)
            self._widget._scroll_view_to_item_top_(item_cur)
            self._view_keyword_filter_occurrence_index_current = idx_cur
        else:
            self._view_keyword_filter_occurrence_index_current = None
        #
        if self._view_keyword_filter_bar is not None:
            self._view_keyword_filter_bar._set_filter_result_index_current_(
                self._view_keyword_filter_occurrence_index_current
            )

    def _execute_view_keyword_filter_occurrence_to_previous_(self):
        items = self._view_keyword_filter_match_items
        if items:
            idx_max, idx_min = len(items)-1, 0
            idx = self._view_keyword_filter_occurrence_index_current or 0
            #
            idx = max(min(idx, idx_max), 0)
            item_cur = items[idx]
            item_cur._set_item_filter_occurrence_(False)
            #
            if idx == idx_min:
                idx = idx_max
            else:
                idx -= 1
            idx_pre = max(min(idx, idx_max), 0)
            item_pre = items[idx_pre]
            item_pre._set_item_filter_occurrence_(True)
            self._widget._scroll_view_to_item_top_(item_pre)
            self._view_keyword_filter_occurrence_index_current = idx_pre
        else:
            self._view_keyword_filter_occurrence_index_current = None
        #
        if self._view_keyword_filter_bar is not None:
            self._view_keyword_filter_bar._set_filter_result_index_current_(
                self._view_keyword_filter_occurrence_index_current
            )

    def _execute_view_keyword_filter_occurrence_to_next_(self):
        items = self._view_keyword_filter_match_items
        if items:
            idx_max, idx_min = len(items)-1, 0
            idx = self._view_keyword_filter_occurrence_index_current or 0
            #
            idx = max(min(idx, idx_max), 0)
            item_cur = items[idx]
            item_cur._set_item_filter_occurrence_(False)
            #
            if idx == idx_max:
                idx = idx_min
            else:
                idx += 1
            idx_nxt = max(min(idx, idx_max), 0)
            item_nxt = items[idx_nxt]
            item_nxt._set_item_filter_occurrence_(True)
            self._widget._scroll_view_to_item_top_(item_nxt)
            self._view_keyword_filter_occurrence_index_current = idx_nxt
        else:
            self._view_keyword_filter_occurrence_index_current = None
        #
        if self._view_keyword_filter_bar is not None:
            self._view_keyword_filter_bar._set_filter_result_index_current_(
                self._view_keyword_filter_occurrence_index_current
            )


class AbsQtStateDef(object):
    ActionState = bsc_configure.ActionState

    def _set_state_def_init_(self):
        self._state = utl_gui_core.State.NORMAL
        self._state_draw_is_enable = False
        self._state_color = Brush.TEXT_NORMAL

    def _set_state_(self, *args, **kwargs):
        self._state = args[0]

    def _get_state_(self, *args, **kwargs):
        return self._state

    def _get_state_color_(self):
        return self._state_color

    def _set_state_color_(self, color):
        self._state_color = color

    def _set_state_draw_enable_(self, boolean):
        self._state_draw_is_enable = boolean


class AbsQtDagDef(object):
    def _set_dag_def_init_(self):
        pass

    def _get_descendants_(self):
        return []

    def _get_ancestors_(self):
        return []


class AbsQtVisibleDef(object):
    def _set_visible_def_init_(self):
        self._visible_src_key = None

    # noinspection PyUnresolvedReferences
    def _set_visible_(self, boolean):
        self.setHidden(not boolean)
    # noinspection PyUnresolvedReferences
    def _get_is_visible_(self):
        return not self.isHidden()

    # noinspection PyUnresolvedReferences
    def _set_hidden_(self, boolean, **kwargs):
        self.setHidden(boolean)

    # noinspection PyUnresolvedReferences
    def _get_is_hidden_(self):
        return self.isHidden()


class AbsQtItemVisibleConnectionDef(object):
    def _get_item_is_hidden_(self):
        raise NotImplementedError()

    def _set_item_visible_connection_def_init_(self):
        self._item_visible_src_key = None
        self._item_visible_tgt_key = None
        #
        self._item_visible_tgt_view = None
        self._item_visible_tgt_raw = None

    def _set_item_visible_connect_to_(self, key, item_tgt):
        self._set_item_visible_src_key_(key)
        self._set_item_visible_tgt_view_(item_tgt._get_view_())
        #
        item_tgt._set_visible_tgt_key_(key)
        item_tgt._set_hidden_(self._get_item_is_hidden_())

    def _get_item_visible_src_key_(self):
        return self._item_visible_src_key

    def _set_item_visible_src_key_(self, key):
        self._item_visible_src_key = key

    def _get_item_visible_tgt_key_(self):
        return self._item_visible_tgt_key

    def _set_item_visible_tgt_key_(self, key):
        self._item_visible_tgt_key = key

    def _get_item_visible_tgt_view_(self):
        return self._item_visible_tgt_view

    def _set_item_visible_tgt_view_(self, view):
        self._item_visible_tgt_view = view

    def _get_item_visible_tgt_raw_(self):
        return self._item_visible_tgt_raw

    def _set_item_visible_tgt_raw_(self, raw):
        self._item_visible_tgt_raw = raw

    def _set_item_visible_connection_refresh_(self):
        src_item = self
        src_key = src_item._get_item_visible_src_key_()
        if src_key is not None:
            tgt_view = src_item._get_item_visible_tgt_view_()
            if tgt_view is not None:
                tgt_raw = tgt_view._get_view_visible_tgt_raw_()
                if src_key in tgt_raw:
                    items_tgt = tgt_raw[src_key]
                    for i_item_tgt in items_tgt:
                        i_item_tgt.set_hidden(self._get_item_is_hidden_())
                        i_item_tgt._set_item_show_start_auto_()


class AbsQtViewVisibleConnectionDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _set_view_visible_connection_def_init_(self):
        self._view_visible_tgt_raw = []

    def _set_view_visible_tgt_raw_(self, raw):
        self._view_visible_tgt_raw = raw

    def _get_view_visible_tgt_raw_(self):
        return self._view_visible_tgt_raw

    def _set_view_visible_tgt_raw_clear_(self):
        self._set_view_visible_tgt_raw_({})

    def _set_view_visible_tgt_raw_update_(self):
        dic = {}
        items = self._get_all_items_()
        for i_item in items:
            i_tgt_key = i_item._get_item_visible_tgt_key_()
            if i_tgt_key is not None:
                dic.setdefault(
                    i_tgt_key, []
                ).append(i_item)
        #
        self._set_view_visible_tgt_raw_(dic)


class AbsQtViewStateDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _set_view_state_def_init_(self):
        pass

    def _get_view_item_states_(self, items=None):
        if isinstance(items, (tuple, list)):
            lis = []
            for i_item in items:
                lis.append(i_item._get_state_())
            return lis
        return []

    def _get_view_item_state_colors_(self, items=None):
        if isinstance(items, (tuple, list)):
            lis = []
            for i_item in items:
                lis.append(i_item._get_state_color_())
            return lis
        return []


class AbsQtBuildItemDef(object):
    def _set_build_item_def_init_(self):
        pass

    def _get_view_(self):
        raise NotImplementedError()

    def _setup_item_show_runnable_stack_(self, view):
        self._build_runnable_stack = view._build_runnable_stack

    def _create_item_show_runnable_(self, cache_fnc, build_fnc, post_fnc=None):
        return self._build_runnable_stack.create_thread(
            cache_fnc, build_fnc, post_fnc
        )


# show base
# for item
class AbsQtShowBaseForItemDef(
    AbsQtBuildItemDef
):
    ShowStatus = bsc_configure.ShowStatus

    def _refresh_widget_(self, *args, **kwargs):
        raise NotImplementedError()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _get_view_(self):
        raise NotImplementedError()

    def _get_item_widget_(self):
        raise NotImplementedError()

    def _init_show_base_for_item_def_(self, widget):
        self._widget = widget
        #
        if bsc_core.ApplicationMtd.get_is_maya():
            self._item_show_use_thread = False
        else:
            self._item_show_use_thread = True
        #
        self._item_show_runnable = None
        self._item_show_image_runnable = None
        #
        self._item_show_cache_fnc = None
        self._item_show_build_fnc = None
        #
        self._item_show_status = self.ShowStatus.Unknown
        # image
        self._item_show_image_cache_fnc = None
        self._item_show_image_build_fnc = None
        #
        self._item_show_image_status = self.ShowStatus.Unknown

        self._set_build_item_def_init_()

    def _setup_item_show_(self, view):
        self._setup_item_show_runnable_stack_(view)

        self._item_show_runnable = None
        self._item_show_image_runnable = None
        #
        self._item_show_timer = QtCore.QTimer(view)
        self._item_show_loading_index = 0
        self._item_show_loading_timer = QtCore.QTimer(view)
        self._item_show_loading_timer.timeout.connect(self._update_item_show_loading_)
        #
        self._item_show_image_timer = QtCore.QTimer(view)
        self._item_show_image_loading_index = 0
        self._item_show_image_loading_timer = QtCore.QTimer(view)
        self._item_show_image_loading_timer.timeout.connect(self._update_item_show_image_loading_)
        #
        self._item_show_image_sub_process = None
        self._item_show_image_cmd = None
        self._item_show_image_file_path = None

    def _set_item_show_build_fnc_(self, method):
        def cache_fnc_():
            return []

        def build_fnc_(data):
            method()

        if method is not None:
            self._set_item_show_fnc_(cache_fnc_, build_fnc_)
    # fnc
    def _set_item_show_fnc_(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._item_show_cache_fnc is None and self._item_show_build_fnc is None:
                self._item_show_cache_fnc = cache_fnc
                self._item_show_build_fnc = build_fnc
                #
                self._item_show_status = self.ShowStatus.Waiting
                if self._get_item_is_viewport_showable_() is True:
                    self._checkout_item_show_()

    def _checkout_item_show_(self, delay_time=10, force=False):
        def run_fnc_():
            if self._item_show_cache_fnc is not None:
                self._start_item_show_()
        #
        if self._item_show_status == self.ShowStatus.Waiting or force is True:
            self._checkout_item_show_loading_()
            self._item_show_timer.singleShot(delay_time, run_fnc_)
    #
    def _checkout_item_show_loading_(self):
        if self._item_show_status == self.ShowStatus.Waiting:
            self._item_show_loading_timer.start(100)

    def _start_item_show_(self):
        if self._item_show_status == self.ShowStatus.Waiting:
            if self._item_show_use_thread is True:
                self._item_show_status = self.ShowStatus.Loading
                #
                self._item_show_runnable = self._create_item_show_runnable_(
                    self._item_show_cache_fnc,
                    self._item_show_build_fnc,
                    self._finish_item_show_
                )
                #
                self._build_runnable_stack.start_runnable(self._item_show_runnable)
            else:
                self._item_show_build_fnc(
                    self._item_show_cache_fnc()
                )
                self._finish_item_show_()

    def _finish_item_show_(self):
        self._set_item_show_stop_(
            self.ShowStatus.Finished
        )

    def _set_item_show_stop_(self, status):
        self._item_show_status = status
        self._finish_item_show_loading_()

    def _get_item_show_is_finished_(self):
        return self._item_show_status in {
            self.ShowStatus.Completed, self.ShowStatus.Failed
        }
    # loading
    def _update_item_show_loading_(self):
        self._item_show_loading_index += 1
        # noinspection PyBroadException
        try:
            self._refresh_widget_draw_()
        except:
            pass

    def _finish_item_show_loading_(self):
        # noinspection PyBroadException
        try:
            self._item_show_loading_timer.stop()
            self._refresh_widget_draw_()
        except:
            pass
    # image fnc
    def _set_item_show_image_cmd_(self, image_file_path, cmd):
        def cache_fnc_():
            # noinspection PyBroadException
            try:
                bsc_core.SubProcessMtd.execute_with_result(
                    cmd
                )
            except:
                pass
            return []

        def build_fnc_(data):
            pass

        if cmd is not None:
            self._item_show_image_file_path = image_file_path
            self._set_item_show_image_fnc_(cache_fnc_, build_fnc_)

    def _set_item_show_image_fnc_(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._item_show_image_cache_fnc is None and self._item_show_image_build_fnc is None:
                self._item_show_image_cache_fnc = cache_fnc
                self._item_show_image_build_fnc = build_fnc
                #
                self._item_show_image_status = self.ShowStatus.Waiting
                if self._get_item_is_viewport_showable_() is True:
                    self._checkout_item_show_image_()

    def _checkout_item_show_image_(self, delay_time=10, force=False):
        def run_fnc():
            if self._item_show_cache_fnc is not None:
                self._start_item_show_image_()
        #
        if self._item_show_image_status == self.ShowStatus.Waiting or force is True:
            self._checkout_item_show_image_loading_()
            #
            self._item_show_image_timer.singleShot(delay_time, run_fnc)

    def _checkout_item_show_image_loading_(self):
        if self._item_show_image_status == self.ShowStatus.Waiting:
            self._item_show_image_loading_timer.start(100)

    def _start_item_show_image_(self):
        if self._item_show_image_status == self.ShowStatus.Waiting:
            self._item_show_image_status = self.ShowStatus.Loading
            if self._item_show_use_thread is True:
                self._item_show_image_runnable = self._create_item_show_runnable_(
                    self._item_show_image_cache_fnc,
                    self._item_show_image_build_fnc,
                    self._finish_item_show_image_
                )
                #
                self._build_runnable_stack.start_runnable(self._item_show_image_runnable)
            else:
                self._item_show_image_build_fnc(
                    self._item_show_image_cache_fnc()
                )
                self._finish_item_show_image_()

    def _finish_item_show_image_(self):
        if self._item_show_image_file_path is not None:
            if os.path.isfile(self._item_show_image_file_path) is True:
                self._set_item_show_image_stop_(self.ShowStatus.Completed)
            else:
                self._set_item_show_image_stop_(self.ShowStatus.Failed)

    def _set_item_show_image_stop_(self, status):
        self._item_show_image_status = status
        if status == self.ShowStatus.Failed:
            item_widget = self._get_item_widget_()
            if item_widget is not None:
                item_widget._set_image_file_path_(
                    utl_gui_core.RscIconFile.get('image_loading_failed_error')
                )
        #
        self._finish_item_show_image_loading_()

    def _get_item_is_viewport_showable_(self, *args, **kwargs):
        raise NotImplementedError()

    def _update_item_show_image_loading_(self):
        self._item_show_image_loading_index += 1
        # noinspection PyBroadException
        try:
            self._refresh_widget_draw_()
        except:
            pass

    def _finish_item_show_image_loading_(self):
        # noinspection PyBroadException
        try:
            self._item_show_image_loading_timer.stop()
            self._refresh_widget_draw_()
        except:
            pass

    def _checkout_item_show_all_(self, force=False):
        self._checkout_item_show_(force=force)
        self._checkout_item_show_image_(force=force)

    def _stop_item_show_all_(self):
        self._set_item_show_stop_(self.ShowStatus.Stopped)
        self._set_item_show_image_stop_(self.ShowStatus.Stopped)

    def _kill_item_all_show_runnables_(self):
        if self._item_show_runnable is not None:
            self._item_show_runnable.set_kill()
        #
        if self._item_show_image_runnable is not None:
            self._item_show_image_runnable.set_kill()

    def _set_item_viewport_visible_(self, boolean):
        if boolean is True:
            self._checkout_item_show_all_()
        #
        self._set_item_widget_visible_(boolean)

    def _set_item_widget_visible_(self, boolean):
        raise NotImplementedError()

    def _set_viewport_show_enable_(self, boolean):
        self._is_viewport_show_enable = boolean

    def _set_item_show_start_auto_(self):
        if self._get_item_is_viewport_showable_() is True:
            self._checkout_item_show_all_()

    def _set_item_show_force_(self):
        self._checkout_item_show_all_(force=True)


# for view
class AbsQtShowForViewDef(object):
    def _init_show_for_view_def_(self, widget):
        self._widget = widget

    def _get_view_item_viewport_showable_(self, item):
        i_rect = self._widget.visualItemRect(item)
        i_w, i_h = i_rect.width(), i_rect.height()
        # check is visible
        if i_w != 0 and i_h != 0:
            viewport_rect = self._widget.rect()
            v_t, v_b = viewport_rect.top(), viewport_rect.bottom()
            i_t, i_b = i_rect.top(), i_rect.bottom()
            if v_b >= i_t and i_b >= v_t:
                return True
        return False

    def _refresh_view_all_items_viewport_showable_(self, includes=None):
        if isinstance(includes, (tuple, list)):
            items_ = includes
        else:
            items_ = self._widget._get_all_items_()
        #
        for i_item in items_:
            if i_item.isHidden() is False:
                if self._get_view_item_viewport_showable_(i_item) is True:
                    i_item._set_item_viewport_visible_(True)

        self._widget.update()

    def _refresh_viewport_showable_auto_(self):
        self._refresh_view_all_items_viewport_showable_()


class ShowFnc(object):
    def __init__(self):
        pass


class AbsQtShowStackForItemDef(object):
    def _init_show_stack_for_item_(self):
        pass


class AbsQtValueEntryExtraDef(object):
    user_key_tab_pressed = qt_signal()
    #
    value_entry_changed = qt_signal()
    value_entry_cleared = qt_signal()
    # change
    user_value_entry_changed = qt_signal()
    # clear
    user_value_entry_cleared = qt_signal()
    def _init_value_entry_extra_def_(self, widget):
        self._widget = widget
        #
        self._value_entry_is_enable = False
        #
        self._value_type = str
        self._item_value_default = None
        self._value_entry = None

    def _set_value_entry_focus_in_(self):
        self._value_entry.setFocus(QtCore.Qt.TabFocusReason)

    def _set_value_entry_enable_(self, boolean):
        self._value_entry_is_enable = boolean

    def _set_value_entry_drop_enable_(self, boolean):
        self._value_entry._set_drop_enable_(boolean)

    def _set_value_validation_fnc_(self, fnc):
        pass

    def _set_value_entry_use_as_storage_(self, boolean):
        pass

    def _build_value_entry_(self, *args, **kwargs):
        pass

    def _get_value_entry_(self):
        return self._value_entry

    def _get_value_entry_gui_(self):
        return self._value_entry

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        self._value_entry._set_value_type_(value_type)

    def _set_value_validator_use_as_frames_(self):
        self._value_entry._set_value_validator_use_as_frames_()

    def _set_value_validator_use_as_rgba_(self):
        self._value_entry._set_value_validator_use_as_rgba_()

    def _get_value_type_(self):
        return self._value_type

    def _set_value_(self, value):
        self._value_entry._set_value_(value)

    def _get_value_(self):
        return self._value_entry._get_value_()

    def _set_value_entry_finished_connect_to_(self, fnc):
        self._value_entry.user_entry_finished.connect(fnc)

    def _set_value_entry_changed_connect_to_(self, fnc):
        self._value_entry.entry_changed.connect(fnc)

    def _set_item_value_entry_enable_(self, boolean):
        pass


class AbsQtValueEntryAsTupleExtraDef(object):
    QT_VALUE_ENTRY_CLS = None

    def _init_value_entry_as_tuple_def_(self):
        self._value_type = str
        #
        self._item_value_default = ()
        #
        self._value = []
        self._value_entries = []

    def _build_value_entry_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        for i_value_entry_widget in self._value_entries:
            i_value_entry_widget._set_value_type_(value_type)

    def _get_value_type_(self):
        return self._value_type

    def _set_value_size_(self, size):
        self._build_value_entry_(size, self._value_type)

    def _get_value_size_(self):
        return len(self._value_entries)

    def _get_value_default_(self):
        return self._item_value_default

    def _set_value_(self, value):
        for i, i_value in enumerate(value):
            widget = self._value_entries[i]
            widget._set_value_(i_value)

    def _get_value_(self):
        value = []
        for i in self._value_entries:
            i_value = i._get_value_()
            value.append(
                i_value
            )
        return tuple(value)

    def _set_value_default_(self, value):
        self._item_value_default = value

    def _get_value_is_default_(self):
        return tuple(self._get_value_()) == tuple(self._get_value_default_())

    def _set_value_entry_changed_connect_to_(self, fnc):
        for i in self._value_entries:
            i.entry_changed.connect(fnc)


class AbsQtValueEntryAsPopupChooseExtraDef(AbsQtValueEntryExtraDef):
    QT_VALUE_ENTRY_CLS = None
    def _init_value_entry_as_popup_choose_extra_def_(self, widget):
        self._init_value_entry_extra_def_(widget)
        #
        self._value_type = str
        #
        self._item_value_default = None
        #
        self._value_enumerate_strings = []
        self._choose_index_showable = False

    def _refresh_widget_(self):
        raise NotImplementedError()

    def _refresh_choose_index_(self):
        raise NotImplementedError()

    def _set_choose_index_showable_(self, boolean):
        self._choose_index_showable = boolean
        self._refresh_choose_index_()

    def _set_value_(self, value):
        super(AbsQtValueEntryAsPopupChooseExtraDef, self)._set_value_(value)
        #
        self._refresh_choose_index_()


class AbsQtDrawGridDef(object):
    def _set_draw_grid_def_init_(self, widget):
        self._widget = widget
        #
        self._grid_border_color = 71, 71, 71, 255
        self._grid_mark_border_color = 191, 191, 191, 255
        self._grid_axis_border_color_x, self._grid_axis_border_color_y = (255, 0, 63, 255), (63, 255, 127, 255)
        #
        self._grid_value_show_mode = 1
        #
        self._grid_width, self._grid_height = 20, 20
        #
        self._grid_offset_x, self._grid_offset_y = 0, 0
        self._grid_scale_x, self._grid_scale_y = 1, 1
        #
        self._grid_value_offset_x, self._grid_value_offset_y = 0, 0

        self._grid_dir_x, self._grid_dir_y = 1, 1

        self._grid_axis_lock_x, self._grid_axis_lock_y = 0, 0

    def _refresh_widget_draw_(self):
        raise NotImplementedError()


class AbsQtTrackActionDef(object):
    def _set_track_action_def_init_(self, widget):
        self._widget = widget
        #
        self._track_offset_flag = False
        #
        self._track_offset_start_point = QtCore.QPoint(0, 0)
        #
        self._tmp_track_offset_x, self._tmp_track_offset_y = 0, 0
        self._track_offset_x, self._track_offset_y = 0, 0
        #
        self._track_offset_minimum_x, self._track_offset_minimum_y = -1000, -1000
        self._track_offset_maximum_x, self._track_offset_maximum_y = 1000, 1000
        #
        self._track_limit_x, self._track_limit_x = 0, 0
        self._track_offset_direction_x, self._track_offset_direction_y = 1, 1
        #
        self._track_offset_radix_x, self._track_offset_radix_y = 2, 2

    def _refresh_widget_draw_(self):
        self._widget.update()

    def _set_tack_offset_action_start_(self, event):
        self._track_offset_flag = True
        self._track_offset_start_point = event.globalPos()

    def _execute_action_track_offset_(self, event):
        track_point = event.globalPos() - self._track_offset_start_point
        track_offset_x, track_offset_y = self._tmp_track_offset_x, self._tmp_track_offset_y
        track_d_offset_x, track_d_offset_y = track_point.x(), track_point.y()
        #
        self._track_offset_x = bsc_core.RawValueMtd.set_offset_range_to(
            value=track_offset_x,
            d_value=track_d_offset_x,
            radix=self._track_offset_radix_x,
            value_range=(self._track_offset_minimum_x, self._track_offset_maximum_x),
            direction=self._track_offset_direction_x
        )
        #
        self._track_offset_y = bsc_core.RawValueMtd.set_offset_range_to(
            value=track_offset_y,
            d_value=track_d_offset_y,
            radix=self._track_offset_radix_y,
            value_range=(self._track_offset_minimum_y, self._track_offset_maximum_y),
            direction=self._track_offset_direction_y
        )
        self._refresh_widget_draw_()

    def _set_track_offset_action_end_(self, event):
        self._tmp_track_offset_x, self._tmp_track_offset_y = self._track_offset_x, self._track_offset_y
        self._track_offset_flag = False


class AbsQtZoomActionDef(object):
    def _set_zoom_action_def_init_(self, widget):
        self._widget = widget
        #
        self._zoom_scale_flag = True
        #
        self._zoom_scale_x, self._zoom_scale_y = 1.0, 1.0
        self._zoom_scale_minimum_x, self._zoom_scale_minimum_y = 0.1, 0.1
        self._zoom_scale_maximum_x, self._zoom_scale_maximum_y = 100.0, 100.0

        self._zoom_scale_radix_x, self._zoom_scale_radix_y = 5.0, 5.0

    def _refresh_widget_draw_(self):
        self._widget.update()

    def _execute_action_zoom_scale_(self, event):
        delta = event.angleDelta().y()
        self._zoom_scale_x = bsc_core.RawValueMtd.step_to(
            value=self._zoom_scale_x,
            delta=delta,
            step=self._zoom_scale_radix_x,
            value_range=(self._zoom_scale_minimum_x, self._zoom_scale_maximum_x),
            direction=1
        )

        self._zoom_scale_y = bsc_core.RawValueMtd.step_to(
            value=self._zoom_scale_y,
            delta=delta,
            step=self._zoom_scale_radix_y,
            value_range=(self._zoom_scale_minimum_y, self._zoom_scale_maximum_y),
            direction=1
        )
        #
        self._refresh_widget_draw_()


# delete
class AbsQtDeleteBaseDef(object):
    delete_text_accepted = qt_signal(str)
    def _init_delete_base_def_(self, widget):
        self._widget = widget
        #
        self._delete_is_enable = False
        self._delete_action_is_enable = False
        #
        self._delete_draw_is_enable = False
        self._delete_action_rect = QtCore.QRect()
        self._delete_icon_draw_rect = QtCore.QRect()
        #
        self._delete_icon_file_draw_size = 12, 12
        self._delete_is_pressed = False
        self._delete_is_hovered = False
        self._delete_icon_file_path = utl_gui_core.RscIconFile.get('delete')

    def _set_delete_enable_(self, boolean):
        self._delete_is_enable = boolean
        self._delete_action_is_enable = boolean
        self._delete_draw_is_enable = boolean

    def _set_delete_rect_(self, x, y, w, h):
        self._delete_action_rect.setRect(
            x, y, w, h
        )

    def _set_delete_draw_rect_(self, x, y, w, h):
        self._delete_icon_draw_rect.setRect(
            x, y, w, h
        )

    def _get_action_delete_is_valid_(self, event):
        if self._delete_action_is_enable is True:
            p = event.pos()
            return self._delete_action_rect.contains(p)
        return False


class AbsQtHelpDef(object):
    def _set_help_def_init_(self, widget):
        self._widget = widget

        self._help_text_is_enable = False
        #
        self._help_text_draw_size = 480, 240
        self._help_frame_draw_rect = QtCore.QRect()
        self._help_draw_rect = QtCore.QRect()
        self._help_text = ''

    def _set_help_text_(self, text):
        self._help_text = text


class AbsQtScreenshotDef(object):
    class Mode(enum.IntEnum):
        Started = 0
        New = 1
        Edit = 2
        Stopped = 3

    RectRegion = utl_gui_configure.RectRegion

    CURSOR_MAPPER = {
        RectRegion.Unknown: QtCore.Qt.ArrowCursor,
        RectRegion.Top: QtCore.Qt.SizeVerCursor,
        RectRegion.Bottom: QtCore.Qt.SizeVerCursor,
        RectRegion.Left: QtCore.Qt.SizeHorCursor,
        RectRegion.Right: QtCore.Qt.SizeHorCursor,
        RectRegion.TopLeft: QtCore.Qt.SizeFDiagCursor,
        RectRegion.TopRight: QtCore.Qt.SizeBDiagCursor,
        RectRegion.BottomLeft: QtCore.Qt.SizeBDiagCursor,
        RectRegion.BottomRight: QtCore.Qt.SizeFDiagCursor,
        RectRegion.Inside: QtCore.Qt.SizeAllCursor,
    }

    screenshot_started = qt_signal()
    screenshot_finished = qt_signal()
    screenshot_accepted = qt_signal(list)
    CACHE = 0, 0, 0, 0

    def _set_screenshot_def_init_(self, widget):
        self._widget = widget

        self._screenshot_mode = self.Mode.Started
        self._screenshot_is_modify = False

        self._screenshot_file_path = None

        self._screenshot_rect = QtCore.QRect()

        self._screenshot_is_activated = False
        #
        self._screenshot_point_start = QtCore.QPoint()
        #
        self._screenshot_rect_point_start = QtCore.QPoint()
        self._screenshot_rect_point_start_offset = [0, 0]
        self._screenshot_rect_point_start_offset_temp = [0, 0]
        self._screenshot_rect_point_end = QtCore.QPoint()
        self._screenshot_rect_point_end_offset = [0, 0]
        self._screenshot_rect_point_end_offset_temp = [0, 0]

        self._screenshot_rect_region_edit = self.RectRegion.Unknown

        self._screenshot_modify_gap = 8

    def _set_action_screenshot_press_start_(self, event):
        self._screenshot_point_start = event.pos()
        if self._screenshot_mode == self.Mode.Started:
            self._screenshot_mode = self.Mode.New

        self._widget.update()

    def _set_action_screenshot_press_execute_(self, event):
        p = event.pos()
        if self._screenshot_mode == self.Mode.New:
            self._screenshot_rect_point_start.setX(self._screenshot_point_start.x())
            self._screenshot_rect_point_start.setY(self._screenshot_point_start.y())
            self._screenshot_rect_point_end = event.pos()
        elif self._screenshot_mode == self.Mode.Edit:
            d_p = p - self._screenshot_point_start
            d_p_x, d_p_y = d_p.x(), d_p.y()
            o_x_0, o_y_0 = self._screenshot_rect_point_start_offset_temp
            o_x_1, o_y_1 = self._screenshot_rect_point_end_offset_temp
            if self._screenshot_rect_region_edit == self.RectRegion.Inside:
                self._screenshot_rect_point_start_offset[0] = o_x_0 + d_p_x
                self._screenshot_rect_point_start_offset[1] = o_y_0 + d_p_y
                self._screenshot_rect_point_end_offset[0] = o_x_1 + d_p_x
                self._screenshot_rect_point_end_offset[1] = o_y_1 + d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Top:
                self._screenshot_rect_point_start_offset[1] = o_y_0 + d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Bottom:
                self._screenshot_rect_point_end_offset[1] = o_y_1 + d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Left:
                self._screenshot_rect_point_start_offset[0] = o_x_0 + d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.Right:
                self._screenshot_rect_point_end_offset[0] = o_x_1 + d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.TopLeft:
                self._screenshot_rect_point_start_offset[0] = o_x_0 + d_p_x
                self._screenshot_rect_point_start_offset[1] = o_y_0 + d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.TopRight:
                self._screenshot_rect_point_start_offset[1] = o_y_0 + d_p_y
                self._screenshot_rect_point_end_offset[0] = o_x_1 + d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.BottomLeft:
                self._screenshot_rect_point_start_offset[0] = o_x_0 + d_p_x
                self._screenshot_rect_point_end_offset[1] = o_y_1 + d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.BottomRight:
                self._screenshot_rect_point_end_offset[0] = o_x_1 + d_p_x
                self._screenshot_rect_point_end_offset[1] = o_y_1 + d_p_y

        self._set_screenshot_update_geometry_()
        self._widget.update()

    def _set_action_screenshot_hover_execute_(self, event):
        if self._screenshot_mode == self.Mode.Edit:
            pos = event.pos()

            x, y = self._screenshot_rect.x(), self._screenshot_rect.y()
            w, h = self._screenshot_rect.width(), self._screenshot_rect.height()

            m_x, m_y = pos.x(), pos.y()

            self._screenshot_rect_region_edit = self._get_rect_region_(
                m_x, m_y, x, y, w, h, 8
            )
            cursor = self.CURSOR_MAPPER[self._screenshot_rect_region_edit]

            self._widget.setCursor(QtGui.QCursor(cursor))

    def _set_action_screenshot_press_stop_(self, event):
        if self._screenshot_mode == self.Mode.New:
            if self._screenshot_rect_point_start != self._screenshot_rect_point_end:
                self._screenshot_mode = self.Mode.Edit
        elif self._screenshot_mode == self.Mode.Edit:
            self._screenshot_rect_point_start_offset_temp[0] = self._screenshot_rect_point_start_offset[0]
            self._screenshot_rect_point_start_offset_temp[1] = self._screenshot_rect_point_start_offset[1]
            self._screenshot_rect_point_end_offset_temp[0] = self._screenshot_rect_point_end_offset[0]
            self._screenshot_rect_point_end_offset_temp[1] = self._screenshot_rect_point_end_offset[1]

        self._widget.update()

    def _set_screenshot_update_geometry_(self):
        x, y = 0, 0
        w, h = self._widget.width(), self._widget.height()

        x_0, y_0 = self._screenshot_rect_point_start.x(), self._screenshot_rect_point_start.y()
        x_1, y_1 = self._screenshot_rect_point_end.x(), self._screenshot_rect_point_end.y()

        o_x_0, o_y_0 = self._screenshot_rect_point_start_offset
        o_x_1, o_y_1 = self._screenshot_rect_point_end_offset

        x_0 += o_x_0
        y_0 += o_y_0
        x_1 += o_x_1
        y_1 += o_y_1

        s_x, s_y = min(x_0, x_1), min(y_0, y_1)
        s_w, s_h = abs(x_1 - x_0), abs(y_1 - y_0)

        self._screenshot_rect.setRect(
            s_x, s_y, s_w, s_h
        )

        t_w, t_h = self._help_text_draw_size

        t_t_w, t_t_h = t_w - 48, t_h - 48

        self._help_frame_draw_rect.setRect(
            x + (w - t_w) / 2, y + (h - t_h) / 2, t_w, t_h
        )
        self._help_draw_rect.setRect(
            x + (w - t_t_w) / 2, y + (h - t_t_h) / 2, t_t_w, t_t_h
        )

    def _set_screenshot_cancel_(self):
        self.screenshot_finished.emit()
        self._widget.close()
        self._widget.deleteLater()

    def _set_screenshot_accept_(self):
        def fnc_():
            x, y, w, h = self._get_screenshot_accept_geometry_()
            self.screenshot_finished.emit()
            self.screenshot_accepted.emit([x, y, w, h])
            self._widget.close()
            self._widget.deleteLater()

        self._screenshot_mode = self.Mode.Stopped
        self._widget.update()

        AbsQtScreenshotDef.CACHE = self._get_screenshot_accept_geometry_()

        self._timer = QtCore.QTimer(self._widget)
        self._timer.singleShot(100, fnc_)

    def _set_screenshot_start_(self):
        self.screenshot_started.emit()
        self._widget.setGeometry(
            QtWidgets.QApplication.desktop().rect()
        )
        self._widget.show()
        self._widget.setCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
    @classmethod
    def _get_rect_region_(cls, m_x, m_y, x, y, w, h, gap):
        # top
        if x + gap < m_x < x + w - gap and y - gap < m_y < y + gap:
            return cls.RectRegion.Top
        # bottom
        elif x + gap < m_x < x + w - gap and y + h - gap < m_y < y + h + gap:
            return cls.RectRegion.Bottom
        # left
        elif x - gap < m_x < x + gap and y + gap < m_y < y + h - gap:
            return cls.RectRegion.Left
        # right
        elif x + w - gap < m_x < x + w + gap and y + gap < m_y < y + h - gap:
            return cls.RectRegion.Right
        # top left
        elif x - gap < m_x < x + gap and y - gap < m_y < y + gap:
            return cls.RectRegion.TopLeft
        # top right
        elif x + w - gap <= m_x <= x + w + gap and y - gap <= m_y <= y + gap:
            return cls.RectRegion.TopRight
        # bottom left
        elif x - gap < m_x < x + gap and y + h - gap < m_y < y + h + gap:
            return cls.RectRegion.BottomLeft
        # bottom right
        elif x + w - gap < m_x < x + w + gap and y + h - gap < m_y < y + h + gap:
            return cls.RectRegion.BottomRight
        # inside
        elif x + gap < m_x < x + w - gap and y + gap < m_y < y + h - gap:
            return cls.RectRegion.Inside
        else:
            return cls.RectRegion.Unknown

    def _get_screenshot_accept_geometry_(self):
        x, y = self._widget.x(), self._widget.y()

        rect_0 = self._screenshot_rect
        x_0, y_0, w_0, h_0 = rect_0.x(), rect_0.y(), rect_0.width(), rect_0.height()
        return x + x_0, y + y_0, w_0, h_0
    @classmethod
    def _set_screenshot_save_to_(cls, geometry, file_path):
        bsc_core.StgFileOpt(file_path).create_directory()
        rect = QtCore.QRect(*geometry)

        if bsc_core.ApplicationMtd.get_is_maya():
            main_window = QtMayaMtd.get_qt_main_window()
            s = QtGui.QPixmap.grabWindow(
                long(main_window.winId())
            )
            s.copy(rect).save(file_path)
        else:
            app_ = QtWidgets.QApplication

            s = app_.primaryScreen().grabWindow(
                app_.desktop().winId()
            )
            s.copy(rect).save(file_path)


class AbsQtItemDagLoading(object):
    def _set_item_dag_loading_def_init_(self, widget):
        self._widget = widget

        self._loading_item = None

    def _set_item_dag_loading_start_(self):
        self._loading_item = self._widget._set_child_add_()
        self._loading_item.setText(0, 'loading ...')

    def _set_item_dag_loading_end_(self):
        if self._loading_item is not None:
            self._loading_item._kill_item_all_show_runnables_()
            self._loading_item._stop_item_show_all_()
            self._widget.takeChild(
                self._widget.indexOfChild(self._loading_item)
            )
            self._loading_item = None