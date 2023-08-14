# coding:utf-8
import sys
import random

from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PySide2.QtGui import QColor

from OpenGL import GL


class OpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

        self._count = 5
        self._data = []

        for _ in range(self._count):
            num_vertices = random.randint(3, 8)
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            for _ in range(num_vertices):
                x = random.uniform(-1.0, 1.0)
                y = random.uniform(-1.0, 1.0)
                z = random.uniform(-1.0, 1.0)
                self._data.extend([x, y, z, color.redF(), color.greenF(), color.blueF()])

        self._vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(self._data) * 4, (GL.GLfloat * len(self._data))(*self._data), GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        GL.glEnable(GL.GL_DEPTH_TEST)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo)
        GL.glVertexPointer(3, GL.GL_FLOAT, 6 * 4, GL.ctypes.c_void_p(0))
        GL.glColorPointer(3, GL.GL_FLOAT, 6 * 4, GL.ctypes.c_void_p(3 * 4))

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        aspect_ratio = self.width() / self.height()
        GL.glOrtho(-1.5 * aspect_ratio, 1.5 * aspect_ratio, -1.5, 1.5, -10, 10)  # Adjust these values as needed

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        # gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)  # Adjust the camera position

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._count * 3)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL.glDisableClientState(GL.GL_COLOR_ARRAY)

        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("OpenGL 3D Polygon Drawing")
        self.setGeometry(100, 100, 800, 600)

        self.opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())