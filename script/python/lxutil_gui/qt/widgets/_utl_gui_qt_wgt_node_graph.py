# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt import utl_gui_qt_abstract

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item


class _QtNGGraphViewport(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtNGGraphViewport, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            pass
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        x, y = 0, 0
        width, height = self.width(), self.height()

        rect = QtCore.QRect(
            x, y, width, height
        )

        painter._set_border_color_(0, 0, 0, 0)
        painter._set_background_color_(127, 127, 127, 31)
        painter.drawRect(rect)


class AbsQtNGGraphActionDef(object):
    def _set_ng_graph_action_def_init_(self, widget):
        self._widget = widget

        self._ng_graph_translate_flag = False
        self._ng_graph_scale_flag = True

        self._ng_graph_translate_point = QtCore.QPoint(0, 0)
        #
        self._ng_graph_composite_matrix = bsc_core.Matrix33Opt.get_identity()
        #
        self._ng_graph_translate_x, self._ng_graph_translate_y = 0, 0
        #
        self._ng_graph_scale_x, self._ng_graph_scale_y = 1.0, 1.0
        self._ng_graph_scale_minimum_x, self._ng_graph_scale_minimum_y = 0.000001, 0.000001
        self._ng_graph_scale_maximum_x, self._ng_graph_scale_maximum_y = 100000.0, 100000.0
        self._ng_graph_scale_radix_x, self._ng_graph_scale_radix_y = 0.25, 0.25
        #
        self._ng_graph_width, self._ng_graph_height = 2000, 2000
        #
        self._ng_graph_point_0 = QtCore.QPoint(0, 0)
        self._ng_graph_point_1 = QtCore.QPoint(
            self._ng_graph_width*self._ng_graph_scale_x, self._ng_graph_height*self._ng_graph_scale_y
        )
        self._ng_rect = QtCore.QRect(
            0, 0,
            self._ng_graph_width, self._ng_graph_height
        )

    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_ng_graph_action_update_(self):
        x_0, y_0 = self._ng_graph_point_0.x(), self._ng_graph_point_0.y()
        x_1, y_1 = self._ng_graph_point_1.x(), self._ng_graph_point_1.y()
        r_w, r_h = x_1-x_0, y_1-y_0
        #
        self._ng_graph_translate_x, self._ng_graph_translate_y = x_0, y_0
        #
        self._ng_graph_scale_x, self._ng_graph_scale_y = (
            r_w/float(self._ng_graph_width), r_h/float(self._ng_graph_height)
        )
        self._ng_rect.setRect(
            x_0, y_0, r_w, r_h
        )

    def _set_ng_graph_action_translate_start_(self, event):
        self._ng_graph_translate_point = event.pos()
        self._ng_graph_translate_flag = True
        self._set_widget_update_()

    def _set_ng_graph_action_translate_execute_(self, event):
        point = event.pos()
        #
        d_p = point - self._ng_graph_translate_point
        d_t_x, d_t_y = d_p.x(), d_p.y()
        self.__set_ng_graph_translate_(d_t_x, d_t_y)
        self.__set_ng_graph_transformation_update_()
        #
        self._ng_graph_translate_point = point
        #
        self._set_widget_update_()

    def _set_ng_graph_action_translate_stop_(self, event):
        self._ng_graph_translate_point = event.pos()
        self._ng_graph_translate_flag = False
        self._set_widget_update_()

    def _set_ng_graph_action_scale_execute_(self, event):
        if self._ng_graph_scale_flag is True:
            delta = event.angleDelta().y()
            point = event.pos()
            #
            if delta > 0:
                d_s_x, d_s_y = 1 + self._ng_graph_scale_radix_x, 1 + self._ng_graph_scale_radix_y
            else:
                d_s_x, d_s_y = 1/(1 + self._ng_graph_scale_radix_x), 1/(1 + self._ng_graph_scale_radix_y)
            #
            c_x, c_y = point.x(), point.y()
            #
            self.__set_ng_graph_scale_(c_x, c_y, d_s_x, d_s_y)
            self.__set_ng_graph_transformation_update_()
            #
            self._ng_graph_translate_point = point
            #
            self._set_widget_update_()
    #
    def _get_ng_graph_scale_(self):
        return self._ng_graph_scale_x, self._ng_graph_scale_y
    #
    def __set_ng_graph_translate_(self, d_t_x, d_t_y):
        m = self._ng_graph_composite_matrix
        #
        m_t = bsc_core.Matrix33Opt.get_default()
        m_t = bsc_core.Matrix33Opt.set_identity(m_t)
        #
        m_t[0][2] = d_t_x
        m_t[1][2] = d_t_y
        #
        self._ng_graph_composite_matrix = bsc_core.Matrix33Opt(m_t).set_multiply_to(m)
    #
    def __set_ng_graph_scale_(self, c_x, c_y, d_s_x, d_s_y):
        m = self._ng_graph_composite_matrix
        #
        s_m = bsc_core.Matrix33Opt.get_default()
        s_m = bsc_core.Matrix33Opt.set_identity(s_m)
        #
        s_m[0][0] = d_s_x
        s_m[0][2] = (1 - d_s_x)*c_x
        #
        s_m[1][1] = d_s_y
        s_m[1][2] = (1 - d_s_y)*c_y
        #
        self._ng_graph_composite_matrix = bsc_core.Matrix33Opt(s_m).set_multiply_to(m)
    #
    def __set_ng_graph_transformation_update_(self):
        m = self._ng_graph_composite_matrix
        #
        self.__set_ng_graph_point_update_bt_matrix_(
            self._ng_graph_point_0, m
        )
        #
        self.__set_ng_graph_point_update_bt_matrix_(
            self._ng_graph_point_1, m
        )
        #
        self._ng_graph_composite_matrix = bsc_core.Matrix33Opt.set_identity(m)
    @staticmethod
    def __set_ng_graph_point_update_bt_matrix_(point, matrix):
        i_x_0, i_y_0 = point.x(), point.y()
        i_x_0_, i_y_0_ = (
            matrix[0][0] * i_x_0 + matrix[0][1] * i_y_0 + matrix[0][2],
            matrix[1][0] * i_x_0 + matrix[1][1] * i_y_0 + matrix[1][2]
        )
        point.setX(i_x_0_); point.setY(i_y_0_)


class AbsQtNGGraphDrawDef(object):
    def _set_ng_graph_draw_def_init_(self, widget):
        self._widget = widget

        self._ng_graph_draw_grid_enable = True
        self._ng_graph_draw_grid_axis_enable = False
        self._ng_graph_draw_grid_mark_enable = False
        
        #
        self._ng_graph_draw_grid_translate_direction_x, self._ng_graph_draw_grid_translate_direction_y = 1, -1
        self._ng_graph_draw_grid_translate_x, self._ng_graph_draw_grid_translate_y = 0, 0

    def _set_ng_graph_draw_update_(self, t_x, t_y):
        self._ng_graph_draw_grid_translate_x, self._ng_graph_draw_grid_translate_y = (
            t_x * self._ng_graph_draw_grid_translate_direction_x,
            t_y * self._ng_graph_draw_grid_translate_direction_y
        )
    @classmethod
    def _set_ng_graph_position_mark_draw_(cls, painter, rect, string, font_color):
        width, height = rect.width(), rect.height()
        rect_ = QtCore.QRect(4, 0, width, height - 4)
        #
        painter._set_font_color_(font_color)
        painter.setFont(get_font(size=10, weight=75))
        painter.drawText(rect_, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, string)
    @classmethod
    def _set_ng_graph_press_key_mark_draw_(cls, painter, rect, key, font_color):
        width, height = rect.width(), rect.height()
        rect_ = QtCore.QRect(width - 120 - 4, 0, 120, height - 4)
        #
        painter._set_font_color_(font_color)
        painter.setFont(get_font(size=10, weight=75))
        painter.drawText(rect_, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom, key)


class AbsQtNGGraphNodeDef(object):
    def _set_ng_graph_node_def_init_(self, widget):
        self._widget = widget

        self._ng_graph_nodes = []

    def _set_ng_graph_node_add_(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_ng_graph_nodes_(self):
        return self._ng_graph_nodes

    def _set_ng_graph_nodes_update_(self):
        for i_ng_node in self._get_ng_graph_nodes_():
            i_ng_node._set_widget_update_()


class _QtNGGraph(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtGridDef,
    AbsQtNGGraphNodeDef,
    #
    AbsQtNGGraphActionDef,
    AbsQtNGGraphDrawDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtNGGraph, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        #
        self._set_grid_def_init_(self)
        self._grid_axis_lock_x, self._grid_axis_lock_y = 1, 1
        #
        self._set_ng_graph_node_def_init_(self)
        #
        self._set_ng_graph_action_def_init_(self)
        self._set_ng_graph_draw_def_init_(self)

        self._ng_graph_viewport = _QtNGGraphViewport(self)

    def _set_widget_update_(self):
        self._set_ng_graph_action_update_()
        #
        self._set_ng_graph_draw_update_(
            self._ng_graph_translate_x, self._ng_graph_translate_y
        )
        self._set_ng_graph_geometry_update_(
            self._ng_rect
        )
        #
        self._set_ng_graph_nodes_update_()
        #
        self._widget.update()

    def _set_ng_graph_geometry_update_(self, rect):
        self._ng_graph_viewport.setGeometry(
            rect
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_widget_update_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._move_flag = True
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_ng_graph_action_translate_start_(event)
                    # Zoom
                    self._zoom_scale_flag = False
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._move_flag = False
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_ng_graph_action_translate_stop_(event)
                    self._ng_graph_scale_flag = True
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._move_flag is True:
                        #
                        self.update()
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    # Track
                    if self._ng_graph_translate_flag is True:
                        self._set_ng_graph_action_translate_execute_(event)
                else:
                    event.ignore()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                if self._ng_graph_scale_flag is True:
                    self._set_ng_graph_action_scale_execute_(event)
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_item._QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_item._QtEntryFrame):
                    parent._set_focused_(False)
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        x, y = 0, 0
        width, height = self.width(), self.height()

        rect = QtCore.QRect(
            x, y, width, height
        )
        if self._ng_graph_draw_grid_enable is True:
            painter._set_grid_draw_(
                rect,
                (self._grid_dir_x, self._grid_dir_y),
                (self._grid_width, self._grid_height),
                (self._ng_graph_draw_grid_translate_x, self._ng_graph_draw_grid_translate_y),
                (self._grid_offset_x, self._grid_offset_y),
                self._grid_border_color
            )
        if self._ng_graph_draw_grid_axis_enable is True:
            painter._set_grid_axis_draw_(
                rect,
                (self._grid_dir_x, self._grid_dir_y),
                (self._ng_graph_draw_grid_translate_x, self._ng_graph_draw_grid_translate_y),
                (self._grid_offset_x, self._grid_offset_y),
                (self._grid_axis_lock_x, self._grid_axis_lock_y),
                (self._grid_axis_border_color_x, self._grid_axis_border_color_y)
            )
        if self._ng_graph_draw_grid_mark_enable is True:
            painter._set_grid_mark_draw_(
                rect,
                (self._grid_dir_x, self._grid_dir_y),
                (self._grid_width, self._grid_height),
                (self._ng_graph_draw_grid_translate_x, self._ng_graph_draw_grid_translate_y),
                (self._grid_offset_x, self._grid_offset_y),
                (self._ng_graph_scale_x, self._ng_graph_scale_y),
                (self._grid_value_offset_x, self._grid_value_offset_y),
                self._grid_mark_border_color,
                self._grid_value_show_mode
            )

        string = 'translate: {}, {}\nscale: {}, {}'.format(
            self._ng_graph_translate_x, self._ng_graph_translate_y,
            self._ng_graph_scale_x, self._ng_graph_scale_y
        )
        self._set_ng_graph_position_mark_draw_(
            painter, rect, string, QtFontColor.Basic
        )

    def _set_ng_graph_universe_(self, universe):
        self._ng_graph_universe = universe

    def _set_ng_graph_node_add_(self, *args, **kwargs):
        ng_node = _QtNGNode(self._ng_graph_viewport)
        self._ng_graph_nodes.append(ng_node)
        ng_node._set_ng_node_graph_(self)
        return ng_node

    def _set_ng_graph_node_show_(self):
        nodes = self._ng_graph_universe.get_objs()
        for i_node in nodes:
            i_ng_node = self._set_ng_graph_node_add_()
            i_ng_node._set_name_text_(
                i_node.path
            )
            i_ng_node._set_icon_name_text_(
                i_node.type_name
            )

        self._set_ng_graph_node_layout_()

    def _set_ng_graph_node_layout_(self):
        for i, i_ng_node in enumerate(self._get_ng_graph_nodes_()):
            i_ng_node._set_ng_node_point_(
                i*160, i*40
            )
            i_ng_node._set_widget_update_()

    def _set_ng_graph_node_move_(self, d_point):
        pass


class AbsQtNGNodeActionDef(object):
    def _set_ng_node_action_def_init_(self, widget):
        self._widget = widget

        self._ng_node_point = QtCore.QPoint(0, 0)
        #
        self._ng_node_move_point = QtCore.QPoint(0, 0)

        self._ng_node_move_flag = False

        self._ng_node_graph = None

        self._ng_node_translate_x, self._ng_node_translate_y = 0, 0
        self._ng_node_width, self._ng_node_height = 192, 48

    def _set_widget_update_(self):
        raise NotImplementedError()

    def _set_ng_node_action_update_(self):
        (x, y), (w, h) = self._get_ng_node_local_pos_(), self._get_ng_node_local_size_()
        #
        self._widget.setGeometry(
            x, y,
            w, h
        )

    def _set_ng_node_graph_(self, widget):
        self._ng_node_graph = widget

    def _set_ng_node_translate_(self, x, y):
        self._ng_node_translate_x, self._ng_node_translate_y = x, y
        self._set_ng_node_action_update_()

    def _get_ng_node_translate_(self):
        return self._ng_node_translate_x, self._ng_node_translate_y

    def _set_ng_node_point_(self, x, y):
        t_x, t_y = self._get_ng_node_translate_()
        s_x, s_y = self._ng_node_graph._get_ng_graph_scale_()
        self._ng_node_point.setX((x - t_x)/s_x), self._ng_node_point.setY((y - t_y)/s_y)
    #
    def _get_ng_node_local_pos_(self):
        t_x, t_y = self._get_ng_node_translate_()
        s_x, s_y = self._ng_node_graph._get_ng_graph_scale_()
        return self._ng_node_point.x()*s_x + t_x, self._ng_node_point.y()*s_y + t_y
    #
    def _get_ng_node_local_size_(self):
        s_x, s_y = self._ng_node_graph._get_ng_graph_scale_()
        return self._ng_node_width*s_x, self._ng_node_height*s_y

    def _set_ng_node_action_move_start_(self, event):
        self._ng_node_move_point = event.globalPos()
        self._ng_node_move_point -= self._widget.pos()
        #
        self._ng_node_move_flag = True
        self._set_widget_update_()

    def _set_ng_node_action_move_execute_(self, event):
        if self._ng_node_move_flag is True:
            d_point = event.globalPos() - self._ng_node_move_point
            self._set_ng_node_move_(d_point)
            self._ng_node_graph._set_ng_graph_node_move_(
                d_point
            )
        #
        self._set_widget_update_()

    def _set_ng_node_move_(self, d_point, offset_point=None):
        if not offset_point:
            offset_point = QtCore.QPoint()
        #
        d_point = d_point - offset_point
        x, y = d_point.x(), d_point.y()
        #
        self._widget.move(x, y)
        # self._updateConnection()
        #
        self._set_ng_node_point_(x, y)

    def _set_ng_node_action_move_stop_(self, event):
        self._ng_node_move_flag = False
        self._set_widget_update_()


class AbsQtNGNodeDrawDef(object):
    def _set_ng_node_draw_def_init_(self, widget):
        self._widget = widget

    def _set_widget_update_(self):
        raise NotImplementedError()


class _QtNGNode(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract.AbsQtFrameDef,
    utl_gui_qt_abstract.AbsQtNameDef,
    utl_gui_qt_abstract.AbsQtIconDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtHoverActionDef,
    utl_gui_qt_abstract.AbsQtPressActionDef,
    #
    AbsQtNGNodeActionDef,
    AbsQtNGNodeDrawDef,
):
    def _get_action_flag_(self):
        pass

    def _get_action_flag_is_match_(self, flag):
        pass

    def __init__(self, *args, **kwargs):
        super(_QtNGNode, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._set_frame_def_init_()
        self._set_name_def_init_()
        self._set_icon_def_init_()
        #
        self._set_action_def_init_(self)
        self._set_hover_action_def_init_()
        self._set_press_action_def_init_()

        self._set_ng_node_action_def_init_(self)
        self._set_ng_node_draw_def_init_(self)

        self._ng_node_draw_font_size = 8
        self._ng_node_draw_border_width = 2
        self._ng_node_draw_border_radius = 2

    def _set_widget_update_(self):
        self._set_ng_node_action_update_()
        self._set_ng_node_geometry_update_()
        #
        self.update()

    def _set_ng_node_geometry_update_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        self._ng_node_draw_border_width = i_s = h/32

        i_x, i_y = x+i_s, y+i_s
        i_w, i_h = w-i_s*2, (h-i_s*2)/2

        self._ng_node_draw_border_radius = i_h/2
        self._ng_node_draw_font_size = i_h/2

        self._set_name_rect_(
            i_x, i_y, i_w, i_h
        )
        self._set_frame_rect_(
            i_x, i_y+i_h, i_w, i_h
        )
        self._set_icon_name_text_rect_(
            i_x+i_s, i_y+i_h+i_s, i_h-i_s*2, i_h-i_s*2
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._set_hover_action_execute_(event)
            #
            if event.type() == QtCore.QEvent.Resize:
                self._set_widget_update_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_ng_node_action_move_start_(event)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_ng_node_action_move_stop_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._set_ng_node_action_move_execute_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)

        offset = 0

        painter._set_frame_draw_by_rect_(
            self._frame_rect,
            border_color=(191, 191, 191, 255),
            background_color=(191, 191, 191, 127),
            border_width=self._ng_node_draw_border_width,
            border_radius=self._ng_node_draw_border_radius,
            offset=offset
        )

        if self._name_text is not None:
            painter._set_text_draw_by_rect_(
                self._name_rect,
                self._name_text,
                font=get_font(size=self._ng_node_draw_font_size),
                font_color=QtFontColor.Basic,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                offset=offset
            )

        if self._icon_name_text is not None:
            painter._set_icon_name_text_draw_by_rect_(
                self._icon_name_text_rect,
                self._icon_name_text,
                offset=offset,
                border_width=self._ng_node_draw_border_width,
                border_radius=self._ng_node_draw_border_radius
            )

