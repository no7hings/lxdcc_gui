# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxuniverse', 'lxresolver',
        'lxarnold', 'lxusd',
        'lxutil', 'lxutil_fnc', 'lxutil_gui',
        'lxmaya', 'lxmaya_fnc', 'lxmaya_gui'
    ]
)
p.set_reload()

from lxmaya_gui.panel import pnl_widgets; w = pnl_widgets.SceneMethodRunnerPanel(); w.set_window_show()


