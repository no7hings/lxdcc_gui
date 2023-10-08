# coding:utf-8
import time

import lxutil_gui.proxy.widgets as utl_prx_widgets

import lxresolver.commands as rsv_commands


class TestWindow(utl_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([640, 640])
        self._test_()

    def _test_(self):
        f = utl_prx_widgets.PrxFilterBar()
        f.set_history_key('filter.test')
        self.add_widget(f)
        n = utl_prx_widgets.PrxNode_('root')
        self.add_widget(n)
        p = n.add_port(
            utl_prx_widgets.PrxPortAsConstantChoose(
                'test_enumerate'
            )
        )
        p.set(['a', 'b'])
        p = n.add_port(
            utl_prx_widgets.PrxPortAsDirectorySave(
                'test_directory_save'
            )
        )
        p = n.add_port(
            utl_prx_widgets.PrxPortForFloatTuple(
                'test_float_array'
            )
        )
        p = n.add_port(
            utl_prx_widgets.PrxPortAsFilesOpen(
                'test_files_open'
            )
        )
        p.set_history_key('filter.test-files')
        p.set(
            ['/home/dongchangbao/Desktop/app-kit.desktop']
        )
        p.set_use_enable(True)
        p = n.add_port(
            utl_prx_widgets.PrxPortAsDirectoriesOpen(
                'test_directories_open'
            )
        )

        p = n.add_port(
            utl_prx_widgets.PrxPortAsMediasOpen(
                'test_medias_open'
            )
        )

        p = n.add_port(
            utl_prx_widgets.PrxPortAsScript(
                'test_script'
            )
        )

        p = n.add_port(
            utl_prx_widgets.PrxPortAsRgbaChoose(
                'test_rgb'
            )
        )
        # p.set(
        #     '/l/temp/td/dongchangbao/texture_manager'
        # )


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
