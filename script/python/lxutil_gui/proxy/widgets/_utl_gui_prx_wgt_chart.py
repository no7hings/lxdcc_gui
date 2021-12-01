# coding:utf-8
from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_chart

from lxutil_gui.proxy import utl_gui_prx_abstract


class PrxSectorChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_chart._QtSectorChart
    def __init__(self, *args, **kwargs):
        super(PrxSectorChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxRadarChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_chart._QtRadarChart
    def __init__(self, *args, **kwargs):
        super(PrxRadarChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxPieChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_chart._QtPieChart
    def __init__(self, *args, **kwargs):
        super(PrxPieChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxHistogramChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_chart._QtHistogramChart
    def __init__(self, *args, **kwargs):
        super(PrxHistogramChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)

    def set_labels(self, labels):
        self.widget._set_labels_(labels)

