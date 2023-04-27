# coding=utf-8
import six

import collections

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
    utl_gui_qt_abstract.AbsQtActionPressDef,
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


class QtIconButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(QtIconButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setPalette(QtDccMtd.get_palette())
        #
        self.setFont(Font.NAME)
        self.setMaximumSize(20, 20)
        self.setMinimumSize(20, 20)
        #
        self._icon_file_path = None
        self._icon_color_rgb = None
        #
        self._icon_file_draw_size = 16, 16
        self._icon_color_draw_size = 8, 8
        self._frame_size = 20, 20
        self._action_is_hovered = False
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
                self._action_is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._action_is_hovered = False
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._action_is_hovered = True
                self._set_menu_show_()
                self.update()
        return False

    def paintEvent(self, event):
        w, h = self.width(), self.height()
        f_w, f_h = self._frame_size
        c_w, c_h = self._icon_file_draw_size
        painter = QtPainter(self)
        #
        f_x, f_y = (w-c_w) / 2, (h-c_h) / 2
        #
        bkg_rect = QtCore.QRect(1, 1, w-1, h-1)
        bkg_color = [QtBackgroundColors.Transparent, QtBackgroundColors.Hovered][self._action_is_hovered]
        painter._draw_frame_by_rect_(
            bkg_rect,
            border_color=bkg_color,
            background_color=bkg_color,
            border_radius=4
        )
        if self._icon_file_path is not None:
            icn = QtCore.QRect(f_x, f_y, c_w, c_h)
            painter._draw_svg_by_rect_(icn, self._icon_file_path)
        elif self._icon_color_rgb is not None:
            pass


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
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
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
        self._set_name_def_init_()
        self._set_icon_def_init_()
        self._set_menu_def_init_()
        self._set_status_def_init_()
        self._set_state_def_init_()
        #
        self._init_action_def_(self)
        self._set_action_hover_def_init_()
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
        self._set_icon_def_init_()

        self._window_system_tray_icon = None
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


class QtLineEdit0(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(QtLineEdit0, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_palette())
        #
        self.setFont(Font.NAME)
        #
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def _set_validator_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())

    def _set_validator_use_as_float_(self):
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
        self.setPalette(QtDccMtd.get_palette())
        #
        self.setFont(Font.NAME)


class QtRadioButton(QtWidgets.QRadioButton):
    def __init__(self, *args, **kwargs):
        super(QtRadioButton, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_palette())
        #
        self.setFont(Font.NAME)


class QtComboBox(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super(QtComboBox, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_palette())
        self.setItemDelegate(QtStyledItemDelegate())
        self.view().setAlternatingRowColors(True)
        self.setFont(Font.NAME)
        #
        self.setLineEdit(QtLineEdit0())


class QtProgressDialog(QtWidgets.QProgressDialog):
    def __init__(self, *args, **kwargs):
        super(QtProgressDialog, self).__init__(*args, **kwargs)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setCancelButton(None)


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


class _AbsQtSplitterHandle(QtWidgets.QWidget):
    QT_ORIENTATION = None
    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitterHandle, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._swap_enable = True
        #
        qt_palette = QtDccMtd.get_palette()
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
        self._contract_l_button._icon_file_draw_size = self._contract_icon_size
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
        self._swap_button._icon_file_draw_size = self._contract_icon_size
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
        self._contract_r_button._icon_file_draw_size = self._contract_icon_size
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
        self._action_is_hovered = False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._action_is_hovered = True
                if self._get_orientation_() == QtCore.Qt.Horizontal:
                    self.setCursor(QtCore.Qt.SplitHCursor)
                elif self._get_orientation_() == QtCore.Qt.Vertical:
                    self.setCursor(QtCore.Qt.SplitVCursor)
                self._set_update_()
            elif event.type() == QtCore.QEvent.Leave:
                self._action_is_hovered = False
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
        self._refresh_widget_draw_geometry_()

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

    def _refresh_widget_draw_geometry_(self):
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
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
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
        self._set_type_def_init_()
        self._set_icon_def_init_()
        self._set_name_def_init_()
        self._set_names_def_init_()
        self._set_path_def_init_()
        self._set_image_def_init_()
        #
        self._set_menu_def_init_()
        #
        self._set_delete_def_init_(self)
        #
        self._set_action_hover_def_init_()
        self._init_action_def_(self)
        self._set_action_press_def_init_()
        self._set_action_check_def_init_()
        self._check_icon_file_path_0 = utl_gui_core.RscIconFile.get('filter_unchecked')
        self._check_icon_file_path_1 = utl_gui_core.RscIconFile.get('filter_checked')
        self._set_check_update_draw_()
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
        self._set_frame_draw_geometry_(
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


class _QtListWidgetForPopup(utl_gui_qt_abstract.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(_QtListWidgetForPopup, self).__init__(*args, **kwargs)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.ListMode)
        self.setPalette(QtDccMtd.get_palette())

    def paintEvent(self, event):
        pass

    def _get_maximum_height_(self, count_maximum, includes=None):
        adjust = 1+8
        if includes is not None:
            rects = [self.visualItemRect(i) for i in includes[:count_maximum]]
        else:
            rects = [self.visualItemRect(self.item(i)) for i in range(self.count())[:count_maximum]]
        if rects:
            return sum([i.height() for i in rects])+adjust
        return 20+adjust


class QtLineEdit_(
    QtWidgets.QLineEdit,
    utl_gui_qt_abstract.AbsQtValueDef,
    #
    utl_gui_qt_abstract.AbsQtEntryBaseDef,
    utl_gui_qt_abstract.AbsQtActionPopupDef,
):
    entry_changed = qt_signal()
    entry_cleared = qt_signal()
    #
    user_entry_changed = qt_signal()
    user_entry_cleared = qt_signal()
    user_entry_finished = qt_signal()
    #
    up_key_pressed = qt_signal()
    down_key_pressed = qt_signal()
    #
    def __init__(self, *args, **kwargs):
        super(QtLineEdit_, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setPalette(QtDccMtd.get_palette())
        self.setFont(Font.NAME)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._value_type = str
        #
        self._item_value_default = None
        #
        self._maximum = 1
        self._minimum = 0
        #
        self.returnPressed.connect(self._send_user_enter_finished_emit_)
        # emit send by setText
        self.textChanged.connect(self._send_enter_changed_emit_)
        # user enter
        self.textEdited.connect(self._send_user_enter_changed_emit_)
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QLineEdit')
        )
        self._set_value_def_init_(self)
        self._set_entry_base_def_init_(self)
        self._init_action_popup_def_(self)
        self.setAcceptDrops(self._action_popup_is_enable)

        # self.setPlaceholderText()

    def _set_entry_tip_(self, text):
        self.setPlaceholderText(text)

    def _execute_action_wheel_(self, event):
        if self._value_type in [int, float]:
            delta = event.angleDelta().y()
            pre_value = self._get_value_()
            if delta > 0:
                self._set_value_(pre_value+1)
            else:
                self._set_value_(pre_value-1)
            #
            self._send_enter_changed_emit_()

    def _execute_action_drop_(self, event):
        data = event.mimeData()
        if data.hasUrls():
            urls = event.mimeData().urls()
            if urls:
                value = urls[0].toLocalFile()
                if self._get_value_is_valid_(value):
                    self._set_value_(value)
                    return True
        return False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(False)
                #
                self._set_value_completion_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._execute_action_wheel_(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Up:
                    self.up_key_pressed.emit()
                if event.key() == QtCore.Qt.Key_Down:
                    self.down_key_pressed.emit()
        return False

    def _set_popup_enable_(self, boolean):
        super(QtLineEdit_, self)._set_popup_enable_(boolean)
        self.setAcceptDrops(boolean)

    def dropEvent(self, event):
        if self._execute_action_drop_(event) is True:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        menu_raw = [
            ('basic', ),
            ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
            ('paste', None, (True, self.paste, False), QtGui.QKeySequence.Paste),
            ('cut', None, (True, self.cut, False), QtGui.QKeySequence.Cut),
            ('extend', ),
            ('undo', None, (True, self.undo, False), QtGui.QKeySequence.Undo),
            ('redo', None, (True, self.redo, False), QtGui.QKeySequence.Redo),
            ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll),
        ]
        #
        if self.isReadOnly():
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('extend', ),
                ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if self._entry_use_as_storage is True:
            menu_raw.extend(
                [
                    ('system',),
                    ('open folder', 'file/folder', (True, self._execute_open_in_system_, False), QtGui.QKeySequence.Open)
                ]
            )
        #
        if menu_raw:
            self._qt_menu = QtMenu(self)
            self._qt_menu._set_menu_raw_(menu_raw)
            self._qt_menu._set_show_()

    def _send_user_enter_finished_emit_(self):
        # noinspection PyUnresolvedReferences
        self.user_entry_finished.emit()

    def _send_enter_changed_emit_(self):
        # noinspection PyUnresolvedReferences
        self.entry_changed.emit()
        text = self.text()
        if not text:
            self.entry_cleared.emit()

    def _send_user_enter_changed_emit_(self):
        # noinspection PyUnresolvedReferences
        self.user_entry_changed.emit()
        text = self.text()
        if not text:
            self.user_entry_cleared.emit()

    def _set_value_completion_(self):
        if self._value_type in [int, float]:
            if not self.text():
                self._set_value_(0)

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        if self._value_type is None:
            pass
        elif self._value_type is str:
            pass
            # self._set_validator_use_as_name_()
        elif self._value_type is int:
            self._set_validator_use_as_integer_()
        elif self._value_type is float:
            self._set_validator_use_as_float_()

    def _get_value_type_(self):
        return self._value_type

    def _execute_open_in_system_(self):
        _ = self.text()
        if _:
            _exist_comp = bsc_core.StgExtraMtd.get_exists_component(_)
            if _exist_comp is not None:
                bsc_core.StgExtraMtd.set_directory_open(
                    _exist_comp
                )

    def _set_validator_use_as_storage_(self, boolean=True):
        super(QtLineEdit_, self)._set_validator_use_as_storage_(boolean)
        if boolean is True:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                self._execute_open_in_system_
            )
            i_action.setShortcut(
                QtGui.QKeySequence.Open
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)

    def _set_validator_use_as_name_(self):
        reg = QtCore.QRegExp(r'^[a-zA-Z0-9_]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #     )
        # )

    def _set_validator_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())
        self._set_value_completion_()
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         '"MMB-wheel" to modify "int" value'
        #     )
        # )

    def _set_validator_use_as_float_(self):
        self.setValidator(QtGui.QDoubleValidator())
        self._set_value_completion_()
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         '"MMB-wheel" to modify "float" value'
        #     )
        # )

    def _set_validator_use_as_frames_(self):
        self._set_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9-,:]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)
        # self.setToolTip(
        #     (
        #         '"LMB-click" to entry\n'
        #         'etc:\n'
        #         '   1\n'
        #         '   1-2\n'
        #         '   1-5,7,50-100,101'
        #     )
        # )

    def _set_validator_use_as_rgba_(self):
        self._set_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9.,]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_value_maximum_(self, value):
        self._maximum = value

    def _get_value_maximum_(self):
        return self._maximum

    def _set_value_minimum_(self, value):
        self._minimum = value

    def _get_value_minimum_(self):
        return self._minimum

    def _set_value_range_(self, maximum, minimum):
        self._set_value_maximum_(maximum), self._set_value_minimum_(minimum)

    def _get_value_range_(self):
        return self._get_value_maximum_(), self._get_value_minimum_()

    def _get_value_(self):
        _ = self.text()
        if self._value_type == str:
            return _
        elif self._value_type == int:
            return int(_)
        elif self._value_type == float:
            return float(_)
        return _

    def _set_value_(self, value):
        pre_value = self.text()
        if value is not None:
            if isinstance(value, six.text_type):
                value = value.encode('utf-8')

            if isinstance(pre_value, six.text_type):
                pre_value = pre_value.encode('utf-8')

            if self._value_type is not None:
                value = self._value_type(value)
            #
            if value != pre_value:
                self.setText(str(value))
                # self._send_enter_changed_emit_()
        else:
            self.setText('')

    def _get_value_default_(self):
        return self._item_value_default

    def _connect_focused_to_(self, widget):
        pass
    #
    def _get_is_selected_(self):
        boolean = False
        if self.selectedText():
            boolean = True
        return boolean

    def _set_value_clear_(self):
        self._set_value_('')

    def _set_enter_enable_(self, boolean):
        self.setReadOnly(not boolean)

    def _set_focused_(self, boolean):
        if boolean is True:
            self.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self.setFocus(
                QtCore.Qt.NoFocusReason
            )

    def _set_clear_(self):
        self.clear()


class QtPopupChooseFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    def __init__(self, *args, **kwargs):
        super(QtPopupChooseFrame, self).__init__(*args, **kwargs)
        # use popup,
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_frame_def_init_()
        self._set_popup_def_init_(self)
        #
        self._popup_item_width, self._popup_item_height = 20, 20
        self._popup_tag_filter_item_width, self._popup_tag_filter_item_height = 20, 20
        #
        self._popup_close_button = QtIconPressItem(self)
        self._popup_close_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('close'))
        self._popup_close_button._set_icon_frame_draw_size_(18, 18)
        self._popup_close_button.press_clicked.connect(self._close_popup_)
        self._popup_close_button.setToolTip(
            '"LMB-click" to close'
        )
        #
        self._popup_multiply_is_enable = False
        self._popup_all_checked_button = QtIconPressItem(self)
        self._popup_all_checked_button.hide()
        self._popup_all_checked_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_checked'))
        self._popup_all_checked_button._set_icon_frame_draw_size_(18, 18)
        self._popup_all_checked_button.setToolTip(
            '"LMB-click" to checked all'
        )
        self._popup_all_checked_button.press_clicked.connect(self._execute_popup_all_checked_)
        #
        self._popup_all_unchecked_button = QtIconPressItem(self)
        self._popup_all_unchecked_button.hide()
        self._popup_all_unchecked_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_unchecked'))
        self._popup_all_unchecked_button._set_icon_frame_draw_size_(18, 18)
        self._popup_all_unchecked_button.setToolTip(
            '"LMB-click" to unchecked all'
        )
        self._popup_all_unchecked_button.press_clicked.connect(self._execute_popup_all_unchecked_)
        # keyword filter
        self._keyword_filter_is_enable = False
        self._keyword_filter_line_edit = QtLineEdit_(self)
        self._keyword_filter_line_edit.hide()
        self._keyword_filter_line_edit._set_entry_enable_(True)
        self._keyword_filter_line_edit.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self._keyword_filter_line_edit.installEventFilter(self)
        # tag filter
        self._tag_filter_is_enable = False
        self._tag_filter_width_percent = 0.375
        self._tag_filter_draw_rect = QtCore.QRect()
        self._tag_filter_list_widget = _QtListWidgetForPopup(self)
        self._tag_filter_list_widget.hide()
        self._tag_filter_list_widget.setGridSize(
            QtCore.QSize(self._popup_item_width, self._popup_item_height)
        )
        self._tag_filter_list_widget.setSpacing(2)
        self._tag_filter_list_widget.setUniformItemSizes(True)
        #
        self._item_list_widget = _QtListWidgetForPopup(self)
        #
        self._item_count_maximum = 10
        self._item_list_widget.setGridSize(
            QtCore.QSize(self._popup_item_width, self._popup_item_height)
        )
        self._item_list_widget.setSpacing(2)
        self._item_list_widget.setUniformItemSizes(True)
        #
        self._choose_index = None
        #
        self._frame_border_color = QtBackgroundColors.Light
        self._hovered_frame_border_color = QtBackgroundColors.Hovered
        self._selected_frame_border_color = QtBackgroundColors.Hovered
        #
        self._frame_background_color = QtBackgroundColors.Dark

        self._read_only_mark = None

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
            # border_radius=4
        )
        painter._draw_line_by_points_(
            point_0=self._popup_toolbar_draw_rect.bottomLeft(),
            point_1=self._popup_toolbar_draw_rect.bottomRight(),
            border_color=self._frame_border_color,
        )
        if self._keyword_filter_is_enable is True:
            if not self._keyword_filter_line_edit.text():
                painter._draw_text_by_rect_(
                    self._popup_toolbar_draw_tool_tip_rect,
                    'entry keyword to filter ...',
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
                self._keyword_filter_line_edit.inputMethodEvent(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self._close_popup_()
                else:
                    self._keyword_filter_line_edit.keyPressEvent(event)
        return False

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
        tbr_w = c_w
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
        self._keyword_filter_line_edit.setGeometry(
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

        self._item_list_widget.setGeometry(
            c_x+1, c_y+1, c_w-2, c_h-2
        )
        self._item_list_widget.updateGeometries()

    def _set_popup_keyword_filter_enable_(self, boolean):
        self._keyword_filter_is_enable = boolean
        self._keyword_filter_line_edit.show()
        self._keyword_filter_line_edit.entry_changed.connect(
            self._execute_popup_filter_
        )

    def _set_popup_tag_filter_enable_(self, boolean):
        self._tag_filter_is_enable = boolean
        self._tag_filter_list_widget.show()
        self._tag_filter_list_widget.itemSelectionChanged.connect(
            self._execute_popup_filter_
        )

    def _set_popup_multiply_enable_(self, boolean):
        self._popup_multiply_is_enable = boolean

    def _get_popup_multiply_is_enable_(self):
        return self._popup_multiply_is_enable

    def _execute_popup_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._item_list_widget._set_scroll_to_pre_item_()

    def _execute_popup_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._item_list_widget._set_scroll_to_next_item_()

    def _set_popup_item_show_(self, item, item_widget, data):
        def cache_fnc_():
            return data

        def build_fnc_(data_):
            _image_url,  = data_
            item_widget._set_image_url_(_image_url)

        item._set_item_show_fnc_(cache_fnc_, build_fnc_)
        item_widget._set_image_draw_enable_(True)

    def _start_action_popup_(self):
        if self._popup_is_activated is False:
            parent = self.parent()
            self._item_list_widget._set_clear_()
            self._tag_filter_list_widget._set_clear_()
            self._keyword_filter_line_edit._set_clear_()
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
                        i_item_widget = _QtHItem()
                        i_item = QtListWidgetItem()
                        i_item.setSizeHint(QtCore.QSize(self._popup_item_width, self._popup_item_height))
                        #
                        self._item_list_widget.addItem(i_item)
                        self._item_list_widget.setItemWidget(i_item, i_item_widget)
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
                                    i_item_widget._set_icon_name_text_(i_name_text)
                        #
                        if i_name_text in keyword_filter_dict:
                            i_filter_keys = keyword_filter_dict[i_name_text]
                            i_item._set_item_keyword_filter_keys_tgt_update_(i_filter_keys)
                            i_item_widget._set_name_texts_(
                                i_filter_keys
                            )
                            i_item_widget._set_tool_tip_(
                                i_filter_keys
                            )
                        else:
                            i_item._set_item_keyword_filter_keys_tgt_update_([i_name_text])
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
                            self._item_list_widget._set_scroll_to_selected_item_top_()
                        #
                        i_item_widget.press_clicked.connect(self._end_action_popup_)
                    #
                    press_pos = self._get_popup_pos_(self._popup_entry_frame)
                    width, height = self._get_popup_size_(self._popup_entry_frame)
                    height_max = self._item_list_widget._get_maximum_height_(self._item_count_maximum)
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
                    self._item_list_widget._refresh_view_all_items_viewport_showable_()

                    if isinstance(self._popup_entry, QtWidgets.QLineEdit):
                        self._read_only_mark = self._popup_entry.isReadOnly()
                        #
                        self._popup_entry.setReadOnly(True)
                    # tag filter
                    if self._tag_filter_is_enable is True:
                        tags = list(set([i for k, v in tag_filter_dict.items() for i in v]))
                        tags = bsc_core.RawTextsMtd.set_sort_by_initial(tags)
                        for i_tag in tags:
                            i_item_widget = _QtHItem()
                            i_item = QtListWidgetItem()
                            i_item.setSizeHint(QtCore.QSize(self._popup_tag_filter_item_width, self._popup_tag_filter_item_height))
                            #
                            self._tag_filter_list_widget.addItem(i_item)
                            self._tag_filter_list_widget.setItemWidget(i_item, i_item_widget)
                            i_item._set_item_show_connect_()
                            #
                            i_item_widget._set_name_text_(i_tag)
                            i_item_widget._set_icon_name_text_(i_tag)
                            i_item_widget._set_tool_tip_text_(i_tag)
                            #
                            i_item_widget._set_item_tag_filter_keys_src_add_(i_tag)

    def _end_action_popup_(self):
        parent = self.parent()
        selected_item_widgets = self._item_list_widget._get_selected_item_widgets_()
        if selected_item_widgets:
            parent._extend_choose_current_values_(
                [i._get_name_text_() for i in selected_item_widgets]
            )
            #
            if parent._get_choose_multiply_is_enable_() is True:
                checked_item_widgets = self._item_list_widget._get_checked_item_widgets_()
                parent._extend_choose_current_values_([i._get_name_text_() for i in checked_item_widgets])
            #
            parent._send_choose_changed_emit_()
            parent._send_user_choose_changed_emit_()
        #
        self._close_popup_()

    def _set_popup_entry_(self, widget):
        self._popup_entry = widget
        self._popup_entry.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._popup_entry)
        self._keyword_filter_line_edit.setFocusProxy(self._popup_entry)
        self._tag_filter_list_widget.setFocusProxy(
            self._popup_entry
        )
        self._item_list_widget.setFocusProxy(
            self._popup_entry
        )

    def _set_popup_item_size_(self, w, h):
        self._popup_item_width, self._popup_item_height = w, h
        self._item_list_widget.setGridSize(
            QtCore.QSize(self._popup_item_width, self._popup_item_height)
        )
    
    def _set_popup_tag_filter_item_size_(self, w, h):
        self._popup_tag_filter_item_width, self._popup_tag_filter_item_height = w, h
        self._tag_filter_list_widget.setGridSize(
            QtCore.QSize(self._popup_tag_filter_item_width, self._popup_tag_filter_item_height)
        )

    def _execute_popup_filter_(self):
        keyword_filter_text = self._keyword_filter_line_edit.text()
        selected_item_widgets = self._tag_filter_list_widget._get_selected_item_widgets_()
        if selected_item_widgets:
            item_src = selected_item_widgets[0]
            tags = [item_src._get_name_text_()]
            self._item_list_widget._set_view_tag_filter_data_src_(tags)
        #
        self._item_list_widget._set_view_items_visible_by_any_filter_(
            keyword_filter_text
        )
        self._item_list_widget._refresh_view_all_items_viewport_showable_()
        #
        if self._popup_auto_resize_is_enable is True:
            self._execute_auto_resize_()

    def _execute_popup_all_checked_(self):
        [i._set_checked_(True) for i in self._item_list_widget._get_all_item_widgets_() if i._get_is_visible_() is True]

    def _execute_popup_all_unchecked_(self):
        [i._set_checked_(False) for i in self._item_list_widget._get_all_item_widgets_() if i._get_is_visible_() is True]

    def _close_popup_(self):
        if isinstance(self._popup_entry, QtWidgets.QLineEdit):
            if self._read_only_mark is not None:
                self._popup_entry.setReadOnly(self._read_only_mark)
        #
        self._set_popup_activated_(False)

    def _execute_auto_resize_(self):
        visible_items = self._item_list_widget._get_visible_items_()
        press_pos = self._get_popup_pos_(self._popup_entry_frame)
        width, height = self._get_popup_size_(self._popup_entry_frame)
        height_max = self._item_list_widget._get_maximum_height_(self._item_count_maximum, includes=visible_items)
        height_max += self._popup_toolbar_h
        #
        self._show_popup_(
            press_pos,
            (width, height_max)
        )


class QtPopupCompletionFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    completion_finished = qt_signal(str)
    def __init__(self, *args, **kwargs):
        super(QtPopupCompletionFrame, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_frame_def_init_()
        self._set_popup_def_init_(self)
        #
        self._popup_close_button = QtIconPressItem(self)
        self._popup_close_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('close')
        )
        self._popup_close_button.press_clicked.connect(self._close_popup_)
        self._popup_close_button.setToolTip(
            '"LMB-click" to close'
        )
        #
        self._item_list_widget = _QtListWidgetForPopup(self)
        #
        self._item_count_maximum = 10
        self._popup_item_width, self._popup_item_height = 20, 20
        self._item_list_widget.setGridSize(QtCore.QSize(self._popup_item_width, self._popup_item_height))
        self._item_list_widget.setSpacing(2)
        self._item_list_widget.setUniformItemSizes(True)
        self._item_list_widget.itemClicked.connect(
            self._end_action_popup_
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
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
            border_radius=4
        )
        painter._draw_line_by_points_(
            point_0=self._popup_toolbar_draw_rect.bottomLeft(),
            point_1=self._popup_toolbar_draw_rect.bottomRight(),
            border_color=self._frame_border_color,
        )

        c = self._item_list_widget._get_all_item_count_()
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

        self._item_list_widget.setGeometry(
            c_x+1, c_y+1, c_w-2, c_h-2
        )
        self._item_list_widget.updateGeometries()

    def _refresh_widget_draw_(self):
        self.update()

    def _execute_popup_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._item_list_widget._set_scroll_to_pre_item_()

    def _execute_popup_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._item_list_widget._set_scroll_to_next_item_()

    def _start_action_popup_(self, *args, **kwargs):
        parent = self.parent()
        self._item_list_widget._set_clear_()
        name_texts = parent._get_entry_completion_data_()
        if name_texts:
            current_name_text = parent._get_value_()
            for index, i_name_text in enumerate(name_texts):
                i_item_widget = _QtHItem()
                i_item = QtListWidgetItem()
                i_item.setSizeHint(QtCore.QSize(self._popup_item_width, self._popup_item_height))
                #
                self._item_list_widget.addItem(i_item)
                self._item_list_widget.setItemWidget(i_item, i_item_widget)
                i_item._set_item_show_connect_()
                #
                i_item_widget._set_name_text_(i_name_text)
                i_item_widget._set_icon_name_text_(i_name_text)
                i_item_widget._set_index_(index)
                #
                if current_name_text == i_name_text:
                    i_item.setSelected(True)

            press_pos = self._get_popup_pos_0_(self._popup_entry_frame)
            width, height = self._get_popup_size_(self._popup_entry_frame)
            height_max = self._item_list_widget._get_maximum_height_(self._item_count_maximum)
            height_max += self._popup_toolbar_h

            self._show_popup_(
                press_pos,
                (width, height_max)
            )

            self._item_list_widget._set_scroll_to_selected_item_top_()

            self._popup_entry._set_focused_(True)

            self._popup_is_activated = True
        else:
            self._close_popup_()

    def _end_action_popup_(self, *args, **kwargs):
        parent = self.parent()
        selected_item_widget = self._item_list_widget._get_selected_item_widget_()
        if selected_item_widget:
            name_text = selected_item_widget._get_name_text_()
            parent._set_value_(name_text)
            #
            parent._send_completion_finished_emit_()
            #
            self.completion_finished.emit(name_text)

        self._close_popup_()

    def _close_popup_(self):
        self._set_popup_activated_(False)


class QtPopupForGuide(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    def __init__(self, *args, **kwargs):
        super(QtPopupForGuide, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setPalette(QtDccMtd.get_palette())
        #
        self._set_frame_def_init_()
        self._set_popup_def_init_(self)
        #
        self._keyword_filter_line_edit = QtLineEdit_(self)
        self._keyword_filter_line_edit.hide()
        self._keyword_filter_line_edit._set_entry_enable_(True)
        self._keyword_filter_line_edit.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self._keyword_filter_line_edit.entry_changed.connect(
            self._execute_popup_filter_
        )
        #
        self._popup_close_button = QtIconPressItem(self)
        self._popup_close_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('close')
        )
        self._popup_close_button.press_clicked.connect(self._close_popup_)
        self._popup_close_button.setToolTip(
            '"LMB-click" to close'
        )
        #
        self._item_list_widget = _QtListWidgetForPopup(self)
        #
        self._item_count_maximum = 10
        self._popup_item_width, self._popup_item_height = 20, 20
        #
        self._item_list_widget.setGridSize(QtCore.QSize(self._popup_item_width, self._popup_item_height))
        self._item_list_widget.setSpacing(2)
        self._item_list_widget.setUniformItemSizes(True)
        self._item_list_widget.itemClicked.connect(
            self._end_action_popup_
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
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
        )
        #
        if not self._keyword_filter_line_edit.text():
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
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._close_popup_()
            #
            elif event.type() == QtCore.QEvent.FocusOut:
                self._close_popup_()
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self._close_popup_()
                else:
                    self._keyword_filter_line_edit.keyPressEvent(event)
        return False

    def _execute_popup_filter_(self):
        keyword_filter_text = self._keyword_filter_line_edit.text()
        self._item_list_widget._set_view_items_visible_by_any_filter_(
            keyword_filter_text
        )
        self._item_list_widget._refresh_view_all_items_viewport_showable_()

    def _set_popup_entry_(self, widget):
        self._popup_entry = widget
        self._popup_entry.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._popup_entry)
        self._keyword_filter_line_edit.setFocusProxy(self._popup_entry)

        self._popup_entry.up_key_pressed.connect(
            self._item_list_widget._set_scroll_to_pre_item_
        )
        self._popup_entry.down_key_pressed.connect(
            self._item_list_widget._set_scroll_to_next_item_
        )
        self._popup_entry.enter_key_pressed.connect(
            self._end_action_popup_
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
        c_w, c_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius - 2

        tbr_w = c_w

        self._popup_toolbar_draw_rect.setRect(
            c_x+2, c_y, c_w-4, tbr_h
        )
        self._popup_toolbar_draw_tool_tip_rect.setRect(
            c_x, c_y, tbr_w-tbr_h, tbr_h
        )
        self._keyword_filter_line_edit.show()
        self._keyword_filter_line_edit.setGeometry(
            c_x, c_y, tbr_w-tbr_h, tbr_h
        )
        # close button
        self._popup_close_button.setGeometry(
            c_x + c_w - tbr_h * 1, c_y, tbr_h, tbr_h
        )
        tbr_w -= (tbr_h + spacing)
        c_y += tbr_h
        c_h -= tbr_h
        #
        self._item_list_widget.setGeometry(
            c_x, c_y, c_w, c_h
        )
        self._item_list_widget.updateGeometries()

    def _start_action_popup_(self, index):
        parent = self.parent()
        content_name_texts = list(parent._get_guide_choose_item_content_name_texts_at_(index))
        if content_name_texts:
            desktop_rect = get_qt_desktop_rect()
            #
            press_pos = parent._get_guide_choose_item_point_at_(index)
            press_rect = parent._get_guide_choose_item_rect_at_(index)
            #
            current_name_text = parent._get_view_guide_item_name_text_at_(index)
            for seq, i_name_text in enumerate(content_name_texts):
                i_item_widget = _QtHItem()
                i_item = QtListWidgetItem()
                i_item.setSizeHint(QtCore.QSize(self._popup_item_width, self._popup_item_height))
                #
                self._item_list_widget.addItem(i_item)
                self._item_list_widget.setItemWidget(i_item, i_item_widget)
                i_item._set_item_show_connect_()
                i_item._set_item_keyword_filter_keys_tgt_update_([i_name_text])
                #
                if i_name_text:
                    i_item_widget._set_name_text_(i_name_text)
                    i_item_widget._set_icon_name_text_(i_name_text)
                #
                i_item_widget._set_index_(seq)
                if current_name_text == i_name_text:
                    i_item.setSelected(True)
            #
            self.setFocus(QtCore.Qt.PopupFocusReason)
            #
            height_max = self._item_list_widget._get_maximum_height_(self._item_count_maximum)
            height_max += self._popup_toolbar_h
            popup_width = self._get_popup_width_(content_name_texts)
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
            self._item_list_widget._set_scroll_to_selected_item_top_()
            #
            self._item_list_widget.itemClicked.connect(
                self._close_popup_
            )
            #
            self._popup_entry._set_focused_(True)
            #
            self._popup_is_activated = True
        else:
            self._close_popup_()

    def _end_action_popup_(self):
        if self._choose_index is not None:
            parent = self.parent()
            selected_item_widget = self._item_list_widget._get_selected_item_widget_()
            if selected_item_widget:
                name_text = selected_item_widget._get_name_text_()
                path_text = parent._get_view_guide_item_path_text_at_(
                    self._choose_index
                )
                path_opt = bsc_core.DccPathDagOpt(path_text)
                path_opt.set_name(name_text)
                #
                parent._set_view_guide_item_name_text_at_(
                    name_text,
                    self._choose_index
                )
                parent._set_view_guide_item_path_text_at_(
                    str(path_opt),
                    self._choose_index
                )
                parent._refresh_guide_draw_geometry_()
            #
            parent._set_view_guide_current_index_(self._choose_index)
            parent._send_action_guide_item_press_clicked_emit_()
            parent._clear_guide_current_()
        #
        self._close_popup_()

    def _set_popup_activated_(self, boolean):
        super(QtPopupForGuide, self)._set_popup_activated_(boolean)
        #
        if self._choose_index is not None:
            parent = self.parent()
            parent._set_guide_choose_item_collapse_at_(self._choose_index)
            parent._send_guid_finished_emit_()

    def _get_popup_width_(self, texts):
        count = len(texts)
        _ = max([self.fontMetrics().width(i) for i in texts]) + 32
        _count_width = self.fontMetrics().width(str(count))
        if count > self._item_count_maximum:
            return _ + _count_width + 24
        return _ + _count_width

    def _get_maximum_height_(self):
        rects = [self._item_list_widget.visualItemRect(self._item_list_widget.item(i)) for i in range(self._item_list_widget.count())[:self._item_count_maximum]]
        if rects:
            rect = rects[-1]
            y = rect.y()
            h = rect.height()
            return y+h+1+4
        return 0

    def _close_popup_(self):
        self._set_popup_activated_(False)


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

        if self._resize_gui is not None:
            frm_w, frm_h = 24, 24
            r_x, r_y = x+(w-frm_w), y+(h-frm_h)
            self._resize_gui.setGeometry(
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
        self._set_name_def_init_()
        self._set_frame_def_init_()
        self._set_status_def_init_()
        #
        self._frame_border_color = QtBorderColors.Light
        self._hovered_frame_border_color = QtBorderColors.Hovered
        self._selected_frame_border_color = QtBorderColors.Selected
        #
        self._frame_background_color = QtBackgroundColors.Dim

        self._resize_gui = QtVResizeFrame(self)
        self._resize_gui.hide()
        # self._resize_gui._set_resize_target_(self)
    # resize
    def _get_resize_gui_(self):
        return self._resize_gui

    def _set_resize_enable_(self, boolean):
        self._resize_gui.setVisible(boolean)

    def _set_resize_minimum_(self, value):
        self._resize_gui._set_resize_minimum_(value)

    def _set_resize_target_(self, widget):
        self._resize_gui._set_resize_target_(widget)

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
        bdr_color = [self._frame_border_color, self._selected_frame_border_color][is_selected]
        for i_rect in self._frame_draw_rects:
            painter._draw_frame_by_rect_(
                i_rect,
                border_color=bdr_color,
                background_color=background_color,
                # border_radius=1,
                # border_width=2,
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


class QtVResizeFrame(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtResizeDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
):
    press_clicked = qt_signal()
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        r = min(w, h)
        #
        icn_frm_w, icn_frm_h = r, r
        icn_w, icn_h = self._resize_icon_draw_size
        self._resize_icon_file_draw_rect.setRect(
            x+(w-icn_w)/2, y+(icn_frm_h-icn_h)/2, icn_w, icn_h
        )

    def __init__(self, *args, **kwargs):
        super(QtVResizeFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        #
        self._set_frame_def_init_()
        self._set_resize_def_init_(self)

        self._init_action_def_(self)
        self._set_action_hover_def_init_()
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
                    self.ActionFlag.SplitVHover
                )
            elif event.type() == QtCore.QEvent.Leave:
                self._set_action_hovered_(False)
                self._set_action_flag_clear_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_action_flag_(
                    self.ActionFlag.SplitVClick
                )
                self._execute_action_resize_move_start_(event)
                self._set_pressed_(True)
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_action_flag_(
                    self.ActionFlag.SplitVMove
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
            rect=self._resize_icon_file_draw_rect,
            file_path=self._resize_icon_file_path,
            is_hovered=self._action_is_hovered,
        )

    def _execute_action_resize_move_start_(self, event):
        self._resize_point_start = event.pos()

    def _execute_action_resize_move_(self, event):
        if self._resize_target is not None:
            p = event.pos() - self._resize_point_start
            d_h = p.y()
            h_0 = self._resize_target.minimumHeight()
            h_1 = h_0+d_h
            if self._resize_minimum+10 <= h_1 <= self._resize_maximum+10:
                self._resize_target.setMinimumHeight(h_1)
                self._resize_target.setMaximumHeight(h_1)

    def _execute_action_resize_move_stop_(self, event):
        pass


class _QtScreenshotFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtScreenshotDef,
    utl_gui_qt_abstract.AbsQtHelpDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
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
        self._set_action_hover_def_init_()
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
        p.fill(QtCore.Qt.white)
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
