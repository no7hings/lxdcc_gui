# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxkatana.fnc.importers as ktn_fnc_importers


class PnlShaderViewer(utl_gui_pnl_abstracts.AbsPnlShaderViewer):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()
import lxsession.commands as ssn_commands; ssn_commands.set_hook_execute("dcc-tools/katana/shader-viewer")
    """
    DCC_SCENE_CLASS = ktn_dcc_objects.Scene
    DCC_FNC_LOOK_IMPORTER_CLASS = ktn_fnc_importers.LookAssImporter
    #
    DCC_MATERIALS_CLS = ktn_dcc_objects.Materials
    DCC_SHADER_CLS = ktn_dcc_objects.AndShader
    #
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    def __init__(self, *args, **kwargs):
        super(PnlShaderViewer, self).__init__(*args, **kwargs)
