# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui.qt import utl_gui_qt_core


class _QtListItemWidget(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIndexDef,
    utl_gui_qt_abstract.AbsQtImageDef,
    utl_gui_qt_abstract.AbsQtMovieDef,
    #
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtIconsDef,
    utl_gui_qt_abstract.AbsQtNamesDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionCheckDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtActionSelectDef,
    #
    utl_gui_qt_abstract.AbsQtStateDef,
    #
    utl_gui_qt_abstract.AbsQtItemMovieActionDef,
):
    viewport_show = qt_signal()
    viewport_hide = qt_signal()
    #
    QT_MENU_CLASS = _utl_gui_qt_wgt_utility.QtMenu

    def _refresh_widget_draw_(self):
        # noinspection PyUnresolvedReferences
        self.update()

    def _execute_action_hover_(self, event):
        p = event.pos()
        self._check_is_hovered = False
        self._press_is_hovered = False
        if self._check_action_is_enable is True:
            if self._check_action_rect.contains(p):
                self._check_is_hovered = True
            else:
                self._press_is_hovered = True
        else:
            self._press_is_hovered = True
        #
        self._refresh_widget_draw_()

    def _get_check_action_is_available_(self, event):
        if self._check_action_is_enable is True:
            p = event.pos()
            return self._check_action_rect.contains(p)
        return False

    def __init__(self, *args, **kwargs):
        super(_QtListItemWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self._set_frame_def_init_()
        self._set_index_def_init_()
        self._set_icon_def_init_()
        self._set_icons_def_init_()
        self._set_image_def_init_()
        self._set_names_def_init_()
        self._set_menu_def_init_()
        self._set_movie_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_check_def_init_()
        self._check_icon_file_path_0 = utl_gui_core.RscIconFile.get('filter_unchecked')
        self._check_icon_file_path_1 = utl_gui_core.RscIconFile.get('filter_checked')
        self._set_action_press_def_init_()
        self._set_action_select_def_init_()
        #
        self._set_item_movie_action_def_init_()
        #
        self._set_state_def_init_()
        #
        self._file_type_icon = None
        #
        self._list_widget = None
        self._list_widget_item = None
        #
        self._frame_icon_width, self._frame_icon_height = 40, 128
        self._frame_image_width, self._frame_image_height = 128, 128
        self._frame_name_width, self._frame_name_height = 128, 40
        #
        self._frame_side = 4
        self._frame_spacing = 2
        #
        self._frame_size = 128, 128
        #
        self._frame_background_color = QtBackgroundColors.Light
        #
        self._is_viewport_show_enable = True
        #
        self.setFont(get_font())

        self._signals = QtItemSignals()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_action_hovered_(True)
            elif event.type() == QtCore.QEvent.Leave:
                self._set_action_hovered_(False)
            #
            elif event.type() == QtCore.QEvent.Resize:
                self.update()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.button() == QtCore.Qt.NoButton:
                    self._execute_action_hover_(event)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                elif event.button() == QtCore.Qt.LeftButton:
                    if self._get_check_action_is_available_(event) is True:
                        self._set_action_check_execute_(event)
                        self.check_clicked.emit()
                        self.check_toggled.emit(self._is_checked)
                        self.user_check_toggled.emit(self._is_checked)
                        self._set_action_flag_(self.ActionFlag.CheckClick)
                    else:
                        self.press_clicked.emit()
                        self._set_pressed_(True)
                        self._set_action_flag_(self.ActionFlag.PressClick)
            #
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_check_action_is_available_(event) is True:
                        self._set_action_check_execute_(event)
                        self.check_clicked.emit()
                        self.check_toggled.emit(self._is_checked)
                        self.user_check_toggled.emit(self._is_checked)
                        self._set_action_flag_(self.ActionFlag.CheckDbClick)
                    else:
                        self.press_clicked.emit()
                        self._set_pressed_(True)
                        self._set_action_flag_(self.ActionFlag.PressDbClick)
            #
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if self._get_action_flag_is_match_(self.ActionFlag.PressClick):
                    self._send_action_press_click_emit_()
                elif self._get_action_flag_is_match_(self.ActionFlag.PressDbClick):
                    self._set_action_press_db_click_emit_send_()
                #
                self._set_pressed_(False)
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        w, h = self.width(), self.height()
        #
        offset = self._get_action_offset_()
        #
        bkg_rect = QtCore.QRect(1, 1, w-2, h-2)
        bkg_color = painter._get_item_background_color_by_rect__(
            rect=bkg_rect,
            is_check_hovered=self._check_is_hovered,
            is_checked=self._is_checked,
            is_press_hovered=self._press_is_hovered,
            is_pressed=self._is_pressed,
            is_selected=self._is_selected
        )
        background_color = painter._get_item_background_color_by_rect_(
            bkg_rect,
            is_hovered=self._action_is_hovered,
            is_selected=self._is_selected,
            is_actioned=self._get_is_actioned_()
        )
        #
        item = self._get_item_()
        if item._item_show_status in [item.ShowStatus.Loading, item.ShowStatus.Waiting]:
            painter._set_loading_draw_by_rect_(
                self._frame_draw_rect,
                item._item_show_loading_index
            )
        else:
            painter._draw_frame_by_rect_(
                bkg_rect,
                border_color=QtBackgroundColors.Transparent,
                background_color=bkg_color,
                border_radius=1,
                offset=offset
            )
            # icon frame
            if self._icon_frame_draw_enable is True:
                if self._get_has_icons_() or self._check_is_enable is True:
                    painter._draw_frame_by_rect_(
                        self._icon_frame_draw_rect,
                        border_color=self._frame_background_color,
                        background_color=self._frame_background_color,
                        offset=offset
                    )
            #
            if self._name_frame_draw_enable is True:
                if self._get_has_names_():
                    painter._draw_frame_by_rect_(
                        self._name_frame_rect,
                        border_color=self._get_name_frame_border_color_(),
                        background_color=self._get_name_frame_background_color_(),
                        offset=offset
                    )
            #
            if self._image_frame_draw_enable is True:
                if self._get_has_image_():
                    painter._draw_frame_by_rect_(
                        self._image_frame_rect,
                        border_color=self._frame_background_color,
                        background_color=self._frame_background_color,
                        offset=offset
                    )
            # check icon
            if self._check_is_enable is True:
                painter._set_icon_file_draw_by_rect_(
                    rect=self._check_icon_draw_rect,
                    file_path=self._check_icon_file_path_current,
                    offset=offset,
                    frame_rect=self._check_icon_frame_draw_rect,
                    is_hovered=self._check_is_hovered
                )
            # icons
            if self._get_has_icons_() is True:
                icon_indices = self._get_icon_indices_()
                if icon_indices:
                    icon_pixmaps = self._get_icons_as_pixmap_()
                    if icon_pixmaps:
                        for icon_index in icon_indices:
                            painter._set_pixmap_draw_by_rect_(
                                self._get_icon_rect_at_(icon_index),
                                self._get_icon_as_pixmap_at_(icon_index),
                                offset=offset
                            )
                    else:
                        icon_file_paths = self._get_icon_file_paths_()
                        if icon_file_paths:
                            for icon_index in icon_indices:
                                painter._set_icon_file_draw_by_rect_(
                                    self._get_icon_rect_at_(icon_index),
                                    self._get_icon_file_path_at_(icon_index),
                                    offset=offset
                                )
            # icon
            if self._icon_is_enable is True:
                if self._icon_name_text:
                    painter._set_icon_name_text_draw_by_rect_(
                        self._icon_name_draw_rect,
                        self._icon_name_text,
                        offset=offset,
                        border_radius=2,
                        border_color=QtBorderColors.Transparent,
                        background_color=QtBackgroundColors.Transparent,
                        font_color=self._frame_background_color
                    )
            # name
            if self._get_has_names_() is True:
                name_indices = self._get_name_indices_()
                if name_indices:
                    text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
                    #
                    name_text_dict = self._get_name_text_dict_()
                    if name_text_dict:
                        painter.setFont(get_font())
                        key_text_width = utl_gui_qt_core.QtTextMtd.get_draw_width_maximum(
                            painter, self._name_text_dict.keys()
                        )
                        for i_name_index, (i_key, i_value) in enumerate(name_text_dict.items()):
                            painter._set_text_draw_by_rect_use_key_value_(
                                self._get_name_rect_at_(i_name_index),
                                key_text=i_key,
                                value_text=i_value,
                                key_text_width=key_text_width,
                                offset=offset,
                                is_hovered=self._action_is_hovered,
                                is_selected=self._is_selected
                            )
                    else:
                        for i_name_index in name_indices:
                            painter._draw_text_by_rect_(
                                rect=self._get_name_rect_at_(i_name_index),
                                text=self._get_name_text_at_(i_name_index),
                                font=get_font(),
                                text_option=text_option,
                                word_warp=self._name_word_warp,
                                offset=offset,
                                is_hovered=self._action_is_hovered,
                                is_selected=self._is_selected
                            )
            # image
            if self._get_has_image_() is True:
                image_file_path = self._image_file_path
                # draw by image file
                if image_file_path:
                    painter._set_any_image_draw_by_rect_(
                        self._get_image_rect_(),
                        image_file_path,
                        offset=offset
                    )
                else:
                    image_name_text = self._image_name_text
                    # draw by text
                    if image_name_text:
                        painter._set_icon_name_text_draw_by_rect_(
                            self._get_image_rect_(),
                            image_name_text,
                            border_radius=4,
                            offset=offset
                        )
            #
            if self._get_movie_enable_():
                painter._set_movie_play_button_draw_by_rect_(
                    self._movie_rect,
                    offset=offset,
                    is_hovered=self._action_is_hovered,
                    is_selected=self._is_selected,
                    is_actioned=self._get_is_actioned_()
                )
            #
            if item._item_show_image_status in [item.ShowStatus.Loading, item.ShowStatus.Waiting]:
                painter._set_loading_draw_by_rect_(
                    self._image_frame_rect,
                    item._item_show_image_loading_index
                )

    def _set_action_hovered_(self, boolean):
        if boolean is True:
            self._check_is_hovered = True
        else:
            self._check_is_hovered = False
            self._press_is_hovered = False
        #
        self._refresh_widget_draw_()

    def _set_frame_icon_size_(self, w, h):
        self._frame_icon_width, self._frame_icon_height = w, h

    def _set_frame_image_size_(self, w, h):
        self._frame_image_width, self._frame_image_height = w, h

    def _set_frame_name_size_(self, w, h):
        self._frame_name_width, self._frame_name_height = w, h

    def _get_item_(self):
        return self._list_widget_item

    def _set_item_(self, item):
        self._list_widget_item = item

    def _set_view_(self, widget):
        self._list_widget = widget

    def _get_view_(self):
        return self._list_widget

    def _refresh_widget_draw_geometry_(self):
        self._refresh_widget_frame_draw_geometries_()
        #
        self._refresh_widget_icon_draw_geometries_()
        self._refresh_widget_image_draw_geometries_()
        self._refresh_widget_name_draw_geometries_()

    def _refresh_widget_frame_draw_geometries_(self):
        if self._list_widget is not None:
            side = 4
            spacing = 2
            x, y = side, side
            w, h = self._frame_size
            self._set_frame_draw_geometry_(x, y, w, h)
            if self._list_widget._get_is_grid_mode_():
                self._set_widget_frame_geometry_update_as_grid_mode_(
                    (x, y), (w, h)
                )
            else:
                self._set_widget_frame_geometry_update_as_list_mode_(
                    (x, y), (w, h)
                )
    # frame for grid mode
    def _set_widget_frame_geometry_update_as_grid_mode_(self, pos, size):
        x, y = pos
        w, h = size
        f_spacing = self._frame_spacing
        if self._get_has_names_() is True:
            name_f_w, name_f_h = self._name_frame_size
            name_c = len(self._get_name_indices_())
            #
            name_w_, name_h_ = w, name_c*name_f_h
            name_x_, name_y_ = x, y+h-name_h_
            #
            self._name_frame_rect.setRect(
                name_x_, name_y_,
                name_w_, name_h_
            )
        else:
            name_w_, name_h_ = 0, -f_spacing
        #
        if self._get_has_icons_() is True or self._check_is_enable is True:
            #
            icn_frm_w, icn_frm_h = self._icon_frame_draw_size
            icn_x_, icn_y_ = x, y
            # add when check is enable
            icn_c = self._get_icon_count_()+[0, 1][self._check_is_enable]
            icn_h_ = h-name_h_-f_spacing
            c_0 = int(float(icn_h_)/icn_frm_h)
            c_1 = math.ceil(float(icn_c)/c_0)
            # grid to
            icn_w_, icn_h_ = icn_frm_w*c_1, icn_h_
            #
            self._icon_frame_draw_rect.setRect(
                icn_x_, icn_y_,
                icn_w_, icn_h_
            )
        else:
            icn_w_, icn_h_ = -f_spacing, 0
        #
        if self._get_has_image_() is True:
            image_x_, image_y_ = x+icn_w_+f_spacing, y
            image_w_, image_h_ = w-(icn_w_+f_spacing), h-(name_h_+f_spacing)
            self._image_frame_rect.setRect(
                image_x_, image_y_, image_w_, image_h_
            )

    def _set_widget_frame_geometry_update_as_list_mode_(self, pos, size):
        x, y = pos
        w, h = size
        width, height = self.width(), self.height()
        f_side = self._frame_side
        f_spacing = self._frame_spacing
        if self._get_has_icons_() is True or self._check_is_enable is True:
            icn_frm_w, icn_frm_h = self._icon_frame_draw_size
            icn_x_, icn_y_ = x, y
            # add when check is enable
            icn_c = self._get_icon_count_() + [0, 1][self._check_is_enable]
            icn_h_ = h
            c_0 = int(float(icn_h_) / icn_frm_h)
            c_1 = math.ceil(float(icn_c) / c_0)
            # grid to
            icn_w_, icn_h_ = icn_frm_w * c_1, icn_h_
            #
            self._icon_frame_draw_rect.setRect(
                icn_x_, icn_y_,
                icn_w_, icn_h_
            )
        else:
            icn_w_, icn_h_ = -f_spacing, 0
        #
        if self._get_has_image_() is True:
            image_x_, image_y_ = x+(icn_w_+f_spacing), y
            image_w_, image_h_ = w-(icn_w_+f_spacing), h
            self._image_frame_rect.setRect(
                image_x_, image_y_, image_w_, image_h_
            )
        else:
            image_w_, image_h_ = -f_spacing, 0
        #
        if self._get_has_names_() is True:
            name_x_, name_y_ = x+(icn_w_+f_spacing)+(image_w_+f_spacing), y
            name_w_, name_h_ = width-(icn_w_+f_spacing)-(image_w_+f_spacing)-f_side*2, h
            #
            self._name_frame_rect.setRect(
                name_x_, name_y_,
                name_w_, name_h_
            )

    def _refresh_widget_icon_draw_geometries_(self):
        if self._get_has_icons_() is True or self._check_is_enable is True:
            rect = self._icon_frame_draw_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            #
            side = 2
            spacing = 0
            #
            icn_frm_w, icn_frm_h = self._icon_frame_draw_size
            icn_w, icn_h = self._icon_size
            if self._check_is_enable is True:
                check_icn_frm_w, check_icn_frm_h = icn_frm_w*self._check_icon_frame_draw_percent, icn_frm_h*self._check_icon_frame_draw_percent
                check_icn_w, check_icn_h = icn_frm_w*self._check_icon_draw_percent, icn_frm_h*self._check_icon_draw_percent
                #
                self._set_check_action_rect_(
                    x, y, icn_frm_w, icn_frm_h
                )
                self._set_check_icon_frame_draw_rect_(
                    x+(icn_frm_w-check_icn_frm_w)/2, y+(icn_frm_h-check_icn_frm_h)/2, check_icn_frm_w, check_icn_frm_h
                )
                self._set_check_icon_draw_rect_(
                    x+(icn_frm_w-check_icn_w)/2, y+(icn_frm_h-check_icn_h)/2, check_icn_w, check_icn_h
                )
            icn_indices = self._get_icon_indices_()
            if icn_indices:
                c_0 = int(float(h) / icn_frm_h)
                if self._check_is_enable is True:
                    icn_indices_ = icn_indices+[len(icn_indices)]
                    for i_icn_index in icn_indices_:
                        i_column = int(float(i_icn_index)/c_0)
                        if i_column > 0:
                            i_icn_index_draw = i_icn_index % c_0
                        else:
                            i_icn_index_draw = i_icn_index
                        #
                        if i_icn_index > 0:
                            self._set_icon_rect_at_(
                                x+(icn_frm_w-icn_w)/2+icn_frm_w*i_column, y+(icn_frm_h-icn_h)/2+i_icn_index_draw*(icn_frm_h+spacing), icn_w, icn_h,
                                i_icn_index-1
                            )
                else:
                    for i_icn_index in icn_indices:
                        i_column = int(float(i_icn_index)/c_0)
                        if i_column > 0:
                            i_icn_index_draw = i_icn_index % c_0
                        else:
                            i_icn_index_draw = i_icn_index
                        #
                        self._set_icon_rect_at_(
                            x+(icn_frm_w-icn_w)/2+icn_frm_w*i_column, y+(icn_frm_h-icn_h)/2+i_icn_index_draw*(icn_frm_h+spacing), icn_w, icn_h,
                            i_icn_index
                        )

    def _refresh_widget_image_draw_geometries_(self):
        if self._get_has_image_() is True:
            image_file_path = self._get_image_file_path_()
            rect = self._image_frame_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            i_w_0, i_h_0 = self._get_image_size_()
            if (i_w_0, i_h_0) != (0, 0):
                i_x, i_y, icn_w, icn_h = bsc_core.SizeMtd.set_fit_to(
                    (i_w_0, i_h_0), (w, h)
                )
                if self._get_movie_enable_() is True:
                    m_f_w, m_f_h = 32, 32
                    self._set_movie_rect_(
                        x+i_x+(icn_w-m_f_w)/2, y+i_y+(icn_h-m_f_h)/2,
                        m_f_w, m_f_h
                    )
                #
                if image_file_path is not None:
                    self._set_image_rect_(
                        x+i_x+2, y+i_y+2, icn_w-4, icn_h-4
                    )
                else:
                    image_name_text = self._image_name_text
                    if image_name_text is not None:
                        self._set_image_rect_(
                            x+i_x, y+i_y, icn_w, icn_h
                        )

    def _refresh_widget_name_draw_geometries_(self):
        if self._get_has_names_():
            name_indices = self._get_name_indices_()
            #
            rect = self._name_frame_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            #
            side = 2
            spacing = 0
            #
            icn_frm_w, icn_frm_h = self._name_frame_size
            icn_w, icn_h = self._name_size
            #
            self._set_index_draw_geometry_(
                x+2, y+h-icn_h, w-4, icn_h
            )
            for i_name_index in name_indices:
                i_x, i_y = x+(icn_frm_w-icn_w)/2+side, y+(icn_frm_h-icn_h)/2+i_name_index*(icn_frm_h+spacing)
                self._set_name_text_rect_at_(
                    i_x, i_y, w-(i_x-x)-side, icn_h,
                    i_name_index
                )

            if self._icon_is_enable is True:
                if self._icon_name_text:
                    self._icon_name_draw_rect.setRect(
                        x+(w-h), y, h, h
                    )

    def __str__(self):
        return '{}(names={})'.format(
            self.__class__.__name__,
            ', '.join(self._get_name_texts_())
        )

    def __repr__(self):
        return self.__str__()
