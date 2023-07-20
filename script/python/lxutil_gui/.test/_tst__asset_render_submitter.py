# coding:utf-8
from lxbasic import bsc_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

bsc_core.EnvExtraMtd.set_td_enable(True)

# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v006.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y_test/srf/surfacing/katana/nn_14y_test.srf.surfacing.v045.td_render.katana')
hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/srf/surfacing/katana/nn_4y_test.srf.surfacing.v111.katana')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/mod/modeling/maya/scenes/nn_4y_test.mod.modeling.v053.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/mod/modeling/maya/scenes/nn_4y_test.mod.modeling.v066.td.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y/mod/modeling/maya/scenes/nn_14y.mod.modeling.v013.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/rig/rigging/maya/scenes/nn_4y_test.rig.rigging.v111.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/grm/groom/maya/scenes/nn_4y_test.grm.groom.v103.ma')

utl_gui_qt_core.show_prx_window_auto(
    utl_pnl_widgets.AssetRenderSubmitter, hook_option=hook_option
)
