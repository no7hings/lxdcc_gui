# coding:utf-8
import lxkit.core as kit_core

s, e = kit_core.KitDesktopHook.get_args(
    'BUILTIN/main'
)
e()
