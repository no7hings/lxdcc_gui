# coding=utf-8
import collections
import copy
import os

import fnmatch

from lxbasic import bsc_configure

from lxutil_gui import utl_gui_configure

from lxutil_gui.qt.utl_gui_qt_core import *


class AbsQtWgtDef(object):
    def _set_wgt_def_init_(self, widget):
        self._widget = widget

    def _get_text_draw_width_(self, text=None):
        return self._widget.fontMetrics().width(text)


class AbsQtFocusDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_widget_focus_update_(self):
        raise NotImplementedError()

    def _set_focused_def_init_(self):
        self._is_focused = False
        self._focus_rect = QtCore.QRect()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        #
        self._set_widget_focus_update_()
        self._set_wgt_update_draw_()

    def _get_is_focused_(self):
        return self._is_focused

    def _set_focused_rect_(self, x, y, w, h):
        self._focus_rect.setRect(
            x, y, w, h
        )

    def _get_focus_rect_(self):
        return self._focus_rect


class AbsQtMenuDef(object):
    QT_MENU_CLASS = None
    def _set_menu_def_init_(self):
        self._menu_title_text = None
        self._menu_raw = []
        self._menu_content = None

    def _set_menu_title_text_(self, text):
        self._menu_title_text = text

    def _set_menu_raw_(self, menu_raw):
        self._menu_raw = menu_raw

    def _set_menu_raw_add_(self, menu_raw):
        if isinstance(menu_raw, list):
            self._menu_raw.extend(menu_raw)
        elif isinstance(menu_raw, tuple):
            pass

    def _set_menu_raw_extend_(self, raw):
        self._menu_raw.extend(raw)

    def _get_menu_raw_(self):
        return self._menu_raw

    def _set_menu_show_(self):
        menu_content = self._get_menu_content_()
        menu_raw = self._get_menu_raw_()
        #
        menu = None
        #
        if menu_content:
            if menu_content.get_is_empty() is False:
                if menu is None:
                    menu = self.QT_MENU_CLASS(self)
                #
                if self._menu_title_text is not None:
                    menu._set_title_text_(self._menu_title_text)
                #
                menu._set_menu_content_(menu_content)
                menu._set_show_()
        #
        if menu_raw:
            if menu is None:
                menu = self.QT_MENU_CLASS(self)
            #
            if self._menu_title_text is not None:
                menu._set_title_text_(self._menu_title_text)
            #
            menu._set_menu_raw_(menu_raw)
            menu._set_show_()

    def _set_menu_content_(self, content):
        self._menu_content = content

    def _get_menu_content_(self):
        return self._menu_content


class _QtStatusDef(object):
    Status = bsc_configure.Status
    @classmethod
    def _get_status_color_(cls, status):
        if status in [bsc_configure.Status.Failed, bsc_configure.Status.Error]:
            r, g, b = 255, 0, 63
            h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
            color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
            hover_color = r, g, b
        elif status in [bsc_configure.Status.Started, bsc_configure.Status.Waiting]:
            r, g, b = 255, 127, 63
            h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
            color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
            hover_color = r, g, b
        elif status in [bsc_configure.Status.Running]:
            r, g, b = 63, 127, 255
            h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
            color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
            hover_color = r, g, b
        elif status in [bsc_configure.Status.Completed, bsc_configure.Status.Finished]:
            r, g, b = 63, 255, 127
            h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
            color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
            hover_color = r, g, b
        else:
            color = QtBackgroundColor.Transparent
            hover_color = QtBackgroundColor.Transparent
        return color, hover_color

    def _set_status_def_init_(self):
        self._is_status_enable = False
        #
        self._status = bsc_configure.Status.Stopped
        #
        self._status_color = QtBackgroundColor.Transparent
        self._hover_status_color = QtBackgroundColor.Transparent
        #
        self._status_rect = QtCore.QRect()

    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_status_(self, status):
        self._is_status_enable = True
        self._status = status
        #
        if status in [bsc_configure.Status.Running]:
            # noinspection PyUnresolvedReferences
            self.setCursor(QtCore.Qt.BusyCursor)
        else:
            # noinspection PyUnresolvedReferences
            self.unsetCursor()
        #
        self._status_color, self._hover_status_color = self._get_status_color_(
            self._status
        )
        self._set_wgt_update_draw_()

    def _get_status_(self):
        return self._status

    def _get_status_is_enable_(self):
        return self._is_status_enable


class AbsQtRateDef(object):
    def _set_rate_def_init_(self):
        self._rate_is_enable = False
        #
        self._rate_statuses = []

        self._rate_text = ''
        #
        self._rate_colors = []
        self._hover_rate_colors = []
        #
        self._rate_rect = QtCore.QRect()

        self._rate_finished_results = []

        self._rate_start_timestamp = 0

    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_rate_statuses_(self, statuses):
        if statuses:
            self._rate_is_enable = True
            self._rate_statuses = statuses
            self._rate_colors = []
            self._hover_rate_colors = []
            for i_element_status in statuses:
                i_color, i_hover_color = _QtStatusDef._get_status_color_(i_element_status)
                self._rate_colors.append(i_color)
                self._hover_rate_colors.append(i_hover_color)
        else:
            self._rate_is_enable = False
            self._rate_statuses = []
            self._rate_colors = []
            self._hover_rate_colors = []
        #
        self._set_wgt_update_draw_()

    def _set_rate_status_update_at_(self, index, status):
        color, hover_color = _QtStatusDef._get_status_color_(status)
        self._rate_statuses[index] = status
        self._rate_colors[index] = color
        self._hover_rate_colors[index] = hover_color

        self._set_wgt_update_draw_()

    def _set_rate_initialization_(self, count, status):
        if count > 0:
            self._rate_is_enable = True
            self._rate_statuses = [status]*count
            color, hover_color = _QtStatusDef._get_status_color_(status)
            self._rate_colors = [color]*count
            self._hover_rate_colors = [hover_color]*count
            self._rate_finished_results = [False]*count

            self._rate_start_timestamp = bsc_core.SystemMtd.get_timestamp()
            self._set_rate_text_update_()
        else:
            self._set_rate_restore_()

        self._set_wgt_update_draw_()

    def _set_rate_restore_(self):
        self._rate_is_enable = False
        self._rate_statuses = []
        self._rate_colors = []
        self._hover_rate_colors = []
        self._rate_finished_results = []

        self._rate_text = ''

    def _set_rate_finished_at_(self, index, status):
        self._rate_finished_results[index] = True
        #
        self._set_rate_text_update_()
        #
        self._set_wgt_update_draw_()

    def _set_rate_text_update_(self):
        cost_timestamp = bsc_core.SystemMtd.get_timestamp() - self._rate_start_timestamp
        self._rate_text = '[{}/{}][{}]'.format(
            sum(self._rate_finished_results), len(self._rate_finished_results),
            bsc_core.IntegerMtd.second_to_time_prettify(cost_timestamp)
        )

    def _get_rate_is_finished_(self):
        return sum(self._rate_finished_results) == len(self._rate_finished_results)

    def _get_rate_is_enable_(self):
        return self._rate_is_enable

    def _set_rate_finished_connect_to_(self, fnc):
        raise NotImplementedError()


class AbsQtFrameDef(object):
    def _set_frame_def_init_(self):
        self._frame_border_color = QtBackgroundColor.Transparent
        self._hovered_frame_border_color = QtBackgroundColor.Transparent
        self._selected_frame_border_color = QtBackgroundColor.Transparent
        self._actioned_frame_border_color = QtBackgroundColor.Transparent
        #
        self._frame_background_color = QtBackgroundColor.Transparent
        self._hovered_frame_background_color = QtBackgroundColor.Transparent
        self._selected_frame_background_color = QtBackgroundColor.Transparent
        self._actioned_frame_background_color = QtBackgroundColor.Transparent
        #
        self._frame_border_radius = 0
        #
        self._frame_rect = QtCore.QRect()
        self._frame_size = 20, 20
        self._frame_draw_enable = False

    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_border_color_(self, color):
        self._frame_border_color = Color._get_qt_color_(color)
        self._set_wgt_update_draw_()

    def _set_background_color_(self, color):
        self._frame_background_color = Color._get_qt_color_(color)
        self._set_wgt_update_draw_()

    def _get_border_color_(self):
        return self._frame_border_color

    def _get_background_color_(self):
        return self._frame_background_color

    def _set_frame_rect_(self, x, y, w, h):
        self._frame_rect.setRect(
            x, y, w, h
        )

    def _get_frame_rect_(self):
        return self._frame_rect

    def _set_frame_size_(self, w, h):
        self._frame_size = w, h

    def _set_frame_draw_enable_(self, boolean):
        self._frame_draw_enable = boolean

    def _set_frame_border_radius_(self, radius):
        self._frame_border_radius = radius


class AbsQtDropDef(object):
    def _set_drop_def_init_(self, widget):
        self._widget = widget
        self._drop_region = 0
        self._drop_side = 2
        self._drop_margin = 8
        self._drop_shadow_radius = 4
    @classmethod
    def _get_drop_pos_(cls, widget):
        rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        p = widget.mapToGlobal(rect.bottomLeft())
        return p.x(), p.y()+1
    @classmethod
    def _get_drop_press_point_(cls, widget, rect=None):
        if rect is None:
            rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        return widget.mapToGlobal(rect.center())
    @classmethod
    def _get_drop_size_(cls, widget):
        rect = widget.rect()
        return rect.width(), rect.height()

    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_widget_geometry_update_(self):
        pass

    def _set_drop_start_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_drop_close_(self):
        self._widget.close()
        self._widget.deleteLater()

    def _set_drop_end_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_drop_fnc_0_(self, press_point, press_rect, desktop_rect, view_width, view_height):
        press_x, press_y = press_point.x(), press_point.y()
        press_w, press_h = press_rect.width(), press_rect.height()
        #
        width_maximum = desktop_rect.width()
        height_maximum = desktop_rect.height()
        #
        side = self._drop_side
        margin = self._drop_margin
        shadow_radius = self._drop_shadow_radius
        #
        o_x = 0
        o_y = 0
        #
        width_ = view_width+margin*2+side*2+shadow_radius
        height_ = view_height+margin*2+side*2+shadow_radius
        #
        r_x, r_y, region = bsc_core.CoordMtd.set_region_to(
            position=(press_x, press_y),
            size=(width_, height_),
            maximum_size=(width_maximum, height_maximum),
            offset=(o_x, o_y)
        )
        self._drop_region = region
        #
        if region in [0, 1]:
            y_ = r_y-side+press_h/2
        else:
            y_ = r_y+side+shadow_radius-press_h/2
        #
        if region in [0, 2]:
            x_ = r_x-margin*3
        else:
            x_ = r_x+margin*3+side+shadow_radius
        #
        self._widget.setGeometry(
            x_, y_,
            width_, height_
        )
        #
        self._set_widget_geometry_update_()
        #
        self._widget.show()
        self._set_wgt_update_draw_()

    def _set_drop_fnc_(self, pos, size):
        x, y = pos
        w, h = size
        # desktop_rect = get_qt_desktop_rect()
        self._widget.setGeometry(
            x, y,
            w, h
        )
        self._set_widget_geometry_update_()
        #
        self._widget.show()
        #
        self._widget.update()


class AbsQtIconDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_icon_def_init_(self):
        self._icon_is_enable = False
        self._icon_name_is_enable = False
        #
        self._icon_file_path = None
        self._hover_icon_file_path = None
        #
        self._color_icon_rgb = None
        self._icon_name_text = None
        #
        self._icon_frame_rect = QtCore.QRect()
        self._file_icon_rect = QtCore.QRect()
        self._color_icon_rect = QtCore.QRect()
        self._icon_name_text_rect = QtCore.QRect()
        #
        self._icon_frame_size = 20, 20
        self._file_icon_size = 16, 16
        self._color_icon_size = 12, 12
        self._icon_name_size = 14, 14

    def _set_icon_enable_(self, boolean):
        self._icon_is_enable = boolean

    def _set_name_icon_enable_(self, boolean):
        self._icon_name_is_enable = boolean

    def _set_icon_file_path_(self, file_path):
        self._icon_is_enable = True
        self._icon_file_path = file_path
        self._set_wgt_update_draw_()

    def _set_hover_icon_file_path_(self, file_path):
        self._hover_icon_file_path = file_path

    def _set_icon_frame_size_(self, w, h):
        self._icon_frame_size = w, h

    def _set_file_icon_size_(self, w, h):
        self._file_icon_size = w, h

    def _get_icon_file_path_(self):
        if self._icon_is_enable is True:
            return self._icon_file_path

    def _set_color_icon_rgb_(self, rgb):
        self._icon_is_enable = True
        self._color_icon_rgb = rgb
        self._set_wgt_update_draw_()

    def _set_icon_name_text_(self, text):
        self._icon_is_enable = True
        self._icon_name_text = text
        self._set_wgt_update_draw_()

    def _set_color_icon_rect_(self, x, y, w, h):
        self._color_icon_rect.setRect(
            x, y, w, h
        )

    def _set_icon_name_text_rect_(self, x, y, w, h):
        self._icon_name_text_rect.setRect(
            x, y, w, h
        )

    def _get_icon_name_text_(self):
        if self._icon_is_enable is True:
            return self._icon_name_text

    def _set_icon_frame_rect_(self, x, y, w, h):
        self._icon_frame_rect.setRect(
            x, y, w, h
        )

    def _set_file_icon_rect_(self, x, y, w, h):
        self._file_icon_rect.setRect(
            x, y, w, h
        )

    def _get_file_icon_rect_(self):
        return self._file_icon_rect


class _QtIconsDef(object):
    def _set_icons_def_init_(self):
        self._icons_enable = False
        self._pixmap_icons = []
        self._icon_file_paths = []
        self._icon_name_texts = []
        self._icon_indices = []
        self._icon_rects = []
        #
        self._icon_frame_size = 20, 20
        self._icon_size = 16, 16
        self._icon_frame_draw_enable = False
        #
        self._icon_frame_rect = QtCore.QRect()

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

    def _set_icons_by_pixmap_(self, icons):
        self._pixmap_icons = icons
        self._icon_indices = range(len(icons))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _get_icon_as_pixmap_at_(self, index):
        if index in self._get_icon_indices_():
            return self._pixmap_icons[index]

    def _get_icons_as_pixmap_(self):
        return self._pixmap_icons

    def _set_icon_file_path_(self, file_path):
        self._set_icon_file_paths_(
            [file_path]
        )

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

    def _get_has_icon_(self):
        return self._icon_indices != []

    def _get_icon_count_(self):
        return len(self._icon_indices)

    def _set_icon_frame_size_(self, w, h):
        self._icon_frame_size = w, h

    def _set_icon_size_(self, w, h):
        self._icon_size = w, h

    def _set_icon_frame_draw_enable_(self, boolean):
        self._icon_frame_draw_enable = boolean


class _QtIndexDef(object):
    def _set_index_def_init_(self):
        self._index_enable = False
        self._index = 0
        self._index_text = '1'
        self._index_text_color = QtFontColor.Dark
        self._index_text_font = Font.INDEX
        self._index_text_option = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        #
        self._index_frame_rect = QtCore.QRect()
        self._index_rect = QtCore.QRect()
        #
        self._index_frame_draw_enable = False
        self._index_draw_enable = False

    def _set_index_(self, index):
        self._index = index
        self._index_text = str(index+1)

    def _get_index_(self):
        return self._index

    def _get_index_text_(self):
        return self._index_text

    def _set_index_rect_(self, x, y, w, h):
        self._index_rect.setRect(
            x, y, w, h
        )

    def _get_index_rect_(self):
        return self._index_rect


class AbsQtTypeDef(object):
    def _set_type_def_init_(self):
        self._type_text = None
        self._type_rect = QtCore.QRect()
        self._type_color = QtGui.QColor(127, 127, 127, 255)

    def _set_type_text_(self, text):
        self._type_text = text
        self._type_color = bsc_core.TextOpt(
            self._type_text
        ).to_rgb()

    def _set_type_rect_(self, x, y, w, h):
        self._type_rect.setRect(
            x, y, w, h
        )


class AbsQtNameDef(object):
    def _set_name_def_init_(self):
        self._name_enable = False
        self._name_text = None
        self._name_text_font = Font.NAME
        self._name_color = QtFontColor.Basic
        self._hover_name_color = QtFontColor.Light
        self._name_text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        #
        self._name_width = 160
        #
        self._name_frame_rect = QtCore.QRect()
        self._name_rect = QtCore.QRect()

    def _set_name_color_(self, color):
        self._name_color = color

    def _set_wgt_update_draw_(self):
        raise NotImplementedError()
    # noinspection PyUnresolvedReferences
    def _get_name_text_draw_width_(self, text=None):
        if text is None:
            text = self._name_text
        return self.fontMetrics().width(text)

    def _set_name_text_(self, text):
        self._name_enable = True
        self._name_text = text
        # noinspection PyUnresolvedReferences
        self._set_wgt_update_draw_()

    def _get_name_text_option_(self):
        return self._name_text_option

    def _set_name_text_option_(self, option):
        self._name_text_option = option

    def _set_name_width_(self, w):
        self._name_width = w

    def _get_name_text_(self):
        if self._name_enable is True:
            return self._name_text

    def _set_name_frame_rect_(self, x, y, w, h):
        self._name_frame_rect.setRect(
            x, y, w, h
        )

    def _set_name_rect_(self, x, y, w, h):
        self._name_rect.setRect(
            x, y, w, h
        )

    def _get_name_rect_(self):
        return self._name_rect

    def _set_tool_tip_(self, raw, as_markdown_style=False):
        if isinstance(raw, (tuple, list)):
            _ = u'\n'.join(raw)
        elif isinstance(raw, (str, unicode)):
            _ = raw
        else:
            raise TypeError()
        #
        self._set_tool_tip_text_(_, as_markdown_style)

    def _set_tool_tip_text_(self, text, markdown_style=False):
        if hasattr(self, 'setToolTip'):
            if markdown_style is True:
                import markdown
                html = markdown.markdown(text)
                # noinspection PyCallingNonCallable
                self.setToolTip(html)
            else:
                html = '<html>\n<body>\n'
                html += '<h3>{}</h3>\n'.format(self._name_text)
                for i in text.split('\n'):
                    html += '<ul>\n<li><i>{}</i></li>\n</ul>\n'.format(i)
                html += '</body>\n</html>'
                # noinspection PyCallingNonCallable
                self.setToolTip(html)
    # noinspection PyUnresolvedReferences
    def _set_name_font_size_(self, size):
        self.setFont(self._name_text_font)
        font = self.font()
        font.setPointSize(size)
        self._name_text_font = font

    def _set_name_font_(self):
        pass


class AbsQtRgbaDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_rgba_def_init_(self):
        self._color_rgba = 1.0, 1.0, 1.0, 1.0
        self._color_rect = QtCore.QRect()

    def _set_color_rgba_(self, r, g, b, a):
        self._color_rgba = r, g, b, a
        self._set_wgt_update_draw_()

    def _get_color_rgba_(self):
        return self._color_rgba

    def _get_color_rgba_255_(self):
        return tuple(map(lambda x: int(x*255), self._color_rgba))

    def _get_color_rect_(self):
        return self._color_rect


class _QtPathDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_path_def_init_(self):
        self._path_text = None
        self._path_rect = QtCore.QRect()

    def _set_path_text_(self, text):
        self._path_text = text
        self._set_wgt_update_draw_()

    def _get_path_text_(self):
        return self._path_text

    def _set_path_rect_(self, x, y, w, h):
        self._path_rect.setRect(x, y, w, h)


class _QtProgressDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_widget_geometry_update_(self):
        pass

    def _set_progress_def_init_(self):
        self._progress_height = 2
        #
        self._progress_maximum_value = 0
        self._progress_value = 0
        #
        self._progress_map_maximum_ = 10
        self._progress_map_value_ = 0
        #
        self._progress_rect = QtCore.QRect()
        #
        self._progress_raw = []

    def _set_progress_height_(self, value):
        self._progress_height = value

    def _set_progress_run_(self):
        self._set_widget_geometry_update_()
        self._set_wgt_update_draw_()
        #
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_progress_maximum_(self, value):
        self._progress_maximum_value = value

    def _set_progress_map_maximum_(self, value):
        self._progress_map_maximum_ = value

    def _set_progress_value_(self, value):
        self._progress_value = value
        #
        if self._progress_map_maximum_ > 1:
            map_value = int(
                bsc_core.RangeMtd.set_map_to((1, self._progress_maximum_value), (1, self._progress_map_maximum_), self._progress_value)
            )
            if map_value != self._progress_map_value_:
                self._progress_map_value_ = map_value
                #
                self._set_progress_run_()

    def _set_progress_update_(self):
        self._set_progress_value_(self._progress_value+1)

    def _set_progress_stop_(self):
        self._set_progress_value_(0)
        self._progress_raw = []
        self._set_wgt_update_draw_()

    def _get_progress_percent_(self):
        return float(self._progress_map_value_) / float(self._progress_map_maximum_)

    def _set_progress_raw_(self, raw):
        self._progress_raw = raw

    def _get_progress_is_enable_(self):
        return self._progress_map_value_ != 0


class AbsQtImageDef(object):
    def _set_image_def_init_(self):
        self._image_enable = False
        #
        self._image_file_path = None
        self._image_name_text = None
        #
        self._image_frame_size = 32, 32
        self._image_size = 30, 30
        self._image_frame_draw_enable = False
        #
        self._image_frame_rect = QtCore.QRect(0, 0, 0, 0)
        self._image_rect = QtCore.QRect(0, 0, 0, 0)

    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_image_file_path_(self, file_path):
        self._image_enable = True
        self._image_file_path = file_path
        self._set_wgt_update_draw_()

    def _set_image_name_text_(self, text):
        self._image_name_text = text

    def _set_image_size_(self, size):
        self._image_size = size

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
                    # print bsc_core.VedioOpt(self._image_file_path).get_size()
        return self._image_size

    def _get_image_file_path_(self):
        if self._image_enable is True:
            return self._image_file_path

    def _set_image_rect_(self, x, y, w, h):
        self._image_rect.setRect(
            x, y, w, h
        )

    def _get_image_rect_(self):
        return self._image_rect

    def _get_has_image_(self):
        return (
            self._image_file_path is not None or
            self._image_name_text is not None
        )

    def _set_image_frame_draw_enable_(self, boolean):
        self._image_frame_draw_enable = boolean

    def _get_image_frame_rect_(self):
        return self._image_frame_rect


class AbsQtMovieDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()
    #
    def _set_movie_def_init_(self):
        self._movie_enable = False
        self._movie_rect = QtCore.QRect()

    def _get_movie_enable_(self):
        return self._movie_enable

    def _set_movie_enable_(self, boolean):
        self._movie_enable = boolean

    def _set_movie_rect_(self, x, y, w, h):
        self._movie_rect.setRect(x, y, w, h)


class AbsQtNamesDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_names_def_init_(self):
        self._names_enable = False
        self._name_texts = []
        self._name_indices = []
        self._name_text_rects = []
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
        self._name_frame_rect = QtCore.QRect(0, 0, 0, 0)

    def _set_name_text_at_(self, text, index=0):
        self._name_texts[index] = text

    def _get_name_text_at_(self, index=0):
        if index in self._get_name_indices_():
            return self._name_texts[index]

    def _set_name_text_rect_at_(self, x, y, w, h, index=0):
        self._name_text_rects[index].setRect(
            x, y, w, h
        )

    def _set_name_text_(self, text):
        self._set_name_texts_([text])

    def _get_name_text_(self):
        if self._name_texts:
            return u'+'.join(self._name_texts)

    def _set_name_texts_(self, texts):
        self._name_texts = texts
        self._name_indices = range(len(texts))
        self._name_text_rects = []
        for _ in self._get_name_indices_():
            self._name_text_rects.append(
                QtCore.QRect()
            )
        #
        self._set_wgt_update_draw_()

    def _get_name_texts_(self):
        return self._name_texts

    def _set_name_text_dict_(self, text_dict):
        self._name_text_dict = text_dict
        self._set_name_texts_(
            self._name_text_dict.values()
        )

    def _get_name_text_dict_(self):
        return self._name_text_dict

    def _set_name_frame_border_color_(self, color):
        self._name_frame_border_color = color

    def _get_name_frame_border_color_(self):
        return self._name_frame_border_color

    def _set_name_frame_background_color_(self, color):
        self._name_frame_background_color = color

    def _get_name_frame_background_color_(self):
        return self._name_frame_background_color

    def _get_name_rect_at_(self, index=0):
        return self._name_text_rects[index]

    def _get_name_indices_(self):
        return self._name_indices

    def _get_has_name_(self):
        return self._name_indices != []

    def _set_name_frame_size_(self, w, h):
        self._name_frame_size = w, h

    def _set_name_size_(self, w, h):
        self._name_size = w, h

    def _set_name_frame_draw_enable_(self, boolean):
        self._name_frame_draw_enable = boolean

    def _set_tool_tip_(self, raw, as_markdown_style=False):
        if raw is not None:
            if isinstance(raw, (tuple, list)):
                _ = u'\n'.join(raw)
            elif isinstance(raw, (str, unicode)):
                _ = raw
            else:
                raise TypeError()
            #
            self._set_tool_tip_text_(_, as_markdown_style)

    def _set_tool_tip_text_(self, text, markdown_style=False):
        if hasattr(self, 'setToolTip'):
            if markdown_style is True:
                import markdown
                html = markdown.markdown(text)
                # noinspection PyCallingNonCallable
                self.setToolTip(html)
            else:
                html = '<html>\n<body>\n'
                html += '<h3>{}</h3>\n'.format(self._get_name_text_())
                for i in text.split('\n'):
                    html += '<ul>\n<li><i>{}</i></li>\n</ul>\n'.format(i)
                html += '</body>\n</html>'
                # noinspection PyCallingNonCallable
                self.setToolTip(html)


class _QtChartDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()
    #
    def _set_chart_def_init_(self):
        self._chart_data = None
        self._chart_draw_data = None
        self._chart_mode = utl_configure.GuiSectorChartMode.Completion
        #
        self._hover_flag = False
        self._hover_point = QtCore.QPoint()
        #
        r, g, b = 143, 143, 143
        h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
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
        self._set_chart_update_data_()
        self._set_chart_data_post_run_()
        self._set_wgt_update_draw_()

    def _set_chart_data_post_run_(self):
        pass

    def _set_chart_update_data_(self):
        raise NotImplementedError()

    def _set_height_(self, h):
        # noinspection PyUnresolvedReferences
        self.setMaximumHeight(h)
        # noinspection PyUnresolvedReferences
        self.setMinimumHeight(h)


class AbsQtActionDef(object):
    ActionFlag = utl_gui_configure.ActionFlag
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_action_def_init_(self, widget):
        self._widget = widget
        self._action_flag = None
        #
        self._action_mdf_flags = []

    def _set_action_flag_(self, flag):
        if flag is not None:
            self._action_flag = flag
            self.__set_action_cursor_update_()
        #
        self._set_wgt_update_draw_()

    def _set_action_mdf_flags_(self, flags):
        self._action_mdf_flags = flags

    def _set_action_mdf_flag_add_(self, flag):
        if flag is not None:
            if flag not in self._action_mdf_flags:
                self._action_mdf_flags.append(flag)
        #
        self._set_wgt_update_draw_()

    def __set_action_cursor_update_(self):
        if self._action_flag is not None:
            if self._action_flag in [
                self.ActionFlag.PressClick,
                self.ActionFlag.PressDbClick,
                #
                self.ActionFlag.TrackClick,
                #
                self.ActionFlag.CheckClick,
                self.ActionFlag.ExpandClick,
                self.ActionFlag.OptionClick,
                self.ActionFlag.ChooseClick,
            ]:
                self._widget.setCursor(
                    QtGui.QCursor(
                        QtCore.Qt.PointingHandCursor
                    )
                )
            elif self._action_flag in [
                self.ActionFlag.PressMove,
            ]:
                self._widget.setCursor(
                    QtCore.Qt.OpenHandCursor
                )
            elif self._action_flag in [
                self.ActionFlag.TrackMove,
                self.ActionFlag.ZoomMove,
                self.ActionFlag.NGNodePressMove
            ]:
                self._widget.setCursor(
                    QtGui.QCursor(
                        QtGui.QPixmap(
                            utl_gui_core.RscIconFile.get('system/track-move')
                        )
                    )
                )
            elif self._action_flag in [
                self.ActionFlag.TrackCircle,
            ]:
                self._widget.setCursor(
                    QtGui.QCursor(
                        QtGui.QPixmap(
                            utl_gui_core.RscIconFile.get('system/track-circle')
                        )
                    )
                )
            elif self._action_flag in [
                self.ActionFlag.SplitHHover,
                self.ActionFlag.SplitHClick,
                self.ActionFlag.SplitHMove,
            ]:
                self._widget.setCursor(
                    QtGui.QCursor(
                        QtGui.QPixmap(
                            utl_gui_core.RscIconFile.get('system/split-h')
                        )
                    )
                )
            elif self._action_flag in [
                self.ActionFlag.SplitVHover,
                self.ActionFlag.SplitVClick,
                self.ActionFlag.SplitVMove
            ]:
                self._widget.setCursor(
                    QtGui.QCursor(
                        QtGui.QPixmap(
                            utl_gui_core.RscIconFile.get('system/split-v')
                        )
                    )
                )
            elif self._action_flag in [
                self.ActionFlag.RectSelectMove,
            ]:
                self._widget.setCursor(
                    QtGui.QCursor(
                        QtGui.QPixmap(
                            utl_gui_core.RscIconFile.get('system/rect-select')
                        )
                    )
                )
        else:
            self._widget.unsetCursor()

    def _get_action_flag_(self):
        return self._action_flag

    def _set_action_flag_clear_(self):
        self._action_flag = None
        #
        self.__set_action_cursor_update_()
        #
        self._set_wgt_update_draw_()

    def _set_action_mdf_flag_clear_(self):
        self._action_mdf_flags = []
        self._set_wgt_update_draw_()

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


class AbsQtActionHoverDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_action_hover_def_init_(self):
        self._item_is_enable = True
        self._is_hovered = False

    def _set_action_enable_(self, boolean):
        self._item_is_enable = boolean

    def _get_action_is_enable_(self):
        return self._item_is_enable

    def _set_hovered_(self, boolean):
        self._is_hovered = boolean
        #
        self._set_wgt_update_draw_()

    def _get_is_hovered_(self):
        return self._is_hovered

    def _set_action_hover_filter_execute_(self, event):
        if event.type() == QtCore.QEvent.Enter:
            self._set_hovered_(True)
        elif event.type() == QtCore.QEvent.Leave:
            self._set_hovered_(False)

    def _set_action_hover_execute_(self, event):
        pass


class AbsQtActionPressDef(object):
    press_clicked = qt_signal()
    press_db_clicked = qt_signal()
    press_toggled = qt_signal(bool)
    #
    clicked = qt_signal()
    db_clicked = qt_signal()
    #
    ActionFlag = utl_gui_configure.ActionFlag
    def _set_action_press_def_init_(self):
        self._press_is_enable = True
        self._press_is_clicked = False
        #
        self._press_rect = QtCore.QRect()

        self._press_db_clicked_methods = []

    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

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
        self._press_is_clicked = boolean

    def _get_is_pressed_(self):
        return self._press_is_clicked

    def _set_press_click_emit_send_(self):
        self.clicked.emit()
        self.press_clicked.emit()

    def _set_press_db_click_emit_send_(self):
        self.press_db_clicked.emit()

    def _get_is_press_click_flag_(self):
        return self._get_action_flag_is_match_(
            self.ActionFlag.PressClick
        )

    def _set_press_db_clicked_method_add_(self, fnc):
        self._press_db_clicked_methods.append(fnc)


class AbsQtActionCheckDef(object):
    check_clicked = qt_signal()
    check_toggled = qt_signal(bool)
    #
    ActionFlag = utl_gui_configure.ActionFlag
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _set_action_check_def_init_(self):
        self._is_check_enable = False
        #
        self._item_check_icon_file_path = None
        self._item_check_icon_file_path_0 = utl_core.Icon.get('box_unchecked')
        self._item_check_icon_file_path_1 = utl_core.Icon.get('box_checked')
        #
        self._item_is_checked = False
        self._item_check_frame_rect = QtCore.QRect()
        self._item_check_icon_rect = QtCore.QRect()

    def _set_action_check_enable_(self, boolean):
        self._is_check_enable = boolean

    def _get_action_check_is_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._is_check_enable
        return False

    def _set_item_checked_(self, boolean):
        self._item_is_checked = boolean
        self._set_item_check_update_()

    def _get_item_is_checked_(self):
        return self._item_is_checked

    def _set_item_check_swap_(self):
        self._item_is_checked = not self._item_is_checked
        self._set_item_check_update_()

    def _set_item_check_update_(self):
        self._item_check_icon_file_path = [
            self._item_check_icon_file_path_0, self._item_check_icon_file_path_1
        ][self._item_is_checked]
        #
        self._set_wgt_update_draw_()

    def _set_item_check_frame_rect_(self, x, y, w, h):
        self._item_check_frame_rect.setRect(
            x, y, w, h
        )

    def _set_item_check_icon_rect_(self, x, y, w, h):
        self._item_check_icon_rect.setRect(
            x, y, w, h
        )

    def _set_item_check_action_run_(self):
        self._set_item_check_swap_()
        #
        self.check_clicked.emit()
        self.check_toggled.emit(self._item_is_checked)

    def _set_item_check_changed_connect_to_(self, fnc):
        self.check_clicked.connect(fnc)


class _QtItemExpandActionDef(object):
    expand_clicked = qt_signal()
    expand_toggled = qt_signal(bool)
    #
    EXPAND_TOP_TO_BOTTOM = 0
    EXPAND_BOTTOM_TO_TOP = 1
    #
    ActionFlag = utl_gui_configure.ActionFlag
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_item_expand_action_def_init_(self):
        self._item_is_expand_enable = False
        #
        self._item_expand_icon_file_path = None
        self._item_expand_icon_file_path_0 = utl_core.Icon.get('box_checked')
        self._item_expand_icon_file_path_1 = utl_core.Icon.get('box_unchecked')
        self._item_is_expanded = False
        #
        self._item_expand_frame_rect = QtCore.QRect()
        self._item_expand_icon_rect = QtCore.QRect()
        #
        self._item_expand_direction = self.EXPAND_TOP_TO_BOTTOM

    def _set_item_expanded_(self, boolean):
        self._item_is_expanded = boolean
        self._set_item_expand_update_()

    def _get_item_is_expanded_(self):
        return self._item_is_expanded

    def _set_item_expanded_swap_(self):
        self._item_is_expanded = not self._item_is_expanded
        self._set_item_expand_update_()

    def _set_item_expand_update_(self):
        pass

    def _set_item_expand_direction_(self, direction):
        self._item_expand_direction = direction
        self._set_item_expand_update_()

    def _set_item_expand_action_run_(self):
        self._set_item_expanded_swap_()
        # noinspection PyUnresolvedReferences
        self.expand_clicked.emit()
        self.expand_toggled.emit(self._item_is_expanded)

    def _get_expand_icon_file_path_(self):
        pass


class _QtItemOptionPressActionDef(object):
    checked = qt_signal()
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _set_item_option_press_action_def_init_(self):
        self._option_click_enable = False
        self._option_icon_file_path = utl_core.Icon.get('option')
        #
        self._option_click_rect = QtCore.QRect()
        self._option_click_icon_rect = QtCore.QRect()

    def _set_item_option_click_enable_(self, boolean):
        self._option_click_enable = boolean

    def _get_item_option_click_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._option_click_enable
        return False


class AbsQtItemActionChooseDef(object):
    choose_changed = qt_signal()
    def _set_item_action_choose_def_init_(self):
        self._choose_expand_icon_file_path = utl_core.Icon.get('choose_expand')
        self._choose_collapse_icon_file_path = utl_core.Icon.get('choose_collapse')
        #
        self._path_text = None
        #
        self._rect = QtCore.QRect()
        #
        self._item_choose_is_dropped = False
        #
        self._item_choose_content_raw = None
        self._item_choose_name_texts = []
        self._item_choose_path_texts = []

    def _get_item_choose_is_dropped_(self):
        return self._item_choose_is_dropped

    def _set_item_choose_dropped_(self, boolean):
        self._item_choose_is_dropped = boolean

    def _set_item_choose_content_raw_(self, raw):
        self._item_choose_content_raw = raw
        if isinstance(raw, (tuple, list)):
            self._item_choose_name_texts = list(raw)

    def _set_item_choose_content_name_texts_(self, contents):
        self._item_choose_name_texts = contents

    def _get_item_choose_content_name_texts_(self):
        return self._item_choose_name_texts

    def _set_item_choose_changed_emit_send_(self):
        self.choose_changed.emit()

    def _set_item_choose_changed_connect_to_(self, fnc):
        self.choose_changed.connect(fnc)


class _QtItemEntryActionDef(object):
    def _set_item_entry_def_init_(self):
        self._entry_enable = False

    def _set_item_entry_enable_(self, boolean):
        self._entry_enable = boolean

    def _set_item_entry_finished_connect_to_(self, fnc):
        pass

    def _set_item_entry_changed_connect_to_(self, fnc):
        pass


class _QtViewBarDef(object):
    pass


class AbsQtGuideChooseActionDef(object):
    CHOOSE_RECT_CLS = None
    CHOOSE_DROP_FRAME_CLASS = None
    #
    choose_item_changed = qt_signal()
    choose_item_clicked = qt_signal()
    choose_item_double_clicked = qt_signal()
    #
    CHOOSE_FLAG = utl_gui_configure.ActionFlag.ChooseClick
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _set_guide_choose_action_def_init_(self):
        self._choose_items = []
        self._guide_choose_current_index = None

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _get_action_flag_is_match_(self, flag):
        raise NotImplementedError()

    def _get_guide_choose_items_(self):
        return self._choose_items

    def _get_guide_choose_item_indices_(self):
        return range(len(self._get_guide_choose_items_()))

    def _get_guide_choose_item_at_(self, index=0):
        return self._get_guide_choose_items_()[index]

    def _get_guide_choose_item_point_at_(self, index=0):
        raise NotImplementedError()

    def _get_guide_choose_item_rect_at_(self, index=0):
        raise NotImplementedError()

    def _set_guide_choose_item_current_at_(self, text, index=0):
        self._get_guide_choose_item_at_(index)._set_name_text_(text)

    def _get_guide_choose_item_current_at_(self, index=0):
        return self._get_guide_choose_item_at_(index)._name_text
    #
    def _set_guide_choose_item_content_at_(self, raw, index=0):
        self._get_guide_choose_item_at_(index)._set_item_choose_content_raw_(raw)
    #
    def _set_guide_choose_item_content_name_texts_at_(self, texts, index=0):
        self._get_guide_choose_item_at_(index)._set_item_choose_content_name_texts_(texts)
    #
    def _get_guide_choose_item_content_name_texts_at_(self, index=0):
        return self._get_guide_choose_item_at_(index)._get_item_choose_content_name_texts_()

    def _set_guide_choose_item_drop_at_(self, index=0):
        widget = self.CHOOSE_DROP_FRAME_CLASS(self)
        widget._set_drop_start_(
            index
        )

    def _set_guide_choose_item_expanded_at_(self, boolean, index=0):
        item = self._get_guide_choose_item_at_(index)
        item._set_item_choose_dropped_(boolean)

    def _get_guide_choose_item_is_expanded_at_(self, index=0):
        item = self._get_guide_choose_item_at_(index)
        return item._get_item_choose_is_dropped_()

    def _set_guide_choose_item_expand_at_(self, index=0):
        self._set_guide_choose_item_expanded_at_(True, index)

    def _set_guide_choose_item_collapse_at_(self, index=0):
        self._set_guide_choose_item_expanded_at_(False, index)

    def _get_is_choose_flag_(self):
        return self._get_action_flag_is_match_(self.CHOOSE_FLAG)

    def _set_guide_choose_clear_(self):
        self._guide_choose_current_index = None
        #
        self._choose_items = []

    def _set_guide_choose_item_create_(self):
        item = self.CHOOSE_RECT_CLS()
        self._choose_items.append(item)
        return item

    def _set_guide_choose_item_clicked_emit_send_(self):
        self.choose_item_clicked.emit()

    def _set_guide_choose_item_db_clicked_emit_send_(self):
        self.choose_item_double_clicked.emit()

    def _set_guide_choose_item_changed_emit_send_(self):
        self.choose_item_changed.emit()

    def _set_guide_choose_current_index_(self, index):
        self._guide_choose_current_index = index

    def _set_guide_choose_current_clear_(self):
        self._guide_choose_current_index = None


class AbsQtGuideActionDef(object):
    guide_item_clicked = qt_signal()
    guide_item_double_clicked = qt_signal()
    def _set_guide_action_def_init_(self):
        self._guide_items = []
        self._view_guide_current_index = None

    def _get_view_guide_items_(self):
        return self._guide_items

    def _get_view_guide_item_indices_(self):
        return range(len(self._get_view_guide_items_()))

    def _get_view_guide_item_at_(self, index=0):
        return self._get_view_guide_items_()[index]

    def _set_view_guide_clear_(self):
        self._guide_items = []
        self._view_guide_current_index = None

    def _set_view_guide_current_index_(self, index):
        self._view_guide_current_index = index

    def _set_view_guide_current_clear_(self):
        self._view_guide_current_index = None

    def _set_view_guide_item_name_text_at_(self, text, index=0):
        self._get_view_guide_item_at_(index)._set_name_text_(text)

    def _get_view_guide_item_name_text_at_(self, index=0):
        return self._get_view_guide_item_at_(index)._name_text

    def _get_view_guide_item_path_text_at_(self, index=0):
        return self._get_view_guide_item_at_(index)._path_text
    #
    def _set_view_guide_item_path_text_at_(self, text, index=0):
        self._get_view_guide_item_at_(index)._set_path_text_(text)
    #
    def _get_view_guide_current_path_(self):
        if self._view_guide_current_index is not None:
            return self._get_view_guide_item_path_text_at_(
                self._view_guide_current_index
            )

    def _set_view_guide_current_path_(self, path_text):
        pass
    # emit
    def _set_view_guide_item_clicked_emit_send_(self):
        self.guide_item_clicked.emit()

    def _set_view_guide_item_double_clicked_emit_send_(self):
        self.guide_item_double_clicked.emit()


class AbsQtActionSelectDef(object):
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()
    #
    def _set_action_select_def_init_(self):
        self._item_is_selected = False

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _set_selected_(self, boolean):
        self._item_is_selected = boolean
        self._set_wgt_update_draw_()

    def _get_is_selected_(self):
        return self._item_is_selected


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


class AbsQtBuildItemDef(object):
    def _set_build_item_def_init_(self):
        pass

    def _get_view_(self):
        raise NotImplementedError()

    def _set_build_item_setup_(self, view):
        self._build_runnable_runner = view._build_runnable_runner

    def _set_build_item_runnable_create_(self, cache_fnc, build_fnc, post_fnc=None):
        return self._build_runnable_runner.set_thread_create(
            cache_fnc, build_fnc, post_fnc
        )

    def _set_build_item_thread_create_(self, cache_fnc, build_fnc, post_fnc=None):
        thread = QtBuildThread(self._get_view_())
        thread.set_cache_fnc(cache_fnc)
        thread.built.connect(build_fnc)
        if post_fnc is not None:
            thread.run_finished.connect(post_fnc)
        return thread


class AbsQtBuildViewDef(object):
    def _set_build_view_def_init_(self):
        pass

    def _set_build_view_setup_(self, view):
        self._build_runnable_runner = QtBuildRunnableRunner(
            view
        )


class AbsShowItemDef(
    AbsQtBuildItemDef
):
    ShowStatus = bsc_configure.ShowStatus
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _get_view_(self):
        raise NotImplementedError()

    def _get_item_widget_(self):
        raise NotImplementedError()

    def _set_show_item_def_init_(self):
        #
        if bsc_core.ApplicationMtd.get_is_maya():
            self._item_show_use_thread = False
        else:
            self._item_show_use_thread = True
        #
        self._item_show_thread = None
        self._item_show_image_thread = None
        #
        self._item_show_cache_fnc = None
        self._item_show_build_fnc = None
        #
        self._item_show_status = self.ShowStatus.Stopped
        # image
        self._item_show_image_cache_fnc = None
        self._item_show_image_build_fnc = None
        #
        self._item_show_image_status = self.ShowStatus.Stopped

        self._set_build_item_def_init_()

    def _set_item_show_def_setup_(self, view):
        self._set_build_item_setup_(view)

        self._item_show_runnable = None
        self._item_show_image_runnable = None
        #
        self._item_show_timer = QtCore.QTimer(view)
        self._item_show_loading_index = 0
        self._item_show_loading_timer = QtCore.QTimer(view)
        #
        self._item_show_image_timer = QtCore.QTimer(view)
        self._item_show_image_loading_index = 0
        self._item_show_image_loading_timer = QtCore.QTimer(view)
        #
        self._item_show_image_sub_process = None
        self._item_show_image_cmd = None
        self._item_show_image_file_path = None

    def _set_item_show_method_(self, method):
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
                if self._get_item_is_viewport_show_able_() is True:
                    self._set_item_show_start_()

    def _set_item_show_fnc_start_(self):
        if self._item_show_status == self.ShowStatus.Waiting:
            if self._item_show_use_thread is True:
                self._item_show_status = self.ShowStatus.Loading
                #
                self._item_show_thread = self._set_build_item_runnable_create_(
                    self._item_show_cache_fnc,
                    self._item_show_build_fnc,
                    self._set_item_show_fnc_stop_
                )
                #
                self._item_show_thread.set_start()
            else:
                self._item_show_build_fnc(
                    self._item_show_cache_fnc()
                )
                self._set_item_show_fnc_stop_()

    def _set_item_show_fnc_stop_(self):
        self._set_item_show_stop_(
            self.ShowStatus.Completed
        )

    def _set_item_show_start_(self, time=50, force=False):
        def run_fnc():
            if self._item_show_cache_fnc is not None:
                self._set_item_show_fnc_start_()
        #
        if self._item_show_status == self.ShowStatus.Waiting or force is True:
            self._set_item_show_start_loading_()
            #
            self._item_show_timer.timeout.connect(run_fnc)
            self._item_show_timer.start(time)

    def _set_item_show_stop_(self, status):
        self._item_show_status = status
        self._item_show_timer.stop()
        self._set_item_show_stop_loading_()

    def _get_item_show_is_finished_(self):
        return self._item_show_status in [
            self.ShowStatus.Completed, self.ShowStatus.Failed
        ]
    # loading
    def _set_item_show_start_loading_(self):
        if self._item_show_status == self.ShowStatus.Waiting:
            self._set_item_show_update_loading_()
            self._item_show_loading_timer.timeout.connect(
                self._set_item_show_update_loading_
            )
            self._item_show_loading_timer.start(100)

    def _set_item_show_update_loading_(self):
        self._item_show_loading_index += 1
        # self._set_wgt_update_draw_()

    def _set_item_show_stop_loading_(self):
        self._item_show_loading_timer.stop()
        # self._set_wgt_update_draw_()
    # image fnc
    def _set_item_show_image_cmd_(self, image_file_path, cmd):
        def cache_fnc_():
            return []

        def build_fnc_(data):
            # noinspection PyBroadException
            try:
                bsc_core.SubProcessMtd.set_run_with_result(
                    cmd
                )
            except:
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
                if self._get_item_is_viewport_show_able_() is True:
                    self._set_item_show_image_start_()

    def _set_item_show_image_fnc_start_(self):
        if self._item_show_image_status == self.ShowStatus.Waiting:
            if self._item_show_use_thread is True:
                self._item_show_image_thread = self._set_build_item_runnable_create_(
                    self._item_show_image_cache_fnc,
                    self._item_show_image_build_fnc,
                    self._set_item_show_image_fnc_stop_
                )
                #
                self._item_show_image_thread.set_start()
            else:
                self._item_show_image_build_fnc(
                    self._item_show_image_cache_fnc()
                )
                self._set_item_show_image_fnc_stop_()
            #
            self._item_show_image_status = self.ShowStatus.Loading

    def _set_item_show_image_fnc_stop_(self):
        if self._item_show_image_file_path is not None:
            if os.path.isfile(self._item_show_image_file_path) is True:
                self._set_item_show_image_stop_(self.ShowStatus.Completed)
            else:
                self._set_item_show_image_stop_(self.ShowStatus.Failed)

    def _set_item_show_image_start_(self, time=50, force=False):
        def run_fnc():
            if self._item_show_cache_fnc is not None:
                self._set_item_show_image_fnc_start_()
        #
        if self._item_show_image_status == self.ShowStatus.Waiting or force is True:
            self._set_item_show_image_start_loading_()
            #
            self._item_show_image_timer.timeout.connect(run_fnc)
            self._item_show_image_timer.start(time)

    def _set_item_show_image_stop_(self, status):
        self._item_show_image_status = status
        if status == self.ShowStatus.Failed:
            item_widget = self._get_item_widget_()
            if item_widget is not None:
                item_widget._set_image_file_path_(
                    utl_gui_core.RscIconFile.get('image_loading_failed_error')
                )
        #
        self._item_show_image_timer.stop()
        self._set_item_show_image_stop_loading_()

    def _get_item_is_viewport_show_able_(self):
        raise NotImplementedError()

    def _set_item_show_image_start_loading_(self):
        if self._item_show_image_status == self.ShowStatus.Waiting:
            self._set_item_show_image_update_loading_()
            self._item_show_image_loading_timer.timeout.connect(
                self._set_item_show_image_update_loading_
            )
            self._item_show_image_loading_timer.start(100)

    def _set_item_show_image_update_loading_(self):
        self._item_show_image_loading_index += 1
        # self._set_wgt_update_draw_()

    def _set_item_show_image_stop_loading_(self):
        self._item_show_image_loading_timer.stop()
        # self._set_wgt_update_draw_()

    def _set_item_show_start_all_(self, force=False):
        self._set_item_show_start_(force=force)
        self._set_item_show_image_start_(force=force)

    def _set_item_show_stop_all_(self):
        self._set_item_show_stop_(self.ShowStatus.Stopped)
        self._set_item_show_image_stop_(self.ShowStatus.Stopped)

    def _set_item_show_kill_all_(self):
        if self._item_show_thread is not None:
            self._item_show_thread.set_kill()
        #
        if self._item_show_image_thread is not None:
            self._item_show_image_thread.set_kill()

    def _set_item_viewport_visible_(self, boolean):
        if boolean is True:
            self._set_item_show_start_all_()
        #
        self._set_item_widget_visible_(boolean)

    def _set_item_widget_visible_(self, boolean):
        raise NotImplementedError()

    def _set_viewport_show_enable_(self, boolean):
        self._is_viewport_show_enable = boolean

    def _set_item_show_start_auto_(self):
        if self._get_item_is_viewport_show_able_() is True:
            self._set_item_show_start_all_()

    def _set_item_show_force_(self):
        self._set_item_show_start_all_(force=True)


class AbsQtItemEntryActionDef(object):
    entry_changed = qt_signal()
    def _set_wgt_update_draw_(self):
        raise NotImplementedError()

    def _get_action_flag_(self):
        raise NotImplementedError()
    #
    def _set_item_entry_action_def_init_(self):
        self._item_is_entered = False
        self._entry_frame_rect = QtCore.QRect()
        self._entry_rect = QtCore.QRect()

    def _set_entered_(self, boolean):
        self._item_is_entered = boolean
        self._set_wgt_update_draw_()

    def _set_entry_frame_rect_(self, x, y, w, h):
        self._entry_frame_rect.setRect(
            x, y, w, h
        )

    def _get_entry_frame_rect_(self):
        return self._entry_frame_rect


class AbsQtViewSelectActionDef(object):
    def _set_view_select_action_def_init_(self):
        self._pre_selected_item = None

    def _set_view_item_selected_(self, item, boolean):
        raise NotImplementedError()

    def _set_item_widget_selected_(self, item, boolean):
        raise NotImplementedError()

    def _get_selected_items_(self):
        raise NotImplementedError()

    def _get_selected_item_widgets_(self):
        raise NotImplementedError()

    def _set_item_select_update_(self):
        raise NotImplementedError()


class _QtVScrollBar(QtWidgets.QScrollBar):
    def __init__(self, *args, **kwargs):
        pass


class AbsQtViewScrollActionDef(object):
    def _set_view_scroll_action_def_init_(self):
        pass

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
            return float(v)/float(v_max)
        return 0


class AbsQtViewTagFilterSrcDef(object):
    def _set_view_tag_filter_src_def_init_(self):
        pass


class AbsQtItemFilterTgtDef(object):
    def _set_item_filter_tgt_def_init_(self):
        self._item_tag_filter_tgt_mode = 'A+B'
        self._item_tag_filter_tgt_keys = []
        #
        self._item_tag_filter_tgt_statistic_enable = False
        #
        self._item_keyword_filter_keys = []
        self._item_keyword_filter_contexts = []

    def _set_item_tag_filter_tgt_mode_(self, mode):
        self._item_tag_filter_tgt_mode = mode

    def _get_item_tag_filter_tgt_mode_(self):
        return self._item_tag_filter_tgt_mode

    def _set_item_tag_filter_tgt_key_add_(self, key, ancestors=False):
        if key not in self._item_tag_filter_tgt_keys:
            self._item_tag_filter_tgt_keys.append(key)
        #
        if ancestors is True:
            self._set_item_tag_filter_tgt_ancestors_update_()

    def _get_item_tag_filter_tgt_keys_(self):
        return self._item_tag_filter_tgt_keys

    def _set_item_tag_filter_tgt_ancestors_update_(self):
        pass

    def _set_item_tag_filter_tgt_statistic_enable_(self, boolean):
        self._item_tag_filter_tgt_statistic_enable = boolean

    def _get_item_tag_filter_tgt_statistic_enable_(self):
        return self._item_tag_filter_tgt_statistic_enable

    def _get_item_tag_filter_tgt_match_args_(self, tag_filter_src_all_keys):
        tag_filter_tgt_keys = self._get_item_tag_filter_tgt_keys_()
        tag_filter_tgt_mode = self._get_item_tag_filter_tgt_mode_()
        if tag_filter_tgt_keys:
            if tag_filter_tgt_mode == 'A+B':
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key not in tag_filter_src_all_keys:
                        return True, True
            elif tag_filter_tgt_mode == 'A/B':
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key in tag_filter_src_all_keys:
                        return True, False
            return True, False
        return False, False

    def _get_item_keyword_filter_tgt_keys_(self):
        return self._item_keyword_filter_keys

    def _set_item_keyword_filter_tgt_contexts_(self, contexts):
        self._item_keyword_filter_contexts = contexts

    def _get_item_keyword_filter_tgt_contexts_(self):
        return self._item_keyword_filter_contexts

    def _get_item_keyword_filter_match_args_(self, keyword):
        if keyword:
            keyword = keyword.lower()
            keyword_filter_contexts = self._get_item_keyword_filter_tgt_contexts_() or []
            if keyword_filter_contexts:
                context = u'+'.join(keyword_filter_contexts)
            else:
                context = u'+'.join([i for i in self._get_item_keyword_filter_tgt_keys_() if i])
            #
            context = context.lower()
            if '*' in keyword:
                filter_key = u'*{}*'.format(keyword.lstrip('*').rstrip('*'))
                if fnmatch.filter([context], filter_key):
                    return True, False
            else:
                filter_key = u'*{}*'.format(keyword)
                if fnmatch.filter([context], filter_key):
                    return True, False
            return True, True
        return False, False


class AbsQtViewFilterTgtDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _set_view_filter_tgt_def_init_(self):
        self._view_tag_filter_tgt_keys = []

    def _get_view_tag_filter_tgt_statistic_raw_(self):
        dic = {}
        items = self._get_all_items_()
        for i_item in items:
            enable = i_item._get_item_tag_filter_tgt_statistic_enable_()
            if enable is True:
                i_keys = i_item._get_item_tag_filter_tgt_keys_()
                for j_key in i_keys:
                    dic.setdefault(j_key, []).append(i_item)
        return dic

    def _set_view_tag_filter_tgt_keys_(self, keys):
        self._view_tag_filter_tgt_keys = keys

    def _get_view_tag_filter_tgt_keys_(self):
        return self._view_tag_filter_tgt_keys

    def _set_view_items_visible_by_any_filter_(self, keyword):
        tag_filter_src_all_keys = self._get_view_tag_filter_tgt_keys_()
        self._keyword_filter_item_prxes = []
        #
        items = self._get_all_items_()
        for i_item in items:
            i_tag_filter_hidden_ = False
            i_keyword_filter_hidden_ = False
            if tag_filter_src_all_keys:
                i_tag_filter_is_enable, i_tag_filter_hidden = i_item._get_item_tag_filter_tgt_match_args_(tag_filter_src_all_keys)
                if i_tag_filter_is_enable is True:
                    i_tag_filter_hidden_ = i_tag_filter_hidden
            #
            if keyword:
                i_keyword_filter_enable, i_keyword_filter_hidden = i_item._get_item_keyword_filter_match_args_(keyword)
                if i_keyword_filter_enable is True:
                    i_keyword_filter_hidden_ = i_keyword_filter_hidden
            #
            if True in [i_tag_filter_hidden_, i_keyword_filter_hidden_]:
                is_hidden = True
            else:
                is_hidden = False
            #
            i_item._set_hidden_(is_hidden)
            for i in i_item._get_ancestors_():
                if is_hidden is False:
                    i._set_hidden_(False)


class AbsQtItemStateDef(object):
    def _set_item_state_def_init_(self):
        self._item_state = utl_gui_core.State.NORMAL
        self._item_state_color = Brush.TEXT_NORMAL

    def _set_item_state_(self, status, *args, **kwargs):
        self._item_state = status

    def _get_item_state_(self, *args, **kwargs):
        return self._item_state

    def _get_item_state_color_(self):
        return self._item_state_color

    def _set_item_state_color_(self, color):
        self._item_state_color = color


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
                lis.append(i_item._get_item_state_())
            return lis
        return []

    def _get_view_item_state_colors_(self, items=None):
        if isinstance(items, (tuple, list)):
            lis = []
            for i_item in items:
                lis.append(i_item._get_item_state_color_())
            return lis
        return []


class AbsShowViewDef(object):
    def _set_show_view_def_init_(self, widget):
        self._widget = widget

    def _get_show_view_item_showable_(self, item):
        rect = self._widget.rect()
        i_rect = self._widget.visualItemRect(item)
        i_w, i_h = i_rect.width(), i_rect.height()
        if i_w != 0 and i_h != 0:
            p_t_, p_b_ = rect.top(), rect.bottom()
            i_p_t, i_p_b = i_rect.top(), i_rect.bottom()
            if i_p_b >= p_t_:
                if i_p_t <= p_b_:
                    return True
        return False

    def _set_show_view_items_update_(self):
        for i_item in self._widget._get_all_items_():
            if i_item.isHidden() is False:
                i_result = self._get_show_view_item_showable_(i_item)
                if i_result is True:
                    i_item._set_item_viewport_visible_(True)


class AbsQtTreeWidget(
    QtWidgets.QTreeWidget,
    AbsQtMenuDef,
    #
    AbsQtViewFilterTgtDef,
    #
    AbsQtViewStateDef,
    AbsQtViewVisibleConnectionDef,
    #
    AbsQtViewScrollActionDef,
    AbsQtBuildViewDef,
    AbsShowViewDef
):
    def __init__(self, *args, **kwargs):
        super(AbsQtTreeWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._set_menu_def_init_()
        #
        self._set_view_filter_tgt_def_init_()
        #
        self._set_view_state_def_init_()
        self._set_view_visible_connection_def_init_()

        self._set_view_scroll_action_def_init_()
        #
        self._get_view_v_scroll_bar_().valueChanged.connect(
            self._set_show_view_items_update_
        )
        #
        self._set_build_view_def_init_()
        self._set_build_view_setup_(self)

        self._set_show_view_def_init_(self)

    def _get_all_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
                lis.append(self.itemFromIndex(index_))
            #
            for row in range(row_count):
                if index_ is None:
                    _index = model.index(row, column)
                else:
                    _index = index_.child(row, index_.column())
                if _index.isValid():
                    _rcs_fnc(_index)
        lis = []
        model = self.model()

        _rcs_fnc(None)
        return lis

    def _set_view_header_(self, raw, max_width):
        texts, widths = zip(*raw)
        count = len(texts)
        max_division = sum(widths)
        w = int(max_width / max_division)
        #
        self.setColumnCount(count)
        self.setHeaderLabels(texts)
        set_column_enable = len(raw) > 1
        for index in range(0, count):
            if set_column_enable is True:
                self.setColumnWidth(index, w*(widths[index]))
            self.headerItem().setBackground(index, Brush.BACKGROUND_NORMAL)
            self.headerItem().setForeground(index, Brush.default_text)
            self.headerItem().setFont(index, Font.NAME)

    def _get_view_h_scroll_bar_(self):
        return self.horizontalScrollBar()

    def _get_view_v_scroll_bar_(self):
        return self.verticalScrollBar()


class AbsQtListWidget(
    QtWidgets.QListWidget,
    #
    AbsQtViewSelectActionDef,
    AbsQtViewScrollActionDef,
    #
    AbsQtViewFilterTgtDef,
    AbsQtViewStateDef,
    AbsQtViewVisibleConnectionDef,
    AbsQtBuildViewDef,
    AbsShowViewDef
):
    item_show_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(AbsQtListWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._set_view_select_action_def_init_()
        self._set_view_scroll_action_def_init_()
        #
        self._set_view_filter_tgt_def_init_()
        #
        self._set_view_state_def_init_()
        self._set_view_visible_connection_def_init_()
        #
        self.itemSelectionChanged.connect(self._set_item_select_update_)
        self.itemSelectionChanged.connect(self._set_item_widget_selected_update_)
        # noinspection PyUnresolvedReferences
        self._get_view_v_scroll_bar_().valueChanged.connect(
            self._set_show_view_items_update_
        )
        self._viewport_rect = QtCore.QRect()
        self._item_rects = []
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QListView')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        #
        self._set_build_view_def_init_()
        self._set_build_view_setup_(self)

        self._set_show_view_def_init_(self)

    def _get_view_h_scroll_bar_(self):
        return self.horizontalScrollBar()

    def _get_view_v_scroll_bar_(self):
        return self.verticalScrollBar()

    def _set_view_item_selected_(self, item, boolean):
        self.setItemSelected(item, boolean)

    def _get_selected_items_(self):
        return self.selectedItems()

    def _set_item_widget_selected_(self, item, boolean):
        self.itemWidget(item)._set_selected_(boolean)
    # select
    def _get_selected_item_widgets_(self):
        return [self.itemWidget(i) for i in self.selectedItems()]

    def _get_selected_item_widget_(self):
        item_widgets = self._get_selected_item_widgets_()
        if item_widgets:
            return item_widgets[-1]

    def _set_item_select_update_(self):
        pass

    def _set_item_widget_selected_update_(self):
        if self._pre_selected_item is not None:
            self._set_item_widget_selected_(self._pre_selected_item, False)
        #
        selected_items = self._get_selected_items_()
        if selected_items:
            item = selected_items[-1]
            self._set_item_widget_selected_(item, True)
            self._pre_selected_item = item
    # scroll
    def _set_scroll_to_item_top_(self, item):
        self.scrollToItem(item, self.PositionAtTop)

    def _set_scroll_to_selected_item_top_(self):
        selected_items = self._get_selected_items_()
        if selected_items:
            item = selected_items[-1]
            self._set_scroll_to_item_top_(item)

    def _get_grid_size_(self):
        s = self.gridSize()
        return s.width(), s.width()

    def _set_wgt_update_draw_(self):
        self.update()
        self.viewport().update()
    #
    def _get_viewport_size_(self):
        return self.viewport().width(), self.viewport().height()

    def _get_all_items_(self):
        return [self.item(i) for i in range(self.count())]

    def _get_visible_items_(self):
        return [i for i in self._get_all_items_() if i.isHidden() is False]

    def _set_loading_update_(self):
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )


class AbsQtItemValueDefaultDef(object):
    def _set_item_value_default_def_init_(self):
        self._item_value_default = None

    def _get_item_value_(self):
        raise NotImplementedError()

    def _set_item_value_default_(self, value):
        self._item_value_default = value

    def _get_item_value_default_(self):
        return self._item_value_default

    def _get_item_value_is_default_(self):
        return self._get_item_value_() == self._get_item_value_default_()


class AbsQtItemValueTypeConstantEntryDef(object):
    QT_VALUE_ENTRY_CLASS = None
    def _set_item_value_type_constant_entry_def_init_(self):
        self._item_value_type = str
        #
        self._item_value_default = None
        #
        self._item_value_entry_widget = None

    def _set_item_value_entry_build_(self, value_type):
        pass

    def _set_item_value_type_(self, value_type):
        self._item_value_type = value_type
        self._item_value_entry_widget._set_item_value_type_(value_type)

    def _set_use_as_frames_(self):
        self._item_value_entry_widget._set_use_as_frames_()

    def _set_use_as_rgba_(self):
        self._item_value_entry_widget._set_use_as_rgba_()

    def _get_item_value_type_(self):
        return self._item_value_type

    def _set_item_value_(self, value):
        self._item_value_entry_widget._set_item_value_(value)

    def _get_item_value_(self):
        return self._item_value_entry_widget._get_item_value_()

    def _set_item_entry_finished_connect_to_(self, fnc):
        self._item_value_entry_widget.entry_finished.connect(fnc)

    def _set_item_entry_changed_connect_to_(self, fnc):
        self._item_value_entry_widget.entry_changed.connect(fnc)

    def _set_item_value_entry_enable_(self, boolean):
        pass


class AbsQtItemValueEnumerateEntryDef(object):
    QT_VALUE_ENTRY_CLASS = None
    def _set_item_value_enumerate_entry_def_init_(self):
        self._item_value_type = str
        #
        self._item_value_default = None
        #
        self._values = []
        #
        self._item_value_entry_widget = None

    def _set_wgt_update_(self):
        raise NotImplementedError()

    def _set_item_value_entry_build_(self, value_type):
        pass

    def _set_item_value_type_(self, value_type):
        self._item_value_type = value_type
        self._item_value_entry_widget._set_item_value_type_(value_type)

    def _get_item_value_type_(self):
        return self._item_value_type

    def _set_item_value_default_(self, value):
        self._item_value_default = value

    def _get_item_value_default_(self):
        return self._item_value_default

    def _set_item_values_(self, values):
        self._values = values
        self._item_value_entry_widget._set_completer_values_(values)
        self._set_wgt_update_()

    def _get_item_values_(self):
        return self._values

    def _set_item_value_append_(self, value):
        self._values.append(value)
        self._set_wgt_update_()

    def _set_item_value_(self, value):
        self._item_value_entry_widget._set_item_value_(value)
        self._set_wgt_update_()

    def _get_item_value_(self):
        return self._item_value_entry_widget._get_item_value_()

    def _set_item_value_clear_(self):
        self._values = []
        self._item_value_entry_widget._set_item_value_clear_()

    def _get_item_value_is_default_(self):
        return self._get_item_value_() == self._get_item_value_default_()


class _QtArrayValueEntryDef(object):
    QT_VALUE_ENTRY_CLASS = None
    def _set_array_value_entry_def_init_(self):
        self._item_value_type = str
        #
        self._item_value_default = ()
        self._value = []
        self._value_entry_widgets = []

    def _set_item_value_entry_build_(self, value_size, value_type):
        pass

    def _set_item_value_type_(self, value_type):
        self._item_value_type = value_type
        for i_value_entry_widget in self._value_entry_widgets:
            i_value_entry_widget._set_item_value_type_(value_type)

    def _get_item_value_type_(self):
        return self._item_value_type

    def _set_value_size_(self, size):
        self._set_item_value_entry_build_(size, self._item_value_type)

    def _get_value_size_(self):
        return len(self._value_entry_widgets)

    def _get_item_value_default_(self):
        return self._item_value_default

    def _set_item_value_(self, value):
        for i, i_value in enumerate(value):
            widget = self._value_entry_widgets[i]
            widget._set_item_value_(i_value)

    def _get_item_value_(self):
        value = []
        for i in self._value_entry_widgets:
            i_value = i._get_item_value_()
            value.append(
                i_value
            )
        return tuple(value)

    def _set_item_value_default_(self, value):
        self._item_value_default = value

    def _get_item_value_is_default_(self):
        return tuple(self._get_item_value_()) == tuple(self._get_item_value_default_())

    def _set_item_entry_changed_connect_to_(self, fnc):
        for i in self._value_entry_widgets:
            i.entry_changed.connect(fnc)


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

    def _set_wgt_update_draw_(self):
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

    def _set_wgt_update_draw_(self):
        self._widget.update()

    def _set_tack_offset_action_start_(self, event):
        self._track_offset_flag = True
        self._track_offset_start_point = event.globalPos()

    def _set_track_offset_action_run_(self, event):
        track_point = event.globalPos() - self._track_offset_start_point
        track_offset_x, track_offset_y = self._tmp_track_offset_x, self._tmp_track_offset_y
        track_d_offset_x, track_d_offset_y = track_point.x(), track_point.y()
        #
        self._track_offset_x = bsc_core.ValueMtd.set_offset_range_to(
            value=track_offset_x,
            d_value=track_d_offset_x,
            radix=self._track_offset_radix_x,
            value_range=(self._track_offset_minimum_x, self._track_offset_maximum_x),
            direction=self._track_offset_direction_x
        )
        #
        self._track_offset_y = bsc_core.ValueMtd.set_offset_range_to(
            value=track_offset_y,
            d_value=track_d_offset_y,
            radix=self._track_offset_radix_y,
            value_range=(self._track_offset_minimum_y, self._track_offset_maximum_y),
            direction=self._track_offset_direction_y
        )
        self._set_wgt_update_draw_()

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

    def _set_wgt_update_draw_(self):
        self._widget.update()

    def _set_zoom_scale_action_run_(self, event):
        delta = event.angleDelta().y()
        self._zoom_scale_x = bsc_core.ValueMtd.step_to(
            value=self._zoom_scale_x,
            delta=delta,
            step=self._zoom_scale_radix_x,
            value_range=(self._zoom_scale_minimum_x, self._zoom_scale_maximum_x),
            direction=1
        )

        self._zoom_scale_y = bsc_core.ValueMtd.step_to(
            value=self._zoom_scale_y,
            delta=delta,
            step=self._zoom_scale_radix_y,
            value_range=(self._zoom_scale_minimum_y, self._zoom_scale_maximum_y),
            direction=1
        )
        #
        self._set_wgt_update_draw_()
