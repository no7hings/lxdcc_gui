# coding=utf-8
import lxutil_gui.qt.abstracts as gui_qt_abstract

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui import utl_gui_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _gui_qt_wgt_chart, _gui_qt_wgt_entry_base


class QtPopupForRgbaChoose(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtPopupBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()
        self._chart.update()

    def __init__(self, *args, **kwargs):
        super(QtPopupForRgbaChoose, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setFocusProxy(self.parent())
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        #
        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        #
        self._frame_border_color = QtBackgroundColors.Light
        self._hovered_frame_border_color = QtBackgroundColors.Hovered
        self._selected_frame_border_color = QtBackgroundColors.Selected
        self._frame_background_color = QtBackgroundColors.Dark

        self._chart = _gui_qt_wgt_chart.QtColorChooseChart(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self.parent():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._close_popup_()
        elif widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._execute_popup_end_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            elif event.type() == QtCore.QEvent.Show:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        painter = QtPainter(self)
        #
        painter._draw_popup_frame_(
            bck_rect,
            margin=self._popup_margin,
            side=self._popup_side,
            shadow_radius=self._popup_shadow_radius,
            region=self._popup_region,
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
        )

    def _refresh_widget_draw_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius-2
        #
        self._chart.setGeometry(
            v_x, v_y, v_w, v_h
        )
        self._chart.update()

    def _execute_popup_start_(self):
        parent = self.parent()
        press_rect = parent._get_color_rect_()
        press_point = self._get_popup_press_point_(parent, press_rect)
        desktop_rect = get_qt_desktop_rect()
        self._show_popup_0_(
            press_point,
            press_rect,
            desktop_rect,
            320, 320
        )
        self._chart._set_color_rgba_(*parent._get_color_rgba_())
        parent._set_focused_(True)

    def _execute_popup_end_(self, *args, **kwargs):
        r, g, b, a = self._chart._get_color_rgba_()
        self.parent()._set_color_rgba_(r, g, b, a)


class QtPopupForChoose(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtPopupBaseDef,
):
    HEIGHT_MAX = 480
    TAG_ALL = 'All'
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        tbr_h = self._popup_toolbar_h
        spacing = 2
        c_x, c_y = x+1, y+1
        c_w, c_h = w-2, h-2
        #
        self._frame_draw_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        #
        self._popup_toolbar_draw_rect.setRect(
            c_x+2, c_y, c_w-4, tbr_h
        )
        tbr_w = c_w
        # close button
        self._popup_close_button.setGeometry(
            c_x+c_w-tbr_h*1, c_y, tbr_h, tbr_h
        )
        tbr_w -= (tbr_h+spacing)
        #
        if self._popup_multiply_is_enable is True:
            self._popup_all_checked_button.show()
            self._popup_all_unchecked_button.show()
            self._popup_all_checked_button.setGeometry(
                c_x+c_w-(tbr_h*3+spacing*2), c_y, tbr_h, tbr_h
            )
            tbr_w -= (tbr_h+spacing)
            self._popup_all_unchecked_button.setGeometry(
                c_x+c_w-(tbr_h*2+spacing*1), c_y, tbr_h, tbr_h
            )
            tbr_w -= (tbr_h+spacing)
        #
        self._popup_toolbar_draw_tool_tip_rect.setRect(
            c_x, c_y, tbr_w-tbr_h, tbr_h
        )
        self._popup_text_entry.setGeometry(
            c_x, c_y, tbr_w-tbr_h, tbr_h
        )
        #
        c_y += tbr_h
        c_h -= tbr_h

        if self._tag_filter_is_enable is True:
            t_w = c_w*self._tag_filter_width_percent
            self._tag_filter_list_widget.setGeometry(
                c_x+1, c_y+1, t_w-2, c_h-2
            )
            self._tag_filter_draw_rect.setRect(
                c_x, c_y, t_w, c_h
            )
            c_x += t_w
            c_w -= t_w
        #
        self._tag_filter_list_widget.updateGeometries()

        self._popup_view.setGeometry(
            c_x+1, c_y+1, c_w-2, c_h-2
        )
        self._popup_view.updateGeometries()

    def __init__(self, *args, **kwargs):
        super(QtPopupForChoose, self).__init__(*args, **kwargs)
        # use popup?
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        #
        self._popup_item_width, self._popup_item_height = 20, 20
        self._popup_tag_filter_item_width, self._popup_tag_filter_item_height = 20, 20
        #
        self._popup_close_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._popup_close_button._set_name_text_('close popup')
        self._popup_close_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('close'))
        self._popup_close_button._set_icon_hover_color_(QtBackgroundColors.DeleteHovered)
        self._popup_close_button._set_icon_frame_draw_size_(18, 18)
        self._popup_close_button.press_clicked.connect(self._close_popup_)
        self._popup_close_button._set_tool_tip_text_(
            '"LMB-click" to close'
        )
        #
        self._popup_multiply_is_enable = False
        self._popup_all_checked_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._popup_all_checked_button.hide()
        self._popup_all_checked_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_checked'))
        self._popup_all_checked_button._set_icon_frame_draw_size_(18, 18)
        self._popup_all_checked_button.setToolTip(
            '"LMB-click" to checked all'
        )
        self._popup_all_checked_button.press_clicked.connect(self._execute_popup_all_checked_)
        #
        self._popup_all_unchecked_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._popup_all_unchecked_button.hide()
        self._popup_all_unchecked_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_unchecked'))
        self._popup_all_unchecked_button._set_icon_frame_draw_size_(18, 18)
        self._popup_all_unchecked_button.setToolTip(
            '"LMB-click" to unchecked all'
        )
        self._popup_all_unchecked_button.press_clicked.connect(self._execute_popup_all_unchecked_)
        # keyword filter
        self._keyword_filter_is_enable = False
        self._popup_text_entry = _gui_qt_wgt_entry_base.QtEntryAsTextEdit(self)
        self._popup_text_entry.hide()
        self._popup_text_entry._set_entry_enable_(True)
        self._popup_text_entry.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self._popup_text_entry.installEventFilter(self)
        # tag filter
        self._tag_filter_is_enable = False
        self._tag_filter_width_percent = 0.375
        self._tag_filter_draw_rect = QtCore.QRect()
        self._tag_filter_list_widget = _gui_qt_wgt_entry_base.QtEntryAsListForPopup(self)
        self._tag_filter_list_widget.hide()
        self._tag_filter_list_widget.setGridSize(
            QtCore.QSize(self._popup_item_width, self._popup_item_height)
        )
        self._tag_filter_list_widget.setSpacing(2)
        self._tag_filter_list_widget.setUniformItemSizes(True)
        #
        self._popup_view = _gui_qt_wgt_entry_base.QtEntryAsListForPopup(self)
        #
        self._item_count_maximum = 10
        self._popup_view.setGridSize(
            QtCore.QSize(self._popup_item_width, self._popup_item_height)
        )
        self._popup_view.setSpacing(2)
        self._popup_view.setUniformItemSizes(True)
        #
        self._choose_index = None
        #
        self._frame_border_color = QtBackgroundColors.Light
        self._hovered_frame_border_color = QtBackgroundColors.Hovered
        self._selected_frame_border_color = QtBackgroundColors.Hovered
        #
        self._frame_background_color = QtBackgroundColors.Dark

        self._read_only_mark = None

        self._popup_name_text = None

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=QtBorderColors.Popup,
            background_color=self._frame_background_color,
            border_radius=1,
            border_width=2
        )
        painter._draw_line_by_points_(
            point_0=self._popup_toolbar_draw_rect.bottomLeft(),
            point_1=self._popup_toolbar_draw_rect.bottomRight(),
            border_color=self._frame_border_color,
        )
        if self._keyword_filter_is_enable is True:
            if not self._popup_text_entry.text():
                painter._draw_text_by_rect_(
                    self._popup_toolbar_draw_tool_tip_rect,
                    'entry keyword to filter ...',
                    font=Font.NAME,
                    font_color=QtFontColors.Disable,
                    text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                )
        else:
            if self._popup_name_text:
                painter._draw_text_by_rect_(
                    self._popup_toolbar_draw_tool_tip_rect,
                    self._popup_name_text,
                    font=Font.NAME,
                    font_color=QtFontColors.Disable,
                    text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                )
        #
        if self._tag_filter_is_enable is True:
            painter._draw_line_by_points_(
                point_0=self._tag_filter_draw_rect.topRight(),
                point_1=self._tag_filter_draw_rect.bottomRight(),
                border_color=self._frame_border_color,
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._popup_entry:
            if event.type() == QtCore.QEvent.FocusOut:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.InputMethod:
                self._popup_text_entry.inputMethodEvent(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self._close_popup_()
                else:
                    self._popup_text_entry.keyPressEvent(event)
        return False

    def _set_popup_keyword_filter_enable_(self, boolean):
        self._keyword_filter_is_enable = boolean
        if boolean is True:
            self._popup_text_entry.show()
            self._popup_text_entry.entry_changed.connect(
                self._execute_popup_filter_
            )

    def _set_popup_tag_filter_enable_(self, boolean):
        self._tag_filter_is_enable = boolean
        if boolean is True:
            self._tag_filter_list_widget.show()
            self._tag_filter_list_widget.itemSelectionChanged.connect(
                self._execute_popup_filter_
            )

    def _set_popup_choose_multiply_enable_(self, boolean):
        self._popup_multiply_is_enable = boolean

    def _get_popup_multiply_is_enable_(self):
        return self._popup_multiply_is_enable

    def _set_popup_name_text_(self, text):
        self._popup_name_text = text

    def _execute_popup_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._popup_view._set_scroll_to_pre_item_()

    def _execute_popup_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._popup_view._set_scroll_to_next_item_()

    def _set_popup_item_show_(self, item, item_widget, data):
        def cache_fnc_():
            return data

        def build_fnc_(data_):
            _image_url, = data_
            item_widget._set_image_url_(_image_url)

        item._set_item_show_fnc_(cache_fnc_, build_fnc_)
        item_widget._set_image_draw_enable_(True)

    def _execute_popup_start_(self):
        if self._popup_is_activated is False:
            parent = self.parent()
            self._popup_view._set_clear_()
            self._tag_filter_list_widget._set_clear_()
            self._popup_text_entry._set_clear_()
            values = parent._get_choose_values_()
            if values:
                if isinstance(values, (tuple, list)):
                    icon_file_path = parent._get_choose_item_icon_file_path_()
                    icon_file_path_dict = parent._get_choose_item_icon_file_dict_()
                    image_url_dict = parent._get_choose_image_url_dict_()
                    keyword_filter_dict = parent._get_choose_keyword_filter_dict_()
                    tag_filter_dict = parent._get_choose_tag_filter_dict_()
                    #
                    current_values = parent._get_choose_current_values_()
                    for index, i_name_text in enumerate(values):
                        i_item_widget = _utl_gui_qt_wgt_utility._QtHItem()
                        i_item = _utl_gui_qt_wgt_utility.QtListWidgetItem()
                        i_item.setSizeHint(QtCore.QSize(self._popup_item_width, self._popup_item_height))
                        #
                        self._popup_view.addItem(i_item)
                        self._popup_view.setItemWidget(i_item, i_item_widget)
                        i_item._set_item_show_connect_()
                        #
                        i_item_widget._set_name_text_(i_name_text)
                        i_item_widget._set_tool_tip_(i_name_text)
                        #
                        if self._get_popup_multiply_is_enable_() is True:
                            i_item_widget._set_check_action_enable_(True)
                            i_item_widget._set_check_enable_(True)
                        #
                        if i_name_text in image_url_dict:
                            self._set_popup_item_show_(
                                i_item, i_item_widget, [image_url_dict[i_name_text]]
                            )
                        else:
                            if icon_file_path:
                                i_item_widget._set_icon_file_path_(icon_file_path)
                            else:
                                if i_name_text in icon_file_path_dict:
                                    i_icon_file_path = icon_file_path_dict[i_name_text]
                                    i_item_widget._set_icon_file_path_(i_icon_file_path)
                                else:
                                    i_item_widget._set_icon_text_(i_name_text)
                        #
                        if i_name_text in keyword_filter_dict:
                            i_filter_keys = keyword_filter_dict[i_name_text]
                            i_item._update_item_keyword_filter_keys_tgt_(i_filter_keys)
                            i_item_widget._set_name_texts_(
                                i_filter_keys
                            )
                            i_item_widget._set_tool_tip_(
                                i_filter_keys
                            )
                        else:
                            i_item._update_item_keyword_filter_keys_tgt_([i_name_text])
                        #
                        if i_name_text in tag_filter_dict:
                            i_filter_keys = tag_filter_dict[i_name_text]
                            i_item._set_item_tag_filter_mode_(i_item.TagFilterMode.MatchOne)
                            i_item._set_item_tag_filter_keys_tgt_update_(i_filter_keys)
                        #
                        if current_values:
                            # auto select last item
                            if isinstance(current_values, (tuple, list)):
                                if i_name_text == current_values[-1]:
                                    i_item.setSelected(True)
                            elif isinstance(current_values, six.string_types):
                                if i_name_text == current_values:
                                    i_item.setSelected(True)
                            # scroll to selected
                            self._popup_view._set_scroll_to_selected_item_top_()
                        #
                        i_item_widget.press_clicked.connect(self._execute_popup_end_)
                    #
                    press_pos = self._get_popup_pos_(self._popup_entry_frame)
                    width, height = self._get_popup_size_(self._popup_entry_frame)
                    item_count = int(self.HEIGHT_MAX/self._popup_item_height)
                    height_max = self._popup_view._get_maximum_height_(item_count)
                    height_max += self._popup_toolbar_h
                    #
                    self._show_popup_(
                        press_pos,
                        (width, height_max)
                    )
                    #
                    self._popup_entry._set_focused_(True)
                    #
                    self._popup_is_activated = True
                    # show
                    self._popup_view._refresh_view_all_items_viewport_showable_()

                    if isinstance(self._popup_entry, QtWidgets.QLineEdit):
                        self._read_only_mark = self._popup_entry.isReadOnly()
                        #
                        self._popup_entry.setReadOnly(True)
                    # tag filter
                    if self._tag_filter_is_enable is True:
                        tags = list(set([i for k, v in tag_filter_dict.items() for i in v]))
                        tags = bsc_core.RawTextsMtd.sort_by_initial(tags)
                        if self.TAG_ALL in tags:
                            tags.remove(self.TAG_ALL)
                            tags.insert(0, self.TAG_ALL)
                        for i_tag in tags:
                            i_item_widget = _utl_gui_qt_wgt_utility._QtHItem()
                            i_item = _utl_gui_qt_wgt_utility.QtListWidgetItem()
                            i_item.setSizeHint(
                                QtCore.QSize(self._popup_tag_filter_item_width, self._popup_tag_filter_item_height)
                                )
                            #
                            self._tag_filter_list_widget.addItem(i_item)
                            self._tag_filter_list_widget.setItemWidget(i_item, i_item_widget)
                            i_item._set_item_show_connect_()
                            #
                            i_item_widget._set_name_text_(i_tag)
                            i_item_widget._set_icon_text_(i_tag)
                            i_item_widget._set_tool_tip_text_(i_tag)
                            #
                            i_item_widget._set_item_tag_filter_keys_src_add_(i_tag)

    def _execute_popup_end_(self):
        selected_item_widgets = self._popup_view._get_selected_item_widgets_()
        if selected_item_widgets:
            texts = [i._get_name_text_() for i in selected_item_widgets]
            self.user_popup_choose_texts_accepted.emit(texts)
            self.user_popup_choose_text_accepted.emit(texts[0])
            #
            if self._get_popup_multiply_is_enable_() is True:
                checked_item_widgets = self._popup_view._get_checked_item_widgets_()
                if checked_item_widgets:
                    texts = [i._get_name_text_() for i in checked_item_widgets]
                    self.user_popup_choose_texts_accepted.emit(texts)
                    self.user_popup_choose_text_accepted.emit(texts[0])
            #
            self.user_popup_choose_finished.emit()
        #
        self._close_popup_()

    def _set_popup_entry_(self, widget):
        self._popup_entry = widget
        self._popup_entry.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._popup_entry)
        self._popup_text_entry.setFocusProxy(self._popup_entry)
        self._tag_filter_list_widget.setFocusProxy(
            self._popup_entry
        )
        self._popup_view.setFocusProxy(
            self._popup_entry
        )

    def _set_popup_item_size_(self, w, h):
        self._popup_item_width, self._popup_item_height = w, h
        self._popup_view.setGridSize(
            QtCore.QSize(self._popup_item_width, self._popup_item_height)
        )

    def _set_popup_tag_filter_item_size_(self, w, h):
        self._popup_tag_filter_item_width, self._popup_tag_filter_item_height = w, h
        self._tag_filter_list_widget.setGridSize(
            QtCore.QSize(self._popup_tag_filter_item_width, self._popup_tag_filter_item_height)
        )

    def _execute_popup_filter_(self):
        # tag filter
        selected_item_widgets = self._tag_filter_list_widget._get_selected_item_widgets_()
        if selected_item_widgets:
            item_src = selected_item_widgets[0]
            tags = [item_src._get_name_text_()]
            self._popup_view._set_view_tag_filter_data_src_(tags)
        # keyword filter
        self._popup_view._set_view_keyword_filter_data_src_([self._popup_text_entry.text()])
        #
        self._popup_view._refresh_view_items_visible_by_any_filter_()
        self._popup_view._refresh_view_all_items_viewport_showable_()
        #
        if self._popup_auto_resize_is_enable is True:
            self._execute_auto_resize_()

    def _execute_popup_all_checked_(self):
        [i._set_checked_(True) for i in self._popup_view._get_all_item_widgets_() if i._get_is_visible_() is True]

    def _execute_popup_all_unchecked_(self):
        [i._set_checked_(False) for i in self._popup_view._get_all_item_widgets_() if
         i._get_is_visible_() is True]

    def _close_popup_(self):
        if isinstance(self._popup_entry, QtWidgets.QLineEdit):
            if self._read_only_mark is not None:
                self._popup_entry.setReadOnly(self._read_only_mark)
        #
        self._set_popup_activated_(False)

    def _execute_auto_resize_(self):
        visible_items = self._popup_view._get_visible_items_()
        press_pos = self._get_popup_pos_(self._popup_entry_frame)
        width, height = self._get_popup_size_(self._popup_entry_frame)
        height_max = self._popup_view._get_maximum_height_(self._item_count_maximum, includes=visible_items)
        height_max += self._popup_toolbar_h
        #
        self._show_popup_(
            press_pos,
            (width, height_max)
        )


class QtPopupForHistory(
    QtPopupForChoose
):
    def __init__(self, *args, **kwargs):
        super(QtPopupForHistory, self).__init__(*args, **kwargs)


class QtPopupForCompletion(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtPopupBaseDef,
):
    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        c_x, c_y = x+1, y+1
        c_w, c_h = w-2, h-2
        tbr_h = self._popup_toolbar_h
        spacing = 2
        #
        self._frame_draw_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        #
        self._frame_draw_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        tbr_w = c_w
        #
        self._popup_toolbar_draw_rect.setRect(
            c_x+2, c_y, c_w-4, tbr_h
        )
        self._popup_toolbar_draw_tool_tip_rect.setRect(
            c_x, c_y, tbr_w-tbr_h, tbr_h
        )
        tbr_w = c_w
        # close button
        self._popup_close_button.setGeometry(
            c_x+c_w-tbr_h*1, c_y, tbr_h, tbr_h
        )
        tbr_w -= (tbr_h+spacing)
        c_y += tbr_h
        c_h -= tbr_h

        self._popup_view.setGeometry(
            c_x+1, c_y+1, c_w-2, c_h-2
        )
        self._popup_view.updateGeometries()

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtPopupForCompletion, self).__init__(*args, **kwargs)
        # use tool tip
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        #
        self._popup_close_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._popup_close_button._set_name_text_('close popup')
        self._popup_close_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('close'))
        self._popup_close_button._set_icon_hover_color_(QtBackgroundColors.DeleteHovered)
        self._popup_close_button.press_clicked.connect(self._close_popup_)
        self._popup_close_button._set_tool_tip_text_(
            '"LMB-click" to close'
        )
        #
        self._popup_view = _gui_qt_wgt_entry_base.QtEntryAsListForPopup(self)
        #
        self._item_count_maximum = 10
        self._popup_item_width, self._popup_item_height = 20, 20
        self._popup_view.setGridSize(QtCore.QSize(self._popup_item_width, self._popup_item_height))
        self._popup_view.setSpacing(2)
        self._popup_view.setUniformItemSizes(True)
        self._popup_view.itemClicked.connect(
            self._execute_popup_end_
        )
        #
        self._choose_index = None
        #
        self._frame_border_color = QtBackgroundColors.Light
        self._hovered_frame_border_color = QtBackgroundColors.Hovered
        self._selected_frame_border_color = QtBackgroundColors.Hovered
        #
        self._frame_background_color = QtBackgroundColors.Dark

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=QtBorderColors.Popup,
            background_color=self._frame_background_color,
            border_radius=1,
            border_width=2
        )
        painter._draw_line_by_points_(
            point_0=self._popup_toolbar_draw_rect.bottomLeft(),
            point_1=self._popup_toolbar_draw_rect.bottomRight(),
            border_color=self._frame_border_color,
        )

        c = self._popup_view._get_all_item_count_()
        if c:
            painter._draw_text_by_rect_(
                self._popup_toolbar_draw_tool_tip_rect,
                '{} results is matching ...'.format(c),
                font=Font.NAME,
                font_color=QtFontColors.Disable,
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._popup_entry:
            if event.type() == QtCore.QEvent.FocusOut:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self._close_popup_()
        return False

    def _set_popup_entry_(self, widget):
        self._popup_entry = widget
        self._popup_entry.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._popup_entry)

    def _execute_popup_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._popup_view._set_scroll_to_pre_item_()

    def _execute_popup_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._popup_view._set_scroll_to_next_item_()

    def _execute_popup_start_(self, *args, **kwargs):
        parent = self.parent()
        self._popup_view._set_clear_()
        name_texts = parent._get_completion_extra_data_()
        if name_texts:
            has_match = False
            current_name_text = self._popup_entry._get_value_()
            for index, i_name_text in enumerate(name_texts):
                i_item_widget = _utl_gui_qt_wgt_utility._QtHItem()
                i_item = _utl_gui_qt_wgt_utility.QtListWidgetItem()
                i_item.setSizeHint(QtCore.QSize(self._popup_item_width, self._popup_item_height))
                #
                self._popup_view.addItem(i_item)
                self._popup_view.setItemWidget(i_item, i_item_widget)
                i_item._set_item_show_connect_()
                #
                i_item_widget._set_name_text_(i_name_text)
                i_item_widget._set_icon_text_(i_name_text)
                i_item_widget._set_index_(index)
                #
                if current_name_text == i_name_text:
                    has_match = True
                    i_item.setSelected(True)
            #
            if has_match is False:
                self._popup_view._get_all_items_()[0].setSelected(True)

            press_pos = self._get_popup_pos_0_(self._popup_entry_frame)
            width, height = self._get_popup_size_(self._popup_entry_frame)
            height_max = self._popup_view._get_maximum_height_(self._item_count_maximum)
            height_max += self._popup_toolbar_h

            self._show_popup_(
                press_pos,
                (width, height_max)
            )

            self._popup_view._set_scroll_to_selected_item_top_()

            self._popup_entry._set_focused_(True)

            self._popup_is_activated = True
        else:
            self._close_popup_()

    def _execute_popup_end_(self, *args, **kwargs):
        selected_item_widget = self._popup_view._get_selected_item_widget_()
        if selected_item_widget:
            text = selected_item_widget._get_name_text_()
            #
            self.user_popup_choose_text_accepted.emit(text)
        #
        self.user_popup_choose_finished.emit()
        #
        self._close_popup_()

    def _close_popup_(self):
        self._set_popup_activated_(False)


class QtPopupForGuideChoose(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtPopupBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(QtPopupForGuideChoose, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setPalette(QtDccMtd.get_palette())
        #
        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        #
        self._popup_text_entry = _gui_qt_wgt_entry_base.QtEntryAsTextEdit(self)
        self._popup_text_entry.hide()
        self._popup_text_entry._set_entry_enable_(True)
        self._popup_text_entry.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self._popup_text_entry.entry_changed.connect(
            self._execute_popup_filter_
        )
        #
        self._popup_close_button = _utl_gui_qt_wgt_utility.QtIconPressButton(self)
        self._popup_close_button._set_name_text_('close popup')
        self._popup_close_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('close'))
        self._popup_close_button._set_icon_hover_color_(QtBackgroundColors.DeleteHovered)
        self._popup_close_button.press_clicked.connect(self._close_popup_)
        self._popup_close_button._set_tool_tip_text_(
            '"LMB-click" to close'
        )
        #
        self._popup_view = _gui_qt_wgt_entry_base.QtEntryAsListForPopup(self)
        #
        self._item_count_maximum = 10
        self._popup_item_width, self._popup_item_height = 20, 20
        #
        self._popup_view.setGridSize(QtCore.QSize(self._popup_item_width, self._popup_item_height))
        self._popup_view.setSpacing(2)
        self._popup_view.setUniformItemSizes(True)
        self._popup_view.itemClicked.connect(
            self._execute_popup_end_
        )
        #
        self._choose_index = None
        #
        self._frame_border_color = QtBackgroundColors.Light
        self._hovered_frame_border_color = QtBackgroundColors.Hovered
        self._selected_frame_border_color = QtBackgroundColors.Selected
        #
        self._frame_background_color = QtBackgroundColors.Dark

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        painter = QtPainter(self)
        #
        painter._draw_popup_frame_(
            bck_rect,
            margin=self._popup_margin,
            side=self._popup_side,
            shadow_radius=self._popup_shadow_radius,
            region=self._popup_region,
            border_color=QtBorderColors.Popup,
            background_color=self._frame_background_color,
            border_width=2
        )
        painter._draw_line_by_points_(
            point_0=self._popup_toolbar_draw_rect.bottomLeft(),
            point_1=self._popup_toolbar_draw_rect.bottomRight(),
            border_color=self._frame_border_color,
        )
        #
        if not self._popup_text_entry.text():
            painter._draw_text_by_rect_(
                self._popup_toolbar_draw_tool_tip_rect,
                'entry keyword to filter ...',
                font=Font.NAME,
                font_color=QtFontColors.Disable,
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._popup_entry:
            #
            if event.type() == QtCore.QEvent.FocusOut:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self._close_popup_()
                else:
                    self._popup_text_entry.keyPressEvent(event)
        return False

    def _execute_popup_filter_(self):
        # keyword filter
        self._popup_view._set_view_keyword_filter_data_src_([self._popup_text_entry.text()])
        #
        self._popup_view._refresh_view_items_visible_by_any_filter_()
        self._popup_view._refresh_view_all_items_viewport_showable_()

    def _set_popup_entry_(self, widget):
        self._popup_entry = widget
        self._popup_entry.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._popup_entry)
        self._popup_text_entry.setFocusProxy(self._popup_entry)

        self._popup_entry.key_up_pressed.connect(
            self._popup_view._set_scroll_to_pre_item_
        )
        self._popup_entry.key_down_pressed.connect(
            self._popup_view._set_scroll_to_next_item_
        )
        self._popup_entry.key_enter_pressed.connect(
            self._execute_popup_end_
        )

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()

        tbr_h = self._popup_toolbar_h
        spacing = 2

        c_x, c_y = x+margin+side+1, y+margin+side+1
        c_w, c_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius-2

        tbr_w = c_w

        self._popup_toolbar_draw_rect.setRect(
            c_x+2, c_y, c_w-4, tbr_h
        )
        self._popup_toolbar_draw_tool_tip_rect.setRect(
            c_x, c_y, tbr_w-tbr_h, tbr_h
        )
        self._popup_text_entry.show()
        self._popup_text_entry.setGeometry(
            c_x, c_y, tbr_w-tbr_h, tbr_h
        )
        # close button
        self._popup_close_button.setGeometry(
            c_x+c_w-tbr_h*1, c_y, tbr_h, tbr_h
        )
        tbr_w -= (tbr_h+spacing)
        c_y += tbr_h
        c_h -= tbr_h
        #
        self._popup_view.setGeometry(
            c_x, c_y, c_w, c_h
        )
        self._popup_view.updateGeometries()

    def _execute_popup_start_(self, index):
        parent = self.parent()
        name_texts = parent._get_guide_child_name_texts_at_(index)
        if name_texts:
            desktop_rect = get_qt_desktop_rect()
            #
            press_pos = parent._get_guide_choose_point_at_(index)
            press_rect = parent._get_guide_choose_rect_at_(index)
            #
            current_name_text = parent._get_guide_name_text_at_(index)
            for seq, i_name_text in enumerate(name_texts):
                i_item_widget = _utl_gui_qt_wgt_utility._QtHItem()
                i_item = _utl_gui_qt_wgt_utility.QtListWidgetItem()
                i_item.setSizeHint(QtCore.QSize(self._popup_item_width, self._popup_item_height))
                #
                self._popup_view.addItem(i_item)
                self._popup_view.setItemWidget(i_item, i_item_widget)
                i_item._set_item_show_connect_()
                i_item._update_item_keyword_filter_keys_tgt_([i_name_text])
                #
                if i_name_text:
                    i_item_widget._set_name_text_(i_name_text)
                    i_item_widget._set_icon_text_(i_name_text)
                #
                i_item_widget._set_index_(seq)
                if current_name_text == i_name_text:
                    i_item.setSelected(True)
            #
            self.setFocus(QtCore.Qt.PopupFocusReason)
            #
            height_max = self._popup_view._get_maximum_height_(self._item_count_maximum)
            height_max += self._popup_toolbar_h
            popup_width = self._get_popup_width_(name_texts)
            popup_width = max(self._popup_width_minimum, popup_width)
            #
            self._show_popup_0_(
                press_pos, press_rect,
                desktop_rect,
                popup_width,
                height_max
            )
            self._choose_index = index
            parent._set_guide_choose_item_expand_at_(index)
            #
            self._popup_view._set_scroll_to_selected_item_top_()
            #
            self._popup_entry._set_focused_(True)
            #
            self._popup_is_activated = True
        else:
            self._close_popup_()

    def _execute_popup_end_(self):
        if self._choose_index is not None:
            parent = self.parent()
            selected_item_widget = self._popup_view._get_selected_item_widget_()
            if selected_item_widget:
                name_text_cur = selected_item_widget._get_name_text_()
                #
                path_text_cur = parent._set_guide_name_text_at_(
                    name_text_cur,
                    self._choose_index
                )
                parent._refresh_guide_draw_geometry_()
                # choose
                parent.guide_text_choose_accepted.emit(path_text_cur)
            # clear latest
            parent._clear_guide_current_()
        #
        self._close_popup_()

    def _set_popup_activated_(self, boolean):
        super(QtPopupForGuideChoose, self)._set_popup_activated_(boolean)
        #
        if self._choose_index is not None:
            parent = self.parent()
            parent._set_guide_choose_item_collapse_at_(self._choose_index)

    def _get_popup_width_(self, texts):
        count = len(texts)
        _ = max([self.fontMetrics().width(i) for i in texts])+32
        _count_width = self.fontMetrics().width(str(count))
        if count > self._item_count_maximum:
            return _+_count_width+24
        return _+_count_width

    def _get_maximum_height_(self):
        rects = [self._popup_view.visualItemRect(self._popup_view.item(i)) for i in
                 range(self._popup_view.count())[:self._item_count_maximum]]
        if rects:
            rect = rects[-1]
            y = rect.y()
            h = rect.height()
            return y+h+1+4
        return 0

    def _close_popup_(self):
        self._set_popup_activated_(False)


class QtPopupProxy(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef
):
    def _refresh_widget_draw_(self):
        pass

    def __init__(self, *args, **kwargs):
        super(QtPopupProxy, self).__init__(*args, **kwargs)

    def _set_popup_widget_(self, widget):
        pass

    def _execute_popup_start_(self):
        pass

    def _execute_popup_end_(self):
        pass
