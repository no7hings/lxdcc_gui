# coding:utf-8
import lxusd.scripts as usd_scripts

from lxutil import utl_core


def yes_fnc_():
    usd_scripts.ScpInstance.generate_grow_cache(
        '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/maya/scenes/usd/env_waterfall_002.usd',
        '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg',
        'st',
        '/data/e/workspace/lynxi/test/maya/vertex-color/test_grow_color_map.usd',
        w
    )


w = utl_core.DccDialog.create(
    'test',
    content='test',
    status=utl_core.DccDialog.ValidationStatus.Warning,
    #
    yes_label='Continue',
    yes_method=yes_fnc_,
    #
    no_visible=False, cancel_visible=False,
    use_exec=False,
    use_thread=False
)
