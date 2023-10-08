# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxuniverse', 'lxresolver',
        'lxarnold', 'lxusd',
        'lxutil', 'lxutil_fnc', 'lxutil_gui',
        'lxkatana', 'lxkatana_fnc', 'lxkatana_gui',
    ]
)
p.set_reload()

from lxkatana_gui.panel import pnl_widgets

w = pnl_widgets.SceneMethodRunnerPanel()

w.set_window_show()
