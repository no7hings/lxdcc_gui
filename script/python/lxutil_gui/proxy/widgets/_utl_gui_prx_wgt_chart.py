# coding:utf-8
from lxutil_gui.qt.widgets import _gui_qt_wgt_chart

from lxutil_gui.proxy import utl_gui_prx_abstract


class PrxSectorChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_chart.QtSectorChart
    def __init__(self, *args, **kwargs):
        super(PrxSectorChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxRadarChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_chart.QtRadarChart
    def __init__(self, *args, **kwargs):
        super(PrxRadarChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxPieChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_chart.QtPieChart
    def __init__(self, *args, **kwargs):
        super(PrxPieChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxHistogramChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_chart.QtHistogramChart
    def __init__(self, *args, **kwargs):
        super(PrxHistogramChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)

    def set_labels(self, labels):
        self.widget._set_labels_(labels)


class PrxSequenceChart(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_chart.QtSequenceChart
    def __init__(self, *args, **kwargs):
        super(PrxSequenceChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)

    def set_name(self, labels):
        self.widget._set_name_text_(labels)

    def set_name_width(self, w):
        self.widget._set_name_width_(w)

    def set_height(self, h):
        self.widget._set_height_(h)

    def set_menu_data(self, raw):
        self.widget._set_menu_data_(raw)

    def get_status(self):
        return self.widget._get_status_()

    def get_index_range(self):
        return self.widget._get_index_range_()

