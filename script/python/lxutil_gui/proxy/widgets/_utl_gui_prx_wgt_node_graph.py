# coding:utf-8
from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_view, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_node_graph

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_view


class PrxNGGraph(
    utl_gui_prx_abstract.AbsPrxWidget
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_node_graph._QtNGGraph
    def __init__(self, *args, **kwargs):
        super(PrxNGGraph, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(2, 2, 2, 2)
        self._qt_layout_0.setSpacing(2)
        self._prx_h_tool_bar = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_h_tool_bar.widget)
        self._prx_h_tool_bar.set_border_radius(1)
        #
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_h_tool_bar.set_widget_add(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLASS()
        self._qt_layout_0.addWidget(self._qt_view)
        #
        self._prx_filter_bar = self._prx_filer_bar_0
    @property
    def view(self):
        return self._qt_view
    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def set_node_add(self, *args, **kwargs):
        self._qt_view._set_ng_graph_sbj_node_create_(*args, **kwargs)

    def set_universe(self, universe):
        self._qt_view._set_ng_universe_(universe)

    def set_node_show(self, obj_path=None):
        self._qt_view._set_ng_show_by_universe_(obj_path)


class PrxNGTree(
    utl_gui_prx_abstract.AbsPrxWidget
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_node_graph._QtNGTree
    def __init__(self, *args, **kwargs):
        super(PrxNGTree, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        self._prx_h_tool_bar = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_h_tool_bar.widget)
        self._prx_h_tool_bar.set_border_radius(1)
        #
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_h_tool_bar.set_widget_add(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLASS()
        self._qt_layout_0.addWidget(self._qt_view)
        #
        self._prx_filter_bar = self._prx_filer_bar_0

        self._qt_view._set_view_header_(
            [('name', 4)], 320
        )

    def set_universe(self, universe):
        self._qt_view._set_ng_universe_(universe)

    def _set_items_hidden_by_keyword_filter_(self):
        pass


class PrxNGImageGraph(
    utl_gui_prx_abstract.AbsPrxWidget
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_node_graph._QtNGImageGraph
    def __init__(self, *args, **kwargs):
        super(PrxNGImageGraph, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        self._prx_h_tool_bar = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_h_tool_bar.widget)
        self._prx_h_tool_bar.set_border_radius(1)
        #
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_h_tool_bar.set_widget_add(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLASS()
        self._qt_layout_0.addWidget(self._qt_view)
        #
        self._prx_filter_bar = self._prx_filer_bar_0
    @property
    def view(self):
        return self._qt_view
    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def set_node_add(self, *args, **kwargs):
        self._qt_view._set_ng_graph_sbj_node_create_(*args, **kwargs)

    def set_restore(self):
        self._qt_view._set_restore_()

    def set_clear(self):
        self._qt_view._set_clear_()

    def set_universe(self, universe):
        self._qt_view._set_ng_universe_(universe)

    def set_node_show(self, obj_path=None):
        self._qt_view._set_ng_show_by_universe_(obj_path)

    def set_graph_save_to(self, file_path):
        self._qt_view._set_ng_graph_image_save_to_(file_path)
