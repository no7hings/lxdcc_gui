# coding:utf-8
from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_view

from lxutil_gui.proxy import utl_gui_prx_abstract


class PrxHSplitter(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view._QtHSplitter
    def __init__(self, *args, **kwargs):
        super(PrxHSplitter, self).__init__(*args, **kwargs)

    def set_widget_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self.widget.addWidget(qt_widget)

    def set_stretches(self, stretches):
        for seq, i in enumerate(stretches):
            self.widget._set_stretch_factor_(seq, i)

    def set_widget_hide_at(self, index):
        self._qt_widget._set_widget_hide_at_(index)

    def set_sizes(self, sizes):
        self.widget._set_sizes_(sizes)

    def set_swap_enable(self, boolean):
        self.widget._swap_enable = boolean

    def get_handle_at(self, index):
        return self._qt_widget._get_handle_at_(index)


class PrxVSplitter(PrxHSplitter):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view._QtVSplitter
    def __init__(self, *args, **kwargs):
        super(PrxVSplitter, self).__init__(*args, **kwargs)


class PrxTabView(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view.QtTabView
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


class AbsPrxViewDef(object):
    @property
    def view(self):
        raise NotImplementedError()
    #
    def set_item_select_changed_connect_to(self, fnc):
        self.view.itemSelectionChanged.connect(fnc)
    # select
    def _get_selected_items_(self):
        return self.view.selectedItems()

    def get_selected_items(self):
        return [i.gui_proxy for i in self._get_selected_items_()]


class PrxGuideBar(
    utl_gui_prx_abstract.AbsPrxWidget,
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view._QtGuideBar
    def __init__(self, *args, **kwargs):
        super(PrxGuideBar, self).__init__(*args, **kwargs)

    def set_path_args(self, path_args):
        self.widget._set_view_path_args_(path_args)

    def set_item_contents_at(self, content, index=0):
        self.widget._set_guide_choose_item_content_at_(content, index)

    def get_current_path(self):
        return self.widget._get_view_guide_current_path_()

    def set_item_clicked_connect_to(self, fnc):
        self.widget.guide_item_press_clicked.connect(fnc)

    def set_item_double_clicked_connect_to(self, fnc):
        self.widget.guide_item_double_clicked.connect(fnc)

    def set_item_changed_connect_to(self, fnc):
        self.widget.choose_item_changed.connect(fnc)

    def set_clear(self):
        self.widget._set_view_guide_and_choose_clear_()
