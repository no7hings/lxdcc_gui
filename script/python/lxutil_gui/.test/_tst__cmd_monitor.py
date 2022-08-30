# coding:utf-8
from lxutil import utl_core

cmd = 'rez-env lxdcc -c "lxhook-engine -o \\\"application=maya&asset=td_test&file=/l/prod/cgm/work/assets/chr/td_test/srf/surfacing/maya/scenes/td_test.srf.surfacing.v006.ma&hook_engine=maya&open_file=True&option_hook_key=rsv-task-methods/asset/maya/gen-surface-validation&project=cgm&save_file=False&step=srf&task=surfacing&time_tag=2022_0829_1846_51_280277&user=dongchangbao&version=v006&with_geometry_check=True&with_geometry_topology_check=True&with_look_check=True&with_scene_check=True&with_shotgun_check=True&with_texture_check=True&with_texture_workspace_check=True&workspace=work\\\""'


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtCore, QtWidgets

    #
    app = QtWidgets.QApplication(sys.argv)

    utl_core.CmdMonitor.set_create(
        'test', cmd
    )

    sys.exit(app.exec_())
