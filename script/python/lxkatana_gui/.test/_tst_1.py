# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxuniverse', 'lxresolver',
        'lxarnold', 'lxusd',
        'lxutil', 'lxutil_fnc', 'lxutil_gui',
        'lxkatana', 'lxkatana_fnc', 'lxkatana_gui',
    ]
)
p.set_reload()

import lxkatana.dcc.dcc_objects as ktn_dcc_objects
#
exclude_paths = ktn_dcc_objects.Node('light_rigs').get_child_paths()

print exclude_paths
