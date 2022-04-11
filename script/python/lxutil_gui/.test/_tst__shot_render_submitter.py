# coding:utf-8
from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

hook_option = 'file={}'.format('/l/prod/cgm/work/shots/z88/z88070/ani/animation/maya/scenes/z88070.ani.animation.v026.ma')

utl_gui_qt_core.set_window_show_standalone(
    utl_pnl_widgets.ShotRenderSubmitter, hook_option=hook_option
)
