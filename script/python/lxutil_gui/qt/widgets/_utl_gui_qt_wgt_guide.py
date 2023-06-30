# coding=utf-8
import fnmatch

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_entry_base, _utl_gui_qt_wgt_popup

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class QtGuideRect(
    utl_gui_qt_abstract.AbsQtIconBaseDef,
    utl_gui_qt_abstract.AbsQtTypeDef,
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    utl_gui_qt_abstract.AbsQtPathBaseDef,
    utl_gui_qt_abstract.AbsQtFrameBaseDef,
    #
    utl_gui_qt_abstract.AbsQtChooseBaseDef,
):
    def _refresh_widget_draw_(self):
        pass

    def update(self):
        pass

    def __init__(self):
        self._init_icon_base_def_(self)
        self._init_type_def_(self)
        self._init_name_base_def_(self)
        self._init_path_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_choose_base_def_()
        #
        self._set_icon_file_path_(
            self._choose_collapse_icon_file_path
        )

    def _get_icon_file_path_(self):
        return [
            self._choose_collapse_icon_file_path,
            self._choose_expand_icon_file_path
        ][self._get_choose_is_activated_()]


class QtGuideEntry(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtNameBaseDef,
    utl_gui_qt_abstract.AbsQtMenuBaseDef,
    #
    utl_gui_qt_abstract.AbsQtActionBaseDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    #
    utl_gui_qt_abstract.AbsQtDeleteBaseDef,
    #
    utl_gui_qt_abstract.AbsQtFocusDef,
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
    #
    utl_gui_qt_abstract.AbsQtGuideEntryDef,
):
    def _refresh_focus_draw_geometry_(self):
        pass

    QT_GUIDE_RECT_CLS = QtGuideRect
    #
    QT_POPUP_GUIDE_CHOOSE_CLS = _utl_gui_qt_wgt_popup.QtPopupForGuideChoose
    #
    QT_VALUE_ENTRY_CLS = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit
    #
    TYPE_FONT_SIZE = 10
    NAME_FONT_SIZE = 12
    #
    entry_started = qt_signal()
    # for popup choose
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()
    key_enter_pressed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtGuideEntry, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setFont(Font.title)
        #
        self.setMaximumHeight(22)
        self.setMinimumHeight(22)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        #
        self._init_name_base_def_(self)
        self._init_entry_base_def_(self)
        self._init_focus_def_(self)
        #
        self._choose_item_icon_file_path = utl_core.Icon.get('choose_close')
        #
        self._init_menu_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_delete_base_def_(self)
        # self._set_delete_enable_(True)
        #
        self._init_guide_entry_def_(self)

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_guide_draw_geometry_(self):
        # side = 2
        spacing = 2
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        frm_w, frm_h = 18, 18
        icn_w, icn_h = 12, 12
        #
        c_x, c_y = x, (h-frm_h)/2
        #
        for i_index in self._get_guide_item_indices_():
            i_item = self._get_guide_item_at_(i_index)
            #
            i_type_text = i_item._type_text
            i_name_text = i_item._name_text
            # text
            i_text_x = c_x
            i_text_w = 0
            if i_type_text:
                i_type_w, _ = RawTextMtd.get_size(self.TYPE_FONT_SIZE, i_type_text)
                i_type_w_ = i_type_w + spacing*2
                i_text_w += i_type_w_
                i_item._set_type_draw_rect_(
                    c_x, c_y, i_type_w_, frm_h
                )
            else:
                i_type_w_ = 0
            #
            i_name_w, _ = RawTextMtd.get_size(self.NAME_FONT_SIZE, i_name_text)
            i_name_w_ = i_name_w + spacing*2
            i_text_w += i_name_w_
            #
            i_item._set_name_draw_rect_(
                i_text_x+i_type_w_, c_y, i_name_w_, frm_h
            )
            i_item._set_name_frame_rect_(
                i_text_x, c_y, i_text_w, frm_h
            )
            #
            c_x += i_text_w
            # popup
            i_item._set_icon_frame_draw_rect_(
                c_x, c_y, frm_w, frm_h
            )

            i_item._set_icon_file_draw_rect_(
                c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
            )
            c_x += frm_w
        #
        dlt_w, dlt_h = self._delete_icon_file_draw_size
        #
        self._delete_action_rect.setRect(
            w-frm_w, c_y, frm_w, frm_h
        )
        self._delete_icon_draw_rect.setRect(
            w-frm_w+(frm_w-dlt_w)/2, c_y+(frm_h-dlt_h)/2, dlt_w, dlt_h
        )
        #
        # self.setFixedWidth(c_x)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_guide_draw_geometry_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._is_hovered = False
                self._delete_is_hovered = False
                self._clear_guide_choose_current_()
                self._clear_guide_current_()
                self.update()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._update_guide_current_(event)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._update_guide_current_(event)
                    self._restore_guide_choose_()
                    # root
                    # choose
                    if self._guide_choose_index_current is not None:
                        self._set_action_flag_(self.ActionFlag.ChooseClick)
                    # press
                    elif self._guide_index_current is not None:
                        self._set_action_flag_(self.ActionFlag.PressClick)
                    else:
                        self.entry_started.emit()
                if event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self.press_db_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    # choose
                    if self._get_is_guide_choose_flag_() is True:
                        self._start_guide_choose_item_popup_at_(self._guide_choose_index_current)
                    # press
                    elif self._get_action_press_flag_is_click_() is True:
                        # press
                        self.guide_text_press_accepted.emit(self._get_guide_path_text_at_(self._guide_index_current))
                        #
                        self.guide_press_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._clear_all_action_flags_()
                #
                self._is_hovered = False
                self._refresh_widget_draw_()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                if self._guide_index_current is not None:
                    self._execute_action_guide_choose_wheel_(event)
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_entry_base.QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _utl_gui_qt_wgt_entry_base.QtEntryFrame):
                    entry_frame._set_focused_(False)
            #
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Up:
                    self.key_up_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Down:
                    self.key_down_pressed.emit()
                elif event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                    self.key_enter_pressed.emit()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)

        for i_index in self._get_guide_item_indices_():
            i_item = self._get_guide_item_at_(i_index)
            i_icon_offset = 0
            name_offset = 0
            choose_is_hovered = i_index == self._guide_choose_index_current
            guide_is_hovered = i_index == self._guide_index_current
            if i_index == self._guide_choose_index_current:
                i_icon_offset = [0, 2][self._get_action_flag_() is not None]
                background_color = painter._get_item_background_color_1_by_rect_(
                    i_item._icon_frame_draw_rect,
                    is_hovered=choose_is_hovered,
                    is_actioned=self._get_is_actioned_(),
                )
                painter._draw_frame_by_rect_(
                    i_item._icon_frame_draw_rect,
                    border_color=QtBackgroundColors.Transparent,
                    background_color=background_color,
                    border_radius=3,
                    offset=i_icon_offset
                )
            elif i_index == self._guide_index_current:
                background_color = painter._get_item_background_color_1_by_rect_(
                    i_item._name_frame_draw_rect,
                    is_hovered=guide_is_hovered,
                    is_actioned=self._get_is_actioned_(),
                )
                name_offset = [0, 2][self._get_action_flag_() is not None]
                painter._draw_frame_by_rect_(
                    i_item._name_frame_draw_rect,
                    border_color=QtBackgroundColors.Transparent,
                    background_color=background_color,
                    border_radius=3,
                    offset=name_offset
                )
            #
            painter._draw_icon_file_by_rect_(
                i_item._icon_draw_rect,
                file_path=i_item._get_icon_file_path_(),
                offset=i_icon_offset
            )
            #
            i_type_text = i_item._type_text
            painter._draw_text_by_rect_(
                rect=i_item._type_rect,
                text=i_type_text,
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                font_color=bsc_core.RawTextOpt(i_type_text).to_rgb_0(s_p=100, v_p=100),
                font=get_font(size=self.TYPE_FONT_SIZE, italic=True),
                offset=name_offset,
                is_hovered=guide_is_hovered,
            )
            #
            i_name_text = i_item._name_text
            painter._draw_text_by_rect_(
                rect=i_item._name_draw_rect,
                text=i_name_text,
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                font=get_font(size=self.NAME_FONT_SIZE),
                offset=name_offset,
                is_hovered=guide_is_hovered,
            )

        if self._delete_draw_is_enable is True:
            if self._get_guide_path_text_() is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._delete_icon_draw_rect,
                    file_path=self._delete_icon_file_path,
                    is_hovered=self._delete_is_hovered
                )

    def _update_guide_current_(self, event):
        p = event.pos()
        #
        self._delete_is_hovered = False
        self._clear_guide_choose_current_()
        self._clear_guide_current_()
        if self._delete_action_rect.contains(p):
            self._delete_is_hovered = True
        else:
            # choose or press
            for i_index in self._get_guide_item_indices_():
                i_item = self._get_guide_item_at_(i_index)
                # popup choose
                if i_item._icon_frame_draw_rect.contains(p) is True:
                    self._set_guide_choose_current_index_(i_index)
                    break
                # execute press
                elif i_item._name_frame_draw_rect.contains(p) is True:
                    self._set_guide_current_index_(i_index)
                    break
            #
            if self._guide_choose_index_current is not None:
                self._set_tool_tip_text_(
                    'LMB-click to popup a choose frame'
                )
            elif self._guide_index_current is not None:
                self._set_tool_tip_text_(
                    (
                        '1, "LMB-click" to jump to current\n'
                        '2, "MMB-wheel" to jump to previous or next'
                    )
                )
            else:
                self.setToolTip('')
        #
        self._refresh_widget_draw_()

    def _execute_action_guide_choose_wheel_(self, event):
        index = self._guide_index_current-1
        delta = event.angleDelta().y()
        name_texts = self._get_guide_child_name_texts_at_(index)
        name_text_pre = self._get_guide_name_text_at_(index+1)
        maximum = len(name_texts)-1
        if name_text_pre in name_texts:
            pre_index = name_texts.index(name_text_pre)
            if delta > 0:
                cur_index = pre_index-1
            else:
                cur_index = pre_index+1
            #
            cur_index = max(min(cur_index, maximum), 0)
            if cur_index != pre_index:
                name_text_cur = name_texts[cur_index]
                path_text_cur = self._set_guide_name_text_at_(name_text_cur, index)
                # press
                self.guide_text_press_accepted.emit(path_text_cur)

    def _get_guide_path_text_(self):
        item = self._get_guide_item_at_(-1)
        if item:
            return item._path_text

    def _set_guide_path_text_(self, path):
        self._clear_all_guide_items_()
        #
        path_opt = bsc_core.DccPathDagOpt(path)
        components = path_opt.get_components()
        if components:
            components.reverse()
            for i_index, i_path_opt in enumerate(components):
                i_item = self._create_guide_item_()
                #
                if self._guide_type_texts:
                    i_type_text = self._guide_type_texts[i_index]
                else:
                    i_type_text = None
                #
                i_path_text = i_path_opt.get_path()
                i_name_text = i_path_opt.get_name()
                #
                i_item._set_type_text_(i_type_text)
                i_item._set_path_text_(i_path_text)
                i_item._set_name_text_(i_name_text)
        #
        self._refresh_guide_draw_geometry_()
        self._refresh_widget_draw_()


class QtGuideBar(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
    utl_gui_qt_abstract.AbsQtCompletionExtraDef,
):
    QT_VALUE_ENTRY_CLS = _utl_gui_qt_wgt_entry_base.QtEntryAsTextEdit
    QT_POPUP_COMPLETION_CLS = _utl_gui_qt_wgt_popup.QtPopupForCompletion

    QT_POPUP_PROXY_CLS = _utl_gui_qt_wgt_popup.QtPopupProxy

    FILTER_MAXIMUM = 50
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtGuideBar, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self._init_value_entry_extra_def_(self)
        self._init_completion_extra_def_(self)

        self._guide_entry_mode = 0

        qt_layout_0 = QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)
        qt_layout_0.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self._value_entry_frame = _utl_gui_qt_wgt_entry_base.QtEntryFrame()
        qt_layout_0.addWidget(self._value_entry_frame)
        #
        self._value_entry_frame.setMinimumHeight(24)
        self._value_entry_frame.setMaximumHeight(24)

        self._value_entry_layout = QtHBoxLayout(self._value_entry_frame)
        self._value_entry_layout.setContentsMargins(2, 0, 2, 0)
        self._value_entry_layout.setSpacing(2)

        self._guide_tree_button = _utl_gui_qt_wgt_utility.QtIconPressButton()
        self._value_entry_layout.addWidget(self._guide_tree_button)
        self._guide_tree_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('tree'))

        self._guide_entry = QtGuideEntry()
        self._value_entry_layout.addWidget(self._guide_entry)

        self._guide_entry.entry_started.connect(
            self._guide_entry_started_cbk_
        )
        self._value_entry = self.QT_VALUE_ENTRY_CLS()
        self._value_entry.hide()
        self._value_entry_layout.addWidget(self._value_entry)
        # self._value_entry.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._value_entry.key_escape_pressed.connect(self._guide_entry_finished_cbk_)
        self._value_entry.focus_out.connect(self._set_guide_entry_finish_)
        self._value_entry.setMinimumHeight(22)
        self._value_entry.setMaximumHeight(22)
        self._value_entry.setFont(get_font(size=10))
        #
        self._build_completion_extra_(self._value_entry, self._value_entry_frame)

        self._set_completion_extra_gain_fnc_(
            self._guide_value_completion_extra_gain_fnc_
        )
        self.user_completion_text_accepted.connect(self._guide_entry_cbk_)

    def _set_guide_entry_started_(self):
        self._guide_entry_mode = 1
        self._guide_entry.hide()
        self._value_entry.show()

    def _guide_entry_started_cbk_(self):
        self._guide_entry_mode = 1
        self._guide_entry.hide()
        self._value_entry.show()
        self._value_entry._set_value_(self._guide_entry._get_guide_path_text_())
        self._value_entry._set_focused_(True)
        self._value_entry._set_all_selected_()

    def _set_guide_entry_finish_(self):
        self._guide_entry_mode = 0
        self._value_entry.hide()
        self._guide_entry.show()

    def _guide_entry_finished_cbk_(self):
        self._set_guide_entry_finish_()
        self._guide_entry._set_focused_(True)
    # noinspection PyUnusedLocal
    def _guide_value_completion_extra_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            if isinstance(keyword, six.text_type):
                keyword = keyword.encode('utf-8')
            #
            path_texts = self._guide_entry._get_guide_valid_path_texts_()
            _ = fnmatch.filter(
                path_texts, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def _guide_entry_cbk_(self, text):
        path_text_cur = text
        if path_text_cur:
            path_texts = self._guide_entry._get_guide_valid_path_texts_()
            if path_text_cur in path_texts:
                path_text_pre = self._guide_entry._get_guide_path_text_()
                if path_text_cur != path_text_pre:
                    self._guide_entry._set_guide_path_text_(path_text_cur)
                    # press
                    self._guide_entry.guide_text_press_accepted.emit(path_text_cur)
                    # any
                    self._guide_entry.guide_text_accepted.emit(path_text_cur)
                self._guide_entry_finished_cbk_()


class QtTagEntry(object):
    pass


class QtTagBar(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtValueEntryExtraDef,
):
    def __init__(self, *args, **kwargs):
        super(QtTagBar, self).__init__(*args, **kwargs)
