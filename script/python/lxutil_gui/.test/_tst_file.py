# coding:utf-8

import lxutil.dcc.dcc_objects as utl_dcd_objects

p = '/data/f/texture-tx-test/v002/cloth_09.normal.1001.exr'

f = utl_dcd_objects.OsTexture(p)

print f._get_unit_tgt_ext_is_exists_(p, ext_tgt='.jpg')
