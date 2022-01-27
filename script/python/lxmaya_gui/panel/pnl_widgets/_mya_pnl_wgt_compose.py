# coding:utf-8
from lxutil import utl_configure

from lxutil_prd import utl_prd_commands

from lxutil_gui.panel import utl_gui_pnl_abstract

from lxmaya_prd.ma_prd_objects import _mya_prd_obj_utility

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_utility, _mya_dcc_obj_obj, _mya_dcc_obj_objs


class SceneComposePanel(utl_gui_pnl_abstract.AbsSceneComposeToolPanel):
    HELP_FILE_PATH = '{}/maya/validation_tool.md'.format(utl_configure.Root.DATA)
    DCC_SELECTION_CLS = _mya_dcc_obj_utility.Selection
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Node
    #
    OBJ_OP_CLASS = _mya_prd_obj_utility.ObjOpt
    OP_REFERENCE_OBJ_CLASS = _mya_prd_obj_utility.ObjReferenceOp
    def __init__(self, *args, **kwargs):
        file_path = _mya_dcc_obj_utility.SceneFile.get_current_file_path()
        s = utl_prd_commands.set_scene_load_from_scene(file_path)
        reference_raw = _mya_dcc_obj_objs.References().get_reference_raw()
        s.set_load_by_reference_file_paths(reference_raw)
        super(SceneComposePanel, self).__init__(s, *args, **kwargs)
