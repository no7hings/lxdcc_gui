# coding:utf-8
from lxgui.qt.warp import *

import pkgutil

QT_USD_FLAG = False

__pypxr = pkgutil.find_loader('pxr')

if __pypxr and QT_LOAD_INDEX == 1:
    QT_USD_FLAG = True

    from pxr import Usd, Sdf, Vt, Gf, Kind, UsdShade, UsdGeom, UsdLux

    from pxr import Usdviewq, UsdAppUtils, UsdImagingGL

