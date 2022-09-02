# coding:utf-8
from lxutil import utl_core

cmd = 'rez-env lxdcc -c "lxhook-engine -o \\\"application=maya&asset=td_test&file=/l/prod/cgm/work/assets/chr/td_test/srf/surfacing/maya/scenes/td_test.srf.surfacing.v006.ma&hook_engine=maya&open_file=True&option_hook_key=rsv-task-methods/asset/maya/gen-surface-validation&project=cgm&save_file=False&step=srf&task=surfacing&time_tag=2022_0829_1846_51_280277&user=dongchangbao&version=v006&with_geometry_check=True&with_geometry_topology_check=True&with_look_check=True&with_scene_check=True&with_shotgun_check=True&with_texture_check=True&with_texture_workspace_check=True&workspace=work\\\""'

# cmd = 'll \'/l/prod/cgm/publish/assets/chr/nn_4y/srf/surfacing/nn_4y.srf.surfacing.v050/texture/nn4y_bag_xiaohua.sheen_clr.1001.tx\''


def failed_fnc_(*args):
    print args


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtCore, QtWidgets

    #
    app = QtWidgets.QApplication(sys.argv)

    w, t = utl_core.CommandMonitor.set_create(
        'test', cmd
    )

    sys.exit(app.exec_())
