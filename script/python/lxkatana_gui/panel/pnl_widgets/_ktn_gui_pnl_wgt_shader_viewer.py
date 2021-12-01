# coding:utf-8
from lxutil_gui.panel import utl_gui_pnl_abs_shader_viewer

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxkatana.fnc.importers as ktn_fnc_importers


class SceneShaderViewerPanel(utl_gui_pnl_abs_shader_viewer.AbsSceneShaderViewerPanel):
    DCC_SCENE_CLASS = ktn_dcc_objects.Scene
    DCC_FNC_LOOK_IMPORTER_CLASS = ktn_fnc_importers.LookAssImporter
    #
    DCC_MATERIALS_CLS = ktn_dcc_objects.Materials
    DCC_SHADER_CLS = ktn_dcc_objects.AndShader
    #
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(SceneShaderViewerPanel, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    import lxkatana
    lxkatana.set_reload()
    #
    import lxkatana_gui.panel.pnl_widgets as ktn_pnl_widgets
    w = ktn_pnl_widgets.SceneShaderViewerPanel()
    w.set_window_show()
