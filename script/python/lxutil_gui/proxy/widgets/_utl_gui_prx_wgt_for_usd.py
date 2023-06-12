# coding:utf-8
from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_for_usd

from lxutil_gui.proxy import utl_gui_prx_abstract


class PrxUsdStageView(
    utl_gui_prx_abstract.AbsPrxWidget,
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_for_usd.QtUsdStageWidget
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

