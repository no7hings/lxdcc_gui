# coding:utf-8
import fnmatch

import time

import lxutil_gui.proxy.widgets as utl_prx_widgets

import lxresolver.commands as rsv_commands

import lxutil.dcc.dcc_objects as utl_dcc_objects


class TestWindow(utl_prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([640, 640])
        self._test_capsule_()

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        return fnmatch.filter(
            ['test'], '*{}*'.format(args[0])
        )

    def _test_capsule_(self):
        self._n = utl_prx_widgets.PrxNode_('options')
        self.set_widget_add(self._n)
        p = self._n.set_port_add(
            utl_prx_widgets.PrxPortAsCapsuleString(
                'test_capsule_string'
            )
        )
        p.set_option(
            ['model', 'groom', 'rig', 'effect', 'surface']
        )
        p.set('model')

        p = self._n.set_port_add(
            utl_prx_widgets.PrxPortAsButton(
                'test_capsule_string_button'
            )
        )

        p.set(
            lambda: self._test_print_('test_capsule_string')
        )

        p = self._n.set_port_add(
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

        p = self._n.set_port_add(
            utl_prx_widgets.PrxPortAsButton(
                'test_capsule_strings_button'
            )
        )

        p.set(
            lambda: self._test_print_('test_capsule_strings')
        )

    def _test_print_(self, key):
        print self._n.get(key)

    def _test_components_(self):
        self._n = utl_prx_widgets.PrxNode_('options')
        self.set_widget_add(self._n)
        p = self._n.set_port_add(
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
    def _test_(self):
        f = utl_prx_widgets.PrxFilterBar()
        f.set_history_key('filter.test')
        self.set_widget_add(f)

        f.set_filter_completion_gain_fnc(self._value_completion_gain_fnc_)
        n = utl_prx_widgets.PrxNode_('options')
        self.set_widget_add(n)
        p = n.set_port_add(
            utl_prx_widgets.PrxPortForShotgunEntitiesAsChoose(
                'test_shotgun_entities'
            )
        )
        p.set_shotgun_entity_kwargs(
            {
                'entity_type': 'HumanUser',
                'filters': [['sg_studio', 'is', 'CG'], ['sg_status_list', 'is', 'act']],
                'fields': ['sg_nickname', 'email', 'name'],
             },
            keyword_filter_fields=['sg_nickname', 'email', 'name'],
            tag_filter_fields=['department']
        )
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
