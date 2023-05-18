# coding:utf-8
import fnmatch

import time

import lxutil_gui.proxy.widgets as utl_prx_widgets

import lxresolver.commands as rsv_commands

import lxutil.dcc.dcc_objects as utl_dcc_objects


class TestWindow(utl_prx_widgets.PrxDialogWindow0):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([640, 640])
        self._test_shotgun_entity_()
        self._test_shotgun_entities_()
        # self._test_()

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        return fnmatch.filter(
            ['test'], '*{}*'.format(args[0])
        )

    def _test_capsule_(self):
        n = self.get_options_node()
        n.set_visible(True)
        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsCapsuleString(
                'test_capsule_string'
            )
        )
        p.set_option(
            ['model', 'groom', 'rig', 'effect', 'surface']
        )
        p.set('model')

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsButton(
                'test_capsule_string_button'
            )
        )

        p.set(
            lambda: self._test_print_('test_capsule_string')
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsCapsuleStrings(
                'test_capsule_strings'
            )
        )
        p.set_option(
            ['model', 'groom', 'rig', 'effect', 'surface']
        )
        p.set(
            ['model', 'groom']
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsButton(
                'test_capsule_strings_button'
            )
        )

        p.set(
            lambda: self._test_print_('test_capsule_strings')
        )

    def _test_print_(self, key):
        print self.get_options_node().get(key)

    def _test_components_(self):
        n = self.get_options_node()
        n.set_visible(True)
        p = n.set_port_add(
            utl_prx_widgets.PrxNodeTreeViewPort(
                'test_components'
            )
        )
        p.set(
            [
                utl_dcc_objects.Obj(i, icon_name='obj/renderable') for i in [
                    '/master/mod/hi',
                    '/master/mod/lo',
                    '/master/hair',
                    '/master/plant',
                    '/master/light'
                ]
            ]+[
                utl_dcc_objects.Obj(i, icon_name='obj/non-renderable') for i in [
                    '/master/grm',
                    '/master/cfx',
                    '/master/efx',
                    '/master/misc'
                ]
            ]
        )

    def _test_shotgun_entity_(self):
        n = self.get_options_node()
        n.set_visible(True)
        # self.set_widget_add(n)
        import lxshotgun.objects as stg_objects

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsShotgunEntity(
                'test_shotgun_user'
            )
        )
        p.set_shotgun_entity_kwargs(
            {
                'entity_type': 'HumanUser',
                'filters': [['sg_studio', 'is', 'CG'], ['sg_status_list', 'is', 'act']],
                'fields': ['name', 'email', 'sg_nickname'],
            },
            keyword_filter_fields=['name', 'email', 'sg_nickname'],
            tag_filter_fields=['department']
        )

    def _test_shotgun_entities_(self):
        n = self.get_options_node()
        n.set_visible(True)
        # self.set_widget_add(n)
        import lxshotgun.objects as stg_objects

        c = stg_objects.StgConnector()

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsShotgunEntities(
                'test_shotgun_users'
            )
        )
        p.set_shotgun_entity_kwargs(
            {
                'entity_type': 'HumanUser',
                'filters': [['sg_studio', 'is', 'CG'], ['sg_status_list', 'is', 'act']],
                'fields': ['name', 'email', 'sg_nickname'],
            },
            keyword_filter_fields=['name', 'email', 'sg_nickname'],
            tag_filter_fields=['department']
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsShotgunEntities(
                'test_shotgun_assets'
            )
        )
        p.set_shotgun_entity_kwargs(
            {
                'entity_type': 'Asset',
                'filters': [
                    ['project', 'is', c.get_stg_project(project='nsa_dev')]
                ],
                'fields': ['sg_chinese_name', 'code'],
            },
            name_field='code',
            keyword_filter_fields=['sg_chinese_name', 'code'],
            tag_filter_fields=['sg_asset_type'],
        )
        #
        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsShotgunEntities(
                'test_shotgun_tasks'
            )
        )
        p.set_shotgun_entity_kwargs(
            {
                'entity_type': 'Task',
                'filters': [
                    ['project', 'is', c.get_stg_project(project='nsa_dev')],
                    ['entity', 'is', c.get_stg_resource(project='nsa_dev', asset='td_test')]
                ],
                'fields': ['content'],
            },
            name_field='content',
            keyword_filter_fields=['content'],
            tag_filter_fields=['step'],
        )

    def _test_file_list_and_tree_(self):
        n = self.get_options_node()
        n.set_visible(True)
        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsFileList(
                'test_file_list'
            )
        )
        p.set(
            [u'/production/shows/nsa_dev/assets/oth/surface_workspace/user/team.srf/katana/scenes/surfacing/surface_workspace.srf.surfacing.v000_001.katana']
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsFileTree(
                'test_file_tree'
            )
        )
        p.set_root(
            '/production/shows/nsa_dev/assets/oth/surface_workspace/user/team.srf/katana/scenes'
        )
        p.set(
            [
                u'/production/shows/nsa_dev/assets/oth/surface_workspace/user/team.srf/katana/scenes/surfacing/surface_workspace.srf.surfacing.v000_001.katana',
                u'/production/shows/nsa_dev/assets/oth/surface_workspace/user/team.srf/katana/scenes/surfacing/surface_workspace.srf.surfacing.v000_002.katana'
            ]
        )

    def _test_(self):
        n = self.get_options_node()

        p = n.set_port_add(
            utl_prx_widgets.PrxMediasOpenPort(
                'test_medias_open'
            )
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxDirectoriesOpenPort(
                'test_directories_open'
            )
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxDirectoryOpenPort(
                'test_directory_open'
            )
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsScript(
                'test_script'
            )
        )

        p = n.set_port_add(
            utl_prx_widgets.PrxPortAsEnumerate(
                'text_enumerate'
            )
        )

        p.set(
            ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        )


if __name__ == '__main__':
    import time
    import sys
    #
    import PySide2
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()

    # c = 2
    # c2 = 20
    # with w.set_progress_create(maximum=c) as p:
    #     for i in range(c):
    #         p.set_update()
    #         time.sleep(1)
    #         with w.set_progress_create(maximum=c2) as p2:
    #             for j in range(c2):
    #                 time.sleep(1)
    #                 p2.set_update()

    #
    sys.exit(app.exec_())
