# coding:utf-8
import six

import uuid

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_resize, _utl_gui_qt_wgt_filter, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_container, _utl_gui_qt_wgt_item_for_entry, _utl_gui_qt_wgt_chart, _utl_gui_qt_wgt_window

from lxutil_gui.proxy import utl_gui_prx_configure, utl_gui_prx_core, utl_gui_prx_abstract

from lxutil_gui import utl_gui_core

from lxbasic import bsc_configure

import lxutil.dcc.dcc_objects as utl_dcc_objects


class AbsPrxToolGroup(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtLine
    QT_HEAD_CLS = None
    QT_HEAD_SIZE = 22
    def __init__(self, *args, **kwargs):
        super(AbsPrxToolGroup, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignTop)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(2)
        # header
        self._qt_head = self.QT_HEAD_CLS()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.setFixedHeight(self.QT_HEAD_SIZE)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        self._qt_head.press_toggled.connect(self._qt_widget._set_pressed_)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(2, 0, 0, 0)
        qt_layout_1.setSpacing(2)
        #
        self._layout = qt_layout_1
        #
        self._qt_view = qt_widget_1
        #
        self._refresh_expand_()

    def _refresh_expand_(self):
        self._qt_view.setVisible(
            self.get_is_expanded()
        )

    def set_name(self, name):
        self._qt_head._set_name_text_(name)

    def set_icon_by_text(self, name):
        self._qt_head._set_icon_text_(name)

    def set_name_icon_enable(self, boolean):
        self._qt_head._set_icon_name_enable_(boolean)

    def set_expand_icon_file(self, icon_file_path_0, icon_file_path_1):
        self._qt_head._set_expand_icon_file_path_(
            icon_file_path_0, icon_file_path_1
        )

    def set_expand_icon_names(self, icon_name_0, icon_name_1):
        self._qt_head._set_expand_icon_names_(
            icon_name_0, icon_name_1
        )

    def set_expand_sub_icon_names(self, icon_name_0, icon_name_1):
        self._qt_head._set_expand_sub_icon_names_(
            icon_name_0, icon_name_1
        )

    def set_name_font_size(self, size):
        self._qt_head._set_name_font_size_(size)

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_()

    def set_head_visible(self, boolean):
        self._qt_head.setHidden(not boolean)

    def get_is_expanded(self):
        return self._qt_head._get_is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
            self._layout.addWidget(widget)
        else:
            qt_widget = widget.widget
        #
        if qt_widget != self.widget:
            #
            self._layout.addWidget(qt_widget)

    def set_layout_alignment_to_top(self):
        self._layout.setAlignment(
            utl_gui_qt_core.QtCore.Qt.AlignTop
        )

    def set_size_mode(self, mode):
        if mode == 0:
            self._qt_view.setSizePolicy(
                utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
            )
        elif mode == 1:
            self._qt_view.setSizePolicy(
                utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
            )

    def set_height_match_to_minimum(self):
        self._qt_view.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def connect_expand_changed_to(self, fnc):
        self._qt_head.expand_clicked.connect(fnc)

    def set_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()
        #
        rcs_fnc_(self._layout)


class PrxHToolGroup(AbsPrxToolGroup):
    QT_HEAD_CLS = _utl_gui_qt_wgt_container.QtHHeadFrame
    QT_HEAD_SIZE = 22
    def __init__(self, *args, **kwargs):
        super(PrxHToolGroup, self).__init__(*args, **kwargs)


class PrxHToolGroup_(AbsPrxToolGroup):
    QT_HEAD_SIZE = 20
    QT_HEAD_CLS = _utl_gui_qt_wgt_container.QtHHeadFrame_
    def __init__(self, *args, **kwargs):
        super(PrxHToolGroup_, self).__init__(*args, **kwargs)


class PrxHScrollArea(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtHScrollArea
    def __init__(self, *args, **kwargs):
        super(PrxHScrollArea, self).__init__(*args, **kwargs)
        self._layout = self.widget._layout

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._layout.addWidget(widget)
        else:
            self._layout.addWidget(widget.widget)

    def set_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()
        #
        rcs_fnc_(self._layout)

    def restore(self):
        self.set_clear()


class PrxVScrollArea(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtVScrollArea
    def __init__(self, *args, **kwargs):
        super(PrxVScrollArea, self).__init__(*args, **kwargs)
        self._qt_layout = self._qt_widget._layout

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget.widget)

    def set_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._qt_layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()
        #
        rcs_fnc_(self._qt_layout)

    def restore(self):
        self.set_clear()

    def set_margins(self, m_l, m_t, m_r, m_b):
        self._qt_layout.setContentsMargins(m_l, m_t, m_r, m_b)


class PrxHToolBar(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxHToolBar, self).__init__(*args, **kwargs)
        #
        self.widget.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def _set_build_(self):
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        # qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        # header
        self._qt_head = _utl_gui_qt_wgt_container.QtHExpandHead1()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head.setToolTip('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(*[0]*4)
        # qt_layout_1.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        self._qt_layout_0 = qt_layout_1
        #
        self._qt_view = qt_widget_1
        #
        self._refresh_expand_()
        #
        self._qt_view.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def _refresh_expand_(self):
        if self.get_is_expanded() is True:
            self._qt_head.setMaximumSize(self._wgt_w_min, self._wgt_h)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h)
            #
            self.widget.setMaximumHeight(self._wgt_h)
            self.widget.setMinimumHeight(self._wgt_h)
        else:
            self._qt_head.setMaximumSize(166667, self._wgt_h_min)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            #
            self.widget.setMaximumHeight(self._wgt_h_min)
            self.widget.setMinimumHeight(self._wgt_h_min)
        #
        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()

    def set_name(self, name):
        self._qt_head.set_name(name)

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_()

    def get_is_expanded(self):
        return self._qt_head._get_is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def set_width(self, w):
        self._wgt_w = w
        self._refresh_expand_()

    def set_height(self, h):
        self._wgt_h = h
        self._refresh_expand_()

    def get_qt_layout(self):
        return self._qt_layout_0

    def set_top_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.TopToBottom)

    def set_bottom_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.BottomToTop)

    def set_alignment_center(self):
        self._qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignHCenter)

    def set_left_alignment_mode(self):
        self._qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)

    def set_border_radius(self, radius):
        self._qt_head._set_frame_border_radius_(radius)


class PrxVToolBar(PrxHToolBar):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxVToolBar, self).__init__(*args, **kwargs)
        #
        self.widget.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )

    def _set_build_(self):
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        # header
        self._qt_head = _utl_gui_qt_wgt_container.QtVExpandHead1()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head.setToolTip('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(0, 0, 0, 0)
        qt_layout_1.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        self._qt_layout_0 = qt_layout_1
        #
        self._qt_view = qt_widget_1
        #
        self._refresh_expand_()
        #
        self._qt_view.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )

    def _refresh_expand_(self):
        if self.get_is_expanded() is True:
            self._qt_head.setMaximumSize(self._wgt_w_min, 166667)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            #
            self.widget.setMaximumWidth(self._wgt_w)
            self.widget.setMinimumWidth(self._wgt_w)
        else:
            self._qt_head.setMaximumSize(self._wgt_w_min, 166667)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            #
            self.widget.setMaximumWidth(self._wgt_w_min)
            self.widget.setMinimumWidth(self._wgt_w_min)
        #
        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()


class PrxLeftExpandedGroup(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_resize.QtHResizeFrame
    def __init__(self, *args, **kwargs):
        super(PrxLeftExpandedGroup, self).__init__(*args, **kwargs)
        #
        self.widget.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def _set_build_(self):
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12
        #
        self._qt_widget._resize_handle._set_resize_alignment_(
            self._qt_widget._resize_handle.ResizeAlignment.Right
        )
        self._qt_widget._resize_handle._set_resize_target_(self._qt_widget)
        self._qt_widget._resize_handle.size_changed.connect(self.__set_width)
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(*[0]*4)
        qt_layout_1.setSpacing(2)
        qt_layout_1.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        self._qt_view = qt_widget_1
        self._qt_layout_0 = qt_layout_1
        # header
        self._qt_head = _utl_gui_qt_wgt_item._QtHContractItem()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head.setToolTip('"LMB-click" to expand "on" / "off"')
        #
        self._refresh_expand_()
        #
        self._qt_view.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )

    def _refresh_expand_(self):
        if self.get_is_expanded() is True:
            self._qt_head.setMaximumSize(self._wgt_w_min, 166667)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            #
            self._qt_widget.setMaximumWidth(self._wgt_w)
            self._qt_widget.setMinimumWidth(self._wgt_w)
            self._qt_widget._resize_handle.show()
        else:
            self._qt_head.setMaximumSize(self._wgt_w_min, 166667)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            self._qt_widget._resize_handle.hide()
            #
            self._qt_widget.setMaximumWidth(self._wgt_w_min)
            self._qt_widget.setMinimumWidth(self._wgt_w_min)
        #
        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()

    def set_name(self, name):
        self._qt_head.set_name(name)

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_()

    def get_is_expanded(self):
        return self._qt_head._get_is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def set_width(self, w):
        self._wgt_w = w
        self._refresh_expand_()

    def __set_width(self, w):
        self._wgt_w = w

    def set_height(self, h):
        self._wgt_h = h
        self._refresh_expand_()

    def get_qt_layout(self):
        return self._qt_layout_0

    def set_top_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.TopToBottom)

    def set_bottom_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.BottomToTop)

    def set_border_radius(self, radius):
        self._qt_head._set_frame_border_radius_(radius)

    def connect_expand_changed_to(self, fnc):
        self._qt_head.expand_clicked.connect(fnc)


class PrxRightExpandedGroup(PrxLeftExpandedGroup):
    def __init__(self, *args, **kwargs):
        super(PrxRightExpandedGroup, self).__init__(*args, **kwargs)

    def _set_build_(self):
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12
        #
        self._qt_widget._resize_handle._set_resize_alignment_(
            self._qt_widget._resize_handle.ResizeAlignment.Left
        )
        self._qt_widget._resize_handle.size_changed.connect(self.__set_width)
        self._qt_widget._resize_handle._set_resize_target_(self._qt_widget)
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        # handle
        self._qt_head = _utl_gui_qt_wgt_item._QtHContractItem()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._set_expand_direction_(self._qt_head.CollapseDirection.LeftToRight)
        self._qt_head.setToolTip('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(*[0]*4)
        qt_layout_1.setSpacing(2)
        qt_layout_1.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        self._qt_view = qt_widget_1
        self._qt_layout_0 = qt_layout_1
        #
        self._refresh_expand_()
        #
        self._qt_view.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Minimum,
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )

    def __set_width(self, w):
        self._wgt_w = w


class PrxHToolBox(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxHToolBox, self).__init__(*args, **kwargs)

    def _set_build_(self):
        self._wgt_w, self._wgt_h = 24, 24
        self._wgt_w_min, self._wgt_h_min = 12, 24
        #
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        # header
        self._qt_head = _utl_gui_qt_wgt_container.QtHExpandHead2()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head.setToolTip('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = _utl_gui_qt_wgt_utility._QtTranslucentWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(*[0]*4)
        qt_layout_1.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignLeft)
        #
        self._qt_view = qt_widget_1
        self._qt_layout_0 = qt_layout_1
        #
        self._refresh_expand_()
        #
        self.set_size_mode(0)

    def _refresh_expand_(self):
        self.widget.setMaximumSize(self._wgt_w_min, self._wgt_h_min)
        self._qt_head.setMaximumSize(self._wgt_w_min, self._wgt_h)
        self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h)
        if self.get_is_expanded() is True:
            self.widget.setMaximumWidth(166667)
        else:
            self.widget.setMaximumWidth(self._wgt_w_min)
        #
        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()

    def set_name(self, name):
        self._qt_head.set_name(name)

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_()

    def get_is_expanded(self):
        return self._qt_head._get_is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget._qt_widget)

    def set_height(self, h):
        self._wgt_h = h
        self._refresh_expand_()

    def get_qt_layout(self):
        return self._qt_layout_0

    def set_top_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.TopToBottom)

    def set_bottom_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.BottomToTop)

    def set_border_radius(self, radius):
        self._qt_head._set_frame_border_radius_(radius)

    def set_size_mode(self, mode):
        # todo: fix size bug
        if mode == 0:
            self._qt_view.setSizePolicy(
                utl_gui_qt_core.QtWidgets.QSizePolicy.Fixed,
                utl_gui_qt_core.QtWidgets.QSizePolicy.Fixed
            )
        elif mode == 1:
            self._qt_view.setSizePolicy(
                utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                utl_gui_qt_core.QtWidgets.QSizePolicy.Fixed
            )


class PrxHToolBox_(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_container.QtHToolBox
    def __init__(self, *args, **kwargs):
        super(PrxHToolBox_, self).__init__(*args, **kwargs)

    def set_expanded(self, boolean):
        self._qt_widget._set_expanded_(boolean)

    def add_widget(self, widget):
        self._qt_widget._add_widget_(widget)


class PrxVToolBox_(PrxHToolBox_):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_container.QtVToolBox
    def __init__(self, *args, **kwargs):
        super(PrxVToolBox_, self).__init__(*args, **kwargs)


class Window(utl_gui_prx_abstract.AbsPrxWindow):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtMainWindow
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

    def _set_build_(self):
        self._qt_main_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._qt_main_widget)
        self._qt_main_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._qt_main_widget)

    def get_main_widget(self):
        return self._qt_main_widget

    def add_widget(self, widget):
        self._qt_main_layout.addWidget(widget)


class PrxLayerWidget(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    def __init__(self, *args, **kwargs):
        super(PrxLayerWidget, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(0)
        #
        qt_widget_0 = _utl_gui_qt_wgt_utility.QtHFrame()
        qt_widget_0.setMaximumHeight(24)
        qt_widget_0.setMinimumHeight(24)
        qt_layout_0.addWidget(qt_widget_0)
        #
        qt_top_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_widget_0)
        qt_top_layout_1.setContentsMargins(0, 0, 0, 0)
        qt_top_layout_1.setSpacing(0)
        self._qt_label_0 = _utl_gui_qt_wgt_utility.QtTextItem()
        self._qt_label_0._set_name_text_option_(
            utl_gui_qt_core.QtCore.Qt.AlignHCenter | utl_gui_qt_core.QtCore.Qt.AlignVCenter
        )
        self._qt_label_0._set_name_font_size_(12)
        qt_top_layout_1.addWidget(self._qt_label_0)
        self._button_0 = PrxIconPressItem()
        self._button_0.set_icon_name('close')
        qt_top_layout_1.addWidget(self._button_0.widget)

        self._qt_line = _utl_gui_qt_wgt_utility.QtHLine()
        qt_layout_0.addWidget(self._qt_line)
        self._qt_central_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_central_widget_0.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding, utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_layout_0.addWidget(self._qt_central_widget_0)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_central_widget_0)
        self._qt_layout_0.setContentsMargins(2, 2, 2, 2)

    def set_name(self, text):
        self._qt_label_0._set_name_text_(text)

    def set_status(self, status):
        self._qt_label_0._set_status_(status)

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget._qt_widget)

    def connect_close_to(self, method):
        self._button_0.widget.clicked.connect(method)
    @property
    def central_layout(self):
        return self._qt_layout_0

    def get_layout(self):
        return self._qt_layout_0

    def clear(self):
        layout = self._qt_layout_0
        c = layout.count()
        if c:
            for i in range(c):
                item = layout.itemAt(i)
                if item:
                    widget = item.widget()
                    widget.deleteLater()


class PrxLayer(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    #
    PRX_LAYER_WIDGET_CLS = PrxLayerWidget
    def __init__(self, *args, **kwargs):
        super(PrxLayer, self).__init__(*args, **kwargs)
        self._layer_widget = None

    def get_widget(self):
        return self._layer_widget

    def create_widget(self, key, label=None):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        self._layer_widget = self.PRX_LAYER_WIDGET_CLS()
        if label is None:
            label = bsc_core.RawTextMtd.to_prettify(key)
        self._layer_widget.set_name(label)
        qt_layout_0.addWidget(self._layer_widget.widget)
        return self._layer_widget


class PrxTextBrowser(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxTextBrowser, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        widget = _utl_gui_qt_wgt_item_for_entry.QtValueEntryAsContentEdit()
        widget._set_value_entry_enable_(False)
        qt_layout_0.addWidget(widget)
        self._qt_text_browser_0 = widget._value_entry

    def set_markdown_file_open(self, file_path):
        if file_path:
            import markdown
            with open(file_path) as f:
                raw = f.read()
                raw = raw.decode('utf-8')
                html = markdown.markdown(raw)
                self._qt_text_browser_0.setHtml(html)

    def set_add(self, text):
        if isinstance(text, six.string_types):
            self._qt_text_browser_0.append(
                text
            )

    def set_result_add(self, text):
        self._qt_text_browser_0.append(
            utl_gui_core.HtmlText.get_text(text)
        )

    def set_error_add(self, text):
        self._qt_text_browser_0.append(
            utl_gui_core.HtmlText.get_text(text, font_color=utl_gui_prx_configure.Html.RED)
        )

    def set_warning_add(self, text):
        self._qt_text_browser_0.append(
            utl_gui_core.HtmlText.get_text(text, font_color=utl_gui_prx_configure.Html.YELLOW)
        )

    def set_print_add(self, text):
        self._qt_text_browser_0._add_value_(text)

    def add_content_with_thread(self, text):
        self._qt_text_browser_0._add_value_with_thread_(text)

    def set_content_with_thread(self, text):
        self._qt_text_browser_0._set_value_with_thread_(text)

    def set_content(self, text, as_html=False):
        if as_html is True:
            self._qt_text_browser_0.setHtml(
                text
            )
        else:
            self._qt_text_browser_0.setText(
                text
            )

    def set_font_size(self, size):
        font = self.widget.font()
        font.setPointSize(size)
        self._qt_text_browser_0.setFont(font)

    def get_content(self, as_html=False):
        if as_html is True:
            return self._qt_text_browser_0.toHtml()
        return self._qt_text_browser_0.toPlainText()

    def set_status(self, status):
        self.widget._set_status_(status)


class PrxMenu(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtMenu
    def __init__(self, *args, **kwargs):
        super(PrxMenu, self).__init__(*args, **kwargs)

    def set_name(self, name):
        self.widget.setTitle(name)

    def set_setup(self, menu_raws):
        self.widget._set_menu_data_(menu_raws)

    def set_menu_data(self, menu_raws):
        self.widget._set_menu_data_(menu_raws)

    def set_menu_content(self, content):
        self.widget._set_menu_content_(content)

    def set_show(self, boolean=True):
        self.widget.popup(
            utl_gui_qt_core.QtGui.QCursor().pos()
        )


class PrxIconPressItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtIconPressItem
    def __init__(self, *args, **kwargs):
        super(PrxIconPressItem, self).__init__(*args, **kwargs)
        self.widget.setFixedSize(20, 20)

    def set_name(self, *args, **kwargs):
        self.widget._set_name_text_(*args, **kwargs)

    def set_icon_name(self, icon_name):
        self.widget._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(icon_name)
        )

    def set_icon_sub_name(self, icon_name):
        self.widget._set_icon_sub_file_path_(
            utl_gui_core.RscIconFile.get(icon_name)
        )

    def set_icon_by_text(self, text):
        self.widget._set_icon_text_(text)

    def set_icon_size(self, w, h):
        self.widget._set_icon_file_draw_size_(w, h)

    def set_icon_frame_size(self, w, h):
        self._qt_widget._set_icon_frame_draw_size_(w, h)

    def connect_press_clicked_to(self, fnc):
        self.widget.clicked.connect(fnc)

    def set_click(self):
        self.widget._send_press_clicked_emit_()

    def set_tool_tip(self, *args, **kwargs):
        self.widget._set_tool_tip_(*args, **kwargs)

    def set_action_enable(self, boolean):
        self._qt_widget._set_action_enable_(boolean)

    def set_menu_data(self, data):
        self._qt_widget._set_menu_data_(data)

    def set_menu_content(self, content):
        self._qt_widget._set_menu_content_(content)

    def connect_press_db_clicked_to(self, fnc):
        self._qt_widget.press_db_clicked.connect(fnc)


class PrxPressItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_item.QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxPressItem, self).__init__(*args, **kwargs)
        self.widget.setFixedHeight(20)

    def set_enable(self, boolean):
        self._qt_widget._set_action_enable_(boolean)

    def get_is_enable(self):
        return self._qt_widget._get_action_is_enable_()

    def set_check_enable(self, boolean):
        self.widget._set_check_action_enable_(boolean)
        self.widget.update()

    def get_is_checked(self):
        return self.widget._get_is_checked_()

    def set_checked(self, boolean):
        self._qt_widget._set_checked_(boolean)

    def set_option_click_enable(self, boolean):
        self._qt_widget._set_option_click_enable_(boolean)

    def set_icon_name(self, icon_name):
        self._qt_widget._set_icon_file_path_(
            bsc_core.RscIconFileMtd.get(icon_name)
        )

    def set_icon_by_color(self, color):
        self.widget._icon_color_rgb = color
        self.widget._icon_is_enable = True
        self.widget.update()

    def set_icon_by_text(self, text):
        self.widget._set_icon_text_(text)

    def set_icon_color_by_name(self, name):
        pass

    def set_width(self, w):
        self.widget.setMinimumWidth(w)

    def set_icon_size(self, w, h):
        self.widget._icon_draw_size = w, h

    def set_name(self, text):
        self.widget._set_name_text_(text)

    def set_tool_tip(self, raw):
        self.widget._set_tool_tip_(raw)

    def set_check_clicked_connect_to(self, fnc):
        self.widget.check_clicked.connect(fnc)

    def connect_press_clicked_to(self, fnc):
        self.widget.clicked.connect(fnc)

    def set_press_clicked(self):
        self.widget.clicked.emit()

    def set_option_click_connect_to(self, fnc):
        self.widget.option_clicked.connect(fnc)

    def set_click(self):
        self.widget._send_press_clicked_emit_()

    def set_status_enable(self, boolean):
        pass

    def set_status(self, status):
        self.widget.status_changed.emit(status)

    def set_status_at(self, index, status):
        self.widget.rate_status_update_at.emit(index, status)

    def set_statuses(self, element_statuses):
        self.widget._set_sub_process_statuses_(element_statuses)

    def set_finished_at(self, index, status):
        self.widget.rate_finished_at.emit(index, status)

    def set_initialization(self, count, status=bsc_configure.Status.Started):
        self.widget._set_sub_process_initialization_(count, status)


class PrxCheckItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_item.QtCheckItem
    def __init__(self, *args, **kwargs):
        super(PrxCheckItem, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(20)
        self.widget.setMinimumHeight(20)

    def set_check_icon_names(self, icon_name_0, icon_name_1):
        self.widget._set_check_icon_file_paths_(
            utl_gui_core.RscIconFile.get(icon_name_0),
            utl_gui_core.RscIconFile.get(icon_name_1)
        )


class PrxEnableItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtIconEnableItem
    def __init__(self, *args, **kwargs):
        super(PrxEnableItem, self).__init__(*args, **kwargs)
        self._qt_widget._set_size_(20, 20)

    def set_name(self, text):
        self._qt_widget._set_name_text_(text)

    def set_icon_name(self, icon_name):
        self._qt_widget._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(icon_name),
        )

    def set_tool_tip(self, text):
        self._qt_widget._set_tool_tip_(text)

    def set_checked(self, boolean):
        self._qt_widget._set_checked_(boolean)

    def execute_swap_check(self):
        self._qt_widget._execute_check_swap_()

    def get_checked(self):
        return self._qt_widget._get_is_checked_()

    def connect_check_clicked_to(self, fnc):
        self._qt_widget.check_clicked.connect(fnc)

    def connect_user_check_clicked_to(self, fnc):
        self._qt_widget.user_check_clicked.connect(fnc)

    def connect_check_clicked_as_exclusive_to(self, fnc):
        self._qt_widget.user_check_clicked_as_exclusive.connect(fnc)

    def connect_check_changed_as_exclusive_to(self, fnc):
        self._qt_widget.check_changed_as_exclusive.connect(fnc)

    def connect_check_swapped_as_exclusive_to(self, fnc):
        self._qt_widget.check_swapped_as_exclusive.connect(fnc)


class PrxFilterBar(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_filter.QtFilterBar
    def __init__(self, *args, **kwargs):
        super(PrxFilterBar, self).__init__(*args, **kwargs)

    def set_tip(self, text):
        self._qt_widget._set_filter_tip_(text)

    def get_enter_widget(self):
        return self._qt_widget._get_value_entry_()

    def set_filter_connect_to(self, proxy):
        proxy._set_filter_bar_(self)

    def get_keyword(self):
        return self.get_enter_widget()._get_value_()

    def get_keywords(self):
        return self._qt_widget._get_all_filter_keyword_texts_()

    def get_is_match_case(self):
        return self.widget._get_is_match_case_()

    def get_is_match_word(self):
        return self.widget._get_is_match_word_()

    def set_result_count(self, value):
        self.widget._set_filter_result_count_(value)

    def set_result_index(self, value):
        self.widget._set_filter_result_index_current_(value)

    def set_result_clear(self):
        self.widget._set_result_clear_()

    def restore(self):
        self._qt_widget._restore_()

    def set_entry_focus(self, boolean):
        self.widget._set_entry_focus_(boolean)

    def set_history_key(self, key):
        self._qt_widget._set_history_extra_key_(key)

    def set_history_filter_fnc(self, fnc):
        pass

    def set_completion_gain_fnc(self, fnc):
        self._qt_widget._set_completion_extra_gain_fnc_(fnc)


class PrxButtonGroup(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtLine
    def __init__(self, *args, **kwargs):
        super(PrxButtonGroup, self).__init__(*args, **kwargs)
        # self._qt_widget._set_line_draw_enable_(True)
        self._layout = _utl_gui_qt_wgt_utility.QtGridLayout(
            self._qt_widget
        )
        self._layout.setContentsMargins(8, 2, 0, 2)
        self._layout.setSpacing(4)

    def add_widget(self, widget, d=2):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._layout._add_widget_(widget, d)
        else:
            self._layout._add_widget_(widget.widget, d)


class PrxFramelessWindow(
    utl_gui_prx_abstract.AbsPrxWindow,
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_window._QtFramelessWindow
    def __init__(self, *args, **kwargs):
        super(PrxFramelessWindow, self).__init__(*args, **kwargs)
        self.widget.setWindowFlags(utl_gui_qt_core.QtCore.Qt.Window | utl_gui_qt_core.QtCore.Qt.FramelessWindowHint)


class PrxWindow(
    utl_gui_prx_abstract.AbsPrxWindow,
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_window._QtWindow
    def __init__(self, *args, **kwargs):
        super(PrxWindow, self).__init__(*args, **kwargs)


class PrxWindow_(
    utl_gui_prx_abstract.AbsPrxWindow,
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtMainWindow
    def __init__(self, *args, **kwargs):
        super(PrxWindow_, self).__init__(*args, **kwargs)


class PrxScreenshotFrame(
    utl_gui_prx_abstract.AbsPrxWidget
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtScreenshotFrame
    def __init__(self, *args, **kwargs):
        main_window = utl_gui_qt_core.QtDccMtd.get_active_window()
        super(PrxScreenshotFrame, self).__init__(main_window, *args, **kwargs)

    def set_start(self):
        self._qt_widget._set_screenshot_start_()

    def set_started_connect_to(self, fnc):
        self._qt_widget.screenshot_started.connect(fnc)

    def set_finished_connect_to(self, fnc):
        self._qt_widget.screenshot_finished.connect(fnc)

    def set_accepted_connect_to(self, fnc):
        self._qt_widget.screenshot_accepted.connect(fnc)
    @classmethod
    def set_save_to(cls, geometry, file_path):
        cls.QT_WIDGET_CLS._set_screenshot_save_to_(geometry, file_path)
