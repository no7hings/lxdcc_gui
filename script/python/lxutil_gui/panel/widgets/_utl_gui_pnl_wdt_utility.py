# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

from lxutil_gui.panel import utl_gui_pnl_abs_utility, utl_gui_pnl_abs_render_submitter, utl_gui_pnl_abs_node_graph


class FncPanel(utl_gui_pnl_abs_utility.AbsFncPanel):
    def __init__(self, file_path=None, *args, **kwargs):
        super(FncPanel, self).__init__(file_path, *args, **kwargs)


class PnlRsvUnitLoader(utl_gui_pnl_abstracts.AbsPnlRsvUnitLoader):
    def __init__(self, session, *args, **kwargs):
        super(PnlRsvUnitLoader, self).__init__(session, *args, **kwargs)


class AssetRenderSubmitter(utl_gui_pnl_abs_render_submitter.AbsAssetRenderSubmitterPanel):
    OPTION_HOOK_KEY = 'tool-panels/asset-render-submitter'

    def __init__(self, hook_option=None, *args, **kwargs):
        super(AssetRenderSubmitter, self).__init__(hook_option, *args, **kwargs)


class ShotRenderSubmitter(utl_gui_pnl_abs_render_submitter.AbsShotRenderSubmitterPanel):
    OPTION_HOOK_KEY = 'tool-panels/shot-render-submitter'

    def __init__(self, hook_option=None, *args, **kwargs):
        super(ShotRenderSubmitter, self).__init__(hook_option, *args, **kwargs)


class RezGraph(utl_gui_pnl_abs_node_graph.AbsRezGraph):
    OPTION_HOOK_KEY = 'tool-panels/rez-graph'

    def __init__(self, hook_option=None, *args, **kwargs):
        super(RezGraph, self).__init__(hook_option, *args, **kwargs)


class AssetLineup(utl_gui_pnl_abs_node_graph.AbsAssetLineup):
    OPTION_HOOK_KEY = 'tool-panels/asset-lineup'

    def __init__(self, session, *args, **kwargs):
        super(AssetLineup, self).__init__(session, *args, **kwargs)


class ComparerOpt(utl_gui_pnl_abstracts.AbsDccComparerOpt):
    DCC_NAMESPACE = 'lynxi'
    DCC_NODE_CLS = utl_dcc_objects.Obj
    DCC_COMPONENT_CLS = utl_dcc_objects.Component
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = '/'

    def __init__(self, *args, **kwargs):
        super(ComparerOpt, self).__init__(*args, **kwargs)


class PnlAssetDccGeometryComparer(utl_gui_pnl_abstracts.AbsPnlAssetGeometryComparer):
    DCC_COMPARER_OPT_CLS = ComparerOpt

    def __init__(self, session, *args, **kwargs):
        super(PnlAssetDccGeometryComparer, self).__init__(session, *args, **kwargs)
