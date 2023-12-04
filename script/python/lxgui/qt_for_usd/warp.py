# coding:utf-8
import platform

from lxgui.qt.wrap import *

import pkgutil

QT_USD_FLAG = False

__pypxr = pkgutil.find_loader('pxr')

if __pypxr and QT_LOAD_INDEX == 1:
    if platform.system() == 'Linux':
        QT_USD_FLAG = True

        from pxr import Usd, Sdf, Vt, Gf, Glf, Tf, Kind, UsdShade, UsdGeom, UsdLux

        from pxr import Usdviewq, UsdAppUtils, UsdImagingGL

