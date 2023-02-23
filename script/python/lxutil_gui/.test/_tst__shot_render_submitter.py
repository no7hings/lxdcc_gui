# coding:utf-8
from lxbasic import bsc_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

bsc_core.EnvExtraMtd.set_td_enable(True)

# hook_option = 'file={}'.format('/l/prod/cgm/work/shots/z88/z88070/ani/animation/maya/scenes/z88070.ani.animation.v026.ma')
hook_option = 'file={}'.format('/l/prod/xkt/work/shots/z88/z88010/efx/effects/houdini/z88010.efx.effects.v032.hip')
# hook_option = 'file={}'.format('/l/prod/xkt/work/shots/z88/z88100/cfx/hair/houdini/z88100.cfx.hair.v010.hip')

utl_gui_qt_core.set_window_show_standalone(
    utl_pnl_widgets.ShotRenderSubmitter, hook_option=hook_option
)
