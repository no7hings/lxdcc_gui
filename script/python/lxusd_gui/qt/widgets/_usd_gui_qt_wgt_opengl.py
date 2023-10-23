# coding:utf-8
from lxgui.qt.core import *

import lxusd_gui.core as usd_gui_core

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from pxr import UsdImagingGL

    from OpenGL import GL

    class QtGLWidget(QtOpenGL.QGLWidget):
        def __init__(self, *args, **kwargs):
            super(QtGLWidget, self).__init__(*args, **kwargs)

            # self._file_path = '/production/library/resource/all/3d_plant_proxy/tree_g001_rsc/v0001/geometry/usd/tree_g001_rsc.usd'
            self._file_path = '/production/library/resource/all/3d_plant_proxy/grass_a001_rsc/v0001/geometry/usd/grass_a001_rsc.usd'
            # self._file_path = '/data/e/workspace/lynxi/script/python/.resources/asset/library/geo/sphere.usda'

            self._location = '/geometries'

            self._rgb = (0.043137254901960784, 0.10980392156862745, 0.011764705882352941)

            self._data = usd_gui_core.GuiGLUsdData(
                self._file_path,
                self._location,
                self._rgb,
            )

        def initializeGL(self):
            GL.glClearColor(0.0, 0.0, 0.0, 0.0)
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glDepthFunc(GL.GL_LESS)

            self._data.build_vbos()

        def resizeGL(self, w, h):
            GL.glViewport(0, 0, w, h)

        def paintGL(self):
            self._data.paint_vbo()

except Exception:
    class QtGLWidgetProxy(QtOpenGL.QGLWidget):
        def __init__(self, *args, **kwargs):
            super(QtGLWidgetProxy, self).__init__(*args, **kwargs)

