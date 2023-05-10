# coding=utf-8
import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui import utl_gui_configure, utl_gui_core


class QtItemDelegate(QtWidgets.QItemDelegate):
    def sizeHint(self, option, index):
        size = super(QtItemDelegate, self).sizeHint(option, index)
        size.setHeight(utl_gui_configure.Size.ITEM_HEIGHT)
        return size


class QtWidget(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtStatusDef
):
    def __init__(self, *args, **kwargs):
        super(QtWidget, self).__init__(*args, **kwargs)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        #
        self.setAutoFillBackground(True)
        #
        self._set_status_def_init_()

    def _refresh_widget_draw_(self):
        self.update()

    def paintEvent(self, event):
        if self._get_status_is_enable_() is True:
            painter = QtPainter(self)
            #
            color, hover_color = self._get_border_color_by_validator_status_(self._status)
            border_color = color
            pox_x, pos_y = 0, 0
            width, height = self.width(), self.height()
            frame_rect = QtCore.QRect(
                pox_x+1, pos_y+1, width-2, height-2
            )
            #
            painter._draw_focus_frame_by_rect_(
                frame_rect,
                border_color=border_color,
                background_color=(0, 0, 0, 0),
                border_width=2,
            )


class QtLine(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
):
    def __init__(self, *args, **kwargs):
        super(QtLine, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._set_frame_def_init_()

        r, g, b = 119, 119, 119
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        self._frame_background_color = 0, 0, 0, 0

        self._line_draw_is_enable = False
        self._line_draw_offset_x, self._line_draw_offset_y = 1, 2

        self._set_action_press_def_init_()
        self._set_action_press_def_init_()

    def _refresh_widget_draw_(self):
        self.update()

    def _set_line_draw_enable_(self, boolean):
        self._line_draw_is_enable = boolean

    def _set_line_draw_offset_x_(self, x):
        self._line_draw_offset_x = x

    def paintEvent(self, event):
        painter = QtPainter(self)

        offset = [0, 1][self._is_pressed]
        o_x, o_y = self._line_draw_offset_x, self._line_draw_offset_y
        x, y = o_x+offset, o_y+offset
        w, h = self.width()-o_x*2-offset, self.height()-o_y*2-offset
        rect = QtCore.QRect(x, y, w, h)
        if self._line_draw_is_enable is True:
            painter._draw_line_by_points_(
                point_0=rect.topLeft(),
                point_1=rect.bottomLeft(),
                border_color=self._frame_border_color,
            )


class QtLineWidget(QtWidgets.QWidget):
    class Style(object):
        Null = 0x00
        Solid = 0x01

    def __init__(self, *args, **kwargs):
        super(QtLineWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        # top, bottom, left, right
        self._line_styles = [self.Style.Null]*4
        self._lines = [QtCore.QLine(), QtCore.QLine(), QtCore.QLine(), QtCore.QLine()]
        self._line_border_color = QtBorderColors.Light

    def _set_line_styles_(self, line_styles):
        self._line_styles = line_styles

    def _update_line_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        t_l, b_l, l_l, r_l = self._lines
        # top
        t_l.setP1(QtCore.QPoint(x, y+1))
        t_l.setP2(QtCore.QPoint(x+w, y+1))
        # bottom
        b_l.setP1(QtCore.QPoint(x, y+h-1))
        b_l.setP2(QtCore.QPoint(x+w, y+h-1))
        # left
        l_l.setP1(QtCore.QPoint(x+1, y))
        l_l.setP2(QtCore.QPoint(x+1, y+h))
        # right
        r_l.setP1(QtCore.QPoint(x+w-1, y))
        r_l.setP2(QtCore.QPoint(x+w-1, y+h))

    def resizeEvent(self, event):
        self._update_line_geometry_()

    def paintEvent(self, event):
        painter = QtPainter(self)
        painter.setRenderHints(
            painter.Antialiasing
        )
        for seq, i in enumerate(self._line_styles):
            i_line = self._lines[seq]
            painter._set_border_color_(self._line_border_color)
            # painter._set_border_width_(2)
            if i == self.Style.Solid:
                painter.drawLine(i_line)


class _QtTranslucentWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtTranslucentWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def _set_visible_(self, boolean):
        self.setVisible(boolean)


class QtPressButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(QtPressButton, self).__init__(*args, **kwargs)
        self.setFont(Font.NAME)
        self.setPalette(QtDccMtd.get_palette())
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
        self.setPalette(QtDccMtd.get_palette())
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
        self.setPalette(QtDccMtd.get_palette())
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
                    if isinstance(icon_name, six.string_types):
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
                    elif isinstance(method_args, six.string_types):
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
                        if isinstance(i_icon_name, six.string_types):
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
        elif isinstance(execute_fnc, six.string_types):
            cmd_str = execute_fnc
            widget_action.triggered.connect(lambda *args, **kwargs: cls._set_cmd_run_(cmd_str))


class _QtInfoFrame(QtWidgets.QWidget):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtInfoFrame, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        #
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.setFont(get_font(size=12, italic=True))

        self._info_text = ''

        self._info_draw_rect = QtCore.QRect()
        self._info_draw_size = 160, 32

    def _refresh_widget_geometry_(self, x, y, w, h):
        self.setGeometry(
            x, y, w, h
        )
        self._refresh_widget_draw_()

    def _set_info_text_(self, text):
        self._info_text = text
        if text:
            self.show()
            self._refresh_widget_draw_()
        else:
            self.hide()

    def _clear_(self):
        self._set_info_text_('')

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._info_text:
            rect = self.rect()

            painter._draw_frame_by_rect_(
                rect=rect,
                border_color=QtBorderColors.Transparent,
                background_color=QtBackgroundColors.ToolTip,
                border_radius=1
            )
            painter._draw_text_by_rect_(
                rect=self.rect(),
                text=self._info_text,
                font=self.font(),
                font_color=QtFontColors.ToolTip,
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            )


class QtAction(QtWidgets.QAction):
    def __init__(self, *args, **kwargs):
        super(QtAction, self).__init__(*args, **kwargs)
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        #
        self.setFont(Font.NAME)


class QtLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(QtLabel, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_palette())
        #
        self.setFont(Font.NAME)


class QtHScrollArea(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super(QtHScrollArea, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWidgetResizable(True)
        widget = QtWidget()
        self.setWidget(widget)
        self._layout = QtHBoxLayout(widget)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(*[0]*4)
        self._layout.setSpacing(Util.LAYOUT_SPACING)
        #
        qt_palette = QtDccMtd.get_palette()
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

    def keyPressEvent(self, event):
        pass


class QtVScrollArea(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super(QtVScrollArea, self).__init__(*args, **kwargs)
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
        qt_palette = QtDccMtd.get_palette()
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

    def keyPressEvent(self, event):
        pass


class QtThreadDef(object):
    def _set_thread_def_init_(self):
        pass

    def _set_thread_create_(self):
        return QtMethodThread(self)


class QtIconPressItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtStatusDef,
    utl_gui_qt_abstract.AbsQtStateDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
):
    clicked = qt_signal()
    db_clicked = qt_signal()
    #
    QT_MENU_CLASS = QtMenu
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        frm_w, frm_h = w, h
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_frm_m_w, icn_frm_m_h = (frm_w-icn_frm_w)/2, (frm_h-icn_frm_h)/2
        #
        icn_w, icn_h = int(icn_frm_w*self._icon_file_draw_percent), int(icn_frm_h*self._icon_file_draw_percent)
        i_c_w, i_c_h = self._icon_color_draw_size
        i_n_w, i_n_h = self._icon_name_draw_size
        # check
        c_w, c_h = w, h
        c_x, c_y = x, y
        if self._icon_is_enable is True:
            self._set_icon_frame_draw_rect_(
                c_x+icn_frm_m_w, c_y+icn_frm_m_h, icn_frm_w, icn_frm_h
            )
            if self._icon_file_path is not None:
                if self._sub_icon_file_path is not None:
                    frm_x, frm_y = c_x+(frm_w-icn_frm_w)/2, c_y+(frm_h-icn_frm_h)/2
                    sub_icn_w, sub_icn_h = icn_frm_w*self._sub_icon_file_draw_percent, icn_frm_h*self._sub_icon_file_draw_percent
                    self._icon_file_draw_rect.setRect(
                        frm_x+icn_frm_m_w, frm_y+icn_frm_m_h, icn_w, icn_h
                    )
                    self._sub_icon_file_draw_rect.setRect(
                        frm_x+frm_w-sub_icn_w-icn_frm_m_w, frm_y+frm_h-sub_icn_h-icn_frm_m_h, sub_icn_w, sub_icn_h
                    )
                else:
                    self._icon_file_draw_rect.setRect(
                        c_x+(frm_w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
                    )

            self._icon_color_draw_rect.setRect(
                c_x+(icn_frm_w-i_c_w)/2, c_y+(icn_frm_h-i_c_h)/2, i_c_w, i_c_h
            )
            self._icon_name_draw_rect.setRect(
                c_x+(icn_frm_w-i_n_w)/2, c_y+(icn_frm_h-i_n_h)/2, i_n_w, i_n_h
            )
            c_x += icn_frm_h
            c_w -= icn_frm_w

        s_w, s_h = w*.5, w*.5
        self._action_state_rect.setRect(
            x, y+h-s_h, s_w, s_h
        )

    def __init__(self, *args, **kwargs):
        super(QtIconPressItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(Font.NAME)
        self.setMaximumSize(20, 20)
        self.setMinimumSize(20, 20)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_name_def_()
        self._init_icon_def_()
        self._init_menu_def_()
        self._set_status_def_init_()
        self._set_state_def_init_()
        #
        self._init_action_def_(self)
        self._init_action_hover_def_()
        self._set_action_press_def_init_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                self._set_action_hover_filter_execute_(event)
                #
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_pressed_(True)
                        self._set_action_flag_(self.ActionFlag.PressClick)
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_pressed_(True)
                        self.db_clicked.emit()
                        self._set_action_flag_(self.ActionFlag.PressDbClick)
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if event.button() == QtCore.Qt.LeftButton:
                        if self._get_action_press_flag_is_click_() is True:
                            self.clicked.emit()
                            self.press_clicked.emit()
                            self._set_menu_show_()
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                    #
                    self._set_action_hovered_(False)
                    self._set_pressed_(False)
                    self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        self._refresh_widget_draw_geometry_()

        offset = self._get_action_offset_()
        # icon
        if self._icon_is_enable is True:
            if self._icon_file_path is not None:
                icon_file_path = self._icon_file_path
                if self._action_is_hovered is True:
                    if self._hover_icon_file_path is not None:
                        icon_file_path = self._hover_icon_file_path
                #
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_file_draw_rect,
                    file_path=icon_file_path,
                    offset=offset,
                    is_hovered=self._action_is_hovered
                )
            elif self._icon_color_rgb is not None:
                painter._set_color_icon_draw_(
                    self._icon_color_draw_rect,
                    self._icon_color_rgb,
                    offset=offset
                )
            elif self._icon_name_text is not None:
                painter._draw_icon_with_name_text_by_rect_(
                    self._icon_name_draw_rect,
                    self._icon_name_text,
                    offset=offset,
                    border_radius=2,
                    is_hovered=self._action_is_hovered
                )
            #
            if self._sub_icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._sub_icon_file_draw_rect,
                    file_path=self._sub_icon_file_path,
                    offset=offset,
                    is_hovered=self._action_is_hovered
                )
        #
        if self._action_state in [self.ActionState.Disable]:
            painter._draw_icon_file_by_rect_(
                self._action_state_rect,
                utl_gui_core.RscIconFile.get('state-disable')
            )

    def _set_visible_(self, boolean):
        self.setVisible(boolean)


class QtMainWindow(
    QtWidgets.QMainWindow,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtWaitingDef,
    QtThreadDef
):
    close_clicked = qt_signal()
    key_escape_pressed = qt_signal()
    key_help_pressed = qt_signal()
    size_changed = qt_signal()
    window_activate_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtMainWindow, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #
        self.setPalette(QtDccMtd.get_palette())
        self.setAutoFillBackground(True)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setFont(Font.NAME)
        #
        set_shadow(self, radius=2)
        #
        self._init_icon_def_()
        self._window_system_tray_icon = None
        self._init_waiting_def_(self)
    #
    def _refresh_widget_draw_(self):
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
                    #
                    # if isinstance(self.parent(), QtWindowForClarisse):
                    #     self.parent().close()
                    #     self.parent().deleteLater()
                elif event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_Escape:
                        self.key_escape_pressed.emit()
                elif event.type() == QtCore.QEvent.Resize:
                    self.size_changed.emit()
                elif event.type() == QtCore.QEvent.WindowActivate:
                    self.window_activate_changed.emit()
                elif event.type() == QtCore.QEvent.WindowDeactivate:
                    self.window_activate_changed.emit()
        return False

    def _set_size_changed_connect_to_(self, fnc):
        self.size_changed.connect(fnc)

    def _set_close_(self):
        self.close()
        self.deleteLater()

    def _set_close_later_(self, time):
        close_timer = QtCore.QTimer(self)
        close_timer.timeout.connect(self._set_close_)
        close_timer.start(time)

    def _create_window_shortcut_action_(self, fnc, shortcut):
        action = QtWidgets.QAction(self)
        action.triggered.connect(fnc)
        action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.addAction(action)


class QtDialog(
    QtWidgets.QDialog,
    utl_gui_qt_abstract.AbsQtStatusDef,
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
        qt_palette = QtDccMtd.get_palette()
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
    def _refresh_widget_draw_(self):
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
        self._icon_file_draw_size = QtCore.QSize(20, 20)

    def _draw_for_hover_(self, painter, option, index):
        if option.state & QtWidgets.QStyle.State_MouseOver:
            if index.column() == 0:
                rect = option.rect
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                hover_rect = QtCore.QRect(
                    x, y, 4, h
                )
                painter.fillRect(
                    hover_rect, QtBackgroundColors.Hovered
                )
        elif option.state & QtWidgets.QStyle.State_Selected:
            if index.column() == 0:
                rect = option.rect
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                hover_rect = QtCore.QRect(
                    x, y, 4, h
                )
                painter.fillRect(
                    hover_rect, QtBackgroundColors.Selected
                )

    def _draw_for_keyword_(self, painter, option, index):
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
                        spans = bsc_core.RawTextMtd.find_spans(content, filter_keyword)
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

    def paint(self, painter, option, index):
        super(QtStyledItemDelegate, self).paint(painter, option, index)

        # self._draw_for_hover_(painter, option, index)

    def updateEditorGeometry(self, editor, option, index):
        super(QtStyledItemDelegate, self).updateEditorGeometry(editor, option, index)

    def sizeHint(self, option, index):
        size = super(QtStyledItemDelegate, self).sizeHint(option, index)
        size.setHeight(utl_gui_configure.Size.ITEM_HEIGHT)
        return size


class QtListWidgetStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, *args, **kwargs):
        super(QtListWidgetStyledItemDelegate, self).__init__(*args, **kwargs)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QtProgressBar(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtProgressDef
):
    def __init__(self, *args, **kwargs):
        super(QtProgressBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMaximumHeight(4)
        self.setMinimumHeight(4)
        #
        self._set_progress_def_init_()

    def _refresh_widget_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._get_progress_is_enable_() is True:
            if self._progress_raw:
                cur_rect = None
                w, h = self.width(), self.height()
                w -= 2
                layer_count = len(self._progress_raw)
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(120, .5, 1)
                for layer_index, i in enumerate(self._progress_raw):
                    i_percent, (i_range_start, i_range_end), i_label = i
                    p_w = w*(i_range_end-i_range_start)*i_percent
                    p_h = 2
                    #
                    i_x, i_y = w*i_range_start, (h-p_h)/2
                    i_x += 1
                    i_rect = QtCore.QRect(i_x, i_y, p_w+1, p_h)
                    #
                    i_p = float(layer_index)/float(layer_count)
                    r_1, g_1, b_1 = bsc_core.RawColorMtd.hsv2rgb(120*i_p, .5, 1)
                    i_cur_color = QtGui.QColor(r_1, g_1, b_1, 255)
                    if layer_index == 0:
                        i_pre_color = QtGui.QColor(r, g, b, 255)
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(.5, i_pre_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_background_color = i_gradient_color
                    else:
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(0, QtBackgroundColors.Transparent)
                        i_gradient_color.setColorAt(.5, i_cur_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_gradient_color.setColorAt(1, QtBackgroundColors.Transparent)
                        i_background_color = i_gradient_color
                    #
                    painter._draw_frame_by_rect_(
                        i_rect,
                        border_color=QtBorderColors.Transparent,
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
                    painter._draw_frame_by_rect_(
                        rect,
                        border_color=QtBorderColors.Transparent,
                        background_color=(255, 255, 255, 255),
                        border_radius=1,
                    )


class QtFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QtFileDialog, self).__init__(*args, **kwargs)


class QtListWidgetItem(
    QtWidgets.QListWidgetItem,
    utl_gui_qt_abstract.AbsQtShowForItemDef,
    #
    utl_gui_qt_abstract.AbsQtItemFilterDef,
    #
    utl_gui_qt_abstract.AbsQtStateDef,
    #
    utl_gui_qt_abstract.AbsQtDagDef,
    utl_gui_qt_abstract.AbsQtVisibleDef,
    #
    utl_gui_qt_abstract.AbsQtItemVisibleConnectionDef,
):
    def __init__(self, *args, **kwargs):
        super(QtListWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        )
        self._set_show_for_item_def_init_(self)
        #
        self._visible_tgt_key = None
        self._set_item_filter_def_init_()
        #
        self._set_state_def_init_()
        #
        self._set_dag_def_init_()
        self._set_visible_def_init_()
        #
        self._set_item_visible_connection_def_init_()

        self._signals = QtItemSignals()

        self._is_checked = False

    def setData(self, role, value):
        if role == QtCore.Qt.CheckStateRole:
            pass
        #
        super(QtListWidgetItem, self).setData(role, value)

    def _set_checked_(self, boolean):
        self._is_checked = boolean
        #
        self._signals.check_clicked.emit(self, 0)
        self._signals.check_toggled.emit(self, 0, boolean)

    def _set_checked_for_user_(self, boolean):
        self._set_checked_(boolean)
        self.listWidget().item_checked.emit(self, 0)

    def _get_is_checked_(self):
        return self._is_checked

    def _get_item_is_hidden_(self):
        return self.isHidden()

    def _refresh_widget_draw_(self):
        item_widget = self._get_item_widget_()
        if item_widget is not None:
            item_widget.update()

    def _set_item_widget_(self, widget):
        list_widget = self.listWidget()
        list_widget.setItemWidget(self, widget)

    def _get_item_widget_(self):
        list_widget = self.listWidget()
        return list_widget.itemWidget(self)

    def _set_visible_tgt_key_(self, key):
        self._visible_tgt_key = key

    def _get_visible_tgt_key_(self):
        return self._visible_tgt_key

    def _set_item_show_connect_(self):
        self._set_item_show_def_setup_(self.listWidget())
    # def _get_keyword_filter_keys_tgt_(self):
    #     item_widget = self._get_item_widget_()
    #     if item_widget is not None:
    #         item_widget._get_name_texts_()
    #     return []
    # show
    def _set_view_(self, widget):
        self._list_widget = widget

    def _get_view_(self):
        return self.listWidget()

    def _get_item_is_viewport_showable_(self):
        item = self
        view = self.listWidget()
        #
        self._set_item_show_start_loading_()
        return view._get_view_item_viewport_showable_(item)

    def _set_item_widget_visible_(self, boolean):
        item_widget = self._get_item_widget_()
        if item_widget is not None:
            self._get_item_widget_().setVisible(boolean)


class _QtHItem(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtIndexDef,
    utl_gui_qt_abstract.AbsQtTypeDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtNamesDef,
    utl_gui_qt_abstract.AbsQtPathDef,
    utl_gui_qt_abstract.AbsQtImageDef,
    #
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtDeleteDef,
    # action
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
    utl_gui_qt_abstract.AbsQtActionCheckDef,
    utl_gui_qt_abstract.AbsQtActionSelectDef,
    #
    utl_gui_qt_abstract.AbsQtItemFilterDef,
):
    delete_press_clicked = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtHItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self._set_frame_def_init_()
        self._set_index_def_init_()
        self._init_type_def_()
        self._init_icon_def_()
        self._init_name_def_()
        self._set_names_def_init_()
        self._set_path_def_init_()
        self._set_image_def_init_()
        #
        self._init_menu_def_()
        #
        self._set_delete_def_init_(self)
        #
        self._init_action_hover_def_()
        self._init_action_def_(self)
        self._set_action_press_def_init_()
        self._init_action_check_def_(self)
        self._check_icon_file_path_0 = utl_gui_core.RscIconFile.get('filter_unchecked')
        self._check_icon_file_path_1 = utl_gui_core.RscIconFile.get('filter_checked')
        self._refresh_check_draw_()
        self._set_action_select_def_init_()
        #
        self._set_item_filter_def_init_()
        #
        self._frame_background_color = QtBackgroundColors.Light

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_action_hovered_(True)
            elif event.type() == QtCore.QEvent.Leave:
                self._set_action_hovered_(False)
                self._check_is_hovered = False
                self._delete_is_hovered = False
            elif event.type() == QtCore.QEvent.Resize:
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                elif event.button() == QtCore.Qt.LeftButton:
                    if self._delete_is_hovered:
                        pass
                    else:
                        self.clicked.emit()
                #
                self._action_is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._delete_is_hovered is True:
                        self.delete_press_clicked.emit()
                    elif self._check_is_hovered is True:
                        self.check_clicked.emit()
                        self._set_action_check_execute_(event)
                    else:
                        self.press_clicked.emit()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._execute_action_hover_(event)
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()

        offset = self._get_action_offset_()
        #
        background_color = painter._get_item_background_color_by_rect_(
            self._frame_draw_rect,
            is_hovered=self._action_is_hovered,
            is_selected=self._is_selected
        )
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=background_color,
            border_radius=2
        )
        # check
        if self._check_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._check_icon_draw_rect,
                file_path=self._check_icon_file_path_current,
                offset=offset,
                # frame_rect=self._check_action_rect,
                is_hovered=self._check_is_hovered
            )
        # icon
        if self._icon_name_text is not None:
            painter._draw_icon_with_name_text_by_rect_(
                self._icon_name_draw_rect,
                self._icon_name_text,
                background_color=background_color,
                offset=offset,
                border_radius=2, border_width=2
            )

        if self._icon_file_path is not None:
            painter._draw_icon_file_by_rect_(
                rect=self._icon_file_draw_rect,
                file_path=self._icon_file_path,
            )
        # image
        if self._image_draw_is_enable is True:
            painter._set_image_data_draw_by_rect_(
                rect=self._image_draw_rect,
                image_data=self._image_data,
                offset=offset,
                text=self._name_text
            )
        #
        if self._name_texts:
            for i in self._name_indices:
                painter._draw_text_by_rect_(
                    rect=self._name_draw_rects[i],
                    text=self._name_texts[i],
                    font_color=self._name_color,
                    font=self._name_draw_font,
                    text_option=self._name_text_option,
                    is_hovered=self._action_is_hovered,
                    is_selected=self._is_selected,
                )
        elif self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font_color=self._name_color,
                font=self._name_draw_font,
                text_option=self._name_text_option,
                is_hovered=self._action_is_hovered,
                is_selected=self._is_selected,
            )
        #
        if self._index_text is not None:
            painter._draw_text_by_rect_(
                self._index_rect,
                self._get_index_text_(),
                font_color=self._index_text_color,
                font=self._index_text_font,
                text_option=self._index_text_option
            )
        #
        if self._delete_draw_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._delete_icon_draw_rect,
                file_path=self._delete_icon_file_path,
                offset=offset,
                # frame_rect=self._delete_rect,
                is_hovered=self._delete_is_hovered
            )

    def _execute_action_hover_(self, event):
        p = event.pos()
        self._check_is_hovered = False
        self._delete_is_hovered = False
        if self._check_action_is_enable is True:
            if self._check_action_rect.contains(p):
                self._check_is_hovered = True
        if self._delete_is_enable is True:
            if self._delete_rect.contains(p):
                self._delete_is_hovered = True
        #
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        spacing = 2
        frm_w = frm_h = h
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_frm_m_w, icn_frm_m_h = (frm_w - icn_frm_w)/2, (frm_h - icn_frm_h)/2
        icn_w, icn_h = int(icn_frm_w*self._icon_file_draw_percent), int(icn_frm_h*self._icon_file_draw_percent)
        #
        c_x, c_y = x, y
        c_w, c_h = w, h
        #
        f_x, f_y = x, y
        f_w, f_h = w, h
        # frame
        self._set_icon_frame_draw_rect_(
            c_x+icn_frm_m_w, c_y+icn_frm_m_h, icn_frm_w, icn_frm_h
        )
        # check
        if self._check_is_enable is True:
            self._set_check_action_rect_(
                c_x, c_y+(c_h-icn_frm_h)/2, icn_frm_w, icn_frm_h
            )
            self._set_check_icon_draw_rect_(
                c_x+(icn_frm_w-icn_w)/2, c_y+(c_h-icn_h)/2, icn_w, icn_h
            )
            c_x += icn_frm_w+spacing
            c_w -= icn_frm_w+spacing
            f_x += icn_frm_w+spacing
            f_w -= icn_frm_w+spacing
        # icon
        if self._icon_file_path is not None:
            icn_w, icn_h = self._icon_file_draw_size
            self._set_icon_file_draw_rect_(
                c_x+(icn_frm_w-icn_w)/2, c_y+(c_h-icn_h)/2, icn_w, icn_h
            )
            c_x += icn_frm_w+spacing
            c_w -= icn_frm_w+spacing
        #
        if self._icon_name_text is not None:
            icn_p = self._icon_name_draw_percent
            icn_w, icn_h = c_h*icn_p, c_h*icn_p
            self._set_icon_name_draw_rect_(
                c_x+(c_h-icn_w)/2, c_y+(c_h-icn_h)/2, icn_w, icn_h
            )
            c_x += c_h+spacing
            c_w -= c_h+spacing
        # image
        if self._image_draw_is_enable is True:
            img_p = self._image_draw_percent
            img_w, img_h = c_h*img_p, c_h*img_p
            self._set_image_rect_(
                c_x+(c_h-img_w)/2, c_y+(c_h-img_h)/2, img_w, img_h
            )
            c_x += c_h+spacing
            c_w -= c_h+spacing
        #
        if self._delete_is_enable is True:
            icn_w, icn_h = self._delete_icon_file_draw_size
            self._set_delete_rect_(
                x+w-icn_frm_w, c_y+(c_h-icn_frm_h)/2, icn_frm_w, icn_frm_h
            )
            self._set_delete_draw_rect_(
                x+(icn_frm_w-icn_w)/2+w-icn_frm_w, c_y+(c_h-icn_h)/2, icn_w, icn_h
            )
            c_w -= icn_frm_w+spacing
            f_w -= icn_frm_w+spacing
        #
        self._set_frame_draw_rect_(
            f_x, f_y, f_w, f_h
        )
        #
        self._set_name_draw_rect_(
            c_x, c_y, c_w, c_h
        )
        # name text
        if self._name_indices:
            n_w, n_h = self._name_frame_size
            for i in self._name_indices:
                i_n_x, i_n_y = c_x, c_y+i*n_h
                i_n_w, i_n_h = w, n_h
                self._set_name_text_draw_rect_at_(
                    i_n_x, i_n_y, i_n_w, i_n_h, i
                )
        #
        self._set_index_draw_rect_(
            c_x, c_y, c_w, c_h
        )

    # def _get_name_texts_(self):
    #     return [self._get_name_text_()]

    def _get_is_visible_(self):
        return self.isVisible()


class QtEntryFrame(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtStatusDef,
):
    geometry_changed = qt_signal(int, int, int, int)
    entry_focus_in = qt_signal()
    entry_focus_out = qt_signal()
    entry_focus_changed = qt_signal()
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        # int left， int top， int right， int bottom
        m_l, m_t, m_r, m_b = self._frame_draw_margins

        c = self._entry_count

        frm_x, frm_y = x+m_l+1, y+m_t+1
        frm_w, frm_h = w-m_l-m_r-2, h-m_t-m_b-2
        if c > 1:
            for i in range(c):
                i_widget = self._value_entries[i]
                i_p = i_widget.pos()
                i_r = i_widget.rect()
                i_x, i_y = i_p.x(), i_p.y()
                i_w, i_h = i_r.width(), i_r.height()
                self._frame_draw_rects[i].setRect(
                    i_x, frm_y, i_w, frm_h
                )
        else:
            self._frame_draw_rects[0].setRect(
                frm_x, frm_y, frm_w, frm_h
            )

        if self._resize_handle is not None:
            frm_w, frm_h = 24, 24
            r_x, r_y = x+(w-frm_w), y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )

    def __init__(self, *args, **kwargs):
        super(QtEntryFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._action_is_hovered = False
        self._is_focused = False
        self._entry_count = 1
        #
        self._value_entry = None
        self._value_entries = []
        #
        self._init_name_def_()
        self._set_frame_def_init_()
        self._set_status_def_init_()
        #
        self._frame_border_color = QtBorderColors.Light
        self._hovered_frame_border_color = QtBorderColors.Hovered
        self._selected_frame_border_color = QtBorderColors.Selected
        self._frame_background_color = QtBackgroundColors.Dim

        self._resize_handle = QtVResizeHandle(self)
        self._resize_handle.hide()
        # self._resize_handle._set_resize_target_(self)
    # resize
    def _get_resize_handle_(self):
        return self._resize_handle

    def _set_resize_enable_(self, boolean):
        self._resize_handle.setVisible(boolean)

    def _set_resize_minimum_(self, value):
        self._resize_handle._set_resize_minimum_(value)

    def _set_resize_target_(self, widget):
        self._resize_handle._set_resize_target_(widget)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
                self.geometry_changed.emit(
                    self.x(), self.y(), self.width(), self.height()
                )
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        is_hovered = self._action_is_hovered
        is_selected = self._is_focused
        background_color = self._frame_background_color
        bdr_color = [QtBorderColors.Basic, QtBorderColors.HighLight][is_selected]
        bdr_w = [1, 2][is_selected]
        for i_rect in self._frame_draw_rects:
            painter._draw_frame_by_rect_(
                i_rect,
                border_color=bdr_color,
                background_color=background_color,
                # border_radius=1,
                border_width=bdr_w,
            )

    def _update_background_color_by_locked_(self, boolean):
        self._frame_background_color = [
            QtBackgroundColors.Basic, QtBackgroundColors.Dim
        ][boolean]

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self._refresh_widget_draw_()
        self.entry_focus_changed.emit()

    def _set_focus_in_(self):
        self._set_focused_(True)
        self.entry_focus_in.emit()

    def set_focus_out_(self):
        self._set_focused_(False)
        self.entry_focus_out.emit()

    def _set_entry_count_(self, size):
        self._entry_count = size
        self._frame_draw_rects = [QtCore.QRect() for i in range(size)]

    def _set_size_policy_height_fixed_mode_(self):
        self._value_entry.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )


class QtHResizeHandle(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtResizeDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
):
    press_clicked = qt_signal()
    size_changed = qt_signal(int)
    resize_stated = qt_signal()
    resize_finished = qt_signal()
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        #
        icn_w, icn_h = self._resize_icon_draw_size
        self._resize_icon_draw_rect.setRect(
            x+(w-icn_w)/2, y+(h-icn_h)/2, icn_w, icn_h
        )

    def __init__(self, *args, **kwargs):
        super(QtHResizeHandle, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        #
        self._set_frame_def_init_()
        self._init_resize_def_(self)

        self._init_action_def_(self)
        self._init_action_hover_def_()
        self._set_action_press_def_init_()
        #
        self._hovered_frame_border_color = QtBorderColors.Button
        self._hovered_frame_background_color = QtBackgroundColors.Button

        self._actioned_frame_border_color = QtBorderColors.Actioned
        self._actioned_frame_background_color = QtBackgroundColors.Actioned

        self.setToolTip(
            '"LMB-move" to resize'
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_action_hovered_(True)
                self._set_action_flag_(
                    [self.ActionFlag.SplitHHover, self.ActionFlag.SplitVHover][self._resize_orientation]
                )
            elif event.type() == QtCore.QEvent.Leave:
                self._set_action_hovered_(False)
                self._set_action_flag_clear_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_action_flag_(
                    [self.ActionFlag.SplitHPess, self.ActionFlag.SplitVPess][self._resize_orientation]
                )
                self._execute_action_resize_move_start_(event)
                self._set_pressed_(True)
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_action_flag_(
                    [self.ActionFlag.SplitHMove, self.ActionFlag.SplitVMove][self._resize_orientation]
                )
                self._execute_action_resize_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._execute_action_resize_move_stop_(event)
                self._set_pressed_(False)
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        painter._draw_icon_file_by_rect_(
            rect=self._resize_icon_draw_rect,
            file_path=self._resize_icon_file_path,
            is_hovered=self._action_is_hovered,
        )

    def _execute_action_resize_move_start_(self, event):
        self._resize_point_start = event.pos()

    def _execute_action_resize_move_(self, event):
        if self._resize_target is not None:
            p = event.pos() - self._resize_point_start
            d_w = p.x()
            w_0 = self._resize_target.minimumWidth()
            if self._resize_alignment == self.ResizeAlignment.Right:
                w_1 = w_0+d_w
            elif self._resize_alignment == self.ResizeAlignment.Left:
                w_1 = w_0-d_w
            else:
                raise RuntimeError()
            if self._resize_minimum+10 <= w_1 <= self._resize_maximum+10:
                self._resize_target.setMinimumWidth(w_1)
                self._resize_target.setMaximumWidth(w_1)
                self.size_changed.emit(w_1)

    def _execute_action_resize_move_stop_(self, event):
        self.resize_finished.emit()


class QtVResizeHandle(QtHResizeHandle):
    press_clicked = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtVResizeHandle, self).__init__(*args, **kwargs)
        self._resize_orientation = self.ResizeOrientation.Vertical

    def _execute_action_resize_move_(self, event):
        if self._resize_target is not None:
            p = event.pos() - self._resize_point_start
            d_h = p.y()
            h_0 = self._resize_target.minimumHeight()
            h_1 = h_0+d_h
            if self._resize_minimum+10 <= h_1 <= self._resize_maximum+10:
                self._resize_target.setMinimumHeight(h_1)
                self._resize_target.setMaximumHeight(h_1)
                self.size_changed.emit(h_1)


class QtHResizeFrame(
    QtWidgets.QWidget,
):
    geometry_changed = qt_signal(int, int, int, int)
    def __init__(self, *args, **kwargs):
        super(QtHResizeFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._resize_handle = QtHResizeHandle(self)
        self._resize_handle._resize_icon_file_paths = [
            utl_gui_core.RscIconFile.get('resize-middle'), utl_gui_core.RscIconFile.get('resize-middle')
        ]
        self._resize_handle._resize_frame_draw_size = 10, 20
        self._resize_handle._resize_icon_draw_size = 8, 16

        self._resize_info_frame = _QtInfoFrame(self)

        self._resize_handle.size_changed.connect(self._set_resize_info_)
        self._resize_handle.resize_finished.connect(self._set_resize_reset_)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self.geometry_changed.emit(
                    self.x(), self.y(), self.width(), self.height()
                )
        return False

    def _set_resize_info_(self, value):
        info = str(value)
        self._resize_info_frame._set_info_text_(info)

        frm_w, frm_h = self._resize_info_frame._info_draw_size
        frm_w = self._resize_info_frame.fontMetrics().width(info)+24
        x, y = 0, 0
        w, h = self.width(), self.height()

        self._resize_info_frame.setGeometry(
            x+(w-frm_w)/2, y+(h-frm_h)/2, frm_w, frm_h
        )
        self._resize_info_frame.raise_()

    def _set_resize_reset_(self):
        self._resize_info_frame._set_info_text_('')

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        if self._resize_handle._resize_alignment == self._resize_handle.ResizeAlignment.Right:
            frm_w, frm_h = 10, 20
            r_x, r_y = x+(w-frm_w), y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )
        elif self._resize_handle._resize_alignment == self._resize_handle.ResizeAlignment.Left:
            frm_w, frm_h = 10, 20
            r_x, r_y = x, y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )
        self._resize_handle.raise_()
    # resize
    def _get_resize_handle_(self):
        return self._resize_handle


class _QtScreenshotFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtScreenshotDef,
    utl_gui_qt_abstract.AbsQtHelpDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionForHoverDef,
    utl_gui_qt_abstract.AbsQtActionForPressDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._frame_draw_rect.setRect(
            x-1, y-1, w+2, h+2
        )

    def __init__(self, *args, **kwargs):
        super(_QtScreenshotFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.Popup
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
        )

        self._set_frame_def_init_()
        self._set_screenshot_def_init_(self)
        self._set_help_def_init_(self)

        self._init_action_def_(self)
        self._init_action_hover_def_()
        self._set_action_press_def_init_()

        self._help_text_draw_size = 480, 240
        self._help_text = (
            u'"LMB-click" and "LMB-move" to create screenshot,\n'
            u'"LMB-double-click" or "Enter Key-press" to accept\n'
            u'"Escape Key-press" to cancel'
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_screenshot_update_geometry_()
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_action_screenshot_press_start_(event)
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                self._set_screenshot_accept_()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._set_action_screenshot_press_execute_(event)
                else:
                    self._set_action_screenshot_hover_execute_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._set_action_screenshot_press_stop_(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                    self._set_screenshot_accept_()
                elif event.key() == QtCore.Qt.Key_Escape:
                    self._set_screenshot_cancel_()
        return False

    def paintEvent(self, event):
        if self._screenshot_mode != self.Mode.Stopped:
            painter = QtPainter(self)

            painter._set_screenshot_draw_by_rect_(
                rect_0=self._frame_draw_rect,
                rect_1=self._screenshot_rect,
                border_color=(63, 127, 255),
                background_color=(0, 0, 0, 127)
            )

            if self._screenshot_mode == self.Mode.Started:
                painter._draw_frame_by_rect_(
                    rect=self._help_frame_draw_rect,
                    border_color=(0, 0, 0),
                    background_color=(0, 0, 0, 127)
                )
                painter._draw_text_by_rect_(
                    rect=self._help_draw_rect,
                    text=self._help_text,
                    font=get_font(12),
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                    word_warp=True
                )


class QtDrag(QtGui.QDrag):
    released = qt_signal(tuple)
    ACTION_MAPPER = {
        QtCore.Qt.IgnoreAction: utl_gui_configure.DragFlag.Ignore,
        QtCore.Qt.CopyAction: utl_gui_configure.DragFlag.Copy,
        QtCore.Qt.MoveAction: utl_gui_configure.DragFlag.Move
    }
    def __init__(self, *args, **kwargs):
        super(QtDrag, self).__init__(*args, **kwargs)
        self.installEventFilter(self)

        self._current_action = QtCore.Qt.IgnoreAction

        self.actionChanged.connect(self._update_action_)

    def _execute_start_(self, point_offset):
        drag = self
        widget = self.parent()

        """
        text/plain ArnoldSceneBake
        nodegraph/nodes ArnoldSceneBake
        nodegraph/noderefs ArnoldSceneBake
        'python/text': 'NodegraphAPI.GetNode('ArnoldSceneBake')',
        python/getParameters NodegraphAPI.GetNode('ArnoldSceneBake').getParameters()
        'python/GetGeometryProducer': 'Nodes3DAPI.GetGeometryProducer(NodegraphAPI.GetNode(\'ArnoldSceneBake\'))',
        'python/GetRenderProducer': Nodes3DAPI.GetRenderProducer(NodegraphAPI.GetNode('ArnoldSceneBake'), useMaxSamples=True)
        """
        #
        w, h = widget.width(), widget.height()
        p = QtGui.QPixmap(w, h)
        p.fill(QtCore.Qt.transparent)
        widget.render(p)
        drag.setPixmap(p)
        drag.setHotSpot(point_offset)
        drag.exec_(QtCore.Qt.CopyAction)

    def _release_(self):
        pass

    def _update_action_(self, *args, **kwargs):
        self._current_action = args[0]

    def _execute_release_(self):
        if self._current_action in self.ACTION_MAPPER:
            self.released.emit(
                (self.ACTION_MAPPER[self._current_action], self.mimeData())
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.DeferredDelete:
                self._execute_release_()
        return False


class QtTreeItemDrag(QtGui.QDrag):
    def __init__(self, *args, **kwargs):
        super(QtTreeItemDrag, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self._item = None
        self._index = 0

    def _execute_release_(self):
        pass

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.DeferredDelete:
                self._execute_release_()
        return False

    def set_item(self, item, point):
        self._item = item

    def _execute_start_(self, point_offset):
        #
        drag = self
        widget = self.parent()
        #
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.BusyCursor
        )
        #
        x, y = 0, 0
        w, h = 48, 20
        name_text = self._item._get_name_text_()
        name_w = widget.fontMetrics().width(name_text)
        w = 20+name_w+10
        pixmap = QtGui.QPixmap(w, h)
        painter = QtPainter(pixmap)
        painter.setFont(
            QtFonts.Button
        )
        icon = self._item.icon(self._index)
        i_f_w, i_f_h = 20, 20
        i_w, i_h = 16, 16
        frame_rect = QtCore.QRect(x, y, w, h)
        painter._draw_frame_by_rect_(
            rect=frame_rect,
            background_color=QtBackgroundColors.Basic,
            border_color=QtBorderColors.Basic,
            border_width=2
        )
        icon_rect = QtCore.QRect(x+(i_f_w-i_w)/2, y+(i_f_h-i_h)/2, i_w, i_h)
        pixmap_ = icon.pixmap(QtCore.QSize(i_w, i_h))
        painter.drawPixmap(icon_rect, pixmap_)
        text_rect = QtCore.QRect(x+i_f_w, y, w-i_f_w, h)
        painter._draw_text_by_rect_(
            rect=text_rect,
            text=name_text,
            font_color=QtFontColors.Basic
        )
        #
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(point_offset)
        drag.exec_(QtCore.Qt.CopyAction)
        #
        QtWidgets.QApplication.restoreOverrideCursor()
