# coding:utf-8
from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

hook_option = 'file={}'.format('/l/prod/xkt/work/shots/z88/z88010/rlo/rough_layout/maya/scenes/z88010.rlo.rough_layout.v001.ma')

utl_gui_qt_core.set_window_show_standalone(
    utl_pnl_widgets.ShotRenderSubmitter, hook_option=hook_option
)
