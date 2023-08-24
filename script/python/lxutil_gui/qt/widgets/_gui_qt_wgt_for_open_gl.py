# coding:utf-8
from lxutil_gui.qt.gui_qt_core import *

from lxusd import usd_core

from lxutil_gui.opengl import gui_ogl_core

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from pxr import UsdImagingGL

    from OpenGL import GL
except:
    pass


class QtGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, *args, **kwargs):
        super(QtGLWidget, self).__init__(*args, **kwargs)

        # self._file_path = '/production/library/resource/all/3d_plant_proxy/tree_g001_rsc/v0001/geometry/usd/tree_g001_rsc.usd'
        self._file_path = '/production/library/resource/all/3d_plant_proxy/grass_a001_rsc/v0001/geometry/usd/grass_a001_rsc.usd'
        # self._file_path = '/data/e/workspace/lynxi/script/python/.resources/asset/library/geo/sphere.usda'

        self._location = '/geometries'

        self._rgb = (0.043137254901960784, 0.10980392156862745, 0.011764705882352941)

        self._data = gui_ogl_core.GLUsdData(
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
