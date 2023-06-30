# coding:utf-8
from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_for_usd

from lxutil_gui.proxy import utl_gui_prx_abstract


class PrxUsdStageViewProxy(
    utl_gui_prx_abstract.AbsPrxWidget
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_utility._QtTranslucentWidget
    def __init__(self, *args, **kwargs):
        super(PrxUsdStageViewProxy, self).__init__(*args, **kwargs)

    def get_usd_stage(self):
        pass

    def refresh_usd_view_draw(self):
        pass

    def refresh_usd_stage_for_texture_preview(self, *args, **kwargs):
        pass

    def refresh_usd_stage_for_asset_preview(self, *args, **kwargs):
        pass

    def refresh_usd_stage_for_texture_render(self, *args, **kwargs):
        pass

    def refresh_usd_stage_for_asset_render(self, *args, **kwargs):
        pass


class PrxUsdStageView(
    utl_gui_prx_abstract.AbsPrxWidget,
):
    if utl_gui_qt_core.LOAD_INDEX == 0:
        QT_WIDGET_CLS = _utl_gui_qt_wgt_for_usd.QtUsdStageWidgetProxy
    else:
        QT_WIDGET_CLS = _utl_gui_qt_wgt_for_usd.QtUsdStageWidget
    #
    def __init__(self, *args, **kwargs):
        super(PrxUsdStageView, self).__init__(*args, **kwargs)

    def get_usd_stage(self):
        return self._qt_widget._get_usd_stage_()

    def refresh_usd_view_draw(self):
        self._qt_widget._refresh_usd_view_draw_()

    def refresh_usd_stage_for_texture_preview(self, *args, **kwargs):
        self._qt_widget._refresh_usd_stage_for_texture_preview_(
            *args, **kwargs
        )

    def refresh_usd_stage_for_asset_preview(self, *args, **kwargs):
        self._qt_widget._refresh_usd_stage_for_asset_preview_(
            *args, **kwargs
        )

    def refresh_usd_stage_for_texture_render(self, *args, **kwargs):
        self._qt_widget._refresh_usd_stage_for_texture_render_(
            *args, **kwargs
        )

    def refresh_usd_stage_for_asset_render(self, *args, **kwargs):
        self._qt_widget._refresh_usd_stage_for_asset_render_(
            *args, **kwargs
        )