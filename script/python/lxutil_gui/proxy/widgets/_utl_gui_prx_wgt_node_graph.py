# coding:utf-8
from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_view, _utl_gui_qt_wgt_item, _utl_gui_qt_wgt_node_graph

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility


class PrxNodeGraph(
    utl_gui_prx_abstract.AbsPrxWidget
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_node_graph._QtNGGraph
    def __init__(self, *args, **kwargs):
        super(PrxNodeGraph, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(2, 2, 2, 2)
        self._qt_layout_0.setSpacing(2)
        self._prx_tool_bar_0 = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_tool_bar_0.widget)
        self._prx_tool_bar_0.set_border_radius(4)
        #
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_tool_bar_0.set_widget_add(self._prx_filer_bar_0)
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
        self._qt_view._set_ng_graph_node_create_(*args, **kwargs)

    def set_node_universe(self, universe):
        self._qt_view._set_ng_graph_universe_(universe)

    def set_node_show(self, obj_path=None):
        self._qt_view._set_ng_graph_node_show_(obj_path)
