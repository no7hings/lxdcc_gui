# coding:utf-8
from lxutil_gui.qt.gui_qt_core import *

from lxusd import usd_core

# noinspection PyBroadException
try:
    from OpenGL import GL
except:
    pass


class QtGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, *args, **kwargs):
        gl_format = QtOpenGL.QGLFormat()
        gl_format.setSampleBuffers(True)
        gl_format.setSamples(2)
        super(QtGLWidget, self).__init__(gl_format, *args, **kwargs)
        self.installEventFilter(self)
        self._translate_x = 0.0
        self._translate_y = 0.0
        self._translate_z = 0.0
        self._scale_factor = 1.0

        self._fov = 35
        self._aspect_ratio = 1.0
        self._near_clip, self._far_clip = 0.1, 100000

        self._x, self._y, self._z = 0, 0, 0
        self._w, self._h, self._d = 0, 0, 0
        self._c_x, self._c_y, self._c_z = 0, 0, 0

        self._dragActive = False
        self._cameraMode = "none"

        # self._file_path = '/production/library/resource/all/3d_plant_proxy/tree_g001_rsc/v0001/geometry/usd/tree_g001_rsc.usd'
        self._file_path = '/production/library/resource/all/3d_plant_proxy/yehua_a007_rsc/v0001/geometry/usd/yehua_a007_rsc.usd'

        self._location = '/geometries/mesh_001_002'

        self.__load_stage(
            self._file_path
        )
        # self.__load_stage(
        #     '/production/library/resource/all/3d_plant_proxy/tree_g001_rsc/v0001/geometry/usd/tree_g001_rsc.usd'
        # )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                x = event.x()*self.devicePixelRatioF()
                y = event.y()*self.devicePixelRatioF()

                if event.button() == QtCore.Qt.MidButton:
                    self._cameraMode = "truck"
                self._lastX = x
                self._lastY = y
            elif event.type() == QtCore.QEvent.Wheel:
                self._cameraMode = "zoom"
            elif event.type() == QtCore.QEvent.MouseMove:
                x = event.x()*self.devicePixelRatioF()
                y = event.y()*self.devicePixelRatioF()

                dx = x-self._lastX
                dy = y-self._lastY
                if dx == 0 and dy == 0:
                    return
                elif self._cameraMode == "truck":
                    self.__do_truck(x, y)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._cameraMode = "none"
                self._dragActive = False
        return False

    def __do_truck(self, x, y):
        self._translate_x, self._translate_y = x, y
        self.updateGL()

    def initializeGL(self):
        GL.glEnable(GL.GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        GL.glViewport(0, 0, w, h)
        self._aspect_ratio = w/h

    def __load_stage(self, file_path):
        from lxusd import usd_core

        self._stage_opt = usd_core.UsdStageOpt(
            file_path
        )

        (self._x, self._y, self._z), (self._c_x, self._c_y, self._c_z), (self._w, self._h, self._d) = self._stage_opt.get_geometry_args(self._location)
        self._scale_factor = 1.0/max(self._w, self._h)*2
        self._translate_x = -self._c_x*self._scale_factor
        self._translate_y = -self._c_y*self._scale_factor

    def __get_gl(self):
        return self.context().versionFunctions()

    def __calculate_project_matrix(self):
        m = QtGui.QMatrix4x4()
        m.perspective(self._fov, self._aspect_ratio, self._near_clip, self._far_clip)
        return m.data()

    def __draw_stage(self):
        for i_prim in usd_core.UsdPrimOpt(self._stage_opt.get_obj(self._location)).get_descendants(include_types=['Mesh']):
            self.__draw_mesh(i_prim)

        # self._save_image_('/data/f/image_render/test_1.jpg')

    def _save_image_(self, file_path, size=(512, 512)):
        from PIL import Image
        print Image.__file__

        c_w, c_h = size
        image_data = GL.glReadPixels(0, 0, c_w, c_h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)

        image = Image.frombytes('RGBA', (c_w, c_h), image_data)

        image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(file_path)

    def __draw_mesh(self, prim):
        mesh_opt = usd_core.UsdMeshOpt(usd_core.UsdGeom.Mesh(prim))
        face_vertex_counts, face_vertex_indices = mesh_opt.get_face_vertices()
        points = mesh_opt.get_points()
        index_cur = 0
        for i_count in face_vertex_counts:
            i_indices = face_vertex_indices[index_cur:index_cur+i_count]
            GL.glBegin(GL.GL_POLYGON)
            GL.glColor3f(1, 0, 0)
            for j_index in i_indices:
                j_point = points[j_index]
                j_x, j_y, j_z = j_point
                i_d = 1.0-abs((j_z-self._c_z)+self._d/2)/self._d
                GL.glColor3f(i_d, i_d, i_d)
                GL.glVertex3f(j_x, j_y, j_z)
            index_cur += i_count
            GL.glEnd()

    def paintGL(self):
        from OpenGL.GL.EXT.framebuffer_sRGB import GL_FRAMEBUFFER_SRGB_EXT

        GL.glEnable(GL_FRAMEBUFFER_SRGB_EXT)

        GL.glClearColor(0, 0, 0, 0)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)

        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        GL.glLoadIdentity()
        GL.glTranslatef(self._translate_x, self._translate_y, self._translate_z)
        GL.glScaled(self._scale_factor, self._scale_factor, self._scale_factor)

        self.__draw_stage()
