# coding:utf-8
import platform as _platform

import pkgutil as _pkgutil
# qt
from ...qt.core.wrap import *

QT_USD_FLAG = False

__pypxr = _pkgutil.find_loader('pxr')

if __pypxr and QT_LOAD_INDEX == 1:
    if _platform.system() == 'Linux':
        QT_USD_FLAG = True

        from pxr import Usd, Sdf, Vt, Gf, Glf, Tf, Kind, UsdShade, UsdGeom, UsdLux

        from pxr import Usdviewq, UsdAppUtils, UsdImagingGL

