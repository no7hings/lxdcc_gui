# coding:utf-8
from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v006.ma')

utl_gui_qt_core.set_window_show_standalone(
    utl_pnl_widgets.AssetRenderSubmitter, option=hook_option
)
