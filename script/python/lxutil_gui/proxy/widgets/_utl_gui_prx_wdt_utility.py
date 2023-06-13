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


class PrxExpandedGroup(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtLine
    def __init__(self, *args, **kwargs):
        super(PrxExpandedGroup, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setAlignment(utl_gui_qt_core.QtCore.Qt.AlignTop)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(2)
        # header
        self._qt_head = _utl_gui_qt_wgt_container.QtHExpandHead0()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.setMaximumHeight(22)
        self._qt_head.setMinimumHeight(22)
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
        self._qt_view.setVisible(self.get_is_expanded())

    def set_name(self, name):
        self._qt_head._set_name_text_(name)

    def set_icon_by_name(self, name):
        self._qt_head._set_icon_name_text_(name)

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

    def set_alignment_left(self):
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
        self._main_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._main_widget)
        self._main_layout = _utl_gui_qt_wgt_utility.QtHBoxLayout(self._main_widget)

    def get_main_widget(self):
        return self._main_widget

    def add_widget(self, widget):
        self._main_layout.addWidget(widget)


class ContentWidget(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(ContentWidget, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._qt_label_0._set_name_text_(text)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(0)
        #
        qt_top_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        qt_top_widget_0.setMaximumHeight(24)
        qt_top_widget_0.setMinimumHeight(24)
        qt_layout_0.addWidget(qt_top_widget_0)
        #
        qt_top_layout_1 = _utl_gui_qt_wgt_utility.QtHBoxLayout(qt_top_widget_0)
        self._qt_label_0 = _utl_gui_qt_wgt_utility.QtTextItem()
        self._qt_label_0._set_name_text_option_(
            utl_gui_qt_core.QtCore.Qt.AlignHCenter | utl_gui_qt_core.QtCore.Qt.AlignVCenter
        )
        self._qt_label_0._set_name_font_size_(12)
        qt_top_layout_1.addWidget(self._qt_label_0)
        self._button_0 = PrxIconPressItem()
        self._button_0.set_icon_name('close')
        qt_top_layout_1.addWidget(self._button_0.widget)

        self._qt_central_widget_0 = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_central_widget_0.setSizePolicy(
            utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding, utl_gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_layout_0.addWidget(self._qt_central_widget_0)
        self._qt_central_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_central_widget_0)
        self._qt_central_layout.setContentsMargins(0, 0, 0, 0)

    def add_widget(self, widget):
        self._qt_central_layout.addWidget(widget)

    def set_close_connect_to(self, method):
        self._button_0.widget.clicked.connect(method)
    @property
    def central_widget(self):
        return self._qt_central_widget_0
    @property
    def central_layout(self):
        return self._qt_central_layout


class PrxTextBrowser(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtWidget
    def __init__(self, *args, **kwargs):
        super(PrxTextBrowser, self).__init__(*args, **kwargs)

    def _set_build_(self):
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self.widget)
        widget = _utl_gui_qt_wgt_item_for_entry.QtValueEntryAsContentEdit()
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

    def set_menu_raw(self, menu_raws):
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
        self.widget.setMaximumSize(20, 20)
        self.widget.setMinimumSize(20, 20)

    def set_name(self, *args, **kwargs):
        self.widget._set_name_text_(*args, **kwargs)

    def set_icon_name(self, icon_name):
        self.widget._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(icon_name)
        )

    def set_sub_icon_name(self, icon_name):
        self.widget._set_icon_sub_file_path_(
            utl_gui_core.RscIconFile.get(icon_name)
        )

    def set_icon_by_name(self, text):
        self.widget._set_icon_name_text_(text)

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


class PrxPressItem(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_item.QtPressItem
    def __init__(self, *args, **kwargs):
        super(PrxPressItem, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(20)
        self.widget.setMinimumHeight(20)

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

    def set_icon_by_name(self, text):
        self.widget._set_icon_name_text_(text)

    def set_icon_color_by_name(self):
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
        self._qt_widget._set_line_draw_enable_(True)
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


class PrxToolWindow(
    utl_gui_prx_abstract.AbsPrxWindow,
    #
    utl_gui_prx_abstract.AbsWidgetContentDef,
    #
    utl_gui_prx_abstract.AbsPrxProgressingDef,
    utl_gui_prx_abstract.AbsPrxWaitingDef,
):
    PRX_CATEGORY = 'tool_window'
    PRX_TYPE = 'tool_window'
    #
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtMainWindow
    #
    CONTENT_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtWidget
    PROGRESS_WIDGET_CLS = _utl_gui_qt_wgt_utility.QtProgressBar
    #
    QT_WAITING_CHART_CLS = _utl_gui_qt_wgt_chart.QtWaitingChart
    QT_PROGRESSING_CHART_CLS = _utl_gui_qt_wgt_chart.QtProgressingChart
    #
    HELP_FILE_PATH = None
    def __init__(self, *args, **kwargs):
        super(PrxToolWindow, self).__init__(*args, **kwargs)
        #
        self.set_log_file_path(bsc_core.StgUserMtd.get_log_directory())
        #
        self._log_file_path = None
        #
        utl_gui_qt_core.set_qt_log_connect_create()
        #
        utl_gui_qt_core.set_qt_progress_connect_create()
        #
        utl_gui_qt_core.set_log_writer_connect()

        self._qt_widget._create_window_shortcut_action_(
            self.show_help, 'F1'
        )
        #
        self.set_show_menu_raw(
            [
                ('log', 'log', self.set_log_unit_show),
                ('help', 'help', self.show_help)
            ]
        )

    def _set_build_(self):
        self._is_loading = False
        # menu bar
        self._qt_menu_bar_0 = _utl_gui_qt_wgt_utility.QtMenuBar()
        self._qt_widget.setMenuBar(self._qt_menu_bar_0)
        self._menu_0 = PrxMenu(self._qt_menu_bar_0)
        self._menu_0.set_name('show')
        self._qt_menu_bar_0.addMenu(self._menu_0.widget)
        #
        self._qt_central_widget = _utl_gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._qt_central_widget)
        #
        self._set_progressing_def_init_()
        #
        self._qt_central_layout = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_central_widget)
        # progress-bar
        #
        self._set_widget_content_def_init_(self._qt_central_layout)
        #
        self._set_cnt_wdt_0_build_()
        self._set_cnt_wdt_1_build_()
        self._set_cnt_wdt_2_build_()
        self._set_cnt_wdt_3_build_()
        self._set_cnt_wdt_4_build_()
        self._set_cnt_wdt_5_build_()
        self._set_cnt_wdt_6_build_()
        #
        self._set_waiting_def_init_()
        #
        self.set_current_unit('main_0')

    def set_menu_add(self, name):
        menu = PrxMenu(self._qt_menu_bar_0)
        menu.set_name(name)
        self._qt_menu_bar_0.addMenu(menu.widget)
        return menu
    # main
    def _set_cnt_wdt_0_build_(self):
        # content_widget_0
        qt_widget_0 = self.create_content_widget('main_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        # central widget
        self._main_widget = _utl_gui_qt_wgt_utility.QtVScrollArea()
        qt_layout_0.addWidget(self._main_widget)
        self._main_layout = self._main_widget._layout
        # bottom bar
        self._expanded_bar_1 = PrxHToolBar()
        qt_layout_0.addWidget(self._expanded_bar_1.widget)
        self._expanded_bar_1.set_expanded(True)
        self._expanded_bar_1.set_hide()
        self._expanded_bar_1.set_bottom_direction()
        #
        self._log_expand_bar = PrxHToolBar()
        qt_layout_0.addWidget(self._log_expand_bar.widget)
        self._log_expand_bar.set_height(120)
        self._log_text_browser_0 = PrxTextBrowser()
        self._log_expand_bar.add_widget(self._log_text_browser_0)
        self._log_expand_bar.set_bottom_direction()
        #
        self._progress_maximum = 10
        self._progress_value = 0
    # option
    def _set_cnt_wdt_1_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self.create_content_widget('option_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        self._option_unit_0 = ContentWidget()
        self._option_unit_0.set_name('Option(s)')
        qt_layout_0.addWidget(self._option_unit_0.widget)
        self._option_unit_0.set_close_connect_to(fnc_)
        #
        self._option_unit_layout_0 = self._option_unit_0.central_layout
    # log
    def _set_cnt_wdt_2_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self.create_content_widget('log_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        content_widget_0 = ContentWidget()
        content_widget_0.set_name('log')
        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)
        #
        self._log_text_browser = PrxTextBrowser()
        content_widget_0.add_widget(self._log_text_browser.widget)
    # help
    def _set_cnt_wdt_3_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self.create_content_widget('help_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        content_widget_0 = ContentWidget()
        content_widget_0.set_name('help')
        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)
        #
        self._help_text_browser = PrxTextBrowser()
        content_widget_0.add_widget(self._help_text_browser.widget)
    # loading
    def _set_cnt_wdt_4_build_(self):
        def fnc_():
            self.set_current_unit('main_0')

        qt_widget_0 = self.create_content_widget('window_loading_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)

        content_widget_0 = ContentWidget()
        # content_widget_0.set_name('loading')

        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)
    # exception
    def _set_cnt_wdt_5_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self.create_content_widget('exception_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        content_widget_0 = ContentWidget()
        content_widget_0.set_name('exception')
        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)
        #
        self._exception_text_browser = PrxTextBrowser()
        self._exception_text_browser.set_font_size(10)
        content_widget_0.add_widget(self._exception_text_browser.widget)
    # message
    def _set_cnt_wdt_6_build_(self):
        def fnc_():
            self.set_current_unit('main_0')
        #
        qt_widget_0 = self.create_content_widget('message_0')
        qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(qt_widget_0)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        #
        content_widget_0 = ContentWidget()
        content_widget_0.set_name('message')
        qt_layout_0.addWidget(content_widget_0.widget)
        content_widget_0.set_close_connect_to(fnc_)
        #
        self._message_text_browser = PrxTextBrowser()
        self._message_text_browser.set_font_size(12)
        content_widget_0.add_widget(self._message_text_browser.widget)

    def get_main_widget(self):
        return self._main_widget

    def get_central_widget(self):
        return self._qt_central_widget

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            self._main_layout.addWidget(widget)
        else:
            self._main_layout.addWidget(widget.widget)

    def set_qt_widget_add(self, qt_widget):
        self._main_layout.addWidget(qt_widget)

    def set_button_add(self, widget):
        self._expanded_bar_1.add_widget(widget)
        self._expanded_bar_1.set_show()

    def set_show_menu_raw(self, menu_raw):
        if menu_raw:
            menu = self._menu_0
            menu.set_setup(menu_raw)

    def set_option_unit_name(self, text):
        self._option_unit_0.set_name(text)

    def set_option_unit_show(self):
        self.set_current_unit('option_0')

    def set_option_unit_hide(self):
        self.set_current_unit('main_0')

    def get_option_unit_layout(self):
        return self._option_unit_layout_0

    def set_option_unit_clear(self):
        layout = self._option_unit_layout_0
        c = layout.count()
        if c:
            for i in range(c):
                item = layout.itemAt(i)
                if item:
                    widget = item.widget()
                    widget.deleteLater()
    # loading
    def set_window_loading_show(self):
        utl_gui_qt_core.set_qt_window_show(
            self.widget,
            size=self.get_definition_window_size()
        )

    def set_loading_start(self, time, method):
        def method_fnc_():
            self.set_window_loading_end()
            method()
        #
        self._is_loading = True
        self._loading_index = 0
        self.set_current_unit('window_loading_0')
        #
        self.start_waiting(auto_stop_time=time)
        #
        self._loading_timer_start = utl_gui_qt_core.QtCore.QTimer(self.widget)
        self._loading_timer_start.singleShot(time, method_fnc_)

        self._loading_show_timer = utl_gui_qt_core.QtCore.QTimer(self.widget)
        self._loading_show_timer.singleShot(int(time*.8), self.set_window_loading_show)

    def set_window_loading_end(self):
        utl_gui_qt_core.set_qt_window_show(
            self.widget, size=self.get_definition_window_size()
        )
        #
        self.set_current_unit('main_0')
        #
        self._is_loading = False
    # log
    def set_log_unit_show(self):
        self.set_current_unit('log_0')
        #
        context = self._log_text_browser_0.get_content()
        self._log_text_browser.set_content(context)

    def get_log_bar(self):
        return self._log_expand_bar

    def get_log_text_browser(self):
        return self._log_text_browser_0

    def set_log_add(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.set_result_add(text)

    def set_log_file_path(self, file_path):
        if file_path is not None:
            f = utl_dcc_objects.OsFile(file_path)
            f.create_directory()
            self._log_file_path = file_path

    def set_log_write(self, text):
        if hasattr(self, '_log_file_path'):
            if self._log_file_path is not None:
                with open(self._log_file_path, mode='a+') as log:
                    log.write(
                        u'{}\n'.format(text).encode('utf-8')
                    )
                #
                log.close()
    # help
    def show_help(self):
        self.set_current_unit('help_0')
        #
        if self.HELP_FILE_PATH is not None:
            self._help_text_browser.set_markdown_file_open(
                self.HELP_FILE_PATH
            )

    def set_help_content(self, text):
        if isinstance(text, six.string_types):
            self._help_text_browser.set_content(text)
        elif isinstance(text, (tuple, list)):
            self._help_text_browser.set_content(
                '\n'.join(text)
            )

    def set_help_file(self, file_path):
        self._help_text_browser.set_markdown_file_open(file_path)
    # exception
    def show_exception(self):
        self.set_current_unit('exception_0')

    def set_exception_content(self, text):
        if isinstance(text, six.string_types):
            self._exception_text_browser.set_content(text)
        elif isinstance(text, (tuple, list)):
            self._exception_text_browser.set_content(
                '\n'.join(text)
            )

    def show_message(self, text=None):
        self.set_current_unit('message_0')
        if text:
            self._message_text_browser.set_content(
                text
            )

    def set_exception_content_add(self, text):
        if isinstance(text, six.string_types):
            self._exception_text_browser.set_add(text)
        elif isinstance(text, (tuple, list)):
            self._exception_text_browser.set_add(
                '\n'.join(text)
            )

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # show unique
        if exclusive is True:
            gui_proxies = utl_gui_prx_core.get_gui_proxy_by_class(self.__class__)
            for i in gui_proxies:
                if hasattr(i, '_window_unicode_id'):
                    if i._window_unicode_id != self._window_unicode_id:
                        utl_core.Log.set_module_warning_trace(
                            'close exists window for "{}"'.format(
                                self.__class__.__name__
                            )
                        )
                        i.set_window_close()
        #
        if self._is_loading is True:
            utl_gui_qt_core.set_qt_window_show(
                self.widget, pos, size=(480, 160)
            )
        else:
            utl_gui_qt_core.set_qt_window_show(
                self.widget, pos, size=self.get_definition_window_size()
            )

    def set_print_add(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.set_print_add(text)

    def add_content_with_thread(self, text):
        text_browser = self.get_log_text_browser()
        text_browser.add_content_with_thread(text)

    def gui_waiting(self):
        return self._qt_widget._gui_waiting_()

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_widget._run_as_thread_(
            cache_fnc, build_fnc, post_fnc
        )


class PrxSessionWindow(PrxToolWindow):
    PRX_TYPE = 'session_window'
    DEFERRED_TIME = 1000
    def __init__(self, session, *args, **kwargs):
        super(PrxSessionWindow, self).__init__(*args, **kwargs)
        self._debug_run_(self._main_fnc_, session)
    @property
    def session(self):
        return self._session

    def _debug_run_(self, fnc, *args, **kwargs):
        # noinspection PyBroadException
        try:
            fnc(*args, **kwargs)
        except Exception as e:
            import sys

            import traceback

            exc_texts = []
            exc_type, exc_value, exc_stack = sys.exc_info()
            if exc_type:
                value = '{}: "{}"'.format(exc_type.__name__, exc_value.message)
                for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
                    i_file_path, i_line, i_fnc, i_fnc_line = stk
                    exc_texts.append(
                        '{indent}file "{file}" line {line} in {fnc}\n{indent}{indent}{fnc_line}'.format(
                            **dict(
                                indent='    ',
                                file=i_file_path,
                                line=i_line,
                                fnc=i_fnc,
                                fnc_line=i_fnc_line
                            )
                        )
                    )
                #
                self.show_exception()
                self.set_exception_content_add('traceback:')
                [self.set_exception_content_add(i) for i in exc_texts]
                self.set_exception_content_add(value)

    def _main_fnc_(self, *args, **kwargs):
        self._session = args[0]
        self._session.reload_configure()
        if self._session.get_is_td_enable() is True:
            self.set_window_title('[TD] {} for {}'.format(self._session.gui_configure.get('name'), str(self._session.application).capitalize()))
        elif self._session.get_is_beta_enable() is True:
            self.set_window_title('[BETA] {} for {}'.format(self._session.gui_configure.get('name'), str(self._session.application).capitalize()))
        else:
            self.set_window_title('{} for {}'.format(self._session.gui_configure.get('name'), str(self._session.application).capitalize()))
        #
        # print self._session.gui_configure.get('size')
        self.set_definition_window_size(self._session.gui_configure.get('size'))
        self._qt_thread_enable = bsc_core.EnvironMtd.get_qt_thread_enable()
        #
        self.set_loading_start(time=self.DEFERRED_TIME, method=self._setup_fnc_)

    def _setup_fnc_(self):
        self.restore_variants()
        self.set_all_setup()

    def _set_collapse_update_(self, collapse_dict):
        for i_k, i_v in collapse_dict.items():
            i_c = self._session.configure.get(
                'build.node_collapse.{}'.format(i_k)
            ) or []
            i_v.set_ports_collapse(i_c)

    def restore_variants(self):
        pass

    def set_all_setup(self):
        raise NotImplementedError()


class PrxSessionToolWindow(PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PrxSessionToolWindow, self).__init__(session, *args, **kwargs)

    def _setup_fnc_(self):
        self.restore_variants()
        #
        self._setup_ssn_tool_()
        self.set_all_setup()

    def apply_fnc(self):
        raise NotImplementedError()

    def apply_and_close_fnc(self):
        self.apply_fnc()
        self.set_window_close_later()

    def close_fnc(self):
        self.set_window_close_later()

    def _setup_ssn_tool_(self):
        self._ssn_tool_apply_and_close_button = PrxPressItem()
        self.set_button_add(self._ssn_tool_apply_and_close_button)
        self._ssn_tool_apply_and_close_button.set_name('Apply and Close')
        self._ssn_tool_apply_and_close_button.connect_press_clicked_to(
            self.apply_and_close_fnc
        )

        self._ssn_tool_apply_button = PrxPressItem()
        self.set_button_add(self._ssn_tool_apply_button)
        self._ssn_tool_apply_button.set_name('Apply')
        self._ssn_tool_apply_button.connect_press_clicked_to(
            self.apply_fnc
        )

        self._ssn_tool_close_button = PrxPressItem()
        self.set_button_add(self._ssn_tool_close_button)
        self._ssn_tool_close_button.set_name('Close')
        self._ssn_tool_close_button.connect_press_clicked_to(
            self.close_fnc
        )
        self._log_expand_bar.set_visible(False)

    def set_all_setup(self):
        raise NotImplementedError()


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
