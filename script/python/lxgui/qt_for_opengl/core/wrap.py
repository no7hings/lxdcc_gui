# coding:utf-8
import pkgutil

QT_OPENGL_FLAG = False

__pyopengl = pkgutil.find_loader('pxr')

if __pyopengl:
    QT_OPENGL_FLAG = True

    from OpenGL import GL, GLUT
