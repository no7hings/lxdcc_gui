# coding=utf-8
from lxutil_gui.qt.gui_qt_core import *

import lxutil_gui.qt.abstracts as gui_qt_abstract

from lxutil_gui import gui_configure, gui_core


class QtItemDelegate(QtWidgets.QItemDelegate):
    def sizeHint(self, option, index):
        size = super(QtItemDelegate, self).sizeHint(option, index)
        size.setHeight(gui_configure.Size.ITEM_HEIGHT)
        return size


class QtWidget(
    QtWidgets.QWidget,
    #
    gui_qt_abstract.AbsQtStatusBaseDef
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
        self._init_status_base_def_(self)

    def _refresh_widget_draw_(self):
        self.update()

    def paintEvent(self, event):
        if self._get_status_is_enable_() is True:
            painter = QtPainter(self)
            #
            color, hover_color = self._get_border_color_by_validator_status_rgba_args_(self._status)
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


class QtButtonFrame(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        self._frame_draw_rect.setRect(
            x, y, w, h
        )

    def __init__(self, *args, **kwargs):
        super(QtButtonFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._init_frame_base_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)

        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=QtBackgroundColors.Basic,
        )


class QtLine(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForPressDef,
):
    def __init__(self, *args, **kwargs):
        super(QtLine, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._init_frame_base_def_(self)

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

        self._init_action_for_press_def_(self)

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

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtLineWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        # top, bottom, left, right
        self._line_styles = [self.Style.Null]*4
        self._lines = [QtCore.QLine(), QtCore.QLine(), QtCore.QLine(), QtCore.QLine()]
        self._line_border_color = QtBorderColors.Basic
        self._line_border_width = 1

    def _set_line_styles_(self, line_styles):
        # top, bottom, left, right
        self._line_styles = line_styles

    def _set_top_line_mode_(self):
        self._line_styles = [self.Style.Solid, self.Style.Null, self.Style.Null, self.Style.Null]
        self._refresh_widget_all_()

    def _refresh_widget_draw_geometry_(self):
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
        self._refresh_widget_draw_geometry_()

    def paintEvent(self, event):
        painter = QtPainter(self)
        for seq, i in enumerate(self._line_styles):
            i_line = self._lines[seq]
            if i == self.Style.Solid:
                painter._set_border_color_(self._line_border_color)
                painter._set_border_width_(self._line_border_width)
                painter._set_antialiasing_(False)
                painter.drawLine(i_line)


class QtHLine(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtHLine, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedHeight(1)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

    def paintEvent(self, event):
        painter = QtPainter(self)
        painter._set_border_color_(
            79, 79, 79, 255
        )
        painter.drawLine(
            QtCore.QLine(
                0, 0, self.width(), 1
            )
        )


class QtHFrame(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtHFrame, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedHeight(24)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

    def paintEvent(self, event):
        painter = QtPainter(self)
        painter._set_border_color_(
            55, 55, 55, 255
        )
        painter._set_background_color_(
            55, 55, 55, 255
        )
        painter.drawRect(
            QtCore.QRect(
                0, 0, self.width(), self.height()
            )
        )


class _QtTranslucentWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtTranslucentWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def _set_visible_(self, boolean):
        self.setVisible(boolean)


class QtMenuBar(QtWidgets.QMenuBar):
    def __init__(self, *args, **kwargs):
        super(QtMenuBar, self).__init__(*args, **kwargs)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
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
            gui_core.QtStyleMtd.get('QMenuBar')
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
            gui_core.QtStyleMtd.get('QMenu')
        )

    @classmethod
    def _set_cmd_run_(cls, cmd_str):
        exec cmd_str

    @classmethod
    def _create_action_(cls, qt_menu, action_args):
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
                name, icon_name, args_extend = action_args[:3]
                item = QtWidgetAction(qt_menu)
                item.setFont(Font.NAME)
                qt_menu.addAction(item)
                #
                item.setText(name)
                #
                is_checked = False
                #
                if args_extend is None:
                    set_disable_fnc_(item)
                else:
                    if isinstance(
                        args_extend,
                        (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                    ):
                        fnc = args_extend
                        item.triggered.connect(fnc)
                    elif isinstance(args_extend, six.string_types):
                        cmd_str = args_extend
                        item.triggered.connect(lambda *args, **kwargs: cls._set_cmd_run_(cmd_str))
                    elif isinstance(args_extend, (tuple, list)):
                        # check
                        if len(args_extend) == 2:
                            check_fnc, fnc = args_extend
                            if isinstance(
                                    check_fnc,
                                    (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                            ):
                                is_checked = check_fnc()
                            else:
                                is_checked = check_fnc
                            #
                            if isinstance(is_checked, bool):
                                if isinstance(
                                        fnc,
                                        (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                                ):
                                    item.triggered.connect(fnc)
                            else:
                                set_disable_fnc_(item)
                        elif len(args_extend) == 3:
                            check_fnc, fnc, enable_fnc = args_extend
                            if isinstance(
                                    check_fnc,
                                    (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                            ):
                                is_checked = check_fnc()
                            else:
                                is_checked = check_fnc
                            #
                            item.triggered.connect(fnc)
                            if isinstance(
                                    enable_fnc,
                                    (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                            ):
                                is_enable = enable_fnc()
                                item.setEnabled(is_enable)
                                if is_enable is False:
                                    item.setFont(Font.disable)
                                else:
                                    item.setDisabled(False)
                                    item.setFont(Font.NAME)
                if icon_name is not None:
                    if isinstance(icon_name, six.string_types):
                        if icon_name:
                            if icon_name == 'box-check':
                                icon = [
                                    QtIconMtd.create_by_icon_name('basic/box-check-off'),
                                    QtIconMtd.create_by_icon_name('basic/box-check-on')
                                ][is_checked]
                                item.setIcon(icon)
                            elif icon_name == 'radio-check':
                                icon = [
                                    QtIconMtd.create_by_icon_name('basic/radio-check-off'),
                                    QtIconMtd.create_by_icon_name('basic/radio-check-on')
                                ][is_checked]
                                item.setIcon(icon)
                            else:
                                item.setIcon(QtUtilMtd.get_qt_icon(icon_name))
                        else:
                            item.setIcon(
                                QtUtilMtd.get_name_text_icon_(name, background_color=(64, 64, 64))
                            )
                else:
                    item.setIcon(
                        QtUtilMtd.get_name_text_icon_(name, background_color=(64, 64, 64))
                    )
                #
                if len(action_args) >= 4:
                    shortcut = action_args[3]
                    item.setShortcut(shortcut)
                    item.setShortcutContext(QtCore.Qt.WidgetShortcut)
        else:
            qt_menu.addSeparator()

    @classmethod
    def _set_icon_color_rgb_(cls, qt_widget, color):
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

    def _set_menu_data_(self, menu_raw):
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
                    self._create_action_(self, i)
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
                        self._create_action_(sub_menu, j)

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
        QtMenuOpt(self).create_by_content(content)

    @classmethod
    def _set_action_create_by_menu_content_(cls, menu):
        menu.clear()

    @classmethod
    def _add_menu_separator_(cls, menu, content):
        name = content.get('name')
        separator = menu.addSeparator()
        separator.setFont(Font.SEPARATOR)
        separator.setText(name)

    @classmethod
    def _add_menu_action_(cls, menu, content):
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
                QtIconMtd.create_by_icon_name(icon_name)
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

    def _popup_start_(self):
        self.popup(
            QtGui.QCursor().pos()
        )


class QtInfoBubble(QtWidgets.QWidget):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtInfoBubble, self).__init__(*args, **kwargs)
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
                background_color=QtBackgroundColors.Bubble,
                border_radius=4
            )
            painter._draw_text_by_rect_(
                rect=self.rect(),
                text=self._info_text,
                font=self.font(),
                font_color=QtFontColors.Bubble,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            )


class QtTextBubble(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForPressDef,
):
    delete_text_accepted = qt_signal(str)

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtTextBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        # noinspection PyArgumentEqualDefault
        self.setFont(get_font(size=9))

        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self._bubble_frame_draw_rect = QtCore.QRect()

        self._bubble_is_hovered = False
        self._bubble_delete_is_hovered = False

        self._bubble_text_w, self._bubble_text_h = 0, 16
        self._bubble_delete_w = 20
        self._bubble_text_side = 2
        self._bubble_text_spacing = 2
        self._bubble_text = None
        self._bubble_text_draw_rect = QtCore.QRect()
        self._bubble_delete_action_rect = QtCore.QRect()
        self._bubble_delete_size = 16, 16
        self._bubble_delete_icon_draw_rect = QtCore.QRect()
        self._bubble_delete_icon_draw_size = 8, 8
        self._bubble_delete_icon_file_path_0 = gui_core.RscIconFile.get('close')
        self._bubble_delete_icon_file_path_1 = gui_core.RscIconFile.get('close-hover')

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if hasattr(event, 'type'):
                if event.type() == QtCore.QEvent.Close:
                    self.delete_text_accepted.emit(self._get_bubble_text_())
                #
                elif event.type() == QtCore.QEvent.Resize:
                    self._refresh_widget_draw_geometry_()
                    self._refresh_widget_draw_()
                #
                elif event.type() == QtCore.QEvent.Enter:
                    self._bubble_is_hovered = True
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.Leave:
                    self._bubble_is_hovered = False
                    self._bubble_delete_is_hovered = False
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.MouseMove:
                    self._execute_action_move_(event)
                #
                elif event.type() == QtCore.QEvent.MouseButtonPress:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_action_flag_(self.ActionFlag.Press)
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                    if event.button() == QtCore.Qt.LeftButton:
                        pass
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if event.button() == QtCore.Qt.LeftButton:
                        if self._bubble_delete_is_hovered is True:
                            self.close()
                            self.deleteLater()
                    #
                    self._clear_all_action_flags_()
                    #
                    self._is_hovered = False
                    self._refresh_widget_draw_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._bubble_text is not None:
            offset = self._get_action_offset_()
            painter._draw_frame_by_rect_(
                rect=self._bubble_frame_draw_rect,
                border_color=QtBorderColors.Transparent,
                background_color=[QtBackgroundColors.Bubble, QtBackgroundColors.BubbleHovered][self._bubble_is_hovered],
                border_radius=4,
                offset=offset
            )
            painter._draw_text_by_rect_(
                rect=self._bubble_text_draw_rect,
                text=self._bubble_text,
                font_color=QtFontColors.Bubble,
                font=self.font(),
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                offset=offset
            )

            painter._draw_icon_file_by_rect_(
                rect=self._bubble_delete_icon_draw_rect,
                file_path=[self._bubble_delete_icon_file_path_0, self._bubble_delete_icon_file_path_1][
                    self._bubble_delete_is_hovered],
                offset=offset
            )

    def _set_bubble_text_(self, text):
        self._bubble_text = text
        self.setToolTip(self._bubble_text)
        self._update_widget_width_()

    def _get_bubble_text_(self):
        return self._bubble_text

    def _execute_action_move_(self, event):
        p = event.pos()
        if self._bubble_delete_action_rect.contains(p):
            self._bubble_delete_is_hovered = True
        else:
            self._bubble_delete_is_hovered = False
        #
        self._refresh_widget_draw_()

    def _update_widget_width_(self):
        w = self.fontMetrics().width(self._bubble_text)+self._bubble_text_side*2
        # fit to max size
        self._bubble_text_w = min(w, 48)
        self.setMinimumWidth(
            self._bubble_text_w+self._bubble_delete_w
        )

    def _refresh_widget_draw_geometry_(self):
        if self._bubble_text:
            side = self._bubble_text_side
            txt_w, txt_h = self._bubble_text_w, self._bubble_text_h
            dlt_w, dlt_h = self._bubble_delete_size
            dlt_icon_w, dlt_icon_h = self._bubble_delete_icon_draw_size
            x, y = 0, 0
            w, h = self.width(), self.height()

            self._bubble_frame_draw_rect.setRect(
                x, y+(h-txt_h)/2, w, txt_h
            )
            x += side
            self._bubble_text_draw_rect.setRect(
                x, y+(h-txt_h)/2, txt_w, txt_h
            )

            self._bubble_delete_action_rect.setRect(
                x+txt_w, y+(h-txt_h)/2, dlt_w, dlt_h
            )
            self._bubble_delete_icon_draw_rect.setRect(
                x+txt_w+(dlt_w-dlt_icon_w)/2, y+(h-dlt_icon_h)/2, dlt_icon_w, dlt_icon_h
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
            gui_core.QtStyleMtd.get('QScrollArea')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            gui_core.QtStyleMtd.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            gui_core.QtStyleMtd.get('QScrollBar')
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
            gui_core.QtStyleMtd.get('QScrollArea')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            gui_core.QtStyleMtd.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            gui_core.QtStyleMtd.get('QScrollBar')
        )

    def keyPressEvent(self, event):
        pass


class QtThreadDef(object):
    def _set_thread_def_init_(self):
        pass

    def _create_fnc_thread_(self):
        return QtMethodThread(self)


class QtTextLabel(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtNameBaseDef,
):
    pass


class QtTextItem(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtNameBaseDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,
    #
    gui_qt_abstract.AbsQtStatusBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtTextItem, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        #
        self._init_name_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self._init_status_base_def_(self)

        self._set_name_draw_font_(QtFonts.Label)
        self._name_text_option = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        if self._name_align == self.AlignRegion.Top:
            icn_frm_w, icn_frm_h = self._name_frame_size
            t_w, t_h = self._name_draw_size
            self._name_draw_rect.setRect(
                x, y+(icn_frm_h-t_h)/2, w, t_h
            )
        else:
            self._name_draw_rect.setRect(
                x, y, w, h
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        self._refresh_widget_draw_geometry_()
        # name
        if self._name_text is not None:
            color, hover_color = self._get_text_color_by_validator_status_rgba_args_(self._status)
            text_color = [color, hover_color][self._is_hovered]
            #
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=self._name_text,
                font_color=text_color,
                font=self._name_draw_font,
                text_option=self._name_text_option,
            )


class QtMainWindow(
    QtWidgets.QMainWindow,
    #
    gui_qt_abstract.AbsQtIconBaseDef,
    gui_qt_abstract.AbsQtBusyBaseDef,
    gui_qt_abstract.AbsQtActionBaseDef,
    #
    gui_qt_abstract.AbsQtThreadBaseDef,
    #
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
        # todo: do not use WA_TranslucentBackground mode, GL bug
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setPalette(QtDccMtd.get_palette())
        self.setAutoFillBackground(True)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setFont(Font.NAME)
        #
        set_shadow(self, radius=2)
        #
        self._init_icon_base_def_(self)
        self._window_system_tray_icon = None
        self._init_busy_base_def_(self)
        self._init_action_base_def_(self)
        self._init_thread_base_def_(self)
        #
        self.setStyleSheet(
            gui_core.QtStyleMtd.get('QMainWindow')
        )
        self.menuBar().setStyleSheet(
            gui_core.QtStyleMtd.get('QMenuBar')
        )
        self._frame_draw_rect = QtCore.QRect()
        self._menu_frame_draw_rect = QtCore.QRect()

    #
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        m_h = self.menuBar().height()
        self._frame_draw_rect.setRect(
            x, y, w, h
        )
        self._menu_frame_draw_rect.setRect(
            x, y, w, m_h
        )

    #
    def _set_icon_name_text_(self, text):
        self.setWindowIcon(QtUtilMtd.get_name_text_icon_(text))

    def _set_icon_name_(self, icon_name):
        self.setWindowIcon(QtIconMtd.create_by_icon_name(icon_name))

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
                # elif event.type() == QtCore.QEvent.ShortcutOverride:
                #     if event.key() == QtCore.Qt.Key_Space:
                #         event.ignore()
        return False

    def paintEvent(self, event):
        self._refresh_widget_draw_geometry_()
        painter = QtPainter(self)
        painter.fillRect(
            self._frame_draw_rect,
            QtBackgroundColors.Basic
        )
        painter.fillRect(
            self._menu_frame_draw_rect,
            QtBackgroundColors.Dark
        )

    def _set_size_changed_connect_to_(self, fnc):
        self.size_changed.connect(fnc)

    def _set_close_(self):
        self.close()
        self.deleteLater()

    def _close_later_(self, delay_time):
        close_timer = QtCore.QTimer(self)
        close_timer.timeout.connect(self._set_close_)
        close_timer.start(delay_time)

    def _create_window_shortcut_action_(self, fnc, shortcut):
        action = QtWidgets.QAction(self)
        action.triggered.connect(fnc)
        action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.addAction(action)


class QtDialog(
    QtWidgets.QDialog,
    gui_qt_abstract.AbsQtStatusBaseDef,
    QtThreadDef
):
    size_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtDialog, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(
            QtCore.Qt.Window|QtCore.Qt.WindowStaysOnTopHint
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
        self._init_status_base_def_(self)

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

    def _close_later_(self, delay_time):
        close_timer = QtCore.QTimer(self)
        close_timer.timeout.connect(self._set_close_)
        close_timer.start(delay_time)

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
        self._icon_draw_size = QtCore.QSize(20, 20)

    def _draw_for_hover_(self, painter, option, index):
        if option.state&QtWidgets.QStyle.State_MouseOver:
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
        elif option.state&QtWidgets.QStyle.State_Selected:
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
        size.setHeight(gui_configure.Size.ITEM_HEIGHT)
        return size


class QtListWidgetStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, *args, **kwargs):
        super(QtListWidgetStyledItemDelegate, self).__init__(*args, **kwargs)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QtProgressBar(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtProgressDef
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
    #
    gui_qt_abstract.AbsQtNamesBaseDef,
    gui_qt_abstract.AbsQtMenuBaseDef,
    #
    gui_qt_abstract.AbsQtItemFilterDef,
    #
    gui_qt_abstract.AbsQtStateDef,
    #
    gui_qt_abstract.AbsQtDagDef,
    gui_qt_abstract.AbsQtVisibleDef,
    #
    gui_qt_abstract.AbsQtShowBaseForItemDef,
    gui_qt_abstract.AbsQtItemVisibleConnectionDef,
):
    def update(self):
        pass

    def _refresh_widget_all_(self, *args, **kwargs):
        item_widget = self._get_item_widget_()
        if item_widget is not None:
            item_widget._refresh_widget_all_(*args, **kwargs)

    def _refresh_widget_draw_(self):
        item_widget = self._get_item_widget_()
        if item_widget is not None:
            item_widget._refresh_widget_draw_()

    def __init__(self, *args, **kwargs):
        super(QtListWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        )
        self._init_names_base_def_(self)
        self._init_menu_base_def_(self)
        self._init_show_base_for_item_def_(self)
        #
        self._visible_tgt_key = None
        self._init_item_filter_extra_def_(self)
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

    def _connect_item_show_(self):
        self._setup_item_show_(self.listWidget())

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
        self._checkout_item_show_loading_()
        return view._get_view_item_viewport_showable_(item)

    def _set_item_widget_visible_(self, boolean):
        item_widget = self._get_item_widget_()
        if item_widget is not None:
            self._get_item_widget_().setVisible(boolean)


class _QtHItem(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtIndexBaseDef,
    gui_qt_abstract.AbsQtTypeDef,
    gui_qt_abstract.AbsQtIconBaseDef,
    gui_qt_abstract.AbsQtNamesBaseDef,
    gui_qt_abstract.AbsQtPathBaseDef,
    gui_qt_abstract.AbsQtImageBaseDef,
    #
    gui_qt_abstract.AbsQtValueBaseDef,
    #
    gui_qt_abstract.AbsQtMenuBaseDef,
    # action
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,
    gui_qt_abstract.AbsQtPressSelectExtraDef,
    gui_qt_abstract.AbsQtCheckBaseDef,
    gui_qt_abstract.AbsQtDeleteBaseDef,
    #
    gui_qt_abstract.AbsQtItemFilterDef,
):
    delete_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(_QtHItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self._init_frame_base_def_(self)
        self._init_index_base_def_(self)
        self._init_type_def_(self)
        self._init_icon_base_def_(self)
        self._init_names_base_def_(self)
        self._init_path_base_def_(self)
        self._init_image_base_def_()
        #
        self._init_value_base_def_(self)
        #
        self._init_menu_base_def_(self)
        #
        self._init_delete_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_check_base_def_(self)
        self._check_icon_file_path_0 = gui_core.RscIconFile.get('filter_unchecked')
        self._check_icon_file_path_1 = gui_core.RscIconFile.get('filter_checked')
        self._refresh_check_draw_()
        self._init_press_select_extra_def_(self)
        #
        self._init_item_filter_extra_def_(self)
        #
        self._frame_background_color = QtBackgroundColors.Light

    def _refresh_widget_all_(self, *args, **kwargs):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        spacing = 2
        #
        frm_w = frm_h = h
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_frm_m_w, icn_frm_m_h = (frm_w-icn_frm_w)/2, (frm_h-icn_frm_h)/2
        icn_w, icn_h = int(icn_frm_w*self._icon_draw_percent), int(icn_frm_h*self._icon_draw_percent)
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
                c_x, c_y, icn_frm_w, c_h
            )
            self._set_check_icon_draw_rect_(
                c_x+(icn_frm_w-icn_w)/2, c_y+(icn_frm_w-icn_h)/2, icn_w, icn_h
            )
            c_x += icn_frm_w+spacing
            c_w -= icn_frm_w+spacing
            # f_x += icn_frm_w+spacing
            # f_w -= icn_frm_w+spacing
        # icon use file
        if self._icon_file_path is not None:
            icn_frm_w_0, icn_frm_h_0 = c_h, c_h
            icn_w_0, icn_h_0 = int(icn_frm_w_0*self._icon_draw_percent), int(icn_frm_h_0*self._icon_draw_percent)
            self._set_icon_file_draw_rect_(
                c_x+(icn_frm_w_0-icn_w_0)/2, c_y+(icn_frm_h_0-icn_h_0)/2, icn_w_0, icn_h_0
            )
            c_x += icn_frm_w_0+spacing
            c_w -= icn_frm_w_0+spacing
        # icon use text
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
        # delete
        if self._delete_is_enable is True:
            icn_w, icn_h = self._delete_icon_file_draw_size
            self._set_delete_rect_(
                x+w-icn_frm_w, c_y+(c_h-icn_frm_h)/2, icn_frm_w, icn_frm_h
            )
            self._set_delete_draw_rect_(
                x+(icn_frm_w-icn_w)/2+w-icn_frm_w, c_y+(c_h-icn_h)/2, icn_w, icn_h
            )
            c_w -= icn_frm_w+spacing
            # f_w -= icn_frm_w+spacing
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

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Close:
                self.delete_text_accepted.emit(self._get_name_text_())
            #
            elif event.type() == QtCore.QEvent.Enter:
                pass
                # self._do_hover_move_(event)
            elif event.type() == QtCore.QEvent.Leave:
                self._check_is_hovered = False
                self._press_is_hovered = False
                self._delete_is_hovered = False
                self._is_hovered = False
                #
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Show:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
                elif event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.AnyClick)
                    if self._get_action_check_is_valid_(event) is True:
                        self.check_clicked.emit()
                        self._set_action_check_execute_(event)
                    elif self._get_action_delete_is_valid_(event) is True:
                        self.delete_press_clicked.emit()
                    else:
                        self.clicked.emit()
                #
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._check_is_hovered is True:
                        pass
                    elif self._delete_is_hovered is True:
                        pass
                    else:
                        self.press_clicked.emit()
                    self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        # todo: refresh error
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        bkg_color = painter._get_frame_background_color_by_rect_(
            rect=self._frame_draw_rect,
            check_is_hovered=self._check_is_hovered,
            is_checked=self._is_checked,
            press_is_hovered=self._press_is_hovered,
            is_pressed=self._is_pressed,
            is_selected=self._is_selected,
            delete_is_hovered=self._delete_is_hovered
        )
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=QtBorderColors.Transparent,
            background_color=bkg_color,
            border_radius=1
        )
        # check
        if self._check_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._check_icon_draw_rect,
                file_path=self._check_icon_file_path_current,
                offset=offset,
                # frame_rect=self._check_rect,
                is_hovered=self._check_is_hovered
            )
        # icon
        if self._icon_name_text is not None:
            painter._draw_image_use_text_by_rect_(
                rect=self._icon_name_draw_rect,
                text=self._icon_name_text,
                background_color=bkg_color,
                offset=offset,
                border_radius=1, border_width=2
            )
        #
        if self._icon_file_path is not None:
            painter._draw_icon_file_by_rect_(
                rect=self._icon_draw_rect,
                file_path=self._icon_file_path,
            )
        # image
        if self._image_draw_is_enable is True:
            painter._draw_image_data_by_rect_(
                rect=self._image_draw_rect,
                image_data=self._image_data,
                offset=offset,
                text=self._name_text
            )
        # name
        if self._name_texts:
            for i in self._name_indices:
                painter._draw_text_by_rect_(
                    rect=self._name_draw_rects[i],
                    text=self._name_texts[i],
                    font_color=self._name_color,
                    font=self._name_draw_font,
                    text_option=self._name_text_option,
                    is_hovered=self._is_hovered,
                    is_selected=self._is_selected,
                    offset=offset
                )
        #
        elif self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font_color=self._name_color,
                font=self._name_draw_font,
                text_option=self._name_text_option,
                is_hovered=self._is_hovered,
                is_selected=self._is_selected,
                offset=offset
            )
        #
        if self._index_text is not None:
            painter._draw_text_by_rect_(
                self._index_rect,
                self._get_index_text_(),
                font_color=self._index_text_color,
                font=self._index_text_font,
                text_option=self._index_text_option,
                offset=offset
            )
        #
        if self._delete_draw_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._delete_icon_draw_rect,
                file_path=self._delete_icon_file_path,
                offset=offset,
                is_hovered=self._delete_is_hovered
            )

    def _execute_action_hover_entry_(self, event):
        pass

    def _do_hover_move_(self, event):
        p = event.pos()
        self._check_is_hovered = False
        self._press_is_hovered = False
        self._delete_is_hovered = False

        if self._check_action_is_enable is True:
            if self._check_rect.contains(p):
                self._check_is_hovered = True
        if self._frame_draw_rect.contains(p):
            self._press_is_hovered = True
        if self._delete_is_enable is True:
            if self._delete_action_rect.contains(p):
                self._delete_is_hovered = True
        #
        self._is_hovered = self._check_is_hovered or self._press_is_hovered or self._delete_is_hovered
        #
        self._refresh_widget_draw_()

    def _get_is_visible_(self):
        return self.isVisible()


class _QtScreenshotFrame(
    QtWidgets.QWidget,
    gui_qt_abstract.AbsQtFrameBaseDef,
    gui_qt_abstract.AbsQtScreenshotDef,
    gui_qt_abstract.AbsQtHelpDef,
    #
    gui_qt_abstract.AbsQtActionBaseDef,
    gui_qt_abstract.AbsQtActionForHoverDef,
    gui_qt_abstract.AbsQtActionForPressDef,
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
            |QtCore.Qt.FramelessWindowHint
            |QtCore.Qt.WindowStaysOnTopHint
        )

        self._init_frame_base_def_(self)
        self._set_screenshot_def_init_(self)
        self._set_help_def_init_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

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
                border_color=(79, 95, 151),
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
                    text_option=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop,
                    word_warp=True
                )
