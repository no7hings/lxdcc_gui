# coding:utf-8
from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_split, _utl_gui_qt_wgt_view

from lxutil_gui.proxy import utl_gui_prx_abstract


class PrxHSplitter(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_split.QtHSplitter
    def __init__(self, *args, **kwargs):
        super(PrxHSplitter, self).__init__(*args, **kwargs)

    def add_widget(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self.widget._add_widget_(qt_widget)

    def set_stretches(self, values):
        self._qt_widget._set_stretch_factors_(values)

    def set_fixed_size_at(self, index, value):
        self._qt_widget._set_fixed_size_at_(index, value)

    def set_widget_hide_at(self, index):
        self._qt_widget._set_widget_hide_at_(index)

    def set_contract_left_or_top_at(self, index, size=None):
        self._qt_widget._set_contract_left_or_top_at_(index, size)

    def set_contract_right_or_bottom_at(self, index, size=None):
        self._qt_widget._set_contract_right_or_bottom_at_(index, size)

    def get_is_contracted_at(self, index):
        return self._qt_widget._get_is_contracted_at_(index)

    def set_swap_enable(self, boolean):
        self.widget._swap_enable = boolean

    def get_handle_at(self, index):
        return self._qt_widget._get_handle_at_(index)

    def set_window(self, widget):
        self._qt_widget._set_window_(widget)

    def set_width(self, value):
        self._qt_widget.setFixedWidth(value)


class PrxVSplitter(PrxHSplitter):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_split.QtVSplitter
    def __init__(self, *args, **kwargs):
        super(PrxVSplitter, self).__init__(*args, **kwargs)


class PrxTabView(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_view.QtTabView
    def __init__(self, *args, **kwargs):
        super(PrxTabView, self).__init__(*args, **kwargs)

    def set_item_add(self, widget, *args, **kwargs):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self.widget._set_item_add_(qt_widget, *args, **kwargs)

    def get_current_name(self):
        return self.widget._get_current_name_text_()

    def set_current_changed_connect_to(self, fnc):
        self.widget._set_item_current_changed_connect_to_(fnc)
