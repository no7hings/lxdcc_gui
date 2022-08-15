# coding=utf-8
import collections

import os

import functools

from lxbasic import bsc_configure

from lxbasic.objects import bsc_obj_abs

from lxutil_gui.qt import utl_gui_qt_abstract

from lxutil_gui.qt.utl_gui_qt_core import *

import lxutil.methods as utl_methods

from lxutil_gui import utl_gui_core


class QtItemDelegate(QtWidgets.QItemDelegate):
    def sizeHint(self, option, index):
        size = super(QtItemDelegate, self).sizeHint(option, index)
        size.setHeight(utl_configure.GuiSize.item_height)
        return size


class QtWidget(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtStatusDef
):
    def __init__(self, *args, **kwargs):
        super(QtWidget, self).__init__(*args, **kwargs)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        #
        self.setAutoFillBackground(True)
        #
        self._set_status_def_init_()

    def _set_wgt_update_draw_(self):
        self.update()

    def paintEvent(self, event):
        if self._get_status_is_enable_() is True:
            painter = QtPainter(self)
            #
            if self._status in [
                bsc_configure.ValidatorStatus.Error
            ]:
                pox_x, pos_y = 0, 0
                width, height = self.width(), self.height()
                frame_rect = QtCore.QRect(
                    pox_x, pos_y, width, height
                )
                #
                painter._set_frame_draw_by_rect_(
                    frame_rect,
                    border_color=(255, 0, 63, 255),
                    background_color=(0, 0, 0, 0),
                    border_width=2,
                    border_radius=2
                )
            elif self._status in [
                bsc_configure.ValidatorStatus.Warning
            ]:
                pox_x, pos_y = 0, 0
                width, height = self.width(), self.height()
                frame_rect = QtCore.QRect(
                    pox_x, pos_y, width, height
                )
                #
                painter._set_frame_draw_by_rect_(
                    frame_rect,
                    border_color=(255, 255, 63, 255),
                    background_color=(0, 0, 0, 0),
                    border_width=2,
                    border_radius=2
                )
            elif self._status in [
                bsc_configure.ValidatorStatus.Correct
            ]:
                pox_x, pos_y = 0, 0
                width, height = self.width(), self.height()
                frame_rect = QtCore.QRect(
                    pox_x, pos_y, width, height
                )
                #
                painter._set_frame_draw_by_rect_(
                    frame_rect,
                    border_color=(63, 255, 127, 255),
                    background_color=(0, 0, 0, 0),
                    border_width=2,
                    border_radius=2
                )


class _QtLine(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef
):
    def __init__(self, *args, **kwargs):
        super(_QtLine, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._set_frame_def_init_()

        self._frame_border_color = 95, 95, 95, 255
        self._frame_background_color = 0, 0, 0, 0

    def _set_wgt_update_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = QtPainter(self)

        x, y = 2, 0
        w, h = self.width(), self.height()
        rect = QtCore.QRect(x, y, w, h)
        painter._set_line_draw_by_rect_(
            rect,
            self._frame_border_color,
            self._frame_background_color
        )


class _QtTranslucentWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtTranslucentWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


class QtFrame(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(QtFrame, self).__init__(*args, **kwargs)


class QtIconButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(QtIconButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setPalette(QtDccMtd.get_qt_palette())
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
        i_w, i_h = self._icon_file_draw_size
        painter = QtPainter(self)
        #
        f_x, f_y = (w-i_w) / 2, (h-i_h) / 2
        #
        bkg_rect = QtCore.QRect(1, 1, w-1, h-1)
        bkg_color = [QtBackgroundColor.Transparent, QtBackgroundColor.Hovered][self._action_is_hovered]
        painter._set_frame_draw_by_rect_(
            bkg_rect,
            border_color=bkg_color,
            background_color=bkg_color,
            border_radius=4
        )
        if self._icon_file_path is not None:
            icn = QtCore.QRect(f_x, f_y, i_w, i_h)
            painter._set_svg_image_draw_by_rect_(icn, self._icon_file_path)
        elif self._icon_color_rgb is not None:
            pass


class QtPressButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(QtPressButton, self).__init__(*args, **kwargs)
        self.setFont(Font.NAME)
        self.setPalette(QtDccMtd.get_qt_palette())
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
        self.setPalette(QtDccMtd.get_qt_palette())
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
        self.setPalette(QtDccMtd.get_qt_palette())
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
                    if isinstance(icon_name, (str, unicode)):
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
                    elif isinstance(method_args, (str, unicode)):
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
                        if isinstance(i_icon_name, (str, unicode)):
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
        # if isinstance(content, bsc_obj_abs.AbsContent):
        #     keys = content.get_keys(regex='*.properties')
        #     for i_key in keys:
        #         type_ = content.get('{}.type'.format(i_key))
        #         i_content = content.get_content(i_key)
        #         if type_ == 'separator':
        #             self._set_separator_add__(self, i_content)
        #         elif type_ == 'action':
        #             self._set_action_add__(self, i_content)
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
        elif isinstance(execute_fnc, (str, unicode)):
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
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        #
        self.setFont(Font.NAME)


class QtLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(QtLabel, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
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
        qt_palette = QtDccMtd.get_qt_palette()
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


class QtMainWindow(
    QtWidgets.QMainWindow,
    utl_gui_qt_abstract.AbsQtIconDef,
    QtThreadDef
):
    close_clicked = qt_signal()
    key_escape_pressed = qt_signal()
    size_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtMainWindow, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #
        self.setPalette(QtDccMtd.get_qt_palette())
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
    def _set_wgt_update_draw_(self):
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
                elif event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_Escape:
                        self.key_escape_pressed.emit()
                elif event.type() == QtCore.QEvent.Resize:
                    self.size_changed.emit()
        return False

    def _set_size_changed_connect_to_(self, fnc):
        self.size_changed.connect(fnc)
    # def close(self):
    #     self.close_clicked.emit()
    #     return super(QtMainWindow, self).close()

    def _set_close_(self):
        self.close()
        self.deleteLater()

    def _set_close_later_(self, time):
        close_timer = QtCore.QTimer(self)
        close_timer.timeout.connect(self._set_close_)
        close_timer.start(time)

    def _set_window_shortcut_action_create_(self, fnc, shortcut):
        action = QtWidgets.QAction(self)
        action.triggered.connect(fnc)
        action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.addAction(action)


class QtDialog(
    QtWidgets.QDialog,
    utl_gui_qt_abstract._QtStatusDef,
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
        qt_palette = QtDccMtd.get_qt_palette()
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
    def _set_wgt_update_draw_(self):
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

    def paint(self, painter, option, index):
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
                        spans = methods.String.find_spans(content, filter_keyword)
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
        super(QtStyledItemDelegate, self).paint(painter, option, index)

    def updateEditorGeometry(self, editor, option, index):
        super(QtStyledItemDelegate, self).updateEditorGeometry(editor, option, index)

    def sizeHint(self, option, index):
        size = super(QtStyledItemDelegate, self).sizeHint(option, index)
        size.setHeight(utl_configure.GuiSize.item_height)
        return size


class QtLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(QtLineEdit, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)
        #
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def _set_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())

    def _set_use_as_float_(self):
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
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)


class QtRadioButton(QtWidgets.QRadioButton):
    def __init__(self, *args, **kwargs):
        super(QtRadioButton, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self.setFont(Font.NAME)


class QtComboBox(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super(QtComboBox, self).__init__(*args, **kwargs)
        self.setPalette(QtDccMtd.get_qt_palette())
        self.setItemDelegate(QtStyledItemDelegate())
        self.view().setAlternatingRowColors(True)
        self.setFont(Font.NAME)
        #
        self.setLineEdit(QtLineEdit())


class QtProgressDialog(QtWidgets.QProgressDialog):
    def __init__(self, *args, **kwargs):
        super(QtProgressDialog, self).__init__(*args, **kwargs)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setCancelButton(None)


class _QtProgressBar(
    QtWidgets.QWidget,
    utl_gui_qt_abstract._QtProgressDef
):
    def __init__(self, *args, **kwargs):
        super(_QtProgressBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMaximumHeight(4)
        self.setMinimumHeight(4)
        #
        self._set_progress_def_init_()

    def _set_wgt_update_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._get_progress_is_enable_() is True:
            if self._progress_raw:
                cur_rect = None
                w, h = self.width(), self.height()
                w -= 2
                layer_count = len(self._progress_raw)
                r, g, b = utl_methods.Color.hsv2rgb(120, .5, 1)
                for layer_index, i in enumerate(self._progress_raw):
                    i_minimum, i_maximum, percent, label = i
                    p_w = w*(i_maximum-i_minimum)*percent
                    p_h = 2
                    #
                    i_x, i_y = w*i_minimum, (h-p_h)/2
                    i_x += 1
                    i_rect = QtCore.QRect(i_x, i_y, p_w+1, p_h)
                    #
                    i_p = float(layer_index)/float(layer_count)
                    r_1, g_1, b_1 = utl_methods.Color.hsv2rgb(120*i_p, .5, 1)
                    i_cur_color = QtGui.QColor(r_1, g_1, b_1, 255)
                    if layer_index == 0:
                        i_pre_color = QtGui.QColor(r, g, b, 255)
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(.5, i_pre_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_background_color = i_gradient_color
                    else:
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(0, QtBackgroundColor.Transparent)
                        i_gradient_color.setColorAt(.5, i_cur_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_gradient_color.setColorAt(1, QtBackgroundColor.Transparent)
                        i_background_color = i_gradient_color
                    #
                    painter._set_frame_draw_by_rect_(
                        i_rect,
                        border_color=QtBorderColor.Transparent,
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
                    painter._set_frame_draw_by_rect_(
                        rect,
                        border_color=QtBorderColor.Transparent,
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
        qt_palette = QtDccMtd.get_qt_palette()
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
        self._set_wgt_update_geometry_()

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

    def _set_wgt_update_geometry_(self):
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
    utl_gui_qt_abstract.AbsShowItemDef,
    #
    utl_gui_qt_abstract.AbsQtItemFilterTgtDef,
    #
    utl_gui_qt_abstract.AbsQtItemStateDef,
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
        self._set_show_item_def_init_(self)
        #
        self._visible_tgt_key = None
        self._set_item_filter_tgt_def_init_()
        #
        self._set_item_state_def_init_()
        #
        self._set_dag_def_init_()
        self._set_visible_def_init_()
        #
        self._set_item_visible_connection_def_init_()

    def setData(self, role, value):
        if role == QtCore.Qt.CheckStateRole:
            pass
        super(QtListWidgetItem, self).setData(role, value)

    def _get_item_is_hidden_(self):
        return self.isHidden()

    def _set_wgt_update_draw_(self):
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
    # show
    def _set_view_(self, widget):
        self._list_widget = widget

    def _set_item_show_connect_(self):
        self._set_item_show_def_setup_(self.listWidget())

    def _get_item_keyword_filter_tgt_keys_(self):
        item_widget = self._get_item_widget_()
        if item_widget is not None:
            item_widget._get_name_texts_()
        return []

    def _get_view_(self):
        return self.listWidget()

    def _get_item_is_viewport_show_able_(self):
        item = self
        view = self.listWidget()
        #
        self._set_item_show_start_loading_()
        return view._get_show_view_item_showable_(item)

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
    utl_gui_qt_abstract.AbsQtPathDef,
    #
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtDeleteDef,
    # action
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtActionSelectDef,
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
        self._set_path_def_init_()
        #
        self._set_menu_def_init_()
        #
        self._set_delete_def_init_(self)
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        self._set_action_select_def_init_()
        #
        self._frame_background_color = QtBackgroundColor.Light

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_action_hovered_(True)
            elif event.type() == QtCore.QEvent.Leave:
                self._set_action_hovered_(False)
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
                    if self._delete_is_hovered:
                        self.delete_press_clicked.emit()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_action_hover_execute_(event)
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        self._set_wgt_update_geometry_()
        #
        background_color = painter._get_item_background_color_by_rect_(
            self._frame_draw_rect,
            is_hovered=self._action_is_hovered,
            is_selected=self._item_is_selected
        )
        painter._set_frame_draw_by_rect_(
            self._frame_draw_rect,
            border_color=QtBackgroundColor.Transparent,
            background_color=background_color,
            border_radius=1
        )
        # icon
        if self._icon_name_text is not None:
            painter._set_icon_name_text_draw_by_rect_(
                self._icon_name_draw_rect,
                self._icon_name_text,
                background_color=background_color,
                # offset=0,
                border_radius=2,
                border_width=2
            )
        if self._icon_file_path is not None:
            painter._set_icon_file_draw_by_rect_(
                rect=self._icon_file_draw_rect,
                file_path=self._icon_file_path,
            )
        #
        if self._name_text is not None:
            painter._set_text_draw_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font_color=self._name_color,
                font=self._name_text_font,
                text_option=self._name_text_option,
                is_hovered=self._action_is_hovered,
                is_selected=self._item_is_selected,
            )
        #
        if self._index_text is not None:
            painter._set_text_draw_by_rect_(
                self._index_rect,
                self._get_index_text_(),
                font_color=self._index_text_color,
                font=self._index_text_font,
                text_option=self._index_text_option
            )

        if self._delete_is_enable is True:
            painter._set_icon_file_draw_by_rect_(
                rect=self._delete_draw_rect,
                file_path=self._get_delete_icon_file_path_(),
            )

    def _set_action_hover_execute_(self, event):
        p = event.pos()
        self._delete_is_hovered = False
        if self._delete_is_enable is True:
            if self._delete_draw_rect.contains(p):
                self._delete_is_hovered = True
        #
        self._set_wgt_update_draw_()

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        spacing = 2
        f_w, f_h = self._icon_frame_size
        #
        i_x, i_y = x, y
        i_w, i_h = w, h
        #
        self._set_frame_rect_(
            x, y, w, h
        )
        if self._icon_file_path is not None:
            i_f_w, i_f_h = self._icon_file_draw_size
            self._set_icon_file_draw_rect_(
                x+(f_w-i_f_w)/2, y+(f_h-i_f_h)/2, i_f_w, i_f_h
            )
            i_x += f_w+spacing
            i_w -= f_w+spacing
        #
        if self._icon_name_text is not None:
            i_n_w, i_n_h = self._icon_name_draw_size
            self._set_icon_name_draw_rect_(
                x+(f_w-i_n_w)/2, y+(f_h-i_n_h)/2, i_n_w, i_n_h
            )
            i_x += f_w+spacing
            i_w -= f_w+spacing
        #
        if self._delete_is_enable is True:
            i_f_w, i_f_h = self._delete_icon_file_draw_size
            self._set_delete_draw_rect_(
                x+(f_w-i_f_w)/2+w-f_w, y+(f_h-i_f_h)/2, i_f_w, i_f_h
            )
            i_w -= f_w+spacing
        #
        self._set_name_rect_(
            i_x, i_y, i_w, i_h
        )
        #
        self._set_index_rect_(
            i_x, i_y, i_w, i_h
        )


class _QtPopupListView(utl_gui_qt_abstract.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(_QtPopupListView, self).__init__(*args, **kwargs)
        self.setDragDropMode(QtWidgets.QListWidget.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.ListMode)
        self.setPalette(QtDccMtd.get_qt_palette())

    def paintEvent(self, event):
        pass

    def _get_maximum_height_(self, count_maximum):
        rects = [self.visualItemRect(self.item(i)) for i in range(self.count())[:count_maximum]]
        if rects:
            rect = rects[-1]
            y = rect.y()
            h = rect.height()
            return y+h+1+4
        return 20


class _QtPopupChooseFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtPopupChooseFrame, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_frame_def_init_()
        self._set_popup_def_init_(self)
        #
        self.setFocusProxy(self._popup_target_entry)
        #
        self._list_widget = _QtPopupListView(self)
        #
        self._item_count_maximum = 20
        self._item_width, self._item_height = 20, 20
        self._list_widget.setGridSize(QtCore.QSize(self._item_width, self._item_height))
        self._list_widget.setSpacing(2)
        self._list_widget.setUniformItemSizes(True)
        self._list_widget.itemClicked.connect(
            self._set_popup_end_
        )
        #
        self._choose_index = None
        #
        self._frame_border_color = QtBackgroundColor.Light
        self._hovered_frame_border_color = QtBackgroundColor.Hovered
        self._selected_frame_border_color = QtBackgroundColor.Hovered
        #
        self._frame_background_color = QtBackgroundColor.Dark

    def paintEvent(self, event):
        painter = QtPainter(self)
        #
        painter._set_frame_draw_by_rect_(
            self._frame_draw_rect,
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
            border_radius=4
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._popup_target_entry:
            if event.type() == QtCore.QEvent.FocusOut:
                self._set_popup_activated_(False)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self._set_popup_activated_(False)
        return False

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius - 2
        #
        self._frame_draw_rect.setRect(
            x+1, y+1, w-2, h-2
        )
        self._list_widget.setGeometry(
            x+1, y+1, w-2, h-2
        )
        self._list_widget.updateGeometries()

    def _set_popup_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._list_widget._set_scroll_to_pre_item_()

    def _set_popup_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._list_widget._set_scroll_to_next_item_()

    def _set_popup_start_(self):
        if self._popup_is_activated is False:
            parent = self.parent()
            self._list_widget._set_clear_()
            name_texts = parent._get_choose_values_()
            if name_texts:
                if isinstance(name_texts, (tuple, list)):
                    icon_file_paths = parent._get_choose_icon_file_paths_()
                    current_name_text = parent._get_choose_current_()
                    for index, i_name_text in enumerate(name_texts):
                        i_item_widget = _QtHItem()
                        i_item = QtListWidgetItem()
                        i_item.setSizeHint(QtCore.QSize(self._item_width, self._item_height))
                        #
                        self._list_widget.addItem(i_item)
                        self._list_widget.setItemWidget(i_item, i_item_widget)
                        i_item._set_item_show_connect_()
                        #
                        i_item_widget._set_name_text_(i_name_text)
                        i_item_widget._set_index_(index)
                        i_icon_file_path = icon_file_paths[index]
                        if i_icon_file_path is not None:
                            i_item_widget._set_icon_file_path_(i_icon_file_path)
                        else:
                            i_item_widget._set_icon_name_text_(i_name_text[0])
                        #
                        if current_name_text == i_name_text:
                            i_item.setSelected(True)
                    #
                    press_pos = self._get_popup_pos_(self._popup_target_entry_frame)
                    width, height = self._get_popup_size_(self._popup_target_entry_frame)
                    height_max = self._list_widget._get_maximum_height_(self._item_count_maximum)
                    height_frame = self._popup_target_entry_frame.height()
                    self._set_popup_fnc_(
                        press_pos,
                        (width, height_max)
                    )
                    #
                    self._list_widget._set_scroll_to_selected_item_top_()
                    #
                    self._popup_target_entry._set_focused_(True)

                    self._popup_is_activated = True

    def _set_popup_end_(self):
        parent = self.parent()
        selected_item_widget = self._list_widget._get_selected_item_widget_()
        if selected_item_widget:
            name_text = selected_item_widget._get_name_text_()
            parent._set_choose_current_(name_text)
            parent._set_choose_changed_emit_send_()
        #
        self._set_popup_activated_(False)


class _QtPopupCompletionFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtPopupCompletionFrame, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._set_frame_def_init_()
        self._set_popup_def_init_(self)
        #
        self.setFocusProxy(self._popup_target_entry)
        #
        self._list_widget = _QtPopupListView(self)
        #
        self._item_count_maximum = 20
        self._item_width, self._item_height = 20, 20
        self._list_widget.setGridSize(QtCore.QSize(self._item_width, self._item_height))
        self._list_widget.setSpacing(2)
        self._list_widget.setUniformItemSizes(True)
        self._list_widget.itemClicked.connect(
            self._set_popup_end_
        )
        #
        self._choose_index = None
        #
        self._frame_border_color = QtBackgroundColor.Light
        self._hovered_frame_border_color = QtBackgroundColor.Hovered
        self._selected_frame_border_color = QtBackgroundColor.Hovered
        #
        self._frame_background_color = QtBackgroundColor.Dark

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        painter = QtPainter(self)
        #
        painter._set_frame_draw_by_rect_(
            self._frame_draw_rect,
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
            border_radius=4
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._popup_target_entry:
            if event.type() == QtCore.QEvent.FocusOut:
                self._set_popup_activated_(False)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self._set_popup_activated_(False)
        return False

    def _set_wgt_update_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius - 2
        #
        self._frame_draw_rect.setRect(
            x, y, w, h
        )
        self._list_widget.setGeometry(
            x+1, y+1, w-2, h-2
        )
        self._list_widget.updateGeometries()

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_popup_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._list_widget._set_scroll_to_pre_item_()

    def _set_popup_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._list_widget._set_scroll_to_next_item_()

    def _set_popup_start_(self, *args, **kwargs):
        parent = self.parent()
        self._list_widget._set_clear_()
        name_texts = parent._get_value_entry_completion_data_()
        if name_texts:
            current_name_text = parent._get_item_value_()
            for index, i_name_text in enumerate(name_texts):
                i_item_widget = _QtHItem()
                i_item = QtListWidgetItem()
                i_item.setSizeHint(QtCore.QSize(self._item_width, self._item_height))
                #
                self._list_widget.addItem(i_item)
                self._list_widget.setItemWidget(i_item, i_item_widget)
                i_item._set_item_show_connect_()
                #
                i_item_widget._set_name_text_(i_name_text)
                i_item_widget._set_index_(index)
                #
                if current_name_text == i_name_text:
                    i_item.setSelected(True)

            press_pos = self._get_popup_pos_0_(parent)
            width, height = self._get_popup_size_(parent)
            height_max = self._list_widget._get_maximum_height_(self._item_count_maximum)

            self._set_popup_fnc_(
                press_pos,
                (width, height_max)
            )

            self._list_widget._set_scroll_to_selected_item_top_()

            self._popup_target_entry._set_focused_(True)

            self._popup_is_activated = True

    def _set_popup_end_(self, *args, **kwargs):
        parent = self.parent()
        selected_item_widget = self._list_widget._get_selected_item_widget_()
        if selected_item_widget:
            name_text = selected_item_widget._get_name_text_()
            parent._set_item_value_(name_text)
            parent._set_choose_changed_emit_send_()

        self._set_popup_activated_(False)


class _QtPopupGuideFrame(
    QtWidgets.QWidget,
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtPopupDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtPopupGuideFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setPalette(QtDccMtd.get_qt_palette())
        #
        self._set_frame_def_init_()
        self._set_popup_def_init_(self)
        #
        self.setFocusProxy(self.parent())
        #
        self._list_widget = _QtPopupListView(self)
        #
        self._item_count_maximum = 20
        self._item_width, self._item_height = 20, 20
        self._list_widget.setGridSize(QtCore.QSize(self._item_width, self._item_height))
        self._list_widget.setSpacing(2)
        self._list_widget.setUniformItemSizes(True)
        #
        self._choose_index = None
        #
        self._frame_border_color = QtBackgroundColor.Light
        self._hovered_frame_border_color = QtBackgroundColor.Hovered
        self._selected_frame_border_color = QtBackgroundColor.Selected
        #
        self._frame_background_color = QtBackgroundColor.Dark

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        painter = QtPainter(self)
        #
        painter._set_popup_frame_draw_(
            bck_rect,
            margin=self._popup_margin,
            side=self._popup_side,
            shadow_radius=self._popup_shadow_radius,
            region=self._popup_region,
            border_color=self._selected_frame_border_color,
            background_color=self._frame_background_color,
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self.parent():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_popup_close_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._set_popup_close_()
        elif widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._set_popup_end_()
        return False

    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius - 2
        #
        self._list_widget.setGeometry(
            v_x, v_y, v_w, v_h
        )
        self._list_widget.updateGeometries()

    def _set_popup_start_(self, index):
        parent = self.parent()
        content_name_texts = parent._get_guide_choose_item_content_name_texts_at_(index)
        if isinstance(content_name_texts, (tuple, list)):
            desktop_rect = get_qt_desktop_rect()
            #
            press_pos = parent._get_guide_choose_item_point_at_(index)
            press_rect = parent._get_guide_choose_item_rect_at_(index)
            #
            current_name_text = parent._get_view_guide_item_name_text_at_(index)
            #
            for seq, i_name_text in enumerate(content_name_texts):
                item_widget = _QtHItem()
                item = QtListWidgetItem()
                item.setSizeHint(QtCore.QSize(self._item_width, self._item_height))
                #
                self._list_widget.addItem(item)
                self._list_widget.setItemWidget(item, item_widget)
                item._set_item_show_connect_()
                #
                if i_name_text:
                    item_widget._set_name_text_(i_name_text)
                    item_widget._set_icon_name_text_(i_name_text[0])
                #
                item_widget._set_index_(seq)
                if current_name_text == i_name_text:
                    item.setSelected(True)
            #
            self.setFocus(QtCore.Qt.PopupFocusReason)
            #
            self._set_popup_fnc_0_(
                press_pos, press_rect,
                desktop_rect,
                self._get_maximum_width_(content_name_texts),
                self._get_maximum_height_()
            )
            self._choose_index = index
            parent._set_guide_choose_item_expand_at_(index)
            #
            self._list_widget._set_scroll_to_selected_item_top_()
            #
            self._list_widget.itemClicked.connect(
                self._set_popup_close_
            )

    def _set_popup_end_(self):
        if self._choose_index is not None:
            parent = self.parent()
            selected_item_widget = self._list_widget._get_selected_item_widget_()
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
                parent._set_view_item_geometries_update_()
            #
            parent._set_guide_choose_item_collapse_at_(self._choose_index)
            parent._set_view_guide_current_index_(self._choose_index)
            parent._set_view_guide_item_clicked_emit_send_()
            parent._set_view_guide_current_clear_()

    def _get_maximum_width_(self, texts):
        count = len(texts)
        texts.append(str(count))
        _ = max([self.fontMetrics().width(i) for i in texts]) + 32
        if count > self._item_count_maximum:
            return _ + 24
        return _

    def _get_maximum_height_(self):
        rects = [self._list_widget.visualItemRect(self._list_widget.item(i)) for i in range(self._list_widget.count())[:self._item_count_maximum]]
        rect = rects[-1]
        y = rect.y()
        h = rect.height()
        return y+h+1+4


class _QtEntryFrame(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract._QtStatusDef,
):
    # def _get_action_is_enable_(self):
    #     pass

    def _set_wgt_update_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtEntryFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._action_is_hovered = False
        self._is_focused = False
        self._entry_count = 1
        #
        self._set_status_def_init_()
        self._set_frame_def_init_()
        #
        self._frame_border_color = QtBackgroundColor.Light
        self._hovered_frame_border_color = QtBackgroundColor.Hovered
        self._selected_frame_border_color = QtBackgroundColor.Selected
        #
        self._frame_background_color = QtBackgroundColor.Dark

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_wgt_update_geometry_()
                self._set_wgt_update_draw_()
        return False

    def paintEvent(self, event):
        width, height = self.width(), self.height()
        #
        painter = QtPainter(self)
        #
        is_hovered = self._action_is_hovered
        is_selected = self._is_focused
        background_color = self._frame_background_color
        bdr_color = [self._frame_border_color, self._selected_frame_border_color][is_selected]
        for i_rect in self._frame_draw_rects:
            painter._set_frame_draw_by_rect_(
                i_rect,
                border_color=bdr_color,
                background_color=background_color,
                border_radius=2,
                # border_width=2,
            )

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self._set_wgt_update_draw_()

    def _set_entry_count_(self, size):
        self._entry_count = size
        self._frame_draw_rects = [QtCore.QRect() for i in range(size)]

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        # int left， int top， int right， int bottom
        m_l, m_t, m_r, m_b = self._frame_draw_margins
        spacing = 2

        c = self._entry_count

        f_x, f_y = x+m_l+1, y+m_t+1
        f_w, f_h = w-m_l-m_r-2, h-m_t-m_b-2
        if c > 1:
            f_d = f_w / c
            for i in range(c):
                if i == 0:
                    self._frame_draw_rects[i].setRect(
                        f_x+i*f_d, f_y, f_d - spacing, f_h
                    )
                elif (i+1) == c:
                    self._frame_draw_rects[i].setRect(
                        f_x+i*f_d+(spacing*i), f_y, f_d-spacing, f_h
                    )
                else:
                    self._frame_draw_rects[i].setRect(
                        f_x+i*f_d+(spacing*i), f_y, f_d-spacing, f_h
                    )
        else:
            self._frame_draw_rects[0].setRect(
                f_x, f_y, f_w, f_h
            )

    def _set_size_policy_height_fixed_mode_(self):
        self._value_entry_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )


class _QtVResizeFrame(
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
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._resize_draw_rect.setRect(
            x+1, y+1, w-2, h-2
        )
        i_w, i_h = self._resize_icon_file_draw_size
        self._resize_icon_file_draw_rect.setRect(
            x+(w-i_w)/2, y+(h-i_h)/2, i_w, i_h
        )

        self._frame_draw_rect.setRect(
            x+1, y+1, w-2, h-2
        )

    def __init__(self, *args, **kwargs):
        super(_QtVResizeFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.setMaximumHeight(10)
        self.setMinimumHeight(10)
        #
        self._set_frame_def_init_()
        self._set_resize_def_init_(self)

        self._set_action_def_init_(self)
        self._set_action_hover_def_init_()
        self._set_action_press_def_init_()
        #
        self._hovered_frame_border_color = QtBorderColor.Button
        self._hovered_frame_background_color = QtBackgroundColor.Button

        self._actioned_frame_border_color = QtBorderColor.Actioned
        self._actioned_frame_background_color = QtBackgroundColor.Actioned

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
                self._set_wgt_update_geometry_()
                self._set_wgt_update_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_action_flag_(
                    self.ActionFlag.SplitVClick
                )
                self._set_action_resize_move_start_(event)
                self._set_action_pressed_(True)
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_action_flag_(
                    self.ActionFlag.SplitVMove
                )
                self._set_action_resize_move_execute_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._set_action_resize_move_stop_(event)
                self._set_action_pressed_(False)
                self._set_action_flag_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)
        if self._action_is_enable is True:
            condition = self._action_is_hovered, self._action_is_pressed
            if condition == (False, False):
                border_color = QtBackgroundColor.Transparent
                background_color = QtBackgroundColor.Transparent
            elif condition == (False, True):
                border_color = self._actioned_frame_border_color
                background_color = self._actioned_frame_background_color
            elif condition == (True, True):
                border_color = self._actioned_frame_border_color
                background_color = self._actioned_frame_background_color
            elif condition == (True, False):
                border_color = self._hovered_frame_border_color
                background_color = self._hovered_frame_background_color
            else:
                raise SyntaxError()
        else:
            border_color = QtBackgroundColor.ButtonDisable
            background_color = QtBackgroundColor.ButtonDisable

        painter._set_frame_draw_by_rect_(
            rect=self._frame_draw_rect,
            border_color=border_color,
            background_color=background_color,
            border_radius=2,
        )
        painter._set_icon_file_draw_by_rect_(
            rect=self._resize_icon_file_draw_rect,
            file_path=self._resize_icon_file_path,
        )

    def _set_action_resize_move_start_(self, event):
        self._resize_point_start = event.pos()

    def _set_action_resize_move_execute_(self, event):
        if self._resize_target is not None:
            p = event.pos() - self._resize_point_start
            d_h = p.y()
            h_0 = self._resize_target.minimumHeight()
            h_1 = h_0+d_h
            if self._resize_minimum+10 <= h_1 <= self._resize_maximum+10:
                self._resize_target.setMinimumHeight(h_1)
                self._resize_target.setMaximumHeight(h_1)

    def _set_action_resize_move_stop_(self, event):
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
    def _set_wgt_update_draw_(self):
        self.update()

    def _set_wgt_update_geometry_(self):
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

        self._set_action_def_init_(self)
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
                self._set_wgt_update_geometry_()
                self._set_wgt_update_draw_()
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
                painter._set_frame_draw_by_rect_(
                    rect=self._help_frame_draw_rect,
                    border_color=(0, 0, 0),
                    background_color=(0, 0, 0, 127)
                )
                painter._set_text_draw_by_rect_(
                    rect=self._help_draw_rect,
                    text=self._help_text,
                    font=get_font(12),
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                    word_warp=True
                )
