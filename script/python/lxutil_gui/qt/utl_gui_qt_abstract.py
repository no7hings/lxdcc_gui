# coding=utf-8
import os

from lxbasic import bsc_configure

from lxutil import utl_configure

from lxutil_gui.qt.utl_gui_qt_core import *


class _QtFocusDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_widget_focus_update_(self):
        raise NotImplementedError()

    def _set_focus_def_init_(self):
        self._is_focused = False
        self._focus_rect = QtCore.QRect()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        #
        self._set_widget_focus_update_()
        self._set_widget_update_()

    def _get_is_focused_(self):
        return self._is_focused

    def _set_focus_rect_(self, x, y, w, h):
        self._focus_rect.setRect(
            x, y, w, h
        )

    def _get_focus_rect_(self):
        return self._focus_rect


class _QtMenuDef(object):
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
        elif status in [bsc_configure.Status.Completed]:
            r, g, b = 63, 255, 127
            h, s, v = bsc_core.ColorMtd.rgb_to_hsv(r, g, b)
            color = bsc_core.ColorMtd.hsv2rgb(h, s * .75, v * .75)
            hover_color = r, g, b
        else:
            color = Color.TRANSPARENT
            hover_color = Color.TRANSPARENT
        return color, hover_color

    def _set_status_def_init_(self):
        self._is_status_enable = False
        #
        self._status = bsc_configure.Status.Stopped
        #
        self._status_color = Color.TRANSPARENT
        self._hover_status_color = Color.TRANSPARENT
        #
        self._status_rect = QtCore.QRect()

    def _set_widget_update_(self):
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
        self._set_widget_update_()

    def _get_status_(self):
        return self._status

    def _get_is_status_enable_(self):
        return self._is_status_enable


class _QtStatusesDef(object):
    def _set_statuses_def_init_(self):
        self._is_element_status_enable = False
        #
        self._element_statuses = []
        #
        self._element_status_colors = []
        self._hover_element_status_colors = []
        #
        self._element_status_rect = QtCore.QRect()

    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_statuses_(self, element_statuses):
        if element_statuses:
            self._is_element_status_enable = True
            self._element_statuses = element_statuses
            self._element_status_colors = []
            self._hover_element_status_colors = []
            for i_element_status in element_statuses:
                color, hover_color = _QtStatusDef._get_status_color_(i_element_status)
                self._element_status_colors.append(color)
                self._hover_element_status_colors.append(hover_color)
        else:
            self._is_element_status_enable = False
            self._element_statuses = []
            self._element_status_colors = []
            self._hover_element_status_colors = []
        #
        self._set_widget_update_()

    def _get_is_statuses_enable_(self):
        return self._is_element_status_enable


class _QtFrameDef(object):
    def _set_frame_def_init_(self):
        self._frame_border_color = Color.TRANSPARENT
        self._hover_frame_border_color = Color.TRANSPARENT
        #
        self._frame_background_color = Color.TRANSPARENT
        self._hover_frame_background_color = Color.TRANSPARENT
        self._frame_rect = QtCore.QRect()

    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_border_color_(self, color):
        self._frame_border_color = Color._get_qt_color_(color)
        self._set_widget_update_()

    def _set_background_color_(self, color):
        self._frame_background_color = Color._get_qt_color_(color)
        self._set_widget_update_()

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


class _QtIconDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_icon_def_init_(self):
        self._icon_enable = False
        self._file_icon_path = None
        self._color_icon_rgb = None
        self._name_icon_text = None
        #
        self._icon_frame_rect = QtCore.QRect()
        self._file_icon_rect = QtCore.QRect()
        self._color_icon_rect = QtCore.QRect()
        self._name_icon_rect = QtCore.QRect()
        #
        self._icon_frame_size = 20, 20
        self._file_icon_size = 16, 16
        self._color_icon_size = 12, 12
        self._name_icon_size = 14, 14

    def _set_file_icon_path_(self, file_path):
        self._icon_enable = True
        self._file_icon_path = file_path
        self._set_widget_update_()

    def _set_frame_icon_size_(self, w, h):
        self._icon_frame_size = w, h

    def _set_icon_frame_size_(self, w, h):
        self._icon_frame_size = w, h

    def _set_file_icon_size_(self, w, h):
        self._file_icon_size = w, h

    def _get_icon_file_path_(self):
        if self._icon_enable is True:
            return self._file_icon_path

    def _set_color_icon_rgb_(self, rgb):
        self._icon_enable = True
        self._color_icon_rgb = rgb
        self._set_widget_update_()

    def _set_name_icon_text_(self, text):
        self._icon_enable = True
        self._name_icon_text = text
        self._set_widget_update_()

    def _set_name_icon_rect_(self, x, y, w, h):
        self._name_icon_rect.setRect(
            x, y, w, h
        )

    def _get_name_icon_text_(self):
        if self._icon_enable is True:
            return self._name_icon_text

    def _set_frame_icon_rect_(self, x, y, w, h):
        self._icon_frame_rect.setRect(
            x, y, w, h
        )

    def _set_file_icon_rect_(self, x, y, w, h):
        self._file_icon_rect.setRect(
            x, y, w, h
        )

    def _get_file_icon_rect_(self):
        return self._file_icon_rect


class _QtIndexDef(object):
    def _set_index_def_init_(self):
        self._index_enable = False
        self._index = 0
        self._index_text = '1'
        self._index_text_color = Color.INDEX_TEXT
        self._index_text_font = Font.INDEX
        self._index_text_option = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        #
        self._index_frame_rect = QtCore.QRect()
        self._index_rect = QtCore.QRect()

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


class _QtTypeDef(object):
    def _set_type_def_init_(self):
        self._type_text = None
        self._type_rect = QtCore.QRect()

    def _set_type_text_(self, text):
        self._type_text = text

    def _set_type_rect_(self, x, y, w, h):
        self._type_rect.setRect(
            x, y, w, h
        )


class _QtNameDef(object):
    def _set_name_def_init_(self):
        self._name_enable = False
        self._name_text = None
        self._name_text_color = Color.NAME_TEXT
        self._name_text_font = Font.NAME
        self._name_text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        #
        self._name_width = 160
        #
        self._frame_name_rect = QtCore.QRect()
        self._name_rect = QtCore.QRect()
        #
        self._name_color = 223, 223, 223
        self._hover_name_color = 255, 255, 255

    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_name_text_(self, name_text):
        self._name_enable = True
        self._name_text = name_text
        # noinspection PyUnresolvedReferences
        self._set_widget_update_()

    def _get_name_text_option_(self):
        return self._name_text_option

    def _set_name_width_(self, w):
        self._name_width = w

    def _get_name_text_(self):
        if self._name_enable is True:
            return self._name_text

    def _set_frame_name_rect_(self, x, y, w, h):
        self._frame_name_rect.setRect(
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
                    html += '<ul>\n<li>{}</li>\n</ul>\n'.format(i)
                html += '</body>\n</html>'
                # noinspection PyCallingNonCallable
                self.setToolTip(html)


class _QtPathDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_path_def_init_(self):
        self._path_text = None
        self._path_rect = QtCore.QRect()

    def _set_path_text_(self, text):
        self._path_text = text
        self._set_widget_update_()

    def _get_path_text_(self):
        return self._path_text

    def _set_path_rect_(self, x, y, w, h):
        self._path_rect.setRect(x, y, w, h)


class _QtProgressDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_widget_geometry_update_(self):
        pass

    def _set_progress_def_init_(self):
        self._progress_height = 2
        #
        self._progress_maximum_value = 100
        self._progress_value = 0
        #
        self._progress_sub_maximum_value = 100
        self._progress_sub_value = 0
        #
        self._progress_rect = QtCore.QRect()
        #
        self._progress_raw = []

    def _set_progress_height_(self, value):
        self._progress_height = value

    def _set_progress_run_(self):
        self._set_widget_geometry_update_()
        self._set_widget_update_()
        #
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_progress_maximum_value_(self, value):
        self._progress_maximum_value = value

    def _set_progress_value_(self, value):
        self._progress_value = value
        sub_value = int(
            (float(value)/float(self._progress_maximum_value))*self._progress_sub_maximum_value
        )
        if sub_value != self._progress_sub_value:
            self._progress_sub_value = sub_value
            self._set_progress_run_()

    def _set_progress_update_(self):
        self._set_progress_value_(self._progress_value+1)

    def _set_progress_stop_(self):
        self._set_progress_value_(0)
        self._progress_raw = []

    def _get_progress_percent_(self):
        return float(self._progress_sub_value) / float(self._progress_sub_maximum_value)

    def _set_progress_raw_(self, raw):
        self._progress_raw = raw

    def _get_is_progress_enable_(self):
        return self._progress_sub_value != 0


class _QtImageDef(object):
    def _set_image_def_init_(self):
        self._image_enable = False
        self._image_file_path = None
        self._image_size = 32, 32
        self._image_rect = QtCore.QRect(0, 0, 0, 0)

    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_image_file_path_(self, file_path):
        self._image_enable = True
        self._image_file_path = file_path
        self._set_widget_update_()

    def _set_image_size_(self, size):
        self._image_size = size

    def _get_image_size_(self):
        if self._image_file_path is not None:
            if os.path.isfile(self._image_file_path):
                ext = os.path.splitext(self._image_file_path)[-1]
                if ext in ['.jpg', '.png']:
                    s = QtGui.QImage(self._image_file_path).size()
                    return s.width(), s.height()
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


class _QtNamesDef(object):
    def _set_names_def_init_(self):
        self._names_enable = False
        self._name_texts = []
        self._name_rects = []
        #
        self._name_frame_border_color = 0, 0, 0, 0
        self._name_frame_background_color = 95, 95, 95, 127

    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_name_text_at_(self, name_text, index=0):
        self._name_texts[index] = name_text

    def _get_name_text_at_(self, index=0):
        if index in self._get_name_indices_():
            return self._name_texts[index]

    def _set_name_rect_at_(self, x, y, w, h, index=0):
        self._name_rects[index].setRect(
            x, y, w, h
        )

    def _set_name_texts_(self, name_texts):
        self._name_texts = name_texts
        self._name_rects = []
        for _ in self._get_name_indices_():
            self._name_rects.append(
                QtCore.QRect()
            )
        #
        self._set_widget_update_()

    def _get_name_texts_(self):
        return self._name_texts

    def _set_name_frame_border_color_(self, color):
        self._name_frame_border_color = color

    def _get_name_frame_border_color_(self):
        return self._name_frame_border_color

    def _set_name_frame_background_color_(self, color):
        self._name_frame_background_color = color

    def _get_name_frame_background_color_(self):
        return self._name_frame_background_color

    def _get_name_rect_at_(self, index=0):
        return self._name_rects[index]

    def _get_name_indices_(self):
        return range(len(self._name_texts))


class _QtIconsDef(object):
    def _set_icons_def_init_(self):
        self._icons_enable = False
        self._pixmap_icons = []
        self._icon_file_paths = []
        self._icon_name_texts = []
        self._icon_indices = []
        self._icon_rects = []

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

    def _set_pixmap_icons_(self, icons):
        self._pixmap_icons = icons
        self._icon_indices = range(len(icons))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _get_pixmap_icon_at_(self, index):
        if index in self._get_icon_indices_():
            return self._pixmap_icons[index]

    def _get_pixmap_icons_(self):
        return self._pixmap_icons

    def _set_icon_file_paths_(self, file_paths):
        self._icon_file_paths = file_paths
        self._icon_indices = range(len(self._icon_file_paths))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _set_icon_name_texts_(self, name_texts):
        self._icon_name_texts = name_texts
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


# item
class _QtItemDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_item_def_init_(self):
        self._item_is_enable = True
        self._item_is_hovered = False

    def _set_item_enable_(self, boolean):
        self._item_is_enable = boolean

    def _get_item_is_enable_(self):
        return self._item_is_enable

    def _set_item_hovered_(self, boolean):
        self._item_is_hovered = boolean
        self._set_widget_update_()

    def _get_item_is_hovered_(self):
        return self._item_is_hovered

    def _set_item_event_filter_(self, event):
        if event.type() == QtCore.QEvent.Enter:
            self._set_item_hovered_(True)
        elif event.type() == QtCore.QEvent.Leave:
            self._set_item_hovered_(False)


class _QtItemActionDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_item_action_def_init_(self):
        self._action_flag = None

    def _set_item_action_flag_(self, flag):
        self._action_flag = flag
        self._set_widget_update_()

    def _get_item_action_flag_(self):
        return self._action_flag

    def _set_item_action_flag_clear_(self):
        self._action_flag = None
        self._set_widget_update_()

    def _get_item_action_flag_is_match_(self, flag):
        return self._action_flag == flag

    def _get_item_action_offset_(self):
        if self._action_flag is not None:
            return 2
        return 0


class _QtItemPressActionDef(object):
    press_clicked = qt_signal()
    press_toggled = qt_signal(bool)
    #
    clicked = qt_signal()
    db_clicked = qt_signal()
    #
    PRESS_CLICK_FLAG = gui_configure.ActionFlag.PRESS_CLICK
    PRESS_MOVE_FLAG = gui_configure.ActionFlag.PRESS_MOVE
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _get_item_is_enable_(self):
        raise NotImplementedError()
    #
    def _set_item_press_action_def_init_(self):
        self._item_is_press_enable = True
        self._item_is_pressed = False
        #
        self._item_press_rect = QtCore.QRect()

    def _get_item_action_flag_(self):
        raise NotImplementedError()

    def _get_item_action_flag_is_match_(self, flag):
        raise NotImplementedError()

    def _get_item_is_press_enable_(self):
        if self._get_item_is_enable_() is True:
            return self._item_is_press_enable
        return False

    def _set_item_click_emit_send_(self):
        self.clicked.emit()

    def _get_item_is_click_flag_(self):
        return self._get_item_action_flag_is_match_(self.PRESS_CLICK_FLAG)


class _QtItemCheckActionDef(object):
    check_clicked = qt_signal()
    check_toggled = qt_signal(bool)
    #
    CHECK_CLICK_FLAG = gui_configure.ActionFlag.CHECK_CLICK
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _get_item_is_enable_(self):
        raise NotImplementedError()

    def _set_item_check_action_def_init_(self):
        self._is_check_enable = False
        #
        self._item_check_icon_file_path = None
        self._item_check_icon_file_path_0 = utl_core.Icon.get('box_unchecked')
        self._item_check_icon_file_path_1 = utl_core.Icon.get('box_checked')
        #
        self._item_is_checked = False
        self._item_check_frame_rect = QtCore.QRect()
        self._item_check_icon_rect = QtCore.QRect()

    def _set_item_checked_enable_(self, boolean):
        self._is_check_enable = boolean

    def _get_item_is_check_enable_(self):
        if self._get_item_is_enable_() is True:
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
        self._set_widget_update_()

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


class _QtItemExpandActionDef(object):
    expand_clicked = qt_signal()
    expand_toggled = qt_signal(bool)
    #
    EXPAND_CLICKED_FLAG = gui_configure.ActionFlag.EXPAND_CLICK
    #
    EXPAND_TOP_TO_BOTTOM = 0
    EXPAND_BOTTOM_TO_TOP = 1
    def _set_widget_update_(self):
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
    #
    OPTION_CLICK_FLAG = gui_configure.ActionFlag.OPTION_CLICK
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _get_item_is_enable_(self):
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
        if self._get_item_is_enable_() is True:
            return self._option_click_enable
        return False


class _QtItemChooseActionDef(object):
    def _set_item_choose_def_init_(self):
        self._choose_expand_icon_file_path = utl_core.Icon.get('choose_expand')
        self._choose_collapse_icon_file_path = utl_core.Icon.get('choose_collapse')
        #
        self._path_text = None
        #
        self._rect = QtCore.QRect()
        #
        self._is_dropped = False
        #
        self._content_raw = None
        self._choose_name_texts = []
        self._choose_path_texts = []

    def _get_is_choose_dropped_(self):
        return self._is_dropped

    def _set_choose_dropped_(self, boolean):
        self._is_dropped = boolean

    def _set_dropped_update_(self):
        pass

    def _get_icon_file_path_(self):
        return [
            self._choose_collapse_icon_file_path,
            self._choose_expand_icon_file_path
        ][self._get_is_choose_dropped_()]

    def _set_choose_content_raw_(self, raw):
        self._content_raw = raw
        if isinstance(raw, (tuple, list)):
            self._choose_name_texts = list(raw)

    def _set_choose_content_name_texts_(self, contents):
        self._choose_name_texts = contents

    def _get_choose_content_name_texts_(self):
        return self._choose_name_texts


class _QtViewChooseActionDef(object):
    CHOOSE_RECT_CLS = None
    CHOOSE_DROP_WIDGET_CLS = None
    #
    choose_item_changed = qt_signal()
    choose_item_clicked = qt_signal()
    choose_item_double_clicked = qt_signal()
    #
    CHOOSE_FLAG = gui_configure.ActionFlag.CHOOSE
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_view_choose_action_def_init_(self):
        self._choose_items = []
        self._view_choose_current_index = None

    def _get_item_action_flag_(self):
        raise NotImplementedError()

    def _get_item_action_flag_is_match_(self, flag):
        raise NotImplementedError()

    def _get_choose_items_(self):
        return self._choose_items

    def _get_choose_item_indices_(self):
        return range(len(self._get_choose_items_()))

    def _get_choose_item_at_(self, index=0):
        return self._get_choose_items_()[index]

    def _get_choose_pos_at_(self, index=0):
        raise NotImplementedError()

    def _get_choose_size_at_(self, index=0):
        raise NotImplementedError()

    def _set_choose_item_current_at_(self, text, index=0):
        self._get_choose_item_at_(index)._set_name_text_(text)

    def _get_choose_item_current_at_(self, index=0):
        return self._get_choose_item_at_(index)._name_text
    #
    def _set_choose_item_content_at_(self, raw, index=0):
        self._get_choose_item_at_(index)._set_choose_content_raw_(raw)
    #
    def _set_choose_item_content_name_texts_at_(self, texts, index=0):
        self._get_choose_item_at_(index)._set_choose_content_name_texts_(texts)
    #
    def _get_choose_item_content_name_texts_at_(self, index=0):
        return self._get_choose_item_at_(index)._get_choose_content_name_texts_()

    def _set_choose_item_drop_at_(self, index=0):
        widget = self.CHOOSE_DROP_WIDGET_CLS(self)
        widget._set_drop_start_at_(
            index
        )

    def _set_choose_item_expanded_at_(self, boolean, index=0):
        item = self._get_choose_item_at_(index)
        item._set_choose_dropped_(boolean)

    def _get_choose_item_is_expanded_at_(self, index=0):
        item = self._get_choose_item_at_(index)
        return item._get_is_choose_dropped_()

    def _set_choose_item_expand_at_(self, index=0):
        self._set_choose_item_expanded_at_(True, index)

    def _set_choose_item_collapse_at_(self, index=0):
        self._set_choose_item_expanded_at_(False, index)

    def _get_is_choose_flag_(self):
        return self._get_item_action_flag_is_match_(self.CHOOSE_FLAG)

    def _set_choose_clear_(self):
        self._view_choose_current_index = None
        #
        self._choose_items = []

    def _set_choose_item_create_(self):
        item = self.CHOOSE_RECT_CLS()
        self._choose_items.append(item)
        return item

    def _set_choose_item_clicked_emit_send_(self):
        self.choose_item_clicked.emit()

    def _set_choose_item_double_clicked_emit_send_(self):
        self.choose_item_double_clicked.emit()

    def _set_choose_item_changed_emit_send_(self):
        self.choose_item_changed.emit()

    def _set_choose_current_(self, index):
        self._view_choose_current_index = index

    def _set_choose_current_clear_(self):
        self._view_choose_current_index = None


class _QtViewGuideActionDef(object):
    guide_item_clicked = qt_signal()
    guide_item_double_clicked = qt_signal()
    def _set_view_guide_action_def_init_(self):
        self._guide_items = []
        self._view_guide_current_index = None

    def _get_guide_items_(self):
        return self._guide_items

    def _get_guide_item_indices_(self):
        return range(len(self._get_guide_items_()))

    def _get_guide_item_at_(self, index=0):
        return self._get_guide_items_()[index]

    def _set_guide_clear_(self):
        self._guide_items = []
        self._view_guide_current_index = None

    def _set_guide_current_(self, index):
        self._view_guide_current_index = index

    def _set_guide_current_clear_(self):
        self._view_guide_current_index = None

    def _set_guide_item_name_text_at_(self, text, index=0):
        self._get_guide_item_at_(index)._set_name_text_(text)

    def _get_guide_item_name_text_at_(self, index=0):
        return self._get_guide_item_at_(index)._name_text

    def _get_guide_item_path_text_at_(self, index=0):
        return self._get_guide_item_at_(index)._path_text
    #
    def _set_guide_item_path_text_at_(self, text, index=0):
        self._get_guide_item_at_(index)._set_path_text_(text)
    #
    def _get_guide_current_path_(self):
        if self._view_guide_current_index is not None:
            return self._get_guide_item_path_text_at_(
                self._view_guide_current_index
            )

    def _set_guide_current_path_(self, path_text):
        pass
    # emit
    def _set_guide_item_clicked_emit_send_(self):
        self.guide_item_clicked.emit()

    def _set_guide_item_double_clicked_emit_send_(self):
        self.guide_item_double_clicked.emit()


class _QtItemSelectActionDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()
    #
    def _set_item_select_action_def_init_(self):
        self._is_selected = False

    def _get_item_action_flag_(self):
        raise NotImplementedError()

    def _set_selected_(self, boolean):
        self._is_selected = boolean
        #
        self._set_widget_update_()

    def _get_is_selected_(self):
        return self._is_selected


class _QtItemShowDef(object):
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _get_view_(self):
        raise NotImplementedError()

    def _get_item_widget_(self):
        raise NotImplementedError()

    def _set_item_show_def_init_(self, view):
        self._item_show_timer = QtCore.QTimer(view)
        self._item_show_thread = QtThread(view)
        #
        self._item_show_loading_index = 0
        #
        self._item_show_loading_timer = QtCore.QTimer(view)
        self._item_show_loading_is_enable = False
        self._item_show_loading_is_finish = True
        #
        self._item_show_image_loading_timer = QtCore.QTimer(view)
        self._item_show_image_loading_is_enable = False
        self._item_show_image_loading_is_finish = True
        #
        self._item_show_image_sub_process = None

    def _set_item_show_sub_process_(self, sub_process):
        self._item_show_image_sub_process = sub_process

    def _get_item_show_sub_process_(self):
        return self._item_show_image_sub_process

    def _get_item_is_viewport_show_able_(self):
        raise NotImplementedError()

    def _set_item_show_loading_start_(self):
        self._item_show_loading_is_enable = True
        self._item_show_loading_is_finish = False
        #
        self._item_show_loading_timer.timeout.connect(
            self._set_item_show_loading_update_
        )
        self._item_show_loading_timer.start(1000)

    def _set_item_show_loading_update_(self):
        self._item_show_loading_index += 1
        self._set_widget_update_()

    def _set_item_show_loading_stop_(self):
        self._item_show_loading_is_enable = False
        self._item_show_loading_is_finish = True

        self._item_show_loading_timer.stop()

    def _get_item_show_image_loading_is_termination_(self):
        sub_process = self._get_item_show_sub_process_()
        if sub_process is not None:
            return sub_process.get_is_termination()
        return True

    def _get_item_show_image_loading_is_abnormal_termination_(self):
        sub_process = self._get_item_show_sub_process_()
        if sub_process is not None:
            return sub_process.get_is_abnormal_termination()
        return False

    def _set_item_show_image_loading_start_(self):
        if self._get_item_show_image_loading_is_termination_() is False:
            self._item_show_image_loading_is_enable = True
            self._item_show_image_loading_is_finish = False
            #
            self._item_show_image_loading_timer.timeout.connect(
                self._set_item_show_image_loading_update_
            )
            self._item_show_image_loading_timer.start(1000)

    def _set_item_show_image_loading_update_(self):
        self._set_item_show_image_sub_process_update_()
        #
        if self._get_item_show_image_loading_is_termination_() is True:
            self._set_item_show_image_loading_stop_()
        else:
            self._item_show_loading_index += 1
        #
        self._set_widget_update_()

    def _set_item_show_image_sub_process_update_(self):
        sub_process = self._get_item_show_sub_process_()
        if sub_process is not None:
            sub_process.set_update()

    def _set_item_show_image_loading_stop_(self):
        self._item_show_image_loading_is_enable = False
        self._item_show_image_loading_is_finish = True
        #
        if self._get_item_show_image_loading_is_abnormal_termination_() is True:
            item_widget = self._get_item_widget_()
            if item_widget is not None:
                item_widget._set_image_file_path_(
                    utl_core.Icon._get_file_path_('@image_loading_failed_error@')
                )
        #
        self._item_show_image_loading_timer.stop()

    def _set_item_show_method_(self, method):
        self._item_show_thread.started.connect(method)
        self._set_item_show_loading_start_()
        if self._get_item_is_viewport_show_able_() is True:
            self._set_item_show_start_()

    def _set_item_show_update_(self):
        if self._get_item_is_viewport_show_able_() is True:
            self._set_item_show_start_()

    def _set_item_show_start_(self, time=100):
        def start_fnc_():
            self._item_show_thread.start()
            self._item_show_timer.stop()
            self._set_item_show_loading_stop_()
        #
        self._item_show_timer.timeout.connect(start_fnc_)
        self._item_show_timer.start(time)

    def _set_item_show_stop_(self):
        self._set_item_show_loading_stop_()
        self._set_item_show_image_loading_stop_()

    def _set_item_viewport_visible_(self, boolean):
        if boolean is True:
            if self._item_show_loading_is_finish is False:
                self._set_item_show_start_()
        #
        self._set_item_widget_visible_(boolean)

    def _set_item_widget_visible_(self, boolean):
        raise NotImplementedError()

    def _set_viewport_show_enable_(self, boolean):
        self._is_viewport_show_enable = boolean


class _QtEntryActionDef(object):
    entry_changed = qt_signal()
    def _set_widget_update_(self):
        raise NotImplementedError()

    def _get_item_action_flag_(self):
        raise NotImplementedError()
    #
    def _set_entry_action_def_init_(self):
        self._is_entered = False
        self._entry_frame_rect = QtCore.QRect()
        self._entry_rect = QtCore.QRect()

    def _set_entered_(self, boolean):
        self._is_entered = boolean
        self._set_widget_update_()

    def _set_entry_frame_rect_(self, x, y, w, h):
        self._entry_frame_rect.setRect(
            x, y, w, h
        )

    def _get_entry_frame_rect_(self):
        return self._entry_frame_rect


class _QtViewSelectActionDef(object):
    def _set_view_select_action_def_init_(self):
        self._pre_selected_item = None

    def _set_item_selected_(self, item, boolean):
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


class _QtViewScrollActionDef(object):
    def _set_view_scroll_action_def_init_(self):
        pass

    def _get_h_scroll_bar_(self):
        raise NotImplementedError()

    def _get_v_scroll_bar_(self):
        raise NotImplementedError()

    def _get_v_scroll_value_(self):
        return self._get_v_scroll_bar_().value()

    def _get_v_minimum_scroll_value_(self):
        return self._get_v_scroll_bar_().minimum()

    def _get_v_maximum_scroll_value_(self):
        return self._get_v_scroll_bar_().maximum()

    def _set_items_show_update_(self):
        pass

    def _get_v_scroll_percent_(self):
        v = self._get_v_scroll_value_()
        v_min, v_max = self._get_v_minimum_scroll_value_(), self._get_v_maximum_scroll_value_()
        if v_max > 0:
            return float(v)/float(v_max)
        return 0


class _QtChartDef(object):
    def _set_widget_update_(self):
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
        self._set_chart_data_update_()
        self._set_chart_data_post_run_()
        self._set_widget_update_()

    def _set_chart_data_post_run_(self):
        pass

    def _set_chart_data_update_(self):
        raise NotImplementedError()

    def _set_height_(self, h):
        # noinspection PyUnresolvedReferences
        self.setMaximumHeight(h)
        # noinspection PyUnresolvedReferences
        self.setMinimumHeight(h)


class _QtAbsListWidget(
    QtWidgets.QListWidget,
    _QtViewSelectActionDef,
    _QtViewScrollActionDef,
):
    item_show_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtAbsListWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._set_view_select_action_def_init_()
        self._set_view_scroll_action_def_init_()
        #
        self.itemSelectionChanged.connect(self._set_item_select_update_)
        self.itemSelectionChanged.connect(self._set_item_widget_selected_update_)
        # noinspection PyUnresolvedReferences
        self._get_v_scroll_bar_().valueChanged.connect(self._set_items_show_update_)
        self._viewport_rect = QtCore.QRect()
        self._item_rects = []

    def _get_h_scroll_bar_(self):
        return self.horizontalScrollBar()

    def _get_v_scroll_bar_(self):
        return self.verticalScrollBar()

    def _set_item_selected_(self, item, boolean):
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

    def _set_widget_update_(self):
        self.update()
        self.viewport().update()

    def _set_items_show_update_(self):
        rect = self.rect()
        self._item_rects = []
        p_t_, p_b_ = rect.top(), rect.bottom()
        for i in self._get_items_():
            if i.isHidden() is False:
                i._set_item_viewport_visible_(False)
                i_rect = self.visualItemRect(i)
                i_p_t, i_p_b = i_rect.top(), i_rect.bottom()
                if i_p_b >= p_t_:
                    if i_p_t <= p_b_:
                        self._item_rects.append(i_rect)
                        i._set_item_viewport_visible_(True)

    def _get_item_is_viewport_show_able_at_(self, item):
        rect = self.rect()
        p_t_, p_b_ = rect.top(), rect.bottom()
        i_rect = self.visualItemRect(item)
        i_p_t, i_p_b = i_rect.top(), i_rect.bottom()
        if i_p_b >= p_t_:
            if i_p_t <= p_b_:
                return True
        return False
    #
    def _get_viewport_size_(self):
        return self.viewport().width(), self.viewport().height()

    def _get_items_(self):
        return [self.item(i) for i in range(self.count())]

    def _get_visible_items_(self):
        return [i for i in self._get_items_() if i.isHidden() is False]

    def _set_loading_update_(self):
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )


class _QtConstantValueEntryDef(object):
    QT_VALUE_ENTRY_CLASS = None
    def _set_constant_value_entry_def_init_(self):
        self._value_type = str
        #
        self._default_value = None
        #
        self._value_entry_widget = None

    def _set_value_entry_build_(self, value_type):
        pass

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        self._value_entry_widget._set_value_type_(value_type)

    def _get_value_type_(self):
        return self._value_type

    def _set_default_value(self, value):
        self._default_value = value

    def _get_default_value_(self):
        return self._default_value

    def _set_value_(self, value):
        self._value_entry_widget._set_value_(value)

    def _get_value_(self):
        return self._value_entry_widget._get_value_()


class _QtEnumerateValueEntryDef(object):
    QT_VALUE_ENTRY_CLASS = None
    def _set_enumerate_value_entry_def_init_(self):
        self._value_type = str
        #
        self._default_value = None
        #
        self._values = []
        #
        self._value_entry_widget = None

    def _set_value_entry_build_(self, value_type):
        pass

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        self._value_entry_widget._set_value_type_(value_type)

    def _get_value_type_(self):
        return self._value_type

    def _set_default_value(self, value):
        self._default_value = value

    def _get_default_value_(self):
        return self._default_value

    def _set_values_(self, values):
        self._values = values
        self._value_entry_widget._set_completer_values_(values)

    def _get_values_(self):
        return self._values

    def _set_value_(self, value):
        self._value_entry_widget._set_value_(value)

    def _get_value_(self):
        return self._value_entry_widget._get_value_()

    def _set_value_clear_(self):
        self._values = []
        self._value_entry_widget._set_value_clear_()


class _QtArrayValueEntryDef(object):
    QT_VALUE_ENTRY_CLASS = None
    def _set_array_value_entry_def_init_(self):
        self._value_type = str
        #
        self._default_value = []
        self._value = []
        self._value_entry_widgets = []

    def _set_value_entry_build_(self, value_size, value_type):
        pass

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        for i_value_entry_widget in self._value_entry_widgets:
            i_value_entry_widget._set_value_type_(value_type)

    def _get_value_type_(self):
        return self._value_type

    def _set_value_size_(self, size):
        self._set_value_entry_build_(size, self._value_type)

    def _get_value_size_(self):
        return len(self._value_entry_widgets)

    def _get_default_value_(self):
        return self._default_value

    def _set_value_(self, value):
        for i, i_value in enumerate(value):
            widget = self._value_entry_widgets[i]
            widget._set_value_(i_value)

    def _get_value_(self):
        value = []
        for i in self._value_entry_widgets:
            i_value = i._get_value_()
            value.append(
                i_value
            )
        return tuple(value)
