# coding:utf-8
import lxbasic.core as bsc_core
p = bsc_core.PyReloader(
    [
        'lxuniverse', 'lxresolver',
        'lxarnold', 'lxusd',
        'lxutil',
        'lxkatana', 'lxkatana_gui',
    ]
)
p.set_reload()

import lxkatana.dcc.dcc_objects as ktn_dcc_objects
#
exclude_paths = ktn_dcc_objects.Node('light_rigs').get_child_paths()

print exclude_paths
